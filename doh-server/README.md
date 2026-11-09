# Locket Gold DOH Server 🌐

Custom **DNS-over-HTTPS (DoH)** server cho Locket Gold — deploy trên Render.com.

## Endpoints

| Method | Path | Mô tả |
|--------|------|--------|
| GET | `/` | Health check |
| GET/POST | `/dns-query` | DoH standard (RFC 8484) |
| GET/POST | `/dns-query/{user}` | DoH có user path (theo mobileconfig) |

## Logic

- **BLOCK** (trả NXDOMAIN): `ocsp.apple.com`, `crl.apple.com`, `ppq.apple.com`, `app-attest.apple.com`, `firebaselogging.googleapis.com`, ads...
- **REWRITE** (nếu set `PROXY_IP`): `api.locketcamera.com` → IP proxy riêng
- **FORWARD**: tất cả domain khác → Cloudflare `1.1.1.1` DOH

## Deploy lên Render

1. Push repo lên GitHub
2. Vào [render.com](https://render.com) → **New Web Service** → chọn repo
3. Render tự detect `render.yaml` → deploy tự động
4. Lấy URL dạng `https://locket-gold-doh.onrender.com`

## Cập nhật mobileconfig

Thay `ServerURL` trong file `.mobileconfig`:
```xml
<key>ServerURL</key>
<string>https://locket-gold-doh.onrender.com/dns-query/links</string>
```

## Env Variables

| Key | Mô tả | Default |
|-----|--------|---------|
| `PORT` | Port server | `8080` |
| `PROXY_IP` | IP proxy cho `api.locketcamera.com` | (trống = không rewrite) |
