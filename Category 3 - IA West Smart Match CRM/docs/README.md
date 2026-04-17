# Documentation Index

## Architecture

| Document | Description |
|----------|-------------|
| [Architecture Overview](architecture/OVERVIEW.md) | System design, layers, data flows, state management |

## API Reference

| Document | Description |
|----------|-------------|
| [API Endpoints](api/ENDPOINTS.md) | Complete endpoint reference for all 8 routers |
| [Interactive Docs](http://localhost:8000/docs) | Swagger UI (run backend locally) |

## Development

| Document | Description |
|----------|-------------|
| [Main README](../README.md) | Project setup, environment, and quick start |
| [E2E Tests](E2E_TESTS.md) | End-to-end test strategy and coverage |
| [Sprint Plan](SPRINT_PLAN.md) | Execution scope, milestones, and go/no-go gates |
| [Data Quality Report](data_quality_report.md) | CSV dataset quality analysis |
| [Scraping Research](scraping_research.md) | Web scraper and LLM extraction notes |
| [Gemini Provider Decision](gemini_provider_decision_2026-03-18.md) | AI provider selection rationale (2026-03-18) |

## Demos & Presentations

| Document | Description |
|----------|-------------|
| [Demo Narrative](demos/demo-narrative-2026-04-14.md) | Six-scene judge walkthrough with verification snapshot |
| [Demo Script (5 min)](demos/demo-script-5min.md) | Timed presentation guide |
| [Voice / Mic UAT Guide](demos/UAT-VOICE-MIC.md) | Manual test guide for TTS/STT features |

## Deliverables

| Document | Description |
|----------|-------------|
| [Business Deliverables Guide](deliverables/BUSINESS_DELIVERABLES_GUIDE.md) | Overview of all deliverables |
| [Demo Script](deliverables/DEMO_SCRIPT.md) | Formal demo script |
| [Growth Strategy](deliverables/GROWTH_STRATEGY.md) | Go-to-market and expansion plan |
| [Measurement Plan](deliverables/MEASUREMENT_PLAN.md) | KPIs and success metrics |
| [Responsible AI Note](deliverables/RESPONSIBLE_AI_NOTE.md) | AI ethics and bias considerations |

## Testing

| Document | Description |
|----------|-------------|
| [Test Log](testing/test_log.md) | Test run history |
| [Bug Log](testing/bug_log.md) | Tracked bugs and resolutions |
| [Rehearsal Log](testing/rehearsal_log.md) | Demo rehearsal notes |
| [Playwright Report](testing/2026-03-25-playwright-demo-report.md) | E2E evidence capture |

## History

Sprint plans, code reviews, and audit artifacts from the development cycle.

| Path | Description |
|------|-------------|
| [history/sprints/](history/sprints/) | Sprint 0–5 plans and closeout reports |
| [history/reviews/](history/reviews/) | Code review reports (Phase 2, Sprint 5) |
| [history/audits/](history/audits/) | Pre-demo and tooling audit reports |

---

## Key Technical Contracts

- **Imports:** `from src...`
- **Canonical match-result keys:** `total_score` + `factor_scores.{topic_relevance, role_fit, geographic_proximity, calendar_fit, historical_conversion, student_interest, event_urgency, coverage_diversity}` (8 factors)
- **Embedding cache:** `cache/` — `.npy` vectors + `.json` metadata + `cache_manifest.json`
- **Scrape cache:** `cache/scrapes/<sha256(url)>.json`
- **Demo database:** `data/demo.db` — built by `python scripts/seed_demo_db.py`
- **CSV event row headers:** `Event / Program`, `Host / Unit`, `Volunteer Roles (fit)` (literal)
- **Web crawler:** tries Gemini grounded search first; falls back to Tavily if `TAVILY_API_KEY` is set
