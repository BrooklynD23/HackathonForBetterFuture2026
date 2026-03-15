## Category 2: PhishGuard AI -- Cyber Safety Coach for Everyone
**Sponsor:** ISACA Orange County | **CTO Tier:** 1 (Highest Win Probability) | **Verdict:** Approved

### Problem Statement

Phishing remains the dominant initial attack vector for data breaches worldwide. According to the Verizon 2025 Data Breach Investigations Report (DBIR), which analyzed over 22,000 incidents and 12,195 confirmed breaches (its largest dataset ever), **16% of all breaches began with phishing**, and **the human element -- errors, social engineering, and misuse -- played a role in 60% of breaches**. Credential abuse accounted for 22% of breaches, often initiated through phishing. The median time for a user to fall for a phishing email is under 60 seconds. Yet the people most vulnerable -- students, families, part-time workers, and small community organizations -- have no accessible, jargon-free tool to evaluate suspicious messages in real time. The business impact is concrete: financial fraud (gift card scams, payment redirection), account takeover (school email, banking, social media), PII exposure, and downstream reputational harm. Existing consumer tools like Norton Genie and ScamAdviser address fragments of this problem but fail to educate users or explain *why* something is dangerous, leaving a critical gap between detection and literacy.

### Proposed Solution

PhishGuard AI is a conversational cyber safety coach that classifies suspicious emails, SMS messages, URLs, and screenshots as Safe, Suspicious, or High Risk -- and then explains *why* in plain, 6th-grade-level English (with a Spanish toggle). The system combines a fast rule-based pre-filter layer (regex patterns for urgency language, domain mismatches, credential requests) with an LLM reasoning engine (GPT-4o-mini) and external URL reputation APIs (Google Safe Browsing, PhishTank) to produce a tri-layer verdict. When the rule-based layer and LLM disagree, URL reputation APIs serve as the tiebreaker, and hard-override rules ensure that any URL flagged by reputation databases is always marked High Risk regardless of LLM output. Every analysis includes a confidence score with uncertainty signaling, a contextual action checklist, a 30-second micro-lesson on the detected threat type, automatic PII redaction before LLM processing, and a one-click exportable report. The tool is built on Streamlit for rapid prototyping and deployed on Streamlit Community Cloud, requiring zero installation from end users.

### Tech Stack

| Layer | Technology | Purpose | Free Tier? | Cost Estimate (2 weeks) |
|-------|-----------|---------|------------|------------------------|
| Primary LLM | OpenAI GPT-4o-mini | Text classification, explanation generation, micro-lessons, Spanish translation | Yes (rate-limited) | ~$2-5 (est. 10K-30K requests at ~500 tokens avg) |
| Vision/OCR | OpenAI GPT-4o (Vision) | Screenshot text extraction and analysis | Yes (rate-limited) | ~$3-8 (est. 500-1K image analyses during dev + demo) |
| URL Reputation (Primary) | Google Safe Browsing API v4 | Real-time URL threat lookup; hard-override source | Yes (free, non-commercial) | $0 |
| URL Reputation (Secondary) | PhishTank API | Phishing URL verification against community database | Yes (free with API key) | $0 |
| PII Redaction | spaCy NER + regex rules | Auto-redact names, emails, phone numbers before LLM processing | Yes (open source) | $0 |
| Rule-Based Pre-Filter | Python (regex + heuristics) | Fast detection of urgency words, domain mismatches, credential asks | N/A (custom code) | $0 |
| Frontend | Streamlit | Rapid UI prototyping with color-coded risk badges, forms, tabs | Yes (open source) | $0 |
| Hosting | Streamlit Community Cloud | Free deployment, public access, no server management | Yes (3 free apps, 1GB resource limit) | $0 |
| Version Control | GitHub (public repo) | Required for Streamlit Cloud deployment | Yes | $0 |
| Styling/Polish | Streamlit components + custom CSS | Color-blind-safe risk colors, large text, accessible design | N/A | $0 |
| **Total** | | | | **~$5-13** |

### API & Service Pricing Breakdown

**OpenAI GPT-4o-mini** (as of March 2026):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- Estimated hackathon usage: ~15M input tokens, ~5M output tokens = ~$5.25 total
- Source: [OpenAI Pricing](https://openai.com/api/pricing/)

**OpenAI GPT-4o** (Vision/OCR, as of March 2026):
- Input: $2.50 per 1M tokens (images converted to tokens based on resolution)
- Output: $10.00 per 1M tokens
- Estimated hackathon usage: ~500 image analyses = ~$3-8 depending on image sizes
- Source: [OpenAI Pricing](https://openai.com/api/pricing/)

**Google Safe Browsing API v4:**
- Free for non-commercial use (hackathon qualifies)
- Default quota provided; increases available on request via Google Developer Console
- No per-query charges
- Source: [Google Safe Browsing Pricing](https://developers.google.com/safe-browsing/v4/pricing)

**PhishTank API:**
- Free with API key registration
- Rate-limited per hour (higher limits with valid API key)
- Downloadable database also available for offline lookups
- HTTP 509 returned if rate limit exceeded
- Source: [PhishTank API Info](https://phishtank.org/api_info.php)

**Streamlit Community Cloud:**
- Free tier: 3 apps, 1GB resource limit (memory + CPU + disk)
- Apps sleep after inactivity, restart on access
- Must link to public GitHub repo
- Source: [Streamlit Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/status)

**spaCy (en_core_web_sm model):**
- Fully open source, no API costs
- ~15MB model download, fits within Streamlit Cloud resource limits

### Complexity Assessment

| Dimension | Score (1-5) | Justification |
|-----------|-------------|---------------|
| AI/ML Complexity | 2 | Uses pre-trained LLM via API (no fine-tuning). Rule-based layer is standard regex. Prompt engineering is the main AI work. |
| Data Requirements | 1 | No training data needed. PhishTank and Safe Browsing provide lookup data. Demo scenarios are hand-crafted synthetic examples. |
| UI/UX Complexity | 3 | Streamlit accelerates development, but polished UX with color-coded badges, tabs for multiple input types, Spanish toggle, report export, and accessibility requires meaningful design effort. |
| Integration Complexity | 2 | Three external APIs (OpenAI, Google Safe Browsing, PhishTank) plus spaCy -- all well-documented with Python SDKs. Conflict resolution logic between layers adds modest complexity. |
| Demo Polish Required | 4 | ISACA judges prioritize storytelling, clarity, and user experience. Building 10+ realistic demo scenarios, ensuring smooth live demo flow, and nailing the "Maria gets a suspicious text" narrative requires significant polish investment. |
| **Average** | **2.4** | Low-to-moderate overall complexity. The challenge is in polish and UX execution, not technical difficulty. |

### 2-Week Implementation Timeline

| Milestone | Days | Deliverables |
|-----------|------|-------------|
| M1: Research & API Validation | 1-2 | OpenAI API key provisioned and tested. Google Safe Browsing and PhishTank API keys obtained and validated with sample queries. spaCy NER pipeline tested for PII redaction accuracy. Conflict resolution rules documented (LLM vs. rule-based vs. URL reputation). 10+ demo scenario scripts drafted (phishing email, smishing text, safe newsletter, ambiguous URL, credential harvesting page, gift card scam, fake shipping notification, social media impersonation, job scam, tech support scam). |
| M2: Core Classification + UI | 3-6 | Rule-based pre-filter engine (urgency detection, domain mismatch, credential ask patterns). LLM classification prompt with structured JSON output (risk level, confidence, reasons, actions, micro-lesson). Google Safe Browsing + PhishTank URL lookup integration. Conflict resolution: URL reputation hard-overrides LLM when URL is flagged; rule-based flags surface as additional evidence to LLM; when rule-based says High Risk but LLM says Safe, escalate to Suspicious with explanation. Streamlit UI with text input tab, URL input tab, risk badge display, reason cards, action checklist. Basic color-coded output (green/yellow/red, color-blind-safe palette). |
| M3: Advanced Features | 7-9 | Screenshot upload with GPT-4o Vision OCR extraction. PII redaction toggle (show before/after with spaCy NER + regex). Spanish language toggle (LLM re-generates explanation in Spanish). Confidence score display with uncertainty messaging ("I'm 85% confident, but here's how to verify"). Micro-lesson cards (30-second tips contextual to detected threat type). Report export (PDF or text summary user can forward to IT/admin). Prompt guardrails to prevent explaining how to craft phishing. |
| M4: Demo Scenarios + Polish | 10-11 | All 10+ demo scenarios loaded as clickable "Try This Example" cards. UI polish pass: large accessible text, consistent spacing, smooth transitions. Color-blind-safe verification (use blue/orange instead of green/red where needed). Demo flow script rehearsed end-to-end. Edge case handling: empty input, extremely long input, non-English input, URLs with redirects. "Was this helpful?" feedback button (narrative prop for ISACA judges). |
| M5: Testing + Presentation | 12-14 | End-to-end testing of all input types across all demo scenarios. Load testing on Streamlit Cloud (verify 1GB resource limit is not exceeded). 5-minute presentation script finalized with "Maria" narrative arc. Backup plan tested: pre-recorded demo video if live API fails. Final security review: verify no user inputs are stored, redaction works, no phishing crafting instructions leak. README and submission materials prepared. |

### Team Allocation

**3-Person Team:**
- **Person 1 -- Backend Lead (LLM + APIs):** Owns OpenAI prompt engineering, Google Safe Browsing and PhishTank integration, conflict resolution logic between rule-based/LLM/URL reputation layers, spaCy PII redaction pipeline, and GPT-4o Vision OCR. Primary debugger for API issues.
- **Person 2 -- Frontend Lead (UI + UX):** Owns Streamlit interface, all visual components (risk badges, reason cards, action checklists, micro-lesson cards), Spanish toggle, report export, accessibility compliance, and the 10+ demo scenario cards. Responsible for UI polish and color-blind-safe design.
- **Person 3 -- Demo Lead (Scenarios + Presentation):** Drafts and tests all demo scenarios, writes the 5-minute presentation script, owns the "Maria" narrative, creates backup demo video, handles submission materials, and performs end-to-end QA. Also writes the rule-based pre-filter regex patterns (urgency words, domain mismatch detection).

**5-Person Team:**
- **Person 1 -- LLM Engineer:** OpenAI prompt engineering, structured JSON output, confidence calibration, Spanish translation prompt, guardrails against phishing instruction generation.
- **Person 2 -- Integration Engineer:** Google Safe Browsing API, PhishTank API, conflict resolution logic, spaCy PII redaction, GPT-4o Vision OCR pipeline.
- **Person 3 -- Frontend Developer:** Streamlit UI, all visual components, tabs, risk badges, micro-lesson cards, report export functionality, custom CSS for polish.
- **Person 4 -- UX/Accessibility + Demo Scenarios:** Accessibility audit (color-blind-safe palette, large text, screen reader labels), Spanish toggle UX, 10+ demo scenario design, "Try This Example" card system.
- **Person 5 -- QA + Presentation Lead:** End-to-end testing, edge case testing, load testing on Streamlit Cloud, 5-minute presentation script, "Maria" narrative, backup demo video, submission materials.

### Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| OpenAI API rate limiting during live demo | Low | High | Cache responses for all 10+ demo scenarios locally. Pre-compute demo outputs. Have a pre-recorded backup video ready. Use GPT-4o-mini (higher rate limits than GPT-4o). |
| LLM produces incorrect classification (false safe on a real phishing email) | Medium | High | URL reputation APIs (Google Safe Browsing, PhishTank) hard-override LLM on known-bad URLs. Rule-based layer catches obvious phishing patterns independently. Confidence score with uncertainty messaging hedges incorrect classifications. |
| LLM explains how to craft better phishing (violates red line) | Low | Critical | System prompt includes explicit guardrails: "Never provide instructions that could help someone create phishing content." Output post-processing regex scans for instructional phishing language. Test with adversarial prompts during QA. |
| Streamlit Cloud 1GB resource limit exceeded | Low | Medium | spaCy en_core_web_sm is only ~15MB. No large datasets loaded into memory. Stateless architecture (no user data stored). Monitor memory usage during testing. |
| PhishTank API downtime or rate limit exceeded | Medium | Low | Google Safe Browsing serves as primary URL reputation source. PhishTank is secondary/supplementary. Graceful degradation: if both APIs fail, LLM + rule-based layers still provide classification with a note that URL reputation could not be checked. |
| Demo scenario feels scripted or unrealistic to judges | Low | Medium | Base demo scenarios on real-world phishing templates (with PII replaced). Include at least 2 "tricky" scenarios where the tool shows uncertainty. Let judges paste their own example for a live unscripted test. |

### Win Probability Assessment
- **CTO Tier:** 1
- **Independent Analysis:** This category has the strongest alignment between technical feasibility and sponsor expectations of any category. ISACA's rubric explicitly de-emphasizes technical sophistication in favor of user experience, clarity, impact, and feasibility -- which is exactly where a well-polished Streamlit prototype excels. The challenge brief itself states "a strong hackathon solution often wins on user experience + clarity + impact + feasibility." The tech stack is proven (API calls, no ML training, no complex infrastructure), the cost is near-zero, and the sponsor's domain (cybersecurity literacy) naturally produces compelling demo narratives. The promotion of all stretch goals to MVP (per CTO review) is achievable within 2 weeks because each stretch goal is a self-contained feature addition, not a foundational architecture change. The primary risk is other teams also recognizing this as the "easiest" category and producing competitive submissions, but the education layer (micro-lessons), privacy-by-design (live PII redaction), and multi-layer conflict resolution provide differentiation.
- **Demo Moment:** The "Maria Moment" -- a live walkthrough where a fictional college student receives a text saying her Netflix account will be suspended unless she clicks a link immediately. The presenter pastes the message into PhishGuard AI. In 8 seconds, the screen lights up red with "High Risk," three plain-English reasons appear (urgency language, mismatched domain, credential request), an action checklist tells Maria exactly what to do, the PII redaction toggle shows her phone number was anonymized before processing, and a 30-second micro-lesson teaches her to always verify account issues by going directly to netflix.com. Then the presenter toggles to Spanish and the same explanation appears in Maria's first language. Finally, one-click exports a report she can forward to her university IT department.
- **Overall Win Probability:** **High (70-80%)**. Tier 1 is justified. The combination of low technical risk, near-zero cost, strong sponsor alignment (ISACA's mission is cyber literacy), a naturally compelling demo narrative, and a rubric that rewards exactly what this solution delivers (clarity, impact, feasibility, trust) makes this the highest-probability category in the hackathon. The only downside risk is a competitor team that also executes well on UX polish in this same category.

### Existing Assets Inventory

- **PhishTank downloadable database:** Full phishing URL database available for offline lookups, providing a fallback if the API is unavailable during demo.
- **Kaggle Phishing Email Dataset:** Labeled phishing email examples that can be used to craft realistic demo scenarios and validate classification accuracy.
- **Enron Email Corpus:** Public "normal email" baseline for contrast testing against phishing patterns.
- **spaCy pre-trained NER models:** Open-source, production-ready named entity recognition for PII detection (names, emails, phone numbers, addresses).
- **OpenAI Python SDK:** Well-documented, stable SDK with structured output support for JSON responses.
- **Streamlit component ecosystem:** Pre-built components for file upload, tabs, download buttons, and custom styling.
- **NIST Cybersecurity Framework references:** Can be woven into the demo narrative to resonate with ISACA judges who champion these standards.
- **ISACA CMMI and Zero Trust references:** Position PhishGuard AI as a grassroots cyber literacy on-ramp aligned with ISACA's published frameworks.
- **CPP hackathon training sessions:** Prompt engineering and storytelling workshops available to the team before the event.

### Responsible AI Considerations

- **No user data storage (red line):** PhishGuard AI operates statelessly. No user inputs are persisted to disk, database, or logs. Each analysis is ephemeral -- processed in memory and discarded after the response is rendered. This is demonstrated live during the demo.
- **PII redaction before LLM processing:** User inputs are passed through spaCy NER and regex-based redaction *before* being sent to the OpenAI API. Names, email addresses, phone numbers, and physical addresses are replaced with [REDACTED] tokens. The user sees a "before/after" toggle showing exactly what was anonymized.
- **No phishing instruction generation (red line):** The system prompt explicitly prohibits generating content that could help someone craft phishing messages. Output post-processing includes a regex scan for instructional phishing language. Adversarial prompt testing is included in the QA phase.
- **Explainability by design:** Every classification includes the top 3 reasons in plain language. No black-box verdicts. Users always understand *why* something was flagged.
- **Uncertainty signaling:** When confidence is below 80%, the system explicitly states "I'm not fully certain -- here's how to verify safely" and provides manual verification steps (e.g., "call the company directly using the number on their official website"). This prevents false confidence in either direction.
- **Inclusive design:** Spanish language toggle ensures accessibility for the large Spanish-speaking population in the ISACA OC (Orange County) region. Color-blind-safe palette uses blue/orange differentiation in addition to green/yellow/red. Large text defaults support low-vision users.
- **URL reputation hard-overrides LLM (red line):** If Google Safe Browsing or PhishTank flags a URL as malicious, the system classifies it as High Risk regardless of what the LLM concludes. This prevents the LLM from being "talked into" classifying a known-bad URL as safe through prompt injection or social engineering of the model.
- **Alignment with ISACA frameworks:** The tool's design maps to NIST Cybersecurity Framework (Identify, Protect, Detect, Respond) and Zero Trust principles ("trust nothing, verify everything"), which can be articulated during the demo to demonstrate responsible AI governance alignment.
