# IA West Smart Match CRM (Category 3)

Local app for speaker-event matching, discovery, and outreach workflows.

## Prerequisites

- Python 3.11+
- A virtual environment at `.venv`
- `GEMINI_API_KEY` in `Category 3 - IA West Smart Match CRM/.env`

## Setup

From `Category 3 - IA West Smart Match CRM/`:

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

Set your real Gemini key in `.env`:

```env
GEMINI_API_KEY=your_real_key_here
```

## Run App (Single Command)

The scripts below start both:
- Backend: local dev backend on `http://127.0.0.1:8000`
- Frontend: Streamlit app on `http://127.0.0.1:8501`

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

## Run From Repo Root (One Click)

If you are at repository root (`HackathonForBetterFuture2026/`), use:

### WSL / Linux

```bash
./start_cat3_dev.sh
```

### Windows (CMD)

```cmd
start_cat3_dev.cmd
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\start_cat3_dev.ps1
```

## Health Checks

- Backend health: `http://127.0.0.1:8000/health`
- Frontend: `http://127.0.0.1:8501`

## Stop Services

- WSL script: `Ctrl+C` in the terminal running `start_dev.sh`
- Windows script: close both launched terminal windows (`CAT3 Backend`, `CAT3 Frontend`)

## Features

### 🏠 Landing Page
- Branded "Academic Curator" design with IA West mission statement
- "How It Works" visual guide explaining the matching workflow
- Feature highlights and trust indicators
- Toggleable view mode for campaign vs. curator workflows

### 🔍 Discovery Tab
- University event scraper with LLM extraction
- Support for 5+ California universities (UCLA, Berkeley, UCSD, etc.)
- Manual URL input for custom event sources
- Extracted event details: name, category, date, volunteer roles
- Caching for offline demo mode

### 🎯 Matches Tab
- AI-powered speaker-to-event matching
- **8-factor scoring algorithm:**
  - Topic Relevance (25%)
  - Role Fit (20%)
  - Geographic Proximity (20%)
  - Calendar Fit (15%)
  - Historical Conversion (5%)
  - Student Interest (5%)
  - Event Urgency (5%)
  - Coverage Diversity (5%)
- Interactive weight adjustment sliders
- Real-time score recomputation
- Match explanation cards with factor breakdowns
- Radar chart visualization of factor scores
- Personalized outreach email generation
- Calendar invite (.ics) download

### 📊 Pipeline Tab
- 6-stage engagement funnel visualization
- Real data labels and stage transitions
- Tooltips showing speaker/event names
- Stage count tracking

### 👥 Volunteer Dashboard
- Speaker-centric view of assignments and capacity
- Utilization bar charts by speaker
- Top-5 matched events per volunteer
- Load balancing analytics

### 🗺️ Expansion Map
- Board-to-campus geographic visualization
- Speaker and university location clustering
- Connection lines showing potential matches
- Multi-state support (CA, HI, NV, AZ, UT)

### ⚙️ Demo Mode
- Cached fixtures for offline presentation
- Artificial delays for demo realism
- Fallback when API keys unavailable
- Pre-warmed embeddings cache

## Testing

Run the full test suite:

```bash
.venv/bin/python -m pytest -v
```

**Current status:** 424 tests passing, 82% code coverage (1 expected Gemini API key test excluded)

Test categories:
- **Unit Tests:** 245 tests covering factors, config, utilities
- **Integration Tests:** 94 tests covering engine, explanations, email
- **UI Tests:** 85 tests covering landing page, dashboards, acceptance flows
