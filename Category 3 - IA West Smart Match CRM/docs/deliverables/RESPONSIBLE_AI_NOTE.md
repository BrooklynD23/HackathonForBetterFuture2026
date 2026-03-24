# Responsible AI Note — IA West SmartMatch CRM

## Privacy & Data Handling

The system contains **zero student PII** — all 77 records are organizational data. Speaker profiles (18 records) derive from publicly listed IA West board information. University contacts are scraped exclusively from publicly published faculty/staff directories and event pages; no login-gated content is accessed. Pipeline metrics track aggregate counts only. No individual student data is collected, stored, or inferred at any point.

## Bias Identification & Mitigation

We identified three specific algorithmic biases in our system and built countermeasures for each.

| Bias | Mechanism | Mitigation |
|------|-----------|------------|
| **Geographic clustering** | 5 of 10 speaker metro designations are LA sub-regions, inflating `geographic_proximity` scores for nearby universities | `coverage_diversity` factor (5% weight) penalizes over-assigned speakers; weight sliders let leadership manually reduce geographic proximity influence |
| **Expertise tag density** | Speakers with richer tag sets could generate inflated `topic_relevance` scores | Cosine similarity normalizes vector magnitude — bias is inherently neutralized by the math |
| **Incumbency advantage** | `historical_conversion` (5% weight) favors previously placed speakers, disadvantaging new board members | Factor capped at 5%; `coverage_diversity` explicitly boosts underutilized speakers; new speakers start with a neutral baseline, not zero |

## Transparency & Explainability

No black-box scores. Every recommendation is decomposable into 8 named factors, explainable in natural language, and adjustable by the end user.

Three mechanisms enforce this:

1. **Score breakdown cards** — Every match displays 8 named factors with individual scores, not just a composite number.
2. **Natural language explanations** — Gemini-generated cards explain in plain English why a speaker was recommended.
3. **Weight sliders** — Chapter leadership adjusts all 8 factor weights in real time; rankings recompute instantly.

## Data Stewardship

- **CSV-based storage** — no cloud database, no third-party data sharing
- **Local-only scraping cache** — hashed filenames, no PII in cache keys
- **Rate-limited scraping** — 1 request per 5 seconds, `robots.txt` respected
- **Closed deployment** — all data stays within IA West infrastructure; nothing leaves the system
