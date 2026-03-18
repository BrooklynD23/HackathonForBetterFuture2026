---
doc_role: canonical
authority_scope:
- category.4.feature_detail
canonical_upstreams:
- Category 4 - Aytm x Neo Smart Living/docs/SPRINT_PLAN.md
- MASTER_SPRINT_PLAN.md
- STRATEGIC_REVIEW.md
last_reconciled: '2026-03-16'
managed_by: repo-governance
---

## Category 4: Simulated Market Research — AI-Powered Consumer Insights Engine
**Sponsor:** Aytm x Neo Smart Living | **CTO Tier:** 2 (Strong Contender) | **Verdict:** Approved with Revisions

> **Governance notice (repo-governance):** This document owns category feature-detail narrative. It must not override execution, staffing, milestone, or gating decisions from its canonical upstreams: `Category 4 - Aytm x Neo Smart Living/docs/SPRINT_PLAN.md`, `MASTER_SPRINT_PLAN.md`, `STRATEGIC_REVIEW.md`.

### Problem Statement

Traditional market research for niche consumer products costs $12,000-$24,000 for a single quantitative study (300-600 respondents) and $3,000-$9,000 for a qualitative phase (20-30 depth interviews), with 4-8 week turnaround times. For an early-stage startup like Neo Smart Living — selling a $23,000 prefab backyard structure (Tahoe Mini) to SoCal homeowners — this represents 52-143% of a typical seed-stage marketing budget spent before a single ad runs. The result: most startups skip rigorous research entirely, launching on founder intuition. This prototype demonstrates that dual-LLM synthetic respondent generation can produce directionally valid consumer insights for approximately $0.08 per full pipeline run (30 interviews + 60 survey responses), a cost reduction of 150,000x-300,000x compared to traditional methods. The open question is not whether this is cheaper, but whether it is reliable enough to inform real business decisions — and that is what ground truth validation answers.

### Proposed Solution

Build an improved open-source simulated market research pipeline that generates synthetic qualitative interviews and quantitative survey responses using dual-LLM cross-validation (GPT-4.1-mini + Gemini 2.5 Flash via OpenRouter). The system focuses on three pipeline stages: Stage 2 (simulated consumer interviews with multi-turn probe logic), Stage 4 (simulated survey respondents with Krippendorff's alpha intra-persona consistency), and Stage 5 (data analysis with ground truth comparison against real Tahoe Mini research data). The deliverable is a Streamlit dashboard that presents a "before vs. after" comparison of prototype improvements, a Tony Koo business recommendation backed by synthetic-vs-real validation, and a cost-per-insight tracker that makes the $0.08 vs. $12K-$24K story viscerally clear. The project is framed as OWNERSHIP of an end-to-end research methodology — not incremental iteration on someone else's code.

### Tech Stack

| Layer | Technology | Purpose | Free Tier? | Cost Estimate (2 weeks) |
|-------|-----------|---------|------------|------------------------|
| LLM (Primary) | GPT-4.1-mini via OpenRouter | Synthetic persona response generation, interview simulation | No (pay-per-token) | ~$0.03-$0.05 per full run |
| LLM (Cross-validation) | Gemini 2.5 Flash via OpenRouter | Dual-LLM reliability check, divergence detection | No (pay-per-token) | ~$0.03-$0.05 per full run |
| Sentiment Analysis | VADER (nltk) | Interview sentiment scoring | Yes (fully free, local) | $0.00 |
| Topic Modeling | scikit-learn LDA + gensim | Emergent theme discovery from interviews | Yes (fully free, local) | $0.00 |
| Statistical Testing | scipy (Mann-Whitney U, Krippendorff's alpha) | Cross-model divergence detection, intra-persona consistency | Yes (fully free, local) | $0.00 |
| Dashboard | Streamlit | Interactive qual + quant visualization | Yes (Community Cloud) | $0.00 |
| Visualization | Plotly + Seaborn + Matplotlib | Publication-ready charts, radar plots, heatmaps | Yes (fully free, local) | $0.00 |
| Token Tracking | tiktoken | Cost-per-insight calculation and display | Yes (fully free, local) | $0.00 |
| Hosting | Streamlit Community Cloud | Demo deployment (public GitHub repo required) | Yes (unlimited apps, resource-limited) | $0.00 |
| Version Control | GitHub | Code repository, CI/CD for Streamlit deploy | Yes (free for public repos) | $0.00 |
| **Total** | | | | **$0.50-$2.00** (5-20 full pipeline runs during development) |

### API & Service Pricing Breakdown

**OpenRouter Pricing (March 2026, 5.5% platform fee included):**

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Source |
|-------|----------------------|------------------------|--------|
| GPT-4.1-mini (openai/gpt-4.1-mini) | $0.12 | $0.48 | [OpenRouter Models](https://openrouter.ai/models) |
| Gemini 2.5 Flash (google/gemini-2.5-flash) | $0.30 | $2.50 | [OpenRouter Gemini 2.5 Flash](https://openrouter.ai/google/gemini-2.5-flash) |

**Direct API Pricing Comparison (March 2026):**

| Provider | Model | Input (per 1M tokens) | Output (per 1M tokens) | Source |
|----------|-------|----------------------|------------------------|--------|
| OpenAI Direct | GPT-4o-mini | $0.15 | $0.60 | [OpenAI Pricing](https://openai.com/api/pricing/) |
| Google Direct | Gemini 2.5 Flash | $0.30 | $2.50 | [Google AI Pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| OpenRouter | GPT-4.1-mini | $0.12 | $0.48 | [OpenRouter Pricing](https://openrouter.ai/pricing) |
| OpenRouter | Gemini 2.5 Flash | $0.30 | $2.50 | [OpenRouter Pricing](https://openrouter.ai/pricing) |

**Cost Per Synthetic Respondent Calculation:**

Each synthetic survey respondent requires approximately:
- System prompt (persona + psychographic): ~800 tokens input
- Survey instrument (35 questions): ~2,500 tokens input
- Response (JSON with all answers): ~600 tokens output
- Total per respondent: ~3,300 input tokens + ~600 output tokens

| Component | GPT-4.1-mini Cost | Gemini 2.5 Flash Cost |
|-----------|------------------|----------------------|
| 1 respondent (input) | 3,300 x $0.00000012 = $0.000396 | 3,300 x $0.00000030 = $0.000990 |
| 1 respondent (output) | 600 x $0.00000048 = $0.000288 | 600 x $0.0000025 = $0.001500 |
| **1 respondent total** | **$0.000684** | **$0.002490** |
| 30 respondents (one model) | $0.021 | $0.075 |
| 60 respondents (both models) | **$0.096** combined | |

Each synthetic interview (8 questions, ~1,500 token response) costs approximately $0.001-$0.004 per interview. Full qualitative phase (30 interviews): ~$0.03-$0.06.

**Total pipeline cost (30 interviews + 60 survey respondents + 30 emotion analyses): ~$0.08-$0.15**

**Comparison: $0.08 synthetic pipeline vs. $12,000-$24,000 traditional research = 150,000x-300,000x cost reduction**

**Aytm Skipper Platform Context:** [Aytm Skipper](https://aytm.com/platform/skipper) is a commercial AI research assistant that provides Skipper Draft (AI survey generation from briefs), Skipper Translate (multilingual survey adaptation), Skipper Explore (AI-powered finding summaries), and Skipper Autocode (automated open-end coding). The open-source prototype is positioned as a complementary academic sandbox that teaches researchers how platforms like Skipper work under the hood — not as a competitor. This framing makes Aytm look good as the sponsor while demonstrating technical depth.

### Complexity Assessment

| Dimension | Score (1-5) | Justification |
|-----------|-------------|---------------|
| AI/ML Complexity | 3 | Dual-LLM prompting with persona grounding is well-understood; adding Krippendorff's alpha and multi-turn probes adds moderate complexity but uses established libraries (scipy, krippendorff). No model training required. |
| Data Requirements | 2 | All data is synthetically generated on-demand. Ground truth images are provided in the challenge materials. No external data collection or cleaning needed. |
| UI/UX Complexity | 3 | Existing Streamlit dashboards (2 apps, 13 tabs total) provide a strong foundation. Improvements focus on adding "before vs. after" panels and Tony Koo recommendation page — incremental, not greenfield. |
| Integration Complexity | 2 | Single API integration (OpenRouter) already built and working. No database, no auth, no third-party service orchestration. Pipeline is linear: personas --> LLM --> parse --> analyze --> display. |
| Demo Polish Required | 4 | The demo must tell a compelling story: cost comparison hook, ground truth validation moment, business recommendation payoff. Needs publication-ready charts and a clear narrative arc for the 5-minute presentation. |
| **Average** | **2.8** | Low-to-moderate complexity; the challenge is polish and storytelling, not technical risk. |

### 2-Week Implementation Timeline

| Milestone | Days | Deliverables |
|-----------|------|-------------|
| M1: Prototype Assessment + Research | 1-3 | Run existing prototype end-to-end and verify all outputs. Inventory ground truth images (real interview transcript, theme analysis, demographics, concept test results). Identify specific "before" metrics for each stage. Research Krippendorff's alpha implementation (krippendorff Python package). Document 3+ synthetic findings to validate against real data. Set up Streamlit Cloud deployment from GitHub. |
| M2: Stage 2 Improvements | 4-6 | Implement multi-turn probe logic in synthetic_interviews.py (follow-up questions triggered by keyword detection in initial answers). Expand persona diversity (add 10 personas with ethnic/cultural dimensions per challenge guidance). Improve interview_analysis.py with better LDA hyperparameters for short text. Create "before vs. after" interview quality comparison panel in interview_dashboard.py. |
| M3: Stage 4 Improvements | 7-9 | Add Krippendorff's alpha calculation for intra-persona consistency (run same persona 3x, measure agreement). Scale to 100+ respondents with cost tracking. Close the qual-quant loop: extract Stage 2 interview themes and use them to refine segment psychographic prompts in segments.py. Add cost-per-insight metric to output (tokens used, dollars spent, insights generated). |
| M4: Stage 5 + Ground Truth | 10-11 | Compare 3+ synthetic findings against real data from provided images (concept test rankings, demographic patterns, purchase interest distribution). Add confidence intervals and effect sizes to all statistical tests. Build Tony Koo business recommendation page: "Based on dual-LLM consensus, Neo Smart Living should prioritize [X] positioning for [Y] audience." Create divergence visualization showing where GPT and Gemini agree vs. disagree. |
| M5: Documentation + Demo | 12-14 | Write Responsible AI note (half page). Document all GenAI usage (prompts, tools, AI-generated components, human modifications). Build demo narrative: cost hook ($0.08 vs. $24K) --> methodology --> ground truth validation --> business recommendation --> open-source vision. Practice 5-minute presentation. Deploy final version to Streamlit Cloud. Polish all charts to publication quality. |

### Team Allocation

**3-Person Team:**
- **Lead Engineer / Pipeline Architect (1 person):** Owns Stage 2 multi-turn interview improvements and Stage 4 Krippendorff's alpha implementation. Manages OpenRouter API integration, token tracking, and cost-per-insight metrics. Responsible for code quality and the qual-quant loop closure.
- **Data Analyst / Visualization Specialist (1 person):** Owns Stage 5 data analysis improvements — confidence intervals, effect sizes, ground truth comparison. Builds Tony Koo recommendation page. Creates all publication-ready charts and the "before vs. after" comparison panels.
- **Demo Lead / Research Coordinator (1 person):** Owns the 5-minute demo narrative, Responsible AI note, and GenAI documentation. Researches Aytm Skipper for positioning context. Manages ground truth image comparison workflow. Handles Streamlit Cloud deployment and demo rehearsal.

**5-Person Team:**
- **Lead Engineer (1 person):** Stage 2 multi-turn probe logic, persona diversity expansion, and interview pipeline improvements. Code architecture decisions and PR reviews.
- **Backend / Statistical Engineer (1 person):** Stage 4 Krippendorff's alpha, respondent scaling to 200+, cost-per-insight tracking, and qual-quant loop closure between Stage 2 themes and Stage 4 segment definitions.
- **Data Analyst (1 person):** Stage 5 statistical improvements — confidence intervals, effect sizes, cross-model divergence interpretation. Ground truth comparison (3+ findings validated against real data images).
- **Frontend / Dashboard Developer (1 person):** Streamlit dashboard enhancements — "before vs. after" panels, Tony Koo recommendation page, divergence heatmaps, publication-ready chart polish, Streamlit Cloud deployment.
- **Demo Lead / Research Writer (1 person):** Demo narrative, Responsible AI note, GenAI documentation, Aytm Skipper positioning research, presentation rehearsal, and overall storytelling arc.

### Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM responses lack diversity (central tendency bias / "funhouse mirror" distortion) | Medium | High | Use temperature 0.8 (already set), add explicit personality variation prompts (already in prototype), implement Krippendorff's alpha to measure and report consistency. If alpha is too high (>0.9), it signals artificial uniformity — report this honestly as a limitation. |
| Ground truth comparison reveals significant synthetic-real divergence | Medium | Medium | This is actually a FEATURE, not a bug. Frame divergence as "here is where synthetic research needs real validation" — methodological honesty scores highly on the Responsible AI criterion. Prepare 2-3 talking points for each divergent finding. |
| OpenRouter API rate limits or downtime during demo | Low | High | Pre-generate all data and cache in output/ CSVs before demo day. Dashboard runs entirely on cached data with zero API calls. Include generate_test_data.py and generate_test_interviews.py as offline fallbacks. |
| Krippendorff's alpha implementation complexity exceeds timeline | Low | Medium | The krippendorff Python package provides a single-function implementation (krippendorff.alpha()). Fallback: use Fleiss' kappa or simple percent agreement, which are trivial to implement. The key is having ANY intra-persona consistency metric, not a specific one. |
| Streamlit Cloud resource limits cause dashboard lag during demo | Medium | Medium | Optimize data loading with @st.cache_data (already used). Reduce chart rendering complexity. Test on Streamlit Cloud 48 hours before demo. Fallback: run locally on presenter's laptop with `streamlit run dashboard.py`. |
| Scope creep into Stages 1, 3, or 6 dilutes focus | Medium | High | CTO directive is explicit: Stages 2, 4, 5 ONLY. Post the directive visibly in the team workspace. Any Stage 1/3/6 work requires team lead approval and must demonstrate direct value to the three focus stages. |

### Win Probability Assessment
- **CTO Tier:** 2 (Strong Contender)
- **Independent Analysis:** This category has the strongest existing codebase advantage of any hackathon category — a fully functional Python pipeline with 13 files, 2 Streamlit dashboards (13 tabs), pre-generated sample data, and comprehensive documentation. The 48-hour clock effectively starts at hour 20+ because the prototype already runs. The dual-LLM reliability methodology (STAMP) and ground truth validation angle give academic credibility that most hackathon projects lack. The $0.08 vs. $24K cost comparison is a memorable opening hook. The primary risk is that the improvements feel incremental rather than transformative — the team must frame this as OWNERSHIP of a methodology, not just bug fixes on someone else's code.
- **Demo Moment:** Open with the cost comparison: "We just ran a complete market research study for Neo Smart Living. The traditional version costs $24,000 and takes 6 weeks. Ours costs 8 cents and takes 3 minutes." Then show the ground truth comparison: "Here are the real research results. Here are ours. They agree on [X], they disagree on [Y], and here is exactly why that matters for Tony Koo's next product launch decision." Close with the Tony Koo recommendation: a single slide that says "Neo Smart Living should lead with the [Adventure/Home Office] positioning for [segment], validated by dual-LLM consensus and ground truth comparison."
- **Overall Win Probability:** Medium-High (25-65%). The existing codebase provides a massive head start, the methodology is academically grounded, and the sponsor alignment is strong (Aytm benefits from open-source research tooling that complements Skipper). The main competition risk is a team that builds something more visually spectacular from scratch in a different category. Executing on ground truth comparison and the Tony Koo recommendation will be the differentiators.

### Existing Assets Inventory

| File | Purpose | Lines of Code | Head Start Estimate |
|------|---------|---------------|-------------------|
| `prototype/synthetic_interviews.py` | Generates 30 depth interviews via dual-LLM (GPT-4.1-mini + Gemini 2.5 Flash) | ~180 | 4 hours saved |
| `prototype/interview_personas.py` | 30 diverse SoCal homeowner personas with demographics and lifestyle notes | ~250 | 3 hours saved |
| `prototype/interview_analysis.py` | VADER sentiment + LDA topic modeling + emotional tone classification | ~200 | 4 hours saved |
| `prototype/interview_dashboard.py` | 6-tab Streamlit dashboard for qualitative analysis | ~350 | 6 hours saved |
| `prototype/synthetic_respondents.py` | Generates 60 survey responses via dual-LLM with JSON validation | ~337 | 5 hours saved |
| `prototype/segments.py` | 5 market segment definitions with psychographic narratives | ~150 | 2 hours saved |
| `prototype/analytics.py` | Shared analytics: descriptive stats, Mann-Whitney U, effect sizes | ~200 | 3 hours saved |
| `prototype/dashboard.py` | 7-tab Streamlit dashboard for quantitative analysis | ~400 | 6 hours saved |
| `prototype/report.py` | Static report generator: 4 CSVs + 5 PNG charts | ~200 | 3 hours saved |
| `prototype/generate_test_data.py` | Offline test data generator (no API needed) | ~100 | 1 hour saved |
| `prototype/generate_test_interviews.py` | Offline test interview generator (no API needed) | ~100 | 1 hour saved |
| `prototype/requirements.txt` | Dependency manifest (pandas, scipy, streamlit, gensim, nltk) | 9 | 0.5 hours saved |
| `prototype/Input/` | Survey instruments (high priority + high+medium priority markdown) | 2 files | 2 hours saved |
| `prototype/output/` | Pre-generated sample data (CSVs, JSON, charts) | 10 files | 2 hours saved |
| Ground truth images | Real interview transcript, theme analysis, demographics, concept test | 4 PNG files | 3 hours saved (no need to source validation data) |
| Challenge documents | Full spec, intro deck, background PDF, STAMP paper, survey PDF | 6 files | 4 hours saved (research already done) |
| **Total** | | **~2,500+ lines** | **~49.5 hours saved** |

The existing prototype provides approximately 49.5 hours of development head start. For a 48-hour hackathon, this means the team can spend nearly 100% of its time on improvements, polish, and demo preparation rather than scaffolding.

### Responsible AI Considerations

**Synthetic Data Transparency:** All synthetic responses must be clearly labeled as AI-generated in every dashboard view, CSV export, and presentation slide. The system must never present synthetic data as real human responses. Every chart title includes "(Synthetic)" and every data download includes a header row stating "Generated by LLM — not real human data."

**Known Distortions (Peng et al., 2026 — "Funhouse Mirror" Effects):** LLM-generated synthetic respondents exhibit five systematic distortions: (1) social desirability bias (responses skew toward socially acceptable answers), (2) central tendency compression (Likert responses cluster around 3-4, avoiding extremes), (3) coherence bias (personas are more internally consistent than real humans), (4) recency bias (LLM training data overweights recent cultural trends), and (5) demographic stereotyping (personas may reinforce rather than challenge demographic assumptions). The prototype's dual-LLM design partially mitigates distortions 1-3 by surfacing divergence, but distortions 4-5 require real human validation.

**When Real Research is Required:** Synthetic research is appropriate for early-stage exploration, hypothesis generation, and survey pretesting. It is NOT appropriate for final go/no-go product launch decisions, regulatory submissions, or claims about real consumer preferences. The Tony Koo recommendation must be framed as "directional guidance warranting real-world validation" — not as a definitive market mandate.

**Ground Truth Obligation:** The prototype includes 4 real research images as validation benchmarks. Any finding that diverges significantly from ground truth must be flagged with a visible warning, not hidden or explained away. Honest reporting of synthetic-real divergence is a feature of responsible methodology, not a failure.

**No PII Risk:** All personas are fully synthetic. No real consumer data is collected, stored, or processed. The real research images used for ground truth comparison contain only aggregate statistics, not individual-level data.
