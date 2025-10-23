# Claude Code – Project Playbook: Rank Rocket Client Tracker

> Repo nickname: **RR** · Purpose: Execute the Rank Rocket SEO Factory vision with SEO automation toolkit, finite scheduling, and reliable session handoffs.

---

## 0) Mission & Working Agreement

When asked for changes in this repo:

1. **Plan** briefly (what/why/files to touch).
2. **Patch** with **small, reviewable diffs**; no broad rewrites unless asked.
3. **Test** using the quality gates in §4.
4. **Summarize** changes, risks, and next steps.
5. Respect the guardrails below.

**Non‑negotiables**

* Production‑ready diffs only (no placeholders or TODO litter in committed code).
* Preserve headers/license blocks; bump versions per project rules.
* No secrets in code; use `.env`/secure config.
* No emojis or other Unicode in source code or test output that would fail in a Windows environment.
* Use ASCII alternatives: PASS/FAIL instead of checkmarks, [INFO] instead of symbols, etc.
* All print statements must use ASCII-safe characters only.

---

## 1) Session Commands (exact phrases to use)

### ▶️ `RR start`

**Goal:** Prime context at the start of a session efficiently.
**Claude should:**

1. **Read session context files** (in priority order, stop when sufficient context achieved):

   * `docs/SESSION_CONTEXT.md` (primary context source)
   * `docs/HANDOFF_SUMMARY.md` (session transition details)
   * Latest `docs/archive/checkpoints/CheckPoint-*.md` (detailed checkpoint)
   * `docs/projectStatus.md` (overall project status)
   * Only if context incomplete: `sop/Rank_Rocket_Flight_Deck_Blueprint_v1.0.md` (partial read with offset/limit)

2. **Post a kickoff note** with:

   * **Last session wins** (3-5 key accomplishments)
   * **Current sprint status** (progress, blockers, next milestones)
   * **Today's priority plan** (1-3 concrete actionable steps)
   * **Critical alerts** (any blockers, failing tests, or urgent issues)

3. **Confirm environment status**:
   * Git branch/status and working tree state
   * Any uncommitted changes or merge conflicts
   * Dependencies and build status if relevant

### 💾 `RR checkpoint`

**Goal:** Capture state at any time (especially near usage limits) so the next session can resume seamlessly.
**Claude should:**

1. Create a new checkpoint file in `docs/archive/checkpoints/` using the existing naming pattern if found; otherwise default to:
   `CheckPoint-YYYY-MM-DD_HHMM.md`
2. Use this template in the file:

   * **Context summary** (why we're here)
   * **Accomplishments** (what shipped)
   * **Technical changes** (files touched, diffs overview)
   * **Known issues / blockers**
   * **Next session priorities** (bullet list)
   * **Backlog movement** (added/removed/deferred)
   * **Git status** (branch, last commit hash, pushed: yes/no)
3. Update live docs:

   * Append any **Design Variations & Rationale** to `docs/Rank_Rocket_Master_Plan.md`.
   * Update `docs/projectStatus.md` (Completed / In‑Progress / Deferred + Next items).
4. **WAIT for user QA testing confirmation before commits** - Only proceed with git operations after user confirms QA results
5. `git add -A && git commit -m "chore(checkpoint): YYYY-MM-DD_HHMM – <short summary>" && git push` (only after QA confirmation)
6. Reply in chat with a 1‑paragraph summary + a checklist of next steps.

> **Trigger words**: "checkpoint now", "prepare for rollover", "juice check", "save state" → run **RR checkpoint** immediately.

### ⏹️ `RR shutdown`

**Goal:** End a session cleanly with comprehensive context capture for next session startup.
**Claude should:**

1. **Create Enhanced Context Capture**:
   - Generate `docs/SESSION_CONTEXT.md` with:
     * **Current Sprint Summary** (goals, status, achievements)
     * **Active Work Items** (in-progress tasks with details)
     * **Recent Major Accomplishments** (last 3-5 significant features/fixes)
     * **Critical Path Items** (blocking issues, dependencies)
     * **Technical Architecture Status** (current system state, known issues)
     * **Quality Gate Status** (test coverage, build status, lint status)
     * **Next Session Action Plan** (prioritized 1-3 concrete steps)

2. **Run Standard RR checkpoint** (mandatory).

3. **Create Session Handoff Summary**:
   - Generate `docs/HANDOFF_SUMMARY.md` with:
     * **Project Status Overview** (where we are in overall plan)
     * **Current Git State** (branch, uncommitted changes, merge conflicts)
     * **Environment Status** (dependencies, config, known env issues)
     * **User Context** (recent requests, pending decisions, feedback status)
     * **Risk Assessment** (technical debt, potential blockers)

4. **Ensure all changes are pushed**; echo branch, commit hash, and tag if created.

5. **Post "Shutdown complete"** with **3 priority bullets** for next session startup.

---

## 2) Project Guardrails (RR specifics)

* **Stack**: Python 3.10-3.12, Tkinter (migrating to PyQt6), pandas, openpyxl
* **APIs**: Google Ads API v26+, OpenAI GPT-4, SerpAPI
* **Purpose**: SEO automation toolkit → Factory orchestration (Tier/Step model, DBR scheduling)
* **Core Modules**: Keyword research, GBP keywords, FAQ generation, business summaries
* **Future Vision**: Unified Flight Deck with finite scheduler, BoM validation, multi-repo integration
* **Idempotency**: Safe reruns (config-based, no duplicate operations)
* **Performance**: Handle large keyword lists, batch processing, progress indicators

---

## 3) Files & Paths (authoritative)

* **Master Plan**: `docs/Rank_Rocket_Master_Plan.md` (consolidation of Flight Deck Blueprint + Factory Integration Index)
* **Status**: `docs/projectStatus.md` (sprint state + next actions)
* **Checkpoints**: `docs/archive/checkpoints/` (one markdown per checkpoint)
* **Session Context**: `docs/SESSION_CONTEXT.md` (primary context for startup)
* **Handoff**: `docs/HANDOFF_SUMMARY.md` (session transitions)
* **SOPs**: `sop/` directory (user guides, operational procedures)

> If these files/folders don't exist, Claude should create them with minimal scaffolding.

---

## 4) Code Quality Gates & Runbook

### Python

```bash
ruff --fix . && black . && mypy . && pytest -q
```

* Full typing on new/changed code (PEP 484); Google‑style docstrings (PEP 257).
* Use structured logging; no `print` in libraries.
* CLIs default to safe behavior (dry‑run when destructive).
* `pathlib` for filesystem ops; write OS‑portable code (Windows paths common).

### File Headers (Standard Format)

```python
"""
Module/Script Name: [Name of the file or module]
Path: [Full path to file with name]

Description:
[Brief summary of what the script does]

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
[YYYY-MM-DD]

Last Modified Date:
[YYYY-MM-DD]

Version:
[v1.00 format - minor +0.01, major +1.00]

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* [Versioning or functional update notes]
"""
```

### Versioning Rules
* Start new files at **v1.00**
* Minor changes: +0.01 (v1.00 → v1.01)
* Major changes: +1.00 (v1.05 → v2.00)
* Optional beta suffix: v1.00β
* **Never** embed version in filename

---

## 5) Debug/Release Hygiene

Before tagging a release:

* Remove debug prints and traces from Python code.
* Re‑run quality gate: `ruff --fix . && black . && mypy . && pytest -q`
* Verify all tools execute successfully with test configs.
* Update README and CHANGELOG with migration notes.

---

## 6) Override Directives (Add / Edit / Delete)

Change rules via chat without manually editing this file. Claude should apply the change, show a small diff, and commit.

### Add

```
ADD RULE → <Section Anchor>
<one sentence rule to append>
```

### Edit

```
EDIT RULE → <Section Anchor>
<existing line text>
--- becomes ---
<new line text>
```

### Delete

```
DELETE RULE → <Section Anchor>
<exact line text to remove>
```

**Section Anchors**:
`0) Mission` · `1) Session Commands` · `2) Project Guardrails` · `3) Files & Paths` · `4) Code Quality Gates` · `5) Debug/Release Hygiene` · `6) Override Directives`

---

## 7) Quick Prompts

* **Start session**: `RR start`
* **Checkpoint now**: `RR checkpoint — summarize, commit, push`
* **End session**: `RR shutdown`
* **Override rule**: `EDIT RULE → 4) Code Quality Gates …`

---

## 8) Notes on Continuity & Limits

* Use **RR checkpoint** whenever you're nearing your daily usage cap or switching tasks.
* A checkpoint is **mandatory** for every **RR shutdown**.
* Next session resumes with **RR start** which reads the last checkpoint and aligns the plan.

---

## 9) Conventional Commits

Use semantic commit messages:
* `feat:` - New feature
* `fix:` - Bug fix
* `perf:` - Performance improvement
* `refactor:` - Code restructuring
* `test:` - Test additions/changes
* `docs:` - Documentation updates
* `build:` - Build system changes
* `chore:` - Maintenance tasks

Example: `feat(faq): add multi-keyword batch processing support`

---

## 10) Integration Ecosystem

This project is part of the larger **SEO Factory** architecture. Related repositories:

* `skippy_yaml_builder` - Client intake
* `ethical_web_scraper` - Data acquisition
* `llm_txt_generator` - Content generation
* `rank-rocket-schema-creator` - Schema generation
* `push_it_real_good` - WordPress publisher
* `cloud-stack-generator` - Cloud stack deployment
* `Location_Page_Generator` - City/service page builder
* `qr_watermark_wizard` - Media prep
* `rank_rocket_calendar_stacker` - Cadence engine

**Integration Strategy**: YAML-based client configs consumed by all downstream modules.
