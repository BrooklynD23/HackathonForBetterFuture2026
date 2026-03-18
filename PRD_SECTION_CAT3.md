---
doc_role: canonical
authority_scope:
- category.3.feature_detail
canonical_upstreams:
- Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md
- MASTER_SPRINT_PLAN.md
- STRATEGIC_REVIEW.md
last_reconciled: '2026-03-16'
managed_by: repo-governance
---

## Category 3: IA SmartMatch --- Intelligent Speaker-Event Matching CRM
**Sponsor:** IA West | **CTO Tier:** 1 (Highest Win Probability) | **Verdict:** Approved with Revisions

> **Governance notice (repo-governance):** This document owns category feature-detail narrative. It must not override execution, staffing, milestone, or gating decisions from its canonical upstreams: `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `MASTER_SPRINT_PLAN.md`, `STRATEGIC_REVIEW.md`.

### Problem Statement

IA West is an entirely volunteer-run regional chapter of the Insights Association, covering the West Coast from Portland to San Diego. The chapter manages 8+ events per year across 6 metro regions, coordinates 18 board-level volunteers with varied expertise, and targets engagement with dozens of universities --- yet has **zero centralized infrastructure** for discovering opportunities, matching speakers, or tracking pipeline conversion. Today, opportunity discovery is ad-hoc (word of mouth, manual web browsing), speaker-event matching is done via email chains and gut feel, and there is no measurement of the engagement-to-membership funnel. Research by the Stanford Social Innovation Review estimates that volunteer-run nonprofit chapters lose 30-40% of potential engagement opportunities due to coordination overhead. For IA West specifically, this means missed guest lectures (35 relevant CPP course sections alone go largely untapped), career fairs without industry panelists, and hackathons where judging panels could be stronger. The lack of a conversion funnel means IA West cannot quantify ROI on volunteer time, cannot identify which engagement types drive membership, and cannot make data-backed decisions about where to invest effort across the Portland-to-San-Diego corridor.

### Proposed Solution

IA SmartMatch is an AI-orchestrated CRM prototype that automates the full lifecycle of university engagement: discovery, matching, outreach, and pipeline tracking. The system uses OpenAI vector embeddings (text-embedding-3-small) to semantically match volunteer expertise profiles against university event descriptions, producing explainable match scores with transparent weight breakdowns across six dimensions (topic relevance, role fit, geographic proximity, calendar fit, historical conversion, and student interest signal). An automated web scraping pipeline powered by BeautifulSoup and Playwright discovers new university opportunities across 5+ campuses, using GPT-4o-mini to extract structured event data from raw HTML. The platform generates personalized outreach emails for top matches, tracks the full engagement funnel from initial campus contact through IA event attendance to membership conversion, and visualizes the pipeline as a funnel chart that resonates with IA West's market research audience. Built in Streamlit for rapid deployment, the prototype leverages 77 rows of pre-existing structured data (speaker profiles, CPP events, course schedules, and the IA event calendar) to deliver a working demo from Day 1.

### Tech Stack

| Layer | Technology | Purpose | Free Tier? | Cost Estimate (2 weeks) |
|-------|-----------|---------|------------|------------------------|
| Frontend / Dashboard | Streamlit + Streamlit Community Cloud | Interactive CRM UI with tabs for Matches, Pipeline, and Discovery | Yes (1 GB RAM, public repo required) | $0 |
| Vector Matching | OpenAI text-embedding-3-small + cosine similarity (via NumPy) | Semantic matching of speaker expertise tags to event descriptions | Yes (free tier available) | < $0.01 (est. ~50K tokens total for 77 records x iterations) |
| LLM (Email Gen + Extraction) | OpenAI GPT-4o-mini | Outreach email generation, HTML-to-JSON event extraction, match explanation cards | Yes (free tier credits) | $0.05 - $0.50 (est. ~100 calls x ~500 tokens each) |
| Web Scraping (Static) | BeautifulSoup 4 + Requests | Parse static HTML from university event/career pages | Yes (MIT License, fully OSS) | $0 |
| Web Scraping (Dynamic) | Playwright (Python) | Render JavaScript-heavy university event pages before parsing | Yes (Apache 2.0 License, fully OSS) | $0 |
| Data Storage | CSV files + Pandas DataFrames | Hackathon-scope data persistence; no database needed | Yes (OSS) | $0 |
| Visualization | Plotly (Sankey / Funnel charts) | Pipeline funnel visualization, match score breakdowns | Yes (MIT License, OSS) | $0 |
| Caching Layer | Python shelve / JSON file cache | Cache scraped university pages to avoid redundant requests | Yes (Python stdlib) | $0 |

### API & Service Pricing Breakdown

All pricing verified as of March 2026 from [OpenAI Pricing](https://openai.com/api/pricing/):

| Service | Pricing Model | Rate | Estimated Usage (2-week hackathon) | Estimated Cost |
|---------|--------------|------|-----------------------------------|----------------|
| OpenAI text-embedding-3-small | Per 1M input tokens | $0.02 / 1M tokens (Standard) | ~50,000 tokens (77 records x multiple embedding passes, testing) | < $0.01 |
| OpenAI GPT-4o-mini (Input) | Per 1M input tokens | $0.15 / 1M tokens | ~200,000 input tokens (scraping extraction, email gen, match explanations) | ~$0.03 |
| OpenAI GPT-4o-mini (Output) | Per 1M output tokens | $0.60 / 1M tokens | ~100,000 output tokens | ~$0.06 |
| Streamlit Community Cloud | Free hosted deployment | $0 | 1 app, unlimited public viewers (within 1 GB RAM) | $0 |
| BeautifulSoup 4 | Open source (MIT) | $0 | Unlimited | $0 |
| Playwright | Open source (Apache 2.0) | $0 | Unlimited | $0 |
| **Total Estimated API Cost** | | | | **< $0.50** |

Note: OpenAI also offers Batch API at 50% discount ($0.01/1M tokens for embeddings, $0.075/$0.30 for GPT-4o-mini input/output). With the Batch API, total cost drops below $0.25. This project is among the lowest-cost categories in the hackathon.

### Complexity Assessment

| Dimension | Score (1-5) | Justification |
|-----------|-------------|---------------|
| AI/ML Complexity | 3 | Vector embeddings + cosine similarity is well-documented; multi-criteria weighted scoring is straightforward; LLM extraction uses standard few-shot prompting. No model training required. |
| Data Requirements | 2 | All four CSV datasets are pre-provided (77 total rows). No data collection, cleaning, or labeling needed. Scraping targets are publicly accessible university pages. |
| UI/UX Complexity | 3 | Streamlit provides rapid UI development; three-tab layout (Matches/Pipeline/Discovery) is standard. Pipeline funnel visualization and match explanation cards require moderate Plotly work. |
| Integration Complexity | 3 | Two OpenAI API integrations (embeddings + chat), web scraping pipeline with caching, and CSV data ingestion. No OAuth, no database, no complex auth flows. |
| Demo Polish Required | 4 | Judges explicitly want a live demo of matching AND automated discovery. The demo must show real-time scraping, real match results, and generated emails. Pipeline funnel visualization adds to polish requirements. |
| **Average** | **3.0** | **Moderate complexity overall --- well within 2-week scope for a 3-5 person team** |

### 2-Week Implementation Timeline

| Milestone | Days | Deliverables |
|-----------|------|-------------|
| M1: Data Exploration & Design | 1-2 | Load and profile all 4 CSV files in Pandas. Define embedding schema for speaker profiles and event descriptions. Design Streamlit wireframes (3-tab layout: Matches, Pipeline, Discovery). Set up project repo, environment, and OpenAI API key. Create vector embeddings for all 18 speaker profiles and 15 event records. Validate cosine similarity produces sensible rankings on known matches. |
| M2: Matching Engine + UI | 3-6 | Implement 6-factor MATCH_SCORE formula with configurable weights (topic relevance 0.30, role fit 0.25, geographic proximity 0.20, calendar fit 0.15, historical conversion 0.05, student interest 0.05). Build Matches tab showing top-3 speaker recommendations per event with score breakdown bar charts. Add match explanation cards using GPT-4o-mini ("Why was this speaker recommended?"). Integrate course schedule data for guest lecture matching. Add weight-tuning sliders for chapter leadership customization. |
| M3: Web Scraping Pipeline | 7-8 | Build scraper for 5 university event pages: UCLA, SDSU, UC Davis, USC, Portland State. Implement BeautifulSoup for static pages, Playwright for JS-rendered pages. Add JSON file cache layer (scrape once, serve from cache thereafter). Build GPT-4o-mini extraction pipeline: raw HTML to structured JSON (event name, category, date, volunteer roles, contact info). Display discovered events in Discovery tab with "Add to Matching" button. |
| M4: Email Gen + Pipeline Tracker | 9-10 | Build GPT-4o-mini email generation: personalized outreach templates using speaker profile + event details. Create Pipeline tab with funnel visualization (Plotly Sankey/funnel): Discovered to Matched to Contacted to Confirmed to Attended to Membership Inquiry. Add sample data to populate funnel with realistic conversion rates. Build email preview and copy-to-clipboard functionality. |
| M5: Written Deliverables + Demo | 11-14 | Write Growth Strategy (2-3 pages): target audience segments, value proposition for volunteers and universities, rollout plan from CPP to 3+ universities, channel strategy. Write Measurement Plan: KPIs (match acceptance rate, email response rate, event attendance rate, membership conversion rate), proposed A/B test for weight tuning, feedback loop for match quality improvement. Write Responsible AI Note (half page). Rehearse demo script: "A new hackathon was just announced at UCLA. SmartMatch detects it, matches Travis Miller as a judge, drafts his outreach email, and adds him to the pipeline --- in under 60 seconds." Record backup demo video. Final polish and edge case testing. |

### Team Allocation

**3-Person Team:**
| Role | Person | Responsibilities |
|------|--------|-----------------|
| AI/Backend Lead | Person 1 | Embedding pipeline, MATCH_SCORE algorithm, GPT-4o-mini integrations (extraction + email gen + match explanations), web scraping pipeline with caching, all API integration |
| Frontend/Viz Lead | Person 2 | Streamlit 3-tab dashboard, Plotly funnel/Sankey visualization, match explanation cards UI, weight-tuning sliders, email preview component, demo polish and rehearsal |
| Strategy/Research Lead | Person 3 | Growth Strategy document (2-3 pages), Measurement Plan with KPIs and A/B test proposal, Responsible AI Note, university event page research and URL curation for scraper targets, demo script authoring, presentation preparation |

**5-Person Team:**
| Role | Person | Responsibilities |
|------|--------|-----------------|
| AI/ML Engineer | Person 1 | Embedding pipeline, cosine similarity matching, MATCH_SCORE formula implementation, weight optimization |
| Backend/Scraping Engineer | Person 2 | Web scraping pipeline (BeautifulSoup + Playwright), GPT-4o-mini HTML extraction, caching layer, data pipeline architecture |
| Frontend Developer | Person 3 | Streamlit dashboard (3 tabs), Plotly visualizations, match explanation card UI, weight-tuning sliders, email preview, responsive layout |
| Growth Strategist | Person 4 | Growth Strategy document, Measurement Plan, KPI framework, A/B test design, channel strategy, rollout plan from CPP to 3+ universities |
| UX/Demo Lead | Person 5 | Responsible AI Note, demo script and rehearsal, university research and URL curation, user testing, presentation slides, backup video recording |

### Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| University event pages change structure or block scraping | Medium | High | Pre-scrape and cache pages for all 5 universities before demo day. Store cached HTML in repo. Use fallback static JSON fixtures if live scraping fails during demo. Rate-limit requests (1 req/5 sec) and respect robots.txt. |
| Match scores produce unintuitive or unexplainable results | Low | High | Use transparent weight breakdown (6 named factors with percentages). Add GPT-4o-mini match explanation cards that narrate why a match was recommended. Allow judges to adjust weights via sliders to see score changes in real time. |
| Written deliverables receive low scores (40% of judging) | Medium | Critical | Dedicate Person 3 (or Persons 4+5 in 5-person team) full-time to written deliverables starting Day 9. Use market research language that resonates with IA West (conversion funnel, A/B testing, segmentation). Include specific KPIs with target ranges. Reference actual data from the provided CSVs. |
| OpenAI API rate limits or outages during demo | Low | High | Implement response caching: once a match explanation or email is generated, cache it locally. Pre-generate all demo-path outputs. Embed API key as Streamlit secret (not hardcoded). Have a recorded backup demo video ready. |
| Streamlit Community Cloud resource limits (1 GB RAM) | Low | Medium | Keep Pandas DataFrames small (77 rows total). Use lazy loading for scraping results. Do not load Playwright in Streamlit Cloud --- run scraping locally and import results as cached JSON. Test memory footprint before deploying. |
| Scope creep --- trying to build too many features | Medium | Medium | Lock MVP scope at M2 milestone: matching engine with explanation cards is the minimum viable demo. Discovery tab and pipeline tracker are stretch goals. Prioritize demo polish over feature breadth. |

### Win Probability Assessment

- **CTO Tier:** 1 (Highest Win Probability)
- **Independent Analysis:** This category has the strongest combination of factors: (1) pre-provided structured data eliminates the cold-start problem that plagues other categories, (2) the technical implementation (embeddings + cosine similarity + LLM extraction) is well within a 2-week timeline, (3) the judging criteria explicitly reward written deliverables (Growth Strategy + Measurement Plan = 40% of points), which can be prepared in parallel with coding, and (4) the demo moment --- live automated discovery of a real university event, matched to a real board member, with a generated outreach email --- is visually compelling and easy to rehearse. The main competitive risk is another team building a similar CRM; differentiation comes from explainable AI (match cards), pipeline visualization (funnel chart), and the live scraping demo.
- **Demo Moment:** "A new hackathon was just announced at UCLA. SmartMatch automatically detected it from the UCLA events page, matched Travis Miller (SVP Sales, Ventura region) as the top judge candidate with an 87% match score, generated a personalized outreach email referencing his data collection expertise, and added him to the pipeline tracker --- all in under 60 seconds, live on stage." The funnel visualization then updates in real time, showing the new engagement flowing through the pipeline.
- **Overall Win Probability:** **High (55-75%)**. The pre-existing data, moderate technical complexity, and heavy weighting on written deliverables (which can be polished regardless of technical blockers) make this the most controllable outcome in the hackathon. The primary downside scenario is a competing team with an exceptionally polished demo; the primary upside is that the 40% written-deliverable weight rewards preparation over raw coding speed.

### Existing Assets Inventory

The team starts with a significant data advantage. Four structured CSV files are provided in the challenge materials:

| File | Rows | Key Fields | Strategic Value |
|------|------|-----------|----------------|
| `data_speaker_profiles.csv` | 18 records | Name, Board Role, Metro Region, Company, Title, Expertise Tags | Complete supply-side data. 18 board members across 6 metro regions (Ventura, LA West, SF, LA Long Beach, Portland, San Diego, Seattle) with rich expertise tags ready for embedding. |
| `data_cpp_events_contacts.csv` | 15 records | Event/Program, Category, Recurrence, Host/Unit, Volunteer Roles, Primary Audience, URL, Contact Name, Contact Email | Complete demand-side data for CPP. 15 distinct engagement opportunities (hackathons, case competitions, career fairs, research symposia) with real contact info. |
| `data_cpp_course_schedule.csv` | 35 records | Instructor, Course, Section, Title, Days, Times, Enrollment Cap, Mode, Guest Lecture Fit (High/Medium/Low) | 35 course sections with pre-labeled guest lecture fit ratings (10 High, 17 Medium, 8 Low). Enables immediate guest lecture matching without manual curation. |
| `data_event_calendar.csv` | 9 records | IA Event Date, Region, Nearby Universities, Suggested Lecture Window, Course Alignment | 9 IA West events across 2026 with pre-mapped university partnerships and timing windows. Directly feeds calendar-fit scoring. |

**Total: 77 structured records across 4 files, covering both supply (speakers) and demand (events/courses) sides of the matching problem.**

Additional assets:
- `IA_West_Smart_Match_Challenge.docx` --- Full challenge specification with detailed judging rubric
- `IA_West_Smart_Match_Challenge_Intro.pptx` --- Sponsor introduction deck with IA West organizational context

The team also has pre-identified scraping targets for 5+ universities with publicly accessible event pages:
- UCLA Career Center Events: https://career.ucla.edu/events/
- SDSU Events Calendar: https://www.sdsu.edu/events-calendar
- UC Davis Career Fairs: https://careercenter.ucdavis.edu/career-center-services/career-fairs
- USC Career Center Events: https://careers.usc.edu/events/
- Portland State University (events page to be confirmed during M1)

### Responsible AI Considerations

**Privacy and Data Handling:** All speaker profile data (names, companies, titles, expertise tags) is sourced from IA West board member information that is publicly available on the IA West website. No private or sensitive personal data is collected. University contact information (faculty emails, career center contacts) is scraped only from publicly listed university web pages. The system does not collect, store, or process any individual student data --- pipeline conversion metrics are tracked at the aggregate level only (e.g., "12 students attended the event" not "Student Jane Doe attended").

**Bias in Matching:** The weighted scoring algorithm could systematically over-match speakers in certain metro regions (e.g., LA-based speakers matched more often due to proximity to more universities) or favor speakers with more detailed expertise tags. Mitigation includes: (1) displaying match score breakdowns so chapter leadership can see which factor is driving recommendations, (2) adding a "diversity of speaker" flag that penalizes recommending the same speaker repeatedly, and (3) conducting a bias audit across the 18 speaker profiles to ensure geographic and expertise-tag balance.

**Transparency and Explainability:** The CTO directive explicitly requires that matching be explainable. Every match recommendation includes: (a) a score breakdown showing contribution of each of the 6 factors, (b) a natural-language explanation card generated by GPT-4o-mini explaining the recommendation in plain English, and (c) adjustable weight sliders so users can see how changing priorities affects rankings. No "black box" scores are shown without explanation.

**Responsible Scraping:** The system respects robots.txt, rate-limits requests to 1 per 5 seconds, caches all scraped pages locally (scrape once, serve from cache), and only accesses publicly available university event pages. No login-gated content is accessed. No automated form submissions are performed. The scraping pipeline includes clear attribution of data sources in the UI.
