import requests
import uuid
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID")
API_SECRET = os.getenv("GA4_API_SECRET")
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

def send_event(client_id, session_id, event_name, params, debug=False):
    payload = {
        "client_id": client_id,
        "events": [{
            "name": event_name,
            "params": {
                "session_id": session_id,
                "engagement_time_msec": str(random.randint(1000, 8000)),
                "debug_mode": 1 if debug else 0,
                **params
            }
        }]
    }
    r = requests.post(URL, json=payload)
    if debug:
        print(f"  HTTP {r.status_code}")

def simulate_user(user_num):
    client_id = str(uuid.uuid4())
    session_id = str(random.randint(1000000, 9999999))
    utm = pick_utm()
    product = pick_product()

    # UTM 放進網址，GA4 才能識別為流量來源
    base_url = "https://smillzy.github.io/ga4-ecommerce-tracking-demo/"
    utm_url = (
        f"{base_url}?utm_source={utm['utm_source']}"
        f"&utm_medium={utm['utm_medium']}"
        f"&utm_campaign={utm['utm_campaign']}"
    )

    item = {
        "item_id": product["item_id"],
        "item_name": product["item_name"],
        "price": product["price"],
        "quantity": 1
    }

    # 1. 所有人瀏覽首頁
    send_event(client_id, session_id, "page_view", {
        "page_location": utm_url,
        "page_title": "Pintoo 拼圖商店",
    })

    # 2. 70% 查看商品
    if random.random() < 0.70:
        send_event(client_id, session_id, "view_item", {
            "page_location": utm_url,
            "currency": "TWD",
            "value": product["price"],
            "items": [item],
        })

        # 3. 45% 加入購物車
        if random.random() < 0.45:
            send_event(client_id, session_id, "add_to_cart", {
                "page_location": utm_url,
                "currency": "TWD",
                "value": product["price"],
                "items": [item],
            })

            # 4. 55% 進入結帳
            if random.random() < 0.55:
                send_event(client_id, session_id, "begin_checkout", {
                    "page_location": utm_url,
                    "currency": "TWD",
                    "value": product["price"],
                    "items": [item],
                })

                # 5. 70% 完成購買
                if random.random() < 0.70:
                    send_event(client_id, session_id, "purchase", {
                        "page_location": utm_url,
                        "transaction_id": "TXN-" + str(random.randint(100000, 999999)),
                        "currency": "TWD",
                        "value": product["price"],
                        "items": [item],
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

print("\n模擬完成！請到 GA4 後台查看：")
print("   - 即時報表：立即可見")
print("   - 事件報表：24~48小時後顯示")
print("   - 流量來源：報表 > 獲客 > 流量獲取")


def send_debug_test():
    """送一筆測試事件到 GA4 DebugView"""
    client_id = "debug-test-user-001"
    session_id = "9999999"
    url = "https://smillzy.github.io/ga4-ecommerce-tracking-demo/?utm_source=debug&utm_medium=test&utm_campaign=debug_test"
    send_event(client_id, session_id, "page_view", {"page_location": url, "page_title": "Debug Test"}, debug=True)
    send_event(client_id, session_id, "add_to_cart", {"page_location": url, "currency": "TWD", "value": 299}, debug=True)
    print("Debug 測試事件已送出！請去 GA4 → 管理 → DebugView 查看")

if __name__ == "__main__":
    send_debug_test()
