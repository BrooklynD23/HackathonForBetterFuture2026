"""Tests for discovery_tool wrapper."""

from __future__ import annotations

from unittest.mock import patch

import pytest


class TestDiscoveryToolRun:
    """Tests for discovery_tool.run()."""

    def test_run_returns_events_for_named_university(self):
        fake_result = {"events": [{"title": "Career Fair"}], "source": "cache"}
        with patch("src.coordinator.tools.discovery_tool.scrape_university", return_value=fake_result) as mock_scrape:
            from src.coordinator.tools import discovery_tool
            result = discovery_tool.run({"university": "UCLA"})
        assert result["status"] == "ok"
        assert result["events"] == [{"title": "Career Fair"}]
        assert result["source"] == "cache"
        mock_scrape.assert_called_once()
        call_kwargs = mock_scrape.call_args
        assert "career.ucla.edu" in call_kwargs.kwargs.get("url", call_kwargs.args[0] if call_kwargs.args else "")

    def test_run_uses_first_university_as_default(self):
        fake_result = {"events": [], "source": "live"}
        with patch("src.coordinator.tools.discovery_tool.scrape_university", return_value=fake_result) as mock_scrape:
            from src.coordinator.tools import discovery_tool
            result = discovery_tool.run({})
        assert result["status"] == "ok"
        mock_scrape.assert_called_once()

    def test_run_propagates_exceptions_from_scrape_university(self):
        with patch("src.coordinator.tools.discovery_tool.scrape_university", side_effect=PermissionError("robots.txt")):
            from src.coordinator.tools import discovery_tool
            with pytest.raises(PermissionError, match="robots.txt"):
                discovery_tool.run({"university": "UCLA"})

    def test_tool_name_is_discover_events(self):
        from src.coordinator.tools import discovery_tool
        assert discovery_tool.TOOL_NAME == "discover_events"

    def test_no_streamlit_import(self):
        import inspect
        import src.coordinator.tools.discovery_tool as mod
        source = inspect.getsource(mod)
        assert "import streamlit" not in source
