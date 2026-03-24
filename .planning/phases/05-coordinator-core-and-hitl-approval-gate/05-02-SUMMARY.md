---
phase: 05-coordinator-core-and-hitl-approval-gate
plan: "02"
subsystem: ui
tags: [hitl, streamlit, action-cards, intent-parser, tts, proactive-suggestions, command-center]

requires:
  - phase: 05-01
    provides: "ActionProposal state machine, parse_intent(), check_staleness_conditions() from src/coordinator/"

provides:
  - "Command Center tab with live intent parsing replacing echo reply"
  - "Action card UI with approve/reject/edit-params/TTS-on-result flow"
  - "Proactive staleness suggestions injected at tab load with duplicate guard"
  - "Extended runtime_state.py with action_proposals and scraped_events_timestamp session keys"
  - "Updated test_command_center.py with 18 tests covering proposal-based intent flow and card rendering"

affects:
  - "Phase 06 (agent tool wrappers) — action_proposals session dict is the hand-off contract for real dispatch"
  - "Phase 07 (NemoClaw lead agent) — stub_execute() in ActionProposal will be replaced with queue dispatch"

tech-stack:
  added: []
  patterns:
    - "st.container + st.columns + st.expander for action card rendering (no raw HTML)"
    - "UUID-keyed Streamlit button widgets to prevent state collisions across multiple cards"
    - "Proactive suggestion guard: check source==proactive AND status in (proposed,approved) before injecting"
    - "TTS extracted to _speak_text() helper to keep _handle_text_command and approve callback DRY"

key-files:
  created: []
  modified:
    - "Category 3 - IA West Smart Match CRM/src/runtime_state.py"
    - "Category 3 - IA West Smart Match CRM/src/ui/command_center.py"
    - "Category 3 - IA West Smart Match CRM/tests/test_command_center.py"
    - "Category 3 - IA West Smart Match CRM/tests/conftest.py"

key-decisions:
  - "st.button mock returns False by default in conftest so button callbacks never fire spuriously during unit tests"
  - "st.columns mock returns list-of-MagicMocks to support tuple-unpacking (col_a, col_b = st.columns(2))"
  - "st.container and st.expander mocks wrapped as contextmanager to support 'with' usage in action card"
  - "Proactive suggestions are injected at render time via _inject_proactive_suggestions() — not stored in DB or file"

patterns-established:
  - "ActionProposal stored in st.session_state['action_proposals'][uuid] — UUID is the stable identity across reruns"
  - "Conversation history entries use role='proposal' + action_id to point at live ActionProposal objects"
  - "conftest.py context-manager mocks for Streamlit widgets that use 'with' syntax"

requirements-completed:
  - HITL-01
  - HITL-02
  - HITL-03
  - ORCH-04

duration: 7min
completed: "2026-03-24"
---

# Phase 05 Plan 02: Coordinator Core and HITL Approval Gate — Command Center UI Wiring Summary

**Command Center tab fully wired: text/voice commands route through Gemini intent parsing to approve/reject action cards with TTS playback, proactive staleness suggestions inject at load, and all echo stubs removed.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-24T07:20:32Z
- **Completed:** 2026-03-24T07:27:32Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- `_handle_text_command` no longer echoes — calls `parse_intent()`, creates `ActionProposal`, stores in `st.session_state["action_proposals"]`, appends `role="proposal"` history entry
- `_render_action_card()` renders agent name, description, reasoning, status badge, edit-params expander, approve/reject buttons, and speaks result via TTS on approval
- `_inject_proactive_suggestions()` runs at tab load, injects one proactive `discover_events` proposal when `scraped_events` is empty or stale, with a duplicate guard that prevents re-injection on reruns
- `runtime_state.py` extended with two new session keys: `action_proposals` (dict) and `scraped_events_timestamp` (str | None)
- All 51 Phase 5 tests green; 0 new regressions in the 490-test non-E2E suite

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend runtime_state.py and rewrite _handle_text_command** - `a6d0aeb` (feat)
2. **Task 2: Update test_command_center.py for intent parsing and action card behavior** - `5d8f34a` (test)

## Files Created/Modified

- `Category 3 - IA West Smart Match CRM/src/runtime_state.py` — Added `action_proposals` and `scraped_events_timestamp` session state guards
- `Category 3 - IA West Smart Match CRM/src/ui/command_center.py` — Full rewrite of `_handle_text_command`, new `_render_action_card`, `_inject_proactive_suggestions`, `_speak_text`; updated `_render_conversation_history` for proposal role entries
- `Category 3 - IA West Smart Match CRM/tests/test_command_center.py` — Replaced echo-based `TestHandleTextCommand` with parse_intent-mocked tests; added `TestRenderActionCard` and `TestProactiveSuggestion` classes; updated `_reset_history` helper
- `Category 3 - IA West Smart Match CRM/tests/conftest.py` — Fixed `st.columns`, `st.container`, `st.expander` mocks for context-manager and tuple-unpack usage; fixed `st.button` to return `False` by default

## Decisions Made

- `st.button` mock must return `False` to prevent spurious button callback execution during unit tests — truthy MagicMock caused approve/reject to both fire on the same proposed card
- `st.columns(n)` mock returns `[MagicMock() for _ in range(n)]` so callers can unpack `col_a, col_b = st.columns(2)`
- `st.container` and `st.expander` wrapped as `@contextmanager` since `_render_action_card` uses them with `with` syntax

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed st.columns, st.container, and st.expander mocks for context-manager and tuple-unpack usage**
- **Found during:** Task 2 (running test_command_center.py)
- **Issue:** `st.columns(2)` returned a single MagicMock, so `col_approve, col_reject = st.columns(2)` raised `ValueError: not enough values to unpack`. `st.container()` and `st.expander()` had no `__enter__`/`__exit__`, causing `AttributeError` on `with st.container():`. `st.button()` returned a truthy MagicMock causing both Approve and Reject to fire, triggering `ValueError: Cannot reject proposal in state 'completed'`.
- **Fix:** Updated conftest.py to provide proper side-effects for all three mocks. Added `_fake_columns`, `_fake_container`, `_fake_expander` helpers and set `st.button` return_value=False.
- **Files modified:** `Category 3 - IA West Smart Match CRM/tests/conftest.py`
- **Verification:** All 18 command center tests pass with `st.button.called` assertions verified
- **Committed in:** `5d8f34a` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — bug in test infrastructure)
**Impact on plan:** Required fix for test correctness; no production code scope change.

## Issues Encountered

- `soundfile` was not installed in `.venv` — `pip install soundfile -q` resolved it (pre-existing missing dep, not introduced by this plan)

## Known Stubs

- `proposal.stub_execute()` sets `result = "[Stub] {agent} completed successfully."` — this is intentional Phase 5 behavior per plan; Phase 6 will replace with real queue-based agent dispatch

## Next Phase Readiness

- Phase 06 can wire real agent tool execution by replacing `stub_execute()` — the `action_proposals` session dict and `role="proposal"` history entries are already in place
- `scraped_events_timestamp` is initialized but never written yet — Phase 06 discovery agent wrapper must set it when scraping completes
- All 51 Phase 5 unit tests green; E2E tests require running Streamlit server (pre-existing baseline)

---
*Phase: 05-coordinator-core-and-hitl-approval-gate*
*Completed: 2026-03-24*

## Self-Check: PASSED
