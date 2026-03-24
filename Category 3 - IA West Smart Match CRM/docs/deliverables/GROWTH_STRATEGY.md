# Growth Strategy: IA West SmartMatch CRM

## 1. Executive Summary

SmartMatch is a volunteer-event matching engine purpose-built for IA West. It takes the chapter's 18 board volunteers, 15 CPP engagement opportunities, and 35 course sections and runs them through an 8-factor weighted algorithm that produces rank-ordered match recommendations in under 60 seconds. The result: every board volunteer sees only high-fit events, every university coordinator receives pre-vetted industry professionals, and chapter leadership gets a live pipeline from first contact through membership inquiry.

The growth thesis is straightforward. SmartMatch is already loaded with real CPP data and pre-configured for five additional universities. Scaling from one campus to seven metro regions does not require new engineering -- it requires pasting a URL and letting the discovery engine extract events automatically. This document lays out the three-phase rollout from CPP pilot to West Coast coverage, with data-backed success criteria at every stage.

---

## 2. The Problem Today

IA West has 18 board member volunteers spread across 10 metro designations and 7 consolidated regions -- Seattle, Portland, San Francisco, Los Angeles, Ventura, Orange County, and San Diego. These volunteers represent decades of market research expertise. The chapter also has access to thousands of university engagement opportunities: guest lectures, career fairs, competitions, and campus events across the West Coast.

Yet there is no system connecting supply to demand. Coordination happens through email chains and spreadsheets. A board member in Los Angeles has no visibility into a guest lecture opportunity at UCLA that matches their specialization. A career center at Cal Poly Pomona has no structured way to request an IA West speaker for a high-fit course section.

The cost of this coordination gap is measurable. Of the 35 course sections at CPP alone, 10 are classified as high-fit for IA West guest lectures -- representing approximately 300 students per term (10 courses at an average enrollment of 30). Without systematic matching, these slots go unfilled or are filled through ad-hoc personal networks, leaving both volunteer capacity and student impact on the table. Across 9 IA calendar events spanning all 7 metro regions, the missed-connection surface area multiplies. SmartMatch exists to close this gap.

---

## 3. Target Audience Segments

### Segment 1: Board Member Volunteers

**Value proposition:** "Spend your limited volunteer hours on high-fit events, not email chains."

IA West's 18 board volunteers are working professionals who donate their time to the chapter. Today, matching a volunteer to an event involves multi-day email threads, manual calendar checks, and geographic guesswork. SmartMatch replaces this with an 8-factor algorithm that evaluates topic relevance, geographic proximity, schedule availability, experience level, audience alignment, engagement history, event urgency, and coverage diversity -- delivering ranked recommendations in under 60 seconds. The time savings alone reduce volunteer burnout. The quality improvement means every speaking engagement is one where the volunteer's expertise genuinely fits the audience. With a target of 3 or more events per speaker per year, SmartMatch ensures utilization is high but sustainable.

### Segment 2: University Coordinators

**Value proposition:** "Get curated, pre-vetted industry professionals delivered to your inbox."

University career centers and faculty coordinators face the inverse problem: they need qualified industry guests but lack a systematic channel to IA West's speaker pool. At CPP, 15 events currently exist with real contact emails in the system, yet none are connected to IA West's 18 volunteers through any structured process. SmartMatch generates match recommendations that include the volunteer's background, expertise areas, and fit score -- giving coordinators confidence that the suggested speaker is relevant to their event. The 6-stage pipeline (Discovered, Matched, Contacted, Confirmed, Attended, Member Inquiry) provides coordinators with visibility into engagement status at every step.

### Segment 3: Students (Indirect Beneficiaries)

**Value proposition:** "Better industry speakers at your events means better career connections."

Students do not interact with SmartMatch directly, but they are its ultimate beneficiaries. When matching quality improves, the speakers who show up at guest lectures, career panels, and networking events are more relevant to the students in the room. At CPP, 10 high-fit courses reach approximately 300 students per term. Each well-matched guest lecture is an opportunity for students to build connections with practicing market research professionals -- connections that feed IA's long-term membership pipeline. The simulated funnel estimates that 15% of event attendees generate a membership inquiry, making student engagement a leading indicator of chapter growth.

---

## 4. Rollout Plan

### Phase 1: CPP Pilot (Q2 2026)

**Scope.** All existing structured data: 15 CPP events with real contact emails, 35 course sections (10 High-fit, 16 Medium-fit, 9 Low-fit), and 18 board volunteers with complete profiles including metro designations, expertise areas, and availability.

**Why CPP first.** The data is already loaded, cleaned, and validated -- 77 total structured records across four CSV files. The prototype is fully functional: matching, feedback collection, pipeline tracking, and discovery are all operational. There is zero cold-start risk.

**Success criteria.**
- Match acceptance rate >= 60% (baseline measured via `feedback_log.csv` through `acceptance.py`)
- 5 or more guest lectures booked from the 10 high-fit course sections
- Volunteer utilization >= 3 events per speaker per year
- Time-to-match consistently < 60 seconds
- Feedback loop generating actionable weight adjustment suggestions after each event cycle

**Data anchors.** The 10 high-fit courses are already identified by name, instructor, and time slot. The 15 events include real coordinator contact emails. This is not a projection -- it is a deployment of existing, tested functionality.

**Risk.** Low. All data is pre-loaded, the algorithm is calibrated, and the feedback module is production-ready. The primary risk is adoption velocity, mitigated by the channel strategy below.

### Phase 2: LA Metro Expansion (Q3-Q4 2026)

**Scope.** Add UCLA and USC to the SmartMatch event pool using the pre-configured discovery scraping module. Extend matching to cover LA-area board volunteers alongside CPP's existing pipeline.

**Why LA Metro.** The IA West event calendar maps the June 18 LA event directly to "UCLA, USC, Cal Poly Pomona, LMU" -- these universities are already identified as target institutions for IA West engagement. The Discovery tab in the prototype is pre-configured with UCLA and USC URLs, meaning event extraction requires activation, not development.

**Success criteria.**
- 3 or more events discovered per university via automated scraping
- 10 or more new matches generated across UCLA and USC events
- Funnel conversion rates tracking to baseline: 80% contact, 45% confirm, 75% attend
- At least 2 LA-area board volunteers matched to UCLA/USC events

**Enablers.** The discovery engine already handles URL-to-event extraction. Adding a university is a three-step process: paste the events page URL, let the AI extract structured event data, and events automatically enter the matching pool. No engineering effort is required beyond configuration.

**Risk.** Moderate. University event pages vary in structure, which may require scraper tuning. Mitigated by the AI-powered extraction layer, which adapts to page formats without hard-coded selectors.

### Phase 3: West Coast Coverage (2027)

**Scope.** Activate all 5 pre-configured discovery universities (UCLA, USC, SDSU, UC Davis, Portland State) and leverage the IA event calendar's 9 events across all 7 metro regions. Target full geographic coverage from Seattle to San Diego.

**Why West Coast.** The IA event calendar already maps 20+ universities to event windows across Portland, San Diego, San Francisco, Seattle, Ventura, Orange County, and Los Angeles. SmartMatch's 18 volunteers span all 7 consolidated regions. The infrastructure to match volunteers to events coast-wide is built -- Phase 3 activates it at scale.

**Success criteria.**
- All 7 metro regions generating active matches
- 50 or more events per year in the SmartMatch pipeline
- Geographic coverage ratio = 7/7 regions active
- Volunteer load balance (coefficient of variation) < 0.30 across regions
- Membership inquiry rate of 10-15% of event attendees, consistent with simulated pipeline projections

**Data anchors.** SDSU maps to the San Diego IA event (August 14). UC Davis maps to the Sacramento/SF corridor. Portland State maps to the Portland IA event (July 16). These are not aspirational targets -- they are entries in `data_event_calendar.csv` with dates, regions, and mapped universities already populated.

**Risk.** Moderate-to-high on coordination complexity; low on technology. The matching engine, feedback loop, and discovery scraper all scale horizontally. The challenge is chapter operations: ensuring each metro director reviews matches, coordinates outreach, and closes the feedback loop. Mitigated by the reporting cadence defined in the Measurement Plan.

---

## 5. Channel Strategy

### Board Meetings

Live SmartMatch demonstrations during quarterly IA West board meetings. Show the matching engine processing a real event, generating volunteer recommendations, and displaying the pipeline dashboard. Board members see their own profiles matched to upcoming events -- making adoption personal, not abstract. This is the primary channel for volunteer segment activation.

### University Outreach

AI-generated personalized outreach emails sent from IA West coordinators to career center contacts. Each email references the specific event, the matched volunteer's expertise, and the relevance score -- moving the conversation from "would you like a speaker?" to "here is a pre-vetted professional who scores 87% fit for your April career panel." The 15 CPP event contacts already in the system provide the initial outreach list; discovered events from UCLA, USC, SDSU, UC Davis, and Portland State extend it in Phases 2 and 3.

### Organic Discovery

The scraper module continuously monitors configured university event pages. When a new event is detected, SmartMatch automatically generates matches and alerts the relevant metro director. This channel requires no manual effort after initial configuration -- events flow into the matching pool as they are published. The result is a self-replenishing pipeline that grows with each university added.

### Scalability Proof Point

Adding a new university to SmartMatch is a three-step process:

1. Paste the university's events page URL into the Discovery configuration
2. The AI extraction engine parses the page and structures event data
3. Extracted events enter the matching pool and receive volunteer recommendations

No code changes. No data migration. No IT tickets. A board volunteer with browser access can expand SmartMatch's coverage in under five minutes. This operational simplicity is what makes the CPP-to-West-Coast trajectory realistic rather than aspirational.

---

## Cross-Reference: Measurement Plan KPIs

Each rollout phase is accountable to the KPIs defined in the Measurement Plan:

| Phase | Primary KPIs | Targets |
|-------|-------------|---------|
| Phase 1 (CPP) | Match acceptance rate, time-to-match, guest lecture penetration | >= 60%, < 60 sec, 5/10 courses |
| Phase 2 (LA Metro) | Events discovered, matches generated, funnel conversion | 3+/university, 10+ matches, 80/45/75% |
| Phase 3 (West Coast) | Geographic coverage, volunteer utilization, membership inquiry | 7/7 regions, >= 3 events/speaker/year, 10-15% |

The feedback loop architecture -- from match generation through decline-reason capture through automated weight suggestions -- ensures that each phase's performance data directly improves the next phase's matching quality. Growth and measurement are not separate workstreams; they are the same closed loop operating at increasing scale.
