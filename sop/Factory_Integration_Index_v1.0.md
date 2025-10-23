# 🧠 Rank Rocket SEO Factory Integration Index
**Version:** 1.0  
**Date:** October 2025  
**Authors:** Skippy the Magnificent & Big G  

---

## 1. Overview
This index maps all Rank Rocket repositories into the unified **SEO Factory** architecture—also known as **Mission Control / Flight Deck**.  
Each repo corresponds to one or more "machines" in the production line, following the **Tier / Step** model and **DBR (Drum‑Buffer‑Rope)** scheduling.

The goal: **Fire‑and‑Forget SEO** — one YAML file to orchestrate intake, sub‑assemblies, publishing, and QA.

---

## 2. Factory Architecture Snapshot
| Stage | Description | Representative Repos |
|--------|--------------|----------------------|
| **Step 1 – Raw Materials** | Intake, configuration, and source data collection. | `skippy_yaml_builder`, `ethical_web_scraper` |
| **Step 2 – Sub‑Assemblies** | Generate campaign assets and reusable modules (keywords, schema, content, media). | `client-tracker`, `llm_txt_generator`, `rank-rocket-schema-creator`, `qr_watermark_wizard`, `url-magic` |
| **Step 3 – Final Assembly** | Assemble and deploy campaigns (WP + Cloud). | `push_it_real_good`, `cloud-stack-generator`, `Location_Page_Generator` |
| **Scheduling & Control** | Finite scheduling, capacity, cadence. | `rank_rocket_calendar_stacker` |
| **Quality Assurance / Telemetry** | Performance audits, CWV, reporting. | Future module (planned: `ams_optimizer_plugin`) |

---

## 3. Repository Details

### 🧩 3.1 skippy_yaml_builder
**Role:** Client Intake Machine  
**Stage:** Step 1 – Raw Materials  
**Inputs:** Operator‑entered business data  
**Outputs:** `/clients/<slug>/client.yaml`  
**Dependencies:** PyQt6 / pyyaml / dotenv  
**Integration Notes:**  
- Primary entrypoint for onboarding.  
- YAML is consumed by all downstream modules.  
- Should write validated configs into `/clients/` and push signals to scheduler.

---

### 🕵️‍♀️ 3.2 ethical_web_scraper
**Role:** Data Acquisition Engine  
**Stage:** Step 1 – Raw Materials  
**Inputs:** Approved partner URLs or CSVs  
**Outputs:** `scraped_data.json`, `image_links.csv`  
**Dependencies:** requests, beautifulsoup4  
**Integration Notes:**  
- Use for media validation or content sourcing.  
- Feeds image/media lists into `/inventory/media/`.

---

### ⚙️ 3.3 client-tracker
**Role:** Core Sub‑Assembly Hub  
**Stage:** Step 2 – Sub‑Assemblies  
**Inputs:** `client.yaml`  
**Outputs:** Keyword CSVs, background briefs, FAQ drafts, schema JSONs  
**Dependencies:** tkinter, openai, google‑ads, pandas  
**Integration Notes:**  
- Contains modular generators: keywords, GBP posts, FAQ builder.  
- Migrate into `/modules/` folder in the Factory; refactor UI → PyQt tab.

---

### 🧠 3.4 llm_txt_generator
**Role:** Content Generator (Briefs / Copy)  
**Stage:** Step 2 – Sub‑Assemblies  
**Inputs:** YAML brand + service info  
**Outputs:** `llms.txt`, HTML or Markdown drafts  
**Dependencies:** openai, python‑dotenv  
**Integration Notes:**  
- Used to create background summaries and long‑form drafts.  
- Should feed outputs into schema and WordPress pipelines.

---

### 🧱 3.5 rank-rocket-schema-creator
**Role:** Schema Wizard  
**Stage:** Step 2 – Sub‑Assemblies  
**Inputs:** YAML entities (NAP, services, products, FAQ)  
**Outputs:** JSON‑LD blocks (`schema/<type>.json`)  
**Dependencies:** json, os, openai (optional for dynamic generation)  
**Integration Notes:**  
- Create LocalBusiness, Service, FAQPage, and Product schemas.  
- Combine with content generator outputs for rich entity linking.

---

### 🖼️ 3.6 qr_watermark_wizard
**Role:** Media Prep / Branding  
**Stage:** Step 2 – Sub‑Assemblies  
**Inputs:** Source images, QR URLs  
**Outputs:** Branded, watermarked images  
**Dependencies:** pillow, qrcode, PyQt6 (UI)  
**Integration Notes:**  
- Automates image watermarking for all campaign graphics.  
- Should integrate into a batch media pipeline triggered from scheduler.

---

### 🔗 3.7 url-magic
**Role:** URL / Slug Normalizer  
**Stage:** Step 2 – Sub‑Assemblies  
**Inputs:** Raw URLs, text inputs  
**Outputs:** Cleaned URLs or slugs  
**Dependencies:** requests, dotenv  
**Integration Notes:**  
- Use for slug standardization in WP & Cloud Stacks.  
- Should be imported as lightweight utility module.

---

### 🧮 3.8 rank_rocket_calendar_stacker
**Role:** Cadence Engine / DBR Rope  
**Stage:** Scheduling Layer  
**Inputs:** Monthly targets (from Excel or scheduler)  
**Outputs:** Time‑phased task list  
**Dependencies:** pandas, datetime  
**Integration Notes:**  
- Provides repeating cadence logic (e.g., 2 stacks per month).  
- Merge with DBR finite scheduler module to manage throughput.

---

### 🚀 3.9 cloud-stack-generator
**Role:** Cloud Stack Builder  
**Stage:** Step 3 – Final Assembly  
**Inputs:** Content pages, schema, interlink map, YAML  
**Outputs:** Static HTML stacks deployed to S3 / GCS / Wasabi  
**Dependencies:** boto3, google‑cloud‑storage, pathlib  
**Integration Notes:**  
- Core deploy engine for cloud stacks.  
- Should log all actions in `/deploy/logs/`.

---

### 🔧 3.10 push_it_real_good
**Role:** WordPress Publisher  
**Stage:** Step 3 – Final Assembly  
**Inputs:** HTML content, featured images, metadata, schema  
**Outputs:** Published WP pages / posts + logs  
**Dependencies:** requests, wordpress‑api, python‑dotenv  
**Integration Notes:**  
- Must authenticate via WP Application Passwords.  
- Should confirm existing slugs to prevent duplicates.  
- Logs go to `/deploy/wp/`.

---

### 🌆 3.11 Location_Page_Generator
**Role:** City / Service Page Builder  
**Stage:** Step 3 – Final Assembly  
**Inputs:** YAML services + cities lists  
**Outputs:** SEO‑optimized HTML pages + JSON‑LD schema  
**Dependencies:** openai, pyyaml, pandas  
**Integration Notes:**  
- Generates 600‑word pages per city with embedded schema.  
- Feeds directly into `push_it_real_good` for publication.

---

## 4. Integration Flow Summary

```
[YAML Builder] → [Scheduler] → [Client Tracker Modules]
                   ↓
         [LLM + Schema + Media Prep]
                   ↓
     [URL Magic] → [WP Publisher / Cloud Stack]
                   ↓
               [QA + Reports]
```

---

## 5. Commands & Execution Map (CLI examples)

| Function | Example Command |
|-----------|-----------------|
| Create new client YAML | `python skippy_yaml_builder.py` |
| Run keyword generator | `python client-tracker/keyword_volume_ui.py` |
| Generate schema | `python rank-rocket-schema-creator/schema_creator.py` |
| Generate content | `python llm_txt_generator/generate.py` |
| Build Cloud Stack | `python cloud-stack-generator/build_stack.py` |
| Publish to WordPress | `python push_it_real_good/post_pusher.py` |
| Generate local pages | `python Location_Page_Generator/location_page_generator.py` |
| Watermark media | `python qr_watermark_wizard/main.py` |
| Normalize URLs | `python url-magic/url_magic.py` |

---

## 6. Next Steps (Factory Consolidation Roadmap)
1. **Create umbrella repo:** `/RankRocket_Factory/`
2. **Submodule all existing repos** into `/machines/<repo-name>/`
3. **Standardize imports** using relative paths and unified `client.yaml`
4. **Add orchestrator core:** DBR Scheduler + BoM Validator
5. **Unify logging:** `/logs/factory.log` (timestamped per module)
6. **Develop PyQt6 UI shell:** tabs for each major step
7. **Implement report exports:** `/schedules/`, `/reports/`, `/deploy/`
8. **Add version control discipline:** Semantic versioning and doc updates per sprint

---

**End of Document**
