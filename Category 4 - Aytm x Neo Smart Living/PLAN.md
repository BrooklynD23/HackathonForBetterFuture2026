# Category 4 — Aytm × Neo Smart Living: Open-Source Simulated Market Research
**Sponsors:** Aytm (insights tech) + Neo Smart Living (prefab homes) | **Event:** CPP AI Hackathon | April 16, 2026

---

## 🎯 Challenge Prompt

> *"Build toward an open-source simulated market research ecosystem that enables students and practitioners to simulate qualitative interviews and quantitative survey responses using LLMs, and validate outputs with cross-model reliability checks."*

**Live business case:** Neo Smart Living's **Tahoe Mini** — a ~117 sq ft prefab backyard structure at ~$23,000, targeting SoCal homeowners as a home office, guest suite, STR, wellness studio, or adventure basecamp.

---

## 🌟 Why This Category Is Special

This is the most **technically rich and academically grounded** category in the hackathon. It comes with:
- A **working prototype codebase** (Python, Streamlit) already built
- **Real survey data and qualitative insights** from actual research
- **Academic paper references** grounding the methodology
- A **live client (Tony Koo, CPP alumnus)** who can use the findings

The challenge is NOT to build from scratch — it's to **improve, extend, and package** an existing proof-of-concept into a reusable open-source tool.

---

## 📦 Deliverable Requirements

All deliverables must include:
1. **Working code or prototype** — Runnable Python scripts, Jupyter notebooks, or Streamlit apps
2. **Responsible AI note** (half page) — Synthetic data transparency, limitations, and when real research is required
3. **GenAI documentation** — Tools used, prompts employed, AI-generated components, human modifications

Participants **choose one or more of the six pipeline stages** to contribute to. Deep work on one stage is valued equally to breadth across all six.

---

## 🏆 Judging Criteria (50 Points)

| Criterion | Description |
|---|---|
| **Technical Quality** | Does the code run? Are the improvements substantive and well-implemented? |
| **Methodological Rigor** | Are the improvements grounded in the research papers provided? |
| **Business Relevance** | Would Tony Koo find actionable insights for the Tahoe Mini? |
| **Open-Source Value** | Is this reusable beyond the Neo Smart Living case? |
| **Responsible AI** | Are synthetic data limitations honestly communicated? |
| **Storytelling** | Is the 5-minute demo narrative clear and compelling? |

---

## 🔬 The Six Pipeline Stages

### Stage 1: Client Discovery Interview
**What it is:** Configure an LLM as a digital twin of Neo Smart Living CEO Tony Koo, enabling practice discovery interviews.

**Baseline:** The `Customized_GPT_for_Learning_Business_Case.pdf` provides the instruction template for a Tony Koo digital twin.

**Improvement opportunities:**
- Richer persona grounding (more detailed background, product specs, competitive landscape)
- Multi-turn follow-up handling (the twin should respond naturally to probing questions)
- Framework for comparing simulated vs. real client answers
- **Generalize** the template so it works for any client (not just Tony Koo)

**Quick win idea:** Build a simple Streamlit chat interface where you can interview the Tony Koo digital twin and compare responses to ground truth from the business case documents.

---

### Stage 2: Simulated Consumer Interviews (HIGH PRIORITY — Recommended Focus)
**What it is:** LLM role-plays as diverse SoCal homeowner personas to surface unmet needs and language patterns for Tahoe Mini.

**Baseline code available:**
- `prototype/interview_personas.py` — 30 persona definitions
- `prototype/synthetic_interviews.py` — Generates interviews (GPT-4.1-mini + Gemini 2.5 Flash)
- `prototype/interview_analysis.py` — VADER sentiment + LDA thematic + emotional tone
- `prototype/interview_dashboard.py` — 6-tab Streamlit dashboard

**Interview guide (8 questions):**
1. Describe your backyard and how you currently use it
2. What unmet needs do you have around your outdoor/backyard space?
3. Describe your ideal lifestyle fantasy for your backyard
4. Reaction to the Tahoe Mini concept ($23K, 117 sqft, one-day install)
5. What barriers would prevent you from purchasing?
6. How would you discover a product like this?
7. What use case appeals most? (home office / guest suite / wellness / STR / adventure)
8. What would make it a must-have vs. nice-to-have?

**Improvement opportunities:**
- Multi-turn probe logic (follow-up questions based on initial answers)
- Persona diversity expansion (ethnic/cultural dimensions, renter vs. owner, urban vs. suburban)
- Segment discovery validation (cluster analysis vs. name-matching)
- Better qual-to-quant handoff (interview themes → survey question generation)

---

### Stage 3: AI-Assisted Survey Design
**What it is:** Translate qualitative findings into a structured ~35-item survey instrument.

**Benchmark:** Compare against **Aytm's Skipper platform** (aytm.com/skipper) — the commercial standard.

**Baseline:** `Neo Smart Living — Tahoe Mini Survey (High + Medium Priority)` covers:
- Screening questions (SoCal homeowner)
- Category baseline (backyard usage, interest in prefab)
- Product stimulus (Tahoe Mini concept)
- Purchase interest (RQ5-RQ8)
- Intended use cases and barriers
- Positioning concept tests (5 concepts)
- Value drivers and sponsorship
- Demographics and attention checks

**Improvement opportunities:**
- AI-assisted question generation FROM interview themes (Stage 2 → Stage 3 handoff)
- Response scale optimization and skip logic suggestions
- Survey pretest simulation (synthetic respondents flag confusing questions)
- Side-by-side comparison with Skipper's AI survey generation outputs

---

### Stage 4: Simulated Survey Respondents
**What it is:** Generate synthetic survey responses from segment-based personas using dual-LLM design (STAMP methodology).

**Five market segments:**
1. Active Adventurer — outdoor enthusiast, values adventure lifestyle
2. Budget-Conscious DIYer — price-sensitive, self-sufficient, practical
3. Property Maximizer — investment-oriented, STR potential, ROI focus
4. Remote Professional — WFH needs, home office priority, tech-forward
5. Wellness Seeker — mindfulness, retreats, personal sanctuary

**Baseline code:**
- `prototype/segments.py` — 5 segment definitions
- `prototype/synthetic_respondents.py` — 60 responses (5 segments × 2 LLMs × 6 each)
- Cross-model reliability: Mann-Whitney U test (p < 0.05 = flag for divergence)

**Improvement opportunities:**
- Close the qual-quant loop (use Stage 2 themes to refine segment definitions)
- Richer persona backstories → more realistic response patterns
- Scale to 200+ respondents; add cost-per-insight tracking
- Intra-persona consistency measurement (Krippendorff's alpha)

---

### Stage 5: Data Analysis (HIGH PRIORITY — Business Impact)
**What it is:** Answer specific research questions from the simulated survey data.

**Key research questions (from survey):**
- RQ5: Do remote workers show higher purchase interest than non-remote?
- RQ6: Does income predict purchase willingness?
- RQ7: Do age groups differ in intended use (home office vs. STR vs. wellness)?
- RQ8: Does outdoor recreation frequency predict purchase interest?
- RQ9: Which positioning concept wins? (Home Office / Guest Suite / Wellness / Adventure / Simplicity)
- RQ11: Does outdoor club membership predict concept preference?
- RQ12: Does the Adventure concept appeal more to high outdoor activity users?

**Baseline:** 6-tab Streamlit quantitative dashboard — Overview, Purchase Interest, Use Case & Barriers, Concept Test, Value Drivers & Sponsorship, Model Comparison

**Improvement opportunities:**
- Confidence intervals and effect sizes (not just p-values)
- Cross-model divergence interpretation (which findings to trust vs. validate with real data)
- Better visualization quality (publication-ready charts)
- Actionable framing: "What should Tony Koo do next?"

---

### Stage 6: Insights Presentation
**What it is:** Synthesize findings into a business presentation for Neo Smart Living.

**Suggested structure:**
1. The problem — why simulated research matters (cost $12K-$24K → vs. ~$0.10)
2. The method — qual-to-quant pipeline walkthrough
3. Key findings — top 3-5 actionable insights for Tahoe Mini positioning
4. Confidence assessment — where do LLMs agree vs. diverge?
5. Recommendations — what should Neo Smart Living do with real research next?
6. Open-source vision — how to package this for the broader research community

---

## 💡 Winning Concept Strategy

### Recommended Focus: Stages 2 + 4 + 5 (Full Qual-Quant Loop)

**Why this combination wins:**
- Stage 2 gives you emotionally rich, persona-grounded interviews
- Stage 4 generates quantitative data grounded in Stage 2 themes (closing the loop)
- Stage 5 delivers actionable business insights that Tony Koo can actually use
- The **dual-LLM reliability check** (GPT-4o-mini + Gemini 2.0 Flash) is a technical differentiator that judges will recognize as methodologically sophisticated

### Methodological Grounding (Use These Papers!)
Reference these in your presentation — it signals serious academic rigor:
- **Toubia et al. (2025)** — Twin-2K-500 dataset showing LLMs can generate coherent synthetic profiles
- **Peng et al. (2026)** — "Digital Twins as Funhouse Mirrors" — 5 systematic distortions to watch for
- **Arora, Chakraborty & Nishimura (2024)** — AI-Human Hybrids: LLMs work best as *collaborators*, not replacements
- **Lin (under review)** — STAMP: dual-LLM coding process (the theoretical basis for cross-model reliability)

### AI Types to Incorporate
- **LLM (GPT-4o-mini + Gemini 2.0 Flash)** — persona-grounded response generation (dual-LLM for reliability)
- **Topic modeling (LDA)** — emergent theme discovery from qualitative interviews
- **Sentiment analysis (VADER)** — emotion scoring without API cost
- **Statistical testing (Mann-Whitney U)** — cross-model divergence detection
- **Embedding-based clustering** — segment discovery from interview features

### Aytm Ecosystem Angle
Position the project as complementary to (not competing with) **Aytm Skipper**:
- "This open-source pipeline is the academic sandbox that teaches researchers *how* Skipper works under the hood"
- Demonstrate a side-by-side: "Here's what our open-source tool generated vs. what Skipper would produce on the same brief"
- This framing makes Aytm look good while showcasing your technical depth

---

## 🔬 Research Directions for the Agent

### Key Questions to Investigate
1. What are the five "funhouse mirror" distortions identified by Peng et al. (2026)? How can the prototype mitigate them?
2. How does Aytm Skipper generate survey questions from a brief? (Review their public demos at aytm.com/skipper)
3. What is Krippendorff's alpha and how should it be implemented for intra-persona consistency measurement?
4. What are the best LDA hyperparameter settings for short-text qualitative interview data?
5. What are the current OpenRouter API pricing structures for GPT-4.1-mini and Gemini 2.5 Flash?
6. How does the STAMP methodology (Lin, under review) implement dual-LLM adjudication for text classification?

### Real Data Available in This Category
- `qualitative interview insights_full transcript.png` — actual interview transcript from real research
- `qualitative interview insights_theme analysis.png` — real thematic analysis output
- `quantiative_survey_demographics.png` — actual demographic breakdown
- `quantiative_survey_positining concept.png` — real concept test results (ground truth to validate against!)
- `Neo Smart Living — Tahoe Mini Survey.pdf` — full survey instrument
- `STAMP_JM_proof.pdf` — Lin's STAMP methodology paper
- `Neo Smart Living Background.pdf` — company background
- `prototype/` — full working Python codebase

### Quick Start for Agent
```bash
cd prototype/
pip install -r requirements.txt
streamlit run dashboard.py   # works immediately with sample data (no API key)

# For full run (~$0.05-$0.10):
export OPENROUTER_API_KEY=your_key
python synthetic_interviews.py
python synthetic_respondents.py
```

---

## 🎨 Prototype MVP Scope (48 hours)

**Must have:**
- Run the existing prototype with sample data — verify it works
- Implement ONE substantive improvement (e.g., multi-turn interviews OR richer segment personas OR better analysis visualizations)
- Demonstrate cross-model reliability check (Mann-Whitney U results with interpretation)
- Compare at least ONE synthetic finding against the real data provided (images in folder)

**Nice to have:**
- New segment definitions informed by the real interview transcript
- Dual-LLM disagreement visualization ("These two models disagree on this question — here's why that matters")
- Business recommendation slide for Tony Koo based on findings

---

## 🧠 Differentiation Angles (How to Win)

1. **Ground truth validation** — compare synthetic outputs against the real data images provided; this shows methodological honesty that judges will respect
2. **Dual-LLM reliability as a feature** — make divergence visible and *explain what it means for business decisions*
3. **Cost comparison** — show "$0.08 for 60 synthetic respondents vs. $12,000-$24,000 for real niche research" in the first minute of the demo
4. **Actionable Tony Koo output** — end with "Based on this simulation, Neo Smart Living should prioritize the Adventure positioning concept for outdoor community sponsorship" — specific, usable, memorable
5. **Open-source framing** — this aligns with NSF PESOSE vision; mention it; judges from academia and industry both respond well to this

---

## 📋 Responsible AI Checklist

- [ ] Synthetic data clearly labeled — never presented as real human responses
- [ ] Confidence calibration — which findings are robust (LLMs agree) vs. uncertain (LLMs diverge)?
- [ ] Limitations section — what the simulation CANNOT tell you (real human nuance, cultural context)
- [ ] When to use real research — clear recommendation on when synthetic insights must be validated
- [ ] No PII — all personas are fully synthetic, no real consumer data used
- [ ] Open-source attribution — all code, prompts, and methods documented for reproducibility

---

## 🏗️ Technical Stack Recommendation

| Component | Recommended Tool |
|---|---|
| Interview generation | OpenRouter API (GPT-4.1-mini + Gemini 2.5 Flash) |
| Sentiment analysis | VADER (free, no API) |
| Topic modeling | scikit-learn LDA |
| Statistical testing | scipy (Mann-Whitney U, Krippendorff's alpha) |
| Dashboard | Streamlit (existing codebase) |
| Visualization | Plotly + Seaborn |
| Cost tracking | Token counting via tiktoken |

---

## 📎 Source Files Reference
- `prototype/` — Complete working Python codebase (start here)
- `Aytm_x_Neo_Smart_Living_Joint_Challenge.docx` — Full challenge specification
- `Aytm_x_Neo_Smart_Living_Challenge_Intro.pptx` — Sponsor intro deck
- `Neo Smart Living Background.pdf` — Company and product context
- `Customized_GPT_for_Learning_Business_Case.pdf` — Tony Koo digital twin instructions
- `Neo Smart Living — Tahoe Mini Survey.pdf` — Full survey instrument
- `STAMP_JM_proof.pdf` — Dual-LLM methodology paper
- `qualitative interview insights_full transcript.png` — Real interview data (ground truth)
- `qualitative interview insights_theme analysis.png` — Real thematic analysis (ground truth)
- `quantiative_survey_demographics.png` — Real demographics data (ground truth)
- `quantiative_survey_positining concept.png` — Real concept test results (ground truth)
- `NeoSmartLiving_Survey_Flyer.png` — Marketing material
