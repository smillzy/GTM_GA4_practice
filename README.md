# GA4 + GTM 電商追蹤練習專案

## 專案說明

本專案以 Pintoo 拼圖商店為情境，建立一個模擬電商網站，透過 Google Tag Manager（GTM）部署 GA4 事件追蹤，並搭配 UTM 參數設計追蹤各行銷渠道的流量來源與轉換效果。

追蹤事件涵蓋完整購物旅程：
```
瀏覽首頁 → 查看商品 → 加入購物車 → 開始結帳 → 完成購買
```

並透過 Python 模擬來自 Google、Facebook、Instagram、Email 等多渠道的使用者行為，產生可分析的數據，最終產出 GA4 數據分析報告。

---

## 使用技術

| 技術 | 用途 |
|------|------|
| Google Analytics 4（GA4） | 收集與分析使用者行為數據 |
| Google Tag Manager（GTM） | 管理與部署追蹤代碼 |
| UTM 參數 | 追蹤各行銷渠道流量來源 |
| Python | 模擬使用者流量、送出 GA4 事件 |
| GitHub Pages | 靜態網站部署 |

---

## 網站結構

| 頁面 | 功能 | 網址 |
|------|------|------|
| `index.html` | 商店首頁，展示三款商品，點擊觸發 `view_item` 事件 | [首頁](https://smillzy.github.io/GTM_GA4_practice/index.html) |
| `product.html` | 商品詳細頁，提供加入購物車與立即購買，觸發 `add_to_cart` / `begin_checkout` 事件 | [商品頁](https://smillzy.github.io/GTM_GA4_practice/product.html) |
| `cart.html` | 購物車與結帳頁，填寫資料後完成購買，觸發 `purchase` 事件 | [購物車](https://smillzy.github.io/GTM_GA4_practice/cart.html) |
| `thankyou.html` | 訂單完成頁，顯示訂單資訊與 UTM 來源 | [訂單完成](https://smillzy.github.io/GTM_GA4_practice/thankyou.html) |
| `utm_links.html` | UTM 連結產生器，提供各渠道測試連結 | [UTM 連結](https://smillzy.github.io/GTM_GA4_practice/utm_links.html) |
| `report.html` | GA4 數據分析報告，呈現流量、漏斗、商品銷售等分析 | [分析報告](https://smillzy.github.io/GTM_GA4_practice/report.html) |

---

## 如何執行模擬腳本

### 1. 安裝套件

```bash
pip install requests python-dotenv
```

### 2. 建立 `.env` 檔案

參考 `.env.example`，在專案根目錄建立 `.env`：

```
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GA4_API_SECRET=your_api_secret_here
```

> API Secret 取得方式：GA4 後台 → 管理 → 資料串流 → Measurement Protocol API secrets

### 3. 執行腳本

```bash
python simulate_traffic.py
```

腳本會模擬 1000 位使用者，來自以下渠道：

| 渠道 | 比例 |
|------|------|
| Google / CPC | 35% |
| Facebook / Social | 25% |
| Instagram / Social | 20% |
| Email | 12% |
| Direct | 8% |

每位使用者會依照真實購物漏斗的流失率，隨機觸發對應事件。
