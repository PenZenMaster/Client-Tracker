# 🧭 Product Requirements Document
**Project Title:** SEO Capacity Planner & Finite Scheduler  
**Version:** v0.4  
**Author:** Skippy the Magnificent with Big G  
**Date:** October 2025  

---

## 1. Purpose & Vision
To create a **finite-capacity, manufacturing-style operations system** for SEO production.  
This system treats SEO deliverables as products built in a factory pipeline, where each task passes through defined production **Steps** (Raw Materials → Sub-Assemblies → Final Assembly) and belongs to a performance **Tier** (Economy → Sedan → Yangwang U9 Xtreme).

The tool provides visibility into:
- Workload by resource, client, and month  
- Progress by production stage  
- Capacity utilization and bottlenecks  
- Planned vs Actual LOE (Level of Effort)  
- Inventory readiness for campaign BoMs (Bill of Materials)  

---

## 2. Framework Overview  

| Concept | Definition | Analogy |
|----------|-------------|---------|
| **Tier** | Defines *performance class* — the sophistication and expected output quality | Economy Car / Sedan / Supercar |
| **Step** | Defines *production stage* — how far along an asset is built | Raw Material → Sub-Assembly → Final Assembly |
| **BoM (Bill of Materials)** | Lists all digital parts required to build one campaign deliverable | Parts list for a car build |
| **DBR Logic** | Drum = constraint / Buffer = safety margin / Rope = release signal | Factory throughput control |
| **Capacity Planning** | Allocation of human + automation hours across months | Finite scheduling by machine hours |

---

## 3. Tier Definitions (Performance Classes)

| Tier | Description | Complexity | LOE Multiplier | Target Outcome |
|------|--------------|-------------|----------------|----------------|
| **Tier 1 – Economy** | Entry-level SEO system emphasizing speed and cost-efficiency | Low | × 1.0 | Crawlability + baseline visibility |
| **Tier 2 – Full-Size Sedan** | Balanced SEO engine integrating multiple subsystems | Medium | × 1.5 – 2.0 | Consistent rankings + brand growth |
| **Tier 3 – Yangwang U9 Xtreme** | High-performance, AI-enhanced authority build | High | × 3.0 – 4.0 | Dominant SERP presence + AI Overview eligibility |

---

## 4. Production Steps (Stages of Work)

| Step | Description | Example Deliverables |
|------|--------------|---------------------|
| **1 – Raw Materials** | Foundational digital assets required to begin production | Gmail accounts, logos, domains, GA4 tags |
| **2 – Sub-Assemblies** | Intermediate assets combining raw materials into usable modules | Watermarked images, blog drafts, configured accounts |
| **3 – Final Assembly** | Fully integrated, QA-ready deliverables ready for execution | SEO NEO Campaigns, Cloud Stacks, GBP Launch Bundles |

---

## 5. Bill of Materials (BoM) Example

| Campaign Type | Component | Step | Tier | Source | Availability |
|----------------|-----------|------|------|---------|--------------|
| SEO NEO Campaign | Gmail Account + App Password | Sub-Assembly | 1–3 | Inventory | ✅/❌ |
| SEO NEO Campaign | Content Bucket (articles + images) | Sub-Assembly | 2 / 3 | Content Library | ✅/❌ |
| SEO NEO Campaign | Keyword List & Entity Map | Raw Material | 2 / 3 | Research Sheet | ✅/❌ |
| SEO NEO Campaign | Schema Template | Raw Material | 1–3 | Template Repo | ✅/❌ |
| SEO NEO Campaign | Reporting Profile | Final Assembly | 2 / 3 | Analytics Stack | ✅/❌ |

Before scheduling, the system checks that all required BoM components are available or queued.

---

## 6. Core Functional Logic
1. **BoM Validation:** Ensure all required components exist before advancing to the next Step.  
2. **Capacity Allocation:** Assign Planned LOE (hrs) to owners; enforce finite scheduling within available capacity.  
3. **DBR Scheduling:**  
   - Drum = limiting resource (GP hours / automation capacity)  
   - Buffer = safety window before due date  
   - Rope = release trigger when buffer and inventory ready  
4. **Progress Tracking:** Update `Production_Step` as work advances.  
5. **Variance Analysis:** Compare Planned vs Actual LOE by Tier and Step.  

---

## 7. Data Model and Schema

### Key Entities

| Table | Purpose | Key Fields |
|--------|----------|------------|
| **Tasks** | Master list of SEO activities | `Task_ID`, `Task_Name`, `Tier_Level`, `Production_Step`, `Category`, `Default_Effort_hr`, `Client_ID`, `Owner_ID` |
| **BoM_Items** | Components required for each Task | `BoM_ID`, `Task_ID`, `Component_Name`, `Step_Required`, `Source_Type`, `Availability_Status`, `Inventory_ID` |
| **Inventory** | Digital materials and sub-assemblies in stock | `Inventory_ID`, `Component_Type`, `Tier_Capable`, `Step`, `Status`, `Last_Updated`, `Location` |
| **Schedule** | Time-phased execution records | `Schedule_ID`, `Task_ID`, `Month`, `Owner_ID`, `Planned_Start`, `Planned_End`, `Planned_LOE_hr`, `Actual_LOE_hr`, `Status` |
| **Resources** | Defines capacity per resource per month | `Owner_ID`, `Month`, `Available_hr`, `Buffer_hr`, `Utilization_%` |
| **Constraints** | DBR control points | `Constraint_ID`, `Constraint_Name`, `Max_Throughput_hr`, `Linked_Tasks`, `Priority_Weight` |
| **Clients** | Client metadata and tier assignments | `Client_ID`, `Client_Name`, `Active_Tier`, `Monthly_Retainer`, `Priority` |

---

### ER Diagram (Simplified Textual)

```
[Clients] 1───∞ [Tasks] 1───∞ [Schedule]
                     │
                     ├──∞ [BoM_Items] ∞───1 [Inventory]
                     │
                     └──∞ [Constraints]
[Resources] ──1───∞ [Schedule]
```

**Relationships**
- Each **Client** can have multiple **Tasks**.  
- Each **Task** may have multiple **BoM Items**, each linked to one **Inventory** record.  
- Each **Task** has one or more **Schedule** entries (monthly execution).  
- **Resources** define available hours and connect to Schedules.  
- **Constraints** identify bottlenecks and govern DBR logic.

---

## 8. Capacity & Performance Metrics

| Metric | Formula | Purpose |
|---------|----------|----------|
| **Capacity Load %** | `Σ Planned LOE / Available hr` | Detect overload conditions |
| **Buffer Utilization %** | `Used Buffer hr / Total Buffer hr` | Track safety margin health |
| **Throughput Rate** | `Tasks Completed / Month` | Production velocity |
| **Variance (Δ LOE)** | `Actual – Planned LOE` | Estimation accuracy |
| **Inventory Readiness** | `% BoM Items Available / Total BoM Items` | Material preparedness |

---

## 9. Dashboards & Views

| Dashboard | Focus | Key Visuals |
|------------|--------|-------------|
| **Shop Floor View** | Tasks by Step & Status | Kanban style view with color-coded steps |
| **Control Room View** | Capacity + Throughput | Heatmap by month, bar for LOE variance |
| **Inventory Readiness** | BoM availability | Gauge per campaign type |
| **Constraint Monitor** | DBR status | Drum overload alerts + buffer tracking |

---

## 10. Scaling Triggers & Automation
| Trigger | Recommended Action |
|----------|--------------------|
| Utilization > 85 % for 2 months | Add SEO VA or automation capacity |
| Inventory shortage > 20 % | Increase Tier 1 production |
| Step 2 backlog > x days | Re-allocate resources or automate |
| LOE variance > 15 % | Review estimation accuracy |

---

## 11. Roadmap
| Phase | Deliverable | Target |
|--------|--------------|--------|
| 1 | PRD v0.4 ✅ | Complete |
| 2 | Python Prototype (v1.00) | Finite scheduler reads Excel → calculates capacity → exports plan |
| 3 | Excel Dashboard (v1.00) | Dynamic Power Query dashboard by Tier & Step |
| 4 | Inventory Module (v1.50) | Track and auto-update BoM availability |
| 5 | Automation Layer (v2.00) | Connect to ClickUp, Notion, GSC, and Google Drive APIs |

---

## 12. Summary
- **Tiers** = Performance level (quality and complexity)  
- **Steps** = Production stage (progress in workflow)  
- **BoM validation + DBR logic** = Predictable throughput  
- **Finite capacity scheduling** = No overload and clear growth signals  
