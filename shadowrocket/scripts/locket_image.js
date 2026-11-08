/**
 * Locket Filter Image Download Engine - Hoàng Quân
 * Matches: ^https:\/\/api\.locketcamera\.com\/uploads\/ai_filters\/
 */

var targetHost = "http://180.93.34.245";
var url = $request.url;
var path = url.split("api.locketcamera.com")[1];

var headers = $request.headers || {};
var userAgent = headers["User-Agent"] || headers["user-agent"] || "Locket/3870 CFNetwork/1568.200.51 Darwin/24.1.0";

var options = {
  url: targetHost + path,
  headers: {
    "Host": "api.locketcamera.com",
    "User-Agent": userAgent
  },
  "binary-mode": true
};

$httpClient.get(options, function(error, response, data) {
  if (error || !data) {
    $done({});
  } else {
    $done({
      response: {
        status: 200,
        headers: {
          "Content-Type": "image/jpeg",
          "Cache-Control": "public, max-age=31536000",
          "Access-Control-Allow-Origin": "*"
        },
        body: data
      }
    });
  }
});
