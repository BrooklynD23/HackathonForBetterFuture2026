# Sprint 2 Swarm Orchestration Plan

**Branch:** `sprint2-cat3` (from `sprint1-cat3`)
**Orchestrator:** Opus 4.6 (you, the harness engineer)
**Workers:** Sonnet 4.6 via Claude Swarm MCP
**Methodology:** Everything Claude Code TDD (RED-GREEN-IMPROVE per worker)
**Sprint Spec:** `docs/sprints/sprint-2-discovery-email.md` (canonical source of truth)

---

## 1. Dependency Graph

```
Phase 1 (parallel)                Phase 2          Phase 3          Phase 4
──────────────────                ─────────        ─────────        ─────────
[A2.1 Scraper]  ─────────────> [A2.2 Extractor] > [A2.3 Discovery] ─┐
[A2.4 Email]  ──> [A2.5 .ics]                                       │
[A2.6 Funnel]                                                        ├> [A2.7 Handoff]
                                                                     │
```

| Feature ID | Task | Dependencies | Phase | Est. Time |
|---|---|---|---|---|
| `feature-1` | A2.1 Web Scraper | none | 1 | 45-60 min |
| `feature-2` | A2.2 LLM Extractor | feature-1 | 2 | 30-45 min |
| `feature-3` | A2.3 Discovery Tab | feature-2 | 3 | 30-45 min |
| `feature-4` | A2.4 Email Gen | none | 1 | 30-45 min |
| `feature-5` | A2.5 Calendar .ics | feature-4 | 1b | 20-30 min |
| `feature-6` | A2.6 Pipeline Funnel | none | 1 | 30-40 min |
| `feature-7` | A2.7 Handoff Package | all above | 4 | 15-20 min |

**Max concurrent workers:** 3 (Phase 1: features 1, 4, 6)

---

## 2. File Ownership Matrix (Conflict Prevention)

Each worker owns a disjoint set of files. Shared files are serialized by dependency order.

| Worker | Owns (creates) | Modifies (shared) |
|---|---|---|
| feature-1 (Scraper) | `src/scraping/__init__.py`, `src/scraping/scraper.py`, `tests/test_scraper.py` | `src/config.py` (append only) |
| feature-2 (Extractor) | `src/extraction/__init__.py`, `src/extraction/llm_extractor.py`, `tests/test_llm_extractor.py` | `src/config.py` (append only) |
| feature-3 (Discovery) | `src/ui/discovery_tab.py`, `tests/test_discovery_tab.py` | `src/app.py` (replace `render_discovery_tab`) |
| feature-4 (Email) | `src/outreach/__init__.py`, `src/outreach/email_generator.py`, `src/ui/email_panel.py`, `tests/test_email_generator.py` | `src/ui/matches_tab.py` (lines 248-256, email button) |
| feature-5 (.ics) | `src/outreach/ics_generator.py`, `tests/test_ics_generator.py` | `src/ui/matches_tab.py` (lines 257-262, .ics button) |
| feature-6 (Funnel) | `src/ui/pipeline_tab.py`, `tests/test_pipeline_tab.py` | `src/app.py` (replace `render_pipeline_tab`) |
| feature-7 (Handoff) | `data/track_b_data_package.md` | none |

### Shared File Serialization

- **`src/app.py`**: feature-6 modifies first (Phase 1), feature-3 modifies later (Phase 3). No conflict.
- **`src/ui/matches_tab.py`**: feature-4 modifies first (Phase 1), feature-5 modifies after (Phase 1b, depends on feature-4). Serialized.
- **`src/config.py`**: All workers append-only to end of file. Each uses unique constant names. Low conflict risk.

---

## 3. Swarm MCP Orchestration Commands (Step-by-Step)

### Step 0: Branch (Already Done)

```bash
git checkout sprint1-cat3
git checkout -b sprint2-cat3
```

### Step 1: Initialize Swarm

```
orchestrator_init(
  projectDir = "Category 3 - IA West Smart Match CRM",
  taskDescription = "Sprint 2: Discovery + Email + Pipeline. 7 features: web scraping (5 universities), LLM extraction, Discovery tab, email generation, .ics calendar, pipeline funnel, Track B handoff. TDD required.",
  existingFeatures = [
    "A2.1: Web scraping pipeline - BS4+Playwright for 5 universities, SSRF protection, robots.txt, rate limiting, hashed JSON cache",
    "A2.2: LLM extraction - Gemini gemini-2.5-flash-lite structured event JSON from scraped HTML",
    "A2.3: Discovery tab - Streamlit UI: university selector, results table, Add to Matching",
    "A2.4: Email generation - Gemini-powered personalized outreach emails with copy-to-clipboard",
    "A2.5: Calendar .ics - Downloadable .ics for matched events",
    "A2.6: Pipeline funnel - Plotly 6-stage funnel with real data and hover tooltips",
    "A2.7: Track B handoff - Compile match results, funnel numbers, coverage map, ROI inputs"
  ]
)
```

### Step 2: Set Dependencies

```
set_dependencies(featureId="feature-2", dependsOn=["feature-1"])
set_dependencies(featureId="feature-3", dependsOn=["feature-2"])
set_dependencies(featureId="feature-5", dependsOn=["feature-4"])
set_dependencies(featureId="feature-7", dependsOn=["feature-1","feature-2","feature-3","feature-4","feature-5","feature-6"])
```

### Step 3: Configure Verification

```
configure_verification(
  commands = ["pytest tests/ -v --tb=short"],
  failOnError = True
)
```

### Step 4: Set Feature Context (per worker)

Each worker receives:
1. **TDD Protocol** (priority: "required") - see Section 4
2. **Sprint Spec Reference** - the relevant section of `docs/sprints/sprint-2-discovery-email.md`
3. **Architecture Reference Files** - key existing modules to follow

```
set_feature_context(featureId="feature-N", documentation=[...], prepared=[...])
```

#### Context for feature-1 (Scraper)

```
documentation:
  - src/config.py (config pattern, append new constants)
  - src/matching/explanations.py (sha256 hashed JSON cache pattern)
  - tests/test_explanations.py (test mock patterns)
  - docs/sprints/sprint-2-discovery-email.md (lines 34-451, full scraper spec)

prepared:
  - key: "tdd-protocol" (see Section 4)
  - key: "architecture"
    content: |
      1. Create src/scraping/__init__.py and src/scraping/scraper.py
      2. FULL SPEC IS IN docs/sprints/sprint-2-discovery-email.md task A2.1
      3. Follow the code spec EXACTLY - it has complete function signatures
      4. Tests in tests/test_scraper.py - mock ALL HTTP/Playwright calls
      5. Append scraping constants to src/config.py
      6. Return contract: {html, scraped_at, url, method, source, ttl_hours, robots_ok}
```

#### Context for feature-2 (Extractor)

```
documentation:
  - src/gemini_client.py (generate_text() function to call)
  - src/matching/explanations.py (LLM integration + cache pattern)
  - src/scraping/scraper.py (upstream input - HTML from scraper)
  - docs/sprints/sprint-2-discovery-email.md (task A2.2)

prepared:
  - key: "architecture"
    content: |
      1. Create src/extraction/__init__.py and src/extraction/llm_extractor.py
      2. FULL SPEC IS IN docs/sprints/sprint-2-discovery-email.md task A2.2
      3. Use generate_text() from src/gemini_client.py (NOT a Gemini SDK import)
      4. HTML preprocessing: strip scripts/styles/nav/footer using BeautifulSoup
      5. Few-shot prompting with system prompt + examples
      6. Cache under cache/extractions/<sha256(url)>.json
      7. Output: list of event dicts matching EXTRACTED_EVENT_SCHEMA
```

#### Context for feature-3 (Discovery Tab)

```
documentation:
  - src/ui/matches_tab.py (UI module pattern to follow)
  - src/app.py (lines 157-173, placeholder to replace)
  - src/scraping/scraper.py (upstream: scrape_all_universities)
  - src/extraction/llm_extractor.py (upstream: extract_events)

prepared:
  - key: "architecture"
    content: |
      1. Create src/ui/discovery_tab.py
      2. Replace render_discovery_tab() in src/app.py with import from new module
      3. Follow src/ui/matches_tab.py patterns: module-level render function, private helpers
      4. University selector (st.selectbox), Discover Events button, results st.dataframe
      5. "Add to Matching" button stores events in st.session_state
      6. Custom URL input with validate_public_demo_url() from src/scraping/scraper.py
```

#### Context for feature-4 (Email)

```
documentation:
  - src/matching/explanations.py (LLM + cache + fallback pattern)
  - src/gemini_client.py (generate_text() API)
  - src/ui/matches_tab.py (lines 248-256, email button to wire)

prepared:
  - key: "architecture"
    content: |
      1. Create src/outreach/__init__.py, src/outreach/email_generator.py, src/ui/email_panel.py
      2. Follow src/matching/explanations.py pattern: system prompt + few-shot + user template + fallback + cache
      3. Use generate_text() from src/gemini_client.py
      4. Cache under cache/emails/<sha256(speaker_name + event_name)>.json
      5. Wire into matches_tab.py: replace no-op email button (lines 250-256) with real generation
      6. Output: {subject, greeting, body, value_prop, cta, full_text}
      7. Add email preview panel (st.expander) below the match card when generated
```

#### Context for feature-5 (.ics)

```
documentation:
  - src/ui/matches_tab.py (lines 257-262, .ics button to wire)

prepared:
  - key: "architecture"
    content: |
      1. Create src/outreach/ics_generator.py
      2. Pure Python .ics generation (RFC 5545 string building, no external library)
      3. Wire into matches_tab.py: replace disabled .ics button (lines 258-262) with st.download_button
      4. Input: event name, date/time, location, description from match result
      5. Output: .ics file content as string, delivered via st.download_button
      6. VEVENT fields: SUMMARY, DTSTART, DTEND, LOCATION, DESCRIPTION, UID
```

#### Context for feature-6 (Funnel)

```
documentation:
  - src/ui/matches_tab.py (UI module pattern)
  - src/app.py (lines 175-190, placeholder to replace)
  - data/pipeline_sample_data.csv (real data from Sprint 1)

prepared:
  - key: "architecture"
    content: |
      1. Create src/ui/pipeline_tab.py
      2. Replace render_pipeline_tab() in src/app.py with import from new module
      3. Use plotly.graph_objects.Funnel for 6-stage visualization
      4. Stages: Discovered -> Matched -> Contacted -> Confirmed -> Attended -> Member Inquiry
      5. Read data/pipeline_sample_data.csv for stage counts
      6. Hover tooltips with actual speaker/event names from the pipeline data
      7. Keep datasets.courses display below the funnel
```

#### Context for feature-7 (Handoff)

```
documentation:
  - All output files from features 1-6

prepared:
  - key: "architecture"
    content: |
      1. Create data/track_b_data_package.md
      2. Compile: match results summary, pipeline funnel numbers, university coverage map, ROI inputs
      3. This is a documentation task, not code - no tests needed
      4. Read existing match data, pipeline CSV, and scraping results
```

### Step 5: Route Features

```
route_feature(featureId="feature-1", preferredWorkerType="backend")
route_feature(featureId="feature-2", preferredWorkerType="backend")
route_feature(featureId="feature-3", preferredWorkerType="frontend")
route_feature(featureId="feature-4", preferredWorkerType="backend")
route_feature(featureId="feature-5", preferredWorkerType="backend")
route_feature(featureId="feature-6", preferredWorkerType="frontend")
route_feature(featureId="feature-7", preferredWorkerType="backend")
```

### Step 6: Launch Phase 1 (3 parallel workers)

```
start_parallel_workers(
  featureIds = ["feature-1", "feature-4", "feature-6"],
  customPrompts = {
    "feature-1": <SCRAPER_PROMPT>,
    "feature-4": <EMAIL_PROMPT>,
    "feature-6": <FUNNEL_PROMPT>
  }
)
```

See Section 5 for full custom prompts.

### Step 7: Monitor & Steer

```
# Heartbeat check every 2-3 minutes
check_all_workers(heartbeat=True)

# Deep inspection when needed
check_worker(featureId="feature-1", lines=50)
get_worker_confidence(featureId="feature-1")

# Course-correct if needed
send_worker_message(featureId="feature-1", message="...")
```

### Step 8: Gate & Chain

When each Phase 1 worker completes:

```
# 1. Verify tests pass
run_verification(command="pytest tests/ -v --tb=short", featureId="feature-N")

# 2. Review output
check_worker(featureId="feature-N", lines=100)

# 3. Mark complete
mark_complete(featureId="feature-N", success=True)

# 4. Commit
commit_progress(message="feat(cat3): <description>")

# 5. Launch dependent worker (if any)
start_worker(featureId="feature-M", customPrompt="...")
```

**Chain order:**
- feature-1 done -> launch feature-2
- feature-4 done -> launch feature-5
- feature-2 done -> launch feature-3
- ALL (1-6) done -> launch feature-7

### Step 9: Final Verification

```
run_verification(command="pytest tests/ -v --cov=src --cov-report=term-missing")
# Expect: 250+ tests, 80%+ coverage
```

---

## 4. TDD Protocol (All Workers)

Every worker receives this as a `prepared` context block with `priority: "required"`:

```
TDD PROTOCOL -- MANDATORY

You MUST follow test-driven development. No exceptions.

PHASE 1 - RED (Write Failing Tests First)
1. Create test file(s) in tests/ directory
2. Write test classes with descriptive names
3. Use pytest fixtures: tmp_path for cache, monkeypatch for env vars
4. Use unittest.mock.patch for external deps (Gemini API, HTTP, Playwright)
5. Run: pytest tests/test_<module>.py -v
6. Confirm: ALL tests FAIL (import errors or assertion errors)

PHASE 2 - GREEN (Minimal Implementation)
1. Create source file(s) in src/ directory
2. Implement the MINIMUM code to pass each test
3. Follow the EXACT code spec from docs/sprints/sprint-2-discovery-email.md
4. Run: pytest tests/test_<module>.py -v
5. Confirm: ALL tests PASS

PHASE 3 - IMPROVE (Refactor)
1. Add type annotations to ALL function signatures
2. Use logging module (never print())
3. Run FULL test suite: pytest tests/ -v --tb=short
4. Confirm: ALL existing 199+ tests STILL PASS plus your new tests
5. No hardcoded secrets. No print() statements.

RULES:
- Mock ALL external calls (HTTP, Gemini API, Playwright). No real network access in tests.
- Follow existing patterns in src/matching/explanations.py for LLM and cache code.
- Use generate_text() from src/gemini_client.py, NOT a Gemini SDK import.
- Append-only to src/config.py (never modify existing constants).
- Keep functions under 50 lines, files under 400 lines.
```

---

## 5. Custom Worker Prompts

### feature-1 (Scraper) Prompt

```
Sprint 2 Task A2.1: Web Scraping Pipeline

YOU MUST FOLLOW TDD. Read the full spec at docs/sprints/sprint-2-discovery-email.md
task A2.1 (lines 34-451). The spec contains COMPLETE function signatures and
implementation details. Follow them exactly.

STEP 1 (RED): Write tests/test_scraper.py with:
- test_validate_public_demo_url_rejects_localhost
- test_validate_public_demo_url_rejects_private_ips
- test_validate_public_demo_url_rejects_non_http
- test_validate_public_demo_url_accepts_edu_domains
- test_cache_key_deterministic
- test_save_and_load_cache (use tmp_path)
- test_cache_ttl_expiration
- test_check_robots_txt_allowed (mock HTTP)
- test_check_robots_txt_disallowed (mock HTTP)
- test_rate_limit_enforces_delay
- test_scrape_bs4_success (mock requests.get)
- test_scrape_playwright_success (mock playwright)
- test_scrape_university_returns_cache_on_hit
- test_scrape_university_raises_on_robots_deny
- test_scrape_all_universities_handles_failures

STEP 2 (GREEN): Create src/scraping/__init__.py and src/scraping/scraper.py
following the spec exactly.

STEP 3 (IMPROVE): Type annotations, docstrings, run full suite.

After implementation: pytest tests/ -v --tb=short
```

### feature-4 (Email) Prompt

```
Sprint 2 Task A2.4: Outreach Email Generation

YOU MUST FOLLOW TDD. Read the full spec at docs/sprints/sprint-2-discovery-email.md
task A2.4.

STEP 1 (RED): Write tests/test_email_generator.py with:
- test_generate_email_returns_all_fields (mock generate_text)
- test_generate_email_uses_cache (use tmp_path)
- test_generate_email_fallback_on_api_error
- test_prompt_includes_speaker_and_event_details
- test_email_cache_key_deterministic
- test_email_panel_renders (test data wiring, not Streamlit rendering)

STEP 2 (GREEN): Create:
- src/outreach/__init__.py
- src/outreach/email_generator.py (follow explanations.py pattern)
- src/ui/email_panel.py

Wire into src/ui/matches_tab.py: replace the no-op email button (lines 250-256)
with real generation. Store result in st.session_state["pending_email_match"],
render email preview via email_panel.

Use generate_text() from src/gemini_client.py. Cache under
cache/emails/<sha256(speaker+event)>.json.

STEP 3 (IMPROVE): Type annotations, run full suite.

After implementation: pytest tests/ -v --tb=short
```

### feature-6 (Funnel) Prompt

```
Sprint 2 Task A2.6: Pipeline Funnel Visualization

YOU MUST FOLLOW TDD. Read the full spec at docs/sprints/sprint-2-discovery-email.md
task A2.6.

STEP 1 (RED): Write tests/test_pipeline_tab.py with:
- test_load_pipeline_data_from_csv
- test_aggregate_funnel_stages (counts are monotonically decreasing)
- test_funnel_stages_correct_order
- test_hover_data_includes_names
- test_empty_data_handled_gracefully
- test_create_funnel_chart_returns_figure

STEP 2 (GREEN): Create src/ui/pipeline_tab.py
- Read data/pipeline_sample_data.csv
- Use plotly.graph_objects.Funnel
- 6 stages: Discovered > Matched > Contacted > Confirmed > Attended > Member Inquiry
- Hover tooltips with real speaker/event names

Modify src/app.py:
- Replace the placeholder render_pipeline_tab (lines 177-190) with import
  from src.ui.pipeline_tab
- Keep the function signature: render_pipeline_tab(datasets) -> None

STEP 3 (IMPROVE): Type annotations, run full suite.

After implementation: pytest tests/ -v --tb=short
```

### feature-2 (Extractor) Prompt

```
Sprint 2 Task A2.2: LLM Extraction Pipeline

YOU MUST FOLLOW TDD. Read the full spec at docs/sprints/sprint-2-discovery-email.md
task A2.2 (lines 455+). The spec has COMPLETE code.

STEP 1 (RED): Write tests/test_llm_extractor.py with:
- test_preprocess_html_strips_scripts_and_styles
- test_preprocess_html_strips_nav_and_footer
- test_preprocess_html_truncates_to_max_chars
- test_extract_events_returns_list (mock generate_text)
- test_extract_events_handles_malformed_json
- test_extract_events_handles_empty_response
- test_extraction_prompt_includes_university_and_url
- test_extraction_cache_save_and_load (tmp_path)
- test_extraction_success_rate_threshold

STEP 2 (GREEN): Create src/extraction/__init__.py and src/extraction/llm_extractor.py.
Use generate_text() from src/gemini_client.py (NOT `from gemini import Gemini`).

STEP 3 (IMPROVE): Type annotations, run full suite.

After implementation: pytest tests/ -v --tb=short
```

### feature-3 (Discovery Tab) Prompt

```
Sprint 2 Task A2.3: Discovery Tab UI

YOU MUST FOLLOW TDD. Read the full spec at docs/sprints/sprint-2-discovery-email.md
task A2.3.

STEP 1 (RED): Write tests/test_discovery_tab.py with:
- test_university_configs_loaded
- test_add_to_matching_transforms_event_data
- test_custom_url_validation_called
- test_discovery_results_formatted_for_dataframe

STEP 2 (GREEN): Create src/ui/discovery_tab.py following src/ui/matches_tab.py patterns.

Modify src/app.py:
- Replace placeholder render_discovery_tab (lines 159-173) with import from new module
- Keep function signature: render_discovery_tab(datasets) -> None
- University selector dropdown, "Discover Events" button, results table
- "Add to Matching" stores events in session state
- Custom URL input with validate_public_demo_url()

STEP 3 (IMPROVE): Type annotations, run full suite.

After implementation: pytest tests/ -v --tb=short
```

### feature-5 (.ics) Prompt

```
Sprint 2 Task A2.5: Calendar .ics Generation

YOU MUST FOLLOW TDD. Read the full spec at docs/sprints/sprint-2-discovery-email.md
task A2.5.

STEP 1 (RED): Write tests/test_ics_generator.py with:
- test_generate_ics_valid_rfc5545
- test_ics_contains_vevent_fields (SUMMARY, DTSTART, LOCATION, DESCRIPTION)
- test_ics_handles_missing_date_gracefully
- test_ics_handles_missing_location
- test_ics_uid_unique_per_event
- test_ics_content_type_correct

STEP 2 (GREEN): Create src/outreach/ics_generator.py.
Pure Python RFC 5545 string building (no external library needed).

Wire into src/ui/matches_tab.py: replace the disabled .ics button (lines 258-262)
with st.download_button that serves the generated .ics file.

STEP 3 (IMPROVE): Type annotations, run full suite.

After implementation: pytest tests/ -v --tb=short
```

---

## 6. Commit Messages (Per Feature)

```
feat(cat3): add web scraping pipeline with BS4/Playwright backends
feat(cat3): add LLM extraction pipeline for university events
feat(cat3): add discovery tab UI with university event scanner
feat(cat3): add outreach email generation with Gemini
feat(cat3): add calendar invite .ics generation
feat(cat3): add pipeline funnel visualization with Plotly
docs(cat3): compile Track B handoff data package
```

---

## 7. Risk Mitigation

| Risk | Mitigation |
|---|---|
| Worker stuck in loop | `get_worker_confidence` to detect, `send_worker_message` to redirect, `rollback_feature` if irrecoverable |
| Worker modifies wrong files | `check_rollback_conflicts` before merge, `rollback_feature` to restore |
| Tests fail after completion | `mark_complete(success=False)` for retry; orchestrator diagnoses before re-launch |
| Merge conflict on shared files | File ownership matrix prevents this; shared files serialized by dependency order |
| Worker imports Gemini SDK | Custom prompts explicitly say "use generate_text() from src/gemini_client.py, NOT SDK" |
| Worker uses print() | TDD protocol requires logging module; orchestrator reviews before mark_complete |
| Playwright unavailable | Spec handles this: fall back to bs4 with logged warning, use cached HTML |
| Context window overflow | Each task scoped to 1-5 files; Sonnet 4.6 has ample context for single-task focus |

---

## 8. Verification Gates

### Gate 1: Per-Worker (after each feature)

```
# Worker's own tests
run_verification(command="pytest tests/test_<module>.py -v", featureId="feature-N")

# Full regression suite
run_verification(command="pytest tests/ -v --tb=short", featureId="feature-N")
```

### Gate 2: Orchestrator Review (before mark_complete)

The orchestrator (Opus 4.6) checks:
1. `check_worker(featureId, lines=100)` -- read worker output
2. Tests were written FIRST (TDD compliance)
3. Type annotations present on all functions
4. No `print()`, no hardcoded secrets
5. Return contracts match spec
6. Only then: `mark_complete(success=True)`

### Gate 3: Integration (after all features)

```
pytest tests/ -v --cov=src --cov-report=term-missing
# Target: 250+ tests, 80%+ coverage
```

### Gate 4: Smoke Test (manual)

```
streamlit run src/app.py
```
- Discovery tab: university selector renders, discover button works
- Pipeline tab: funnel chart renders with hover tooltips
- Matches tab: email and .ics buttons work

---

## 9. Timeline Estimate

| Phase | Workers | Wall Clock |
|---|---|---|
| Phase 1: features 1, 4, 6 (parallel) | 3 | ~45-60 min |
| Phase 1b: feature 5 (after 4) | 1 + ongoing | ~20-30 min |
| Phase 2: feature 2 (after 1) | 1 + ongoing | ~30-45 min |
| Phase 3: feature 3 (after 2) | 1 | ~30-45 min |
| Phase 4: feature 7 (after all) | 1 | ~15-20 min |
| Integration verification | -- | ~15 min |
| **Total** | | **~2.5-3.5 hours** |

vs. sequential human dev: ~20+ hours

---

## 10. Orchestrator Checklist

```
[ ] Branch sprint2-cat3 created from sprint1-cat3
[ ] orchestrator_init called with all 7 features
[ ] Dependencies set (2->1, 3->2, 5->4, 7->all)
[ ] Verification configured (pytest)
[ ] Feature context set for all 7 features
[ ] Phase 1 launched: features 1, 4, 6
[ ] Phase 1 monitored: heartbeat checks every 2-3 min
[ ] feature-4 complete -> feature-5 launched
[ ] feature-1 complete -> feature-2 launched
[ ] feature-6 complete -> committed
[ ] feature-5 complete -> committed
[ ] feature-2 complete -> feature-3 launched
[ ] feature-3 complete -> committed
[ ] feature-7 launched (all deps met)
[ ] feature-7 complete -> committed
[ ] Full test suite: 250+ tests, 80%+ coverage
[ ] Smoke test: app runs, all 3 tabs functional
[ ] Final commit on sprint2-cat3
```
