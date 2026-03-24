# Phase 3 Implementation Hand-Off
# Session Date: 2026-03-21
# Status: READY TO IMPLEMENT

## NEXT SESSION PROMPT

```
Read ".claude/handoff-phase3.md" in "Category 3 - IA West Smart Match CRM/" and follow it step by step:

1. Add 2 FactorSpec entries to config.py FACTOR_REGISTRY + rebalance weights
2. Implement event_urgency() factor in factors.py
3. Implement coverage_diversity() factor in factors.py
4. Add dispatch entries in engine.py compute_match_score()
5. Update explanations.py (template + few-shot + generate_match_explanation)
6. Update email_gen.py alias_map
7. Create tests/test_factors_extended.py with TDD
8. Update ALL test fixtures (6 files) for 8-factor factor_scores dicts
9. Update demo fixture match_explanations.json
10. Run full test suite: .venv/bin/python -m pytest -v
11. Commit and write handoff for Phase 4
```

---

## PROJECT CONTEXT

- **Project:** Category 3 - IA West Smart Match CRM
- **Branch:** sprint5-cat3
- **Venv:** `.venv/bin/python` (python3.12)
- **Test command:** `.venv/bin/python -m pytest -v`
- **Baseline:** 425 tests collected, 1 pre-existing failure (`test_embeddings.py::test_get_api_key_requires_real_gemini_key` — environment-dependent, IGNORE)
- **Master plan:** `/home/danny/.claude/plans/deep-wiggling-cupcake.md` (Phase 3: lines 238-291)
- **Phase sequence:** Phase 0 (done) -> Phase 1 (done) -> Phase 2 (done) -> **Phase 3 (implement)** -> Phase 4 (next)

## COMPLETED PHASES

| Phase | Commit | Summary |
|-------|--------|---------|
| 0 — Engine Factor Registry | `1443fdb` | FactorSpec registry in config.py, single source of truth for 6 factors |
| 1 — Landing Page | `21d41bc` | Academic Curator design system, view switching, 21 new tests |
| 2 — Geodesic Fallback | `8b95b77` | Haversine geodesic fallback, OC coordinate fix, 12 new tests |

---

## PHASE 3 GOAL

Add `event_urgency` and `coverage_diversity` factors (6-factor -> 8-factor matching). Leverages Phase 0's dynamic FactorSpec registry.

---

## FILE-BY-FILE IMPLEMENTATION GUIDE

### 1. `src/config.py` — FACTOR_REGISTRY (lines 79-96) + DEFAULT_WEIGHTS (line 100)

**ALREADY DONE.** The 8-factor registry with rebalanced weights is already in place (lines 79-96). Verify the following entries exist at the end of `FACTOR_REGISTRY`:
```python
    FactorSpec("event_urgency", "Event Urgency", "Urgency", 0.05,
               "scheduling urgency", "Event Urgency"),
    FactorSpec("coverage_diversity", "Coverage Diversity", "Coverage", 0.05,
               "assignment diversity", "Coverage Balance"),
```

**Weight rebalance already applied:** `topic_relevance` 0.30->0.25, `role_fit` 0.25->0.20. All 8 weights sum to 1.00.

**Derived constants auto-update:** `FACTOR_KEYS`, `DEFAULT_WEIGHTS`, `FACTOR_DISPLAY_LABELS`, etc. are all derived from `FACTOR_REGISTRY` (lines 98-104), so they update automatically.

---

### 2. `src/matching/factors.py` — Add 2 new factor functions

**Insert after line 500 (after `student_interest()`):**

#### `event_urgency` Scoring Table (from plan)

| Condition | Score |
|-----------|-------|
| Specific date, <=14 days away | 1.00 |
| Specific date, 15-30 days | 0.85 |
| Specific date, 31-60 days | 0.70 |
| Specific date, 61-90 days | 0.55 |
| Specific date, >90 days | 0.40 |
| Recurrence "Weekly" | 0.75 |
| Recurrence "Monthly" | 0.65 |
| Recurrence "Quarterly" | 0.55 |
| Recurrence "Annual" / "Annually" | 0.50 |
| Recurrence "One-time" | 0.85 |
| Unknown / missing | 0.50 |

**Signature:**
```python
def event_urgency(
    event_date_or_recurrence: object,
    reference_date: date | None = None,
) -> float:
```

**IMPORTANT:** The primary data source is `Recurrence (typical)` column. "Event Date" is NOT a CSV column — it's a transient runtime key in engine.py:215. Date parsing is secondary.

#### `coverage_diversity` Scoring Table (from plan)

| Assignments | Score |
|-------------|-------|
| 0 | 1.00 |
| 1 | 0.85 |
| 2 | 0.70 |
| 3 | 0.55 |
| 4+ | 0.40 |
| No data | 0.50 |

**Signature:**
```python
def coverage_diversity(
    speaker_name: str,
    current_assignments: dict[str, int] | None = None,
) -> float:
```

**Data source:** `st.session_state["feedback_decisions"]` — but the function is PURE. The caller extracts the assignment count and passes it. The function receives a dict of `{speaker_name: assignment_count}` or None.

**IMPORTANT:** `feedback_decisions` requires `init_feedback_state()` to be called first. The dispatch wrapper in engine.py should handle this gracefully — if `current_assignments` is None, return 0.50.

---

### 3. `src/matching/engine.py` — Add dispatch for 2 new factors

**Current `compute_match_score()` (lines 105-126) builds `factor_scores` dict inline:**
```python
factor_scores: dict[str, float] = {
    "topic_relevance": ...,
    "role_fit": role_fit(speaker_board_role, event_volunteer_roles),
    "geographic_proximity": geographic_proximity(speaker_metro_region, event_region),
    "calendar_fit": calendar_fit(...),
    "historical_conversion": historical_conversion(speaker_name, conversion_overrides),
    "student_interest": ...,
}
```

**Add to this dict:**
```python
    "event_urgency": event_urgency(event_date_or_recurrence),
    "coverage_diversity": coverage_diversity(speaker_name, coverage_assignments),
```

**Required changes:**
1. Add `event_urgency` and `coverage_diversity` to the import block (line 16-23)
2. Add `coverage_assignments: Optional[dict[str, int]] = None` parameter to `compute_match_score()` (line 78)
3. Pass `coverage_assignments` through from `rank_speakers_for_event()` (add parameter, line 189)
4. Pass through from `rank_speakers_for_course()` too (line 306)

---

### 4. `src/matching/explanations.py` — Add new factors to prompt template + few-shot + generation

**4a. EXPLANATION_USER_TEMPLATE (lines 56-61)** — Add 2 new score lines:

Current:
```python
- Historical Conversion: {historical_conversion:.2f}
- Student Interest: {student_interest:.2f}
```

Target (append after student_interest):
```python
- Historical Conversion: {historical_conversion:.2f}
- Student Interest: {student_interest:.2f}
- Event Urgency: {event_urgency:.2f}
- Coverage Diversity: {coverage_diversity:.2f}
```

**4b. FEW_SHOT_EXAMPLES (lines 67-134)** — Add new factor scores to `.format()` calls:

The two `.format()` calls start at line 70 (first example) and line 103 (second example). Add 2 new kwargs after `student_interest` in each:
```python
event_urgency=0.50,        # neutral default for examples
coverage_diversity=0.50,   # neutral default for examples
```

**4c. `generate_match_explanation()` (lines 326-343)** — Add new kwargs to `.format()` call:

Current format call (line 337-343):
```python
topic_relevance=factor_scores.get("topic_relevance", 0.0),
role_fit=factor_scores.get("role_fit", 0.0),
geographic_proximity=factor_scores.get("geographic_proximity", 0.0),
calendar_fit=factor_scores.get("calendar_fit", 0.0),
historical_conversion=factor_scores.get("historical_conversion", 0.0),
student_interest=factor_scores.get("student_interest", 0.0),
```

Add after `student_interest`:
```python
event_urgency=factor_scores.get("event_urgency", 0.0),
coverage_diversity=factor_scores.get("coverage_diversity", 0.0),
```

**4d. `_normalized_factor_scores()` (line 157-163)** — No change needed. It already iterates `FACTOR_LABELS` which derives from `FACTOR_PROMPT_LABELS` which derives from `FACTOR_REGISTRY`. Auto-expands to 8 factors.

---

### 5. `src/outreach/email_gen.py` — Add new factor aliases

**`_match_score_value()` alias_map (lines 50-58)** — Add 2 new entries:

```python
"event_urgency": ("event_urgency",),
"coverage_diversity": ("coverage_diversity",),
```

**EMAIL_USER_PROMPT_TEMPLATE (lines 149-183)** — DECISION: Do NOT add new factors to email prompt. The email template only shows 3 scores (topic, role, geo) as MATCH QUALITY. Adding urgency/coverage to outreach emails would confuse recipients. Leave unchanged.

---

### 6. `tests/test_factors_extended.py` — CREATE NEW FILE

**Template:**
```python
"""Tests for Phase 3 factors: event_urgency and coverage_diversity."""

from datetime import date, timedelta

import pytest

from src.matching.factors import coverage_diversity, event_urgency


class TestEventUrgency:
    """Event urgency scoring based on date proximity and recurrence."""

    def test_specific_date_within_14_days(self) -> None: ...
    def test_specific_date_15_to_30_days(self) -> None: ...
    def test_specific_date_31_to_60_days(self) -> None: ...
    def test_specific_date_61_to_90_days(self) -> None: ...
    def test_specific_date_over_90_days(self) -> None: ...
    def test_recurrence_weekly(self) -> None: ...
    def test_recurrence_monthly(self) -> None: ...
    def test_recurrence_quarterly(self) -> None: ...
    def test_recurrence_annual(self) -> None: ...
    def test_recurrence_one_time(self) -> None: ...
    def test_unknown_recurrence_returns_default(self) -> None: ...
    def test_none_returns_default(self) -> None: ...
    def test_result_in_unit_range(self) -> None: ...


class TestCoverageDiversity:
    """Coverage diversity scoring based on assignment count."""

    def test_zero_assignments_returns_one(self) -> None: ...
    def test_one_assignment(self) -> None: ...
    def test_two_assignments(self) -> None: ...
    def test_three_assignments(self) -> None: ...
    def test_four_plus_assignments(self) -> None: ...
    def test_no_data_returns_default(self) -> None: ...
    def test_none_assignments_returns_default(self) -> None: ...
    def test_unknown_speaker_returns_default(self) -> None: ...
    def test_result_in_unit_range(self) -> None: ...
```

---

### 7. Tests Requiring Mechanical Updates — COMPLETE LIST

#### 7a. Tests that will AUTO-PASS (no changes needed)

These tests use `DEFAULT_WEIGHTS` dynamically or check `> 0` / `<= 1.0`:
- `test_engine.py:180` — `test_default_weights_produce_nonzero_total` (checks `> 0`)
- `test_engine.py:159` — `test_factor_scores_in_unit_range` (iterates result dict)
- `test_engine.py:140` — `test_total_score_equals_sum_of_weighted` (sums values)

#### 7b. Tests with HARDCODED 6-factor weight dicts — MUST UPDATE to 8-factor

| File | Lines | What to Change |
|------|-------|----------------|
| `tests/test_engine.py` | 202-209 | `custom_weights` dict in `test_custom_weights_override_defaults` — add `"event_urgency": 0.0, "coverage_diversity": 0.0` |
| `tests/test_engine.py` | 252-258 | `heavy_weights` dict in `test_weight_normalization` — add 2 new keys |
| `tests/test_engine.py` | 279-286 | `zero_weights` dict in `test_all_zero_weights_give_zero_total` — add 2 new keys |
| `tests/test_engine.py` | 643-650 | `custom_weights` in `test_student_interest_override_recomputes_weighted_scores` — add 2 new keys |

#### 7c. Tests with HARDCODED 6-factor `factor_scores` dicts — MUST ADD 2 new keys

| File | Lines | What to Change |
|------|-------|----------------|
| `tests/test_explanations.py` | 19-26 | `_make_match_result()` — add `"event_urgency": 0.50, "coverage_diversity": 0.50` to `factor_scores` |
| `tests/test_email_gen.py` | 43-53 | `_make_match_scores()` — add 2 new factor_scores entries |
| `tests/test_matches_tab.py` | 120-127 | Hardcoded `factor_scores` dict — add 2 new entries |
| `tests/test_matches_tab.py` | 238-241 | Another `factor_scores` dict — add 2 new entries |
| `tests/test_volunteer_dashboard.py` | 11-36 | `match_results` fixture — add `"event_urgency"` and `"coverage_diversity"` columns to ALL 8 rows |
| `tests/test_acceptance.py` | 42-48 | `scores` dict in `test_feedback_entry_fields_correct` — add 2 new entries |

#### 7d. Landing page tests — dynamic count assertions

| File | Lines | What to Change |
|------|-------|----------------|
| `tests/test_landing_page.py` | 109-111 | `test_donut_uses_default_weights` — assertions use `len(DEFAULT_WEIGHTS)` dynamically, so they auto-pass (6→8). **NO CHANGE NEEDED.** |
| `tests/test_landing_page.py` | 126 | `test_donut_heading_uses_dynamic_factor_count` — checks `f"{len(DEFAULT_WEIGHTS)}-Factor"` dynamically. **NO CHANGE NEEDED.** |

#### 7e. Acceptance test — weight suggestion assertion

| File | Lines | What to Change |
|------|-------|----------------|
| `tests/test_acceptance.py` | 387-388 | `test_generate_weight_suggestions_above_threshold` — asserts `"0.20"` is current weight for `geographic_proximity`. Value is unchanged (0.20). **NO CHANGE NEEDED.** |

---

### 8. Demo Fixtures to Update

**`cache/demo_fixtures/match_explanations.json`** — Add 2 new factor scores:

Current (6 factors):
```json
"factor_scores": {
    "topic_relevance": 0.85,
    "role_fit": 0.90,
    "geographic_proximity": 0.82,
    "calendar_fit": 0.88,
    "historical_conversion": 0.50,
    "student_interest": 0.75
}
```

Target (8 factors):
```json
"factor_scores": {
    "topic_relevance": 0.85,
    "role_fit": 0.90,
    "geographic_proximity": 0.82,
    "calendar_fit": 0.88,
    "historical_conversion": 0.50,
    "student_interest": 0.75,
    "event_urgency": 0.50,
    "coverage_diversity": 0.50
}
```

---

## KEY DESIGN DECISIONS

1. **`event_urgency` vs `calendar_fit`:** These are different. `calendar_fit` measures proximity to IA events in the speaker's region. `event_urgency` measures how soon the event needs a speaker (time pressure).

2. **`coverage_diversity` data source:** Uses `feedback_decisions` from session state, but the factor function is PURE — caller extracts and passes the data. If no data, return 0.50 (neutral).

3. **Radar chart auto-expansion:** If the radar chart reads from `FACTOR_KEYS` (which it should after Phase 0), it will auto-expand to 8 axes. Verify this.

4. **Weight rebalance is minimal:** Only `topic_relevance` (0.30->0.25) and `role_fit` (0.25->0.20) change. The other 4 factors keep their weights. The 0.10 freed up goes to the 2 new factors (0.05 each).

---

## AFTER IMPLEMENTATION

1. Run full test suite: `.venv/bin/python -m pytest -v`
2. Verify 8-factor radar chart renders (if UI is testable)
3. Commit with message:
```
feat: add event_urgency + coverage_diversity factors (Phase 3)

Sprint 5 Phase 3. Expands matching from 6 to 8 factors. Adds
event_urgency (date proximity / recurrence urgency) and
coverage_diversity (speaker assignment balancing). Rebalances
default weights: topic_relevance 0.30->0.25, role_fit 0.25->0.20.

Radar chart auto-expands to 8 axes via FACTOR_REGISTRY.
All existing tests updated for new weight values.
```
4. Write handoff for Phase 4 (QR Code Generation)
