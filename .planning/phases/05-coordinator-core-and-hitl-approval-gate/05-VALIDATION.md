---
phase: 05
slug: coordinator-core-and-hitl-approval-gate
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-23
---

# Phase 05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.3.4 |
| **Config file** | `Category 3 - IA West Smart Match CRM/pytest.ini` |
| **Quick run command** | `cd "Category 3 - IA West Smart Match CRM" && python -m pytest tests/ -x -q --timeout=30` |
| **Full suite command** | `cd "Category 3 - IA West Smart Match CRM" && python -m pytest tests/ --timeout=60` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick run command
- **After every plan wave:** Run full suite command
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | HITL-01 | unit | `pytest tests/test_intent_parser.py -x` | ❌ W0 | ⬜ pending |
| 05-01-02 | 01 | 1 | HITL-01 | unit | `pytest tests/test_approval.py -x` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 1 | HITL-02 | unit | `pytest tests/test_command_center.py -x` | ✅ | ⬜ pending |
| 05-02-02 | 02 | 1 | HITL-03 | unit | `pytest tests/test_command_center.py -x` | ✅ | ⬜ pending |
| 05-03-01 | 03 | 2 | ORCH-04 | unit | `pytest tests/test_suggestions.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_intent_parser.py` — stubs for HITL-01 (ParsedIntent, parse_user_command)
- [ ] `tests/test_approval.py` — stubs for HITL-02, HITL-03 (ActionProposal state machine)
- [ ] `tests/test_suggestions.py` — stubs for ORCH-04 (staleness check, proactive suggestion)
- [ ] `tests/conftest.py` — extend with coordinator fixtures (mock Gemini responses)

*Existing pytest infrastructure covers framework needs.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Action card renders with approve/reject buttons | HITL-01 | Streamlit UI rendering | Open Command Center, type command, verify card appears |
| TTS speaks stub result after approval | HITL-02 | Audio playback | Approve action card, verify Jarvis speaks result |
| Proactive suggestion appears on tab load | ORCH-04 | Session state timing | Load Command Center with empty scraped_events |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
