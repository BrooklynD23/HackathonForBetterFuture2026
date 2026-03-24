# Codebase Concerns

**Analysis Date:** 2026-03-20

## Tech Debt

**Verification and governance drift around Sprint 5 closeout:**
- Issue: Category 3 closeout evidence disagrees across the repo. `Category 3 - IA West Smart Match CRM/docs/README.md`, `Category 3 - IA West Smart Match CRM/docs/sprints/README.md`, and `Category 3 - IA West Smart Match CRM/.status.md` still state `366 passed`, while `tasks/todo.md` records `373 passed`, and the current 2026-03-20 verification run is `./.venv/bin/python -m pytest -q` -> `378 passed`.
- Files: `Category 3 - IA West Smart Match CRM/docs/README.md`, `Category 3 - IA West Smart Match CRM/docs/sprints/README.md`, `Category 3 - IA West Smart Match CRM/.status.md`, `tasks/todo.md`
- Impact: Sprint 5 wrap-up lacks one trustworthy verification baseline, so a closeout commit can be declared done against stale numbers.
- Fix approach: reconcile one canonical closeout result first, then refresh every derived mirror from that single source.

**Sprint 5 planning is still task-board driven instead of GSD-driven:**
- Issue: `tasks/todo.md` assumes Sprint 5 will be executed as a GSD closeout milestone, but `.planning/` had no checked-in planning state before this concerns map was written.
- Files: `tasks/todo.md`, `.planning/`
- Impact: wrap-up scope, verification gates, and residual risks live in a mutable task board instead of structured planning artifacts.
- Fix approach: create the Sprint 5 planning state before more closeout changes land.

**Generated-runtime outputs are not clearly separated from source-controlled content:**
- Issue: runtime caches and feedback outputs are written under tracked project folders, but ignore rules only cover embedding `.npy` artifacts and a few Python-generated files.
- Files: `.gitignore`, `Category 3 - IA West Smart Match CRM/.gitignore`, `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`, `Category 3 - IA West Smart Match CRM/cache/`, `Category 3 - IA West Smart Match CRM/data/`
- Impact: a demo or rehearsal can dirty the worktree with cache JSON, feedback logs, and other generated artifacts that look like product changes during Sprint 5 closeout.
- Fix approach: move generated runtime outputs to an explicitly untracked location or expand ignore coverage before the final closeout pass.

**Large single-file hotspots raise regression risk for late-stage changes:**
- Issue: several core modules stay monolithic: `src/embeddings.py` (562 lines), `src/scraping/scraper.py` (479 lines), `src/matching/factors.py` (462 lines), `src/extraction/llm_extractor.py` (452 lines), `src/ui/matches_tab.py` (435 lines), and `src/matching/engine.py` (397 lines).
- Files: `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`, `Category 3 - IA West Smart Match CRM/src/matching/factors.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/matching/engine.py`
- Impact: Sprint 5 bug-fix work is likely to touch multi-responsibility modules where a narrow change can perturb unrelated behavior.
- Fix approach: defer structural refactors until after closeout, but protect each touched hotspot with focused contract tests.

## Known Bugs

**Discovered events do not actually enter the match pool:**
- Symptoms: `render_discovery_tab()` appends transformed events into `st.session_state["matching_discovered_events"]`, but `render_matches_tab()` and `_render_event_matches()` only read the original `events` DataFrame and never consume that state key.
- Files: `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/docs/testing/test_log.md`
- Trigger: click `Add to Matching` after a discovery run.
- Workaround: none for newly discovered events; only the preloaded CPP event list can be matched.

**Demo Mode does not cover the core matching flow on a clean checkout:**
- Symptoms: `scripts/sprint4_preflight.py` currently warns that all embedding artifacts are missing. `src/app.py` blocks the Matches tab when embedding cache validation fails, and `src/demo_mode.py` only fixtures discovery, explanation, email, pipeline, volunteer, and feedback payloads, not the match-ranking inputs themselves.
- Files: `Category 3 - IA West Smart Match CRM/src/app.py`, `Category 3 - IA West Smart Match CRM/src/demo_mode.py`, `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`, `Category 3 - IA West Smart Match CRM/cache/demo_fixtures/`, `Category 3 - IA West Smart Match CRM/tests/test_demo_mode.py`
- Trigger: launch the app without warmed embedding cache artifacts and without live Gemini access.
- Workaround: pre-generate embeddings or provide a valid Gemini key before the session starts.

**Feedback persistence depends on current working directory instead of project root:**
- Symptoms: `record_feedback()` appends to `data/feedback_log.csv` via a plain relative path, unlike the rest of the runtime which resolves paths from `PROJECT_ROOT` and `DATA_DIR`.
- Files: `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`
- Trigger: launch the app from a directory other than `Category 3 - IA West Smart Match CRM/`.
- Workaround: only run the app from the Category 3 project root.

## Security Considerations

**robots.txt failures currently fail open:**
- Risk: `check_robots_txt()` logs a warning and returns `True` whenever the robots fetch fails, allowing `scrape_university()` to proceed.
- Files: `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`
- Current mitigation: `validate_public_demo_url()` constrains protocol, host type, and public-IP resolution.
- Recommendations: for Sprint 5 closeout, prefer cache-only fallback or explicit operator acknowledgement instead of assuming permission on robots fetch failure.

**Generated feedback and cache artifacts can be mistaken for source-controlled product data:**
- Risk: `data/feedback_log.csv` and cache directories such as `cache/scrapes/`, `cache/extractions/`, `cache/explanations/`, and `cache/emails/` are operational outputs but are not comprehensively ignored.
- Files: `.gitignore`, `Category 3 - IA West Smart Match CRM/.gitignore`, `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`
- Current mitigation: checked-in demo fixtures stay isolated in `cache/demo_fixtures/`.
- Recommendations: explicitly ignore or relocate these outputs before final wrap-up so rehearsal data and generated content do not bleed into release commits.

## Performance Bottlenecks

**Cold-start embedding generation is a blocking prerequisite, not a background task:**
- Problem: `_resolve_embedding_lookup_dicts()` performs cache validation during app startup and prevents match rendering until valid speaker, event, and course embeddings exist.
- Files: `Category 3 - IA West Smart Match CRM/src/app.py`, `Category 3 - IA West Smart Match CRM/src/embeddings.py`
- Cause: the app treats embedding availability as a hard gate and falls back to synchronous Gemini generation when a key is available.
- Improvement path: ship prebuilt artifacts for demo/closeout paths or add a deterministic offline ranking path for Demo Mode.

**Discovery and AI generation remain synchronous UI-path operations:**
- Problem: scraping, extraction, explanation generation, and email generation run inline from Streamlit interactions.
- Files: `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`
- Cause: cache hits are the only latency control; there is no background queue or precomputed closeout bundle beyond demo fixtures.
- Improvement path: treat warmed caches as a release artifact and surface cache-miss risk before rehearsals and day-of use.

## Fragile Areas

**The session-state contract is fragmented across tabs and helpers:**
- Files: `Category 3 - IA West Smart Match CRM/src/runtime_state.py`, `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/email_panel.py`, `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`
- Why fragile: some keys are centrally initialized (`match_results_df`, `scraped_events`, `emails_generated`), while others are created ad hoc (`feedback_log`, `feedback_decisions`, `discovered_events`, `matching_discovered_events`, `pending_email_match`).
- Safe modification: define one shared runtime-state schema and keep cross-tab keys in a single module.
- Test coverage: unit-level state normalization is covered, but cross-tab end-to-end behavior is not.

**Pipeline and volunteer metrics blend real and simulated values:**
- Files: `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/volunteer_dashboard.py`, `Category 3 - IA West Smart Match CRM/data/pipeline_sample_data.csv`
- Why fragile: counts fall back to hard-coded assumptions such as `cpp_event_count = 15`, `Contacted = 80%`, `Confirmed = 45%`, and volunteer acceptance/attendance simulation when live feedback is absent.
- Safe modification: keep projection logic clearly separate from real runtime metrics and derive baseline counts from loaded datasets instead of constants.
- Test coverage: helpers are unit-tested, but the end-user distinction between projected and real data is easy to blur during closeout.

**Sprint 5 closeout runs inside a dirty worktree:**
- Files: `.claude/settings.local.json`, `tasks/todo.md`, `Category 3 - IA West Smart Match CRM/.claude/`, `Category 3 - IA West Smart Match CRM/claude-progress.txt`, `Category 3 - IA West Smart Match CRM/init.sh`
- Why fragile: unrelated local edits and untracked files increase the chance of staging or reviewing the wrong delta during final closeout.
- Safe modification: stage with explicit pathspecs and review `git status --short` before every Sprint 5 commit.
- Test coverage: not applicable.

## Scaling Limits

**The current product contract is tuned to the 77-row hackathon dataset:**
- Current capacity: `18` speakers, `15` CPP events, `35` course sections, and `9` calendar rows loaded from `Category 3 - IA West Smart Match CRM/data/`.
- Limit: multiple UI paths embed assumptions about the fixed CPP baseline and top-3 matching shape.
- Scaling path: derive event/course counts and funnel baselines from loaded data, then lift hard-coded constants before any post-hackathon expansion.

**Persistence is single-user and file-based:**
- Current capacity: one local operator session with append-only files and cache directories.
- Limit: `st.session_state` plus CSV/JSON append patterns do not provide concurrency control, deduplication, or audit isolation across multiple operators.
- Scaling path: if the app survives beyond the hackathon demo, move feedback, pipeline state, and generated artifacts into an explicit data store.

## Dependencies at Risk

**Python and package parity are not fully pinned to the tested environment:**
- Risk: the local verification environment is Python `3.12.3`, while `runtime.txt` pins Streamlit Cloud to `python-3.11`, and `requirements.txt` already documents package-version drift on this platform.
- Impact: local green tests do not fully prove cloud runtime parity for Sprint 5 closeout.
- Migration plan: capture one verified run in a Python 3.11 environment and update dependency pins to the versions actually required.

**The scraping path depends on optional browser/runtime availability:**
- Risk: `playwright` is required for the SDSU target in `UNIVERSITY_TARGETS`, but cloud and clean-machine behavior depend on warmed cache fallback when browser support is absent.
- Impact: the discovery story is only stable when cache artifacts already exist.
- Migration plan: keep a fully warmed cache bundle for all target universities and reduce the live scrape surface before closeout.

## Missing Critical Features

**Sprint 5 lacks a canonical closeout spec inside the active planning system:**
- Problem: `tasks/todo.md` frames Sprint 5 as a GSD closeout milestone, but there is still no canonical Sprint 5 spec or phase plan under `.planning/`.
- Blocks: a clean wrap-up process with traceable scope, verification gates, and residual-risk handoff.

**Operational closeout evidence is still template-grade rather than completed evidence:**
- Problem: `Category 3 - IA West Smart Match CRM/docs/testing/test_log.md` and `Category 3 - IA West Smart Match CRM/docs/testing/rehearsal_log.md` remain mostly blank templates, and `bug_log.md` records no new issues while the discovery-to-matching flow remains broken.
- Blocks: a defensible Sprint 5 claim that demo rehearsal, fallback behavior, and wrap-up validation are complete.

**The repo claims only documentation/governance wrap-up remains, but runtime prep is still incomplete:**
- Problem: `Category 3 - IA West Smart Match CRM/docs/README.md` states the remaining work is documentation/governance refresh and a sprint-closeout commit, while current preflight still warns about missing embedding, scrape, extraction, explanation, and email cache readiness.
- Blocks: safe declaration that the product is demo-ready without additional operational prep.

## Test Coverage Gaps

**No cross-tab regression proves discovery output reaches the matches flow:**
- What's not tested: the actual `Discover Events` -> `Add to Matching` -> `Matches` selector handoff.
- Files: `Category 3 - IA West Smart Match CRM/tests/test_discovery_tab.py`, `Category 3 - IA West Smart Match CRM/tests/test_matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`
- Risk: the main live-demo path can stay broken while unit tests still pass.
- Priority: High

**The suite is heavily mocked and does not exercise a real Streamlit/browser path:**
- What's not tested: real Streamlit rendering, real browser interactions, clipboard flow, and end-to-end tab traversal.
- Files: `Category 3 - IA West Smart Match CRM/tests/conftest.py`, `Category 3 - IA West Smart Match CRM/tests/`, `Category 3 - IA West Smart Match CRM/docs/testing/test_log.md`
- Risk: integration defects can hide behind mocked `streamlit` calls and only appear during rehearsal.
- Priority: High

**Deployment-parity coverage is still narrow:**
- What's not tested: a full Python 3.11 / Streamlit Cloud style run with cache-only discovery and missing-live-network conditions.
- Files: `Category 3 - IA West Smart Match CRM/runtime.txt`, `Category 3 - IA West Smart Match CRM/tests/test_sprint4_preflight.py`, `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`
- Risk: the repo can be locally green on Python 3.12.3 and still fail in the target hosted runtime.
- Priority: Medium

---

*Concerns audit: 2026-03-20*
