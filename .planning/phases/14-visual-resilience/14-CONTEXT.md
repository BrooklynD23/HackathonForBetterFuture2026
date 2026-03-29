# Phase 14: Visual Resilience - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 14 delivers guaranteed visual resilience across all chart-bearing pages: every chart renders with real or demo data, never breaks on empty/failed API responses, and surfaces a discrete "Demo Mode" badge when fallback data is active. The coordinator always knows the data source state.

</domain>

<decisions>
## Implementation Decisions

### Fallback Trigger & Scope
- API error OR empty array after successful fetch both trigger "Demo Mode" — either means no real data for the demo
- Page-level `isMockData: boolean` flag per page — one flag governs all charts on that page (not per-chart)
- All 4 chart-bearing pages covered: Dashboard, AIMatching, Pipeline, Volunteers
- QR stats and Feedback trend charts also get Demo Mode + fallback (full demo resilience on all chart pages)
- Empty arrays from recharts look broken in a demo; fallback ensures something coherent always renders

### Demo Mode Badge Design
- Small blue pill badge placed inline next to the section heading where the chart lives — discrete and contextual
- Badge text: "Demo Mode" (exact ROADMAP wording)
- Visual style: `bg-blue-50 text-blue-700 border border-blue-200` — consistent with V1.2 blue/white theme
- Persistent (non-dismissible) while mock data is active; disappears automatically when real data loads
- NOT a yellow/amber warning — informational blue keeps the demo professional

### Mock Data Architecture (3-layer)
- **Layer 1 (Primary):** Production data from real API endpoints (CSV/live data)
- **Layer 2 (Demo DB):** `data/demo.db` SQLite3 database — comprehensive demonstration-ready dataset designed to show all features working; FastAPI falls back to this when primary data is empty or errors
- **Layer 3 (Last resort):** Thin hardcoded React constants — activates only if the backend itself is unreachable (network/server down)
- Backend adds `"source": "demo"` field to API responses when serving from demo.db → React uses this to set `isMockData = true` and show the badge
- Shared mock store: when React falls back to layer 3, all pages use the same shared mock constants module for cross-page coherence

### Demo Dataset Design
- Comprehensive dataset designed to demonstrate all features: specialists, events, pipeline stages, calendar assignments, QR scan data, feedback records
- Realistic plausible numbers: ~10 specialists, 5 events, pipeline funnel showing 40→18→7 progression, 3 calendar assignments, 5 QR scan records, 8 feedback records
- Cross-feature coherent: same speaker names appear in pipeline + calendar + QR + feedback, same event names reference across tables
- Designed by Codex for maximum demonstration impact

### Claude's Discretion
- Exact SQLite3 schema design for demo.db — should mirror existing CSV/JSON column names exactly for schema compatibility
- Exact fallback detection logic in FastAPI routers (e.g., after fetching, if `len(rows) == 0`, serve from demo.db)
- React `MOCK_DATA` constants in a shared file (layer 3 only — thin, minimal)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/app/components/figma/ImageWithFallback.tsx` — existing fallback pattern (image-specific but shows the component shape)
- `src/styles/theme.css` — V1.2 design tokens for badge styling
- `src/app/components/ui/` — shadcn/ui components including badge-like patterns
- `src/lib/api.ts` — API client, good place to detect `source: "demo"` in responses
- FastAPI routers in `src/api/` — `data.py`, `matching.py`, `calendar.py`, `feedback.py`, `qr.py`

### Established Patterns
- Page-level `isLoading`/`error`/`useState` pattern already used in Dashboard, AIMatching, Pipeline, Volunteers
- Recharts charts: FunnelChart, BarChart, LineChart in Dashboard; FactorRadar (custom) in AIMatching
- Tailwind v4 with V1.2 blue/white tokens; `bg-blue-50 text-blue-700` already used in FeedbackForm
- Immutable data pattern: derive mock data from constants, never mutate

### Integration Points
- FastAPI response models: add optional `source: Literal["live", "demo"]` field to endpoint responses
- React pages: check `response.source === "demo"` OR `data.length === 0` to set `isMockData`
- Dashboard: `funnelData`, `eventVolume`, `reachTrend` derived from pipeline/calendar — if `pipeline.length === 0`, use mock
- AIMatching: `rankedMatches` array — if empty, use mock ranked matches
- Pipeline, Volunteers: list data — if empty array, use mock list

</code_context>

<specifics>
## Specific Ideas

- User confirmed: SQLite3 demo.db is the right fallback approach (not just inline React constants)
- "Comprehensive dataset that loads into every feature" — demo.db should be a complete seed covering all API endpoints
- The demo badge should help coordinators/judges understand they're seeing the product working, not broken — it's a feature, not an apology
- The React layer-3 constants are a safety net only; the demo.db is the real demonstration backbone

</specifics>

<deferred>
## Deferred Ideas

- Gmail send integration from outreach modal — captured in backlog
- Online/cloud demo DB (Supabase/Firebase) for multi-device demos — beyond hackathon scope
- Live data refresh / websocket updates — Phase 14 scope is static fallback only

</deferred>
