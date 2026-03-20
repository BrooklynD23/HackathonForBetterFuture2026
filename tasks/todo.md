# Todo

## Current Work

### Sprint 3 Audit Plan

#### Requirements Restatement

- Audit the Sprint 3 orchestration branch against actual runtime behavior, not just unit-test intent.
- Repair the three confirmed feature-integration failures:
  - Real pipeline data path is unreachable from the shipped app.
  - Volunteer dashboard never receives populated match results.
  - Demo Mode toggle is present but not wired into production call sites.
- Tighten verification so future tests catch app-level integration breaks instead of only helper-level behavior.

#### Risks

- High: The branch advertises features that do not execute in the running app, creating demo and stakeholder trust risk.
- High: Fixes cross shared runtime seams (`app.py`, matches flow, pipeline flow, demo dispatch), so partial edits can introduce new state-contract bugs.
- Medium: Existing tests mock around the real app contract and currently miss these failures.
- Medium: Local verification depends on the project virtualenv or missing packages being available.

#### Remediation Phases

- [x] Phase 1: Reconcile the runtime data contract.
  - Define one canonical source for match results, feedback log, scraped events, and email counts.
  - Decide whether these live on `LoadedDatasets`, `st.session_state`, or a dedicated runtime state helper.
  - Remove dead assumptions that `load_all()` returns fields it does not provide today.

- [x] Phase 2: Fix the real pipeline integration.
  - Wire `render_pipeline_tab()` to the actual runtime source used by the app.
  - Preserve the richer hover/detail payload from real funnel data instead of degrading back to `"No data"`.
  - Add an app-level test that proves the real-data branch is reachable from the concrete app contract.

- [x] Phase 3: Fix the volunteer dashboard integration.
  - Persist match results from both event-based and course-based match flows into a shared runtime location.
  - Ensure the dashboard reads the same canonical structure and renders non-empty results after running matches.
  - Add regression tests covering the state handoff from Matches to Volunteers.

- [x] Phase 4: Fix Demo Mode wiring.
  - Replace the current checkbox-only behavior with actual fixture dispatch at production call sites.
  - Use `demo_or_live()` only where the live behavior and fixture shape are contract-compatible.
  - Add integration tests proving the toggle changes app behavior, not just helper return values.

- [x] Phase 5: Verification and audit closeout.
  - Run targeted tests for app, pipeline, matches, demo mode, and volunteer dashboard paths.
  - Run the relevant full regression suite in the project environment.
  - Record final verification evidence and any residual gaps in the review section below.

#### Success Criteria

- The Pipeline tab can render real runtime data from the app’s actual state contract.
- The Volunteer tab shows real matches after running the matching workflow.
- Demo Mode materially swaps live behavior for fixtures in the shipped app.
- New tests fail on the pre-fix branch and pass after the remediation.

#### Execution Guidance For Worker

- Start with the runtime contract, not isolated helper fixes.
- Prefer one clean state handoff mechanism over duplicating data across dataset objects and session state.
- Preserve existing user-facing behavior unless it is directly part of the broken integration.
- Add tests that exercise the concrete app wiring paths which were previously missed.

## Review

- Status: Complete
- Notes: Added a dedicated runtime-state helper so shared dynamic data now lives in `st.session_state` instead of being assumed on `LoadedDatasets`. Matches now persists normalized match results, Discovery populates `scraped_events`, Pipeline reads runtime state and preserves real hover text, Volunteer Dashboard tolerates the normalized schema, and Demo Mode now affects discovery, match explanations, email preview, pipeline rendering, and empty feedback summary rendering.
- Verification:
  - `./.venv/bin/python -m pytest tests/test_matches_tab.py tests/test_email_panel.py tests/test_discovery_tab.py tests/test_pipeline_tab.py tests/test_volunteer_dashboard.py -q` -> 44 passed
  - `./.venv/bin/python -m pytest -q` -> 366 passed
- Follow-ups:
  - The runtime match-results contract currently reflects the most recent matching run, not an accumulated history across all events. That is sufficient for the repaired Sprint 3 flows but worth revisiting if the pipeline or volunteer views need multi-event session analytics later.
