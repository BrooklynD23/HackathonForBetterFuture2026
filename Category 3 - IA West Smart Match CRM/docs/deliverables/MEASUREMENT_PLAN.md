# Measurement Plan: IA West SmartMatch CRM

## 1. KPI Dashboard

SmartMatch tracks six operational KPIs that mirror standard market-research quality metrics. Each KPI has a defined numeric target, an automated or semi-automated data source, and a reporting cadence aligned with IA West's event calendar.

| KPI | Target | Source | Frequency | MR Parallel |
|-----|--------|--------|-----------|-------------|
| Match Acceptance Rate | >= 60% | `feedback_log.csv` via `acceptance.py` | Per event cycle | Incidence rate |
| Outreach Response Rate | >= 25% | Email tracking (future); simulated for demo | Per campaign | Response rate |
| Event Attendance Rate | >= 70% of confirmed | Pipeline stage 5 / stage 4 | Quarterly | Completion rate |
| Membership Inquiry Rate | 10-15% of attendees | Pipeline stage 6 / stage 5 | Annually | Conversion rate |
| Volunteer Utilization | >= 3 events/speaker/year | Match assignments per speaker | Quarterly | Panel utilization |
| Time-to-Match | < 60 seconds | System timer | Per match | Field time |

These KPIs cover the full volunteer engagement funnel -- from initial match generation through membership conversion -- across all 18 board volunteers, 15 CPP events, and 9 IA calendar events.

**Calculation Formulas**

- **Match Acceptance Rate** = `accepted_count / total_decisions x 100`. The primary signal of algorithm quality. With 18 volunteers and approximately 3 match suggestions per event, each cycle generates 45-50 measurable decisions -- a sufficient sample frame for trend detection.
- **Funnel Drop-off** = `1 - (stage_N / stage_N-1)`. Applied across the 6 pipeline stages. Current simulated baselines: 80% contact rate, 45% confirmation rate, 75% attendance rate, 15% inquiry rate. Each drop-off point identifies where chapter outreach can be improved.
- **Volunteer Load Balance** = `std_dev(events_per_speaker) / mean(events_per_speaker)`. A coefficient of variation targeting < 0.30. Ensures equitable distribution of speaking opportunities across the 10 metro designations and 7 consolidated regions.
- **Guest Lecture Penetration** = `booked_lectures / high_fit_courses (10) x 100`. Of the 35 courses in the CPP program, 10 are classified as high-fit for IA West guest lectures. This metric tracks market penetration within that addressable universe.

---

## 2. Validation Experiment

**Hypothesis.** Increasing the `topic_relevance` weight from 0.25 to 0.35 -- redistributing 0.10 from `geographic_proximity` -- will increase match acceptance rate by >= 10 percentage points. The rationale: preliminary decline-reason data suggests "topic mismatch" is cited more frequently than "too far," indicating the current weighting under-indexes on subject-matter alignment.

**Design.** Two-cell A/B test. Cell A (control) uses the current prototype defaults: `topic_relevance = 0.25` as defined in `src/config.py` `FACTOR_REGISTRY`. Cell B (treatment) boosts `topic_relevance` to 0.35, with `geographic_proximity` reduced by 0.10 to maintain a weight sum of 1.0. Volunteers are randomly assigned to cells, stratified by metro designation to control for geographic confounds.

**Sample Size.** Minimum 30 match decisions per cell. With approximately 3 match suggestions per event and 15 CPP events per cycle, a single quarter provides 45 decisions -- sufficient for a two-proportion z-test at 80% power (alpha = 0.05, assuming a baseline acceptance rate of 55%).

**Primary Metric.** Match acceptance rate per cell.

**Secondary Metrics.** Decline reason distribution (shift in "topic mismatch" vs. "too far" citations); average match score of accepted matches; volunteer load balance by cell.

**Duration.** One IA West event cycle, approximately one quarter.

**Feasibility.** The weight configuration sliders are already built into the prototype. The feedback module in `src/feedback/acceptance.py` captures accept/decline decisions with structured decline reasons. The `REASON_TO_FACTOR` dictionary maps each decline reason to the corresponding scoring factor, enabling automated analysis. This experiment is immediately executable with no additional development.

---

## 3. Feedback Loop

SmartMatch implements a closed-loop architecture where every volunteer decision feeds back into algorithm calibration. The circuit operates in six steps:

**[1] Match Generated** -- The 8-factor weighted algorithm scores all eligible volunteer-event pairs across the 77-record dataset and surfaces top candidates.
**[2] Volunteer Accepts or Declines** -- If declining, the volunteer selects a structured reason (e.g., "Topic not relevant," "Too far," "Schedule conflict"). This is not free-text; reasons map directly to scoring factors.
**[3] Feedback Aggregated** -- `aggregate_feedback()` compiles acceptance rates and decline reason frequencies per factor, per region, and per time period.
**[4] Weight Suggestions Generated** -- `generate_weight_suggestions()` applies a threshold rule: 3 or more declines citing a specific factor triggers a recommendation to adjust that factor's weight by +0.05. Example: three "Too far" declines produce a suggestion to increase `geographic_proximity` by +0.05.
**[5] Chapter Leadership Reviews** -- Suggestions are presented to IA West leadership as recommendations, not automatic changes. Human judgment governs whether to adopt, modify, or reject each suggestion.
**[6] Updated Weights Applied** -- Approved adjustments are applied to the next matching cycle, and the loop returns to step 3 for continued monitoring.

Steps 1 through 4 are fully implemented in the working prototype. This is production-ready code, not a theoretical framework. The `REASON_TO_FACTOR` dictionary in `acceptance.py` is the mechanism that closes the signal path from qualitative volunteer feedback to quantitative weight adjustment.

---

## 4. Reporting Cadence

**After Each Event.** Match acceptance rate, decline reason breakdown, and weight adjustment suggestions. Delivered to the event coordinator within 48 hours. Enables immediate course correction for the next event.

**Quarterly.** Funnel conversion rates across all 6 pipeline stages, volunteer utilization metrics (events per speaker, load balance coefficient), geographic coverage across the 7 consolidated regions, and A/B test interim results if an experiment is active.

**Annually.** Membership pipeline ROI (inquiry-to-member conversion traced back to SmartMatch-facilitated introductions), year-over-year growth in match acceptance and attendance rates, completed A/B test results with statistical significance assessment, and guest lecture penetration across the 10 high-fit courses.
