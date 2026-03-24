---
phase: 08-frontend-ui-redesign
plan: "03"
subsystem: ui
tags: [landing-page, html, tailwind, streamlit, data-integration]
dependency_graph:
  requires: [08-01, 08-02]
  provides: [landing-page-v2]
  affects: [app entrypoint, page_router navigation]
tech_stack:
  added: []
  patterns:
    - f-string HTML body builder injected into render_html_page()
    - load_specialists() + name-search fallback for dynamic data injection
    - SVG segmented donut chart via stroke-dasharray inline in HTML
    - Streamlit buttons below HTML component for navigation
key_files:
  created:
    - "Category 3 - IA West Smart Match CRM/src/ui/landing_page_v2.py"
  modified: []
decisions:
  - "External googleusercontent heatmap image replaced with CSS gradient placeholder div — no external runtime image dependencies"
  - "Sign in nav button uses postMessage JS for HTML-layer interaction; primary navigation remains via Streamlit buttons below the component"
  - "Travis Miller lookup uses case-insensitive name search with hardcoded fallback dict for resilience when data file is missing"
metrics:
  duration_minutes: 5
  completed_date: "2026-03-24"
  tasks_completed: 1
  tasks_total: 1
  files_created: 1
  files_modified: 0
---

# Phase 08 Plan 03: Landing Page v2 Summary

**One-liner:** Pixel-faithful landing page reproducing the ia_smartmatch_landing_page_updated mockup, rendered via st.components.v1.html() with real Travis Miller specialist data and SVG donut chart.

## Objective

Replace the st.markdown-based landing_page.py with a true full-page HTML experience. The new `render_landing_page_v2()` function builds the full mockup body as a Python f-string, injects real specialist data from `data_helpers.load_specialists()`, and delegates rendering to `render_html_page()` from Plan 01.

## Tasks Completed

| # | Task | Commit | Files |
|---|------|--------|-------|
| 1 | Build landing_page_v2.py — full HTML landing page | 4bf1527 | src/ui/landing_page_v2.py (created, 531 lines) |

## Output

`src/ui/landing_page_v2.py` exports `render_landing_page_v2()`.

### Sections reproduced from mockup

- Glass nav bar (fixed top, Sign in postMessage button)
- Hero section ("Match your specialist database with every university opportunity")
- Product preview bento: UCLA Career Fair 2026 + Travis Miller (real data) + Bridge Logic panel
- Features grid: 3 columns — Proprietary Web Scraping, Industry Specialist CRM, Bridge Matching
- 6-factor MATCH_SCORE section with SVG segmented donut chart (stroke-dasharray)
- Automation pipeline visual (scrape → parse → sync CRM)
- Analytics dashboard: heatmap placeholder + matching funnel
- Partner showcase: CPP, UCLA, SDSU, UC DAVIS, USC, PORTLAND STATE
- Final CTA
- Footer

### Data wiring

`load_specialists()` is called at render time. `_get_travis_miller()` searches for a case-insensitive "travis" match and falls back to a hardcoded dict if the CSV is missing. The specialist's `name`, `title`, `company`, and `initials` are injected into the HTML body via f-string.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] Gradient placeholder for heatmap image**
- **Found during:** Task 1
- **Issue:** The mockup references a `https://lh3.googleusercontent.com/...` heatmap image that would be blocked or unavailable at runtime.
- **Fix:** Replaced `<img>` tag with a `<div>` using a CSS gradient background. Preserves layout and visual intent without external dependency.
- **Files modified:** src/ui/landing_page_v2.py
- **Commit:** 4bf1527 (inline with task)

## Known Stubs

None. All content is structural (mockup HTML) or wired to real data (Travis Miller from CSV). The heatmap is intentionally a placeholder per the plan's instructions ("replace with placeholder colored divs").

## Self-Check: PASSED

- FOUND: Category 3 - IA West Smart Match CRM/src/ui/landing_page_v2.py
- FOUND: commit 4bf1527
