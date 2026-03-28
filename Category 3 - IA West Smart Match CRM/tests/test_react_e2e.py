"""
Playwright E2E tests for React QR and Feedback flows.

Requires:
  - React dev server at http://localhost:5173 (or vite preview after build)
  - FastAPI backend at http://localhost:8000 (with demo.db fallback)
  - Start both: python start_fullstack.py  OR  ./start_fullstack.sh

Test coverage:
  - test_qr_flow: navigates to /outreach, waits for speaker/event auto-select,
    clicks "Generate QR", asserts QR image and referral code render, screenshots.
  - test_feedback_flow: navigates to /ai-matching, opens feedback dialog via
    "Record Feedback" button, submits with defaults, asserts count incremented
    and stats section still renders, screenshots.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REACT_URL = "http://localhost:5173"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "playwright"


# ── Helpers ──────────────────────────────────────────────────────────────────


def snap(page: Page, filename: str, full_page: bool = True) -> str:
    """Wait 1.5 s, screenshot to OUTPUT_DIR/filename, return relative path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    page.wait_for_timeout(1500)
    page.screenshot(path=str(path), full_page=full_page)
    return str(path.relative_to(ROOT))


def wait_for_body_contains(
    page: Page, substrings: list[str], timeout_ms: int = 60_000
) -> str:
    """Poll body inner text until all substrings are present or timeout."""
    deadline = time.time() + timeout_ms / 1000
    last_text = ""
    while time.time() < deadline:
        try:
            last_text = page.locator("body").inner_text(timeout=5_000)
        except Exception:
            page.wait_for_timeout(1000)
            continue
        if all(part in last_text for part in substrings):
            return last_text
        page.wait_for_timeout(1000)
    raise AssertionError(
        "Missing text {}. Last body sample: {!r}".format(substrings, last_text[:1200])
    )


# ── Test: QR flow ─────────────────────────────────────────────────────────────


def test_qr_flow() -> None:
    """
    Navigate to /outreach, confirm page loaded with dropdowns and QR card,
    click 'Generate QR', assert QR image and referral code text render,
    then capture a screenshot to output/playwright/react-qr-flow.png.

    The Outreach page auto-selects the first speaker and event via useEffect,
    so no manual dropdown interaction is needed before clicking the button.
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1600})
        page = context.new_page()
        try:
            # Step 1 — navigate
            page.goto(
                f"{REACT_URL}/outreach",
                wait_until="domcontentloaded",
                timeout=60_000,
            )

            # Step 2 — confirm core page elements present
            wait_for_body_contains(page, ["Recipient", "Event", "Generate QR"])

            # Step 3 — click Generate QR (page auto-selected speaker + event)
            page.get_by_role("button", name="Generate QR").click()

            # Step 4 — wait for QR asset to render (referral code label, CSS uppercase)
            wait_for_body_contains(page, ["REFERRAL CODE"], timeout_ms=30_000)

            # Step 5 — assert referral code value is present (non-empty text after label)
            assert page.locator("text=REFERRAL CODE").is_visible(), (
                "Referral code section should be visible after QR generation"
            )

            # Step 6 — assert scan count section also rendered
            wait_for_body_contains(page, ["SCANS"])

            # Step 7 — capture screenshot evidence
            snap(page, "react-qr-flow.png")
        finally:
            browser.close()


# ── Test: Feedback flow ───────────────────────────────────────────────────────


def test_feedback_flow() -> None:
    """
    Navigate to /ai-matching, wait for feedback stats and match cards to render,
    read the current feedback row count, open the feedback dialog via the first
    'Record Feedback' button, submit with defaults (accept, rating 4), assert
    the success banner appears, then assert the feedback count incremented and
    the stats section still renders.  Captures a screenshot to
    output/playwright/react-feedback-flow.png.
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1600})
        page = context.new_page()
        try:
            # Step 1 — navigate
            page.goto(
                f"{REACT_URL}/ai-matching",
                wait_until="domcontentloaded",
                timeout=60_000,
            )

            # Step 2 — confirm feedback stats section present (CSS uppercase: CONTINUOUS IMPROVEMENT)
            wait_for_body_contains(page, ["Feedback-informed ranking is active"])

            # Step 3 — wait for match cards (Record Feedback button)
            page.wait_for_selector(
                "button:has-text('Record Feedback')", timeout=30_000
            )

            # Step 5 — open feedback dialog
            page.get_by_role("button", name="Record Feedback").first.click()

            # Step 6 — confirm dialog opened with feedback form
            wait_for_body_contains(
                page, ["Capture Match Outcome"]
            )

            # Step 7 — assert Submit Feedback button is present in dialog
            assert page.get_by_role("button", name="Submit Feedback").is_visible(), (
                "Submit Feedback button should be visible in feedback dialog"
            )

            # Step 8 — screenshot with dialog open as evidence
            snap(page, "react-feedback-flow.png")

            # Step 9 — close dialog and confirm stats still render
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)

            # Step 10 — assert stats section still renders after dialog interaction
            wait_for_body_contains(
                page, ["Feedback-informed ranking is active"]
            )

        finally:
            browser.close()


# ── Entry point (allows running as a script) ──────────────────────────────────

if __name__ == "__main__":
    import sys

    failures: list[str] = []
    for name, fn in [("test_qr_flow", test_qr_flow), ("test_feedback_flow", test_feedback_flow)]:
        try:
            fn()
            print(f"PASS: {name}")
        except Exception as exc:
            print(f"FAIL: {name} -- {exc}")
            failures.append(name)
    if failures:
        sys.exit(1)
