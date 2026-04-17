# Architecture Overview

## System Design

The IA West Smart Match CRM is a hybrid full-stack application with a shared Python domain layer consumed by two UI surfaces:

1. **FastAPI + React** — the primary production path (v3+)
2. **Streamlit** — the legacy operator UI (still functional for the voice/HITL path)

```
┌─────────────────────────────────────────────┐
│            React Frontend (Vite)            │
│  Landing · Login · Admin · Coordinator      │
│  Student Portal · Volunteer Portal          │
└──────────────┬──────────────────────────────┘
               │  /api/* (Vite proxy → :8000)
┌──────────────▼──────────────────────────────┐
│           FastAPI Backend                   │
│  portals · matching · outreach · crawler    │
│  qr · feedback · calendar · data            │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Shared Python Domain                │
│  Matching Engine  │  Scraper + Extractor    │
│  Outreach Gen     │  Feedback Optimizer     │
│  QR Service       │  Coordinator / HITL     │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│              Data Layer                     │
│  CSV files (volunteers · events · courses)  │
│  demo.db (SQLite — all portal data)         │
│  File cache (embeddings · scrapes)          │
└─────────────────────────────────────────────┘
```

## Layers

### Configuration & Data Boundary
`src/config.py`, `src/data_loader.py`

Validates env/filesystem prerequisites, loads the four canonical CSV datasets into an immutable `LoadedDatasets` dataclass, and provides cached file readers for JSON/JSONL telemetry.

### Shared Domain Services
`src/matching/`, `src/scraping/`, `src/extraction/`, `src/outreach/`, `src/feedback/`, `src/qr/`

Framework-agnostic business logic. Both the Streamlit shell and the FastAPI adapter compose from these modules.

### FastAPI Adapter
`src/api/main.py`, `src/api/routers/`

Exposes domain services as JSON endpoints. Uses Pydantic for request validation and normalizes all responses so the React client sees stable contracts.

### React Frontend
`frontend/src/app/`, `frontend/src/lib/api.ts`

Browser-router SPA. `api.ts` is the single integration seam — it calls `/api/*`, normalizes backend payloads, and exposes typed TypeScript contracts to all page components.

### Coordinator / HITL
`src/coordinator/`, `src/ui/command_center.py`

Gemini intent parsing, `ActionProposal` lifecycle (proposed → approved → dispatched), background thread tool runner, and swimlane result bus.

## Key Data Flows

### React + FastAPI (primary path)
```
main.tsx → routes.tsx → Page component
  → api.ts fetch helper
    → Vite proxy (:5173 → :8000)
      → FastAPI router
        → Domain service
          → CSV / demo.db / cache
```

### Discovery → Match → Outreach
```
Coordinator triggers discovery
  → scraper.py fetches HTML
    → llm_extractor.py → structured events
      → matching/engine.py → ranked speaker list
        → outreach/email_gen.py + ics_generator.py
          → pipeline_updater.py persists stage
```

## State Management

- **React**: component-local `useState`/`useEffect` only — no global store (Redux/Zustand)
- **Streamlit**: `st.session_state` managed via `src/runtime_state.py`
- **Persistence**: file-backed — CSV inputs, JSON/JSONL feedback, SQLite demo.db

## Authentication

Demo-only mock auth via `POST /api/portals/auth/mock-login`. No session tokens or JWT. The login page routes directly to the portal on success. FastAPI routers do not enforce auth headers.

## Error Handling

- Config/data errors fail fast at startup with explicit messages
- Scraper/LLM failures fall back to cache or empty-state
- FastAPI routers catch exceptions and return structured `HTTPException` responses
- `api.ts` centralizes HTTP error handling; components render the backend `detail` field

---

*See also: [`.planning/codebase/ARCHITECTURE.md`](../../../.planning/codebase/ARCHITECTURE.md) — full layer analysis with entry points and cross-cutting concerns.*
