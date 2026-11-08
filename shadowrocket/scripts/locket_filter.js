/**
 * Locket Filter Engine for Shadowrocket
 * Author: Hoàng Quân
 * Matches: ^https:\/\/api\.locketcamera\.com\/(generateFilteredImage|uploads\/ai_filters\/)
 */

const url = $request.url;
const targetHost = "http://180.93.34.245";

if (url.includes("/generateFilteredImage")) {
  const options = {
    url: targetHost + "/generateFilteredImage",
    headers: {
      "Host": "api.locketcamera.com",
      "Content-Type": "application/json",
      "User-Agent": $request.headers["User-Agent"] || $request.headers["user-agent"] || "Locket/3870"
    },
    body: $request.body
  };
  
  $httpClient.post(options, function(error, response, data) {
    if (error) {
      $done({});
    } else {
      $done({
        status: 200,
        headers: { "Content-Type": "application/json; charset=utf-8" },
        body: data
      });
    }
  });
} else if (url.includes("/uploads/ai_filters/")) {
  const path = url.split("api.locketcamera.com")[1];
  const options = {
    url: targetHost + path,
    headers: {
      "Host": "api.locketcamera.com",
      "User-Agent": $request.headers["User-Agent"] || $request.headers["user-agent"] || "Locket/3870"
    },
    "binary-mode": true
  };
  
  $httpClient.get(options, function(error, response, data) {
    if (error) {
      $done({});
    } else {
      $done({
        status: 200,
        headers: {
          "Content-Type": "image/jpeg",
          "Cache-Control": "public, max-age=31536000"
        },
        body: data
      });
    }
  });
} else {
  $done({});
}
