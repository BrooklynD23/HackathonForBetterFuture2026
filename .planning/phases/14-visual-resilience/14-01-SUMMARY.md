---
plan: 14-01
phase: 14-visual-resilience
status: complete
completed: 2026-03-27
---

# Plan 14-01 Summary: Backend demo.db, helper module, and router fallback wiring

## What Was Built

Implemented the complete backend demo-data layer (Layer 2) for Visual Resilience:

1. **`data/demo.db`** — SQLite3 seed database with 8 tables, cross-feature coherent data:
   - `specialists` (10 rows): Dr. Sarah Chen, Marcus Webb, Priya Nair, James Rodriguez, Dr. Emily Park, Kevin O'Brien, Aisha Johnson, Dr. Michael Torres, Lisa Chang, Robert Kim
   - `pipeline` (40 rows): funnel-distributed across 5 stages (Matched, Contacted, Confirmed, Attended, Member Inquiry)
   - `calendar_events` (5 rows): AI Hackathon, ITC Conference, Bronco Startup Challenge, IA West Annual Summit, Tech Career Fair
   - `calendar_assignments` (3 rows): specialist-to-event assignments
   - `cpp_events` (5 rows): CPP event catalog
   - `event_calendar` (5 rows): IA event calendar
   - `qr_stats` (1 JSON payload): 5 QR codes, 42 total scans, 12 conversions
   - `feedback_stats` (1 JSON payload): 8 feedback records, 62.5% accept rate

2. **`scripts/seed_demo_db.py`** — Reproducible seed script (~350 lines). Deletes and recreates demo.db from scratch. Named specialists appear consistently across all tables.

3. **`src/api/demo_db.py`** — 8 helper functions:
   - `load_demo_specialists()`, `load_demo_pipeline()`, `load_demo_cpp_events()`, `load_demo_event_calendar()`
   - `load_demo_calendar_events()`, `load_demo_calendar_assignments()`
   - `load_demo_qr_stats()`, `load_demo_feedback_stats()`
   - Uses stdlib `sqlite3` only (no new dependencies). JSON fields decoded via `_decode_json_fields`.

4. **Updated routers** with `_load_rows_with_fallback` pattern:
   - `data.py`: specialists, events, pipeline, calendar — fallback via `_demo_rows()` helper
   - `calendar.py`: /events, /assignments — fallback with `"source": "demo"` tag
   - `feedback.py`: /stats — fallback via `load_demo_feedback_stats()`
   - `qr.py`: /stats — fallback via `load_demo_qr_stats()`
   - `matching.py` and `outreach.py` — unchanged

5. **`tests/test_demo_db.py`** — 7 unit tests for all 6 helper functions + cross-reference check (pipeline speakers ⊆ specialist names)

## Self-Check: PASSED

- ✓ `data/demo.db` exists (40KB, 8 tables with non-trivial row counts)
- ✓ All 6 chart-feeding GET endpoints fall back to demo.db when production data is empty or errors
- ✓ Every fallback response contains `"source": "demo"` field
- ✓ Demo data is cross-feature coherent (same 10 specialist names across all tables)
- ✓ No new pip dependencies added (stdlib sqlite3 only)
- ✓ `matching.py` and `outreach.py` untouched
- ✓ 34 tests pass (test_demo_db.py + all existing API tests)

## key-files

created:
  - Category 3 - IA West Smart Match CRM/data/demo.db
  - Category 3 - IA West Smart Match CRM/src/api/demo_db.py
  - Category 3 - IA West Smart Match CRM/scripts/seed_demo_db.py
  - Category 3 - IA West Smart Match CRM/tests/test_demo_db.py

modified:
  - Category 3 - IA West Smart Match CRM/src/api/routers/data.py
  - Category 3 - IA West Smart Match CRM/src/api/routers/calendar.py
  - Category 3 - IA West Smart Match CRM/src/api/routers/feedback.py
  - Category 3 - IA West Smart Match CRM/src/api/routers/qr.py
  - Category 3 - IA West Smart Match CRM/tests/test_api_data.py
  - Category 3 - IA West Smart Match CRM/tests/test_api_calendar.py
  - Category 3 - IA West Smart Match CRM/tests/test_api_feedback.py
  - Category 3 - IA West Smart Match CRM/tests/test_api_qr.py
  - Category 3 - IA West Smart Match CRM/.gitattributes
