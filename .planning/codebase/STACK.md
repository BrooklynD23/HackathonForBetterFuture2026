# Technology Stack

**Analysis Date:** 2026-03-20

## Languages

**Primary:**
- Python 3.11 deploy target, Python 3.12.3 local venv - Application code, scripts, and tests live in `Category 3 - IA West Smart Match CRM/src/`, `Category 3 - IA West Smart Match CRM/scripts/`, and `Category 3 - IA West Smart Match CRM/tests/`. Deployment is pinned by `Category 3 - IA West Smart Match CRM/runtime.txt`; the checked-in local venv is recorded in `Category 3 - IA West Smart Match CRM/.venv/pyvenv.cfg`.

**Secondary:**
- Markdown - Category 3 execution authority and closeout context live in `Category 3 - IA West Smart Match CRM/docs/README.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, `PRD_SECTION_CAT3.md`, `Category 3 - IA West Smart Match CRM/.status.md`, `Agents.md`, and `tasks/todo.md`.
- TOML - Streamlit runtime and theme configuration live in `Category 3 - IA West Smart Match CRM/.streamlit/config.toml`.
- YAML - Repo governance ownership mapping lives in `docs/governance/canonical-map.yaml`.
- CSV/JSON/NumPy artifacts - Runtime data and caches are stored under `Category 3 - IA West Smart Match CRM/data/` and `Category 3 - IA West Smart Match CRM/cache/`.

## Runtime

**Environment:**
- Local development uses CPython 3.12.3 in `Category 3 - IA West Smart Match CRM/.venv/pyvenv.cfg`.
- Deployment targets CPython 3.11 via `Category 3 - IA West Smart Match CRM/runtime.txt`.
- The supported launch command is `streamlit run src/app.py`, documented in `Category 3 - IA West Smart Match CRM/docs/README.md` and wired into `Makefile`.
- The app is a single-process Streamlit runtime with shared cross-tab state in `st.session_state`, initialized by `Category 3 - IA West Smart Match CRM/src/runtime_state.py`.

**Package Manager:**
- `pip` installs Category 3 dependencies from `Category 3 - IA West Smart Match CRM/requirements.txt`.
- Lockfile: missing.
- Shared baseline file `requirements-common.txt` exists at the repo root, but Category 3 installs from its own `Category 3 - IA West Smart Match CRM/requirements.txt`.

## Frameworks

**Core:**
- Streamlit 1.42.2 - Main UI and runtime shell in `Category 3 - IA West Smart Match CRM/src/app.py` and `Category 3 - IA West Smart Match CRM/src/ui/`.
- pandas >=2.2.3 - CSV ingestion, tabular transforms, and fallback pipeline storage in `Category 3 - IA West Smart Match CRM/src/data_loader.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, and `Category 3 - IA West Smart Match CRM/src/feedback/acceptance.py`.
- NumPy 1.26.4 - Embedding matrices and similarity math in `Category 3 - IA West Smart Match CRM/src/embeddings.py`, `Category 3 - IA West Smart Match CRM/src/similarity.py`, and `Category 3 - IA West Smart Match CRM/src/matching/`.
- Plotly 5.24.1 - Funnel, radar, map, and volunteer charts in `Category 3 - IA West Smart Match CRM/src/ui/matches_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/pipeline_tab.py`, `Category 3 - IA West Smart Match CRM/src/ui/expansion_map.py`, and `Category 3 - IA West Smart Match CRM/src/ui/volunteer_dashboard.py`.

**Testing:**
- pytest 8.3.4 - Primary test runner for `Category 3 - IA West Smart Match CRM/tests/`.
- pytest-cov >=6.0.0 - Coverage-enabled test command is exposed in `Makefile`.

**Build/Dev:**
- python-dotenv 1.0.1 - Local env loading in `Category 3 - IA West Smart Match CRM/src/config.py`.
- requests 2.32.3 + beautifulsoup4 4.12.3 - Static discovery scraping and HTML preprocessing in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` and `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`.
- Playwright 1.49.1 - Dynamic scrape fallback and screenshot automation in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` and `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py`.
- Root `Makefile` - Repo-level setup/run/test/lint entrypoints; Category 3 uses `CAT=3`.
- Not detected: `pyproject.toml`, `package.json`, GitHub Actions, Dockerfiles, `packages.txt`, or a dedicated deployment manifest beyond Streamlit files.

## Key Dependencies

**Critical:**
- `streamlit==1.42.2` - Category 3 is a Streamlit-first application, and core runtime behavior depends on `st.session_state` contracts defined in `Category 3 - IA West Smart Match CRM/src/runtime_state.py` and referenced from `Category 3 - IA West Smart Match CRM/docs/README.md`.
- `pandas>=2.2.3` - All canonical inputs are CSV-backed and loaded through `Category 3 - IA West Smart Match CRM/src/data_loader.py`.
- `numpy==1.26.4` - Embeddings are stored as `.npy` files and loaded by `Category 3 - IA West Smart Match CRM/src/embeddings.py`.
- `plotly==5.24.1` - User-facing charts are rendered throughout `Category 3 - IA West Smart Match CRM/src/ui/`.
- No Gemini SDK package is installed or required for the shipped runtime. `Category 3 - IA West Smart Match CRM/src/gemini_client.py` uses stdlib `urllib` directly against Gemini REST endpoints.

**Infrastructure:**
- `python-dotenv==1.0.1` - Supports local `.env` based configuration in `Category 3 - IA West Smart Match CRM/src/config.py`.
- `requests==2.32.3` - Performs outbound HTTP scraping in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py`.
- `beautifulsoup4==4.12.3` - Cleans and preprocesses scraped HTML in `Category 3 - IA West Smart Match CRM/src/extraction/llm_extractor.py`.
- `playwright==1.49.1` - Required for SDSU-style JS-rendered pages and local screenshot capture scripts.
- `fuzzywuzzy>=0.18.0` and `python-Levenshtein>=0.12.0` - Optional fuzzy role matching fallback in `Category 3 - IA West Smart Match CRM/src/matching/factors.py`.
- `scipy==1.14.1` and `scikit-learn>=1.5.2` are declared in `Category 3 - IA West Smart Match CRM/requirements.txt`, but they are not directly imported from the current `Category 3 - IA West Smart Match CRM/src/` tree. Treat them as dormant unless a future phase reintroduces them intentionally.

## Configuration

**Environment:**
- `Category 3 - IA West Smart Match CRM/src/config.py` calls `load_dotenv()` and reads configuration from environment variables first, then from `st.secrets` when Streamlit is loaded.
- Live Gemini-backed features require `GEMINI_API_KEY`.
- Operational overrides are templated in `Category 3 - IA West Smart Match CRM/.env.example`: `GEMINI_BASE_URL`, `GEMINI_EMBEDDING_MODEL`, `GEMINI_TEXT_MODEL`, `DATA_DIR`, `CACHE_DIR`, `EMBEDDING_DIMENSION`, `EMBEDDING_BATCH_SIZE`, `EMBEDDING_MAX_RETRIES`, `APP_ENV`, `LOG_LEVEL`, `STREAMLIT_PAGE_TITLE`, and `STREAMLIT_PAGE_ICON`.
- An additional runtime toggle, `SMARTMATCH_CACHE_ONLY`, is used in `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` to force cache-only discovery behavior.
- Secret files are intentionally ignored by both `.gitignore` at the repo root and `Category 3 - IA West Smart Match CRM/.gitignore`.

**Build:**
- `Category 3 - IA West Smart Match CRM/.streamlit/config.toml` sets theme colors, headless mode, port `8501`, and disables Streamlit usage stats.
- `Category 3 - IA West Smart Match CRM/runtime.txt` is the only checked-in runtime pin for deployment.
- `Category 3 - IA West Smart Match CRM/scripts/sprint4_preflight.py` validates runtime, required data files, cache/artifact presence, and optional discovery prewarming.
- `docs/governance/canonical-map.yaml`, `docs/governance/REPO_REFERENCE.md`, `Agents.md`, and `tasks/todo.md` are part of the execution stack for closeout work even though they do not affect app code at runtime.

## Platform Requirements

**Development:**
- Use Python with virtualenv support; the current checked-in environment is `3.12.3`, but Category 3 deployment expectations remain `3.11`.
- Install browser binaries when using Playwright-dependent paths. `Category 3 - IA West Smart Match CRM/scripts/capture_screenshots.py` explicitly expects `playwright install chromium`.
- The app assumes local read/write access to `Category 3 - IA West Smart Match CRM/data/` and `Category 3 - IA West Smart Match CRM/cache/`.

**Production:**
- Target host is Streamlit Community Cloud, as referenced by `PRD_SECTION_CAT3.md`, `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md`, and `Category 3 - IA West Smart Match CRM/docs/testing/README.md`.
- Provide `GEMINI_API_KEY` through Streamlit secrets or equivalent environment injection.
- Plan for a cache-first discovery posture on hosted deployments. `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md` and `Category 3 - IA West Smart Match CRM/src/scraping/scraper.py` both assume cached scrape artifacts can replace live Playwright scraping when cloud browser support is limited.

---

*Stack analysis: 2026-03-20*
