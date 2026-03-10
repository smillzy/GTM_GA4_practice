import requests
import uuid
import random
import time

MEASUREMENT_ID = "G-8BB44LWN0M"
API_SECRET = "WD7qW4l3QJ6Wg3C5SoTu1g"
URL = f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"

# UTM 流量來源設定
UTM_SOURCES = [
    {"utm_source": "google",     "utm_medium": "cpc",      "utm_campaign": "spring_sale",   "weight": 35},
    {"utm_source": "facebook",   "utm_medium": "social",   "utm_campaign": "fb_post_0310",  "weight": 25},
    {"utm_source": "instagram",  "utm_medium": "social",   "utm_campaign": "ig_story_0310", "weight": 20},
    {"utm_source": "email",      "utm_medium": "email",    "utm_campaign": "newsletter_mar","weight": 12},
    {"utm_source": "(direct)",   "utm_medium": "(none)",   "utm_campaign": "(direct)",      "weight": 8},
]

PRODUCTS = [
    {"item_id": "P001", "item_name": "AI學習筆記",   "price": 299},
    {"item_id": "P002", "item_name": "設計插畫拼圖", "price": 499},
    {"item_id": "P003", "item_name": "世界地圖拼圖", "price": 599},
]

def pick_utm():
    weights = [u["weight"] for u in UTM_SOURCES]
    return random.choices(UTM_SOURCES, weights=weights, k=1)[0]

def pick_product():
    return random.choice(PRODUCTS)

def send_event(client_id, event_name, params):
    payload = {
        "client_id": client_id,
        "events": [{
            "name": event_name,
            "params": {
                "session_id": str(random.randint(1000000, 9999999)),
                "engagement_time_msec": str(random.randint(1000, 8000)),
                **params
            }
        }]
    }
    requests.post(URL, json=payload)

def simulate_user(user_num):
    client_id = str(uuid.uuid4())
    utm = pick_utm()
    product = pick_product()

    utm_params = {
        "source": utm["utm_source"],
        "medium": utm["utm_medium"],
        "campaign": utm["utm_campaign"],
    }

    item = {
        "item_id": product["item_id"],
        "item_name": product["item_name"],
        "price": product["price"],
        "quantity": 1
    }

    # 1. 所有人瀏覽首頁
    send_event(client_id, "page_view", {
        "page_location": "https://smillzy.github.io/GTM_GA4_practice/",
        "page_title": "Pintoo 拼圖商店",
        **utm_params
    })

    # 2. 70% 查看商品
    if random.random() < 0.70:
        send_event(client_id, "view_item", {
            "currency": "TWD",
            "value": product["price"],
            "items": [item],
            **utm_params
        })

        # 3. 45% 加入購物車
        if random.random() < 0.45:
            send_event(client_id, "add_to_cart", {
                "currency": "TWD",
                "value": product["price"],
                "items": [item],
                **utm_params
            })

            # 4. 55% 進入結帳
            if random.random() < 0.55:
                send_event(client_id, "begin_checkout", {
                    "currency": "TWD",
                    "value": product["price"],
                    "items": [item],
                    **utm_params
                })

                # 5. 70% 完成購買
                if random.random() < 0.70:
                    send_event(client_id, "purchase", {
                        "transaction_id": "TXN-" + str(random.randint(100000, 999999)),
                        "currency": "TWD",
                        "value": product["price"],
                        "items": [item],
                        **utm_params
                    })

    source_label = utm["utm_source"] + "/" + utm["utm_medium"]
    print(f"[{user_num:4d}] {client_id[:8]}... | {source_label:<25} | {product['item_name']}")

# ── 執行模擬 ──────────────────────────────────
TOTAL_USERS = 1000

print(f"開始模擬 {TOTAL_USERS} 位使用者...\n")
print(f"{'#':>4}  {'Client ID':<12}  {'流量來源':<25}  {'商品'}")
print("-" * 65)

for i in range(1, TOTAL_USERS + 1):
    simulate_user(i)
    time.sleep(0.05)

print("\n✅ 模擬完成！請到 GA4 後台查看：")
print("   - 即時報表：立即可見")
print("   - 事件報表：24~48小時後顯示")
print("   - 流量來源：報表 > 獲客 > 流量獲取")
