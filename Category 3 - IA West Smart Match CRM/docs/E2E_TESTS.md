# E2E Tests for IA SmartMatch CRM

This document describes the End-to-End (E2E) tests for the IA SmartMatch CRM landing page and critical user flows using Playwright.

## Overview

The E2E tests validate the following critical user flows:

1. **Landing Page** - Renders with 'Start Matching' and 'View Demo' buttons
2. **CRM Navigation** - Clicking buttons navigates to CRM view with 5 tabs
3. **Tab Visibility** - All tabs are visible: Matches, Discovery, Pipeline, Expansion, Volunteers
4. **Demo Mode** - Toggle is present and functional
5. **Discovery Tab** - Tab can be clicked and content loads

## Test Files

- `tests/test_e2e_flows.py` - Main pytest-based E2E tests
- `scripts/e2e_tests_simple.py` - Standalone Playwright test script
- `scripts/e2e_tests.py` - Original E2E test script
- `scripts/run_e2e_tests.sh` - Bash wrapper to run Streamlit app and tests

## Prerequisites

1. **Playwright installed** - Included in `requirements.txt`
2. **Chromium browser** - Install with:
   ```bash
   python -m playwright install chromium
   ```

## Running E2E Tests

### Option 1: Using pytest (Recommended)

1. Start the Streamlit app in one terminal:
   ```bash
   streamlit run src/app.py --server.port 8501 --server.address 127.0.0.1
   ```

2. Run tests in another terminal:
   ```bash
   # Run all E2E tests
   pytest tests/test_e2e_flows.py -v

   # Run specific test class
   pytest tests/test_e2e_flows.py::TestLandingPage -v

   # Run with output
   pytest tests/test_e2e_flows.py -v -s
   ```

### Option 2: Using standalone script

1. Start the Streamlit app:
   ```bash
   streamlit run src/app.py --server.port 8501 --server.address 127.0.0.1
   ```

2. Run the simple test script:
   ```bash
   python scripts/e2e_tests_simple.py
   ```

### Option 3: Using the wrapper script

```bash
bash scripts/run_e2e_tests.sh
```

This script will:
- Start Streamlit app automatically
- Wait for it to be ready
- Run the E2E tests
- Clean up (kill Streamlit process)

## Test Structure

### TestLandingPage
- `test_landing_page_loads` - Validates page loads successfully
- `test_start_matching_button_exists` - Checks for 'Start Matching' button
- `test_view_demo_button_exists` - Checks for 'View Demo' button

### TestCRMNavigation
- `test_navigate_to_crm_view` - Tests navigation to CRM with tabs
- `test_all_crm_tabs_visible` - Validates all 5 tabs are present
- `test_back_to_home_button` - Tests return to landing page

### TestDemoMode
- `test_demo_mode_checkbox_exists` - Checks Demo Mode toggle presence
- `test_view_demo_button_enables_demo` - Tests demo mode activation

### TestDiscoveryTab
- `test_discovery_tab_clickable` - Tests tab can be clicked
- `test_discovery_tab_content_loads` - Validates content loads

## Skipping E2E Tests

To skip E2E tests (e.g., in CI/CD without a running app):

```bash
export SKIP_E2E=1
pytest tests/
```

## Troubleshooting

### "net::ERR_CONNECTION_REFUSED"
- Ensure Streamlit app is running on http://localhost:8501
- Check that the port is not in use by another process

### Timeout errors
- Streamlit may need more time to load on first run
- Increase timeout values in test code if needed
- Check that data files are accessible

### Browser not found
- Install Chromium: `python -m playwright install chromium`
- Check available browsers: `python -m playwright install-deps`

### Tests failing intermittently
- Increase wait times in test code
- Use explicit waits instead of fixed sleep times where possible
- Ensure system has enough resources

## Test Coverage

Current test coverage includes:
- Landing page rendering
- Navigation flows (Start Matching, View Demo)
- CRM tab layout (5 tabs visible)
- Demo Mode toggle presence
- Discovery tab functionality
- Back to Home button

## Future Improvements

- [ ] Test Matches tab with sample data
- [ ] Test Pipeline tab functionality
- [ ] Test Expansion tab with geographic data
- [ ] Test Volunteer Dashboard
- [ ] Test live scraping in Discovery tab (if API available)
- [ ] Test Demo Mode fixture data loading
- [ ] Performance testing (page load times)
- [ ] Accessibility testing (WCAG compliance)
- [ ] Mobile responsive testing
- [ ] Cross-browser testing (Firefox, WebKit)

## CI/CD Integration

To integrate these tests into CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run Streamlit app
  run: |
    streamlit run src/app.py --server.port 8501 &
    sleep 20

- name: Run E2E tests
  run: pytest tests/test_e2e_flows.py -v
```

## References

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Streamlit Testing Guide](https://docs.streamlit.io/library/advanced-features/app-testing)
