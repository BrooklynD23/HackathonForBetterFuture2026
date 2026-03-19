"""Tests for demo mode fixture dispatch (A3.5)."""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure conftest mocks streamlit before imports
import streamlit as st

from src.demo_mode import (
    DEMO_FIXTURES_DIR,
    demo_or_live,
    init_demo_mode,
    load_fixture,
)

# ── Fixture file expectations ──

EXPECTED_FIXTURE_FILES = [
    "discovery_scan.json",
    "match_explanations.json",
    "email_generation.json",
    "expansion_connections.json",
    "pipeline_funnel.json",
    "volunteer_metrics.json",
    "feedback_summary.json",
]


class TestFixtureFilesExist:
    """All 7 fixture JSON files must exist under cache/demo_fixtures/."""

    @pytest.mark.parametrize("filename", EXPECTED_FIXTURE_FILES)
    def test_fixture_files_exist(self, filename: str) -> None:
        filepath = Path(DEMO_FIXTURES_DIR) / filename
        assert filepath.exists(), f"Missing fixture file: {filepath}"


class TestFixtureFilesValidJSON:
    """Each fixture file must contain valid, non-empty JSON."""

    @pytest.mark.parametrize("filename", EXPECTED_FIXTURE_FILES)
    def test_fixture_files_valid_json(self, filename: str) -> None:
        filepath = Path(DEMO_FIXTURES_DIR) / filename
        with open(filepath) as f:
            data = json.load(f)
        assert data, f"Fixture file is empty: {filepath}"


class TestLoadFixture:
    """load_fixture() reads and parses JSON from cache/demo_fixtures/."""

    def test_load_fixture_returns_dict(self) -> None:
        result = load_fixture("discovery_scan")
        assert isinstance(result, (dict, list))

    def test_load_fixture_nonexistent_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_fixture("nonexistent_fixture_key_xyz")


class TestInitDemoMode:
    """init_demo_mode() sets session_state.demo_mode if absent."""

    def test_init_demo_mode_creates_session_state(self) -> None:
        # Clear any existing key
        st.session_state.pop("demo_mode", None)
        init_demo_mode()
        assert "demo_mode" in st.session_state
        assert st.session_state["demo_mode"] is False

    def test_init_demo_mode_preserves_existing(self) -> None:
        st.session_state["demo_mode"] = True
        init_demo_mode()
        assert st.session_state["demo_mode"] is True


class TestDemoOrLive:
    """demo_or_live() dispatches between fixture and live function."""

    def setup_method(self) -> None:
        st.session_state.clear()

    def test_demo_or_live_returns_fixture_in_demo_mode(self) -> None:
        st.session_state["demo_mode"] = True
        live_fn = MagicMock(return_value="live_result")

        result = demo_or_live(live_fn, fixture_key="discovery_scan")

        assert isinstance(result, (dict, list))
        live_fn.assert_not_called()

    def test_demo_or_live_calls_func_in_live_mode(self) -> None:
        st.session_state["demo_mode"] = False
        live_fn = MagicMock(return_value="live_result")

        result = demo_or_live(live_fn, "arg1", "arg2", fixture_key="discovery_scan", extra="kw")

        live_fn.assert_called_once_with("arg1", "arg2", extra="kw")
        assert result == "live_result"

    def test_demo_or_live_passes_args_to_live_fn(self) -> None:
        st.session_state["demo_mode"] = False
        live_fn = MagicMock(return_value=42)

        result = demo_or_live(live_fn, 1, 2, fixture_key="pipeline_funnel", x=3)

        live_fn.assert_called_once_with(1, 2, x=3)
        assert result == 42


class TestDemoModeWrapsAPICalls:
    """demo_or_live wraps specific API call sites."""

    def setup_method(self) -> None:
        st.session_state["demo_mode"] = True

    def test_demo_mode_wraps_discovery_scan(self) -> None:
        live_fn = MagicMock()
        result = demo_or_live(live_fn, fixture_key="discovery_scan")
        assert result is not None
        live_fn.assert_not_called()

    def test_demo_mode_wraps_email_gen(self) -> None:
        live_fn = MagicMock()
        result = demo_or_live(live_fn, fixture_key="email_generation")
        assert result is not None
        live_fn.assert_not_called()

    def test_demo_mode_wraps_match_explanations(self) -> None:
        live_fn = MagicMock()
        result = demo_or_live(live_fn, fixture_key="match_explanations")
        assert result is not None
        live_fn.assert_not_called()

    def test_demo_mode_wraps_pipeline_funnel(self) -> None:
        live_fn = MagicMock()
        result = demo_or_live(live_fn, fixture_key="pipeline_funnel")
        assert result is not None
        live_fn.assert_not_called()

    def test_demo_mode_wraps_volunteer_metrics(self) -> None:
        live_fn = MagicMock()
        result = demo_or_live(live_fn, fixture_key="volunteer_metrics")
        assert result is not None
        live_fn.assert_not_called()

    def test_demo_mode_wraps_feedback_summary(self) -> None:
        live_fn = MagicMock()
        result = demo_or_live(live_fn, fixture_key="feedback_summary")
        assert result is not None
        live_fn.assert_not_called()
