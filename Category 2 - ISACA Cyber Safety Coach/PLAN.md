# Category 2 — ISACA OC: "AI for Everyone: Personal Cyber Safety Coach"
**Sponsor:** ISACA Orange County Chapter | **Event:** CPP AI Hackathon "AI for a Better Future" | April 16, 2026

---

## 🎯 Challenge Prompt

> *"Build an AI-enabled experience that helps non-experts quickly understand risk and choose a safe next step — without requiring them to be cybersecurity experts."*

**Target users:** Everyday users — students, families, part-time workers, small clubs — who encounter phishing, scam messages, and risky links across email/SMS/social platforms.

---

## 📦 Deliverable Requirements

### Minimum Viable Prototype (MVP)
The prototype must support **at least one input type**:
- Paste email text, OR
- Paste a URL, OR
- Upload/screenshot text (optional bonus)

And produce **three outputs**:
1. **Risk label** — Safe / Suspicious / High Risk
2. **Top 3 reasons** — bulleted, plain-language explanation (e.g., "urgency language + mismatched domain + credential request")
3. **Recommended action checklist** — what the user should do next

### Stretch Goals (Bonus Points)
- Multi-lingual explanations (English + Spanish)
- Confidence score + uncertainty signaling ("I'm not sure — here's how to verify safely")
- Privacy mode — auto-redact PII (names, emails, phone numbers) before processing
- "Teach-back" micro-lessons (30-second literacy tips after each analysis)
- Lightweight report export (shareable summary a user could forward to IT/admin)

---

## 🏆 Judging Rubric (50 Points)

| Criterion | What Judges Look For |
|---|---|
| **Impact** | Would a non-expert actually use this? Would it reduce real harm? |
| **Clarity** | Are explanations understandable to "everyone" (no jargon)? |
| **Feasibility** | Could this be piloted at a university, club, or small business? |
| **Trust** | Privacy-by-design, transparent reasoning, safe recommendations |
| **Storytelling** | Clear 5-minute demo narrative with a relatable scenario |

*Key judging philosophy: "A strong hackathon solution often wins on user experience + clarity + impact + feasibility" — not just technical sophistication.*

---

## 💡 Winning Concept Strategy

### Why ISACA? Leverage Their Domain
ISACA is the premier global cybersecurity and IT governance association. They want a solution that:
- **Advances cyber literacy** for non-technical populations
- **Demonstrates responsible AI** — transparent, explainable, privacy-respecting
- Could be adopted by universities, community organizations, or SMBs

### Recommended Concept: "PhishGuard AI" — Conversational Cyber Safety Coach

**Core differentiator:** Don't just classify — *educate*. The winning submission won't just say "this is phishing" — it will explain *why* in plain English AND leave the user smarter after each interaction.

**Architecture:**

```
Input Layer
  └── Text paste (email body / URL / SMS text)
  └── Optional: screenshot OCR (Tesseract or GPT-4 Vision)
        ↓
Analysis Engine
  └── LLM-based classification (GPT-4o / Claude API / Gemini)
      Prompt: "Analyze this message for phishing indicators.
               Classify as Safe/Suspicious/High Risk.
               List top 3 red flags in plain English.
               Recommend 3 concrete next steps."
  └── Rule-based pre-filters (regex for urgency words, domain mismatch, credential asks)
  └── URL reputation check (PhishTank API or VirusTotal API)
        ↓
Output Layer
  └── Risk badge (color-coded: green/yellow/red)
  └── Plain-language explanation card (3 bullet points)
  └── Action checklist (contextual: "Don't click" / "Verify via official site" / "Report to IT")
  └── Micro-lesson: 30-second tip related to the detected threat type
  └── Privacy redaction preview (show user what was anonymized)
```

### AI Types to Incorporate
- **LLM (GPT-4o, Claude 3.5, or Gemini 2.0)** — primary reasoning engine for classification + explanation
- **NLP rule-based layer** — keyword/pattern detection (urgency words, mismatched URLs, credential requests) as a fast pre-filter
- **Computer Vision (GPT-4 Vision / Tesseract OCR)** — for screenshot/image text extraction
- **External API enrichment** — PhishTank or VirusTotal for URL reputation

### ISACA Technology Ecosystem Angle
ISACA champions these frameworks — weave them into the design narrative:
- **NIST Cybersecurity Framework** — reference it in the "responsible AI" section
- **Zero Trust principles** — "trust nothing, verify everything" mirrors the tool's logic
- **ISACA's CMMI for cybersecurity** — position the tool as a grassroots cyber literacy on-ramp

---

## 🔬 Research Directions for the Agent

### Key Questions to Investigate
1. What are the most common phishing indicators that non-experts miss? (urgency, spoofed domains, credential harvesting, lookalike logos)
2. What does the latest Verizon Data Breach Investigations Report say about phishing success rates?
3. How do existing tools (VirusTotal, PhishTank, Google Safe Browsing) expose their APIs — and what are the rate limits for a hackathon demo?
4. What UX patterns work best for security tools aimed at non-experts? (plain language, color coding, progressive disclosure)
5. What are ISACA's published guidelines on AI in cybersecurity?
6. What demographic groups are most vulnerable to phishing attacks?

### Datasets to Use
- **Phishing Email Dataset (Kaggle)** — labeled phishing email examples: https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset
- **PhishTank** — phishing URL intelligence: https://www.phishtank.com/ (free API)
- **Enron Email Corpus** — "normal email" language baseline: https://www.cs.cmu.edu/~enron/
- **CISA Known Exploited Vulnerabilities** — real-world threat context
- **Google Safe Browsing API** — URL reputation (free, high rate limit)

### Prompt Engineering Strategy

**Classification Prompt Template:**
```
You are a cybersecurity expert explaining threats to a non-technical person.
Analyze the following message/URL for phishing and social engineering indicators.

Message: [INPUT]

Respond in JSON with:
{
  "risk_level": "Safe | Suspicious | High Risk",
  "confidence": 0.0-1.0,
  "top_3_reasons": ["reason1", "reason2", "reason3"],
  "action_checklist": ["action1", "action2", "action3"],
  "micro_lesson": "One 2-sentence tip about this type of threat",
  "redacted_message": "[message with PII replaced by [REDACTED]]"
}

Use plain English. No jargon. Write as if explaining to a family member.
```

---

## 🎨 Prototype MVP Scope (48 hours)

**Must have:**
- Web UI with text input field (Streamlit or simple HTML/Flask)
- LLM integration returning risk label + 3 reasons + action checklist
- Color-coded risk display
- "Explain why" button for deeper reasoning

**Nice to have:**
- URL scan integration (PhishTank API)
- Privacy redaction toggle (show/hide redacted version)
- Spanish language toggle
- "Was this helpful?" feedback button (improves trust scoring narrative)
- Demo scenario cards ("Try these examples")

---

## 🧠 Differentiation Angles (How to Win)

1. **Plain language obsession** — every output should pass a 6th-grade reading level test
2. **Education layer** — micro-lessons make this a *literacy tool*, not just a classifier
3. **Privacy-by-design demo** — show the redaction feature live; ISACA judges will love this
4. **Confidence + uncertainty** — "I'm 85% confident this is phishing, but here's how to double-check" is more trustworthy than a binary output
5. **Accessibility** — large text, color-blind-safe risk colors, Spanish mode
6. **Demo narrative**: "Maria gets a text that her Netflix account will be suspended. She pastes it in PhishGuard. In 8 seconds, she knows it's a scam — and why — without needing to be a security expert."

---

## 📋 Responsible AI Checklist

- [ ] No storage of user inputs (privacy-by-design explicitly stated)
- [ ] Redaction of PII before LLM processing (demonstrate live)
- [ ] Explainability — every classification comes with a reason
- [ ] No instructions that enable wrongdoing (never explain how to craft better phishing)
- [ ] Uncertainty signaling — system admits when it's unsure
- [ ] Inclusive design — multilingual, accessibility-friendly UI

---

## 🏗️ Technical Stack Recommendation

| Component | Recommended Tool |
|---|---|
| Frontend | Streamlit (fast to build) or React + Tailwind |
| LLM API | OpenAI GPT-4o-mini (cost-effective) or Anthropic Claude |
| URL check | PhishTank API (free) + Google Safe Browsing |
| OCR (optional) | Tesseract or GPT-4o Vision |
| Redaction | spaCy NER or regex rules |
| Demo hosting | Streamlit Cloud or HuggingFace Spaces |

---

## 📎 Source Files Reference
- `Sponsored Problem Challenge ISACA OC.pdf` — Full challenge brief with rubric, datasets, and constraints
