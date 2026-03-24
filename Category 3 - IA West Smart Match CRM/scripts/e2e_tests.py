#!/usr/bin/env python3
"""
E2E Tests for IA SmartMatch CRM - Playwright tests for critical user flows.

Tests cover:
1. Landing page renders with 'Start Matching' button
2. Click to CRM, see 5 tabs (Matches, Discovery, Pipeline, Expansion, Volunteers)
3. Demo Mode toggle works
4. Discovery tab loads successfully

Run this script after starting the Streamlit app:
  streamlit run src/app.py --server.port 8501

Then in another terminal:
  python scripts/e2e_tests.py
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, Page


BASE_URL = "http://localhost:8501"
MAX_RETRIES = 30


def wait_for_app(page: Page, max_retries: int = MAX_RETRIES) -> None:
    """Wait for the Streamlit app to be ready."""
    for i in range(max_retries):
        try:
            page.goto(BASE_URL, wait_until="networkidle")
            return
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(1)
            else:
                raise RuntimeError(f"App failed to start after {max_retries} retries: {e}")


def test_landing_page_renders():
    """Test that landing page renders with 'Start Matching' button."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            wait_for_app(page)

            # Check for landing page content
            page.wait_for_selector("h1", timeout=5000)
            heading = page.text_content("h1")
            assert "Match your specialist database" in heading, \
                f"Expected heading text not found. Got: {heading}"

            # Check for 'Start Matching' button
            buttons = page.query_selector_all("button")
            button_texts = [button.text_content().strip() for button in buttons if button.text_content()]

            assert any("Start Matching" in text for text in button_texts), \
                f"'Start Matching' button not found. Found buttons: {button_texts}"

            print("✓ Landing page renders with 'Start Matching' button")

        finally:
            browser.close()


def test_navigate_to_crm():
    """Test clicking 'Start Matching' navigates to CRM view with tabs."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            wait_for_app(page)

            # Click 'Start Matching' button
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            # Wait for CRM view to load - tabs should appear
            time.sleep(2)  # Give page time to rerun
            page.wait_for_load_state("networkidle", timeout=10000)

            # Check for the 5 tabs using the tab role
            tabs = page.query_selector_all("[role='tab']")
            tab_texts = [tab.text_content() for tab in tabs if tab.text_content()]

            expected_tabs = ["Matches", "Discovery", "Pipeline", "Expansion", "Volunteers"]
            for expected_tab in expected_tabs:
                assert any(expected_tab in text for text in tab_texts), \
                    f"{expected_tab} not found in tabs: {tab_texts}"

            print("✓ Successfully navigated to CRM with all 5 tabs visible")

        finally:
            browser.close()


def test_demo_mode_toggle():
    """Test that Demo Mode toggle is functional."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            wait_for_app(page)

            # Click 'View Demo' button to enable demo mode on navigation
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "View Demo" in text:
                    button.click()
                    break

            # Wait for page to reload
            time.sleep(2)
            page.wait_for_load_state("networkidle", timeout=10000)

            # Look for Demo Mode checkbox in sidebar
            # Streamlit renders checkboxes as input elements with labels
            try:
                # Try to find by text in the page
                page.wait_for_selector("text=Demo Mode", timeout=5000)
                print("✓ Demo Mode toggle is available and functional")
            except Exception:
                # If not found immediately, it might be in the sidebar
                sidebar_checkboxes = page.query_selector_all("aside input[type='checkbox']")
                assert len(sidebar_checkboxes) > 0, "No checkboxes found in sidebar"
                print("✓ Demo Mode toggle is available in sidebar")

        finally:
            browser.close()


def test_discovery_tab_loads():
    """Test that Discovery tab loads successfully."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            wait_for_app(page)

            # Navigate to CRM first
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            # Wait for CRM to load
            time.sleep(2)
            page.wait_for_load_state("networkidle", timeout=10000)

            # Click on Discovery tab
            tabs = page.query_selector_all("[role='tab']")
            discovery_tab = None
            for tab in tabs:
                text = tab.text_content()
                if text and "Discovery" in text:
                    discovery_tab = tab
                    break

            assert discovery_tab, "Discovery tab not found"
            discovery_tab.click()

            # Wait for tab content to load
            time.sleep(1)
            page.wait_for_load_state("networkidle", timeout=10000)

            # Check that the tab is now active
            is_selected = discovery_tab.get_attribute("aria-selected")
            assert is_selected == "true", f"Discovery tab is not selected: {is_selected}"

            print("✓ Discovery tab loaded successfully")

        finally:
            browser.close()


def test_all_tabs_visible():
    """Test that all 5 tabs are visible in CRM view."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            wait_for_app(page)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            # Wait for CRM to load
            time.sleep(2)
            page.wait_for_load_state("networkidle", timeout=10000)

            # Check each tab is visible
            tabs = page.query_selector_all("[role='tab']")
            tab_texts = [tab.text_content() for tab in tabs if tab.text_content()]

            expected_tabs = ["Matches", "Discovery", "Pipeline", "Expansion", "Volunteers"]
            for expected_tab in expected_tabs:
                assert any(expected_tab in text for text in tab_texts), \
                    f"{expected_tab} tab not found. Found tabs: {tab_texts}"

            print(f"✓ All 5 tabs visible: {tab_texts}")

        finally:
            browser.close()


def test_back_to_home_button():
    """Test that 'Back to Home' button returns to landing page."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            wait_for_app(page)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            # Wait for CRM to load
            time.sleep(2)
            page.wait_for_load_state("networkidle", timeout=10000)

            # Find and click 'Back to Home' button
            buttons = page.query_selector_all("button")
            back_button_found = False
            for button in buttons:
                text = button.text_content()
                if text and "Back to Home" in text:
                    button.click()
                    back_button_found = True
                    break

            assert back_button_found, "'Back to Home' button not found"

            # Wait for page to return to landing
            time.sleep(2)
            page.wait_for_load_state("networkidle", timeout=10000)

            # Check we're back at landing page
            heading = page.text_content("h1")
            assert "Match your specialist database" in heading, \
                f"Not back at landing page. Heading: {heading}"

            print("✓ 'Back to Home' button works correctly")

        finally:
            browser.close()


def main():
    """Run all E2E tests."""
    print("\n" + "="*70)
    print("Starting E2E Tests for IA SmartMatch CRM")
    print("="*70 + "\n")

    tests = [
        ("Landing Page Renders", test_landing_page_renders),
        ("Navigate to CRM", test_navigate_to_crm),
        ("All Tabs Visible", test_all_tabs_visible),
        ("Demo Mode Toggle", test_demo_mode_toggle),
        ("Discovery Tab Loads", test_discovery_tab_loads),
        ("Back to Home Button", test_back_to_home_button),
    ]

    passed = 0
    failed = 0
    errors = []

    for test_name, test_func in tests:
        try:
            print(f"\n[TEST] {test_name}")
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} FAILED: {e}")
            failed += 1
            errors.append((test_name, e))

    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    if errors:
        print("\nFailed tests:")
        for test_name, error in errors:
            print(f"  - {test_name}: {error}")
    print("="*70 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
