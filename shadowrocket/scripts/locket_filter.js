/**
 * Locket Filter Generation Engine - Hoàng Quân
 * Matches: ^https:\/\/api\.locketcamera\.com\/generateFilteredImage
 */

var targetHost = "http://180.93.34.245";
var headers = $request.headers || {};
var userAgent = headers["User-Agent"] || headers["user-agent"] || "Locket/3870 CFNetwork/1568.200.51 Darwin/24.1.0";

var options = {
  url: targetHost + "/generateFilteredImage",
  headers: {
    "Host": "api.locketcamera.com",
    "Content-Type": "application/json",
    "User-Agent": userAgent
  },
  body: $request.body
};

$httpClient.post(options, function(error, response, data) {
  if (error || !data) {
    $done({});
  } else {
    $done({
      response: {
        status: 200,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Access-Control-Allow-Origin": "*"
        },
        body: data
      }
    });
  }
});
