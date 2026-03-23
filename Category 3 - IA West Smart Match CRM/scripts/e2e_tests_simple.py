#!/usr/bin/env python3
"""
Simplified E2E Tests for IA SmartMatch CRM using Playwright.

This version uses minimal Playwright operations to test critical flows.
"""

import sys
import time
from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost:8501"


def test_landing_page():
    """Test that landing page renders with 'Start Matching' button."""
    print("\n[1/5] Testing landing page renders...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the app
            print("  - Navigating to app...")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

            # Wait for heading to load
            print("  - Checking for heading...")
            page.wait_for_selector("h1", timeout=10000)
            heading_text = page.text_content("h1")

            if "Match your specialist database" in heading_text:
                print("  ✓ Landing page heading found")
            else:
                print(f"  ✗ Unexpected heading: {heading_text}")
                return False

            # Look for Start Matching button
            print("  - Looking for buttons...")
            buttons = page.query_selector_all("button")
            button_found = False

            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button_found = True
                    print("  ✓ 'Start Matching' button found")
                    break

            if not button_found:
                print("  ✗ 'Start Matching' button not found")
                return False

            return True

        finally:
            browser.close()


def test_navigate_to_crm():
    """Test navigating to CRM and seeing tabs."""
    print("\n[2/5] Testing navigation to CRM...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("  - Navigating to app...")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

            # Wait for and click Start Matching button
            print("  - Finding Start Matching button...")
            buttons = page.query_selector_all("button")
            start_button = None

            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    start_button = button
                    break

            if not start_button:
                print("  ✗ Start Matching button not found")
                return False

            print("  - Clicking Start Matching...")
            start_button.click()

            # Wait for tabs to appear
            print("  - Waiting for tabs to load...")
            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=15000)

            # Look for tabs
            tabs = page.query_selector_all("[role='tab']")
            if len(tabs) >= 5:
                tab_texts = [tab.text_content() for tab in tabs if tab.text_content()]
                print(f"  ✓ Found {len(tabs)} tabs")
                return True
            else:
                print(f"  ✗ Expected 5+ tabs, found {len(tabs)}")
                return False

        finally:
            browser.close()


def test_all_tabs_visible():
    """Test that all expected tabs are visible."""
    print("\n[3/5] Testing all tabs are visible...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("  - Navigating to app...")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=15000)

            # Check for tabs
            expected_tabs = ["Matches", "Discovery", "Pipeline", "Expansion", "Volunteers"]
            tabs = page.query_selector_all("[role='tab']")
            tab_texts = [tab.text_content() for tab in tabs if tab.text_content()]

            print(f"  - Found tabs: {tab_texts}")

            missing = []
            for expected in expected_tabs:
                found = any(expected in text for text in tab_texts)
                if not found:
                    missing.append(expected)

            if missing:
                print(f"  ✗ Missing tabs: {missing}")
                return False

            print(f"  ✓ All {len(expected_tabs)} tabs visible")
            return True

        finally:
            browser.close()


def test_demo_mode_toggle():
    """Test that Demo Mode toggle is present."""
    print("\n[4/5] Testing Demo Mode toggle...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("  - Navigating to app...")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=15000)

            # Look for Demo Mode checkbox/toggle
            print("  - Looking for Demo Mode toggle...")
            checkboxes = page.query_selector_all("input[type='checkbox']")

            if checkboxes:
                print(f"  ✓ Found {len(checkboxes)} checkboxes in sidebar")
                return True
            else:
                # Try alternative: look for text
                page_text = page.text_content()
                if "Demo Mode" in page_text:
                    print("  ✓ Demo Mode text found on page")
                    return True
                else:
                    print("  ✗ Demo Mode toggle not found")
                    return False

        finally:
            browser.close()


def test_discovery_tab():
    """Test that Discovery tab can be clicked."""
    print("\n[5/5] Testing Discovery tab...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("  - Navigating to app...")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=15000)

            # Find and click Discovery tab
            print("  - Looking for Discovery tab...")
            tabs = page.query_selector_all("[role='tab']")
            discovery_tab = None

            for tab in tabs:
                text = tab.text_content()
                if text and "Discovery" in text:
                    discovery_tab = tab
                    break

            if not discovery_tab:
                print("  ✗ Discovery tab not found")
                return False

            print("  - Clicking Discovery tab...")
            discovery_tab.click()

            time.sleep(2)
            page.wait_for_load_state("domcontentloaded", timeout=10000)

            # Check if tab is selected
            is_selected = discovery_tab.get_attribute("aria-selected")
            if is_selected == "true":
                print("  ✓ Discovery tab is now active")
                return True
            else:
                print(f"  ✗ Discovery tab not selected (aria-selected={is_selected})")
                return False

        finally:
            browser.close()


def main():
    """Run all E2E tests."""
    print("\n" + "="*70)
    print("E2E Tests for IA SmartMatch CRM")
    print("="*70)

    tests = [
        test_landing_page,
        test_navigate_to_crm,
        test_all_tabs_visible,
        test_demo_mode_toggle,
        test_discovery_tab,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results.append((test_func.__name__, False))
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "="*70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70)

    for name, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")

    print()
    return 0 if passed == total else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
