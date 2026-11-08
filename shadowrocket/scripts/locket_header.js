/***********************************************
> deleteHeader by HoangQuan (inspired by all-in-one.conf)
***********************************************/

function setHeaderValue(headers, key, value) {
    const lowerKey = key.toLowerCase();
    if (lowerKey in headers) {
        headers[lowerKey] = value;
    } else {
        headers[key] = value;
    }
}

var modifiedHeaders = $request.headers || {};

const headersToModify = {
    "X-RevenueCat-ETag": "",
    "If-None-Match": "",
    "If-Modified-Since": "",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
};

for (let key in headersToModify) {
    setHeaderValue(modifiedHeaders, key, headersToModify[key]);
}

delete modifiedHeaders["Accept-Encoding"];
delete modifiedHeaders["accept-encoding"];
delete modifiedHeaders["X-Nonce"];
delete modifiedHeaders["x-nonce"];

$done({ headers: modifiedHeaders });
