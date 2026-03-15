# CTO Review Output — CPP AI Hackathon "AI for a Better Future"
**Reviewer:** CTO Review Agent | **Date:** March 14, 2026
**Event:** April 16, 2026 | **Prep Window:** ~2 weeks | **Team Size:** 3–5

---

## Executive Summary

The planning agent has produced five well-structured category plans with clear challenge extraction, researched tech stacks, and actionable MVP scoping. With a **2-week preparation window** (not a typical 48-hour sprint), the team has significantly more room to build polished prototypes, iterate on UX, and pre-validate technical components before demo day. This changes the calculus: plans that would be risky in 48 hours become realistic, and the bar for what constitutes a "winning" submission rises — judges will expect more polish.

The portfolio is strongest in **Categories 2 (Cyber Safety Coach)** and **3 (Smart Match CRM)** — both have tightly scoped MVPs, available data, and clear demo moments that can be elevated to near-production quality in 2 weeks. **Category 4 (Aytm Simulated Research)** is the dark horse: a working codebase plus 2 weeks means the team can deliver genuinely substantive improvements and a compelling ground-truth validation story. **Category 5 (SDG Creative)** becomes much more viable with 2 weeks — enough time to properly configure a CV model, build a quality LLM advisory system, and craft a powerful narrative. **Category 1 (Wellbeing)** is solid but risks blending into a crowded field of wellness tools unless the team invests in a truly distinctive UI/demo moment.

No fatal flaws were found. Several plans can now incorporate "nice-to-have" features into the core MVP given the extended timeline.

---

## Category 1 Review — Avanade AI Wellbeing ("BalanceIQ")

**Overall Verdict:** APPROVED WITH REVISIONS

### Scores
- **Technical Feasibility: 4/5** — With 2 weeks, the team can build a realistic Viva Insights-style dashboard with synthetic data, implement a rules-based wellbeing scoring engine, and integrate LLM-powered nudge generation. Azure ML anomaly detection remains overkill, but the overall architecture is buildable. NLP sentiment analysis on meeting transcripts is feasible if scoped to pre-recorded samples.
- **Competitive Differentiation: 3/5** — "AI wellbeing coach for tech workers" remains a crowded space (BetterUp, Headspace for Work, Calm Business, Viva Insights itself). The dual-layer design (individual + manager aggregate) is the genuine differentiator, but the core concept needs a sharper hook beyond "another wellness dashboard."
- **Sponsor Alignment: 4/5** — Strong Avanade/Microsoft ecosystem awareness. Correctly identifies Viva Insights, Teams, Azure AI, Power BI. The tech worker focus aligns well with Avanade's consulting practice.
- **Risk Profile: Medium** — Top risk: The concept doesn't clearly escape the "just another chatbot/dashboard" perception. With 2 weeks the technical risk drops, but the differentiation risk remains. The team needs to lean hard into the manager heatmap and team-level insights as the unique angle.
- **PRD/MVP Readiness: 3/5** — The MVP scope is reasonable but vague on what the actual working AI inference looks like. "Analyze sample meeting data → output wellbeing score + nudge" needs more specificity: what model? What input format? What's the score calculation?

### Strengths
- Correctly identifies tech workers over students as the stronger Avanade play
- Dual-layer design (individual + anonymized team view) shows systems thinking
- Responsible AI checklist is thorough — non-clinical positioning, consent, bias audit
- Strong demo persona narrative ("Sarah hasn't taken lunch in 3 weeks")

### Gaps & Concerns
- Architecture oversells Azure ML anomaly detection — even with 2 weeks, training a time-series model on synthetic data produces meaningless results. Use rules-based thresholds instead.
- No concrete fallback if Microsoft API integrations don't work
- "Wellbeing score across 4 dimensions" is undefined — what's the formula?
- The concept doesn't clearly escape the "just another chatbot" trap

### CTO Recommendations
1. **Replace anomaly detection with a well-designed rules engine.** Define explicit thresholds (meetings > 6/day = boundary score drops; no focus blocks > 2hrs = focus score drops). This is honest, interpretable, and more impressive than a black-box ML model on fake data.
2. **Define the wellbeing score formula explicitly.** Four dimensions (focus, boundaries, rest, social connection), each scored 0-100 based on configurable rules, with an LLM generating the narrative explanation and personalized nudge.
3. **The manager heatmap dashboard IS the demo moment.** With 2 weeks, build a genuinely polished Power BI-style grid showing team burnout hotspots with drill-down capability. This is more memorable than any chatbot interaction.
4. **Build a realistic onboarding flow.** 2 weeks allows for a proper consent-and-setup experience that demonstrates responsible AI thinking. Show the user exactly what data is collected and why.
5. **Sharpen the positioning:** "Viva Insights for companies that don't have Microsoft 365 E5 licenses" — a democratized version. That's a clearer hook than generic "AI wellbeing advisor."

### Handoff Instructions for Research Agent
- **Priority 1:** Define the exact wellbeing score calculation (4 dimensions, input metrics, thresholds, formula). Make it rules-based.
- **Priority 2:** Research Microsoft Viva Insights data schema and create a realistic synthetic dataset (JSON) with 2 weeks of simulated work pattern data for 8-10 employees.
- **Priority 3:** Design and build the manager heatmap dashboard — this is the demo moment. Use Plotly heatmaps in Streamlit.
- **Priority 4:** Build the onboarding flow with consent model and data transparency screens.
- **Must answer before PRD:** What specific data inputs does the system need, and can they all be simulated convincingly?
- **Red line:** Do NOT propose training any ML model. All AI should be LLM-based (API calls) + rules-based scoring.

---

## Category 2 Review — ISACA Cyber Safety Coach ("PhishGuard AI")

**Overall Verdict:** APPROVED

### Scores
- **Technical Feasibility: 5/5** — This was already the most buildable plan in a 48-hour window. With 2 weeks, the team can build every "nice-to-have" feature: URL scanning, privacy redaction, Spanish toggle, screenshot OCR, demo scenario library, and a polished UI. This should be the most complete, most polished submission in the portfolio.
- **Competitive Differentiation: 4/5** — The "educate, don't just classify" angle is the right move. The micro-lesson feature genuinely differentiates. The privacy redaction toggle is a strong demo moment. Confidence + uncertainty signaling builds trust. With 2 weeks, the team can build ALL of these to a high standard.
- **Sponsor Alignment: 5/5** — Perfectly aligned. References NIST, Zero Trust, ISACA CMMI. Uses PhishTank. The "cyber literacy for non-experts" mission is exactly what ISACA cares about.
- **Risk Profile: Low** — Top risk: LLM hallucination on classification. Mitigation is already in the plan (rule-based pre-filters + URL reputation). With 2 weeks, the team can build robust cross-validation between layers.
- **PRD/MVP Readiness: 5/5** — Prompt template already written, tech stack defined, demo narrative exists. Ready for immediate PRD writing.

### Strengths
- Most technically feasible plan — every component is proven and well-understood
- Prompt template is already written and well-structured
- Privacy-by-design (PII redaction) is both a feature AND a responsible AI differentiator
- Demo narrative is concrete and relatable ("Maria gets a Netflix suspension text")
- With 2 weeks, ALL stretch goals become achievable

### Gaps & Concerns
- No conflict resolution strategy when LLM and rule-based layer disagree
- The "Teach-back" micro-lesson feature is listed as stretch but should be core — it's the primary differentiator
- No mention of building a curated demo scenario library (pre-analyzed examples that showcase different threat types)

### CTO Recommendations
1. **Promote ALL stretch goals to MVP.** With 2 weeks: micro-lessons, Spanish toggle, URL scanning (PhishTank + Google Safe Browsing), privacy redaction, screenshot OCR (GPT-4o Vision), confidence scores, and report export are all achievable. Build them all.
2. **Define conflict resolution between layers.** Rule: if URL is in PhishTank, override LLM to "High Risk." If rule-based pre-filter flags 3+ indicators but LLM says "Safe," escalate to "Suspicious" with explanation of disagreement.
3. **Build a curated demo library of 10+ scenarios.** Cover: obvious phishing, subtle phishing, legitimate email that looks suspicious, scam SMS, malicious URL, clean URL, borderline case, non-English phishing. Pre-run all through the system. This becomes both test suite and demo material.
4. **Invest in UI polish.** With 2 weeks, go beyond Streamlit defaults. Use custom CSS, branded colors, professional typography. A polished UI signals "this could be deployed tomorrow" — which is what ISACA judges want to see.
5. **Build a "threat landscape" dashboard page** showing aggregate statistics from analyzed messages (most common threat types, average confidence scores). This signals scalability beyond single-message analysis.

### Handoff Instructions for Research Agent
- **Priority 1:** Validate PhishTank API AND Google Safe Browsing API. Test both with 10 sample URLs. Document response times and rate limits.
- **Priority 2:** Build the 10+ demo scenario dataset — diverse inputs with expected outputs and micro-lesson content for each threat type.
- **Priority 3:** Research the top 15 phishing patterns from the 2025 Verizon DBIR — these inform both the rule-based layer and the micro-lesson content library.
- **Priority 4:** Design the full UI with all features: input field, risk display, explanation card, micro-lesson, redaction toggle, language toggle, feedback button, report export.
- **Priority 5:** Implement screenshot OCR pipeline using GPT-4o Vision — test with 5 sample phishing screenshots.
- **Must answer before PRD:** What is the PhishTank API response time? Can classification complete in under 10 seconds end-to-end?
- **Red line:** Do NOT store user inputs. Do NOT explain how to craft phishing attacks. URL reputation must be a hard override on LLM classification.

---

## Category 3 Review — IA West Smart Match CRM

**Overall Verdict:** APPROVED WITH REVISIONS

### Scores
- **Technical Feasibility: 5/5** — With 2 weeks, the entire four-module architecture is buildable. The matching algorithm is well-defined. CSV data is provided. Web scraping + LLM extraction can be properly tested and hardened. Even vector embeddings (originally recommended as a downgrade to TF-IDF for 48h) are now feasible with OpenAI text-embedding-3-small.
- **Competitive Differentiation: 4/5** — Live web scraping + LLM extraction is the killer differentiator. The "add a university in 3 clicks" story is compelling. With 2 weeks, the team can scrape and cache 5+ universities, making the scalability story much more convincing.
- **Sponsor Alignment: 4/5** — Good market research language. Correctly identifies IA West as volunteer-run. Minor gap: doesn't explicitly reference IA West's membership value proposition or specific volunteer coordination pain points.
- **Risk Profile: Low-Medium** — Top risk: Web scraping is inherently brittle. With 2 weeks, mitigation is straightforward: pre-scrape and cache 5 universities, show one live scrape with cached fallback.
- **PRD/MVP Readiness: 4/5** — Matching algorithm formula is explicitly defined. Data files listed. Missing: the Growth Strategy and Measurement Plan deliverables (worth ~20 of 50 points) are under-specified in the plan.

### Strengths
- Real data provided (speaker profiles, CPP events, course schedules) — eliminates synthetic data concerns
- Matching algorithm is explicitly specified with tunable weights — not a black box
- Four-module architecture cleanly maps to challenge brief requirements
- Demo narrative is specific and memorable ("SmartMatch detects UCLA hackathon, matches Travis Miller, drafts email — 60 seconds")

### Gaps & Concerns
- Growth Strategy and Measurement Plan deliverables are mentioned but not detailed — worth 20 of 50 judging points
- Pipeline tracker (Module 4) is underdeveloped
- The plan doesn't reference IA West's specific membership value proposition

### CTO Recommendations
1. **Use vector embeddings (OpenAI text-embedding-3-small) for the matching engine.** With 2 weeks, the team has time to implement and validate semantic matching properly. This produces better matches than TF-IDF and is more impressive in the demo.
2. **Pre-scrape 5+ university event pages and cache results.** Test scraping on: UCLA, SDSU, UC Davis, USC, Portland State. Build a robust extraction pipeline that handles different HTML structures. Show 1-2 live scrapes in demo with cached fallback.
3. **Allocate serious time for Growth Strategy and Measurement Plan.** These written deliverables are worth 20 of 50 points. The research agent must produce a polished 2-3 page Growth Strategy and a 1-page Measurement Plan with specific KPIs.
4. **Build a proper pipeline tracker.** With 2 weeks, build a real pipeline visualization — a Sankey or funnel chart showing conversion stages (Discovered → Contacted → Confirmed → Attended → Member). Market researchers love funnel visualizations.
5. **Add match explanation cards with natural language.** When showing a match, display the score breakdown AND a generated explanation: "Travis Miller matched to UCLA Hackathon because his expertise in MR technology aligns with data analytics competition (Topic: 0.85), and Ventura is 45 min from UCLA (Proximity: 0.90)."

### Handoff Instructions for Research Agent
- **Priority 1:** Verify all CSV data files load correctly. Build a data quality report (missing values, encoding issues, field consistency). Explore the data and document insights.
- **Priority 2:** Identify 5+ university event pages with structured listings. Test LLM extraction on each. Build a robust pipeline. Cache results.
- **Priority 3:** Draft the Growth Strategy document (2-3 pages): target segments, CPP-first rollout, expansion to 3+ universities, value proposition for volunteers and universities, channel strategy.
- **Priority 4:** Draft the Measurement Plan (1 page): KPIs for match acceptance rate, event attendance, membership conversion, volunteer utilization. Include one proposed A/B test for weight tuning.
- **Priority 5:** Build the pipeline funnel visualization using Plotly Sankey.
- **Must answer before PRD:** Does semantic matching with embeddings produce meaningfully better results than keyword overlap on this dataset? Run a comparison.
- **Red line:** Do NOT skip the Growth Strategy and Measurement Plan — they're 40% of the judging score. Do NOT scrape without caching and fallback.

---

## Category 4 Review — Aytm x Neo Smart Living (Simulated Market Research)

**Overall Verdict:** APPROVED WITH REVISIONS

### Scores
- **Technical Feasibility: 5/5** — Working codebase provided. With 2 weeks, the team can run the entire pipeline, deeply improve 2-3 stages, build publication-quality visualizations, and validate against ground truth data. This is the lowest-risk category technically.
- **Competitive Differentiation: 4/5** — Dual-LLM reliability check is a genuinely sophisticated differentiator. Ground truth validation is rare and impressive. With 2 weeks, the team can make the "before vs. after" improvement story compelling. The risk is narrative: "we improved someone else's prototype" is harder to sell than "we built this."
- **Sponsor Alignment: 4/5** — Good positioning relative to Aytm Skipper. References STAMP paper. Could more explicitly frame how this feeds Aytm's ecosystem.
- **Risk Profile: Low** — Top risk: Spreading too thin across 6 pipeline stages. The plan recommends Stages 2+4+5, which is now achievable in 2 weeks, but the team must still resist the temptation to touch all 6.
- **PRD/MVP Readiness: 4/5** — Good existing codebase documentation. Missing: explicit "before vs. after" specification for each improvement.

### Strengths
- Working prototype eliminates most execution risk
- Real ground-truth data enables validation — rare and valuable
- Academic paper references signal methodological seriousness
- Cost comparison ($0.08 vs. $12K-$24K) is an immediately compelling demo opener
- Dual-LLM reliability is genuine innovation

### Gaps & Concerns
- No mention of how to handle the business presentation deliverable for Tony Koo
- Existing codebase quality is unknown — could have hidden complexity
- API costs for running 200+ synthetic respondents need budgeting
- The "improvement" narrative must be carefully crafted to feel like ownership, not just iteration

### CTO Recommendations
1. **Focus on Stages 2 + 4 + 5 as planned — 2 weeks makes this achievable.** Stage 2: richer multi-turn interviews with follow-up probing. Stage 4: scale to 200+ respondents with better persona diversity. Stage 5: publication-quality analysis with confidence intervals and effect sizes.
2. **Build a compelling "before vs. after" comparison.** Show the original prototype output, then the improved version side-by-side. Document specific improvements with metrics.
3. **Create a first-class Tony Koo business recommendation.** End the demo with: "Based on simulated research across 200 synthetic respondents, Neo Smart Living should prioritize the [Adventure/Home Office] positioning for [segment], validated by cross-model agreement (p < 0.01)."
4. **Compare at least 3 synthetic findings against real data images.** Show: "Our simulation predicted [X]. Actual research found [Y]. Agreement rate: [Z]%." This honesty IS the demo moment.
5. **Add Krippendorff's alpha for intra-persona consistency.** With 2 weeks, this is implementable and adds methodological credibility that judges from Aytm will recognize.

### Handoff Instructions for Research Agent
- **Priority 1:** Run the existing prototype locally. Document setup process, bugs, code quality, and API costs for a full run.
- **Priority 2:** Read the STAMP methodology paper. Extract principles for implementation.
- **Priority 3:** Compare synthetic data outputs against all 4 real data images (transcript, theme analysis, demographics, concept test). Build a structured comparison report.
- **Priority 4:** Research Aytm Skipper capabilities. Understand the commercial landscape.
- **Priority 5:** Implement Krippendorff's alpha for intra-persona consistency measurement.
- **Priority 6:** Scale respondent generation to 200+ with cost tracking (token counting via tiktoken).
- **Must answer before PRD:** What is the existing prototype's code quality? What's the API cost for 200 respondents? What specific improvements would be most visible in a demo?
- **Red line:** Do NOT attempt all 6 stages — focus on Stages 2, 4, 5. Do NOT rewrite the codebase from scratch. Do NOT skip the ground truth comparison. Do NOT present synthetic data as real.

---

## Category 5 Review — Avanade Creative SDG ("CropSense AI")

**Overall Verdict:** APPROVED WITH REVISIONS

### Scores
- **Technical Feasibility: 4/5** — With 2 weeks, the team can properly configure Azure Custom Vision on PlantVillage data (2-3 days for data prep + training + validation), build a quality LLM advisory system with multi-language support (3-4 days), and craft a polished frontend with SDG dashboard (2-3 days). Weather API integration becomes feasible as a secondary feature. SMS delivery via Twilio is still a stretch but possible if scoped carefully.
- **Competitive Differentiation: 5/5** — Strongest narrative in the portfolio. "Every precision ag tool is built for John Deere tractors, not for Amina's 2-acre maize plot" is genuinely moving. The equity angle (SMS-first, multi-lingual, feature-phone compatible) is emotionally compelling. Multi-type AI stack signals ambition.
- **Sponsor Alignment: 5/5** — Perfect Avanade/Microsoft alignment: Azure AI Vision, Azure OpenAI, Planetary Computer, sustainability commitments. Hits Avanade's trifecta: responsible AI, sustainability, inclusion.
- **Risk Profile: Medium** — Top risk: PlantVillage dataset is well-known; judges may have seen crop disease classifiers before. The differentiator must be the ADVISORY system + equity story, not the classification itself. Secondary: Azure Custom Vision requires an Azure subscription with credits.
- **PRD/MVP Readiness: 3/5** — Compelling concept but MVP feature list still needs clearer prioritization even with 2 weeks.

### Strengths
- Strongest storytelling potential in the entire portfolio — judges will remember "Amina"
- SDG alignment is authentic, with verifiable impact numbers
- Multi-type AI stack demonstrates technical sophistication
- Microsoft ecosystem alignment is near-perfect
- Alternative concepts (EduBridge, ClimateGuard, HealthAccess) provide fallback pivots

### Gaps & Concerns
- PlantVillage is a well-known dataset — the differentiator must be the advisory, not the classification
- The plan tries to incorporate 4 AI systems (CV + LLM + forecasting + time-series); even with 2 weeks, 3 is the safe maximum
- Azure Custom Vision requires Azure credits — need to confirm access
- No provided data or prototype — everything built from scratch

### CTO Recommendations
1. **Use Azure Custom Vision with PlantVillage data.** 2 weeks allows proper setup: curate 500-1000 images across 5-7 diseases, train, validate, iterate. Target >90% accuracy on the selected diseases.
2. **The LLM advisory IS the product.** Spend 40% of dev time on advisory quality: contextual, actionable, multi-lingual, SMS-friendly. Build a prompt that takes disease + confidence + crop type + region and generates advice a farmer can actually use.
3. **Add weather API integration as a secondary feature.** With 2 weeks, Open-Meteo API (free) integration is feasible. Show: "Your maize has gray leaf spot AND rain is forecast for 3 of the next 5 days — apply fungicide TODAY before the moisture worsens spread."
4. **Build a proper SMS output mode** (but skip Twilio). Show SMS-formatted advisory (<160 chars) in the UI with a clear "SMS-ready" label. If time permits, add a Twilio sandbox demo.
5. **Invest in the narrative.** With 2 weeks, create a 60-second video vignette of the "Amina" use case to open the demo. This emotional hook, followed by a live technical demo, is a winning formula for the creative category.

### Handoff Instructions for Research Agent
- **Priority 1:** Set up Azure Custom Vision. Upload PlantVillage subset (5-7 diseases, 500-1000 images). Train and validate. Target >90% accuracy. Document the process.
- **Priority 2:** Design the LLM advisory prompt system. Test with 10 disease scenarios across 3 languages (English, Spanish, Swahili). Evaluate output quality.
- **Priority 3:** Integrate Open-Meteo weather API. Build the logic: disease + weather forecast → urgency-adjusted advisory.
- **Priority 4:** Research existing smallholder AI tools (Plantix, DigiFarm, Hello Tractor). Build a competitive comparison slide.
- **Priority 5:** Compile impact statistics with citations (FAO, World Bank) for SDG alignment narrative.
- **Priority 6:** Design the SDG impact dashboard — visual showing contributions to SDG 2, 13, 10 with quantified claims.
- **Must answer before PRD:** Can Azure Custom Vision achieve >90% accuracy on a PlantVillage subset with <3 days of setup? Does the team have Azure credits?
- **Red line:** Do NOT train a model from scratch with PyTorch/TensorFlow. Do NOT attempt price prediction for MVP. Do NOT overclaim accuracy — show confidence scores honestly. Limit to 3 AI systems max (CV + LLM + weather integration).

---

## Priority Tier Rankings

### Tier 1 — Highest Win Probability: Category 2 (ISACA Cyber Safety Coach), Category 3 (IA West Smart Match CRM)

**Rationale:** Category 2 is the most technically feasible plan with perfect sponsor alignment and the lowest execution risk. With 2 weeks, every stretch goal becomes achievable — the team can deliver a near-production-quality tool that ISACA could genuinely pilot. Category 3 benefits from real provided data, a well-defined matching algorithm, and a killer demo moment (live web scraping + instant match). Two weeks allows the team to build a robust multi-university discovery pipeline and properly develop the Growth Strategy and Measurement Plan documents that are worth 40% of the judging score.

### Tier 2 — Strong Contenders: Category 4 (Aytm Simulated Research), Category 5 (Avanade Creative SDG)

**Rationale:** Category 4 has the lowest technical risk (working codebase provided) and 2 weeks allows genuinely substantive improvements — scaling to 200+ respondents, publication-quality analysis, and a compelling ground-truth validation story. The challenge is narrative: the team must present improvements as ownership, not just iteration. Category 5 has the strongest emotional narrative and sponsor alignment. With 2 weeks, the CV model + LLM advisory + weather integration becomes a realistic three-system architecture. The "Amina" story could be the most memorable demo in the entire hackathon if executed well.

### Tier 3 — Lower Priority / Optional: Category 1 (Avanade Wellbeing)

**Rationale:** Category 1 is a solid plan in a crowded space. Even with 2 weeks of development, "AI wellbeing coach" remains one of the most common hackathon submissions, and differentiating from the field is harder here than in any other category. The manager heatmap dashboard is the one unique angle worth developing. If the team has bandwidth, invest in making this dashboard visually exceptional — otherwise, deprioritize in favor of Categories 2-5.

---

## Master Handoff Brief — For Research Agents

### Team Strategy

With a 2-week preparation window, the team can realistically pursue all 5 categories with high-quality submissions. **Prioritize Categories 2 and 3** for highest win probability — both can be built to near-production quality. Invest strong secondary effort in **Categories 4 and 5** — Category 4 leverages existing code for a polished improvement story, and Category 5 leverages narrative strength with now-feasible technical ambition. **Category 1** should receive the least development time unless the team has surplus bandwidth or a breakthrough differentiation idea.

**Suggested team allocation (if 4 people, 2 weeks):**
- Person A: Category 2 lead (week 1) → Category 5 support (week 2)
- Person B: Category 3 lead (full 2 weeks — largest deliverable set)
- Person C: Category 4 lead (week 1) → Category 1 lead (week 2)
- Person D: Category 5 lead (full 2 weeks — most from-scratch work)
- Shared: Demo scripts, presentations, responsible AI docs (final 2-3 days)

### Cross-Category Synergies

- **LLM integration pattern:** Categories 1, 2, 3, and 5 all use GPT-4o/Claude for text generation. Build ONE reusable LLM wrapper (API key management, error handling, response parsing, retry logic) and share across all categories.
- **Streamlit dashboard pattern:** Categories 1, 2, 3, and 4 all use Streamlit for the frontend. Create a shared template with consistent styling (header, sidebar, color scheme, custom CSS) and fork it per category.
- **Responsible AI module:** All 5 categories require responsible AI documentation. Create a shared template with common elements (data consent, bias audit, transparency statement, limitations disclosure) and customize per category.
- **Demo script structure:** All demos are 5 minutes. Create a shared template: Problem (30s) → Solution (60s) → Live Demo (2min) → Impact (30s) → Responsible AI (30s) → Q&A readiness.
- **Testing infrastructure:** With 2 weeks, build proper test scenarios for each category. Pre-run all demo flows at least 3 times before demo day.

### Shared Technical Infrastructure

| Component | Tool | Used By |
|---|---|---|
| LLM API wrapper | OpenAI Python SDK (GPT-4o-mini default, GPT-4o for quality) | All categories |
| Frontend framework | Streamlit 1.x with shared custom theme | Categories 1, 2, 3, 4 |
| Data processing | Pandas + NumPy | Categories 3, 4 |
| Visualization | Plotly (interactive) + Matplotlib (static) | Categories 1, 3, 4, 5 |
| Deployment | Streamlit Cloud or HuggingFace Spaces | All categories |
| Version control | GitHub repo with category branches | All categories |
| Azure services | Custom Vision (Cat 5), OpenAI Service (Cat 1, 5) | Categories 1, 5 |

### Research Agent Dispatch Instructions

---

#### Category 1 (Avanade Wellbeing) Research Agent Brief
- **Primary Focus:** Define the wellbeing score engine and build a polished manager heatmap dashboard
- **Key Research Questions:**
  1. What are the top 5 evidence-based non-clinical interventions for tech worker burnout? (need citations)
  2. What is the exact data schema of Microsoft Viva Insights' wellbeing metrics?
  3. What are leading competitor products (BetterUp, Calm Business, Viva Insights)? What gaps exist for mid-market companies?
  4. What does the APA say about appropriate vs. inappropriate uses of AI in workplace wellbeing?
- **Must-Have MVP Features:**
  - Landing page with explicit non-clinical positioning and onboarding consent flow
  - Simulated work pattern data input (JSON or form-based)
  - Rules-based wellbeing score across 4 dimensions with LLM-generated narrative explanation
  - Personalized micro-nudges based on score patterns
  - Manager anonymized heatmap view with drill-down (the demo moment)
  - Professional resource escalation links
  - "About this score" transparency panel
- **Sponsor Alignment Notes:** Emphasize Microsoft ecosystem — Azure OpenAI, Power BI aesthetic, Viva Insights data model compatibility. Name-drop Avanade's enterprise consulting practice.
- **Red Lines:**
  - Do NOT claim to diagnose or treat mental health conditions
  - Do NOT propose training ML models — all AI is LLM API calls + rules-based scoring
  - Do NOT build real Microsoft API integrations — use simulated data with correct schema
  - Do NOT build a chatbot as the primary interface — dashboard-first
- **Suggested PRD Structure:** Problem Statement → Target User Persona → Wellbeing Score Definition (formula) → System Architecture → MVP Feature Spec → UI Wireframes → Onboarding Flow → Responsible AI Framework → Demo Script
- **Time Budget (2 weeks):** Days 1-2: research + scoring engine design | Days 3-7: core development (scoring, nudges, dashboard) | Days 8-10: manager heatmap + UI polish | Days 11-12: testing + demo prep | Days 13-14: presentation + buffer

---

#### Category 2 (ISACA Cyber Safety Coach) Research Agent Brief
- **Primary Focus:** Build a full-featured classification + education platform with all stretch goals included
- **Key Research Questions:**
  1. What are PhishTank API and Google Safe Browsing API response times and rate limits? Test both.
  2. What are the top 15 phishing indicators from the 2025 Verizon DBIR?
  3. What reading level do ISACA's consumer-facing publications target?
  4. What existing consumer phishing detection tools exist? What do they NOT do?
  5. What UX patterns work best for security tools aimed at non-experts?
- **Must-Have MVP Features (all stretch goals promoted):**
  - Text input field (email body, URL, or SMS text)
  - LLM classification → Risk label (Safe/Suspicious/High Risk) with color coding
  - Top 3 plain-language reasons + action checklist
  - Micro-lesson (30-second educational tip per threat type)
  - PII redaction toggle with before/after preview
  - Spanish language toggle (GPT-4o native translation)
  - Screenshot OCR pipeline (GPT-4o Vision)
  - URL reputation check (PhishTank + Google Safe Browsing) with hard override logic
  - Confidence score + uncertainty signaling
  - "Was this helpful?" feedback button
  - Lightweight report export (shareable PDF/text summary)
  - 10+ curated demo scenarios covering diverse threat types
  - Polished, branded UI with custom CSS
- **Sponsor Alignment Notes:** Reference NIST Cybersecurity Framework. Use "Zero Trust" language. Position as "grassroots cyber literacy platform." Mention CPP pilot deployment potential.
- **Red Lines:**
  - Do NOT store user inputs — privacy-by-design is non-negotiable
  - Do NOT explain how to craft phishing attacks
  - URL reputation must hard-override LLM classification when flagged
  - Do NOT sacrifice UI polish for feature count — quality over quantity
- **Suggested PRD Structure:** Problem Statement (DBIR statistics) → User Persona ("Maria") → System Architecture (LLM + rules + API layers) → Classification Logic with Conflict Resolution → Micro-Lesson Content Library (10+ entries) → Privacy Architecture → OCR Pipeline → Multi-Language Strategy → UI Wireframes → Demo Script with 10 Scenarios → Responsible AI Framework
- **Time Budget (2 weeks):** Days 1-2: research + API validation + prompt engineering | Days 3-6: core classification + UI framework | Days 7-9: micro-lessons, OCR, redaction, Spanish | Days 10-11: demo scenarios + UI polish | Days 12-13: testing (all scenarios) | Day 14: presentation prep

---

#### Category 3 (IA West Smart Match CRM) Research Agent Brief
- **Primary Focus:** Build the full four-module CRM with matching engine, discovery pipeline, and the critical written deliverables
- **Key Research Questions:**
  1. Do the CSVs load cleanly? Column names, data types, missing values? Build a data quality report.
  2. What 5+ university event pages in the Portland-to-San Diego corridor have scrapable listings?
  3. What is IA West's membership value proposition? (Check website + challenge intro deck)
  4. Does semantic matching with OpenAI embeddings outperform keyword overlap on this dataset?
  5. What are realistic conversion rates for professional-association membership funnels?
- **Must-Have MVP Features:**
  - Load speaker profiles and event data from CSVs
  - Vector embedding-based matching (OpenAI text-embedding-3-small + cosine similarity)
  - Match score computation with weight breakdown display
  - Top 3 recommended matches per event with natural language explanation cards
  - LLM-generated outreach email for top matches
  - Automated discovery: scrape 5+ university event pages with LLM extraction
  - Pipeline tracker with funnel visualization (Plotly Sankey)
  - Growth Strategy document (2-3 pages)
  - Measurement Plan document (1 page with specific KPIs)
  - Responsible AI note (half page)
- **Sponsor Alignment Notes:** Use market research language — "conversion funnel," "panel matching," "response optimization." Frame as "research-grade recommendation engine." Reference A/B testing for weight tuning.
- **Red Lines:**
  - Do NOT skip the Growth Strategy and Measurement Plan — 40% of judging score
  - Do NOT scrape without caching and fallback strategy
  - Do NOT use a black-box matching approach — explainability is explicitly required
- **Suggested PRD Structure:** Challenge Requirements → Data Dictionary → Matching Algorithm Spec → Module 1-4 Feature Specs → Web Scraping Architecture → Growth Strategy (2-3 pages) → Measurement Plan (1 page) → Pipeline Visualization Design → UI Wireframes → Demo Script → Responsible AI Framework
- **Time Budget (2 weeks):** Days 1-2: data exploration + matching algorithm design + embedding tests | Days 3-6: matching engine + UI | Days 7-8: web scraping pipeline (5 universities) | Days 9-10: email generation + pipeline tracker | Days 11-12: Growth Strategy + Measurement Plan writing | Day 13: testing | Day 14: presentation prep

---

#### Category 4 (Aytm Simulated Research) Research Agent Brief
- **Primary Focus:** Run existing prototype, deliver substantive improvements on Stages 2+4+5, and build compelling ground truth comparison
- **Key Research Questions:**
  1. Does the prototype run without errors? Document setup, bugs, code quality.
  2. What are the 5 "funhouse mirror" distortions from Peng et al. (2026)?
  3. What does Aytm Skipper produce for a similar brief? (Review public demos)
  4. What are the specific findings in the real data images?
  5. What does the STAMP paper say about cross-model adjudication?
  6. What is the API cost for 200+ respondents across 2 LLMs?
- **Must-Have MVP Features:**
  - Running, verified prototype with sample data
  - Stage 2 improvement: multi-turn interview probing + expanded persona diversity (cultural dimensions, renter vs. owner)
  - Stage 4 improvement: scale to 200+ respondents with cost tracking + Krippendorff's alpha for consistency
  - Stage 5 improvement: publication-quality charts with confidence intervals, effect sizes, and cross-model divergence visualization
  - Ground truth comparison: side-by-side synthetic vs. real data for 3+ findings with interpretation
  - Cross-model divergence dashboard (where GPT and Gemini agree/disagree, and business implications)
  - Tony Koo business recommendation (specific, actionable: "prioritize [X] positioning for [Y] segment")
  - "Before vs. After" comparison slides showing prototype improvement
- **Sponsor Alignment Notes:** Position as complementary to Aytm Skipper: "open-source academic sandbox." Reference STAMP paper and academic rigor. Lead with cost comparison ($0.08 vs. $12K-$24K).
- **Red Lines:**
  - Do NOT attempt all 6 stages — focus on Stages 2, 4, 5
  - Do NOT rewrite the codebase from scratch — improve incrementally
  - Do NOT skip ground truth comparison — most impressive demo element
  - Do NOT present synthetic data as real research — always label clearly
- **Suggested PRD Structure:** Existing Prototype Assessment → Improvement Plan (Stages 2, 4, 5) → Before/After Specification → Ground Truth Comparison Plan → Cross-Model Reliability Analysis → Krippendorff's Alpha Implementation → Business Recommendation Template → Demo Script → Responsible AI Statement
- **Time Budget (2 weeks):** Days 1-3: prototype assessment + STAMP paper study + ground truth analysis | Days 4-6: Stage 2 improvements (multi-turn, expanded personas) | Days 7-9: Stage 4 improvements (scale to 200+, consistency metrics) | Days 10-11: Stage 5 improvements (visualizations, confidence intervals) | Day 12: ground truth comparison + business recommendation | Day 13: before/after documentation | Day 14: presentation prep

---

#### Category 5 (Avanade Creative SDG — CropSense AI) Research Agent Brief
- **Primary Focus:** Build a working CV + LLM advisory + weather system with compelling SDG narrative
- **Key Research Questions:**
  1. Can Azure Custom Vision classify 5-7 crop diseases from PlantVillage with >90% accuracy?
  2. What existing smallholder AI tools exist (Plantix, DigiFarm, Hello Tractor)? Competitive gaps?
  3. What languages are most needed for agricultural advisory in sub-Saharan Africa and South Asia?
  4. What are the most recent FAO/World Bank statistics on smallholder farming and food insecurity?
  5. What does Microsoft's Planetary Computer offer for agricultural use cases?
  6. Can Open-Meteo API provide regional weather forecasts for sub-Saharan African locations?
- **Must-Have MVP Features:**
  - Crop disease classifier: upload leaf photo → disease label + confidence (Azure Custom Vision, >90% accuracy)
  - LLM-generated plain-language advisory per disease (actionable, contextual)
  - Multi-language output: English + Spanish + Swahili (test quality in all three)
  - Weather-aware advisory: disease + weather forecast → urgency-adjusted recommendation
  - SMS-ready format display (under 160 chars) in the web UI
  - SDG impact dashboard: visual showing SDG 2, 13, 10 with quantified claims and citations
  - "Consult local extension officer" escalation for low-confidence classifications
  - Competitive comparison slide (CropSense vs. Plantix vs. DigiFarm)
  - "Amina" persona narrative video or storyboard for demo opening
- **Sponsor Alignment Notes:** Maximum Microsoft visibility: Azure Custom Vision, Azure OpenAI GPT-4o, Planetary Computer reference. Tie to Microsoft's carbon-negative commitment. This should FEEL like a Microsoft demo.
- **Red Lines:**
  - Do NOT train a model from scratch — use Azure Custom Vision
  - Do NOT attempt price prediction for MVP
  - Do NOT overclaim accuracy — show confidence scores honestly
  - Limit to 3 AI systems (CV + LLM + weather). Cut anything beyond that.
  - Do NOT build Twilio/WhatsApp integration unless core features are complete and polished
- **Suggested PRD Structure:** Problem Statement (FAO statistics) → SDG Alignment Deep-Dive (3 SDGs) → User Persona ("Amina") → System Architecture → CV Component Spec → LLM Advisory Spec → Multi-Language Strategy → Weather Integration → SMS Format Design → MVP Feature Spec → UI Wireframes → Demo Script → Impact Quantification → Competitive Landscape → Responsible AI Framework
- **Time Budget (2 weeks):** Days 1-3: Azure Custom Vision setup + PlantVillage data curation + training | Days 4-6: LLM advisory system + multi-language testing | Days 7-8: weather API integration + urgency logic | Days 9-10: frontend (Streamlit with SDG dashboard) | Days 11-12: demo narrative + persona video/storyboard | Day 13: end-to-end testing | Day 14: presentation prep

---

*End of CTO Review. All 5 categories approved for research agent handoff with the revisions noted above. Research agents should treat the recommendations in this document as directives, not suggestions. With 2 weeks of preparation, the bar for quality is higher — judges will expect polished, well-tested prototypes with clear narratives, not rough hackathon sketches. Use the extra time to iterate, test, and rehearse.*
