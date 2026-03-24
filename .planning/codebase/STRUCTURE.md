# Codebase Structure

**Analysis Date:** 2026-03-20

## Directory Layout

```text
[project-root]/
├── Category 3 - IA West Smart Match CRM/   # Category 3 product app, docs, scripts, cache, tests
│   ├── src/                                # Streamlit runtime and domain modules
│   ├── data/                               # CSV source data and pipeline sample data
│   ├── cache/                              # Embedding, scrape, extraction, explanation, email, and demo fixture artifacts
│   ├── docs/                               # Category-specific execution docs, sprint specs, testing artifacts, screenshots
│   ├── scripts/                            # Preflight and screenshot automation
│   ├── tests/                              # Pytest suite for runtime modules and scripts
│   ├── .streamlit/                         # Streamlit runtime/theme config
│   └── runtime.txt                         # Streamlit Cloud Python version pin
├── docs/governance/                        # Repo-wide canonical ownership map and governance reports
├── tasks/                                  # Active task board and lessons learned
├── .planning/codebase/                     # Generated codebase map documents for future GSD phases
├── Agents.md                               # Repo workflow/orchestration rules
├── PRD_SECTION_CAT3.md                     # Canonical Category 3 feature-detail doc
└── Makefile                                # Shared run/test/setup entry points
```

## Directory Purposes

**`Category 3 - IA West Smart Match CRM/src/`:**
- Purpose: Hold all checked-in product runtime code.
- Contains: `src/app.py`, config/data loaders, AI integrations, scoring logic, Streamlit UI modules, and runtime-state helpers.
- Key files: `Category 3 - IA West Smart Match CRM/src/app.py`, `Category 3 - IA West Smart Match CRM/src/config.py`, `Category 3 - IA West Smart Match CRM/src/runtime_state.py`, `Category 3 - IA West Smart Match CRM/src/matching/engine.py`, `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`

**`Category 3 - IA West Smart Match CRM/src/ui/`:**
- Purpose: Keep presentation code separate from lower-level matching/scraping/email modules.
- Contains: tab renderers, panel components, CSS injection, and chart-building logic.
- Key files: `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/volunteer_dashboard.py`

**`Category 3 - IA West Smart Match CRM/src/matching/`:**
- Purpose: Own scoring and explanation behavior.
- Contains: factor functions, ranking engine, explanation-generation cache logic.
- Key files: `Category 3 - IA West Smart Match CRM/src/matching/factors.py`, `Category 3 - IA West Smart Match CRM/src/matching/engine.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`

**`Category 3 - IA West Smart Match CRM/src/scraping/`, `Category 3 - IA West Smart Match CRM/src/extraction/`, `Category 3 - IA West Smart Match CRM/src/outreach/`, `Category 3 - IA West Smart Match CRM/src/feedback/`:**
- Purpose: Group pipeline-stage integrations outside the UI.
- Contains: public-site scraping, Gemini extraction, outreach generation, calendar invite generation, and feedback capture.
- Key files: `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`, `Category 3 - IA West Smart Match CRM/src/outreach/ics_generator.py`, `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`

**`Category 3 - IA West Smart Match CRM/data/`:**
- Purpose: Store CSV-backed source-of-truth inputs and fallback sample datasets.
- Contains: the four core CSVs referenced by `src/data_loader.py` plus `pipeline_sample_data.csv` used by the Pipeline tab when live runtime state is absent.
- Key files: `Category 3 - IA West Smart Match CRM/data/data_speaker_profiles.csv`, `Category 3 - IA West Smart Match CRM/data/data_cpp_events_contacts.csv`, `Category 3 - IA West Smart Match CRM/data/data_cpp_course_schedule.csv`, `Category 3 - IA West Smart Match CRM/data/data_event_calendar.csv`

**`Category 3 - IA West Smart Match CRM/cache/`:**
- Purpose: Store durable generated artifacts and offline demo fixtures.
- Contains: embedding arrays/metadata at the cache root, hashed scrape JSON in `cache/scrapes/`, extraction JSON in `cache/extractions/`, explanation JSON in `cache/explanations/`, email JSON in `cache/emails/`, and offline fixtures in `cache/demo_fixtures/`.
- Key files: `Category 3 - IA West Smart Match CRM/cache/cache_manifest.json`, `Category 3 - IA West Smart Match CRM/cache/demo_fixtures/discovery_scan.json`, `Category 3 - IA West Smart Match CRM/cache/demo_fixtures/pipeline_funnel.json`

**`Category 3 - IA West Smart Match CRM/docs/`:**
- Purpose: Keep category-local execution docs, sprint specs, testing instructions, and screenshot assets near the product code.
- Contains: the canonical category readme and sprint plan, sprint-specific implementation specs, testing/rehearsal templates, screenshots guidance, and provider decision notes.
- Key files: `Category 3 - IA West Smart Match CRM/docs/README.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `Category 3 - IA West Smart Match CRM/docs/sprints/README.md`, `Category 3 - IA West Smart Match CRM/docs/testing/README.md`, `Category 3 - IA West Smart Match CRM/docs/gemini_provider_decision_2026-03-18.md`

**`Category 3 - IA West Smart Match CRM/scripts/`:**
- Purpose: Hold non-UI operational utilities.
- Contains: preflight/cache-warm automation and screenshot capture tooling.
- Key files: `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`, `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`

**`Category 3 - IA West Smart Match CRM/tests/`:**
- Purpose: Mirror the runtime structure with targeted module-level regression coverage.
- Contains: test modules for config, loader, scraper, extractor, UI tabs, preflight, and end-to-end state contracts.
- Key files: `Category 3 - IA West Smart Match CRM/tests/conftest.py`, `Category 3 - IA West Smart Match CRM/tests/test_app.py`, `Category 3 - IA West Smart Match CRM/tests/test_scraper.py`, `Category 3 - IA West Smart Match CRM/tests/test_sprint4_preflight.py`

**`docs/governance/`:**
- Purpose: Hold repo-wide canonical ownership metadata and generated governance audit/reconcile outputs.
- Contains: the canonical map, the human-readable repo reference index, and dated governance reports.
- Key files: `docs/governance/canonical-map.yaml`, `docs/governance/REPO_REFERENCE.md`, `docs/governance/reports/2026-03-20-category-3-governance.md`, `docs/governance/reports/2026-03-20-category-3-audit.md`

**`tasks/`:**
- Purpose: Hold the active execution board and self-correction memory for repo work.
- Contains: the current sprint/task checklist and lessons file.
- Key files: `tasks/todo.md`, `tasks/lessons.md`

**`.planning/codebase/`:**
- Purpose: Hold generated codebase-reference documents used by later GSD planning/execution phases.
- Contains: architecture, structure, stack, conventions, testing, integrations, and concerns docs when generated.
- Key files: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`

## Key File Locations

**Entry Points:**
- `Category 3 - IA West Smart Match CRM/src/app.py`: Streamlit product entry point and composition root.
- `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`: operational verification and optional cache-prewarm entry point.
- `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`: documentation asset generation entry point.
- `Makefile`: shared wrapper for `setup`, `run`, `test`, and `lint`.
- `tasks/todo.md`: sprint execution and closeout board entry point.

**Configuration:**
- `Category 3 - IA West Smart Match CRM/src/config.py`: runtime paths, model names, cache roots, default weights, and config validation.
- `Category 3 - IA West Smart Match CRM/.streamlit/config.toml`: Streamlit theme/server settings.
- `Category 3 - IA West Smart Match CRM/runtime.txt`: Streamlit Cloud Python version pin.
- `Category 3 - IA West Smart Match CRM/requirements.txt`: category-specific Python dependency list.
- `docs/governance/canonical-map.yaml`: canonical ownership map for governed docs.

**Core Logic:**
- `Category 3 - IA West Smart Match CRM/src/data_loader.py`: CSV loading and schema validation.
- `Category 3 - IA West Smart Match CRM/src/embeddings.py`: embedding-cache generation and lookup loading.
- `Category 3 - IA West Smart Match CRM/src/matching/engine.py`: speaker ranking and match-score composition.
- `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`: scrape orchestration, caching, robots, and URL safety.
- `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`: HTML-to-event extraction.
- `Category 3 - IA West Smart Match CRM/src/runtime_state.py`: shared `st.session_state` contract.

**Testing:**
- `Category 3 - IA West Smart Match CRM/tests/`: pytest suite root.
- `Category 3 - IA West Smart Match CRM/tests/test_app.py`: composition-root and startup behavior coverage.
- `Category 3 - IA West Smart Match CRM/tests/test_discovery_tab.py`: discovery tab and scrape/extract contract coverage.
- `Category 3 - IA West Smart Match CRM/tests/test_pipeline_tab.py`: funnel and runtime-state coverage.
- `Category 3 - IA West Smart Match CRM/docs/testing/README.md`: manual verification and preflight command reference.

## Naming Conventions

**Files:**
- Python runtime modules use `snake_case.py`: `Category 3 - IA West Smart Match CRM/src/runtime_state.py`
- Test files mirror runtime module intent with `test_<module>.py`: `Category 3 - IA West Smart Match CRM/tests/test_email_gen.py`
- Sprint specs use `sprint-<number>-<topic>.md`: `Category 3 - IA West Smart Match CRM/docs/sprints/sprint-4-ship.md`
- Governance reports use date-prefixed kebab case: `docs/governance/reports/2026-03-20-category-3-governance.md`
- Generated codebase map docs use uppercase names: `.planning/codebase/ARCHITECTURE.md`

**Directories:**
- Product source directories are lowercase by domain: `Category 3 - IA West Smart Match CRM/src/ui/`, `Category 3 - IA West Smart Match CRM/src/matching/`
- Governance/report directories are noun-based and stable: `docs/governance/`, `docs/governance/reports/`
- Sprint/test/support directories stay local to Category 3: `Category 3 - IA West Smart Match CRM/docs/testing/`, `Category 3 - IA West Smart Match CRM/docs/screenshots/`

## Where to Add New Code

**New Feature:**
- Primary code: add domain logic under the matching pipeline directory that owns it, then wire it into `Category 3 - IA West Smart Match CRM/src/app.py` through the relevant UI module in `Category 3 - IA West Smart Match CRM/src/ui/`.
- Tests: add targeted pytest coverage under `Category 3 - IA West Smart Match CRM/tests/` next to the affected module family, for example `Category 3 - IA West Smart Match CRM/tests/test_matches_tab.py` or `Category 3 - IA West Smart Match CRM/tests/test_scraper.py`.

**New Component/Module:**
- Implementation: keep UI-only concerns in `Category 3 - IA West Smart Match CRM/src/ui/`; keep reusable service logic in the closest domain package such as `Category 3 - IA West Smart Match CRM/src/matching/`, `Category 3 - IA West Smart Match CRM/src/scraping/`, `Category 3 - IA West Smart Match CRM/src/extraction/`, or `Category 3 - IA West Smart Match CRM/src/outreach/`.

**Utilities:**
- Shared helpers: extend `Category 3 - IA West Smart Match CRM/src/utils.py` only for cross-cutting helpers that are not owned by a single domain package. Keep domain-specific helpers beside their owning module instead of growing `utils.py` by default.

**Sprint Closeout / Governance Refresh:**
- Task tracking and review evidence: `tasks/todo.md`
- Workflow guardrails and lessons: `Agents.md`, `tasks/lessons.md`
- Category execution/status authority: `Category 3 - IA West Smart Match CRM/docs/README.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `Category 3 - IA West Smart Match CRM/.status.md`, `PRD_SECTION_CAT3.md`
- Repo ownership and reconcile outputs: `docs/governance/REPO_REFERENCE.md`, `docs/governance/canonical-map.yaml`, `docs/governance/reports/`
- Planner-facing generated reference docs: `.planning/codebase/`

## Special Directories

**`Category 3 - IA West Smart Match CRM/cache/`:**
- Purpose: Generated runtime artifacts and demo fixtures.
- Generated: Yes
- Committed: Yes, at least for demo fixtures and expected cache-layout artifacts used by the checked-in workflow.

**`docs/governance/reports/`:**
- Purpose: Dated governance audit/reconcile outputs.
- Generated: Yes
- Committed: Yes

**`.planning/codebase/`:**
- Purpose: Generated codebase reference docs for GSD planners/executors.
- Generated: Yes
- Committed: Yes

**`Category 3 - IA West Smart Match CRM/.streamlit/`:**
- Purpose: Local Streamlit runtime configuration.
- Generated: No
- Committed: Yes

**`Category 3 - IA West Smart Match CRM/docs/screenshots/`:**
- Purpose: Screenshot artifacts used by documentation and demo materials.
- Generated: Yes
- Committed: Yes

---

*Structure analysis: 2026-03-20*
