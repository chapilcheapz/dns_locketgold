/**
 * Locket RevenueCat Script - Hoàng Quân
 * Matches: ^https:\/\/api\.revenuecat\.com\/.+\/(receipts|subscribers)
 */

var url = (typeof $request !== "undefined" && $request.url) ? $request.url : "";

// Bỏ qua offerings và config
if (url.indexOf("/offerings") !== -1 || url.indexOf("/config/app") !== -1) {
  $done({});
} else {
  var obj = {};
  try {
    obj = JSON.parse($response.body);
  } catch (e) {
    obj = {};
  }

  obj.Attention = "Kích hoạt Locket Gold VIP thành công - Hoàng Quân";
  var now = new Date().toISOString();
  var expireDate = "2099-12-31T23:59:59Z";
  var purchaseDate = "2024-01-01T00:00:00Z";

  if (!obj.subscriber) {
    obj.subscriber = {};
  }
  if (!obj.subscriber.entitlements) {
    obj.subscriber.entitlements = {};
  }
  if (!obj.subscriber.subscriptions) {
    obj.subscriber.subscriptions = {};
  }

  var goldEntitlement = {
    "expires_date": expireDate,
    "grace_period_expires_date": null,
    "product_identifier": "locket_1600_1y",
    "purchase_date": purchaseDate
  };

  var goldSub = {
    "auto_resume_date": null,
    "billing_issues_detected_at": null,
    "expires_date": expireDate,
    "grace_period_expires_date": null,
    "is_sandbox": false,
    "original_purchase_date": purchaseDate,
    "ownership_type": "PURCHASED",
    "period_type": "normal",
    "product_plan_identifier": null,
    "purchase_date": purchaseDate,
    "refunded_at": null,
    "store": "app_store",
    "unsubscribe_detected_at": null
  };

  // Cấp quyền Gold chuẩn cho tất cả các key
  var entKeys = ["Gold", "gold", "locket_gold", "pro", "filters", "filter", "all_filters", "camera_filters", "camera_roll", "video"];
  for (var i = 0; i < entKeys.length; i++) {
    obj.subscriber.entitlements[entKeys[i]] = goldEntitlement;
  }

  obj.subscriber.subscriptions["locket_1600_1y"] = goldSub;
  obj.subscriber.subscriptions["locket_2400_1y"] = goldSub;
  obj.subscriber.subscriptions["locket_gold_yearly"] = goldSub;
  obj.subscriber.subscriptions["locket_199_1m"] = goldSub;

  obj.subscriber.original_purchase_date = purchaseDate;
  obj.subscriber.non_subscriptions = obj.subscriber.non_subscriptions || {};
  obj.subscriber.other_purchases = obj.subscriber.other_purchases || {};

  var headers = $response.headers || {};
  delete headers["x-signature"];
  delete headers["X-Signature"];
  delete headers["x-revenuecat-etag"];
  delete headers["X-RevenueCat-ETag"];
  delete headers["etag"];
  delete headers["ETag"];

  $done({
    status: 200,
    headers: headers,
    body: JSON.stringify(obj)
  });
}
