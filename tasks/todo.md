# Todo

## Current Work

### CRM Routing and Jarvis Fix Pass

_Overlap with **Frontend Routing and Match Engine QA Fix Pass** below: that pass owns the initial router/query-param sync + Match Engine regression work; this pass closes the Jarvis discovery wiring, NemoClaw documentation, coordinator/Jarvis UI ordering, sign-out follow-up, and the dated Playwright demo re-check._

- [x] Refactor Category 3 query-param handling to prefer `st.query_params` on the pinned Streamlit 1.42.x runtime, keep fallback support for legacy experimental APIs, and update router regression tests.
- [x] Wire the Jarvis `discover_events` tool through scrape + `extract_events(...)`, then update `tests/test_discovery_tool.py` to cover the extracted-event path and the no-Streamlit contract.
- [x] Document the dormant NemoClaw path in the Category 3 README and add a clarifying module note in `src/coordinator/nemoclaw_adapter.py`.
- [x] Apply the small demo-hardening UI tweaks: move the Jarvis checkbox above the dashboard iframe, keep the coordinator coverage-map expectation caption honest, and add a brief match-engine discoverability caption.
- [x] Run targeted verification for the touched Category 3 tests (`test_page_router`, `test_discovery_tool`, `test_app`, `test_match_engine_page`).
- [x] Run a dated Playwright browser pass on `http://127.0.0.1:8501`, save screenshots under `Category 3 - IA West Smart Match CRM/output/playwright/`, and write the QA report to `Category 3 - IA West Smart Match CRM/docs/testing/2026-03-25-playwright-demo-report.md`.
- [x] Add a review note here with implementation results, verification evidence, and any residual demo risk.

#### Review

- Implementation:
  - `page_router.py` now stages demo-mode changes through a pending navigation override so sign-out can clear `demo=1` without tripping Streamlit’s widget-state mutation guard.
  - `discovery_tool.py` stays wired through scrape + `extract_events(...)`; README/module documentation reflects NemoClaw’s dormant status; dashboard and Match Engine captions/ordering match the intended demo story.
  - Added `scripts/run_playwright_demo_qa.py` plus updated `tests/test_e2e_flows.py` so the routed workspace, deep links, Jarvis proposal flow, and sign-out path have reproducible browser coverage.
- Verification:
  - `python3 -m py_compile 'Category 3 - IA West Smart Match CRM/src/ui/page_router.py' 'Category 3 - IA West Smart Match CRM/tests/test_page_router.py' 'Category 3 - IA West Smart Match CRM/tests/conftest.py' 'Category 3 - IA West Smart Match CRM/scripts/run_playwright_demo_qa.py' 'Category 3 - IA West Smart Match CRM/tests/test_e2e_flows.py'`
  - `cd 'Category 3 - IA West Smart Match CRM' && /tmp/hbf-pytest-venv/bin/python -m pytest tests/test_page_router.py -q` -> `8 passed`
  - `cd 'Category 3 - IA West Smart Match CRM' && /tmp/hbf-pytest-venv/bin/python scripts/run_playwright_demo_qa.py` -> `16 cases`, `10 warnings`, `0 page_errors`, `0 request_failures`
  - `cd 'Category 3 - IA West Smart Match CRM' && /tmp/hbf-pytest-venv/bin/python -m pytest tests/test_e2e_flows.py -q` -> `9 passed`
  - `cd 'Category 3 - IA West Smart Match CRM' && /tmp/hbf-pytest-venv/bin/python -m pytest -q` -> `591 passed`, `1 failed`
  - Dated browser report: `Category 3 - IA West Smart Match CRM/docs/testing/2026-03-25-playwright-demo-report.md`
- Demo outcome:
  - The Playwright pass covered landing, login, View Demo, deep links, workspace nav, Jarvis toggle + text command + approve path, and sign-out. All 16 scripted checks passed, and screenshots were saved under `Category 3 - IA West Smart Match CRM/output/playwright/`.
  - Jarvis approval completed end-to-end in the UI with `Found 0 event(s) (source: cache)`, which confirms the patched tool path in this environment.
- Residual risk:
  - The embeddings API-key regression was a test isolation issue, not a runtime bug. The targeted regression now passes; the full suite was not rerun after this cleanup-only follow-up.
  - Jarvis voice/TTS dependencies were absent locally, so the command center degraded to text-only warnings during QA.
  - Discovery execution completed from cache with zero events here; live discovery quality still depends on cache freshness, network reachability, and Gemini availability.
  - Cleanup note: removed the accidental mockup `node_modules` tree and added ignore rules so dependency reinstalls do not flood the worktree again.

### Frontend Routing and Match Engine QA Fix Pass

_See **CRM Routing and Jarvis Fix Pass** for Jarvis/NemoClaw/discovery-tool deliverables and the latest Browser MCP table._

- [x] Reproduce the routing defects from the browser QA report against the current router helpers and Streamlit runtime assumptions.
- [x] Harden query-param read/write behavior so deep links, in-app navigation, and invalid-route normalization keep the URL bar in sync.
- [x] Improve the Match Engine page so the primary workspace shows meaningful above-the-fold content and an explicit empty state when match data is sparse.
- [x] Add or update targeted regression tests for router normalization/synchronization and Match Engine rendering.
- [x] Run targeted verification, then add a review note here summarizing pass/fail status and residual risk.

#### Review

- Root cause for the routing defects was the mixed query-param API usage in `page_router.py`: reads could come from `st.query_params` while writes went through `experimental_set_query_params`, which is fragile on the Streamlit 1.42.x runtime captured in QA.
- The router now uses one read/write family consistently, so alias routes, unknown-route normalization, and in-app navigation all go through the same query-param sync path.
- The Match Engine page no longer reserves a 5000px iframe height; it uses a tighter height and renders a visible shortlist summary or explicit empty state instead of leaving the main pane visually blank.
- Added regression coverage for query-param synchronization and Match Engine sparse-data rendering.
- Verification:
  - `python3 -m py_compile 'Category 3 - IA West Smart Match CRM/src/ui/page_router.py' 'Category 3 - IA West Smart Match CRM/src/ui/match_engine_page.py' 'Category 3 - IA West Smart Match CRM/tests/test_page_router.py' 'Category 3 - IA West Smart Match CRM/tests/test_match_engine_page.py'`
  - `cd 'Category 3 - IA West Smart Match CRM' && /tmp/hbf-pytest-venv/bin/python -m pytest tests/test_page_router.py -q` -> `5 passed`
  - `cd 'Category 3 - IA West Smart Match CRM' && /tmp/hbf-pytest-venv/bin/python -m pytest tests/test_match_engine_page.py -q` -> `2 passed`
- Residual risk:
  - The live browser QA run used Streamlit 1.42.2 on the already-running `:8501` server. I did not re-run that exact browser flow after the patch, so bookmark/deep-link behavior still needs one manual confirmation pass against that runtime.
- 2026-03-25 closeout: Playwright follow-up on `127.0.0.1:8501` confirms cold `?route=matches`, `?route=coordinator&demo=1`, unknown-route normalization, workspace nav, Jarvis proposal/approve flow, and sign-out; see `Category 3 - IA West Smart Match CRM/docs/testing/2026-03-25-playwright-demo-report.md`.

### UI Audit Review Fix Pass

- [x] Replace the split `current_page`/`current_view` navigation with a single routed V2 workspace.
- [x] Wire landing, login, coordinator, and match-engine controls to real destinations instead of dead `#` links.
- [x] Promote the legacy Matches, Discovery, Pipeline, Expansion, and Volunteer surfaces into reachable V2 routes.
- [x] Replace the coordinator dashboard heatmap placeholder with a real Plotly map and warn on unmapped metro data.
- [x] Update the affected tests/docs, run targeted verification, and add a review note with results.

#### Review

- Unified the V2 router around query-param-synced `current_page` routes and removed the live dependency on the unreachable `current_view` CRM shell.
- Wired the landing/login/dashboard/match-engine iframe controls to real page destinations, added a shared iframe navigation bridge, and made the public landing nav scroll to real sections instead of `#`.
- Exposed reachable V2 pages for Dashboard, Matches, Discovery, Pipeline, Analytics, and Match Engine; Analytics now hosts the expansion map and volunteer dashboard, and the dashboard can surface Jarvis on demand.
- Replaced the coordinator heatmap mock with a live Plotly campus coverage map built from the shared expansion-map geography logic, including warnings for unmapped metro regions.
- Verification:
  - `python3 -m py_compile src/app.py src/ui/page_router.py src/ui/html_base.py src/ui/landing_page_v2.py src/ui/login_page.py src/ui/coordinator_dashboard.py src/ui/match_engine_page.py src/ui/expansion_map.py tests/test_app.py tests/test_expansion_map.py tests/test_page_router.py`
  - `"/mnt/c/Users/DangT/documents/github/HackathonForBetterFuture2026/.venv/Scripts/python.exe" -m pytest tests/test_app.py tests/test_expansion_map.py tests/test_page_router.py -q` -> `25 passed`

### Milestone Wrap-Up: v1.0 then v2.0 (Sequential)

- [x] Validate milestone pre-flight status for v1.0 and v2.0 (audit presence, phase completion, requirement coverage).
- [x] Clean accidental `--help` milestone artifacts generated during CLI probing.
- [x] Finalize v1.0 archive state (ensure archive docs + MILESTONES entry + audit archive) and create tag `v1.0`.
- [x] Archive v2.0 milestone artifacts (`ROADMAP`, `REQUIREMENTS`, milestones entry), then collapse active roadmap scope.
- [x] Update PROJECT/STATE for post-v2 shipped state and remove live `.planning/REQUIREMENTS.md` for next milestone reset.
- [x] Commit v2.0 archive changes and create tag `v2.0`.
- [x] Add verification + outcomes to the review section.

### Sprint 6 Phase 0-1 Review Fix Pass

- [x] Fix all HIGH findings from the latest `$ecc-code-review` report for Phase 0/1.
- [x] Close the MEDIUM finding by making landing-page factor visuals resilient to factor-count changes.
- [x] Close the LOW finding by removing unused imports and tightening test quality.
- [x] Verify touched files with targeted automated checks in the available environment.
- [x] Commit only the scoped fix files with a clear message.

### Sprint 5 GSD Closeout Orchestration

#### Requirements Restatement

- [x] Initialize GSD for this brownfield repo because `.planning/` does not exist yet.
- [x] Work on the new git branch `sprint5-cat3`.
- [x] Treat Sprint 5 as a closeout milestone for Category 3 unless a stronger local authority emerges:
  - The repo has no canonical Sprint 5 spec.
  - `Category 3 - IA West Smart Match CRM/docs/README.md` says the remaining work is documentation/governance refresh plus sprint closeout.
- [x] Use parallel subagents wherever they materially reduce context pressure or shorten independent discovery/review work.
- [x] Create a phase-based plan that ends with an `$ecc-code-review` audit, fixes, documentation updates, per-phase commits, and sprint closure.
- [x] Verify each phase with direct evidence before marking it complete.

#### Risks

- High: No canonical Sprint 5 spec exists in the repo, so scope must be derived from current closeout signals and verified against authoritative Category 3 docs.
- High: The worktree already contains unrelated local changes; do not revert or accidentally include them in Sprint 5 commits.
- Medium: GSD brownfield initialization may require codebase mapping before milestone planning can proceed.
- Medium: Closeout work may surface doc/governance drift that forces additional scoped cleanup beyond the initial assumption.

#### Execution Board

- [x] Phase 1: Establish Sprint 5 orchestration context.
  - Create and switch to branch `sprint5-cat3`.
  - Confirm whether GSD is already initialized.
  - Rewrite this task board for Sprint 5 orchestration.

- [x] Phase 2: Bootstrap GSD for the brownfield repo.
  - Map the existing codebase with parallel mapper agents.
  - Create `.planning/` project state, config, requirements, and roadmap for Sprint 5 closeout.
  - Record the Sprint 5 scope assumption in the planning docs.

- [x] Phase 3: Execute Sprint 5 closeout phases.
  - Run the planned closeout phases with parallel subagents where appropriate.
  - Keep commits scoped per phase with explicit pathspecs only.
  - Update progress in this file as work lands.

- [x] Phase 3.1: Runtime fixes and clean outputs.
  - Discovery events added from the Discovery tab now merge into the Matches event pool during the same session.
  - Demo Mode and offline/no-key runs no longer hard-block the Matches tab when embeddings are missing; warnings stay visible and fallback scoring is explicit.
  - Feedback persistence now resolves from config-backed project paths, and generated runtime artifacts are ignored without hiding checked-in demo fixtures.
  - Combined verification: `Category 3 - IA West Smart Match CRM/.venv/bin/python -m pytest tests/test_acceptance.py tests/test_discovery_tab.py tests/test_matches_tab.py tests/test_app.py -q` -> `37 passed in 21.78s`

- [x] Phase 3.2: Documentation and governance reconciliation.
  - Established one authoritative live verification baseline from `Category 3 - IA West Smart Match CRM/` with:
    - `timeout 300s ./.venv/bin/python -m pytest -q` -> `385 passed in 37.40s`
    - `timeout 180s ./.venv/bin/python scripts/sprint4_preflight.py` -> passes with warnings only for un-warmed live caches
  - Reconciled `docs/README.md`, `docs/sprints/README.md`, `.status.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, and this task board to that baseline.
  - Ran the repo governance workflow for `category:3`, regenerated `docs/governance/REPO_REFERENCE.md`, and emitted dated Sprint 5 audit/reconcile reports under `docs/governance/reports/`.
  - Verified the governance outputs report `0` safe reconciliations and `0` human-decision items before committing Phase 3.2.

- [x] Phase 3.3: Adversarial audit and sprint closure.
  - Planning artifacts created in `.planning/phases/03-adversarial-audit-and-sprint-closure/`: `03-CONTEXT.md`, `03-01-PLAN.md`, `03-02-PLAN.md`, `03-03-PLAN.md`.
  - Created `Category 3 - IA West Smart Match CRM/docs/reviews/2026-03-21-sprint5-code-review.md` and fixed the accepted findings without expanding scope.
  - Reran targeted verification (`87 passed in 6.56s`), full `pytest -q` (`392 passed in 11.93s`), and `scripts/sprint4_preflight.py` (same expected cache warnings only).
  - Updated `.planning/ROADMAP.md`, `.planning/STATE.md`, and this review section with final evidence, residual risks, and truthful manual follow-ups.
  - Close out Sprint 5 on `sprint5-cat3` with a scoped final commit.

### Sprint 4 Review Fix Pass

- [x] Fix the Sprint 4 review findings without expanding product scope.
- [x] Make `scripts/sprint4_preflight.py --prewarm-discovery` actually warm the caches it claims to warm.
- [x] Reconcile the deployment/runtime contract with Sprint 4 docs and make preflight validate content, not just file presence.
- [x] Harden discovery and extraction cache reads so corrupt or malformed cache files degrade safely instead of crashing.
- [x] Add regression tests for each fixed review finding and rerun targeted verification.

### Sprint 4 Autonomous Orchestration

#### Requirements Restatement

- Execute Sprint 4 for Category 3 from the reviewed sprint docs, using `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md` and `Category 3 - IA West Smart Match CRM/docs/sprints/sprint-4-ship.md` as the implementation authority.
- Work on the new git branch `sprint4-cat3`.
- Orchestrate with subagents and keep progress visible in this file.
- Treat Sprint 4 as ship-hardening only: testing, bug fixing, performance, deployment readiness, demo readiness, cache/demo-mode readiness, and final cleanup.
- Verify every code change with direct evidence before marking it complete.

#### Risks

- High: Sprint 4 explicitly forbids new feature work, so fixes must stay inside existing product contracts.
- High: Demo-mode, cache, and fallback paths can pass unit tests while still failing in the real demo flow.
- High: Deployment and performance work may expose environment-specific bugs not covered by the current local suite.
- Medium: The repo already has unrelated dirty files; avoid reverting or entangling them.
- Medium: Some Sprint 4 items are human-only operational tasks and must be separated from code-completable work.

#### Execution Board

- [x] Phase 1: Establish Sprint 4 execution context.
  - Create and switch to branch `sprint4-cat3`.
  - Reconcile current repo state, Sprint 4 authority docs, and Category 3 status.
  - Rewrite this task board for Sprint 4 orchestration.

- [ ] Phase 2: Audit Sprint 4 gaps with subagents.
- [x] Phase 2: Audit Sprint 4 gaps with subagents.
  - Compare current code/test/docs state against A4.1-A4.10 requirements.
  - Identify missing automation, weak fallback paths, deployment gaps, and verification gaps.
  - Turn findings into a prioritized implementation backlog.

- [x] Phase 3: Close code and test gaps.
  - Implement only Sprint 4 bug-fix, hardening, performance, deployment, and cleanup work.
  - Add or tighten tests where the current suite misses Sprint 4 acceptance criteria.
  - Keep fixes minimal and aligned with the existing runtime contracts.

- [x] Phase 4: Produce Sprint 4 operational artifacts.
  - Create testing/rehearsal/day-of prep artifacts that can be committed now.
  - Separate automated evidence from human-only rehearsal/video tasks.
  - Record any items that still require manual execution by the team.

- [x] Phase 5: Verify and close out.
  - Run targeted verification for all touched areas.
  - Run the full relevant regression suite if feasible in the project environment.
  - Update this review section with evidence, residual risks, and next manual steps.

#### Execution Guidance For Worker

- Start with the delta between Sprint 4 acceptance criteria and the current checked-in behavior.
- Prefer fixes that improve the real demo path and Demo Mode together instead of maintaining separate logic branches.
- Do not invent new UX or product scope under the banner of polish.
- If a Sprint 4 requirement is human-only, document it cleanly rather than faking completion in code.

## Review

- Milestone wrap-up (2026-03-24): finalized v1.0 then v2.0 sequentially, archived both milestones under `.planning/milestones/`, moved milestone tracking into `.planning/MILESTONES.md`, collapsed `.planning/ROADMAP.md` to shipped one-line entries, removed live `.planning/REQUIREMENTS.md` for next-milestone reset, and created annotated tags `v1.0` + `v2.0`. Note: no dedicated `.planning/v2.0-MILESTONE-AUDIT.md` existed at closeout; this was recorded as accepted tech debt in milestones.
- Sprint 6 Phase 0-1 review fix pass: refactored `src/ui/landing_page.py` into smaller helpers (clearing the >50-line function finding), made donut heading/colors derive from `DEFAULT_WEIGHTS` count for future factor expansion, removed dead/unused test imports, and replaced the partner-logo no-op assertions with concrete per-university checks plus dynamic-factor donut assertions in `tests/test_landing_page.py`.
- Sprint 6 Phase 0-1 verification:
  - `python3 -m compileall Category 3 - IA West Smart Match CRM/src/ui/landing_page.py Category 3 - IA West Smart Match CRM/tests/test_landing_page.py` -> both files compiled successfully.
  - `rg -n \"TODO|FIXME|console\\.log\" Category 3 - IA West Smart Match CRM/src/ui/landing_page.py Category 3 - IA West Smart Match CRM/tests/test_landing_page.py` -> no matches.
- Sprint 5 bootstrap: created `sprint5-cat3`, initialized GSD at repo root, wrote `.planning/config.json`, `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, and the 7-file brownfield codebase map under `.planning/codebase/`, then committed the bootstrap as `docs: bootstrap sprint 5 planning`.
- Sprint 5 Phase 1 runtime fixes: discovery-to-match handoff now merges in-session discovered events into Matches, offline/demo runs can render Matches with fallback scoring when embeddings are unavailable, and feedback/generated output paths are repo-stable plus ignored correctly.
- Sprint 5 Phase 1 verification:
  - `Category 3 - IA West Smart Match CRM/.venv/bin/python -m pytest tests/test_acceptance.py tests/test_discovery_tab.py tests/test_matches_tab.py tests/test_app.py -q` -> `37 passed in 21.78s`
  - `git check-ignore -v -- Category 3 - IA West Smart Match CRM/data/feedback_log.csv Category 3 - IA West Smart Match CRM/cache/cache_manifest.json Category 3 - IA West Smart Match CRM/cache/extractions/generated.json` -> all ignored by `Category 3 - IA West Smart Match CRM/.gitignore`
  - `git check-ignore -v -n -- Category 3 - IA West Smart Match CRM/cache/demo_fixtures/pipeline_funnel.json` -> non-match, confirming the demo fixture path remains trackable
- Sprint 5 Phase 2 documentation/governance reconciliation: Category 3 readme surfaces, `.status.md`, and `.planning/` state now point to the live Sprint 5 baseline instead of stale Sprint 3 closeout counts, and governance artifacts were regenerated under dated Sprint 5 report names.
- Sprint 5 Phase 2 verification:
  - `timeout 300s ./.venv/bin/python -m pytest -q` -> `385 passed in 37.40s`
  - `timeout 180s ./.venv/bin/python scripts/sprint4_preflight.py` -> passes with warnings only for missing embedding artifacts plus empty or absent scrape, extraction, explanation, and email caches
  - `python3 .agents/skills/repo-governance/scripts/inventory.py --scope category:3` -> `Managed docs: 22`, `Selected docs: 6`, `Unmanaged governed docs: none`
  - `python3 .agents/skills/repo-governance/scripts/audit.py --scope category:3 --date 2026-03-20 --report docs/governance/reports/2026-03-20-category-3-sprint5-audit.md` -> `Safe reconciliations: 0`, `Needs human decision: 0`
  - `python3 .agents/skills/repo-governance/scripts/reconcile.py --scope category:3 --date 2026-03-20 --report docs/governance/reports/2026-03-20-category-3-sprint5-governance.md --index-output docs/governance/REPO_REFERENCE.md` -> `Safe issues before reconcile: 0`, `Safe issues after reconcile: 0`, `Needs human decision after reconcile: 0`
  - `python3 .agents/skills/repo-governance/scripts/build_index.py --output docs/governance/REPO_REFERENCE.md` -> `docs/governance/REPO_REFERENCE.md`
- Sprint 5 Phase 3 adversarial audit and closeout: checked in `Category 3 - IA West Smart Match CRM/docs/reviews/2026-03-21-sprint5-code-review.md`, normalized discovered events around stable `event_id` plus dedupe semantics, added fallback topic scoring for discovered events without cached embeddings, corrected discovered-event region handling, and routed merged events into Volunteer Dashboard accounting.
- Sprint 5 Phase 3 verification:
  - `Category 3 - IA West Smart Match CRM/.venv/bin/python -m pytest tests/test_discovery_tab.py tests/test_matches_tab.py tests/test_engine.py tests/test_app.py tests/test_acceptance.py tests/test_volunteer_dashboard.py -q` -> `87 passed in 6.56s`
  - `timeout 300s ./.venv/bin/python -m pytest -q` -> `392 passed in 11.93s`
  - `timeout 180s ./.venv/bin/python scripts/sprint4_preflight.py` -> passes with the same expected cache warnings for missing live-warmed embedding, scrape, extraction, explanation, and email artifacts
- Category 3 output/path hygiene: feedback CSV persistence now defaults to `src.config.DATA_DIR / "feedback_log.csv"` instead of a CWD-relative string, generated feedback/cache JSON outputs are ignored in the Category 3 subproject, and checked-in `cache/demo_fixtures/*.json` remain trackable.
- Codebase map review: `arch` mapping completed on 2026-03-20. Wrote `.planning/codebase/ARCHITECTURE.md` (177 lines) and `.planning/codebase/STRUCTURE.md` (181 lines) after inspecting the Category 3 runtime, root governance docs, and sprint task board. Verification: `wc -l .planning/codebase/ARCHITECTURE.md .planning/codebase/STRUCTURE.md` -> `177`, `181`.
- Status: Sprint 4 CLOSED for engineering scope (code + committed artifacts)
- Notes: Created `sprint4-cat3`, hardened discovery for stale-cache fallback and cache-first status visibility, made cache paths repo-stable for root/subdir execution, blocked all-zero match-weight runs, added file-specific empty-dataset errors, aligned the demo funnel fixture to the 6-stage runtime contract, added `runtime.txt`, and committed Sprint 4 testing/rehearsal templates plus `scripts/sprint4_preflight.py`.
- Review fix pass: `scripts/sprint4_preflight.py --prewarm-discovery` now persists extraction caches, `runtime.txt` and preflight now match the Sprint 4 Streamlit Cloud contract, scrape/extraction cache loaders degrade safely on corrupt payloads, and regression coverage was added for those cases.
- Verification:
  - `Category 3 - IA West Smart Match CRM/.venv/bin/python -m pytest tests/test_acceptance.py -q` -> 16 passed in 20.37s
  - `git check-ignore -v -- Category 3 - IA West Smart Match CRM/data/feedback_log.csv Category 3 - IA West Smart Match CRM/cache/cache_manifest.json Category 3 - IA West Smart Match CRM/cache/extractions/generated.json` -> all ignored by `Category 3 - IA West Smart Match CRM/.gitignore`
  - `git check-ignore -v -n -- Category 3 - IA West Smart Match CRM/cache/demo_fixtures/pipeline_funnel.json` -> non-match, confirming the demo fixture path stays trackable
  - `git checkout -b sprint4-cat3` -> branch created from `sprint3-cat3`
  - `./.venv/bin/python -m pytest tests/test_scraper.py tests/test_llm_extractor.py tests/test_matches_tab.py tests/test_app.py -q` -> 47 passed
  - `./.venv/bin/python -m pytest tests/test_demo_mode.py tests/test_pipeline_tab.py -q` -> 47 passed
  - `./.venv/bin/python -m pytest -q` -> 373 passed
  - `./.venv/bin/python scripts/sprint4_preflight.py` -> passes with warnings only for missing live-warmed caches (`cache/scrapes`, embedding cache, `cache/explanations`, `cache/emails`)
  - `Category 3 - IA West Smart Match CRM/.venv/bin/python -m pytest 'Category 3 - IA West Smart Match CRM/tests/test_demo_mode.py' -q` from repo root -> 27 passed
  - `./.venv/bin/python -m pytest tests/test_scraper.py tests/test_llm_extractor.py tests/test_sprint4_preflight.py -q` -> 45 passed
  - `./.venv/bin/python -m pytest tests/test_app.py tests/test_scraper.py tests/test_llm_extractor.py tests/test_matches_tab.py tests/test_pipeline_tab.py tests/test_discovery_tab.py tests/test_sprint4_preflight.py -q` -> 81 passed
- Follow-ups:
  - Run `./.venv/bin/python scripts/sprint4_preflight.py --prewarm-discovery` on the actual demo machine with `GEMINI_API_KEY` configured to warm live scrape and extraction caches.
  - Generate real embedding, explanation, and email caches on the demo machine before rehearsal and day-of use.
  - Complete the human-only Sprint 4 items in `docs/testing/rehearsal_log.md`, `docs/testing/test_log.md`, and `docs/testing/bug_log.md`.
  - Manual gaps still remaining: true copy-to-clipboard confirmation in the email UI, full browser-level E2E rehearsal automation, Streamlit Cloud deployment verification, and backup video recording.

## Sprint 4 Closure

- Closed on branch `sprint4-cat3` after Sprint 4 hardening implementation plus review-fix pass.
- Closure scope: repository code, tests, deployment/runtime wiring, and Sprint 4 operational scaffolding templates.
- Remaining items are explicitly manual/demo-operations tasks and are tracked in `Category 3 - IA West Smart Match CRM/docs/testing/`.
