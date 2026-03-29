# Phase 17: Persistent Database Layer + Web Crawler Live Feed - Research

**Researched:** 2026-03-27
**Domain:** SQLite 3-layer fallback architecture + FastAPI SSE + Gemini/Tavily web search crawling + React EventSource live feed
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- Layer 0: `data/smartmatch.db` — persistent, primary; created by `scripts/seed_smartmatch_db.py`
- Layer 1: `data/demo.db` — existing demo.db, moves from primary to fallback
- Layer 2: CSV files in `data/` — last-resort fallback via `src/ui/data_helpers.py`
- All IA West CSV datasets seeded into Layer 0 on first run (specialists, cpp_events, cpp_courses, calendar_events, pipeline, poc_contacts)
- `web_crawler_events` table in `smartmatch.db`
- New helper module: `src/api/smartmatch_db.py` (mirrors `demo_db.py` interface exactly)
- New router: `src/api/routers/crawler.py` with POST /api/crawler/start, GET /api/crawler/feed, GET /api/crawler/results
- SSE via FastAPI's `StreamingResponse` with `text/event-stream` media type
- Primary crawler: Google Gemini API; secondary: Tavily search API
- Frontend: `CrawlerFeed` component in coordinator dashboard
- GEMINI_API_KEY and TAVILY_API_KEY are optional (graceful degradation)
- Source tags: `live` (Layer 0), `demo` (Layer 1), `csv` (Layer 2)

### Claude's Discretion

- Exact CSS/animation implementation for the live feed panel
- Whether to use polling as fallback if SSE not supported
- Rate limiting strategy for crawler
- Whether to deduplicate crawl results by URL before storing

### Deferred Ideas (OUT OF SCOPE)

- Full OAuth Gmail integration
- Cloud database
- Crawler scheduling (cron/scheduled crawls)
- Crawler deduplication UI
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DB-01 | Persistent `data/smartmatch.db` SQLite exists and is primary data source for all API endpoints | smartmatch_db.py module pattern, seed script, 3-layer fallback chain |
| DB-02 | All IA West CSV datasets imported into `smartmatch.db` on first run | CSV column mapping for all 6 source files documented below |
| DB-03 | Layer fallback order: `smartmatch.db` → `demo.db` → CSV, with source tag in every API response | `_load_rows_with_fallback()` 3-layer extension pattern |
| DB-04 | Web crawler events stored in `smartmatch.db`'s `web_crawler_events` table | Table schema documented below |
| CRAWLER-01 | `/api/crawler/feed` SSE endpoint streams real-time crawler activity | FastAPI SSE pattern (StreamingResponse + asyncio.Queue) |
| CRAWLER-02 | Coordinator dashboard shows live scrolling feed of crawler activity | React EventSource hook + animated list component |
| CRAWLER-03 | Coordinator can trigger a new crawl targeting IA West directed school pages from UI | POST /api/crawler/start + "Start Crawl" button |
</phase_requirements>

---

## Summary

Phase 17 delivers two tightly coupled subsystems built on existing project patterns.

The **3-layer database architecture** is a straightforward extension of the current 2-layer fallback. The existing `_load_rows_with_fallback(loader, demo_loader)` in `data.py` grows to `_load_rows_with_fallback(live_loader, demo_loader, csv_loader)`. A new `src/api/smartmatch_db.py` mirrors `demo_db.py` exactly — same `_connect()`, same `_load_rows()`, same `_decode_json_fields()` helpers, same public function signatures. A new seed script `scripts/seed_smartmatch_db.py` reads the real IA West CSVs (unlike `seed_demo_db.py` which uses hardcoded Python constants) and populates the same table schema. Layer 0 also gets an additional `web_crawler_events` table and a `cpp_courses` table not present in demo.db.

The **web crawler** uses Google Gemini's `google-search` grounding tool (via REST API — the project already uses stdlib urllib for Gemini, so no SDK needed) and Tavily Python SDK as a parallel/fallback. Crawl jobs run as FastAPI BackgroundTasks. Real-time activity is communicated via an `asyncio.Queue` per-session. The `/api/crawler/feed` endpoint uses `StreamingResponse` with `text/event-stream` to drain that queue as SSE. The React frontend uses the native browser `EventSource` API to receive events and renders an animated list.

**Primary recommendation:** Use `StreamingResponse` with manual SSE formatting rather than `fastapi.sse.EventSourceResponse`. The project pins `fastapi>=0.115.0` and `EventSourceResponse` was added in 0.135.0 — upgrading is risky mid-hackathon. The manual StreamingResponse pattern is battle-tested and requires zero new dependencies.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sqlite3 | stdlib | Layer 0 + Layer 1 databases | Already used by demo_db.py; zero-dependency |
| fastapi | >=0.115.0 (pinned in requirements.txt) | SSE endpoint, BackgroundTasks, router | Already in use |
| asyncio | stdlib | Queue for SSE fan-out from crawler to feed endpoint | Built-in; no extra install |
| requests | 2.31.0 (already installed) | HTTP fetch for seed URL validation, Tavily fallback | Already installed |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| tavily-python | 0.7.23 (latest, Mar 2026) | Web search via Tavily API | When TAVILY_API_KEY is set |
| google-genai | 1.68.0 (latest, Mar 2026) | Gemini grounding with Google Search | When GEMINI_API_KEY is set; or use existing REST client in src/gemini_client.py |
| csv (stdlib) | stdlib | Reading IA West CSVs in seed script | Already used in data_helpers.py |
| json (stdlib) | stdlib | poc_contacts.json seed + JSON field encode/decode | Already used throughout |

### Decision: google-genai SDK vs. existing REST client

The project already has `src/gemini_client.py` which calls the Gemini REST API directly via stdlib urllib. Two options:

**Option A (recommended):** Use the existing `gemini_client.py` pattern — add a `web_search()` function that calls `generateContent` with a `googleSearch` tool config. No new package needed.

**Option B:** Install `google-genai` SDK. Provides cleaner API, async support, but adds a new dependency. The legacy `google-generativeai` package is deprecated as of November 30, 2025; the new package is `google-genai`.

For hackathon stability, **Option A** is preferred: extend the existing REST helper with a search function. If the grounding metadata response format is complex, fall back to Option B.

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual SSE via StreamingResponse | sse-starlette library | sse-starlette adds a dependency; manual SSE is 15 lines of code |
| Manual SSE via StreamingResponse | fastapi.sse.EventSourceResponse | Requires fastapi>=0.135.0; project pins >=0.115.0 |
| asyncio.Queue for SSE fan-out | Global list of queues | asyncio.Queue is thread-safe and well-understood |
| Tavily SDK | Direct Tavily REST API | SDK is simpler; REST is dependency-free |

**Installation (new dependencies only):**
```bash
pip install tavily-python==0.7.23
# google-genai only if using SDK approach:
# pip install google-genai==1.68.0
```

**Version verification (confirmed 2026-03-27):**
- tavily-python: 0.7.23 (PyPI, released Mar 9, 2026)
- google-genai: 1.68.0 (PyPI, released Mar 18, 2026)
- fastapi: >=0.115.0 (project constraint; EventSourceResponse requires >=0.135.0 — do NOT rely on it)

---

## Architecture Patterns

### Recommended Project Structure (new files only)
```
src/api/
├── smartmatch_db.py          # Layer 0 reader (mirrors demo_db.py)
├── routers/
│   ├── crawler.py            # POST /start, GET /feed, GET /results
│   └── data.py               # UPDATE: extend fallback chain to 3 layers
scripts/
├── seed_smartmatch_db.py     # NEW: reads real CSVs, creates smartmatch.db
data/
└── smartmatch.db             # NEW: created by seed script
frontend/src/app/
├── components/
│   └── CrawlerFeed.tsx       # NEW: live scrolling panel
└── pages/
    └── Dashboard.tsx         # UPDATE: add CrawlerFeed panel
```

### Pattern 1: smartmatch_db.py (mirror demo_db.py)

`smartmatch_db.py` is a structural copy of `demo_db.py` with a different path constant and additional functions for the `web_crawler_events` and `cpp_courses` tables.

```python
# src/api/smartmatch_db.py
_SMARTMATCH_DB_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "smartmatch.db"
)

def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(str(_SMARTMATCH_DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection

# Same _decode_json_fields() and _load_rows() helpers as demo_db.py

def load_live_specialists() -> list[dict[str, Any]]:
    return _load_rows("SELECT * FROM specialists ORDER BY name")

# ... mirrors every load_demo_* function with load_live_* equivalent

def load_crawler_events() -> list[dict[str, Any]]:
    return _load_rows(
        "SELECT * FROM web_crawler_events ORDER BY crawled_at DESC"
    )

def insert_crawler_event(event: dict[str, Any]) -> None:
    with _connect() as conn:
        conn.execute(
            """INSERT INTO web_crawler_events
               (url, title, description, school_name, crawled_at, source, status)
               VALUES (:url, :title, :description, :school_name, :crawled_at, :source, :status)""",
            event,
        )
        conn.commit()
```

### Pattern 2: 3-Layer Fallback in data.py

Extend `_load_rows_with_fallback()` to handle 3 layers:

```python
# src/api/routers/data.py

from src.api.smartmatch_db import load_live_specialists  # etc.

def _live_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**row, "source": "live"} for row in rows]

def _demo_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**row, "source": "demo"} for row in rows]

def _csv_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**row, "source": "csv"} for row in rows]

def _load_rows_with_fallback(
    live_loader: Callable[[], list[dict[str, Any]]],
    demo_loader: Callable[[], list[dict[str, Any]]],
    csv_loader: Callable[[], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    try:
        rows = live_loader()
        if rows:
            return _live_rows(rows)
    except Exception:
        pass
    try:
        rows = demo_loader()
        if rows:
            return _demo_rows(rows)
    except Exception:
        pass
    return _csv_rows(csv_loader())
```

### Pattern 3: FastAPI SSE with asyncio.Queue (manual StreamingResponse)

The crawler runs in a BackgroundTask and publishes events to a per-request asyncio.Queue. The SSE endpoint drains that queue.

```python
# src/api/routers/crawler.py
import asyncio
import json
from collections.abc import AsyncIterator
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse

router = APIRouter()

# Module-level queue so background task can push while SSE endpoint pulls
_crawler_queue: asyncio.Queue[dict | None] = asyncio.Queue()


async def _event_stream() -> AsyncIterator[str]:
    """Drain the crawler queue, yielding SSE-formatted strings."""
    while True:
        event = await _crawler_queue.get()
        if event is None:  # Sentinel: crawl finished
            yield "data: {\"status\": \"done\"}\n\n"
            break
        payload = json.dumps(event)
        yield f"data: {payload}\n\n"


@router.get("/feed")
async def crawler_feed() -> StreamingResponse:
    return StreamingResponse(
        _event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/start")
async def start_crawl(background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(_run_crawl)
    return {"status": "started"}


async def _run_crawl() -> None:
    """Crawl IA West directed school pages; push events to queue."""
    for url in SEED_URLS:
        await _crawler_queue.put({
            "url": url,
            "status": "crawling",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        result = await _fetch_page_info(url)  # Gemini or Tavily
        await _crawler_queue.put({**result, "status": "found"})
    await _crawler_queue.put(None)  # Done sentinel
```

**Important caveat:** A single module-level `asyncio.Queue` means only one active crawl at a time, and concurrent SSE connections share the same queue. For a hackathon demo this is acceptable. For multi-user production use, each SSE connection would need its own queue (fan-out pattern).

### Pattern 4: React EventSource Hook

```typescript
// frontend/src/app/components/CrawlerFeed.tsx
import { useEffect, useRef, useState } from "react";

interface CrawlerEvent {
  url: string;
  title?: string;
  status: "crawling" | "found" | "error" | "done";
  timestamp: string;
}

function useCrawlerFeed(active: boolean) {
  const [events, setEvents] = useState<CrawlerEvent[]>([]);
  const [done, setDone] = useState(false);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!active) return;
    const es = new EventSource("/api/crawler/feed");
    esRef.current = es;

    es.onmessage = (e) => {
      const data: CrawlerEvent = JSON.parse(e.data);
      if (data.status === "done") {
        setDone(true);
        es.close();
        return;
      }
      setEvents((prev) => [...prev, data]);
    };

    es.onerror = () => es.close();
    return () => es.close();
  }, [active]);

  return { events, done };
}
```

### Pattern 5: Gemini Web Search via Existing REST Client

Extend `src/gemini_client.py` with a `web_search()` function that sends a `generateContent` request with the `googleSearch` grounding tool:

```python
# Extension to src/gemini_client.py
def web_search(
    query: str,
    *,
    api_key: str,
    model: str = "gemini-2.0-flash",
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Search the web using Gemini's Google Search grounding tool."""
    payload = {
        "contents": [{"parts": [{"text": query}], "role": "user"}],
        "tools": [{"googleSearch": {}}],
    }
    return _post_json(
        f"v1beta/models/{model}:generateContent",
        payload,
        api_key=api_key,
        timeout=timeout,
    )
```

The response contains `candidates[0].groundingMetadata.groundingChunks` with `{web: {uri, title}}` entries. Extract those as the crawl results.

### Anti-Patterns to Avoid

- **Blocking the event loop in the SSE generator:** `_run_crawl` must be `async def` and any I/O must use `asyncio` primitives or `run_in_executor`. Using `requests.get()` synchronously inside an `async def` blocks the event loop.
- **Importing demo_db loaders as the fallback without a wrapper:** The `source` tag must be injected at the fallback chain level, not inside `demo_db.py`.
- **Creating `smartmatch.db` at import time:** The path constant is safe at module level; the actual `sqlite3.connect()` only happens inside function calls. Same pattern as demo_db.py.
- **Using `fastapi.sse.EventSourceResponse`:** Only available in fastapi>=0.135.0; the project pins >=0.115.0. Use `StreamingResponse` with `text/event-stream` instead.
- **One seed script that both creates and re-creates on every startup:** `seed_smartmatch_db.py` should skip creation if the DB already exists and has rows (like checking `SELECT COUNT(*) FROM specialists > 0`). Only drop-and-recreate if `--force` flag is passed.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Web search | Custom HTTP scraper for school pages | Gemini `googleSearch` grounding + Tavily SDK | Google/Tavily handle robots.txt, pagination, rate limits, JS rendering |
| SSE keep-alive | Custom ping timer | Set `Cache-Control: no-cache` + `X-Accel-Buffering: no` headers | Browsers handle reconnect; nginx proxies need the header |
| JSON serialization in SSE | Custom encoder | `json.dumps(event)` — already using stdlib json throughout | No new deps needed |
| CSV import with type coercion | Custom parser | `csv.DictReader` + explicit column mapping (already in data_helpers.py) | Same pattern, proven |
| DB existence check before seed | Custom lock/flag file | `SELECT COUNT(*) FROM sqlite_master WHERE type='table'` + row count check | sqlite3 stdlib handles this |

---

## Database Schema

### Layer 0 — `data/smartmatch.db` Tables

All tables from `demo.db` (see `seed_demo_db.py` `create_schema()`) plus two new tables:

**`cpp_courses` (new in Layer 0 only):**
```sql
CREATE TABLE cpp_courses (
    instructor TEXT,
    course TEXT,
    section TEXT,
    title TEXT,
    days TEXT,
    start_time TEXT,
    end_time TEXT,
    enrl_cap TEXT,
    mode TEXT,
    guest_lecture_fit TEXT
);
```
Source: `data/data_cpp_course_schedule.csv` columns: `Instructor, Course, Section, Title, Days, Start Time, End Time, Enrl Cap, Mode, Guest Lecture Fit`

**`web_crawler_events` (new in Layer 0 only):**
```sql
CREATE TABLE web_crawler_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    title TEXT,
    description TEXT,
    school_name TEXT,
    crawled_at TEXT NOT NULL,
    source TEXT NOT NULL,        -- 'gemini' | 'tavily'
    status TEXT NOT NULL         -- 'found' | 'error'
);
```

**`poc_contacts` (new in Layer 0 only — `demo.db` does not have this):**
```sql
CREATE TABLE poc_contacts (
    name TEXT,
    email TEXT,
    org TEXT,
    role TEXT,
    comm_history TEXT  -- JSON array stored as TEXT
);
```
Source: `data/poc_contacts.json` — array of objects with `name`, `email`, `org`, `role`, `comm_history` fields.

### CSV Column Mapping for Seed Script

| CSV File | Table Name | Key Columns |
|----------|------------|-------------|
| `data_speaker_profiles.csv` | `specialists` | `Name→name`, `Board Role→board_role`, `Metro Region→metro_region`, `Company→company`, `Title→title`, `Expertise Tags→expertise_tags` |
| `data_cpp_events_contacts.csv` | `cpp_events` | `Event / Program`, `Category`, `Recurrence (typical)`, `Host / Unit`, `Volunteer Roles (fit)`, `Primary Audience`, `Public URL`, `Point(s) of Contact (published)`, `Contact Email / Phone (published)` |
| `data_cpp_course_schedule.csv` | `cpp_courses` | `Instructor`, `Course`, `Section`, `Title`, `Days`, `Start Time`, `End Time`, `Enrl Cap`, `Mode`, `Guest Lecture Fit` |
| `data_event_calendar.csv` | `event_calendar` | `IA Event Date`, `Region`, `Nearby Universities`, `Suggested Lecture Window`, `Course Alignment` |
| `pipeline_sample_data.csv` | `pipeline` | `event_name`, `speaker_name`, `match_score`, `rank`, `stage`, `stage_order` |
| `poc_contacts.json` | `poc_contacts` | `name`, `email`, `org`, `role`, `comm_history` (JSON encode as TEXT) |

Note: `calendar_events`, `calendar_assignments`, `qr_stats`, `feedback_stats` tables are carried forward using the same Python constants as `seed_demo_db.py` (no CSV source exists for these). The seed script for Layer 0 imports the constants from `seed_demo_db.py` to avoid duplication.

---

## Directed School Seed URLs

URLs derivable from existing CSV data for the crawler's starting targets:

```python
SEED_URLS = [
    "https://www.cpp.edu/cba/digital-innovation/what-we-do/ai-hackathon.shtml",
    "https://www.cpp.edu/cba/ai-hackathon/index.shtml",
    "https://www.cpp.edu/",
    "https://www.insightsassociation.org/ai-hackathon",
    "https://www.insightsassociation.org/itc",
    "https://www.insightsassociation.org/ia-west-summit",
    "https://www.sdsu.edu/",
    "https://www.ucsd.edu/",
    "https://www.ucla.edu/",
    "https://www.pdx.edu/",  # Portland State
]
```

These come from `data_cpp_events_contacts.csv`'s `Public URL` column and the universities listed in `data_event_calendar.csv`'s `Nearby Universities` column.

---

## Common Pitfalls

### Pitfall 1: asyncio.Queue blocks when SSE consumer disconnects mid-crawl
**What goes wrong:** The background crawler task keeps `await _crawler_queue.put()` indefinitely if the SSE consumer has disconnected and nobody is draining the queue.
**Why it happens:** The queue has no size limit by default (unbounded). The background task will eventually finish and put None (done sentinel), but until then the queue grows.
**How to avoid:** Create the queue with `asyncio.Queue(maxsize=100)`. The crawler uses `put_nowait()` with a try/except `asyncio.QueueFull` to drop events when no consumer is connected.
**Warning signs:** Memory grows during crawl without visible consumer.

### Pitfall 2: seed_smartmatch_db.py drops and recreates on every startup
**What goes wrong:** If `main.py` calls the seed script on startup unconditionally, every restart wipes the persistent database — defeating the purpose of Layer 0.
**Why it happens:** `seed_demo_db.py` always drops and recreates (appropriate for demo.db which is always from constants). `seed_smartmatch_db.py` must not do this.
**How to avoid:** Check `if SMARTMATCH_DB_PATH.exists()` at the start of `main()`. Only seed if missing. Add a `--force` CLI flag for explicit recreation.
**Warning signs:** `source: "live"` never appears even after seeding.

### Pitfall 3: `requests.get()` blocking calls inside async FastAPI
**What goes wrong:** Using synchronous `requests` inside `async def _run_crawl()` blocks the entire event loop during HTTP requests.
**Why it happens:** FastAPI runs on an asyncio event loop; synchronous I/O blocks all other coroutines while waiting.
**How to avoid:** Either use `asyncio.get_event_loop().run_in_executor(None, requests.get, url)` or use `httpx` with `async with httpx.AsyncClient()`. For the seed URL list which is short (10-20 URLs), `run_in_executor` is the simplest fix.
**Warning signs:** SSE feed freezes for several seconds between events.

### Pitfall 4: `_load_rows_with_fallback` signature change breaks existing callers
**What goes wrong:** `data.py` currently calls `_load_rows_with_fallback(loader, demo_loader)` with 2 args. Changing to 3 args without updating all call sites breaks every endpoint.
**Why it happens:** The existing function signature must be extended, not replaced.
**How to avoid:** Make `csv_loader` a required third positional argument. Update all 4-5 call sites in `data.py` in the same commit. Check `calendar.py`, `qr.py`, `feedback.py` for any local fallback patterns that also need 3-layer updates.
**Warning signs:** `TypeError: _load_rows_with_fallback() takes 2 positional arguments but 3 were given`.

### Pitfall 5: Gemini API grounding not available on free tier
**What goes wrong:** The `googleSearch` grounding tool returns a 400 or 403 error if the API key does not have grounding enabled.
**Why it happens:** Google Search grounding is a paid feature on some Gemini API tiers.
**How to avoid:** Wrap Gemini search in try/except. If `GeminiAPIError` is raised, fall through to Tavily. If both fail, use the seed URL list directly with a simulated "found" status.
**Warning signs:** Crawler immediately produces all-error events.

### Pitfall 6: EventSource CORS issue with Vite dev proxy
**What goes wrong:** Browser `EventSource` ignores the Vite proxy and hits `localhost:5173/api/crawler/feed` directly, which fails.
**Why it happens:** `EventSource` does not use `fetch` or `XMLHttpRequest` — it uses the browser's native streaming, which respects the origin header but not Vite's dev proxy configuration by default.
**How to avoid:** Vite's `server.proxy` config already proxies `/api` to `http://127.0.0.1:8000`. The `EventSource` constructor must use a relative URL (`/api/crawler/feed`), not an absolute URL. Verify `vite.config.ts` has `/api` proxy configured.
**Warning signs:** Console error `GET http://localhost:5173/api/crawler/feed` returns HTML (Vite's 404 page) instead of `text/event-stream`.

---

## Code Examples

### SSE Endpoint (manual StreamingResponse)
```python
# Source: FastAPI docs + verified pattern
# src/api/routers/crawler.py

import asyncio
import json
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse

router = APIRouter()
_crawler_queue: asyncio.Queue[dict | None] = asyncio.Queue(maxsize=100)

async def _event_stream() -> AsyncIterator[str]:
    while True:
        try:
            event = await asyncio.wait_for(_crawler_queue.get(), timeout=30.0)
        except asyncio.TimeoutError:
            yield ": keepalive\n\n"  # SSE comment keeps connection alive
            continue
        if event is None:
            yield 'data: {"status": "done"}\n\n'
            break
        yield f"data: {json.dumps(event)}\n\n"

@router.get("/feed")
async def crawler_feed() -> StreamingResponse:
    return StreamingResponse(
        _event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

### React EventSource with Cleanup
```typescript
// Source: MDN EventSource API
// frontend/src/app/components/CrawlerFeed.tsx

useEffect(() => {
  if (!isActive) return;
  const es = new EventSource("/api/crawler/feed");
  es.onmessage = (e) => {
    const data = JSON.parse(e.data) as CrawlerEvent;
    if (data.status === "done") { es.close(); setIsActive(false); return; }
    setEvents((prev) => [data, ...prev].slice(0, 50)); // Keep last 50
  };
  es.onerror = () => { es.close(); };
  return () => es.close();
}, [isActive]);
```

### 3-Layer Fallback Chain
```python
# src/api/routers/data.py (updated signature)
def _load_rows_with_fallback(
    live_loader: Callable[[], list[dict[str, Any]]],
    demo_loader: Callable[[], list[dict[str, Any]]],
    csv_loader: Callable[[], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    for loader, tag in [
        (live_loader, "live"),
        (demo_loader, "demo"),
        (csv_loader, "csv"),
    ]:
        try:
            rows = loader()
            if rows:
                return [{**row, "source": tag} for row in rows]
        except Exception:
            pass
    return []

# Updated endpoint:
@router.get("/specialists")
async def specialists() -> list[dict]:
    return _load_rows_with_fallback(
        load_live_specialists,   # Layer 0
        load_demo_specialists,   # Layer 1
        load_specialists,        # Layer 2 (CSV)
    )
```

### Seed Script Guard Pattern
```python
# scripts/seed_smartmatch_db.py
def main(*, force: bool = False) -> None:
    if SMARTMATCH_DB_PATH.exists() and not force:
        with sqlite3.connect(str(SMARTMATCH_DB_PATH)) as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
            ).fetchone()[0]
        if count > 0:
            print(f"smartmatch.db already seeded ({count} tables). Use --force to reseed.")
            return
    # ... create and seed
```

### Gemini REST Web Search
```python
# Extension to src/gemini_client.py
def web_search(
    query: str,
    *,
    api_key: str,
    model: str = "gemini-2.0-flash",
    timeout: float = 30.0,
) -> list[dict[str, str]]:
    """Return list of {url, title} from Gemini Google Search grounding."""
    payload = {
        "contents": [{"parts": [{"text": query}], "role": "user"}],
        "tools": [{"googleSearch": {}}],
    }
    response = _post_json(
        f"v1beta/models/{model}:generateContent",
        payload,
        api_key=api_key,
        timeout=timeout,
    )
    candidates = response.get("candidates", [])
    if not candidates:
        return []
    metadata = candidates[0].get("groundingMetadata", {})
    chunks = metadata.get("groundingChunks", [])
    return [
        {"url": c["web"]["uri"], "title": c["web"].get("title", "")}
        for c in chunks
        if "web" in c
    ]
```

### Tavily Search
```python
# src/api/routers/crawler.py
from tavily import TavilyClient

def _tavily_search(query: str, api_key: str) -> list[dict[str, str]]:
    client = TavilyClient(api_key=api_key)
    response = client.search(query)
    results = response.get("results", [])
    return [{"url": r.get("url", ""), "title": r.get("title", "")} for r in results]
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `google-generativeai` SDK | `google-genai` SDK | Nov 2025 (deprecated) | Old package is deprecated; use `pip install google-genai` if SDK needed |
| SSE via third-party `sse-starlette` | FastAPI native `EventSourceResponse` | FastAPI 0.135.0 | Project pins >=0.115.0, so use StreamingResponse manually |
| Gemini REST endpoint: `v1beta/models/...` | Same (stable endpoint) | N/A | No change needed; existing gemini_client.py uses v1beta already |
| Tavily `search()` returns flat results | Same (confirmed 0.7.23) | N/A | `response["results"]` is a list of `{url, title, content, ...}` dicts |

**Deprecated/outdated:**
- `google-generativeai` package: deprecated Nov 30, 2025; replaced by `google-genai`
- `fastapi.sse.EventSourceResponse`: not available in fastapi<0.135.0

---

## Open Questions

1. **Gemini grounding tier availability**
   - What we know: The project's existing `GEMINI_API_KEY` is configured and used for embeddings
   - What's unclear: Whether this key has Google Search grounding enabled (paid tier feature)
   - Recommendation: Wrap in try/except and fall through to Tavily if grounding returns an error. Test at start of Plan 17-02 implementation.

2. **`calendar_events` / `calendar_assignments` CSV source**
   - What we know: These tables exist in demo.db seeded from Python constants; no CSV file provides this data
   - What's unclear: Should Layer 0 seed these from the same Python constants or skip them?
   - Recommendation: Import constants from `seed_demo_db.py` and reuse them in `seed_smartmatch_db.py`. This keeps the seeded content identical and avoids duplication.

3. **routers beyond `data.py` that need Layer 0**
   - What we know: `calendar.py`, `qr.py`, `feedback.py` also use demo_db fallbacks
   - What's unclear: Whether the CONTEXT.md "all existing routers" requirement means updating calendar/qr/feedback too
   - Recommendation: Check each router for `load_demo_*` imports. If present, update to 3-layer fallback. `calendar.py` definitely needs it (uses `load_demo_calendar_events`). `qr.py` and `feedback.py` use `_load_json_payload` pattern which is slightly different — treat as separate but parallel update.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.3.4 |
| Config file | none — run from project root |
| Quick run command | `pytest tests/ -x -q` |
| Full suite command | `pytest tests/ --cov=src --cov-report=term-missing` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DB-01 | smartmatch.db created and queried by load_live_* | unit | `pytest tests/test_smartmatch_db.py -x` | Wave 0 |
| DB-02 | All CSV datasets imported into correct tables | unit | `pytest tests/test_seed_smartmatch_db.py -x` | Wave 0 |
| DB-03 | 3-layer fallback returns `source: live/demo/csv` correctly | unit | `pytest tests/test_data_router.py -x` | Wave 0 |
| DB-04 | insert_crawler_event() writes to web_crawler_events table | unit | `pytest tests/test_smartmatch_db.py::test_insert_crawler_event -x` | Wave 0 |
| CRAWLER-01 | /api/crawler/feed returns text/event-stream | integration | `pytest tests/test_crawler_router.py::test_feed_returns_sse -x` | Wave 0 |
| CRAWLER-02 | CrawlerFeed component renders events from SSE | manual-only | N/A — React component, requires browser | manual |
| CRAWLER-03 | POST /api/crawler/start returns 200 and triggers background task | integration | `pytest tests/test_crawler_router.py::test_start_crawl -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_smartmatch_db.py tests/test_seed_smartmatch_db.py tests/test_crawler_router.py -x -q`
- **Per wave merge:** `pytest tests/ --cov=src --cov-report=term-missing`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_smartmatch_db.py` — covers DB-01, DB-04
- [ ] `tests/test_seed_smartmatch_db.py` — covers DB-02 (uses tmp_path fixture to avoid writing to real data/)
- [ ] `tests/test_data_router.py` — covers DB-03 (mock all three loaders)
- [ ] `tests/test_crawler_router.py` — covers CRAWLER-01, CRAWLER-03

---

## Sources

### Primary (HIGH confidence)
- FastAPI official docs (https://fastapi.tiangolo.com/tutorial/server-sent-events/) — SSE patterns, EventSourceResponse, StreamingResponse
- PyPI tavily-python (https://pypi.org/project/tavily-python/) — version 0.7.23, install command
- PyPI google-genai (https://pypi.org/project/google-genai/) — version 1.68.0, async support
- Google AI Gemini Grounding docs (https://ai.google.dev/gemini-api/docs/google-search) — googleSearch tool, groundingMetadata structure
- Project source code (demo_db.py, seed_demo_db.py, data.py, main.py, data_helpers.py) — verified directly

### Secondary (MEDIUM confidence)
- WebSearch: FastAPI EventSourceResponse added in 0.135.0 — confirmed with official docs reference
- WebSearch: tavily-python TavilyClient.search() result format `response["results"]` — confirmed on PyPI page

### Tertiary (LOW confidence)
- Gemini grounding tier requirement (paid feature) — mentioned in search results but not explicitly documented in official pricing page checked

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages verified on PyPI, project dependencies confirmed in requirements.txt
- Architecture: HIGH — patterns directly derived from existing project code (demo_db.py, seed_demo_db.py, data.py)
- SSE pattern: HIGH — official FastAPI docs confirm StreamingResponse approach; EventSourceResponse version constraint confirmed
- Pitfalls: HIGH — asyncio blocking pitfall is a well-documented FastAPI issue; seed script idempotency derived from project context
- Gemini grounding availability: LOW — tier restrictions unverified for the project's API key

**Research date:** 2026-03-27
**Valid until:** 2026-04-27 (stable libraries; Gemini API endpoints may change)
