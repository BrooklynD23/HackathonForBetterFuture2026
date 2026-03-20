# Todo

## Current Work

### Codebase Map: Arch Focus

- [x] Inspect root governance files, relevant configs, and the `Category 3 - IA West Smart Match CRM/` layout.
- [x] Identify module boundaries, runtime/data flow, and architecture entry points with concrete file references.
- [x] Write `.planning/codebase/ARCHITECTURE.md` and `.planning/codebase/STRUCTURE.md`.
- [x] Verify both files exist, record line counts, and update the review notes below.

### Codebase Map: Tech Focus

- [x] Audit Category 3 manifests, configs, and canonical runtime docs for the real stack surface.
- [x] Trace external services, storage paths, and environment boundaries in Category 3 source and scripts.
- [x] Write `.planning/codebase/STACK.md` and `.planning/codebase/INTEGRATIONS.md`.
- [x] Verify both files exist, record line counts, and update the review note below.

- Review: Wrote `.planning/codebase/STACK.md` (94 lines) and `.planning/codebase/INTEGRATIONS.md` (137 lines) after verifying Category 3 manifests, Streamlit deployment files, Gemini/runtime config, discovery/scraping modules, cache layout, and root governance/task docs that affect closeout execution.

### Sprint 5 GSD Closeout Orchestration

#### Requirements Restatement

- [ ] Initialize GSD for this brownfield repo because `.planning/` does not exist yet.
- [ ] Work on the new git branch `sprint5-cat3`.
- [ ] Treat Sprint 5 as a closeout milestone for Category 3 unless a stronger local authority emerges:
  - The repo has no canonical Sprint 5 spec.
  - `Category 3 - IA West Smart Match CRM/docs/README.md` says the remaining work is documentation/governance refresh plus sprint closeout.
- [ ] Use parallel subagents wherever they materially reduce context pressure or shorten independent discovery/review work.
- [ ] Create a phase-based plan that ends with an `$ecc-code-review` audit, fixes, documentation updates, per-phase commits, and sprint closure.
- [ ] Verify each phase with direct evidence before marking it complete.

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

- [ ] Phase 3: Execute Sprint 5 closeout phases.
  - Run the planned closeout phases with parallel subagents where appropriate.
  - Keep commits scoped per phase.
  - Update progress in this file as work lands.

- [ ] Phase 4: Run adversarial review and remediation.
  - Create an `$ecc-code-review` agent after implementation changes are in.
  - Apply the review fixes without expanding scope.
  - Re-verify touched behavior.

- [ ] Phase 5: Documentation and sprint closure.
  - Refresh docs/governance artifacts affected by the closeout work.
  - Update this review section with evidence and residual risks.
  - Close out Sprint 5 on the branch.

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

- Codebase map review: `arch` mapping completed on 2026-03-20. Wrote `.planning/codebase/ARCHITECTURE.md` (177 lines) and `.planning/codebase/STRUCTURE.md` (181 lines) after inspecting the Category 3 runtime, root governance docs, and sprint task board. Verification: `wc -l .planning/codebase/ARCHITECTURE.md .planning/codebase/STRUCTURE.md` -> `177`, `181`.
- Status: Sprint 4 CLOSED for engineering scope (code + committed artifacts)
- Notes: Created `sprint4-cat3`, hardened discovery for stale-cache fallback and cache-first status visibility, made cache paths repo-stable for root/subdir execution, blocked all-zero match-weight runs, added file-specific empty-dataset errors, aligned the demo funnel fixture to the 6-stage runtime contract, added `runtime.txt`, and committed Sprint 4 testing/rehearsal templates plus `scripts/sprint4_preflight.py`.
- Review fix pass: `scripts/sprint4_preflight.py --prewarm-discovery` now persists extraction caches, `runtime.txt` and preflight now match the Sprint 4 Streamlit Cloud contract, scrape/extraction cache loaders degrade safely on corrupt payloads, and regression coverage was added for those cases.
- Verification:
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
