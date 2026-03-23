#!/usr/bin/env bash
#
# Run E2E tests for IA SmartMatch CRM.
#
# This script:
# 1. Starts the Streamlit app in the background
# 2. Waits for it to be ready
# 3. Runs the Playwright E2E tests
# 4. Stops the app and cleanup
#

set -euo pipefail

# Get the root directory (parent of scripts)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Get Python executable
PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Error: Python executable not found at $PYTHON_BIN"
  exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting E2E Tests for IA SmartMatch CRM${NC}"
echo "=================================="

# Start Streamlit app
echo -e "${YELLOW}Starting Streamlit app...${NC}"
"$PYTHON_BIN" -m streamlit run src/app.py --server.port 8501 --server.address 127.0.0.1 2>&1 | grep -v "^$" &
STREAMLIT_PID=$!

# Cleanup function
cleanup() {
  echo -e "${YELLOW}Cleaning up...${NC}"
  if kill -0 "$STREAMLIT_PID" >/dev/null 2>&1; then
    kill "$STREAMLIT_PID" >/dev/null 2>&1 || true
  fi
  wait "$STREAMLIT_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

# Wait for Streamlit to start
echo -e "${YELLOW}Waiting for Streamlit to start (max 30 seconds)...${NC}"
for i in {1..30}; do
  if curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Streamlit is ready${NC}"
    break
  fi
  if [[ $i -eq 30 ]]; then
    echo -e "${RED}✗ Streamlit failed to start${NC}"
    exit 1
  fi
  echo "Waiting... ($i/30)"
  sleep 1
done

# Run E2E tests
echo ""
echo -e "${YELLOW}Running E2E tests...${NC}"
"$PYTHON_BIN" scripts/e2e_tests.py

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
if [[ $TEST_EXIT_CODE -eq 0 ]]; then
  echo -e "${GREEN}All E2E tests passed!${NC}"
else
  echo -e "${RED}Some E2E tests failed${NC}"
fi

exit $TEST_EXIT_CODE
