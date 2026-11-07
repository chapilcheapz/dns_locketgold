/***********************************************
> deleteHeader by HoangQuan
***********************************************/

var modifiedHeaders = $request.headers || {};
delete modifiedHeaders["X-RevenueCat-ETag"];
delete modifiedHeaders["x-revenuecat-etag"];
delete modifiedHeaders["If-None-Match"];
delete modifiedHeaders["if-none-match"];
delete modifiedHeaders["X-Nonce"];
delete modifiedHeaders["x-nonce"];

$done({ headers: modifiedHeaders });
