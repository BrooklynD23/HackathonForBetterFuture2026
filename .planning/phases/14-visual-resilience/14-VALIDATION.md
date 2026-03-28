---
phase: 14
slug: visual-resilience
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-27
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (backend) + grep/file checks (frontend) |
| **Config file** | None — no pytest.ini; direct function call tests per STATE.md constraint |
| **Quick run command** | `python -m pytest src/api/tests/test_demo_fallback.py -v` (backend); `grep -rn "isMockData\|Demo Mode" "Category 3 - IA West Smart Match CRM/frontend/src"` (frontend) |
| **Full suite command** | `python -m pytest src/api/tests/ -v --ignore=tests/` |
| **Estimated runtime** | ~15 seconds (backend tests) + ~5 seconds (grep checks) |

---

## Sampling Rate

- **After every task commit:** Run the backend pytest and frontend grep
- **After every plan wave:** Verify demo.db exists + check `source: "demo"` in API responses via curl
- **Before `/gsd:verify-work`:** Full visual walkthrough — disconnect backend, confirm Demo Mode badges appear on all pages; reconnect, confirm badges disappear

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 14-backend-demo-db | 01 | 1 | POLISH-04 | Unit | `python -m pytest src/api/tests/test_demo_fallback.py -v` | Pending | ⬜ pending |
| 14-fastapi-source-field | 01 | 1 | POLISH-04 | Smoke | `curl localhost:8000/api/data/specialists \| python3 -c "import sys,json; d=json.load(sys.stdin); assert all('source' in r for r in d)"` | N/A | ⬜ pending |
| 14-react-mock-store | 02 | 2 | POLISH-04 | Static | `test -f "Category 3 - IA West Smart Match CRM/frontend/src/lib/mockData.ts" && grep -q "MOCK_PIPELINE\|MOCK_SPECIALISTS" frontend/src/lib/mockData.ts` | Pending | ⬜ pending |
| 14-demo-badge | 02 | 2 | POLISH-05 | Static | `grep -rn "Demo Mode" "Category 3 - IA West Smart Match CRM/frontend/src/app/pages/" --include="*.tsx" \| wc -l` → expect ≥4 | N/A | ⬜ pending |
| 14-pages-fallback | 02 | 2 | POLISH-04 | Static | `grep -rn "isMockData" "Category 3 - IA West Smart Match CRM/frontend/src/app/pages/" --include="*.tsx" \| wc -l` → expect ≥4 | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

No Wave 0 test file creation needed — validation uses direct function calls and grep checks that require no additional infrastructure.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Demo Mode badge appears when backend is down | POLISH-05 | Requires stopping FastAPI server | Stop uvicorn, reload each page, confirm "Demo Mode" badge visible on Dashboard, AIMatching, Pipeline, Volunteers |
| Demo Mode badge absent when real data loads | POLISH-05 | Requires running FastAPI server with real data | Start uvicorn with `data/` CSVs present, reload pages, confirm no "Demo Mode" badge |
| Charts display coherent data in demo mode | POLISH-04 | Visual coherence check | With backend down, open Dashboard — funnel, bar, and line charts should show plausible numbers, not empty axes |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: pytest + grep checks cover POLISH-04/05 continuously
- [ ] Wave 0: not applicable
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
