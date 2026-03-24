#!/usr/bin/env python3
"""Capture screenshots of the IA West Smart Match CRM Streamlit app.

Requires: playwright (pip install playwright && playwright install chromium)
Usage:    python scripts/capture_screenshots.py [--base-url URL]

Produces 6 PNGs in docs/screenshots/ for Track B documentation:
  1. matches_tab.png
  2. discovery_tab.png
  3. pipeline_tab.png
  4. expansion_map.png
  5. volunteer_dashboard.png
  6. demo_mode.png
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import NamedTuple

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print(
        "ERROR: playwright is not installed.\n"
        "  pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(1)


class TabCapture(NamedTuple):
    """Definition of a single screenshot to capture."""

    tab_label: str
    filename: str
    wait_ms: int = 3000


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "screenshots"

VIEWPORT = {"width": 1920, "height": 1080}

TABS: list[TabCapture] = [
    TabCapture(tab_label="Matches", filename="matches_tab.png"),
    TabCapture(tab_label="Discovery", filename="discovery_tab.png"),
    TabCapture(tab_label="Pipeline", filename="pipeline_tab.png"),
    TabCapture(tab_label="Expansion", filename="expansion_map.png", wait_ms=5000),
    TabCapture(tab_label="Volunteers", filename="volunteer_dashboard.png"),
]


def _click_tab(page, label: str) -> None:
    """Click a Streamlit tab by its visible text (ignoring emoji prefix)."""
    tab_btn = page.locator(f'button[role="tab"]:has-text("{label}")')
    tab_btn.click()


def _wait_for_content(page, ms: int) -> None:
    """Wait for Streamlit content to render."""
    time.sleep(ms / 1000)
    # Also wait for any Streamlit spinner to disappear
    try:
        page.wait_for_selector(
            '[data-testid="stSpinner"]', state="hidden", timeout=10_000
        )
    except PWTimeout:
        pass


def capture_all(base_url: str) -> list[Path]:
    """Launch browser, navigate app, and capture all screenshots.

    Returns list of saved file paths.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport=VIEWPORT)
        page = context.new_page()

        # Navigate to app
        print(f"Navigating to {base_url} ...")
        page.goto(base_url, wait_until="networkidle", timeout=30_000)
        _wait_for_content(page, 3000)

        # Capture each tab
        for tab in TABS:
            print(f"  Capturing {tab.filename} (tab: {tab.tab_label}) ...")
            _click_tab(page, tab.tab_label)
            _wait_for_content(page, tab.wait_ms)
            out_path = OUTPUT_DIR / tab.filename
            page.screenshot(path=str(out_path), full_page=False)
            saved.append(out_path)

        # Capture demo mode: toggle the checkbox then screenshot the Matches tab
        print("  Capturing demo_mode.png ...")
        demo_checkbox = page.locator('label:has-text("Demo Mode")')
        demo_checkbox.click()
        _wait_for_content(page, 2000)
        _click_tab(page, "Matches")
        _wait_for_content(page, 3000)
        out_path = OUTPUT_DIR / "demo_mode.png"
        page.screenshot(path=str(out_path), full_page=False)
        saved.append(out_path)

        browser.close()

    return saved


def _verify(saved: list[Path]) -> bool:
    """Check that all screenshots exist and are >100 KB."""
    ok = True
    for p in saved:
        if not p.exists():
            print(f"  FAIL: {p.name} missing", file=sys.stderr)
            ok = False
            continue
        size_kb = p.stat().st_size / 1024
        status = "OK" if size_kb > 100 else "WARN (<100 KB)"
        print(f"  {p.name}: {size_kb:.0f} KB  [{status}]")
        if size_kb <= 100:
            ok = False
    return ok


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default="http://localhost:8501",
        help="Streamlit app URL (default: http://localhost:8501)",
    )
    args = parser.parse_args()

    saved = capture_all(args.base_url)

    print("\nVerification:")
    if _verify(saved):
        print("\nAll 6 screenshots captured successfully.")
    else:
        print("\nSome screenshots may need attention.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
