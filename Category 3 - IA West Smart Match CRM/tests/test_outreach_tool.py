"""Tests for outreach_tool wrapper."""

from __future__ import annotations

from unittest.mock import patch

import pytest


def _make_valid_params():
    return {
        "speaker": {"Name": "Alice", "Title": "VP Engineering"},
        "event": {"Event / Program": "Career Fair", "event_id": "e1"},
        "match_scores": {"total_score": 0.85},
    }


class TestOutreachToolRun:
    """Tests for outreach_tool.run()."""

    def test_run_returns_email_dict(self):
        fake_email = {
            "subject_line": "Invite: Career Fair",
            "greeting": "Dear Alice,",
            "body": "We would like to invite you...",
            "closing": "Best regards,",
            "full_email": "...",
        }
        with patch("src.coordinator.tools.outreach_tool.generate_outreach_email", return_value=fake_email):
            from src.coordinator.tools import outreach_tool
            result = outreach_tool.run(_make_valid_params())
        assert result["status"] == "ok"
        assert result["email"] == fake_email

    def test_run_missing_speaker_returns_error(self):
        from src.coordinator.tools import outreach_tool
        params = _make_valid_params()
        del params["speaker"]
        result = outreach_tool.run(params)
        assert result["status"] == "error"
        assert "speaker" in result["error"]

    def test_run_missing_event_returns_error(self):
        from src.coordinator.tools import outreach_tool
        params = _make_valid_params()
        del params["event"]
        result = outreach_tool.run(params)
        assert result["status"] == "error"
        assert "event" in result["error"]

    def test_run_missing_match_scores_returns_error(self):
        from src.coordinator.tools import outreach_tool
        params = _make_valid_params()
        del params["match_scores"]
        result = outreach_tool.run(params)
        assert result["status"] == "error"
        assert "match_scores" in result["error"]

    def test_tool_name_is_generate_outreach(self):
        from src.coordinator.tools import outreach_tool
        assert outreach_tool.TOOL_NAME == "generate_outreach"

    def test_no_streamlit_import(self):
        import inspect
        import src.coordinator.tools.outreach_tool as mod
        source = inspect.getsource(mod)
        assert "import streamlit" not in source
