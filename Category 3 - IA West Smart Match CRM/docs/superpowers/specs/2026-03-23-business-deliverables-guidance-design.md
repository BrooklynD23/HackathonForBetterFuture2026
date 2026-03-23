# Business Deliverables Guidance Document — Design Spec

**Date:** 2026-03-23
**Project:** IA SmartMatch CRM (Category 3 — IA West)
**Hackathon:** CPP AI Hackathon "AI for a Better Future" — April 16, 2026
**Purpose:** Design spec for a guidance markdown file that an implementation agent can use to draft all four business deliverables, written in language a non-technical stakeholder familiar with the market research industry can review and understand.

---

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Audience | Hybrid — agent-executable + stakeholder-reviewable | Agent needs prescriptive structure; stakeholder needs readable language |
| Scope | All 4 deliverables: Growth Strategy + Measurement Plan + Responsible AI Note + Demo Script | Demo script ties the prototype to the written submissions |
| Data approach | Pre-calculated headlines + formulas for derived metrics | Consistency on key numbers; flexibility on contextual calculations |
| Tone | Blended MR-native + business-professional | Credibility with IA West judges without alienating non-MR reviewers |
| Growth ambition | Conservative — CPP to 5 universities to West Coast | Fully defensible with existing data and prototype capabilities |
| Structure | "Mission Brief" style — single file, shared preamble, 4 mission sections, narrative thread | Coherence across all deliverables; single source of truth |

---

## Output File

**Path:** `docs/deliverables/BUSINESS_DELIVERABLES_GUIDE.md`
**Estimated length:** ~1000 lines
**Consumers:** Implementation agent (primary), human team reviewers (secondary)

---

## Structure

### Preamble — Project Context & Data Inventory (~150 lines)

Shared foundation referenced by all 4 mission sections.

#### 1a. Project Identity
- Project name, sponsor, hackathon event/date (April 16, 2026)
- One-paragraph elevator pitch of IA SmartMatch
- Challenge prompt verbatim: "How might IA West systematically discover university engagement opportunities — guest lectures, competitions, career programs, and campus events — match them with the right board member volunteers, and convert that engagement into a measurable pipeline to IA membership?"

#### 1b. Judging Criteria Breakdown

| Criterion | Points | What Judges Look For | Addressed By |
|-----------|--------|----------------------|--------------|
| Prototype Quality | ~15 | Live matching engine + automated discovery | Mission 4 (Demo Script) |
| Growth Strategy | ~10 | Realistic rollout from CPP to 3+ universities | Mission 1 |
| Measurement Plan | ~10 | Actionable KPIs + real feedback loop | Mission 2 |
| Responsible AI | ~10 | Concrete privacy, bias, transparency measures | Mission 3 |
| Scalability | ~5 | Volunteer can add university with minimal effort | Missions 1 & 4 |

Emphasis callout: "Written deliverables = 30 of 50 points (60%)"

#### 1c. Pre-Computed Data Stats (Ready to Cite)

All headline numbers pre-calculated from actual CSV data:

| Stat | Value | Source |
|------|-------|--------|
| Board volunteers | 18 across 7 metro regions | data_speaker_profiles.csv |
| Metro regions | Seattle, Portland, SF, LA (4 sub-regions), Ventura, San Diego | data_speaker_profiles.csv |
| CPP events | 15 distinct opportunities | data_cpp_events_contacts.csv |
| CPP courses | 35 sections (10 High / 17 Medium / 8 Low guest lecture fit) | data_cpp_course_schedule.csv |
| High-fit course percentage | 28.6% (10/35) | Derived |
| IA West calendar events | 9 events across 7 regions in 2026 | data_event_calendar.csv |
| Universities mapped to IA events | 20+ across CA, OR, WA | data_event_calendar.csv |
| Discovery universities configured | 5 (UCLA, SDSU, UC Davis, USC, Portland State) | Prototype config |
| Matching factors | 8-factor weighted algorithm | Prototype |
| Pipeline stages | 6 (Discovered, Matched, Contacted, Confirmed, Attended, Member Inquiry) | Prototype |
| Simulated pipeline conversion | 80% contact, 45% confirm, 75% attend, 15% inquiry | src/ui/pipeline_tab.py |
| Total structured records | 77 rows across 4 CSV files | All data files |
| Student PII collected | 0 rows | Design choice |

#### 1d. Calculation Guide for Derived Metrics

Formulas the implementation agent can use for contextual calculations:

```
Total addressable events = CPP events (15) + discovered events per university x number of universities
Volunteer utilization rate = events assigned / events available per speaker
Match acceptance rate = accepted_count / total_decisions x 100
Funnel conversion rate per stage = stage_N count / stage_N-1 count
Funnel drop-off per stage = 1 - (stage_N / stage_N-1)
Guest lecture penetration = booked_lectures / high_fit_courses (10) x 100
Geographic coverage ratio = metros with active matches / total metros (7)
Volunteer load balance (CV) = std_dev(events_per_speaker) / mean(events_per_speaker)
Student reach per course = enrollment cap (avg 30-35 per section)
Total student reach (High-fit) = 10 courses x avg 30 enrollment = ~300 students/term
```

#### 1e. Tone & Language Guide

**MR-native terms (use for IA West concepts):**
- conversion funnel, response rate, sample frame, segmentation, A/B cell, panel, recruitment, incidence rate, field time, completion rate

**Business terms (use for strategy/growth sections):**
- value proposition, rollout, channel strategy, TAM, unit economics, go-to-market

**Terms to avoid:**
- "AI magic," "black box," undefined jargon, vague platitudes ("we care about fairness"), overly technical model descriptions

**Voice:** Confident, data-backed, practitioner-credible. Write as if presenting to the IA West board of directors.

---

### Mission 1 — Growth Strategy (2-3 pages, ~10 pts) (~200 lines)

**Judging Target:** "Realistic, specific rollout from CPP to 3+ universities"

#### Outline

| Section | ~Words | Content |
|---------|--------|---------|
| Executive Summary | 150 | What SmartMatch does, why it matters, the growth thesis |
| The Problem Today | 200 | Quantify coordination gap with real numbers and MR framing |
| Target Audience Segments | 250 | Three segments with value propositions |
| Rollout Plan | 400 | Three phases, data-backed, with success criteria |
| Channel Strategy | 200 | How SmartMatch reaches each segment |

#### Target Audience Segments

**Segment 1: Board Member Volunteers**
- Value prop: "Spend your limited volunteer hours on high-fit events, not email chains."
- Data point: 18 speakers currently coordinated ad-hoc; SmartMatch reduces matching time from days to 60 seconds
- Pain point: volunteers burn out on logistics, not impact

**Segment 2: University Coordinators**
- Value prop: "Get curated, pre-vetted industry professionals delivered to your inbox."
- Data point: 15 CPP events currently have no systematic link to IA West's 18-person speaker pool
- Pain point: career centers scramble to find qualified industry guests

**Segment 3: Students (Indirect Beneficiaries)**
- Value prop: "Better industry speakers at your events = better career connections."
- Data point: 10 High-fit guest lecture courses = ~300 students per term who could interact with IA professionals (10 courses x avg 30 enrollment cap)
- Framing: students are the future talent pipeline for IA membership

#### Rollout Plan

**Phase 1 — CPP Pilot (Q2 2026)**
- Scope: All existing data — 15 events, 35 courses, 18 speakers
- Success criteria: match acceptance rate >60%, 5+ guest lectures booked
- Data anchor: 10 High-fit courses already identified with instructor names and times; 15 events with real contact emails in the CSV
- Risk: Low — all data pre-loaded, prototype fully functional

**Phase 2 — LA Metro Expansion (Q3-Q4 2026)**
- Scope: Add UCLA + USC from pre-configured discovery scraping
- Data anchor: IA event calendar maps June 18 LA event to "UCLA, USC, Cal Poly Pomona, LMU"
- Success criteria: 3+ events discovered per university, 10+ new matches generated
- Enabler: Discovery tab already configured for UCLA and USC URLs

**Phase 3 — West Coast Coverage (2027)**
- Scope: Activate all 5 pre-configured universities + leverage IA event calendar's 9 events across Portland, San Diego, SF, Seattle, Ventura, OC
- Data anchor: Calendar already maps 20+ universities to event windows across all 7 metro regions
- Success criteria: All 7 metro regions generating matches, 50+ events/year in pipeline

#### Channel Strategy

- **Board meetings:** Live SmartMatch demo during quarterly IA West board meetings
- **University outreach:** AI-generated personalized emails sent from IA West coordinators to career center contacts
- **Organic discovery:** Scraper detects new events automatically; SmartMatch alerts the relevant metro director
- **Scalability proof point:** "Adding a new university takes 3 steps: paste URL, AI extracts events, events enter matching pool"

#### Must-Include Checklist

- [ ] At least 3 named universities beyond CPP
- [ ] Specific data points from provided CSVs (not hypothetical numbers)
- [ ] Clear success criteria for each rollout phase
- [ ] Value proposition per audience segment
- [ ] Connection to prototype's actual capabilities (not vaporware)

---

### Mission 2 — Measurement Plan (1 page, ~10 pts) (~200 lines)

**Judging Target:** "Are KPIs actionable? Is there a real feedback loop?"

#### Outline

| Section | ~Words | Content |
|---------|--------|---------|
| KPI Dashboard | 250 | 6 primary KPIs with targets, sources, MR parallels |
| Validation Experiment | 200 | A/B test design using weight-tuning mechanism |
| Feedback Loop | 200 | Closed-loop architecture with diagram |
| Reporting Cadence | 100 | Who sees what, when |

#### KPI Table

| KPI | Target | Source | Frequency | MR Parallel |
|-----|--------|--------|-----------|-------------|
| Match Acceptance Rate | >=60% | feedback_log.csv via acceptance.py | Per event cycle | Incidence rate |
| Outreach Response Rate | >=25% | Email tracking (future); simulated for demo | Per campaign | Response rate |
| Event Attendance Rate | >=70% of confirmed | Pipeline stage 5 / stage 4 | Quarterly | Completion rate |
| Membership Inquiry Rate | 10-15% of attendees | Pipeline stage 6 / stage 5 | Annually | Conversion rate |
| Volunteer Utilization | >=3 events/speaker/year | Match assignments per speaker | Quarterly | Panel utilization |
| Time-to-Match | <60 seconds | System timer | Per match | Field time |

#### Calculation Formulas

```
Match Acceptance Rate = accepted_count / total_decisions x 100
Funnel Drop-off = 1 - (stage_N / stage_N-1)
Volunteer Load Balance = std_dev(events_per_speaker) / mean(events_per_speaker)
Guest Lecture Penetration = booked_lectures / high_fit_courses (10) x 100
```

#### Validation Experiment — A/B Test Design

Format as formal experimental design (MR professionals will respect this):

- **Hypothesis:** Increasing topic_relevance weight from 0.25 to 0.35 (redistributing from geographic_proximity) will increase match acceptance rate by >=10 percentage points
- **Design:** Two-cell A/B test. Cell A = default weights (control). Cell B = boosted topic_relevance (treatment). Randomly assign incoming events to cells.
- **Sample size:** Minimum 30 match decisions per cell (practical: ~10 events x 3 matches each)
- **Primary metric:** Match acceptance rate per cell
- **Secondary metrics:** Decline reason distribution, average match score of accepted matches
- **Duration:** One IA West event cycle (~1 quarter)
- **Feasibility:** Weight sliders already built in prototype. Feedback module already captures accept/decline with structured decline reasons. A/B test is immediately executable.
- **Code reference:** `src/feedback/acceptance.py` — `REASON_TO_FACTOR` dict maps decline reasons to factor names; `generate_weight_suggestions()` closes the feedback signal

#### Feedback Loop Architecture

```
[1] Match Generated (8-factor score)
         |
[2] Volunteer Accepts or Declines
    --> If decline: captures reason (geographic/schedule/topic/committed)
         |
[3] Feedback Aggregated (aggregate_feedback())
    --> Decline reason frequencies tallied
         |
[4] Weight Suggestions Generated (generate_weight_suggestions())
    --> "3+ declines for 'Too far' -> increase geographic_proximity by +0.05"
         |
[5] Chapter Leadership Reviews Suggestions
    --> Adjusts sliders or accepts auto-suggestion
         |
[6] Next Matching Cycle Uses Updated Weights
    --> Acceptance rate measured --> feeds back to [3]
```

Key selling point: Steps 1-4 are already implemented in the prototype. This is working code, not a theoretical loop.

#### Reporting Cadence

- **After each event:** Match acceptance rate, decline reasons, weight suggestions
- **Quarterly:** Funnel conversion rates, volunteer utilization, geographic coverage
- **Annually:** Membership pipeline ROI, year-over-year growth, A/B test results

#### Must-Include Checklist

- [ ] >=5 KPIs with specific numeric targets
- [ ] At least one formal validation experiment with hypothesis, design, and sample size
- [ ] Feedback loop described as closed circuit (not one-way measurement)
- [ ] MR-native language (incidence rate, response rate, sample frame parallels)
- [ ] Reference to actual prototype capabilities (acceptance.py, weight sliders)

---

### Mission 3 — Responsible AI Note (half page, ~10 pts) (~150 lines)

**Judging Target:** "Are privacy, bias, and transparency addressed concretely?"

**Constraint:** Half page = ~400 words max. Every sentence must carry weight.

#### Outline

| Section | ~Words | Content |
|---------|--------|---------|
| Privacy & Data Handling | 100 | What data is collected, what isn't, consent |
| Bias Identification & Mitigation | 150 | Specific biases named with countermeasures |
| Transparency & Explainability | 100 | Three demonstrable mechanisms |
| Data Stewardship | 50 | Storage, retention, access |

#### Privacy & Data Handling — Talking Points

- Speaker profiles: 18 records sourced from publicly listed IA West board information. No private data (no home addresses, personal emails, phone numbers).
- University contacts: Scraped exclusively from publicly published faculty/staff directories and event pages. No login-gated content accessed.
- Student data: Zero individual student data collected. Pipeline metrics track aggregate counts only ("12 attended" not "Jane Doe attended").
- Must-cite stat: "0 rows of student PII in the entire system — all 77 records are organizational data"

#### Bias Identification & Mitigation

Three concrete biases to name with countermeasures:

| Bias | Mechanism | Mitigation Built |
|------|-----------|-----------------|
| Geographic clustering | LA-area speakers (4 of 7 metros are LA sub-regions) have proximity to more universities, inflating geographic_proximity scores | `coverage_diversity` factor (5% weight) penalizes over-assigned speakers; weight sliders let leadership manually reduce geographic_proximity influence |
| Expertise tag density | Speakers with richer/longer expertise tags could generate inflated topic_relevance scores | Cosine similarity normalizes vector magnitude — inherently handled by the math |
| Incumbency advantage | `historical_conversion` factor (5% weight) favors previously placed speakers; new board members disadvantaged | Factor capped at 5% weight; `coverage_diversity` explicitly boosts underutilized speakers; new speakers start with neutral (not zero) baseline |

Framing instruction: "We identified three specific algorithmic biases in our system and built countermeasures for each."

#### Transparency & Explainability — Three Mechanisms

1. **Score breakdown cards** — Every match shows 8 named factors with individual scores, not just a composite number
2. **Natural language explanations** — Gemini-generated cards explain in plain English why a speaker was recommended
3. **Weight sliders** — Chapter leadership adjusts all 8 factor weights in real time, rankings recompute instantly

Must-include quote: "No black-box scores. Every recommendation is decomposable into 8 named factors, explainable in natural language, and adjustable by the end user."

#### Data Stewardship

- CSV-based storage — no cloud database, no third-party data sharing
- Scraping cache local-only, hashed filenames, no PII in cache keys
- Rate-limited scraping (1 req/5 sec), robots.txt respected
- All data stays within the IA West deployment — no data leaves the system

#### Must-Include Checklist

- [ ] >=2 specific biases named with specific countermeasures (not generic)
- [ ] Zero student PII claim with evidence
- [ ] 3 transparency mechanisms cited from working prototype
- [ ] Scraping ethics addressed (robots.txt, rate limits, caching)
- [ ] Under 400 words total

---

### Mission 4 — Demo Script & Presentation Narrative (~200 lines)

**Judging Target:** Prototype Quality (15 pts) — also reinforces Growth Strategy, Measurement Plan, and Responsible AI through demonstration

#### Outline

| Section | ~Words | Content |
|---------|--------|---------|
| Demo Philosophy | 50 | Three guiding principles |
| The "60-Second Moment" | 200 | Beat-by-beat walkthrough |
| Tab Tour Guide | 200 | What to show and say per tab |
| Narrative Bridges | 150 | Lines connecting demo to written deliverables |
| Failure Contingency | 100 | Fallbacks for common failures |

#### Demo Philosophy

1. **Show, don't tell** — Every claim in the written deliverables should be visible in the demo
2. **Name real people and real events** — "Travis Miller matched to UCLA's hackathon" beats "Speaker A matched to Event B"
3. **End on the funnel** — Last thing judges see is the pipeline visualization, connecting demo to Growth Strategy and Measurement Plan

#### The "60-Second Moment" — Beat-by-Beat

| Beat | Time | Action | Say |
|------|------|--------|-----|
| 1 | 0:00-0:10 | Open Discovery tab, paste UCLA events URL | "A new hackathon was just announced at UCLA. Let's see SmartMatch find it." |
| 2 | 0:10-0:20 | System scrapes and extracts events | "Our AI reads the page, extracts structured event data — name, date, roles needed, contact info." |
| 3 | 0:20-0:30 | Click "Add to Matching," switch to Matches tab | "One click and it's in our matching pool. SmartMatch instantly scores all 18 board members." |
| 4 | 0:30-0:40 | Show top-3 matches with radar chart + explanation card | "Travis Miller, 87% match — his data collection expertise and Ventura proximity make him the top candidate. You can see exactly why." |
| 5 | 0:40-0:50 | Generate outreach email + show .ics download | "One click generates a personalized email referencing Travis's background. Calendar invite attached." |
| 6 | 0:50-0:60 | Switch to Pipeline tab, show funnel updating | "And Travis flows into our conversion pipeline — from discovered to matched to contacted. This is the funnel IA West has never had." |

#### Tab Tour Guide

| Tab | Duration | Must Show | Connects To |
|-----|----------|-----------|-------------|
| Landing Page | 30 sec | "How It Works" visual, IA West branding, "Start Matching" CTA | First impression, polish |
| Discovery | 60 sec | Live scrape of one university, extracted event cards, custom URL input | Growth Strategy (scalability), Responsible AI (scraping ethics) |
| Matches | 90 sec | Top-3 matches with radar charts, explanation cards, weight sliders, accept/decline | Measurement Plan (feedback loop), Responsible AI (transparency) |
| Pipeline | 45 sec | Funnel chart with real data, stage counts, conversion percentages | Growth Strategy (funnel), Measurement Plan (KPIs) |
| Volunteer Dashboard | 30 sec | Per-speaker utilization, load balancing view | Measurement Plan (utilization KPI) |
| Expansion Map | 30 sec | Geographic scatter showing speakers vs. universities with connection lines | Growth Strategy (West Coast coverage) |
| Demo Mode | Mention only | Note it exists for offline/reliable presentation | Risk mitigation |

**Course schedule note:** Judges specifically asked for course schedule integration. During the Matches tab tour, highlight the 10 High-fit courses and show how guest lectures are matched to speakers.

#### Narrative Bridges

Scripted transition lines connecting demo to written deliverables:

- **Demo to Growth Strategy:** "What you just saw with UCLA is Phase 2 of our rollout. Phase 1 is already loaded — 15 CPP events, 35 courses, all matched. Phase 3 extends this to all 5 pre-configured West Coast universities."
- **Demo to Measurement Plan:** "That accept/decline button Travis would click feeds directly into our feedback loop. After 30 decisions, the system suggests weight adjustments — like A/B testing your own matching algorithm."
- **Demo to Responsible AI:** "Notice every match shows 8 named factors, not a black-box score. Travis can see exactly why he was recommended, and chapter leadership can override any weight they disagree with."
- **Demo to Scalability:** "Adding UCLA took 3 steps — paste URL, AI extracts events, confirm. Any volunteer metro director can do this for their local universities."

#### Failure Contingency

| Failure | Fallback | Preparation |
|---------|----------|-------------|
| Scraping fails during demo | Switch to Demo Mode — pre-cached results for all 5 universities | Pre-warm cache before presentation |
| Gemini API down | Demo Mode serves cached email text and explanation cards | Verify all demo fixtures populated |
| Streamlit crashes | Recorded backup video of full 60-second moment | Record video in advance, have queued |
| Network down entirely | Local-only mode with all cached data, no live scraping | Test offline mode end-to-end |

#### Must-Include Checklist

- [ ] Beat-by-beat 60-second script with named speakers and events
- [ ] Tab tour order with time allocations
- [ ] >=3 narrative bridge lines connecting demo to written deliverables
- [ ] Failure contingency for >=3 scenarios
- [ ] Demo mode as safety net
- [ ] Course schedule mention in Matches tab tour

---

### Narrative Thread — Connective Tissue (~100 lines)

Ensures all 4 deliverables tell one unified story.

#### The Single Story

"IA West has 18 expert volunteers and thousands of university engagement opportunities across the West Coast — but no system to connect them. SmartMatch uses AI to discover opportunities, match the right volunteer to each one, generate outreach, and track the conversion pipeline from first contact to IA membership. Every match is explainable, every decision feeds back into the algorithm, and every new university is 3 clicks away."

#### Cross-Reference Matrix

Concepts that must appear across multiple deliverables for coherence:

| Concept | Growth Strategy | Measurement Plan | Responsible AI | Demo Script |
|---------|:-:|:-:|:-:|:-:|
| "18 speakers, 7 metros" | Segment sizing | Utilization KPI | Geographic bias context | Name real speakers |
| "15 CPP events + 35 courses" | Phase 1 scope | Guest lecture penetration KPI | — | Show in Matches tab |
| "8-factor scoring" | — | A/B test on weights | Transparency mechanism | Radar chart + sliders |
| Feedback loop | — | Core architecture | Bias correction signal | Accept/decline buttons |
| Conversion funnel | Pipeline growth projections | Stage-by-stage KPIs | Aggregate-only metrics | End demo on funnel |
| University discovery | Rollout phases | Events-per-university metric | Scraping ethics | 60-second moment |
| "60 seconds" | Time-to-value claim | Time-to-match KPI | — | The centerpiece |

#### Recurring Data Points

These numbers should appear across multiple deliverables:

- **18** — board member volunteers (supply side)
- **15** — CPP events (demand side, Phase 1)
- **35 / 10** — total courses / High-fit courses (guest lecture opportunity)
- **5** — pre-configured universities (Phase 2-3 scope)
- **9** — IA West calendar events with university mappings (growth anchor)
- **60 seconds** — time-to-match (demo moment + KPI)
- **8 factors** — matching algorithm dimensions (transparency proof)
- **0 rows** — student PII (Responsible AI headline)

#### Document Drafting Order

The implementation agent should draft in this order (each builds on previous):

1. **Measurement Plan first** — defines KPIs that Growth Strategy references
2. **Growth Strategy second** — references KPIs and builds rollout narrative
3. **Responsible AI Note third** — references scoring transparency and data practices
4. **Demo Script last** — weaves narrative bridges to all three written documents

---

## Implementation Notes

- The guidance file should be placed at `docs/deliverables/BUSINESS_DELIVERABLES_GUIDE.md`
- The implementation agent will use this guidance to produce 4 separate deliverable documents in `docs/deliverables/`:
  - `GROWTH_STRATEGY.md` (2-3 pages)
  - `MEASUREMENT_PLAN.md` (1 page)
  - `RESPONSIBLE_AI_NOTE.md` (half page)
  - `DEMO_SCRIPT.md` (~1 page)
- All data references point to files in `data/` directory
- All code references point to files in `src/` directory
- Pre-computed stats are derived from CSV data as of 2026-03-23

---

## Approval Status

- [x] Preamble design approved
- [x] Mission 1 (Growth Strategy) design approved
- [x] Mission 2 (Measurement Plan) design approved
- [x] Mission 3 (Responsible AI) design approved
- [x] Mission 4 (Demo Script) design approved
- [x] Narrative Thread design approved
- [x] Approach C (Mission Brief) selected
