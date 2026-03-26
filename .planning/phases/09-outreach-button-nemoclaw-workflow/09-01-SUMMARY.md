---
phase: 09-outreach-button-nemoclaw-workflow
plan: "01"
subsystem: backend
tags: [fastapi, pipeline, outreach, csv, lru-cache, tdd]
dependency_graph:
  requires: []
  provides: [pipeline_updater, outreach_workflow_endpoint]
  affects: [src/api/routers/outreach.py, src/ui/data_helpers.py]
tech_stack:
  added: []
  patterns: [tdd, immutable-row-update, per-step-error-handling, lru-cache-invalidation]
key_files:
  created:
    - "Category 3 - IA West Smart Match CRM/src/outreach/pipeline_updater.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_pipeline_updater.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_api_outreach_workflow.py"
  modified:
    - "Category 3 - IA West Smart Match CRM/src/api/routers/outreach.py"
decisions:
  - "Immutable row update pattern (dict copy) in pipeline_updater to avoid mutation"
  - "Per-step try/except in /workflow endpoint for partial failure tolerance"
  - "LRU cache cleared immediately after CSV write to ensure GET /api/data/pipeline freshness"
  - "update_pipeline_status returns bool (True=updated, False=appended) for caller awareness"
metrics:
  duration: "252 seconds (~4 minutes)"
  completed_date: "2026-03-26"
  tasks_completed: 2
  files_changed: 4
---

# Phase 9 Plan 01: Backend Workflow Endpoint + Pipeline Updater Summary

One-liner: JWT-free CSV pipeline updater with LRU cache invalidation + orchestrating `/workflow` endpoint returning email, ICS, and stage update in one serial call with per-step error reporting.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Create pipeline_updater.py with CSV write + cache invalidation | 3833437 | src/outreach/pipeline_updater.py, tests/test_pipeline_updater.py |
| 2 | Add /workflow endpoint to outreach router + integration tests | 794d3bd | src/api/routers/outreach.py, tests/test_api_outreach_workflow.py |

## What Was Built

### pipeline_updater.py

New module at `src/outreach/pipeline_updater.py` providing:
- `PIPELINE_STAGES` dict mapping stage names to integer sort order
- `PIPELINE_CSV` path constant resolved at module load via `_data_dir()`
- `update_pipeline_status(event_name, speaker_name, new_stage) -> bool`: reads cached rows, applies immutable update (new dict copy per row), writes back, clears `_load_pipeline_data_cached` LRU cache, returns True if row existed or False if new row was appended
- `_write_pipeline_csv(rows)`: DictWriter overwrite helper with `extrasaction="ignore"`

### /api/outreach/workflow endpoint

Added to `src/api/routers/outreach.py`:
- `WorkflowRequest` Pydantic model (speaker_name, event_name)
- `StepResult` Pydantic model (status: Literal["ok","error"], error: str|None)
- `POST /workflow` handler: finds ranked match (404 propagates), then wraps email, ICS, and pipeline steps each in independent try/except blocks so partial failures return completed steps alongside error details
- Response shape: `{email, email_data, ics_content, pipeline_updated, steps, dispatch_mode: "serial"}`

## Verification Results

```
8 new tests passing:
  tests/test_pipeline_updater.py: 4 passed
  tests/test_api_outreach_workflow.py: 4 passed

Existing tests unaffected:
  tests/test_api_data.py: 6 passed
  tests/test_api_matching.py: 4 passed
  tests/test_outreach_bridge.py: 14 passed
  Total: 28 passed
```

## Success Criteria Verification

- [x] POST /api/outreach/workflow returns 200 with email, ics_content, pipeline_updated, steps, dispatch_mode fields
- [x] Pipeline CSV stage transitions from "Matched" to "Contacted" and LRU cache is invalidated
- [x] Partial failure returns completed steps alongside errored steps (test_workflow_partial_failure)
- [x] 8 new tests passing (4 unit + 4 integration)
- [x] All existing tests remain green

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None — all data flows are wired to real CSV and real API calls (email mocked only in tests).

## Self-Check: PASSED
