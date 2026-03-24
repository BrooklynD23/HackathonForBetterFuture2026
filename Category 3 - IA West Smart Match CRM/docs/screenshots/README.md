# Track B Screenshots

Screenshots of the IA West Smart Match CRM for Track B documentation.

## Automated Capture

```bash
# Install dependencies
pip install playwright
playwright install chromium

# Start the Streamlit app (in another terminal)
streamlit run src/app.py

# Capture all 6 screenshots
python scripts/capture_screenshots.py
```

## Manual Capture (if Playwright unavailable)

1. Start the app: `streamlit run src/app.py`
2. Open http://localhost:8501 in a browser (viewport 1920x1080)
3. Capture each screenshot:

| File | How |
|------|-----|
| `matches_tab.png` | Click "Matches" tab, screenshot |
| `discovery_tab.png` | Click "Discovery" tab, screenshot |
| `pipeline_tab.png` | Click "Pipeline" tab, screenshot |
| `expansion_map.png` | Click "Expansion" tab, wait for map to render, screenshot |
| `volunteer_dashboard.png` | Click "Volunteers" tab, screenshot |
| `demo_mode.png` | Enable "Demo Mode" checkbox in sidebar, screenshot Matches tab |

Each screenshot should be at least 100 KB at 1920x1080 resolution.
