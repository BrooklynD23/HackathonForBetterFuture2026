# IA West Smart Match CRM

AI-orchestrated speaker-event matching platform for the **Insights Association West Chapter**. Discovers university engagement opportunities, matches them with board member volunteers using an 8-factor scoring algorithm, and coordinates outreach through a voice-enabled command center with human-in-the-loop approval.

Built for the **Hackathon for a Better Future 2026** (Category 3).

## Prerequisites

- Python 3.11+
- A virtual environment at `.venv`
- `GEMINI_API_KEY` in `.env` (optional for demo mode)

## Setup

From the `Category 3 - IA West Smart Match CRM/` directory:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

Set your Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_real_key_here
```

For voice features (optional):

```bash
# KittenTTS — install from GitHub release
.venv/bin/pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl
```

## Run the App

### WSL / Linux

```bash
chmod +x scripts/start_dev.sh
./scripts/start_dev.sh
```

### Windows (CMD)

```cmd
scripts\start_dev.cmd
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_dev.ps1
```

The app starts at **http://127.0.0.1:8501** with a health check backend at **http://127.0.0.1:8000/health**.

To stop: `Ctrl+C` in the terminal (WSL/Linux) or close both terminal windows (Windows).

## Demo Mode

Toggle **Demo Mode** in the sidebar to run the app entirely offline using cached fixture data. No API key required.

## Features

### Landing Page

Branded "Academic Curator" design with IA West mission statement, visual "How It Works" guide, feature highlights, and toggleable campaign/curator view modes.

### Command Center (v2.0)

Voice-enabled AI coordinator with natural language intent parsing:

- **Text & voice input** — type commands or use push-to-talk with faster-whisper STT
- **TTS voice output** — KittenTTS reads results aloud with the "Bella" voice
- **Intent parsing** — Gemini extracts structured intents from natural language
- **Action proposal cards** — every action requires explicit approve/reject before execution
- **Proactive suggestions** — data staleness detection and overdue contact reminders
- **Background dispatch** — tool execution runs in daemon threads via a result bus
- **Swimlane dashboard** — live per-agent status with colored badges and elapsed time
- **Multi-step orchestration** — compound intents like "prepare for event" chain discover + rank + outreach
- **NemoClaw adapter** — optional NVIDIA NemoClaw orchestration with graceful direct-dispatch fallback

### Matches Tab

AI-powered speaker-to-event matching with an **8-factor scoring algorithm**:

| Factor | Default Weight |
|--------|---------------|
| Topic Relevance | 25% |
| Role Fit | 20% |
| Geographic Proximity | 20% |
| Calendar Fit | 15% |
| Historical Conversion | 5% |
| Student Interest | 5% |
| Event Urgency | 5% |
| Coverage Diversity | 5% |

- Interactive weight adjustment sliders with real-time recomputation
- Match explanation cards with factor breakdowns
- Radar chart visualization of factor scores
- Personalized outreach email generation
- Calendar invite (.ics) download

### Discovery Tab

University event scraper with LLM extraction supporting 5+ California universities (UCLA, Berkeley, UCSD, etc.). Manual URL input for custom sources. Caching for offline demo mode.

### Pipeline Tab

6-stage engagement funnel visualization with real data labels, stage transitions, tooltips, and count tracking.

### Volunteer Dashboard

Speaker-centric view with utilization bar charts, top-5 matched events per volunteer, and load balancing analytics.

### Expansion Map

Board-to-campus geographic visualization with speaker and university clustering, connection lines, and multi-state support (CA, HI, NV, AZ, UT).

## Architecture

```
src/
  app.py                          # Streamlit entry point
  config.py                       # Centralized configuration and factor registry
  runtime_state.py                # Session state initialization
  data_loader.py                  # CSV data loading pipeline
  embeddings.py                   # Gemini embedding generation and caching
  similarity.py                   # Cosine similarity scoring
  demo_mode.py                    # Offline demo with cached fixtures
  gemini_client.py                # Gemini API REST client
  utils.py                        # Shared utilities

  matching/
    engine.py                     # 8-factor matching engine
    factors.py                    # Factor scoring functions
    explanations.py               # LLM-generated match explanations

  scraping/
    scraper.py                    # University event web scraper

  outreach/
    email_gen.py                  # Personalized email generation
    ics_generator.py              # Calendar invite (.ics) generation

  voice/
    tts.py                        # KittenTTS text-to-speech wrapper
    stt.py                        # faster-whisper speech-to-text wrapper

  coordinator/
    intent_parser.py              # Gemini-powered intent extraction
    approval.py                   # HITL approval state machine
    suggestions.py                # Proactive suggestion engine
    result_bus.py                 # Background thread dispatch and polling
    nemoclaw_adapter.py           # NemoClaw orchestration adapter
    tools/
      discovery_tool.py           # Wraps scrape_university()
      matching_tool.py            # Wraps rank_speakers_for_event()
      outreach_tool.py            # Wraps generate_outreach_email()
      contacts_tool.py            # POC contact CRUD and follow-up tracking

  ui/
    command_center.py             # Voice panel, approval cards, swimlane, chat history
    swimlane_dashboard.py         # Per-agent status dashboard
    matches_tab.py                # Matching results with radar charts
    discovery_tab.py              # Event discovery interface
    pipeline_tab.py               # Engagement funnel visualization
    expansion_map.py              # Geographic map visualization
    volunteer_dashboard.py        # Volunteer analytics
    landing_page.py               # Landing page
    email_panel.py                # Email composition panel
    styles.py                     # Custom CSS injection

  feedback/
    acceptance.py                 # Feedback collection and sidebar

  extraction/                     # Event data extraction from scraped HTML
```

## Testing

Run the full test suite:

```bash
.venv/bin/python -m pytest -v
```

**580 tests** covering:

- **Unit tests** — factors, config, utilities, voice wrappers, tool wrappers
- **Integration tests** — matching engine, email generation, intent parsing, approval state machine, result bus
- **UI tests** — landing page, command center, swimlane dashboard, all tabs
- **E2E flows** — discovery-to-matching handoff, feedback collection

Run with coverage:

```bash
.venv/bin/python -m pytest --cov=src --cov-report=term-missing
```

## Environment Variables

See `.env.example` for all options. Key variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | For live mode | Google Gemini API key |
| `GEMINI_TEXT_MODEL` | No | Text model (default: `gemini-2.5-flash-lite`) |
| `GEMINI_EMBEDDING_MODEL` | No | Embedding model (default: `gemini-embedding-001`) |
| `USE_NEMOCLAW` | No | Enable NemoClaw orchestration (`0` or `1`) |
| `NVIDIA_NGC_API_KEY` | For NemoClaw | NVIDIA NGC API key |
| `KITTENTTS_VOICE` | No | TTS voice name (default: `Bella`) |
| `WHISPER_MODEL_SIZE` | No | STT model size (default: `base`) |

## Deliverables

Located in `docs/deliverables/`:

- **Demo Script** — step-by-step walkthrough for judges
- **Growth Strategy** — IA West chapter engagement roadmap
- **Measurement Plan** — KPIs and success metrics
- **Responsible AI Note** — ethical considerations and safeguards
- **Business Deliverables Guide** — overview of all deliverable documents
