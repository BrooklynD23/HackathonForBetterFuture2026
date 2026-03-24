# Testing Patterns

**Analysis Date:** 2026-03-20

## Test Framework

**Runner:**
- `pytest` (declared as `pytest==8.3.4` in `Category 3 - IA West Smart Match CRM/requirements.txt`)
- Config: Not detected. `Category 3 - IA West Smart Match CRM/` does not contain `pytest.ini`, `pyproject.toml`, or `tox.ini`, so test discovery and options come from direct command invocation.

**Assertion Library:**
- Native `assert` statements plus `pytest.raises(...)`; see `tests/test_similarity.py`, `tests/test_data_loader.py`, and `tests/test_scraper.py`.

**Run Commands:**
```bash
./.venv/bin/python -m pytest -q
./.venv/bin/python -m pytest tests/test_<module>.py -q
./.venv/bin/python -m pytest --cov=src --cov-report=term-missing
```

**Current Baseline:**
- Direct inventory check from `Category 3 - IA West Smart Match CRM/`: `timeout 60s ./.venv/bin/python -m pytest --collect-only -q` collected 378 tests.
- Direct smoke slice from `Category 3 - IA West Smart Match CRM/`: `timeout 60s ./.venv/bin/python -m pytest tests/test_config.py tests/test_app.py tests/test_sprint4_preflight.py -q` passed with 7 tests.
- Historical docs such as `Category 3 - IA West Smart Match CRM/docs/README.md` and `Category 3 - IA West Smart Match CRM/docs/sprints/README.md` still mention older pass counts. Treat live command output as the authority.

## Test File Organization

**Location:**
- Keep automated tests in `Category 3 - IA West Smart Match CRM/tests/`.
- Keep manual verification artifacts in `Category 3 - IA West Smart Match CRM/docs/testing/`.
- Keep deployment/demo preflight logic in `Category 3 - IA West Smart Match CRM/scripts/` with direct tests in `Category 3 - IA West Smart Match CRM/tests/test_sprint4_preflight.py`.

**Naming:**
- Name modules `test_<feature>.py`, aligned to the source file or feature contract: `tests/test_engine.py`, `tests/test_llm_extractor.py`, `tests/test_demo_mode.py`, `tests/test_pipeline_tab.py`.
- Shared cross-suite bootstrapping belongs in `tests/conftest.py`.

**Structure:**
```text
Category 3 - IA West Smart Match CRM/
├── src/
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_engine.py
│   ├── test_scraper.py
│   └── test_sprint4_preflight.py
├── docs/testing/
│   ├── test_log.md
│   ├── bug_log.md
│   └── rehearsal_log.md
└── scripts/
    └── sprint4_preflight.py
```

## Test Structure

**Suite Organization:**
```python
@pytest.fixture()
def mock_speakers_df() -> pd.DataFrame:
    return pd.DataFrame([...])


class TestComputeMatchScore:
    def test_returns_required_keys(self, mock_calendar_df: pd.DataFrame) -> None:
        result = compute_match_score(...)
        assert "total_score" in result
```

**Patterns:**
- Group tests by behavior inside `class Test...:` containers, with file-level banner comments separating fixtures, unit areas, and regression sections; see `tests/test_engine.py`, `tests/test_scraper.py`, and `tests/test_data_loader.py`.
- Keep fixtures close to the tests that use them. Most data factories live in the same module as the tests, while `tests/conftest.py` is reserved for the shared Streamlit stub.
- Use deterministic pandas and NumPy inputs instead of hidden global fixtures. Examples: `tests/test_engine.py`, `tests/test_pipeline_tab.py`, and `tests/test_volunteer_dashboard.py`.
- Add regression tests directly next to the failure mode that motivated them. `tests/test_scraper.py`, `tests/test_llm_extractor.py`, and `tests/test_sprint4_preflight.py` all encode post-review bug fixes this way.

## Mocking

**Framework:** `unittest.mock` (`patch`, `MagicMock`, `AsyncMock`) plus `pytest` `monkeypatch`

**Patterns:**
```python
@patch("src.extraction.llm_extractor.generate_text", return_value=MOCK_LLM_RESPONSE)
def test_returns_list(self, mock_gen: object) -> None:
    events = extract_events(SAMPLE_HTML, university="UCLA", url="https://career.ucla.edu/events/")
    assert len(events) == 1
```

```python
@patch("streamlit.session_state", new_callable=dict)
def test_render_pipeline_tab_prefers_real_data(self, mock_state: dict, monkeypatch: pytest.MonkeyPatch) -> None:
    import src.ui.pipeline_tab as mod
    monkeypatch.setattr(mod.st, "plotly_chart", lambda *args, **kwargs: None)
```

**What to Mock:**
- Mock Gemini calls at the module import site, for example `src.extraction.llm_extractor.generate_text` and `src.matching.explanations.generate_text`.
- Mock HTTP, DNS, robots, and Playwright in scraper tests. `tests/test_scraper.py` patches `requests.get`, `socket.getaddrinfo`, `RobotFileParser`, and async Playwright APIs.
- Mock Streamlit UI methods and `streamlit.session_state` for UI tests. `tests/conftest.py` creates a fake `streamlit` module before `src` imports, and individual UI tests refine behavior with `patch` or `monkeypatch`.
- Mock filesystem destinations with `tmp_path` when testing caches, CSV outputs, or generated artifacts.

**What NOT to Mock:**
- Do not mock the scoring math when testing `src/matching/engine.py` or `src/matching/factors.py`. Those tests intentionally run real pandas/NumPy logic with deterministic inputs.
- Do not replace real DataFrame aggregation in pipeline, volunteer, or quality-report tests unless the test is specifically about caller orchestration.
- Do not bypass the checked-in fixture files for Demo Mode existence/shape checks. `tests/test_demo_mode.py` treats `cache/demo_fixtures/*.json` as a repo contract.

## Fixtures and Factories

**Test Data:**
```python
SPEAKER_CSV = textwrap.dedent("""\
    Name,Board Role,Metro Region,Company,Title,Expertise Tags
    Alice Smith,President,Los Angeles — West,AcmeCo,SVP Sales,"sales, innovation"
""")


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    (tmp_path / "data_speaker_profiles.csv").write_text(SPEAKER_CSV, encoding="utf-8")
    return tmp_path
```

**Location:**
- Inline CSV strings and DataFrame fixtures live inside the owning test file, especially in `tests/test_data_loader.py`, `tests/test_engine.py`, and `tests/test_pipeline_tab.py`.
- Shared Streamlit bootstrapping lives in `tests/conftest.py`.
- Demo-mode golden fixtures live in `Category 3 - IA West Smart Match CRM/cache/demo_fixtures/` and are validated by `tests/test_demo_mode.py`.

## Coverage

**Requirements:** None enforced by checked-in tooling. There is no committed coverage gate or config file.
- Sprint orchestration docs under `Category 3 - IA West Smart Match CRM/docs/sprints/sprint-2-swarm-orchestration-plan.md` and `Category 3 - IA West Smart Match CRM/docs/sprints/sprint-3-swarm-orchestration-plan.md` prescribe `--cov=src --cov-report=term-missing` and treat 80%+ as the phase target.

**View Coverage:**
```bash
./.venv/bin/python -m pytest --cov=src --cov-report=term-missing
```

## Test Types

**Unit Tests:**
- The dominant test type. Most modules in `Category 3 - IA West Smart Match CRM/src/` have a direct unit-test peer under `Category 3 - IA West Smart Match CRM/tests/`.
- Unit tests cover scoring, config validation, cache IO, prompt shaping, UI helper logic, and runtime-state normalization.

**Integration Tests:**
- Light integration coverage exists for module boundaries and script loading rather than true external-service runs.
- Examples include `tests/test_app.py` for embedding bootstrap orchestration, `tests/test_pipeline_tab.py` for runtime-state vs CSV fallback behavior, and `tests/test_sprint4_preflight.py` for script import and prewarm wiring.
- No active `@pytest.mark.integration` configuration is checked in.

**E2E Tests:**
- Browser E2E automation is not part of the committed regression suite.
- Manual E2E is the repository standard for ship-readiness: `Category 3 - IA West Smart Match CRM/docs/sprints/sprint-4-ship.md` defines the 21-step checklist, while `docs/testing/test_log.md`, `docs/testing/bug_log.md`, and `docs/testing/rehearsal_log.md` capture execution evidence.
- `scripts/capture_screenshots.py` and `docs/screenshots/README.md` use Playwright for screenshot capture, not as a formal E2E test harness.

## Common Patterns

**Async Testing:**
```python
mock_page = AsyncMock()
mock_browser = AsyncMock()
mock_pw_ctx = AsyncMock()
mock_pw_ctx.__aenter__ = AsyncMock(return_value=mock_pw)
```
- Follow the pattern in `tests/test_scraper.py` when isolating Playwright-backed code.

**Error Testing:**
```python
with pytest.raises(ValueError, match="Localhost"):
    validate_public_demo_url("http://localhost/evil")
```

```python
df = load_pipeline_data("missing.csv")
assert df.empty
```
- Use `pytest.raises(...)` for true contract violations and empty containers for recoverable fallbacks, mirroring the production behavior in `src/scraping/scraper.py`, `src/config.py`, and `src/ui/pipeline_tab.py`.

## Verification Workflow

- Run targeted module tests first, then the full suite from `Category 3 - IA West Smart Match CRM/` using `./.venv/bin/python -m pytest -q`.
- For deployment, demo, or cache-contract changes, run the preflight script as part of verification:
```bash
./.venv/bin/python scripts/sprint4_preflight.py
./.venv/bin/python scripts/sprint4_preflight.py --json-out docs/testing/preflight_report.json
./.venv/bin/python scripts/sprint4_preflight.py --prewarm-discovery
```
- Use `streamlit run src/app.py` as the smoke-launch command before manual rehearsal or screenshot capture, per `Category 3 - IA West Smart Match CRM/docs/README.md` and `Category 3 - IA West Smart Match CRM/docs/screenshots/README.md`.
- When work affects sprint execution or closeout, preserve the manual evidence loop from `Agents.md`, `tasks/todo.md`, and `Category 3 - IA West Smart Match CRM/docs/sprints/sprint-4-ship.md`:
  - Update the execution board in `tasks/todo.md`.
  - Record review evidence before marking work complete.
  - Keep `docs/testing/test_log.md`, `docs/testing/bug_log.md`, and `docs/testing/rehearsal_log.md` in sync with any rehearsal or ship-readiness activity.
- Current direct preflight evidence shows the script exits successfully while treating missing warmed caches and embedding artifacts as warnings, not failures. Future phases should preserve that warning-only behavior unless they intentionally change the ship contract in `scripts/sprint4_preflight.py`.

---

*Testing analysis: 2026-03-20*
