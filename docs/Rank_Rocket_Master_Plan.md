# Skippy Mission Control — Rank Rocket Flight Deck Blueprint
**Version:** 1.0  
**Date:** October 2025  
**Authors:** Skippy the Magnificent & Big G  

---

## 1) Purpose
Unify all Rank Rocket SEO tools into a single **Flight Deck** that orchestrates intake → production → deployment → QA using a manufacturing-style pipeline (Tiers & Steps) with Drum‑Buffer‑Rope (DBR) finite scheduling. One YAML to rule them all.

---

## 2) Scope (MVP)
- Client intake via YAML (Cloud Stacker UI or YAML Builder)
- Inventory/BoM validation for campaign types (SEO NEO, Cloud Stack, Google Stack, GBP ops, AMPiFire)
- DBR finite scheduler (capacity by owner/month, buffers, bottleneck alerts)
- Sub-assembly automations: Keywords, PAA, Background summaries, Schema blocks, Media prep
- Final assembly automations: WordPress publishing, Cloud Stack deployments
- QA & telemetry: Core Web Vitals checks, basic Analytics/GSC pulls
- Outputs: Excel/CSV schedule, HTML/DOCX briefs, deployed static stacks

Out of scope (MVP): Full web app, OAuth user management, enterprise RBAC, deep BI dashboards.

---

## 3) System Architecture (High Level)

```
        ┌──────────────────────┐
        │   Client Intake UI   │  (Cloud Stacker / YAML Builder)
        └─────────┬────────────┘
                  │ YAML (client.yaml)
                  ▼
     ┌───────────────────────────────┐
     │  Flight Deck Orchestrator     │  (Mission Control: Python core)
     │  - DBR Finite Scheduler       │
     │  - BoM/Inventory Validator    │
     │  - Runbook / Task Router      │
     └───┬───────────┬───────────┬───┘
         │           │           │
         │           │           │
   ┌─────▼───┐ ┌─────▼───┐ ┌─────▼─────┐
   │ Step 1  │ │ Step 2  │ │ Step 3     │
   │ Raw Mat │ │ SubAsm  │ │ Final Asm  │
   │ (Inputs)│ │ (Modules)││ (Deploy/QA)│
   └─────┬───┘ └─────┬───┘ └─────┬─────┘
         │           │           │
   ┌─────▼────┐ ┌────▼─────┐ ┌───▼─────────┐
   │ Keyword  │ │ Content  │ │ Publisher   │
   │ Volume   │ │ + Schema │ │ (WP/Stacks) │
   └──────────┘ └──────────┘ └─────────────┘
```

**Data Stores**
- `/clients/<slug>/client.yaml` (source-of-truth)
- `/inventory/` (content buckets, accounts, schema templates, media lists)
- `/schedules/` (Excel/CSV exports, dashboards)
- `/deploy/` (stack outputs, WP publish logs)

---

## 4) Tiers & Steps (Production Model)
- **Tier = Performance class:** Tier 1 Economy, Tier 2 Sedan, Tier 3 Yangwang U9 Xtreme (applies LOE multipliers, buffer sizes)
- **Step = Stage:** Step 1 Raw Materials → Step 2 Sub‑Assemblies → Step 3 Final Assembly

**Examples**
- Step 1 Raw Materials: Gmail accounts, logos, GA4/GSC IDs, keyword seeds
- Step 2 Sub‑Assemblies: Gmail + app password, watermarked images, city/service copy drafts, schema JSON blocks
- Step 3 Final Assembly: SEO NEO campaign package, Cloud/Google Stacks, AMPiFire submission, WP content push

---

## 5) Core Modules (with Inputs/Outputs)

### 5.1 Client Intake
- **Inputs:** User forms or YAML file
- **Outputs:** `client.yaml` (NAP, services, cities, stack settings, credentials refs, tiers), folder skeleton

### 5.2 Inventory / BoM Validator
- **Inputs:** `client.yaml`, BoM templates per campaign type
- **Logic:** Confirms availability of required components by Step/Tier
- **Outputs:** BoM readiness report; missing items checklist

### 5.3 DBR Finite Scheduler
- **Inputs:** Task catalog (Tier 2 Growth SEO playbook), owner capacity (hrs/month), month targets, buffers
- **Logic:** Allocate Planned LOE within finite capacity; create start/due dates; flag drum overloads
- **Outputs:** `schedule.xlsx`, color-coded dashboard, alerts

### 5.4 Keyword Volume (Google Ads)
- **Inputs:** seed keywords, location, language
- **Outputs:** ideas + search volumes CSV; clusters (optional)

### 5.5 PAA Fetcher (SERP/SerpAPI)
- **Inputs:** topics/services/cities
- **Outputs:** normalized PAA list; optional Q&A drafts

### 5.6 Background Summary Generator (LLM)
- **Inputs:** brand/city/service context from YAML
- **Outputs:** background briefs, page outlines, talking points (HTML/DOCX/MD)

### 5.7 Schema Wizard
- **Inputs:** YAML entities, services, products, FAQs
- **Outputs:** JSON‑LD blocks per page type (LocalBusiness, Service, FAQPage, Product, BreadcrumbList)

### 5.8 Media Scraper / Image Prep
- **Inputs:** source URLs or partner pages
- **Outputs:** validated image URLs; watermarked/renamed files

### 5.9 Publisher: WordPress ("Push It Real Good")
- **Inputs:** HTML content, meta, images, schema
- **Outputs:** Published pages/posts; slugs; response logs

### 5.10 Publisher: Cloud Stack Deployer
- **Inputs:** page JSON/HTML, assets, interlink maps
- **Outputs:** S3/GCS/Azure static sites with interlinks; deployment logs

### 5.11 QA: AMS Optimizer / CWV Checks
- **Inputs:** page URLs
- **Outputs:** PSI metrics, optimization notes; pass/fail flags

### 5.12 Analytics Collector (Phase 2)
- **Inputs:** GSC/GA4 pulls
- **Outputs:** KPI snapshot back to dashboard

---

## 6) Data Model (MVP)
**Tables/Files**
- `Tasks`: ID, Name, Tier, Step, Category, Default_Effort_hr
- `Schedule`: Task_ID, Owner, Client, Month, Planned_Start, Planned_End, Planned_LOE_hr, Actual_LOE_hr, Status
- `Resources`: Owner, Month, Available_hr, Buffer_hr, Utilization_%
- `BoM_Items`: Task_ID, Component_Name, Step_Required, Source_Type, Availability_Status, Inventory_ID
- `Inventory`: Component_ID, Type, Tier_Capable, Step, Status, Location
- `Clients`: Client_ID, Name, Active_Tier, Priority, YAML_Path

---

## 7) YAML Blueprint (fields consumed by modules)
```yaml
client:
  name: "Salvo Metal Works"
  slug: "salvo-metal-works"
  nap:
    phone: "+1-866-713-3396"
    address: "566 W 5th Ave, Naperville, IL 60563"
  web:
    domain: "salvometalworks.com"
    money_site_url: "https://salvometalworks.com"
    same_as:
      - "https://www.facebook.com/SalvoMetalWorks"
  services:
    - "custom-copper-dormers"
    - "chimney-shrouds"
  cities:
    - "naperville-il"
    - "aurora-il"
  tier: 2
  campaigns:
    seo_neo:
      enabled: true
      keywords_seed: ["copper dormers", "chimney shroud"]
    cloud_stack:
      enabled: true
      provider: "aws"
      bucket_prefix: "stack"
  credentials_ref:
    aws_profile: "my-aws"
    wp:
      base_url: "https://example.com"
      user: "api_user"
      app_password_ref: "vault://wp/app_pw"
```

---

## 8) Secrets & Profiles
- **AWS:** Access Key ID/Secret (local encrypted profile), default region
- **Google Ads:** `google-ads.yaml` (Developer Token, Client ID/Secret, Refresh Token)
- **OpenAI/LLM:** API key via `.env`
- **WordPress:** Application Password stored in local vault; only reference in YAML

---

## 9) Orchestration Workflows

### 9.1 Onboard → Plan → Build → Ship
1. Intake client → generate `client.yaml`
2. BoM Validator → missing items list
3. Scheduler → allocate tasks for target month with buffers
4. Sub‑assemblies run (Keywords, PAA, Briefs, Schema, Media)
5. Final assembly (WP publish, Cloud Stack deploy)
6. QA (AMS Optimizer/PSI) → fixes
7. Export reports; archive artifacts

### 9.2 Monthly Cycle
- Recompute capacity → roll incomplete tasks
- Regenerate GBP posts / content batches
- Add 2–4 Cloud/Google stacks (Tier-based)
- Pull GSC/GA4 deltas; adjust roadmap

---

## 10) UI Plan (PyQt6 recommended)

**Main Navigation (tabs):**
- Dashboard (Capacity heatmap, drum alert, buffer health)
- Clients (YAML loader/editor)
- Inventory (BoM readiness)
- Scheduler (month board + Gantt-like grid)
- Sub-Assemblies (Keywords, PAA, Schema, Media)
- Final Assembly (Publishers: WP, Stacks)
- QA & Telemetry (CWV checks, logs)

**Wireframe (text):**
```
┌─────────────────────────────────────────────────────────┐
│  Skippy Mission Control                                 │
├───────────────┬─────────────────────────────────────────┤
│ Clients       │ [Client: ▼] [Load YAML] [Edit] [Save]   │
│ Inventory     │ BoM:  ███ Ready  ██ Missing  ░ Pending  │
│ Scheduler     │ Month: 09-2025  [Recalc]  Drum: GREEN   │
│ Sub-Assemblies│ [Keywords][PAA][Briefs][Schema][Media]  │
│ Final Assembly│ [Publish WP] [Deploy Stacks] [AMPiFire] │
│ QA & Telemetry│ PSI: LCP 2.9s  CLS 0.00  [Run Checks]   │
└───────────────┴─────────────────────────────────────────┘
```

---

## 11) Tech Stack & Dependencies (MVP)
- **Python 3.11+**, **PyQt6** (UI) or Tkinter (existing), **pandas**, **openpyxl**, **numpy**
- **google-ads**, **google-api-python-client**, **google-auth-oauthlib**
- **requests**, **pillow**, **python-dotenv**
- **openai** (LLM)
- Optional: **APScheduler** (job runner), **FastAPI** (future API), **sqlite3**

`requirements.txt` (baseline):
```
pillow
requests
openai
python-dotenv
google-ads
google-api-python-client
google-auth
google-auth-oauthlib
google-auth-httplib2
pandas
openpyxl
numpy
pyqt6
colorama
```

---

## 12) Milestones & Deliverables

**M1 — Skeleton (1–2 days)**
- Repo skeleton, venv, requirements, YAML schema, folder scaffolder
- Minimal PyQt6 shell with tabs + YAML load/save
- Task catalog import; capacity model stub

**M2 — Scheduler (2–3 days)**
- DBR logic (load %, buffers, start/end)
- `schedule.xlsx` export; month heatmap in UI

**M3 — Sub‑Assembly Hooks (2–3 days)**
- Keyword Volume, PAA, Briefs, Schema modules wired to selected client

**M4 — Final Assembly (2–3 days)**
- Push It Real Good (WP) + Cloud Stack deploy buttons + logs

**M5 — QA & Telemetry (1–2 days)**
- PSI check hook; AMS Optimizer summary panel

**M6 — Hardening & Docs**
- Error handling, logging, versioning; “Operator’s Handbook”

---

## 13) Risks & Mitigations
- **API quota/keys:** Centralize in profiles; fail‑gracefully with queued retries
- **Capacity overcommit:** 85% drum guardrail; visible alerts; hire/automation trigger
- **BoM gaps block builds:** Inventory dashboard + one‑click task to produce missing parts
- **UI debt:** Start simple; avoid premature web app; evolve as needed

---

## 14) Definition of Done (MVP)
- Load any client YAML and produce a **valid monthly schedule** with BoM validation
- Run at least **3 sub‑assemblies** and **1 final assembly** from the UI
- Export **schedule.xlsx** + **deployment logs** per client
- Pass **QA checks** on at least one published asset (CWV pass/fail visible)

---

## 15) Versioning & Folders
- Semantic versioning `v1.0.0` → increment minors for features, patch for fixes
- Folders:
```
/clients/<slug>/client.yaml
/inventory/ (assets, schema, media lists)
/modules/ (keywords, paa, briefs, schema, media, publishers)
/orchestrator/ (scheduler, bom, runbook)
/ui/
/schedules/
/deploy/
/logs/
```

---

## 16) Quickstart (Operator Notes)
1. Create or load `client.yaml`
2. Run **BoM Check** → fix missing items
3. Open **Scheduler** → choose month, recalc, accept plan
4. Execute **Sub‑Assemblies** (auto‑fill checkboxes as done)
5. Execute **Final Assembly** (WP/Stacks)
6. Run **QA & Telemetry** → resolve issues → archive
