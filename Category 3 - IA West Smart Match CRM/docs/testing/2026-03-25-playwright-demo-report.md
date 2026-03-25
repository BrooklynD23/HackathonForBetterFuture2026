# Playwright Demo Report

## Metadata

| Field | Value |
| --- | --- |
| Date | 2026-03-25 |
| App URL | `http://127.0.0.1:8501` |
| App launch | `PYTHONPATH=. /tmp/hbf-pytest-venv/bin/streamlit run src/app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false` |
| Browser runtime | Playwright Chromium from `/tmp/hbf-pytest-venv` |
| Artifact directory | `output/playwright/` |
| Summary JSON | `output/playwright/2026-03-25-summary.json` |

## Scope

This pass covered the live routed demo flows the March 25, 2026 handoff called out:

- landing
- login
- View Demo
- deep links: `?route=matches`, `?route=coordinator&demo=1`, `?route=unknown`
- workspace nav: dashboard, matches, discovery, pipeline, analytics, match_engine
- Jarvis checkbox + text command + approve path
- sign out

## Result

Status: pass for all scripted browser checks.

- 16/16 Playwright cases passed.
- 16 screenshots were written under `output/playwright/`.
- No browser page errors were captured.
- No failed network requests were captured.
- Console output contained 10 unique warnings, all matching known iframe capability warnings or the Tailwind CDN dev warning.

## Key Findings

- Routed landing/login/demo flows now keep the URL in sync:
  - landing normalized to `?route=landing`
  - login normalized to `?route=login`
  - View Demo landed on `?route=dashboard&role=coordinator&demo=1`
- Deep links behaved correctly:
  - `?route=matches` rendered the Matches workspace
  - `?route=coordinator&demo=1` normalized to `?route=dashboard&demo=1`
  - `?route=unknown` normalized to `?route=landing`
- Workspace nav reached Dashboard, Matches, Discovery, Pipeline, Analytics, and Match Engine.
- The dashboard Jarvis checkbox now sits above the long iframe and opened the command center without layout hunting.
- Jarvis text-command flow produced a Discovery Agent proposal and completed after approval with:
  - `Found 0 event(s) (source: cache)`
- Sign out returned cleanly to landing after fixing the `demo_mode` widget-state mutation bug in `page_router.py`.

## Console Notes

Observed warnings were limited to:

- Chromium iframe feature-policy warnings for `ambient-light-sensor`, `battery`, `document-domain`, `layout-animations`, `legacy-image-formats`, `oversized-images`, `vr`, and `wake-lock`
- sandbox warning about `allow-scripts` plus `allow-same-origin`
- Tailwind CDN development warning

No application-thrown browser exceptions were observed during the pass.

## Artifacts

Screenshots:

- `output/playwright/01-landing.png`
- `output/playwright/02-login.png`
- `output/playwright/03-view-demo-dashboard.png`
- `output/playwright/04-workspace-dashboard.png`
- `output/playwright/05-workspace-matches.png`
- `output/playwright/06-workspace-discovery.png`
- `output/playwright/07-workspace-pipeline.png`
- `output/playwright/08-workspace-analytics.png`
- `output/playwright/09-workspace-match_engine.png`
- `output/playwright/10-jarvis-open.png`
- `output/playwright/11-jarvis-proposal.png`
- `output/playwright/12-jarvis-execution.png`
- `output/playwright/13-sign-out.png`
- `output/playwright/14-deep-link-matches.png`
- `output/playwright/15-deep-link-coordinator.png`
- `output/playwright/16-deep-link-unknown.png`

Machine-readable summary:

- `output/playwright/2026-03-25-summary.json`

## Follow-up / Residual Risk

- `tests/test_embeddings.py::TestGenerateEmbeddings::test_get_api_key_requires_real_gemini_key` still fails and remains outside this routing/Jarvis scope.
- Jarvis voice/TTS dependencies were absent in this environment, so the command center intentionally degraded to text-only warnings during the demo pass.
- Discovery approval completed from cache with zero events in this environment; that proves the UI path and patched tool wiring, but live discovery quality still depends on cache freshness, network reachability, and Gemini availability.

## Verification Summary

- `python3 -m py_compile src/ui/page_router.py tests/test_page_router.py tests/conftest.py scripts/run_playwright_demo_qa.py tests/test_e2e_flows.py`
- `/tmp/hbf-pytest-venv/bin/python -m pytest tests/test_page_router.py -q` -> `8 passed`
- `/tmp/hbf-pytest-venv/bin/python scripts/run_playwright_demo_qa.py` -> `16 cases`, `10 warnings`, `0 page_errors`, `0 request_failures`
- `/tmp/hbf-pytest-venv/bin/python -m pytest tests/test_e2e_flows.py -q` -> `9 passed`
- `/tmp/hbf-pytest-venv/bin/python -m pytest -q` -> `591 passed`, `1 failed` (the unrelated embeddings test above)
