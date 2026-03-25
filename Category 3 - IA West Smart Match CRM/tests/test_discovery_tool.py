"""Tests for discovery_tool wrapper."""

from __future__ import annotations

from unittest.mock import patch

import pytest


class TestDiscoveryToolRun:
    """Tests for discovery_tool.run()."""

    def test_run_returns_events_for_named_university(self):
        fake_result = {"html": "<html>career fair</html>", "source": "cache"}
        extracted_events = [{"event_name": "Career Fair"}]
        with (
            patch("src.coordinator.tools.discovery_tool.scrape_university", return_value=fake_result) as mock_scrape,
            patch("src.coordinator.tools.discovery_tool.extract_events", return_value=extracted_events) as mock_extract,
        ):
            from src.coordinator.tools import discovery_tool
            result = discovery_tool.run({"university": "UCLA"})
        assert result["status"] == "ok"
        assert result["events"] == extracted_events
        assert result["source"] == "cache"
        mock_scrape.assert_called_once()
        mock_extract.assert_called_once()
        call_kwargs = mock_scrape.call_args
        assert "career.ucla.edu" in call_kwargs.kwargs.get("url", call_kwargs.args[0] if call_kwargs.args else "")
        extract_kwargs = mock_extract.call_args.kwargs
        assert extract_kwargs["raw_html"] == "<html>career fair</html>"
        assert extract_kwargs["university"] == "UCLA"
        assert "career.ucla.edu" in extract_kwargs["url"]
        assert extract_kwargs["prefer_cache"] is True

    def test_run_uses_first_university_as_default(self):
        fake_result = {"html": "<html></html>", "source": "live"}
        with (
            patch("src.coordinator.tools.discovery_tool.scrape_university", return_value=fake_result) as mock_scrape,
            patch("src.coordinator.tools.discovery_tool.extract_events", return_value=[]),
        ):
            from src.coordinator.tools import discovery_tool
            result = discovery_tool.run({})
        assert result["status"] == "ok"
        mock_scrape.assert_called_once()

    def test_run_returns_empty_events_when_extraction_fails(self):
        fake_result = {"html": "<html>broken</html>", "source": "stale_cache"}
        with (
            patch("src.coordinator.tools.discovery_tool.scrape_university", return_value=fake_result),
            patch("src.coordinator.tools.discovery_tool.extract_events", side_effect=RuntimeError("boom")),
        ):
            from src.coordinator.tools import discovery_tool
            result = discovery_tool.run({"university": "UCLA"})

        assert result == {"status": "ok", "events": [], "source": "stale_cache"}

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
