# External Integrations

**Analysis Date:** 2026-03-20

## APIs & External Services

**LLM and Embeddings:**
- Gemini Developer API - Used for embeddings, structured event extraction, match explanations, and outreach email generation.
  - SDK/Client: Direct REST wrapper in `Category 3 - IA West Smart Match CRM/src/gemini_client.py` using stdlib `urllib`; current callers are `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, and `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`.
  - Auth: `GEMINI_API_KEY`
  - Boundary: Keep raw Gemini request/response shaping inside `Category 3 - IA West Smart Match CRM/src/gemini_client.py`. Feature modules should call `batch_embed_texts()` or `generate_text()`, not hand-roll new HTTP clients.
  - Current models: `gemini-embedding-001` and `gemini-2.5-flash-lite`, defined in `Category 3 - IA West Smart Match CRM/src/config.py` and documented in `Category 3 - IA West Smart Match CRM/docs/gemini_provider_decision_2026-03-18.md`.

**Public University Event Websites:**
- UCLA, SDSU, UC Davis, USC, and Portland State event pages - Used as discovery targets in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`.
  - SDK/Client: `requests`, `urllib.robotparser`, `BeautifulSoup`, and optional `playwright.async_api`
  - Auth: None; only public pages are allowed
  - Boundary: Discovery UI in `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py` must go through `scrape_university()` and then `extract_events()`. URL validation, robots checks, IP validation, rate limiting, and stale-cache fallback all live in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`.

**Custom Public University URLs:**
- User-entered `.edu` URLs in the Discovery tab - Used for demo-scoped ad hoc discovery.
  - SDK/Client: Same discovery stack as the built-in university targets
  - Auth: None
  - Boundary: Validation is intentionally restrictive in `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py` and `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`: only `http/https`, no localhost/private-network targets, and public university hosts only.

**Hosting and Secret Injection:**
- Streamlit Community Cloud - Intended public hosting target for the app.
  - SDK/Client: Streamlit runtime and `st.secrets` via `Category 3 - IA West Smart Match CRM/src/config.py`
  - Auth: Streamlit secrets dashboard or local `.streamlit/secrets.toml`
  - Boundary: Runtime assumptions are documented in `Category 3 - IA West Smart Match CRM/runtime.txt`, `Category 3 - IA West Smart Match CRM/.streamlit/config.toml`, `Category 3 - IA West Smart Match CRM/docs/testing/README.md`, and `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`.

**Browser Automation:**
- Playwright Chromium - Used locally for JS-rendered page scraping and screenshot capture, not as a hosted SaaS dependency.
  - SDK/Client: `playwright` in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` and `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`
  - Auth: None
  - Boundary: Treat this as a local tooling dependency. The closeout docs already assume hosted deployments may need cache-first discovery instead of live Playwright execution.

**Not detected:**
- No transactional email API. `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py` generates and caches draft email content only.
- No calendar API. `Category 3 - IA West Smart Match CRM/src/outreach/ics_generator.py` creates local `.ics` content without Google or Microsoft calendar integration.
- No user auth provider, payment provider, analytics SDK, or error-tracking SaaS.

## Data Storage

**Databases:**
- None.
  - Connection: Not applicable
  - Client: File-backed storage and in-memory pandas DataFrames in `Category 3 - IA West Smart Match CRM/src/data_loader.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, and `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`

**File Storage:**
- Canonical data inputs are CSV files in `Category 3 - IA West Smart Match CRM/data/`:
  - `data_speaker_profiles.csv`
  - `data_cpp_events_contacts.csv`
  - `data_cpp_course_schedule.csv`
  - `data_event_calendar.csv`
  - `pipeline_sample_data.csv`
- Feedback persistence appends to `Category 3 - IA West Smart Match CRM/data/feedback_log.csv` by default from `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`.
- Generated screenshots are written under `Category 3 - IA West Smart Match CRM/docs/screenshots/` by `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`.
- Demo artifacts live under `Category 3 - IA West Smart Match CRM/cache/demo_fixtures/`.

**Caching:**
- Filesystem-only caches; no Redis or managed cache service.
- Embeddings:
  - `Category 3 - IA West Smart Match CRM/cache/speaker_embeddings.npy`
  - `Category 3 - IA West Smart Match CRM/cache/event_embeddings.npy`
  - `Category 3 - IA West Smart Match CRM/cache/course_embeddings.npy`
  - `Category 3 - IA West Smart Match CRM/cache/*_metadata.json`
  - `Category 3 - IA West Smart Match CRM/cache/cache_manifest.json`
- Scrapes:
  - `Category 3 - IA West Smart Match CRM/cache/scrapes/<sha256(url)>.json`
  - Owned by `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`
- Extractions:
  - `Category 3 - IA West Smart Match CRM/cache/extractions/<sha256(url)>.json`
  - Owned by `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`
- Explanations:
  - `Category 3 - IA West Smart Match CRM/cache/explanations/<speaker>__<event>__<hash>.json`
  - Owned by `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`
- Emails:
  - `Category 3 - IA West Smart Match CRM/cache/emails/<sha256(speaker,event,score)>.json`
  - Owned by `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`

## Authentication & Identity

**Auth Provider:**
- No end-user authentication provider is implemented.
  - Implementation: Single-user Streamlit app. Sensitive access is environmental only, through `GEMINI_API_KEY` and optional `st.secrets` in `Category 3 - IA West Smart Match CRM/src/config.py`.

## Monitoring & Observability

**Error Tracking:**
- None.

**Logs:**
- Standard Python `logging` is used across the runtime, especially in `Category 3 - IA West Smart Match CRM/src/app.py`, `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`, `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`, `Category 3 - IA West Smart Match CRM/src/matching/explanations.py`, and `Category 3 - IA West Smart Match CRM/src/outreach/email_gen.py`.
- User-visible operational feedback is surfaced with Streamlit status components (`st.error`, `st.warning`, `st.info`, `st.success`) in `Category 3 - IA West Smart Match CRM/src/app.py` and `Category 3 - IA West Smart Match CRM/src/ui/discovery_tab.py`.
- `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py` can emit a JSON validation report for deployment/rehearsal checks.

## CI/CD & Deployment

**Hosting:**
- Streamlit Community Cloud is the intended hosted destination, but local execution remains first-class:
  - Local run path: `streamlit run src/app.py`
  - Repo helper: `make run CAT=3` from `Makefile`
- Deployment-critical files:
  - `Category 3 - IA West Smart Match CRM/runtime.txt`
  - `Category 3 - IA West Smart Match CRM/.streamlit/config.toml`
  - `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py`

**CI Pipeline:**
- None detected. There is no `.github/workflows/` directory or other checked-in CI system definition.

## Environment Configuration

**Required env vars:**
- `GEMINI_API_KEY` - Required for live embeddings, extraction, explanations, and email generation.
- Optional runtime overrides supported by `Category 3 - IA West Smart Match CRM/src/config.py`: `GEMINI_BASE_URL`, `GEMINI_TEXT_MODEL`, `GEMINI_EMBEDDING_MODEL`, `DATA_DIR`, `CACHE_DIR`, `EMBEDDING_DIMENSION`, `EMBEDDING_BATCH_SIZE`, `EMBEDDING_MAX_RETRIES`, `STREAMLIT_PAGE_TITLE`, `STREAMLIT_PAGE_ICON`
- Optional discovery mode flag supported by `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`: `SMARTMATCH_CACHE_ONLY`

**Secrets location:**
- Local `.env` loaded by `Category 3 - IA West Smart Match CRM/src/config.py`
- Streamlit secrets via `st.secrets` in `Category 3 - IA West Smart Match CRM/src/config.py`
- Template only: `Category 3 - IA West Smart Match CRM/.env.example`
- Secret files are intentionally ignored by `.gitignore` and `Category 3 - IA West Smart Match CRM/.gitignore`

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- HTTPS POST requests to Gemini REST endpoints from `Category 3 - IA West Smart Match CRM/src/gemini_client.py`.
- HTTPS GET requests plus `robots.txt` fetches to public university domains from `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`.
- Local Playwright browser sessions to target URLs from `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` and `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`.

---

*Integration audit: 2026-03-20*
