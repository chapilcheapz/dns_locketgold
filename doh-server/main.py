"""
DOH Server - Locket Gold Pipeline
Dựa trên mobileconfig logic
Deploy: Render.com
"""

import os
import struct
import socket
import base64
import asyncio
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI(title="Locket Gold DOH Server")

# === UPSTREAM DNS ===
UPSTREAM_DOH = "https://cloudflare-dns.com/dns-query"

# === DOMAIN RULES ===
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

# Proxy IP xử lý SSL MITM và Gold injection
PROXY_IP = os.getenv("PROXY_IP", "180.93.34.245")

REWRITE_DOMAINS = {
    "api.revenuecat.com": PROXY_IP,
    "api.locketcamera.com": PROXY_IP,
}


def is_blocked(name: str) -> bool:
    """Kiểm tra domain hoặc suffix có bị block không."""
    name = name.rstrip(".")
    if name in BLOCKED_DOMAINS:
        return True
    for blocked in BLOCKED_DOMAINS:
        if name.endswith("." + blocked):
            return True
    return False


def get_rewrite_ip(name: str) -> str | None:
    """Trả về IP rewrite nếu domain khớp."""
    name = name.rstrip(".")
    if name in REWRITE_DOMAINS:
        return REWRITE_DOMAINS[name]
    if name.endswith(".revenuecat.com"):
        return PROXY_IP
    return None


# =====================================================
# DNS Wireformat helpers (RFC 1035)
# =====================================================

def build_nxdomain(query_data: bytes) -> bytes:
    if len(query_data) < 12:
        return b""
    tx_id = query_data[:2]
    flags = struct.pack("!H", 0x8183)
    counts = struct.pack("!HHHH", 1, 0, 0, 0)
    question = query_data[12:]
    return tx_id + flags + counts + question


def build_a_response(query_data: bytes, ip: str) -> bytes:
    if len(query_data) < 12:
        return b""
    tx_id = query_data[:2]
    flags = struct.pack("!H", 0x8180)
    counts = struct.pack("!HHHH", 1, 1, 0, 0)
    question = query_data[12:]

    answer = b"\xc0\x0c"
    answer += struct.pack("!HHI", 1, 1, 60)
    packed_ip = socket.inet_aton(ip)
    answer += struct.pack("!H", 4) + packed_ip

    return tx_id + flags + counts + question + answer


def parse_qname(data: bytes, offset: int) -> tuple[str, int]:
    labels = []
    while offset < len(data):
        length = data[offset]
        if length == 0:
            offset += 1
            break
        if (length & 0xC0) == 0xC0:
            ptr = ((length & 0x3F) << 8) | data[offset + 1]
            name, _ = parse_qname(data, ptr)
            labels.append(name)
            offset += 2
            break
        offset += 1
        labels.append(data[offset:offset + length].decode("ascii", errors="replace"))
        offset += length
    return ".".join(labels), offset


def build_json_nxdomain(name: str, qtype: int) -> dict:
    return {
        "Status": 3,
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


MOBILECONFIG_XML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PayloadDisplayName</key>
  <string>Locket Gold — Hoàng Quân</string>
  <key>PayloadDescription</key>
  <string>Tự động kích hoạt Locket Gold 💛 — Chặn revoke &amp; Không cần Shadowrocket</string>
  <key>PayloadIdentifier</key>
  <string>com.locketgold.hoangquan.allinone</string>
  <key>PayloadOrganization</key>
  <string>Hoàng Quân</string>
  <key>PayloadType</key>
  <string>Configuration</string>
  <key>PayloadUUID</key>
  <string>34D91000-AFAE-4EB0-2540-F8FE34AB7AB6</string>
  <key>PayloadVersion</key>
  <integer>1</integer>
  <key>PayloadRemovalDisallowed</key>
  <false/>
  <key>PayloadContent</key>
  <array>
    <dict>
      <key>PayloadType</key>
      <string>com.apple.security.root</string>
      <key>PayloadIdentifier</key>
      <string>com.locketgold.hoangquan.ca</string>
      <key>PayloadUUID</key>
      <string>00893BDE-36C5-C8EE-1267-580C1BBF5737</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>PayloadDisplayName</key>
      <string>Locket Gold Root CA</string>
      <key>PayloadCertificateFileName</key>
      <string>LocketGoldRootCA.der</string>
      <key>PayloadContent</key>
      <data>
MIIDYjCCAkqgAwIBAgIUS7u544iqsduNXak3obh9JcG944YwDQYJKoZIhvcNAQELBQAwSTELMAkG
A1UEBhMCVk4xHDAaBgNVBAoME0xvY2tldCBHb2xkIE5ldHdvcmsxHDAaBgNVBAMME0xvY2tldCBH
b2xkIFJvb3QgQ0EwHhcNMjYwOTI2MDYxNzE1WhcNMzYwOTIzMDYxNzE1WjBJMQswCQYDVQQGEwJW
TjEcMBoGA1UECgwTTG9ja2V0IEdvbGQgTmV0d29yazEcMBoGA1UEAwwTTG9ja2V0IEdvbGQgUm9v
dCBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJ4H13uT3sKa8OBJHJTcyY084PZs
dU734K6wAq5Onv9vITdJ2YW20354W7y092d2pUtV3KFtfB/7CQdRG51KEd2mDpK2XmNPmoIetW70
YQKzvmhhuO0N6IUWoDmkbjcRIDoGv0z/eDi08oB/sKtKtU8y/efBPv0Z1T/UpcaScVHahLBKz2Y9
weJR+GR1b5hB6X+M8eFG33DSHUt5dMMic2g1CPgizEVXbdxXnUdl/t83X0NAIQfoK4znm977ZIzz
gVynGpAunBTh28bMC0AIF77sea+2FSD4HkWSUxX7xDnYOVymIzkxbkD8RcbVayjLCUEV8vyboTys
aJ8SX4ANMMMCAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAQYwHQYDVR0O
BBYEFNY5tbrBOyd3FRT6R0WRmxIsiVFPMA0GCSqGSIb3DQEBCwUAA4IBAQB5XHksW7bGB3yudvy2
KAABaXfoL5egKFh7UDyaht4R+Kh0XhwsWLA0DR0L4RzP+17GdmNwojdWb40lmIlX3sb4MsYl0sii
AJ5FR+okC8k8aeb/1mupEX5ChAPgd0rQDF4ln2O1DQ7QtVr56gN/qwqxzC386ceG5hZ2lGaDsoDu
Ejw0E+ZUv/AIBJgxlv7uGw6g9VU6aoCW9/0pHTx6YiUPfT0JcOMpqqnjDA5RwBfCjrjdbFQiw3+L
oOQeW4UNPyUBbs7ldDTTwE6hgHwgFTQqKLKGKUxV+f0mKuSCpVcCTS2AOzDykb4d6bFdnIZb6eTd
+c81qOPES1gcIfec1eOt
      </data>
    </dict>
    <dict>
      <key>PayloadType</key>
      <string>com.apple.dnsSettings.managed</string>
      <key>PayloadIdentifier</key>
      <string>com.locketgold.hoangquan.dns</string>
      <key>PayloadUUID</key>
      <string>A2F3C21B-A28C-5FA9-7308-A3AC203859DB</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>PayloadDisplayName</key>
      <string>Locket Gold DNS Server</string>
      <key>DNSSettings</key>
      <dict>
        <key>DNSProtocol</key>
        <string>HTTPS</string>
        <key>ServerURL</key>
        <string>https://dns-locketgold.onrender.com/dns-query/hoangquan</string>
        <key>ServerAddresses</key>
        <array>
          <string>1.1.1.1</string>
          <string>1.0.0.1</string>
        </array>
        <key>SupplementalMatchDomains</key>
        <array>
          <string>api.revenuecat.com</string>
          <string>*.revenuecat.com</string>
          <string>api.locketcamera.com</string>
          <string>firebaseremoteconfig.googleapis.com</string>
          <string>*.firebaseremoteconfig.googleapis.com</string>
          <string>firebaseremoteconfigrealtime.googleapis.com</string>
          <string>ocsp.apple.com</string>
          <string>ocsp2.apple.com</string>
          <string>crl.apple.com</string>
          <string>ppq.apple.com</string>
          <string>app-attest.apple.com</string>
          <string>vpp.itunes.apple.com</string>
          <string>gdmf.apple.com</string>
          <string>certs.apple.com</string>
          <string>firebaselogging.googleapis.com</string>
          <string>logs.ads.vungle.com</string>
          <string>ad.youtube.com</string>
          <string>ads.youtube.com</string>
          <string>googleads.g.doubleclick.net</string>
          <string>pagead2.googlesyndication.com</string>
        </array>
      </dict>
    </dict>
  </array>
</dict>
</plist>"""


@app.get("/profile")
@app.get("/profile/{user}")
async def serve_mobileconfig(user: str = "hoangquan"):
    return Response(
        content=MOBILECONFIG_XML.strip(),
        media_type="application/x-apple-aspen-config",
        headers={
            "Content-Disposition": f'attachment; filename="LocketGold_{user}.mobileconfig"'
        }
    )


@app.get("/install")
async def install_page():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Locket Gold — Cài đặt 1 chạm</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 440px; margin: 30px auto; padding: 20px; background: #0f0f11; color: #fff; }
  .card { background: #1c1c1e; border-radius: 20px; padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.4); border: 1px solid #2c2c2e; }
  h1 { font-size: 24px; margin-bottom: 8px; color: #ffd60a; }
  p { color: #a1a1a6; font-size: 15px; line-height: 1.5; }
  .btn { display: block; background: linear-gradient(135deg, #ffd60a, #ff9f0a); color: #000; text-decoration: none;
         text-align: center; padding: 15px; border-radius: 14px; font-size: 17px;
         font-weight: 700; margin-top: 20px; box-shadow: 0 4px 16px rgba(255,214,10,0.3); }
  .steps { background: #2c2c2e; border-radius: 14px; padding: 16px; margin-top: 20px; }
  .steps ol { margin: 0; padding-left: 20px; }
  .steps li { color: #e5e5ea; font-size: 14px; margin: 10px 0; }
  .steps b { color: #ffd60a; }
  .badge { background: #30d158; color: #000; border-radius: 6px; padding: 3px 8px; font-size: 12px; font-weight: 600; }
</style>
</head>
<body>
<div class="card">
  <h1>💛 Locket Gold VIP</h1>
  <p>Cài đặt 1 profile duy nhất — Tự động kích hoạt Gold, chặn revoke, không cần mở Shadowrocket.</p>
  <span class="badge">● Server Online</span>
  <a class="btn" href="/profile">📲 Cài Profile Ngay (mở Safari)</a>
  <div class="steps">
    <b>Các bước hoàn tất (chỉ làm 1 lần):</b>
    <ol>
      <li>Nhấn nút trên bằng <b>Safari</b> → Chọn <b>Allow (Cho phép)</b></li>
      <li>Vào <b>Cài đặt (Settings) → Đã tải về hồ sơ</b> → Chọn <b>Cài đặt (Install)</b></li>
      <li>Vào <b>Cài đặt chung → Giới thiệu → Cài đặt tin cậy chứng nhận</b> (Certificate Trust Settings)</li>
      <li>Bật gạt xanh <b>Locket Gold Root CA</b></li>
      <li>🎉 Mở Locket — Thưởng thức Locket Gold!</li>
    </ol>
  </div>
</div>
</body>
</html>"""
    return HTMLResponse(html)


@app.get("/dns-query")
@app.get("/dns-query/{user}")
async def doh_get(request: Request, user: str = "default"):
    accept = request.headers.get("accept", "")

    if "dns-json" in accept or "json" in accept:
        name = request.query_params.get("name", "")
        qtype_str = request.query_params.get("type", "A")
        qtype = 1 if qtype_str == "A" else 28 if qtype_str == "AAAA" else 1

        if is_blocked(name):
            return JSONResponse(build_json_nxdomain(name, qtype))

        rewrite_ip = get_rewrite_ip(name)
        if rewrite_ip and qtype == 1:
            return JSONResponse(build_json_a(name, rewrite_ip))

        return await forward_json(name, qtype_str)

    dns_param = request.query_params.get("dns", "")
    if not dns_param:
        raise HTTPException(400, "Missing dns parameter")

    padding = "=" * (-len(dns_param) % 4)
    query_data = base64.urlsafe_b64decode(dns_param + padding)
    return await handle_wireformat(query_data)


@app.post("/dns-query")
@app.post("/dns-query/{user}")
async def doh_post(request: Request, user: str = "default"):
    query_data = await request.body()
    return await handle_wireformat(query_data)


async def handle_wireformat(query_data: bytes) -> Response:
    if len(query_data) < 12:
        raise HTTPException(400, "Invalid DNS query")

    try:
        qname, offset = parse_qname(query_data, 12)
        qtype = struct.unpack("!H", query_data[offset:offset + 2])[0]
    except Exception:
        qname, qtype = "", 1

    if is_blocked(qname):
        resp_data = build_nxdomain(query_data)
        return Response(content=resp_data, media_type="application/dns-message")

    rewrite_ip = get_rewrite_ip(qname)
    if rewrite_ip and qtype == 1:
        resp_data = build_a_response(query_data, rewrite_ip)
        return Response(content=resp_data, media_type="application/dns-message")

    return await forward_wireformat(query_data)


async def forward_wireformat(query_data: bytes) -> Response:
    encoded = base64.urlsafe_b64encode(query_data).rstrip(b"=").decode()
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            r = await client.get(
                UPSTREAM_DOH,
                params={"dns": encoded},
                headers={"accept": "application/dns-message"}
            )
            return Response(content=r.content, media_type="application/dns-message")
        except Exception:
            tx_id = query_data[:2]
            flags = struct.pack("!H", 0x8182)
            counts = struct.pack("!HHHH", 0, 0, 0, 0)
            return Response(content=tx_id + flags + counts, media_type="application/dns-message")


async def forward_json(name: str, qtype: str) -> JSONResponse:
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
