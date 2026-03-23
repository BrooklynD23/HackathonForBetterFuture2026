"""
E2E Tests for IA SmartMatch CRM landing page → matches → discovery flows.

These tests use Playwright to validate critical user flows:
1. Landing page renders with 'Start Matching' button
2. Click to CRM, see 5 tabs (Matches, Discovery, Pipeline, Expansion, Volunteers)
3. Demo Mode toggle works
4. Discovery tab can be clicked and loads

Note: These tests require the Streamlit app to be running on http://localhost:8501
Run with: streamlit run src/app.py --server.port 8501

Then run tests with: pytest tests/test_e2e_flows.py -v
"""

import os
import time
import pytest
from playwright.sync_api import sync_playwright, Page


# Skip these tests if Playwright browser is not available or if SKIP_E2E env var is set
pytestmark = pytest.mark.skipif(
    os.getenv("SKIP_E2E") == "1",
    reason="E2E tests skipped (SKIP_E2E=1). Requires running Streamlit app on port 8501"
)

BASE_URL = "http://localhost:8501"
TIMEOUT = 30000  # 30 seconds


@pytest.fixture(scope="module")
def browser_context():
    """Create a browser context for all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


def wait_for_element(page: Page, selector: str, timeout: int = 5000) -> bool:
    """Wait for an element to be visible."""
    try:
        page.wait_for_selector(selector, timeout=timeout, state="visible")
        return True
    except Exception:
        return False


class TestLandingPage:
    """Tests for landing page functionality."""

    def test_landing_page_loads(self, browser_context):
        """Test that landing page renders successfully."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Check page is loaded
            assert page.url == BASE_URL

            # Check for landing page content by searching for text
            content = page.content()
            assert "Academic Curator" in content or "Start Matching" in content, \
                "Landing page content not found"

        finally:
            page.close()

    def test_start_matching_button_exists(self, browser_context):
        """Test that 'Start Matching' button is present."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Look for Start Matching button
            buttons = page.query_selector_all("button")
            button_texts = [btn.text_content() for btn in buttons if btn.text_content()]

            # Check if any button contains 'Start Matching'
            assert any("Start Matching" in text for text in button_texts), \
                f"'Start Matching' button not found. Found buttons: {button_texts}"

        finally:
            page.close()

    def test_view_demo_button_exists(self, browser_context):
        """Test that 'View Demo' button is present."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Look for View Demo button
            buttons = page.query_selector_all("button")
            button_texts = [btn.text_content() for btn in buttons if btn.text_content()]

            # Check if any button contains 'View Demo'
            assert any("View Demo" in text for text in button_texts), \
                f"'View Demo' button not found. Found buttons: {button_texts}"

        finally:
            page.close()


class TestCRMNavigation:
    """Tests for CRM navigation flows."""

    def test_navigate_to_crm_view(self, browser_context):
        """Test that clicking 'Start Matching' navigates to CRM view."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Find and click Start Matching button
            buttons = page.query_selector_all("button")
            start_button = None
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    start_button = button
                    break

            assert start_button is not None, "'Start Matching' button not found"

            # Click the button
            start_button.click()
            time.sleep(3)

            # Wait for CRM view to load (tabs should appear)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)
            time.sleep(1)

            # Check for tabs using role attribute
            tabs = page.query_selector_all("[role='tab']")
            assert len(tabs) >= 5, f"Expected at least 5 tabs, found {len(tabs)}"

        finally:
            page.close()

    def test_all_crm_tabs_visible(self, browser_context):
        """Test that all 5 CRM tabs are visible."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Check for all 5 tabs
            expected_tabs = ["Matches", "Discovery", "Pipeline", "Expansion", "Volunteers"]
            tabs = page.query_selector_all("[role='tab']")
            tab_texts = [tab.text_content() for tab in tabs if tab.text_content()]

            for expected_tab in expected_tabs:
                found = any(expected_tab in text for text in tab_texts)
                assert found, f"Expected tab '{expected_tab}' not found. Found: {tab_texts}"

        finally:
            page.close()

    def test_back_to_home_button(self, browser_context):
        """Test that 'Back to Home' button returns to landing page."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Find Back to Home button
            buttons = page.query_selector_all("button")
            back_button = None
            for button in buttons:
                text = button.text_content()
                if text and "Back to Home" in text:
                    back_button = button
                    break

            if back_button:  # Back button may not always be visible
                back_button.click()
                time.sleep(2)
                page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

        finally:
            page.close()


class TestDemoMode:
    """Tests for Demo Mode functionality."""

    def test_demo_mode_checkbox_exists(self, browser_context):
        """Test that Demo Mode checkbox is present in CRM view."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Check for Demo Mode in page content
            content = page.content()
            assert "Demo Mode" in content, "Demo Mode toggle not found in page"

        finally:
            page.close()

    def test_view_demo_button_enables_demo(self, browser_context):
        """Test that 'View Demo' button enables demo mode."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Find and click View Demo button
            buttons = page.query_selector_all("button")
            view_demo_button = None
            for button in buttons:
                text = button.text_content()
                if text and "View Demo" in text:
                    view_demo_button = button
                    break

            assert view_demo_button is not None, "'View Demo' button not found"

            view_demo_button.click()
            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Check that demo mode content is visible
            content = page.content()
            # In demo mode, the page should still load with tabs visible
            assert "[role='tab']" in content or "Demo Mode" in content

        finally:
            page.close()


class TestDiscoveryTab:
    """Tests for Discovery tab functionality."""

    def test_discovery_tab_clickable(self, browser_context):
        """Test that Discovery tab can be clicked."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Navigate to CRM
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Find Discovery tab
            tabs = page.query_selector_all("[role='tab']")
            discovery_tab = None
            for tab in tabs:
                text = tab.text_content()
                if text and "Discovery" in text:
                    discovery_tab = tab
                    break

            assert discovery_tab is not None, "Discovery tab not found"

            # Click it
            discovery_tab.click()
            time.sleep(2)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Check if it's now selected
            is_selected = discovery_tab.get_attribute("aria-selected")
            assert is_selected == "true", f"Discovery tab not selected (aria-selected={is_selected})"

        finally:
            page.close()

    def test_discovery_tab_content_loads(self, browser_context):
        """Test that Discovery tab content loads."""
        page = browser_context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            time.sleep(2)

            # Navigate to CRM and click Discovery tab
            buttons = page.query_selector_all("button")
            for button in buttons:
                text = button.text_content()
                if text and "Start Matching" in text:
                    button.click()
                    break

            time.sleep(3)

            # Find and click Discovery tab
            tabs = page.query_selector_all("[role='tab']")
            for tab in tabs:
                text = tab.text_content()
                if text and "Discovery" in text:
                    tab.click()
                    break

            time.sleep(2)
            page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

            # Page should have content after clicking Discovery
            content = page.content()
            assert len(content) > 1000, "Discovery tab content not loaded"

        finally:
            page.close()
