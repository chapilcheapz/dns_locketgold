"""
DOH Server - Locket Gold Pipeline
"""

import os
import struct
import socket
import base64
import asyncio
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Locket Gold DOH Server")

# === UPSTREAM DNS ===
UPSTREAM_DOH = "https://cloudflare-dns.com/dns-query"

# === DOMAIN RULES (từ module [Rule]) ===
# Trả về NXDOMAIN / 0.0.0.0 cho các domain này
BLOCKED_DOMAINS = {
    "ocsp.apple.com",
    "ocsp2.apple.com",
    "crl.apple.com",
    "ppq.apple.com",
    "app-attest.apple.com",
    "vpp.itunes.apple.com",
    "gdmf.apple.com",
    "certs.apple.com",
    "firebaselogging.googleapis.com",
    "logs.ads.vungle.com",
    "ad.youtube.com",
    "ads.youtube.com",
    "googleads.g.doubleclick.net",
    "pagead2.googlesyndication.com",
}

# === REWRITE: trỏ về server proxy của mình (khi có) ===
# Nếu có PROXY_IP env thì rewrite api.locketcamera.com về đó
PROXY_IP = os.getenv("PROXY_IP", "")

REWRITE_DOMAINS = {}
if PROXY_IP:
    REWRITE_DOMAINS["api.locketcamera.com"] = PROXY_IP


def is_blocked(name: str) -> bool:
    """Kiểm tra domain hoặc suffix có bị block không."""
    name = name.rstrip(".")
    if name in BLOCKED_DOMAINS:
        return True
    # check suffix
    for blocked in BLOCKED_DOMAINS:
        if name.endswith("." + blocked):
            return True
    return False


def get_rewrite_ip(name: str) -> str | None:
    """Trả về IP rewrite nếu domain khớp."""
    name = name.rstrip(".")
    return REWRITE_DOMAINS.get(name)


# =====================================================
# DNS Wireformat helpers (RFC 1035)
# =====================================================

def build_nxdomain(query_data: bytes) -> bytes:
    """Build NXDOMAIN response từ query bytes."""
    if len(query_data) < 12:
        return b""
    tx_id = query_data[:2]
    # Flags: QR=1, Opcode=0, AA=0, TC=0, RD=1, RA=1, RCODE=3 (NXDOMAIN)
    flags = struct.pack("!H", 0x8183)
    # QD=1, AN=0, NS=0, AR=0
    counts = struct.pack("!HHHH", 1, 0, 0, 0)
    question = query_data[12:]  # copy nguyên question section
    return tx_id + flags + counts + question


def build_a_response(query_data: bytes, ip: str) -> bytes:
    """Build A record response với IP chỉ định."""
    if len(query_data) < 12:
        return b""
    tx_id = query_data[:2]
    flags = struct.pack("!H", 0x8180)  # QR=1, RD=1, RA=1, RCODE=0
    counts = struct.pack("!HHHH", 1, 1, 0, 0)
    question = query_data[12:]

    # Answer: pointer đến question name + type A + class IN + TTL + RDATA
    answer = b"\xc0\x0c"  # pointer to name in question
    answer += struct.pack("!HHI", 1, 1, 60)  # type=A, class=IN, ttl=60
    packed_ip = socket.inet_aton(ip)
    answer += struct.pack("!H", 4) + packed_ip

    return tx_id + flags + counts + question + answer


def parse_qname(data: bytes, offset: int) -> tuple[str, int]:
    """Parse DNS qname từ wireformat, trả (name, next_offset)."""
    labels = []
    while offset < len(data):
        length = data[offset]
        if length == 0:
            offset += 1
            break
        if (length & 0xC0) == 0xC0:  # pointer
            ptr = ((length & 0x3F) << 8) | data[offset + 1]
            name, _ = parse_qname(data, ptr)
            labels.append(name)
            offset += 2
            break
        offset += 1
        labels.append(data[offset:offset + length].decode("ascii", errors="replace"))
        offset += length
    return ".".join(labels), offset


# =====================================================
# JSON DNS helpers
# =====================================================

def build_json_nxdomain(name: str, qtype: int) -> dict:
    return {
        "Status": 3,  # NXDOMAIN
        "TC": False, "RD": True, "RA": True, "AD": False, "CD": False,
        "Question": [{"name": name, "type": qtype}],
        "Answer": []
    }


def build_json_a(name: str, ip: str) -> dict:
    return {
        "Status": 0,
        "TC": False, "RD": True, "RA": True, "AD": False, "CD": False,
        "Question": [{"name": name, "type": 1}],
        "Answer": [{"name": name, "type": 1, "TTL": 60, "data": ip}]
    }


# =====================================================
# Endpoints
# =====================================================

@app.get("/")
async def health():
    return {"status": "ok", "service": "Locket Gold DOH Server", "by": "Hoàng Quân"}


@app.get("/dns-query")
@app.get("/dns-query/{user}")
async def doh_get(request: Request, user: str = "default"):
    """
    DOH GET - RFC 8484 (wireformat) hoặc Google JSON API
    iOS dùng: application/dns-message (wireformat)
    Browser dùng: application/dns-json
    """
    accept = request.headers.get("accept", "")

    # --- JSON mode (application/dns-json) ---
    if "dns-json" in accept or "json" in accept:
        name = request.query_params.get("name", "")
        qtype_str = request.query_params.get("type", "A")
        qtype = 1 if qtype_str == "A" else 28 if qtype_str == "AAAA" else 1

        if is_blocked(name):
            return JSONResponse(build_json_nxdomain(name, qtype))

        rewrite_ip = get_rewrite_ip(name)
        if rewrite_ip and qtype == 1:
            return JSONResponse(build_json_a(name, rewrite_ip))

        # forward lên Cloudflare
        return await forward_json(name, qtype_str)

    # --- Wireformat mode (application/dns-message) ---
    dns_param = request.query_params.get("dns", "")
    if not dns_param:
        raise HTTPException(400, "Missing dns parameter")

    # base64url decode
    padding = "=" * (-len(dns_param) % 4)
    query_data = base64.urlsafe_b64decode(dns_param + padding)

    return await handle_wireformat(query_data)


@app.post("/dns-query")
@app.post("/dns-query/{user}")
async def doh_post(request: Request, user: str = "default"):
    """DOH POST - RFC 8484 wireformat."""
    query_data = await request.body()
    return await handle_wireformat(query_data)


async def handle_wireformat(query_data: bytes) -> Response:
    """Xử lý DNS wireformat query."""
    if len(query_data) < 12:
        raise HTTPException(400, "Invalid DNS query")

    # Parse tên domain từ query
    try:
        qname, offset = parse_qname(query_data, 12)
        qtype = struct.unpack("!H", query_data[offset:offset + 2])[0]
    except Exception:
        qname, qtype = "", 1

    if is_blocked(qname):
        resp_data = build_nxdomain(query_data)
        return Response(content=resp_data, media_type="application/dns-message")

    rewrite_ip = get_rewrite_ip(qname)
    if rewrite_ip and qtype == 1:  # type A
        resp_data = build_a_response(query_data, rewrite_ip)
        return Response(content=resp_data, media_type="application/dns-message")

    # Forward lên Cloudflare DOH
    return await forward_wireformat(query_data)


async def forward_wireformat(query_data: bytes) -> Response:
    """Forward query dạng wireformat lên upstream DOH."""
    encoded = base64.urlsafe_b64encode(query_data).rstrip(b"=").decode()
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            r = await client.get(
                UPSTREAM_DOH,
                params={"dns": encoded},
                headers={"accept": "application/dns-message"}
            )
            return Response(content=r.content, media_type="application/dns-message")
        except Exception as e:
            # Fallback: trả SERVFAIL
            tx_id = query_data[:2]
            flags = struct.pack("!H", 0x8182)  # RCODE=2 SERVFAIL
            counts = struct.pack("!HHHH", 0, 0, 0, 0)
            return Response(content=tx_id + flags + counts, media_type="application/dns-message")


async def forward_json(name: str, qtype: str) -> JSONResponse:
    """Forward JSON DNS query lên Cloudflare."""
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            r = await client.get(
                UPSTREAM_DOH,
                params={"name": name, "type": qtype},
                headers={"accept": "application/dns-json"}
            )
            return JSONResponse(r.json())
        except Exception:
            return JSONResponse(build_json_nxdomain(name, 1))


# =====================================================
# Run
# =====================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
