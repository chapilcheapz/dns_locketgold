/**
 * Locket Gold RevenueCat Unlock - Hoàng Quân
 * Lightweight, Clean & Fast Version (inspired by all-in-one.conf)
 */

var obj = {};
try {
  obj = JSON.parse($response.body);
} catch (e) {
  obj = {};
}

if (!obj || typeof obj !== "object") {
  obj = {};
}

if (!obj.subscriber) {
  obj.subscriber = { entitlements: {}, subscriptions: {} };
}
if (!obj.subscriber.entitlements) obj.subscriber.entitlements = {};
if (!obj.subscriber.subscriptions) obj.subscriber.subscriptions = {};

obj.Attention = "Kích hoạt Locket Gold thành công bởi Hoàng Quân!";

var goldSub = {
  is_sandbox: false,
  ownership_type: "PURCHASED",
  billing_issues_detected_at: null,
  period_type: "normal",
  expires_date: "2099-12-31T23:59:59Z",
  grace_period_expires_date: null,
  unsubscribe_detected_at: null,
  original_purchase_date: "2024-01-01T00:00:00Z",
  purchase_date: "2024-01-01T00:00:00Z",
  store: "app_store"
};

var goldEntitlement = {
  grace_period_expires_date: null,
  purchase_date: "2024-01-01T00:00:00Z",
  product_identifier: "locket_2400_1y",
  expires_date: "2099-12-31T23:59:59Z",
  ownership_type: "PURCHASED",
  store: "app_store",
  is_sandbox: false
};

const entitlements = ["Gold", "gold", "locket_gold"];
for (let e of entitlements) {
  obj.subscriber.entitlements[e] = goldEntitlement;
}

obj.subscriber.subscriptions["locket_2400_1y"] = goldSub;

$done({
  status: 200,
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-cache, no-store, must-revalidate"
  },
  body: JSON.stringify(obj)
});
