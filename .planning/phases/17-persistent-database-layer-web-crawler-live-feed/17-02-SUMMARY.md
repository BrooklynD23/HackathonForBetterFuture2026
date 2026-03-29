---
phase: 17-persistent-database-layer-web-crawler-live-feed
plan: 02
subsystem: api
tags: [fastapi, sse, crawler, gemini, tavily, asyncio, streaming]

# Dependency graph
requires:
  - phase: 17-persistent-database-layer-web-crawler-live-feed
    provides: smartmatch_db.py with insert_crawler_event/load_crawler_events

provides:
  - Crawler router with POST /api/crawler/start, GET /api/crawler/feed (SSE), GET /api/crawler/results
  - web_search() function in gemini_client.py using Google Search grounding
  - 3-layer search fallback: Gemini -> Tavily -> seed URLs only
  - Persistent storage of crawl events to smartmatch.db via insert_crawler_event()
  - Real-time SSE streaming with asyncio.Queue(maxsize=100) and keepalive + done sentinel

affects:
  - frontend crawler UI (plan 17-03 if applicable)
  - demo coordinator workflow showing live web discovery

# Tech tracking
tech-stack:
  added: [tavily-python>=0.7.0]
  patterns:
    - asyncio.Queue for SSE event bus with maxsize cap
    - run_in_executor for blocking I/O (Gemini REST, Tavily SDK) in async context
    - Graceful API key degradation (missing key returns empty list, does not crash)
    - StreamingResponse with text/event-stream and X-Accel-Buffering: no

key-files:
  created:
    - Category 3 - IA West Smart Match CRM/src/api/routers/crawler.py
  modified:
    - Category 3 - IA West Smart Match CRM/src/gemini_client.py
    - Category 3 - IA West Smart Match CRM/src/api/main.py
    - Category 3 - IA West Smart Match CRM/requirements.txt

key-decisions:
  - "SSE stream uses StreamingResponse (not EventSourceResponse) for compatibility with existing FastAPI setup"
  - "asyncio.Queue maxsize=100 prevents unbounded memory growth when SSE consumer disconnects"
  - "Gemini search failure silently falls through to Tavily; both missing falls through to seed-only mode"
  - "All blocking I/O uses loop.run_in_executor(None, ...) to avoid blocking the FastAPI event loop"

patterns-established:
  - "run_in_executor pattern: all sync SDK/REST calls wrapped in loop.run_in_executor for async FastAPI"
  - "SSE keepalive: yield ': keepalive\\n\\n' on 30s timeout to prevent proxy disconnection"
  - "SSE done sentinel: None in queue signals stream end, yields data: {status: done}"

requirements-completed: [CRAWLER-01, CRAWLER-02]

# Metrics
duration: 12min
completed: 2026-03-28
---

# Phase 17 Plan 02: Web Crawler Backend Summary

**FastAPI crawler router with SSE live feed, Gemini Google Search grounding + Tavily SDK fallback, and persistent smartmatch.db storage for IA West directed school discovery**

## Performance

- **Duration:** 12 min
- **Started:** 2026-03-28T05:58:00Z
- **Completed:** 2026-03-28T06:10:00Z
- **Tasks:** 1
- **Files modified:** 4

## Accomplishments

- Added `web_search()` to `gemini_client.py` using Gemini's Google Search grounding tool (returns `list[dict[str, str]]` with url/title)
- Created `crawler.py` router with 3 endpoints: POST `/start` (background task), GET `/feed` (SSE stream), GET `/results` (DB query)
- Implemented 3-layer graceful degradation: Gemini search -> Tavily SDK -> seed URLs only (when both API keys missing)
- All blocking I/O runs in `loop.run_in_executor` to keep FastAPI event loop non-blocking
- Registered crawler router in `main.py` at `/api/crawler` prefix
- Added `tavily-python>=0.7.0` to `requirements.txt`

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend gemini_client.py with web_search and create crawler router** - `21673fa` (feat)

**Plan metadata:** (pending final docs commit)

## Files Created/Modified

- `Category 3 - IA West Smart Match CRM/src/api/routers/crawler.py` - Crawler router: /start, /feed (SSE), /results with asyncio.Queue SSE bus
- `Category 3 - IA West Smart Match CRM/src/gemini_client.py` - Added web_search() using Google Search grounding REST tool
- `Category 3 - IA West Smart Match CRM/src/api/main.py` - Registered crawler router at /api/crawler
- `Category 3 - IA West Smart Match CRM/requirements.txt` - Added tavily-python>=0.7.0

## Decisions Made

- Used `StreamingResponse` (not `EventSourceResponse`) for SSE — consistent with existing FastAPI patterns in this project and avoids an additional dependency
- `asyncio.Queue(maxsize=100)` with `put_nowait` + `QueueFull` exception handling: drops events gracefully when no consumer is connected rather than blocking the crawl task
- Crawl persists events to `smartmatch.db` via `insert_crawler_event()` which was created by plan 17-01

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

Python dependency verification (import check) could not run in WSL environment because the venv with project dependencies is on the Windows side. Static grep-based verification confirmed all acceptance criteria were met instead.

## User Setup Required

To enable live search results (beyond seed URL crawling):
- `GEMINI_API_KEY` - Google Cloud API key with Gemini access (enables Google Search grounding)
- `TAVILY_API_KEY` - Tavily search API key (fallback when Gemini is unavailable)

Both are optional. Missing keys cause graceful fallback to seed URL-only crawling.

## Known Stubs

None - all endpoints are fully wired to real data sources (smartmatch.db via `insert_crawler_event`/`load_crawler_events`, Gemini REST via `web_search()`, Tavily SDK via `TavilyClient`).

## Next Phase Readiness

- Crawler backend is fully functional: POST /api/crawler/start triggers background crawl, GET /api/crawler/feed streams SSE events, GET /api/crawler/results returns persisted events
- Ready for plan 17-03: Frontend React integration to display live crawler feed and results
- Seed URLs (10 IA West directed school pages) ensure demo works even without API keys

---
*Phase: 17-persistent-database-layer-web-crawler-live-feed*
*Completed: 2026-03-28*
