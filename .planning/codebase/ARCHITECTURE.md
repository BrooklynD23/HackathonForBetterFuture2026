# Architecture

**Analysis Date:** 2026-03-20

## Pattern Overview

**Overall:** Single-process Streamlit application with file-backed AI workflows and a separate repo-governed sprint orchestration layer.

**Key Characteristics:**
- `Category 3 - IA West Smart Match CRM/src/app.py` is the composition root; it loads data, validates configuration, initializes session state, prepares caches, and mounts all UI tabs.
- Domain behavior is split by pipeline stage under `Category 3 - IA West Smart Match CRM/src/` (`matching`, `scraping`, `extraction`, `outreach`, `feedback`, `ui`) rather than by framework layer alone.
- Dynamic user interaction state lives in `st.session_state` via `Category 3 - IA West Smart Match CRM/src/runtime_state.py`, while durable artifacts live on disk under `Category 3 - IA West Smart Match CRM/data/` and `Category 3 - IA West Smart Match CRM/cache/`.

## Layers

**Governance And Sprint Control Layer:**
- Purpose: Own sprint authority, task tracking, canonical document ownership, and closeout execution rules.
- Location: `Agents.md`, `tasks/todo.md`, `tasks/lessons.md`, `PRD_SECTION_CAT3.md`, `docs/governance/REPO_REFERENCE.md`, `docs/governance/canonical-map.yaml`, `Category 3 - IA West Smart Match CRM/docs/README.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `Category 3 - IA West Smart Match CRM/.status.md`
- Contains: workflow rules, current sprint board, lessons learned, canonical ownership maps, category execution plan, category status.
- Depends on: checked-in repo state and generated governance reports under `docs/governance/reports/`.
- Used by: human operators and GSD orchestration commands before implementation or closeout work starts.

**Application Composition Layer:**
- Purpose: Bootstrap the Streamlit runtime and wire all modules together.
- Location: `Category 3 - IA West Smart Match CRM/src/app.py`
- Contains: page config, sidebar rendering, configuration validation, dataset loading, embedding-cache bootstrapping, tab creation, and cross-tab state handoff.
- Depends on: `Category 3 - IA West Smart Match CRM/src/config.py`, `Category 3 - IA West Smart Match CRM/src/data_loader.py`, `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/src/runtime_state.py`, and `Category 3 - IA West Smart Match CRM/src/ui/`.
- Used by: `streamlit run src/app.py`, `make run CAT=3`, and screenshot/manual demo flows.

**Configuration And Data Boundary Layer:**
- Purpose: Define filesystem roots, runtime options, cache locations, model names, and CSV schemas.
- Location: `Category 3 - IA West Smart Match CRM/src/config.py`, `Category 3 - IA West Smart Match CRM/src/data_loader.py`
- Contains: environment-backed settings, derived path constants, default scoring weights, CSV validation schemas, `LoadedDatasets`, and `DataQualityResult`.
- Depends on: environment variables, Streamlit secrets, and the CSV files in `Category 3 - IA West Smart Match CRM/data/`.
- Used by: every runtime module that needs paths, model settings, or loaded tabular data.

**Domain Logic Layer:**
- Purpose: Compute matches, normalize cross-tab state, and turn user actions into funnel/feedback signals.
- Location: `Category 3 - IA West Smart Match CRM/src/matching/engine.py`, `Category 3 - IA West Smart Match CRM/src/matching/factors.py`, `Category 3 - IA West Smart Match CRM/src/runtime_state.py`, `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`, `Category 3 - IA West Smart Match CRM/src/similarity.py`, `Category 3 - IA West Smart Match CRM/src/utils.py`
- Contains: factor scoring, rank generation, normalized match-result DataFrames, feedback capture, and formatting helpers.
- Depends on: loaded DataFrames, embedding lookups, default weights from `Category 3 - IA West Smart Match CRM/src/config.py`, and `st.session_state`.
- Used by: `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, and `Category 3 - IA West Smart Match CRM/src/ui/volunteer_dashboard.py`.

**AI And Integration Layer:**
- Purpose: Call Gemini, generate embeddings, scrape public university pages, extract event JSON, generate explanations, and generate outreach artifacts.
- Location: `Category 3 - IA West Smart Match CRM/src/gemini_client.py`, `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`, `Category 3 - IA West Smart Match CRM/src/outreach/ics_generator.py`
- Contains: direct REST calls to Gemini, retry/backoff for embeddings, scrape caching, SSRF/robots protections, extraction caching, explanation caching, email caching, and calendar invite generation.
- Depends on: `Category 3 - IA West Smart Match CRM/src/config.py`, `Category 3 - IA West Smart Match CRM/cache/`, and public network access when not in demo mode.
- Used by: `Category 3 - IA West Smart Match CRM/src/app.py` and the `Discovery` and `Matches` UI paths.

**Presentation Layer:**
- Purpose: Render tab-specific UX and translate domain outputs into Streamlit interactions.
- Location: `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/expansion_map.py`, `Category 3 - IA West Smart Match CRM/src/ui/email_panel.py`, `Category 3 - IA West Smart Match CRM/src/ui/volunteer_dashboard.py`, `Category 3 - IA West Smart Match CRM/src/ui/styles.py`
- Contains: selectors, sliders, tables, charts, expanders, email preview, and demo-mode-aware rendering.
- Depends on: the composition layer, domain logic layer, and AI/integration layer.
- Used by: end users in the Streamlit dashboard and `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`.

**Operational Utilities Layer:**
- Purpose: Verify deployment/demo readiness and generate documentation assets.
- Location: `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`, `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`, `Makefile`, `Category 3 - IA West Smart Match CRM/docs/testing/README.md`
- Contains: preflight checks, optional cache prewarming, screenshot capture automation, and shared developer commands.
- Depends on: the product runtime modules and the on-disk cache/data layout.
- Used by: Sprint 4 verification, demo rehearsal, and likely Sprint 5 closeout evidence gathering.

## Data Flow

**App Startup And Tab Composition:**

1. `streamlit run src/app.py` enters `Category 3 - IA West Smart Match CRM/src/app.py`, sets page config, injects CSS, and calls `init_runtime_state()`.
2. `Category 3 - IA West Smart Match CRM/src/config.py` validates filesystem prerequisites and Gemini configuration through `validate_config()`.
3. `Category 3 - IA West Smart Match CRM/src/data_loader.py` loads the four CSV datasets into a `LoadedDatasets` dataclass and emits per-file quality results.
4. `Category 3 - IA West Smart Match CRM/src/embeddings.py` loads cached embedding lookups from `Category 3 - IA West Smart Match CRM/cache/` and, when allowed, bootstraps missing caches through Gemini.
5. `Category 3 - IA West Smart Match CRM/src/app.py` creates five tabs and delegates rendering to `Category 3 - IA West Smart Match CRM/src/ui/`.

**Discovery Flow:**

1. `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py` chooses a target from `UNIVERSITY_TARGETS` in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`.
2. `scrape_university()` validates the URL, checks cache, enforces robots/rate-limit protections, and returns live, cached, or stale-cached HTML.
3. `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py` preprocesses HTML, calls Gemini, validates JSON, and caches the extracted event list.
4. `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py` writes discovered events to `st.session_state["scraped_events"]` and `st.session_state["matching_discovered_events"]`.

**Matching And Outreach Flow:**

1. `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py` reads loaded datasets plus embedding lookup dicts.
2. `Category 3 - IA West Smart Match CRM/src/matching/engine.py` computes six-factor scores and returns ranked match dicts.
3. `Category 3 - IA West Smart Match CRM/src/runtime_state.py` normalizes those match dicts into `st.session_state["match_results_df"]`.
4. `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, `Category 3 - IA West Smart Match CRM/src/ui/email_panel.py`, and `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py` generate explanation/email artifacts on demand, preferring cache or demo fixtures first.
5. `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py` records accept/decline decisions, persists feedback CSV rows, and drives downstream funnel metrics.

**Pipeline And Volunteer Flow:**

1. `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py` reads `match_results_df`, `scraped_events`, `feedback_log`, and `emails_generated` from `st.session_state`.
2. It computes a real-time funnel when runtime state exists; otherwise it falls back to `pipeline_sample_data.csv` in `Category 3 - IA West Smart Match CRM/data/`.
3. `Category 3 - IA West Smart Match CRM/src/ui/volunteer_dashboard.py` reuses the normalized match DataFrame and feedback log to derive per-speaker utilization views.

**Sprint Closeout And Governance Flow:**

1. `tasks/todo.md` tracks the active sprint board and verification evidence for closeout work.
2. Canonical ownership is checked against `docs/governance/REPO_REFERENCE.md` and `docs/governance/canonical-map.yaml`.
3. Category-specific authority updates land in `PRD_SECTION_CAT3.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, and `Category 3 - IA West Smart Match CRM/.status.md`.
4. Reconciliation and audit outputs are written under `docs/governance/reports/`.
5. Generated architecture/structure maps for future phases land under `.planning/codebase/`.

**State Management:**
- Live interactive state uses `st.session_state`; the documented cross-tab contract is `match_results_df`, `scraped_events`, `feedback_log`, `emails_generated`, `generated_email_keys`, and `demo_mode` in `Category 3 - IA West Smart Match CRM/src/runtime_state.py`, `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`, and `Category 3 - IA West Smart Match CRM/src/demo_mode.py`.
- Durable source data stays in CSV form under `Category 3 - IA West Smart Match CRM/data/`.
- Durable generated artifacts stay in filesystem caches under `Category 3 - IA West Smart Match CRM/cache/`.

## Key Abstractions

**Loaded Datasets Contract:**
- Purpose: Carry the four canonical CSV tables plus data-quality results through the runtime.
- Examples: `Category 3 - IA West Smart Match CRM/src/data_loader.py`
- Pattern: immutable dataclass (`LoadedDatasets`) passed from `load_all()` into UI and matching code.

**Normalized Match Result Contract:**
- Purpose: Give every tab a stable schema for event-speaker rankings and factor scores.
- Examples: `Category 3 - IA West Smart Match CRM/src/matching/engine.py`, `Category 3 - IA West Smart Match CRM/src/runtime_state.py`
- Pattern: event/course rankings are produced as dicts, then normalized into a DataFrame with canonical columns such as `total_score` and `topic_relevance`.

**Hash-Based Cache Contract:**
- Purpose: Make networked and AI-generated artifacts reproducible and reusable across sessions.
- Examples: `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`
- Pattern: derive a stable key from prompt/input content, write JSON or `.npy` files under `Category 3 - IA West Smart Match CRM/cache/`, and tolerate cache misses/corruption by falling back to recomputation or safe empties.

**Demo Mode Dispatch Contract:**
- Purpose: Switch production call sites between live behavior and pre-generated fixtures without changing UI code.
- Examples: `Category 3 - IA West Smart Match CRM/src/demo_mode.py`, `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/email_panel.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`
- Pattern: wrap live functions with `demo_or_live(...)` and source fixtures from `Category 3 - IA West Smart Match CRM/cache/demo_fixtures/`.

**Governed Document Ownership Contract:**
- Purpose: Separate product/runtime architecture from sprint-authority documents and keep closeout edits targeted.
- Examples: `docs/governance/canonical-map.yaml`, `docs/governance/REPO_REFERENCE.md`, `PRD_SECTION_CAT3.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `Category 3 - IA West Smart Match CRM/.status.md`
- Pattern: each planning concern has one canonical owner; derived or historical docs are explicitly marked as non-authoritative.

## Entry Points

**Product Runtime:**
- Location: `Category 3 - IA West Smart Match CRM/src/app.py`
- Triggers: `streamlit run src/app.py`, `make run CAT=3`, or manual Streamlit launch from the category directory.
- Responsibilities: validate config, load data, initialize state, prepare caches, and mount all application tabs.

**Operational Verification:**
- Location: `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`
- Triggers: `./.venv/bin/python scripts/sprint4_preflight.py` and optional `--prewarm-discovery`.
- Responsibilities: verify data/runtime/cache/demo-fixture layout and optionally prewarm scrape/extraction caches.

**Documentation Asset Capture:**
- Location: `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`
- Triggers: manual execution during rehearsal or closeout artifact generation.
- Responsibilities: drive the Streamlit UI with Playwright and save screenshot evidence into `Category 3 - IA West Smart Match CRM/docs/screenshots/`.

**Sprint Execution Context:**
- Location: `tasks/todo.md`
- Triggers: every non-trivial repo task under the checked-in workflow rules in `Agents.md`.
- Responsibilities: hold the active board, review notes, verification evidence, and closeout checklist.

## Error Handling

**Strategy:** Fail fast on missing local prerequisites, degrade safely on networked/AI/cache failures, and keep the UI responsive with explicit user-facing messages.

**Patterns:**
- `Category 3 - IA West Smart Match CRM/src/app.py` calls `validate_config()` and uses `st.stop()` after rendering explicit configuration/data errors.
- `Category 3 - IA West Smart Match CRM/src/data_loader.py` validates schema and records issues instead of silently coercing structural mismatches away.
- `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` prefers fresh cache, then stale cache on live failure, and rejects unsafe custom URLs before network access.
- `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, and `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py` treat malformed cache/API output as cache miss or fallback input rather than crashing the whole app.
- `Category 3 - IA West Smart Match CRM/src/ui/` modules surface exceptions with `st.error(...)` and keep empty-table / warning states available for partial flows.

## Cross-Cutting Concerns

**Logging:** Standard-library `logging` is used throughout `Category 3 - IA West Smart Match CRM/src/` and `Category 3 - IA West Smart Match CRM/scripts/`; exceptions are logged close to the failing integration point and then converted into UI-safe states.
**Validation:** Configuration validation is centralized in `Category 3 - IA West Smart Match CRM/src/config.py`; CSV schema validation is centralized in `Category 3 - IA West Smart Match CRM/src/data_loader.py`; scrape URL safety is centralized in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`; operational validation is centralized in `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`.
**Authentication:** No end-user auth layer is present. The only credential boundary is Gemini configuration via environment variables or Streamlit secrets in `Category 3 - IA West Smart Match CRM/src/config.py`.

---

*Architecture analysis: 2026-03-20*
