/**
 * Locket RevenueCat Script - Hoàng Quân
 * Matches: ^https:\/\/api\.revenuecat\.com\/.+\/(receipts$|subscribers\/[^/?#]+$)
 */

var obj = {};
try {
  obj = JSON.parse($response.body);
} catch (e) {
  obj = {};
}

obj.Attention = "Kích hoạt Locket Gold thành công - Hoàng Quân";

var HQ = {
  auto_resume_date: null,
  display_name: "locket_1600_1y",
  is_sandbox: true,
  ownership_type: "PURCHASED",
  billing_issues_detected_at: null,
  management_url: "https://apps.apple.com/account/subscriptions",
  period_type: "normal",
  price: {
    "amount": 399000.0,
    "currency": "VND"
  },
  expires_date: "9999-01-09T10:10:14Z",
  grace_period_expires_date: null,
  refunded_at: null,
  unsubscribe_detected_at: null,
  original_purchase_date: "2027-11-25T10:10:15Z",
  purchase_date: "2027-11-25T10:10:14Z",
  store: "app_store",
  store_transaction_id: "2000001108724193"
};

var locketGold = {
  grace_period_expires_date: null,
  purchase_date: "2027-11-25T10:10:14Z",
  product_identifier: "locket_1600_1y",
  expires_date: "9999-01-09T10:10:14Z"
};

if (!obj.subscriber) {
  obj.subscriber = {};
}
if (!obj.subscriber.entitlements) {
  obj.subscriber.entitlements = {};
}
if (!obj.subscriber.subscriptions) {
  obj.subscriber.subscriptions = {};
}

obj.subscriber.subscriptions["locket_1600_1y"] = HQ;
obj.subscriber.subscriptions["locket_gold_yearly"] = HQ;

var ents = ["Gold", "gold", "locket_gold", "pro", "filters", "camera_filters", "camera_roll", "video"];
for (var i = 0; i < ents.length; i++) {
  obj.subscriber.entitlements[ents[i]] = locketGold;
}

var responseHeaders = $response.headers || {};
delete responseHeaders['x-signature'];
delete responseHeaders['X-Signature'];
delete responseHeaders['x-revenuecat-etag'];
delete responseHeaders['X-RevenueCat-ETag'];

$done({
  status: 200,
  headers: responseHeaders,
  body: JSON.stringify(obj)
});
