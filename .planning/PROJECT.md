# Hackathon For Better Future 2026 - Category 3 SmartMatch Closeout

## What This Is

This repository contains the IA West SmartMatch CRM hackathon build, with the active product implementation living in `Category 3 - IA West Smart Match CRM/`. The application is a Streamlit-based demo that loads curated IA West data, discovers public university events, ranks speakers against event and course opportunities, and generates outreach artifacts. GSD is being initialized here to drive a Sprint 5 closeout milestone focused on reliability, documentation, governance, and final review rather than net-new product scope.

## Core Value

An operator can run a dependable end-to-end SmartMatch demo flow that surfaces credible matches and outreach artifacts without closeout-time surprises.

## Current Milestone: v1.0 Sprint 5 Closeout

**Goal:** Finish the Category 3 wrap-up work in a controlled, reviewable way on `sprint5-cat3`.

**Target features:**
- Fix any broken runtime flows that block the intended discovery-to-match demo path.
- Reconcile verification evidence and governance/docs state to a single live source of truth.
- Run adversarial review, implement accepted fixes, and close the sprint cleanly.

## Requirements

### Validated

- ✓ Operators can load the four canonical Category 3 CSV datasets and inspect data quality in the Streamlit app - existing
- ✓ Operators can compute six-factor speaker rankings for events and courses, with explainable score breakdowns - existing
- ✓ Operators can scrape approved university pages, cache results, and extract structured event candidates - existing
- ✓ Operators can generate outreach emails, calendar invites, and pipeline or volunteer views from runtime state - existing
- ✓ Operators can use preflight and demo-support tooling to validate local/demo readiness - existing

### Active

- [ ] Sprint 5 closeout resolves any broken discovery-to-matching or demo-path behavior required for the operator flow.
- [ ] Sprint 5 closeout reconciles tests, status docs, and governance mirrors from one live verification baseline.
- [ ] Sprint 5 closeout keeps generated runtime artifacts from polluting source-controlled diffs.
- [ ] Sprint 5 ends with adversarial review, a fix pass, documentation refresh, and explicit closure evidence on `sprint5-cat3`.

### Out of Scope

- Net-new Category 3 product features beyond the existing hackathon MVP - the checked-in docs only justify wrap-up work at this stage
- Large structural refactors of monolithic runtime modules - too risky for a closeout sprint with an already green baseline
- New persistence, authentication, or cloud-infrastructure features - not part of the current product contract or remaining wrap-up scope
- Portfolio-wide replanning outside the Category 3 closeout lane - this milestone is scoped to finishing Category 3 cleanly

## Context

- Category 3 authority lives in `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `PRD_SECTION_CAT3.md`, `archived/general_project_docs/MASTER_SPRINT_PLAN.md`, and `archived/general_project_docs/STRATEGIC_REVIEW.md`.
- Before this initialization, the repo had no `.planning/` state even though `tasks/todo.md` was already tracking Sprint 5 as a GSD-driven closeout.
- The brownfield codebase map in `.planning/codebase/` confirms that the app runtime already exists and the remaining work is closeout-oriented, not greenfield delivery.
- Closeout evidence is currently inconsistent: Category 3 docs mention older pytest totals while the mapped testing baseline reports `378` collected tests.
- The current worktree contains unrelated local changes and untracked files, so all Sprint 5 commits must use explicit pathspecs.

## Constraints

- **Scope**: Sprint 5 is a closeout milestone - avoid inventing new product scope unless the current runtime contract is already broken.
- **Tech stack**: Preserve the existing Python + Streamlit + pandas + Plotly + Gemini runtime centered in `Category 3 - IA West Smart Match CRM/src/`.
- **Verification**: No phase is done without direct evidence from tests, scripts, or document reconciliation.
- **Working tree**: The repo is already dirty outside this milestone - do not revert or accidentally stage unrelated files.
- **Deployment**: Keep the Streamlit Cloud and cache-first demo assumptions documented in the Category 3 docs intact unless intentionally corrected.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Treat Sprint 5 as a closeout milestone derived from local wrap-up signals | No canonical Sprint 5 spec exists, but the repo explicitly says remaining work is documentation/governance refresh plus closeout | - Pending |
| Initialize GSD at the repo root with Category 3 as the active implementation focus | The user asked for repo-level GSD initialization, while the actual runtime work is concentrated in the Category 3 subtree | - Pending |
| Use parallel mapper and review agents, but keep implementation fixes targeted | Parallel subagents reduce context pressure, while closeout changes should still minimize surface area | - Pending |
| Prefer live command output over stale historical pass-count mirrors | Multiple docs disagree on verification totals, so closeout needs one authoritative baseline | - Pending |
| Run `$ecc-code-review` before declaring Sprint 5 closed | The request explicitly requires adversarial audit plus remediation before closure | - Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-20 after GSD initialization*
