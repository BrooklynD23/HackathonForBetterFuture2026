---
phase: 06-agent-tool-wrappers-and-result-bus
plan: "01"
subsystem: coordinator/tools + coordinator/result_bus
tags: [tools, result-bus, tdd, threading, poc-contacts]
dependency_graph:
  requires:
    - "05-01: ActionProposal state machine"
    - "05-02: Command Center UI shell"
    - "src/scraping/scraper.py: scrape_university(), UNIVERSITY_TARGETS"
    - "src/matching/engine.py: rank_speakers_for_event()"
    - "src/outreach/email_gen.py: generate_outreach_email()"
  provides:
    - "TOOL_REGISTRY: 4 intent → callable mappings for Phase 6 Plan 02 wiring"
    - "result_bus.dispatch() / poll_results() for Command Center polling loop"
    - "poc_contacts.json: 5 seed contacts with overdue detection"
  affects:
    - "06-02: Command Center UI wiring (consumes TOOL_REGISTRY and result_bus)"
tech_stack:
  added:
    - "queue.Queue (stdlib) for per-proposal result channels"
    - "threading.Thread (stdlib) for daemon tool execution"
  patterns:
    - "Thin adapter pattern: tool wrappers delegate to existing service functions unchanged"
    - "TDD: RED → GREEN for all 29 new tests"
    - "No Streamlit imports in tool modules — pure Python for testability"
key_files:
  created:
    - "Category 3 - IA West Smart Match CRM/src/coordinator/tools/__init__.py"
    - "Category 3 - IA West Smart Match CRM/src/coordinator/tools/discovery_tool.py"
    - "Category 3 - IA West Smart Match CRM/src/coordinator/tools/matching_tool.py"
    - "Category 3 - IA West Smart Match CRM/src/coordinator/tools/outreach_tool.py"
    - "Category 3 - IA West Smart Match CRM/src/coordinator/tools/contacts_tool.py"
    - "Category 3 - IA West Smart Match CRM/src/coordinator/result_bus.py"
    - "Category 3 - IA West Smart Match CRM/data/poc_contacts.json"
    - "Category 3 - IA West Smart Match CRM/tests/test_discovery_tool.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_matching_tool.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_outreach_tool.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_contacts_tool.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_result_bus.py"
  modified:
    - "Category 3 - IA West Smart Match CRM/tests/conftest.py"
decisions:
  - "Tool wrappers do not catch exceptions — propagation to result_bus thread is intentional (result_bus posts {status:failed})"
  - "contacts_tool uses Path(__file__).resolve().parents[3] to locate poc_contacts.json without Streamlit session state"
  - "TOOL_REGISTRY is a plain dict (not lazy); all four tools imported at module load time"
  - "conftest.py st.fragment mock is lambda **kw: (lambda f: f) — transparent identity decorator for @st.fragment(run_every=N)"
metrics:
  duration: "~8 minutes"
  completed: "2026-03-24"
  tasks: 2
  files: 13
---

# Phase 06 Plan 01: Tool Wrappers, Result Bus, and POC Seed Data Summary

**One-liner:** Four thin adapter tools wrapping existing SmartMatch services + thread-based result bus with per-proposal queues and POC contact seed data with overdue detection.

## Tasks Completed

| # | Name | Commit | Files |
|---|------|--------|-------|
| 1 | Tool wrappers, TOOL_REGISTRY, POC seed data, and all tool tests | 8ff8975 | 10 new files |
| 2 | result_bus.py with dispatch/poll and tests, conftest.py update | e4e58ac | 3 files (2 new, 1 modified) |

## What Was Built

### Tool Wrapper Package (`src/coordinator/tools/`)

Four thin adapter modules, each with `TOOL_NAME: str` and `run(params: dict) -> dict`:

- **discovery_tool.py** — calls `scrape_university(url, method)` using `UNIVERSITY_TARGETS` lookup; defaults to first key when university not specified; exceptions propagate.
- **matching_tool.py** — calls `rank_speakers_for_event()` with 5 required params; returns `{"status": "error", ...}` if any required key is missing.
- **outreach_tool.py** — calls `generate_outreach_email()` with 3 required params; same error pattern.
- **contacts_tool.py** — reads `data/poc_contacts.json`; identifies contacts where `follow_up_due < today`; graceful empty on missing/invalid file.
- **`__init__.py`** — exports `TOOL_REGISTRY` dict mapping all 4 intent names to their `run()` callables.

### Result Bus (`src/coordinator/result_bus.py`)

- `dispatch(proposal_id, tool_fn, params)`: creates fresh `queue.Queue(maxsize=1)`, stores it in `st.session_state["result_queues"][proposal_id]`, spawns daemon thread that posts `{"status":"completed","result":...}` or `{"status":"failed","error":...}`.
- `poll_results()`: iterates all queues, drains via `get_nowait()`, returns list of `(proposal_id, payload)` tuples for ready results.

### POC Seed Data (`data/poc_contacts.json`)

5 contacts at CPP-related institutions (Cal Poly Pomona, UCLA Engineering, CSUF Business, SDSU, UC Davis GSM). 3 contacts have `follow_up_due` dates before 2026-03-24 (overdue for demo). Schema: `{name, email, org, role, comm_history: [{date, type, summary}], last_contact, follow_up_due}`.

### conftest.py Update

Added `_mock_st.fragment = lambda **kw: (lambda f: f)` before `sys.modules["streamlit"] = _mock_st`. Makes `@st.fragment(run_every=2)` a transparent identity decorator in tests.

## Test Results

- **New tests added:** 29 (24 tool tests + 5 result_bus tests)
- **All 29 new tests pass**
- **Full suite:** 519 passed, 2 pre-existing failures (e2e requires live server; embeddings requires real Gemini API key — both unrelated to this plan)
- **No Streamlit imports in any tool module** (verified via inspect.getsource in tests)

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None. All tool wrappers delegate to real service functions. contacts_tool reads real seed data. result_bus uses real threading. No placeholder return values.

## Self-Check: PASSED

- `src/coordinator/tools/__init__.py` — FOUND
- `src/coordinator/tools/discovery_tool.py` — FOUND
- `src/coordinator/tools/matching_tool.py` — FOUND
- `src/coordinator/tools/outreach_tool.py` — FOUND
- `src/coordinator/tools/contacts_tool.py` — FOUND
- `src/coordinator/result_bus.py` — FOUND
- `data/poc_contacts.json` — FOUND
- Commit 8ff8975 — FOUND
- Commit e4e58ac — FOUND
