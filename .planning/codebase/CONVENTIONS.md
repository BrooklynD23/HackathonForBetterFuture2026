# Coding Conventions

**Analysis Date:** 2026-03-20

## Naming Patterns

**Files:**
- Use `snake_case.py` for Python modules under `Category 3 - IA West Smart Match CRM/src/` and `Category 3 - IA West Smart Match CRM/tests/`; examples: `src/runtime_state.py`, `src/ui/matches_tab.py`, `tests/test_pipeline_tab.py`.
- Name test modules `test_<module>.py` and keep them aligned with the production module or feature area they cover; examples: `tests/test_scraper.py`, `tests/test_llm_extractor.py`, `tests/test_sprint4_preflight.py`.
- Name cached fixture and artifact files with stable snake_case JSON/CSV names; examples: `cache/demo_fixtures/discovery_scan.json`, `cache/demo_fixtures/pipeline_funnel.json`, `data/pipeline_sample_data.csv`.

**Functions:**
- Use `snake_case` verbs for all public functions: `load_all()`, `validate_config()`, `render_pipeline_tab()`, `generate_outreach_email()`, `compute_match_score()`.
- Prefix internal helpers with `_` when they exist only to support one module: `_embedding_cache_issues()` in `src/app.py`, `_cache_key()` in `src/extraction/llm_extractor.py`, `_resolve_validated_ips()` in `src/scraping/scraper.py`.
- Reserve `render_*` for Streamlit UI entry points, `load_*`/`save_*` for disk or cache IO, `init_*` for session-state setup, and `compute_*`/`generate_*` for pure or mostly pure business logic.

**Variables:**
- Use `snake_case` for locals and parameters, including Streamlit session-state keys such as `"match_results_df"`, `"scraped_events"`, `"feedback_log"`, and `"demo_mode"` in `src/runtime_state.py`, `src/feedback/acceptance.py`, and `src/app.py`.
- Use `UPPER_SNAKE_CASE` for module constants and schema maps: `DEFAULT_WEIGHTS` in `src/config.py`, `FUNNEL_STAGES` in `src/ui/pipeline_tab.py`, `EXPECTED_FIXTURE_FILES` in `tests/test_demo_mode.py`.
- Keep CSV column access literal and centralized. The code reads source fields exactly as stored in the data package, for example `"Event / Program"`, `"Volunteer Roles (fit)"`, and `"Guest Lecture Fit"` in `src/data_loader.py`, `src/matching/engine.py`, and `src/ui/matches_tab.py`.

**Types:**
- Use `PascalCase` for dataclasses and typed containers: `DataQualityResult` and `LoadedDatasets` in `src/data_loader.py`, `FeedbackEntry` in `src/feedback/acceptance.py`, `CheckResult` in `scripts/sprint4_preflight.py`.
- Add type hints broadly, including container shapes such as `dict[str, np.ndarray]`, `list[dict[str, Any]]`, and `OrderedDict[str, int]`; see `src/runtime_state.py`, `src/matching/engine.py`, and `src/ui/pipeline_tab.py`.

## Code Style

**Formatting:**
- No formatter config is checked in for the Category 3 app. `Category 3 - IA West Smart Match CRM/` does not contain `pyproject.toml`, `ruff.toml`, `.ruff.toml`, `.flake8`, `tox.ini`, `.coveragerc`, or `pytest.ini`, so future phases should match the existing file style rather than introducing a new tool contract.
- Preserve 4-space indentation, triple-quoted module docstrings, and section-divider comments. The codebase mixes banner styles such as `# ---------------------------------------------------------------------------` in `src/matching/engine.py` and `# ── Fixtures ─────────────────` in `tests/test_data_loader.py`; keep the surrounding file’s existing style.
- Keep strings ASCII unless the file already uses a deliberate Unicode token. `src/app.py` uses emoji tab labels and icon glyphs, while most backend modules stay plain ASCII.
- In `src/app.py`, keep `st.set_page_config(...)` as the first Streamlit call and leave the subsequent `from src...` imports marked with `# noqa: E402`. That ordering is part of the checked-in app contract, not accidental style drift.

**Linting:**
- No active lint config is detected. Use the source itself as the lint baseline.
- Preserve targeted suppressions already in use instead of broadening them. Examples: `# noqa: E402` in `src/app.py` and `# noqa: F401` on the `BeautifulSoup` import in `src/scraping/scraper.py`.
- Avoid style-only rewrites. `Agents.md` and `tasks/lessons.md` both favor small, targeted changes over broad cleanup.

## Import Organization

**Order:**
1. Standard-library imports first.
2. Third-party imports second.
3. Local imports from the package root `src` last.

```python
import logging
from pathlib import Path

import pandas as pd

from src.config import DATA_DIR
```

**Path Aliases:**
- Use package-root imports from `src`, not bare module imports and not relative package hops. This is explicitly required by `Category 3 - IA West Smart Match CRM/docs/README.md` and repeated throughout `src/app.py`, `src/ui/pipeline_tab.py`, and the test suite.
- For standalone scripts under `Category 3 - IA West Smart Match CRM/scripts/`, add `PROJECT_ROOT` to `sys.path` once and then import from `src`, following `scripts/sprint4_preflight.py`.
- Keep tests importing production code through the same `src...` path the application uses; examples: `tests/test_engine.py`, `tests/test_config.py`, `tests/test_pipeline_tab.py`.

## Error Handling

**Patterns:**
- Validate early and fail with clear, local errors for configuration or unsafe input. Examples: `validate_config()` in `src/config.py`, `validate_public_demo_url()` in `src/scraping/scraper.py`, and `validate_weights()` in `src/ui/matches_tab.py`.
- Prefer graceful degradation in demo-sensitive paths. `src/ui/pipeline_tab.py` returns empty DataFrames on CSV load failure, `src/extraction/llm_extractor.py` returns `[]` on malformed LLM output and falls back to extraction cache, and `src/scraping/scraper.py` returns stale cache payloads when live scraping fails.
- Surface user-facing errors through Streamlit and operational detail through logging. `src/app.py` uses `st.error(...)` plus `logger.exception(...)` before stopping, while `src/ui/styles.py` wraps API failures in `api_call_spinner()` and shows a recovery hint.
- Preserve warning-vs-failure semantics in `scripts/sprint4_preflight.py`: missing runtime or deployment files are `fail`, but unwarmed caches and missing optional demo-time artifacts are `warn`.

## Logging

**Framework:** `logging`

**Patterns:**
- Create one module logger per file with `logger = logging.getLogger(__name__)`; see `src/matching/factors.py`, `src/matching/engine.py`, `src/extraction/llm_extractor.py`, and `src/ui/pipeline_tab.py`.
- Use log levels consistently: `info` for successful major steps, `warning` for recoverable cache or API problems, `error` or `exception` for hard failures. Do not replace existing log calls with `print()`.
- If a CLI or script needs logging setup, use `configure_logging()` from `src/utils.py` instead of ad hoc formatting.
- The one intentional plain-text report path is `scripts/sprint4_preflight.py`, which prints a final human-readable report after collecting structured `CheckResult` objects.

## Comments

**When to Comment:**
- Start modules with a concise docstring that states the file’s responsibility. This is pervasive across `src/`, `tests/`, and `scripts/`.
- Use section dividers for long modules to separate schemas, helpers, caching, validation, and public APIs; examples: `src/data_loader.py`, `src/scraping/scraper.py`, `src/extraction/llm_extractor.py`.
- Use inline comments only for non-obvious contracts or backward compatibility. Good examples include the `src/app.py` note that page config must be first, the TOCTOU explanation in `src/scraping/scraper.py`, and the cache-compatibility note around naive timestamps.

**JSDoc/TSDoc:**
- Not applicable. Use Python docstrings instead.
- Public functions often include `Args`/`Returns` or `Parameters`/`Returns` sections when the behavior is subtle; see `src/matching/engine.py`, `src/extraction/llm_extractor.py`, and `src/demo_mode.py`.

## Function Design

**Size:** `Category 3 - IA West Smart Match CRM/src/` favors functional modules with medium-sized public functions and small private helpers instead of large classes. Split new logic into focused helpers before introducing another multi-hundred-line function.

**Parameters:** Prefer explicit typed parameters over ambient globals. When a function has many arguments, callers usually switch to keyword form for readability, as in `rank_speakers_for_event(...)` calls from `src/ui/matches_tab.py` and `extract_events(...)` calls from `scripts/sprint4_preflight.py`.

**Return Values:** Return structured, typed values that downstream code can normalize without guessing:
- `list[str]` for validation errors in `src/config.py`.
- Frozen dataclasses in `src/data_loader.py`.
- `dict[str, Any]` payloads with stable keys in `src/matching/engine.py`, `src/scraping/scraper.py`, and `src/ui/pipeline_tab.py`.
- Empty DataFrames or lists instead of exceptions for recoverable UI-facing data gaps.

## Module Design

**Exports:** Prefer direct imports from leaf modules. Most packages are consumed with explicit imports such as `from src.matching.engine import ...` or `from src.ui.pipeline_tab import ...`.

**Barrel Files:** Barrel files are minimal and should stay minimal. `src/extraction/__init__.py` is the clearest example, exporting only `extract_events`, `preprocess_html`, and `EXTRACTED_EVENT_SCHEMA`. Do not add broad re-export layers unless there is a real package-boundary need.

## Repo Workflow Rules

- Before non-trivial work, review `tasks/lessons.md` and use `tasks/todo.md` as the active execution board. `Agents.md` requires checkable planning, progress tracking, a review section, and lesson capture after corrections.
- Treat `Category 3 - IA West Smart Match CRM/docs/SPRINT_PLAN.md` as the execution authority, `PRD_SECTION_CAT3.md` as the feature-detail authority, and `Category 3 - IA West Smart Match CRM/PLAN.md` as background only. This hierarchy is documented in `Category 3 - IA West Smart Match CRM/docs/README.md`, `docs/governance/REPO_REFERENCE.md`, and `docs/governance/canonical-map.yaml`.
- Preserve the Category 3 runtime contracts listed in `Category 3 - IA West Smart Match CRM/docs/README.md`:
  - Use `from src...` imports.
  - Launch with `streamlit run src/app.py`.
  - Keep cross-tab live state in `st.session_state`.
  - Keep hashed scrape, email, and explanation caches under `cache/`.
  - Ensure Demo Mode changes production call sites, not isolated helpers only.
- Favor minimal-impact fixes. `Agents.md` explicitly rejects temporary hacks and broad refactors when a targeted change will solve the problem.

---

*Convention analysis: 2026-03-20*
