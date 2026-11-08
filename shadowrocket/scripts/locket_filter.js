/**
 * Locket Filter Generation Engine - Hoàng Quân
 * Matches: ^https:\/\/api\.locketcamera\.com\/generateFilteredImage
 */

var targetHost = "http://180.93.34.245";
var headers = $request.headers || {};
var userAgent = headers["User-Agent"] || headers["user-agent"] || "Locket/3870 CFNetwork/1568.200.51 Darwin/24.1.0";

var bodyStr = typeof $request.body === "string" ? $request.body : JSON.stringify($request.body || {});

var options = {
  url: targetHost + "/generateFilteredImage",
  headers: {
    "Host": "api.locketcamera.com",
    "Content-Type": "application/json",
    "User-Agent": userAgent
  },
  body: bodyStr,
  timeout: 10
};

$httpClient.post(options, function(error, response, data) {
  if (!error && data && data.indexOf("outputUrl") !== -1) {
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
  } else {
    // Robust Fallback: extract image_url so Locket never fails
    try {
      var reqJson = JSON.parse(bodyStr);
      var inputUrl = (reqJson.data && reqJson.data.image_url) || reqJson.image_url || "";
      if (inputUrl) {
        var fallbackRes = {
          result: {
            data: {
              outputUrl: inputUrl,
              output_url: inputUrl,
              url: inputUrl
            },
            outputUrl: inputUrl,
            output_url: inputUrl,
            url: inputUrl,
            status: 200
          }
        };
        $done({
          response: {
            status: 200,
            headers: {
              "Content-Type": "application/json; charset=utf-8",
              "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify(fallbackRes)
          }
        });
        return;
      }
    } catch(e) {}
    $done({});
  }
});
