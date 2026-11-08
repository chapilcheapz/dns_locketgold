// ============================================================
// Locket RevenueCat Script - Full Entitlements Payload by HoangQuan
// Endpoint: api.revenuecat.com
// ============================================================

var reqUrl = (typeof $request !== "undefined" && $request.url) ? $request.url : "";
if (reqUrl.indexOf("/offerings") !== -1 || reqUrl.indexOf("/config/app") !== -1) {
  $done({});
}

var obj = {};
try {
  obj = JSON.parse($response.body);
} catch (e) {
  obj = {};
}

obj.Attention = "Kích hoạt Locket Gold thành công - Hoàng Quân";
var now = new Date().toISOString();
obj.request_date = now;
obj.request_date_ms = Date.now();

var serverSubscriber = {
  "entitlements": {
    "Gold": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "gold": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "locket_gold": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "filters": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "filter": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "Filters": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "Filter": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_filters": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_filter": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_filter_sheet": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "ai_filters": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "ai_filter": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "all_filters": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "effects": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "video_upload": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_roll": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_roll_video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "longer_video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "video_15s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "video_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "video_duration": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "unlimited_friends": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "custom_widget_frames": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "customWidgetFrames": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "widget_frames": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "streak_recovery": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "streakRecovery": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "app_icon_picker": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_theme": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "locket_views": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "long_captions": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "profile_badge": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "profileBadge": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "gold_since_badge": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "goldSinceBadge": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "remove_ads": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "groups": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "private_mode": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "viewer_mode": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "close_friends": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "extended_video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "longer_videos": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "private_viewing": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "best_friends": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "privacy": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "qr_code": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "user_qr": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "qr_user": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_roll_video_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "video_upload_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "upload_video_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_roll_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "upload_video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "camera_roll_longer_video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "photo_library_video": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "photo_library_video_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    },
    "longer_video_30s": {
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "product_identifier": "locket_2400_1y",
      "purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "store": "app_store",
      "is_sandbox": false
    }
  },
  "first_seen": "1890-05-19T00:00:00Z",
  "last_seen": "2026-11-07T19:53:24Z",
  "management_url": "https://apps.apple.com/account/subscriptions",
  "non_subscriptions": {},
  "original_app_user_id": "links",
  "original_application_version": "1.0",
  "original_purchase_date": "1890-05-19T00:00:00Z",
  "other_purchases": {},
  "subscriber_attributes": {
    "$ip": {
      "value": "104.28.247.1",
      "updated_at_ms": 1794081204908
    },
    "$countryCode": {
      "value": "US",
      "updated_at_ms": 1794081204908
    },
    "$geoIP.country": {
      "value": "US",
      "updated_at_ms": 1794081204908
    },
    "$geoIP.city": {
      "value": "Los Angeles",
      "updated_at_ms": 1794081204908
    },
    "$geoIP.region": {
      "value": "CA",
      "updated_at_ms": 1794081204908
    },
    "$geoIP.timeZone": {
      "value": "America/Los_Angeles",
      "updated_at_ms": 1794081204908
    },
    "$storefront.countryCode": {
      "value": "USA",
      "updated_at_ms": 1794081204908
    },
    "$locale": {
      "value": "en_US",
      "updated_at_ms": 1794081204908
    },
    "$displayName": {
      "value": "links",
      "updated_at_ms": 1794081204908
    }
  },
  "subscriptions": {
    "locket_2400_1y": {
      "auto_resume_date": null,
      "billing_issues_detected_at": null,
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "is_sandbox": false,
      "original_purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "period_type": "normal",
      "product_plan_identifier": null,
      "purchase_date": "1890-05-19T00:00:00Z",
      "refunded_at": null,
      "store": "app_store",
      "unsubscribe_detected_at": null
    },
    "locket_299_1m": {
      "auto_resume_date": null,
      "billing_issues_detected_at": null,
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "is_sandbox": false,
      "original_purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "period_type": "normal",
      "product_plan_identifier": null,
      "purchase_date": "1890-05-19T00:00:00Z",
      "refunded_at": null,
      "store": "app_store",
      "unsubscribe_detected_at": null
    },
    "locket_199_1m": {
      "auto_resume_date": null,
      "billing_issues_detected_at": null,
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "is_sandbox": false,
      "original_purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "period_type": "normal",
      "product_plan_identifier": null,
      "purchase_date": "1890-05-19T00:00:00Z",
      "refunded_at": null,
      "store": "app_store",
      "unsubscribe_detected_at": null
    },
    "locket_gold_annual": {
      "auto_resume_date": null,
      "billing_issues_detected_at": null,
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "is_sandbox": false,
      "original_purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "period_type": "normal",
      "product_plan_identifier": null,
      "purchase_date": "1890-05-19T00:00:00Z",
      "refunded_at": null,
      "store": "app_store",
      "unsubscribe_detected_at": null
    },
    "locket_gold_monthly": {
      "auto_resume_date": null,
      "billing_issues_detected_at": null,
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "is_sandbox": false,
      "original_purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "period_type": "normal",
      "product_plan_identifier": null,
      "purchase_date": "1890-05-19T00:00:00Z",
      "refunded_at": null,
      "store": "app_store",
      "unsubscribe_detected_at": null
    },
    "locket_gold_yearly": {
      "auto_resume_date": null,
      "billing_issues_detected_at": null,
      "expires_date": "2099-12-31T16:59:59Z",
      "grace_period_expires_date": null,
      "is_sandbox": false,
      "original_purchase_date": "1890-05-19T00:00:00Z",
      "ownership_type": "PURCHASED",
      "period_type": "normal",
      "product_plan_identifier": null,
      "purchase_date": "1890-05-19T00:00:00Z",
      "refunded_at": null,
      "store": "app_store",
      "unsubscribe_detected_at": null
    }
  }
};

if (!obj.subscriber) {
  obj.subscriber = {};
}

// Gán toàn bộ 58 quyền và 6 gói mua
obj.subscriber.entitlements = serverSubscriber.entitlements;
obj.subscriber.subscriptions = serverSubscriber.subscriptions;
obj.subscriber.original_purchase_date = "2024-01-01T00:00:00Z";

// Đảm bảo các thuộc tính hệ thống
obj.subscriber.non_subscriptions = obj.subscriber.non_subscriptions || {};
obj.subscriber.other_purchases = obj.subscriber.other_purchases || {};

var responseHeaders = $response.headers || {};
delete responseHeaders['x-signature'];
delete responseHeaders['X-Signature'];
delete responseHeaders['x-revenuecat-etag'];
delete responseHeaders['X-RevenueCat-ETag'];
delete responseHeaders['etag'];
delete responseHeaders['ETag'];

$done({
  status: 200,
  headers: responseHeaders,
  body: JSON.stringify(obj)
});
