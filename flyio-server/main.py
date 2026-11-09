"""
Locket Gold All-in-One Server
-------------------------------
Chạy 3 service trên 1 process:

1. DOH Server     :443/tcp  → DNS-over-HTTPS (block ocsp/crl, rewrite revenuecat → 127.0.0.1)
2. TLS MITM Proxy :443/tcp  → Giả api.revenuecat.com, inject Gold
3. Profile Serve  :80/tcp   → Serve .mobileconfig để iPhone cài

Flow:
  iPhone cài mobileconfig
    → DOH server chặn anti-revoke, rewrite api.revenuecat.com → IP máy này
    → iPhone gọi HTTPS tới máy này (tưởng là revenuecat)
    → TLS MITM dùng custom cert → inject Gold response
    → Locket thấy Gold ✅
"""

import os, ssl, json, struct, socket, base64, asyncio, threading
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn

# ─── Config ──────────────────────────────────────────────────────────────────
PORT_HTTP   = int(os.getenv("PORT", 8080))       # HTTP: profile serve + DOH JSON
PORT_MITM   = int(os.getenv("PORT_MITM", 8443))  # HTTPS MITM: giả revenuecat
CERT_DIR    = os.path.join(os.path.dirname(__file__), "certs")
CA_CERT     = os.path.join(CERT_DIR, "ca.crt")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY  = os.path.join(CERT_DIR, "server.key")
UPSTREAM    = "https://cloudflare-dns.com/dns-query"

# ─── Block list (anti-revoke + ads) ──────────────────────────────────────────
BLOCKED = {
    "ocsp.apple.com", "ocsp2.apple.com", "crl.apple.com", "ppq.apple.com",
    "app-attest.apple.com", "vpp.itunes.apple.com", "gdmf.apple.com",
    "certs.apple.com", "firebaselogging.googleapis.com",
    "logs.ads.vungle.com", "ad.youtube.com", "ads.youtube.com",
    "googleads.g.doubleclick.net", "pagead2.googlesyndication.com",
}

def is_blocked(name: str) -> bool:
    name = name.rstrip(".")
    if name in BLOCKED: return True
    return any(name.endswith("." + b) for b in BLOCKED)

# ─── DNS wireformat helpers ───────────────────────────────────────────────────
def build_nxdomain(q: bytes) -> bytes:
    if len(q) < 12: return b""
    return q[:2] + struct.pack("!H", 0x8183) + struct.pack("!HHHH", 1,0,0,0) + q[12:]

def build_a_resp(q: bytes, ip: str) -> bytes:
    if len(q) < 12: return b""
    ans = b"\xc0\x0c" + struct.pack("!HHI", 1, 1, 60) + struct.pack("!H", 4) + socket.inet_aton(ip)
    return q[:2] + struct.pack("!H", 0x8180) + struct.pack("!HHHH", 1,1,0,0) + q[12:] + ans

def parse_qname(data: bytes, off: int) -> tuple[str, int]:
    labels = []
    while off < len(data):
        ln = data[off]
        if ln == 0: off += 1; break
        if (ln & 0xC0) == 0xC0:
            ptr = ((ln & 0x3F) << 8) | data[off+1]
            labels.append(parse_qname(data, ptr)[0])
            off += 2; break
        off += 1
        labels.append(data[off:off+ln].decode("ascii", errors="replace"))
        off += ln
    return ".".join(labels), off

# ─── Gold entitlements injector ───────────────────────────────────────────────
def inject_gold(body: str) -> str:
    try: obj = json.loads(body)
    except: return body
    if not isinstance(obj, dict): return body
    if "subscriber" not in obj:
        obj["subscriber"] = {}
    sub = obj["subscriber"]
    sub.setdefault("entitlements", {})
    sub.setdefault("subscriptions", {})

    gold_ent = {
        "expires_date": "2099-12-31T23:59:59Z",
        "grace_period_expires_date": None,
        "product_identifier": "locket_2400_1y",
        "purchase_date": "2024-01-01T00:00:00Z",
        "ownership_type": "PURCHASED",
        "store": "app_store",
        "is_sandbox": False,
    }
    gold_sub = {
        "expires_date": "2099-12-31T23:59:59Z",
        "original_purchase_date": "2024-01-01T00:00:00Z",
        "purchase_date": "2024-01-01T00:00:00Z",
        "period_type": "normal",
        "ownership_type": "PURCHASED",
        "billing_issues_detected_at": None,
        "grace_period_expires_date": None,
        "unsubscribe_detected_at": None,
        "store": "app_store",
        "is_sandbox": False,
    }
    for e in ["Gold", "gold", "locket_gold"]:
        sub["entitlements"][e] = gold_ent
    sub["subscriptions"]["locket_2400_1y"] = gold_sub
    return json.dumps(obj)

# ─── FastAPI app (HTTP :PORT_HTTP) ────────────────────────────────────────────
app = FastAPI()

@app.get("/")
async def index():
    return {"status": "ok", "service": "Locket Gold Server", "by": "Hoàng Quân"}

# ── DOH endpoint (JSON mode cho test) ────────────────────────────────────────
@app.get("/dns-query")
@app.get("/dns-query/{user}")
async def doh_get(request: Request, user: str = "default"):
    accept = request.headers.get("accept", "")
    if "dns-json" in accept or "json" in accept:
        name = request.query_params.get("name", "")
        qtype_str = request.query_params.get("type", "A")
        qtype = 28 if qtype_str == "AAAA" else 1
        if is_blocked(name):
            return JSONResponse({"Status":3,"TC":False,"RD":True,"RA":True,"AD":False,"CD":False,
                                 "Question":[{"name":name,"type":qtype}],"Answer":[]})
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(UPSTREAM, params={"name":name,"type":qtype_str},
                            headers={"accept":"application/dns-json"})
            return JSONResponse(r.json())

    # wireformat GET
    dns_b64 = request.query_params.get("dns","")
    if not dns_b64: raise HTTPException(400, "missing dns param")
    q = base64.urlsafe_b64decode(dns_b64 + "=" * (-len(dns_b64) % 4))
    return await _handle_wire(q)

@app.post("/dns-query")
@app.post("/dns-query/{user}")
async def doh_post(request: Request, user: str = "default"):
    q = await request.body()
    return await _handle_wire(q)

async def _handle_wire(q: bytes) -> Response:
    if len(q) < 12: raise HTTPException(400, "bad query")
    try:
        qname, off = parse_qname(q, 12)
        qtype = struct.unpack("!H", q[off:off+2])[0]
    except: qname, qtype = "", 1
    if is_blocked(qname):
        return Response(build_nxdomain(q), media_type="application/dns-message")
    enc = base64.urlsafe_b64encode(q).rstrip(b"=").decode()
    async with httpx.AsyncClient(timeout=5) as c:
        try:
            r = await c.get(UPSTREAM, params={"dns":enc},
                            headers={"accept":"application/dns-message"})
            return Response(r.content, media_type="application/dns-message")
        except:
            return Response(q[:2]+struct.pack("!H",0x8182)+struct.pack("!HHHH",0,0,0,0),
                            media_type="application/dns-message")

# ── Profile serve ─────────────────────────────────────────────────────────────
def _profile_xml(server_ip: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>PayloadDisplayName</key><string>Locket Gold — Hoàng Quân</string>
  <key>PayloadDescription</key><string>Tự động kích hoạt Gold — không cần Shadowrocket</string>
  <key>PayloadIdentifier</key><string>com.locketgold.hoangquan.full</string>
  <key>PayloadOrganization</key><string>Hoàng Quân</string>
  <key>PayloadType</key><string>Configuration</string>
  <key>PayloadUUID</key><string>C9E2B41D-5F7A-4B0C-8D3E-A6F1C2B3D4E5</string>
  <key>PayloadVersion</key><integer>1</integer>
  <key>PayloadRemovalDisallowed</key><false/>
  <key>PayloadContent</key><array>
    <!-- 1. Trust custom Root CA -->
    <dict>
      <key>PayloadType</key><string>com.apple.security.root</string>
      <key>PayloadIdentifier</key><string>com.locketgold.hoangquan.ca</string>
      <key>PayloadUUID</key><string>D1E3F52A-6B8C-4D0E-9F1A-B2C3D4E5F6A7</string>
      <key>PayloadVersion</key><integer>1</integer>
      <key>PayloadDisplayName</key><string>Locket Gold Root CA</string>
      <key>PayloadContent</key>
      <data>{_read_ca_b64()}</data>
    </dict>
    <!-- 2. DOH server -->
    <dict>
      <key>PayloadType</key><string>com.apple.dnsSettings.managed</string>
      <key>PayloadIdentifier</key><string>com.locketgold.hoangquan.dns</string>
      <key>PayloadUUID</key><string>E2F4A63B-7C9D-4E1F-A02B-C3D4E5F6A7B8</string>
      <key>PayloadVersion</key><integer>1</integer>
      <key>PayloadDisplayName</key><string>Locket Gold DOH</string>
      <key>DNSSettings</key><dict>
        <key>DNSProtocol</key><string>HTTPS</string>
        <key>ServerURL</key><string>https://dns-locketgold.onrender.com/dns-query/hoangquan</string>
        <key>ServerAddresses</key><array>
          <string>1.1.1.1</string><string>1.0.0.1</string>
        </array>
        <key>SupplementalMatchDomains</key><array>
          <string>api.revenuecat.com</string>
          <string>*.revenuecat.com</string>
          <string>ocsp.apple.com</string>
          <string>ocsp2.apple.com</string>
          <string>crl.apple.com</string>
          <string>ppq.apple.com</string>
          <string>app-attest.apple.com</string>
          <string>vpp.itunes.apple.com</string>
          <string>gdmf.apple.com</string>
          <string>certs.apple.com</string>
          <string>firebaselogging.googleapis.com</string>
        </array>
      </dict>
    </dict>
  </array>
</dict></plist>"""

def _read_ca_b64() -> str:
    try:
        import subprocess
        # Convert PEM → DER → base64
        result = subprocess.run(
            ["openssl", "x509", "-in", CA_CERT, "-outform", "DER"],
            capture_output=True
        )
        return base64.b64encode(result.stdout).decode()
    except:
        return ""

@app.get("/profile")
@app.get("/profile/{user}")
async def serve_profile(request: Request, user: str = "hoangquan"):
    host = request.headers.get("host", "localhost").split(":")[0]
    xml = _profile_xml(host)
    return Response(
        content=xml,
        media_type="application/x-apple-aspen-config",
        headers={"Content-Disposition": f'attachment; filename="LocketGold_{user}.mobileconfig"'}
    )

@app.get("/install")
async def install_page(request: Request):
    host = request.headers.get("host", "localhost")
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Locket Gold</title>
<style>
body{{font-family:-apple-system,sans-serif;max-width:420px;margin:40px auto;padding:20px;background:#f5f5f7}}
.card{{background:white;border-radius:16px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.1)}}
h1{{font-size:22px;color:#1d1d1f}}p{{color:#6e6e73;font-size:15px;line-height:1.5}}
.btn{{display:block;background:#0071e3;color:white;text-decoration:none;text-align:center;
      padding:14px;border-radius:12px;font-size:17px;font-weight:600;margin-top:20px}}
.steps{{background:#f5f5f7;border-radius:12px;padding:16px;margin-top:16px}}
.steps li{{color:#1d1d1f;font-size:14px;margin:8px 0}}
</style></head><body>
<div class="card">
  <h1>🌟 Locket Gold</h1>
  <p>Chỉ cài 1 profile là xong — không cần Shadowrocket.</p>
  <a class="btn" href="http://{host}/profile">📲 Tải Profile (mở bằng Safari)</a>
  <div class="steps"><b>Hướng dẫn:</b><ol>
    <li>Nhấn nút trên bằng <b>Safari</b></li>
    <li>Chọn <b>Allow</b></li>
    <li><b>Settings → General → VPN & Device Management</b></li>
    <li>Chọn <b>Locket Gold</b> → <b>Install</b></li>
    <li>Vào Settings → tin tưởng Root CA</li>
    <li>✅ Mở Locket — Gold đã kích hoạt!</li>
  </ol></div>
</div></body></html>"""
    return HTMLResponse(html)

# ─── MITM HTTPS server (:PORT_MITM) ──────────────────────────────────────────
# Nhận TLS từ iPhone (dùng custom cert), forward lên revenuecat thật,
# inject Gold vào response trước khi trả về.

REAL_RC = "api.revenuecat.com"

async def handle_mitm_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        raw = b""
        # Đọc HTTP request headers
        while b"\r\n\r\n" not in raw:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=10)
            if not chunk: break
            raw += chunk

        # Parse method + path + headers
        lines = raw.split(b"\r\n")
        req_line = lines[0].decode("utf-8", errors="replace")
        parts = req_line.split(" ")
        method = parts[0] if len(parts) > 0 else "GET"
        path   = parts[1] if len(parts) > 1 else "/"

        headers = {}
        for line in lines[1:]:
            if b":" in line:
                k, v = line.split(b":", 1)
                headers[k.strip().lower().decode()] = v.strip().decode()

        # Read body if present
        body = b""
        content_length = int(headers.get("content-length", 0))
        if content_length > 0:
            body = raw.split(b"\r\n\r\n", 1)[1] if b"\r\n\r\n" in raw else b""
            while len(body) < content_length:
                chunk = await asyncio.wait_for(reader.read(4096), timeout=10)
                if not chunk: break
                body += chunk

        # Forward lên revenuecat thật
        url = f"https://{REAL_RC}{path}"
        fwd_headers = {k: v for k, v in headers.items()
                       if k not in ("host", "content-length")}
        fwd_headers["host"] = REAL_RC

        async with httpx.AsyncClient(timeout=15, verify=True) as client:
            resp = await client.request(method, url, headers=fwd_headers, content=body)
            resp_body = resp.content
            resp_text = resp_body.decode("utf-8", errors="replace")

        # Inject Gold nếu là subscribers/receipts endpoint
        inject_paths = ["/subscribers", "/receipts"]
        if any(p in path for p in inject_paths):
            resp_text = inject_gold(resp_text)
            resp_body = resp_text.encode("utf-8")

        # Trả response về iPhone
        status = resp.status_code
        resp_headers = (
            f"HTTP/1.1 {status} OK\r\n"
            f"Content-Type: application/json; charset=utf-8\r\n"
            f"Content-Length: {len(resp_body)}\r\n"
            f"Cache-Control: no-cache, no-store\r\n"
            f"Connection: close\r\n\r\n"
        )
        writer.write(resp_headers.encode() + resp_body)
        await writer.drain()
    except Exception as e:
        pass
    finally:
        writer.close()


async def start_mitm_server():
    """Start TLS server giả api.revenuecat.com."""
    if not (os.path.exists(SERVER_CERT) and os.path.exists(SERVER_KEY)):
        print(f"⚠️  Certs không tìm thấy tại {CERT_DIR} — MITM server bỏ qua")
        return

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(SERVER_CERT, SERVER_KEY)

    server = await asyncio.start_server(
        handle_mitm_client, "0.0.0.0", PORT_MITM, ssl=ctx
    )
    print(f"✅ MITM server chạy tại :{PORT_MITM} (giả api.revenuecat.com)")
    async with server:
        await server.serve_forever()


# ─── Main ─────────────────────────────────────────────────────────────────────
async def main():
    # Chạy song song: FastAPI (HTTP) + MITM TLS server
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT_HTTP, log_level="info")
    server = uvicorn.Server(config)
    await asyncio.gather(
        server.serve(),
        start_mitm_server(),
    )

if __name__ == "__main__":
    asyncio.run(main())
