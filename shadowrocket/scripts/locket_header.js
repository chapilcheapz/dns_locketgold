/***********************************************
> deleteHeader by HoangQuan
***********************************************/

function setHeaderValue(e, a, d) {
  var r = a.toLowerCase();
  r in e ? (e[r] = d) : (e[a] = d);
}

var modifiedHeaders = $request.headers;
setHeaderValue(modifiedHeaders, "X-RevenueCat-ETag", "");
setHeaderValue(modifiedHeaders, "If-None-Match", "");
if (modifiedHeaders["x-revenuecat-etag"]) delete modifiedHeaders["x-revenuecat-etag"];
if (modifiedHeaders["if-none-match"]) delete modifiedHeaders["if-none-match"];

$done({ headers: modifiedHeaders });
