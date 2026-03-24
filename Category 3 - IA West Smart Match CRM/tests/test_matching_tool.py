"""Tests for matching_tool wrapper."""

from __future__ import annotations

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest


def _make_valid_params():
    return {
        "event_row": pd.Series({"Event / Program": "Career Fair", "event_id": "e1"}),
        "speakers_df": pd.DataFrame({"Name": ["Alice"]}),
        "speaker_embeddings": {"Alice": np.zeros(128)},
        "event_embedding": np.zeros(128),
        "ia_event_calendar": pd.DataFrame(),
    }


class TestMatchingToolRun:
    """Tests for matching_tool.run()."""

    def test_run_returns_rankings(self):
        fake_rankings = [{"rank": 1, "speaker_name": "Alice", "total_score": 0.9}]
        with patch("src.coordinator.tools.matching_tool.rank_speakers_for_event", return_value=fake_rankings):
            from src.coordinator.tools import matching_tool
            result = matching_tool.run(_make_valid_params())
        assert result["status"] == "ok"
        assert result["rankings"] == fake_rankings

    def test_run_missing_event_row_returns_error(self):
        from src.coordinator.tools import matching_tool
        params = _make_valid_params()
        del params["event_row"]
        result = matching_tool.run(params)
        assert result["status"] == "error"
        assert "event_row" in result["error"]

    def test_run_missing_speakers_df_returns_error(self):
        from src.coordinator.tools import matching_tool
        params = _make_valid_params()
        del params["speakers_df"]
        result = matching_tool.run(params)
        assert result["status"] == "error"
        assert "speakers_df" in result["error"]

    def test_run_missing_speaker_embeddings_returns_error(self):
        from src.coordinator.tools import matching_tool
        params = _make_valid_params()
        del params["speaker_embeddings"]
        result = matching_tool.run(params)
        assert result["status"] == "error"
        assert "speaker_embeddings" in result["error"]

    def test_tool_name_is_rank_speakers(self):
        from src.coordinator.tools import matching_tool
        assert matching_tool.TOOL_NAME == "rank_speakers"

    def test_no_streamlit_import(self):
        import inspect
        import src.coordinator.tools.matching_tool as mod
        source = inspect.getsource(mod)
        assert "import streamlit" not in source
