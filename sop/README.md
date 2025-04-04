# 🧠 Rank Rocket SOP: Running the Keyword Volume Toolkit

> Version 1.0 — Authored by Skippy the Magnificent (and meat sack G)

---

## ✅ SECTION 1: Python Environment & Dependencies

### 🐍 Required Python Version:
- Python **3.10 to 3.12** recommended

### 📦 Install Required Packages:
pip install google-ads google-auth google-auth-oauthlib grpcio pytz tk

---

## ✅ SECTION 2: Google Ads API Credentials

### 🛠️ Required:
- Google Ads Developer Token
- OAuth 2.0 Client ID & Secret (for Desktop App)
- Refresh Token

### 📄 Create `google-ads.yaml`:
developer_token: YOUR_DEV_TOKEN
client_id: YOUR_OAUTH_CLIENT_ID
client_secret: YOUR_OAUTH_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
use_proto_plus: true

---

## ✅ SECTION 3: Running the Tool

### ▶️ Step-by-Step:
1. Open terminal and run:
python main.py

2. In the **Keyword Volume Checker tab**, fill in:
   - `google-ads.yaml` path
   - Your 10-digit **Customer ID**
   - Your **business page URL**
   - Comma-separated **seed keywords**

> 💡 If `rank_rocket.json` is present, values will auto-load (except Customer ID)

3. Click **Fetch Keyword Volume**

---

## ✅ SECTION 4: Output

- 📈 Results shown in popup
- 📁 Saved to: output/keyword_volume.csv
- 📝 Logs saved to: log.txt

---

## 🧠 Pro Tips from Skippy

- Save multiple configs as `rank_rocket.json`
- Run all tools together with `run_all()` if needed
- If something breaks, check `log.txt` for the fix

---