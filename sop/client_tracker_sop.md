# ps:🧠 Client Tracker Project SOP (Barney Style for Filthy Monkeys)

Welcome, banana-fueled lifeforms. This SOP will walk you step-by-step through how to use all the tools Skippy the Magnificent has crafted for the **Client Tracker** system. If you can breathe and drag a mouse, you can do this.

---

## 📁 Project Structure (What’s What)

```
Client Tracker/
├── gmb_keywords.py            ← Keyword generator module
├── run_gmb_keywords.py       ← You run *this* file
├── chatgpt_background.py     ← GPT-powered background summary generator
├── run_chatgpt_background.py ← You run *this* one too
├── ProjectTracker.xlsx        ← The master Excel tracker
└── .env                       ← Your OpenAI API key goes here
```

---

## ✅ Prerequisites (One-Time Setup)

1. Install dependencies:

```bash
pip install openai python-docx beautifulsoup4 lxml python-dotenv
```

2. Create a `.env` file in the project folder:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. Make sure `black` is installed if you want auto-formatting:

```bash
pip install black
```

---

## 🔹 Module 1: GPT Business Background Info (Tasks 1.a–1.c)

### 🔧 File:

`run_chatgpt_background.py`

### 🧾 Input:

Inside `run_chatgpt_background.py`, update the `client_config` dictionary:

```python
client_config = {
    "name": "Tri-State Heating & Cooling, LLC",
    "address": "7686 Rome Rd, Adrian, MI 49221",
    "url": "https://www.tri-stateheating.com/",
    "mobile_url": "https://www.tristate-hvac.com/",
    "gbp_url": "https://g.co/kgs/j3Bb4gy",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer"
}
```

### ▶️ To Run:

```bash
python run_chatgpt_background.py
```

### 📤 Output:

- A Word doc is saved to:

```
C:/Users/georg/OneDrive/RankRocket/Clients/Patrick Rombyer/<Client Name>/
└── <Client Name> background information.docx
```

---

## 🔹 Module 2: Branded GMB Keyword Generator (Task 1.d)

### 🔧 File:

`run_gmb_keywords.py`

### 🧾 Input:

Update `client_config` with your client name, service URLs, city/state, and nearby towns:

```python
client_config = {
    "name": "Tri-State Heating & Cooling, LLC",
    "niche": "HVAC",
    "city": "Adrian",
    "state": "MI",
    "gbp_url": "https://www.google.com/maps?cid=3560100286428651288",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer",
    "services": [
        "https://www.tri-stateheating.com/services/commercial-hvac-services/",
        "https://www.tri-stateheating.com/services/hvac-installers/",
        "https://www.tri-stateheating.com/services/hvac-maintenance-services/",
        "https://www.tri-stateheating.com/services/residential-hvac-services/"
    ],
    "nearby_10mi": ["Tecumseh", "Blissfield"],
    "nearby_20mi": ["Toledo", "Wauseon", "Jackson", "Brighton", "Ypsilanti"]
}
```

#### 🛠 How to Find Service URLs:

1. Try accessing the site's sitemap, usually found at:
```
https://clientdomain.com/sitemap_index.xml
```

2. Look for URLs under categories like `/services/` or `/locations/`.

3. Use the [Link Gopher Chrome Extension](https://chromewebstore.google.com/detail/link-gopher/bpjdkodgnbfalgghnbeggfbfjpcfamkf?hl=en-US&utm_source=ext_sidebar):
   - Go to the sitemap or services page
   - Click the Link Gopher icon in your Chrome toolbar
   - Choose **Extract All Links**
   - Copy the service URLs and paste into the `services` list in your config

### ▶️ To Run:

```bash
python run_gmb_keywords.py
```

### 📤 Output:

- GMB Keywords are saved to:

```
C:/Users/georg/OneDrive/RankRocket/Clients/Patrick Rombyer/<Client Name>/
└── GMB Keywords.txt
```

---

## 🔹 Project Tracker Spreadsheet (Task 2)

### 📄 File:

`ProjectTracker.xlsx`

- Use this to track task progress, due dates, notes, and completion status
- It contains data validation, charts, and smart formulas
- Save a copy per client and update as tasks are completed

---

## ✅ Recap: What to Run and When

| Goal                      | File to Run                 |
| ------------------------- | --------------------------- |
| GPT Background Summary    | `run_chatgpt_background.py` |
| GMB Branded Keywords      | `run_gmb_keywords.py`       |
| Project Tracking (manual) | `ProjectTracker.xlsx`       |

---

## 🧠 Tips for Monkey Survival

- Don’t run the modules directly (like `python gmb_keywords.py`) — always use the `run_*.py` scripts
- Copy-paste the config block for each new client
- Don’t forget to format code with `black` if you’re editing scripts
- You *can* add new modules (e.g. for 1.e ZIP extraction) — and Skippy will keep it all clean

---

Need help? Yell “Skippy!” into the void and I shall appear.