"""Tests for Match Acceptance Feedback Loop (A3.2)."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------- FeedbackEntry creation ----------


class TestFeedbackEntryCreation:
    """FeedbackEntry dataclass must instantiate with correct fields."""

    def test_feedback_entry_creation(self) -> None:
        """FeedbackEntry can be created with required fields."""
        from src.feedback.acceptance import FeedbackEntry

        entry = FeedbackEntry(
            timestamp="2026-03-19T10:00:00",
            event_id="AI Hackathon",
            speaker_id="Travis Miller",
            match_score=0.87,
            decision="accept",
        )
        assert entry.timestamp == "2026-03-19T10:00:00"
        assert entry.decision == "accept"
        assert entry.decline_reason is None
        assert entry.decline_notes is None
        assert entry.factor_scores == {}

    def test_feedback_entry_fields_correct(self) -> None:
        """FeedbackEntry stores all provided fields including optional ones."""
        from src.feedback.acceptance import FeedbackEntry

        scores = {
            "topic_relevance": 0.9,
            "role_fit": 0.8,
            "geographic_proximity": 0.7,
            "calendar_fit": 0.6,
            "historical_conversion": 0.5,
            "student_interest": 0.4,
        }
        entry = FeedbackEntry(
            timestamp="2026-03-19T10:00:00",
            event_id="AI Hackathon",
            speaker_id="Travis Miller",
            match_score=0.87,
            decision="decline",
            decline_reason="Schedule conflict",
            decline_notes=None,
            factor_scores=scores,
        )
        assert entry.event_id == "AI Hackathon"
        assert entry.speaker_id == "Travis Miller"
        assert entry.match_score == 0.87
        assert entry.decline_reason == "Schedule conflict"
        assert entry.factor_scores == scores


# ---------- Session state init ----------


class TestInitFeedbackState:
    """init_feedback_state() must create session state keys."""

    @patch("streamlit.session_state", new_callable=dict)
    def test_init_feedback_state_creates_keys(self, mock_state: dict) -> None:
        """Session state gets feedback_log and feedback_decisions keys."""
        from src.feedback.acceptance import init_feedback_state

        init_feedback_state()
        assert "feedback_log" in mock_state
        assert "feedback_decisions" in mock_state
        assert mock_state["feedback_log"] == []
        assert mock_state["feedback_decisions"] == {}


# ---------- record_feedback ----------


class TestRecordFeedback:
    """record_feedback() must add entries to session state."""

    @patch("src.feedback.acceptance._persist_to_csv")
    @patch("streamlit.session_state", new_callable=dict)
    def test_record_feedback_adds_to_log(
        self, mock_state: dict, mock_persist: MagicMock
    ) -> None:
        """Recording feedback appends to feedback_log."""
        from src.feedback.acceptance import FeedbackEntry, record_feedback

        entry = FeedbackEntry(
            timestamp="2026-03-19T10:00:00",
            event_id="AI Hackathon",
            speaker_id="Travis Miller",
            match_score=0.87,
            decision="accept",
            factor_scores={"topic_relevance": 0.9},
        )
        record_feedback(entry)

        assert len(mock_state["feedback_log"]) == 1
        assert mock_state["feedback_log"][0]["decision"] == "accept"
        # factor_scores should be JSON string for CSV
        assert mock_state["feedback_log"][0]["factor_scores"] == json.dumps(
            {"topic_relevance": 0.9}
        )
        mock_persist.assert_called_once()

    @patch("src.feedback.acceptance._persist_to_csv")
    @patch("streamlit.session_state", new_callable=dict)
    def test_record_feedback_sets_decision(
        self, mock_state: dict, mock_persist: MagicMock
    ) -> None:
        """Recording feedback updates feedback_decisions lookup."""
        from src.feedback.acceptance import FeedbackEntry, record_feedback

        entry = FeedbackEntry(
            timestamp="2026-03-19T10:00:00",
            event_id="AI Hackathon",
            speaker_id="Travis Miller",
            match_score=0.87,
            decision="decline",
            decline_reason="Topic mismatch",
        )
        record_feedback(entry)

        assert (
            mock_state["feedback_decisions"][("AI Hackathon", "Travis Miller")]
            == "decline"
        )


# ---------- get_decision ----------


class TestGetDecision:
    """get_decision() must look up prior decisions."""

    @patch("streamlit.session_state", new_callable=dict)
    def test_get_decision_returns_none_when_missing(
        self, mock_state: dict
    ) -> None:
        """Returns None when no decision recorded for this pair."""
        from src.feedback.acceptance import get_decision

        result = get_decision("AI Hackathon", "Travis Miller")
        assert result is None

    @patch("streamlit.session_state", new_callable=dict)
    def test_get_decision_returns_accept(self, mock_state: dict) -> None:
        """Returns 'accept' when match was previously accepted."""
        from src.feedback.acceptance import get_decision

        mock_state["feedback_decisions"] = {
            ("AI Hackathon", "Travis Miller"): "accept"
        }
        mock_state["feedback_log"] = []
        result = get_decision("AI Hackathon", "Travis Miller")
        assert result == "accept"


# ---------- CSV persistence ----------


class TestPersistToCsv:
    """_persist_to_csv must create/append CSV files."""

    def test_default_csv_path_uses_configured_data_dir(self) -> None:
        """Default persistence path stays anchored to the configured data dir."""
        from src.feedback.acceptance import DATA_DIR, DEFAULT_CSV_PATH

        assert DEFAULT_CSV_PATH == DATA_DIR / "feedback_log.csv"
        assert DEFAULT_CSV_PATH.is_absolute()

    def test_persist_to_csv_creates_file(self, tmp_path: object) -> None:
        """First write creates the CSV with headers."""
        from src.feedback.acceptance import _persist_to_csv

        csv_path = str(tmp_path / "feedback_log.csv")  # type: ignore[operator]
        entry_dict = {
            "timestamp": "2026-03-19T10:00:00",
            "event_id": "AI Hackathon",
            "speaker_id": "Travis Miller",
            "match_score": 0.87,
            "decision": "accept",
            "decline_reason": None,
            "decline_notes": None,
            "factor_scores": "{}",
        }

        _persist_to_csv(entry_dict, csv_path=csv_path)

        assert os.path.exists(csv_path)
        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) == 2  # header + 1 data row
        assert "timestamp" in rows[0]

    def test_persist_to_csv_appends(self, tmp_path: object) -> None:
        """Second write appends without duplicating headers."""
        from src.feedback.acceptance import _persist_to_csv

        csv_path = str(tmp_path / "feedback_log.csv")  # type: ignore[operator]
        entry1 = {
            "timestamp": "2026-03-19T10:00:00",
            "event_id": "AI Hackathon",
            "speaker_id": "Travis Miller",
            "match_score": 0.87,
            "decision": "accept",
            "decline_reason": None,
            "decline_notes": None,
            "factor_scores": "{}",
        }
        entry2 = {
            "timestamp": "2026-03-19T11:00:00",
            "event_id": "Case Competition",
            "speaker_id": "Amanda Keller-Grill",
            "match_score": 0.72,
            "decision": "decline",
            "decline_reason": "Schedule conflict",
            "decline_notes": None,
            "factor_scores": "{}",
        }

        _persist_to_csv(entry1, csv_path=csv_path)
        _persist_to_csv(entry2, csv_path=csv_path)

        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) == 3  # header + 2 data rows

    def test_persist_to_csv_default_path_is_independent_of_cwd(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Default persistence path should not drift with the process CWD."""
        from src.feedback import acceptance

        csv_path = tmp_path / "project_root" / "data" / "feedback_log.csv"
        monkeypatch.setattr(acceptance, "DEFAULT_CSV_PATH", csv_path)

        cwd = tmp_path / "elsewhere"
        cwd.mkdir()
        monkeypatch.chdir(cwd)

        entry_dict = {
            "timestamp": "2026-03-19T10:00:00",
            "event_id": "AI Hackathon",
            "speaker_id": "Travis Miller",
            "match_score": 0.87,
            "decision": "accept",
            "decline_reason": None,
            "decline_notes": None,
            "factor_scores": "{}",
        }

        acceptance._persist_to_csv(entry_dict)

        assert csv_path.exists()
        assert not (cwd / "data" / "feedback_log.csv").exists()


# ---------- Aggregation ----------


class TestAggregateFeedback:
    """aggregate_feedback() must return summary stats."""

    @patch("streamlit.session_state", new_callable=dict)
    def test_aggregate_feedback_empty(self, mock_state: dict) -> None:
        """Empty log returns zeroed summary."""
        from src.feedback.acceptance import aggregate_feedback

        result = aggregate_feedback()
        assert result["total"] == 0
        assert result["accepted"] == 0
        assert result["declined"] == 0
        assert result["acceptance_rate"] == 0.0

    @patch("streamlit.session_state", new_callable=dict)
    def test_aggregate_feedback_with_entries(self, mock_state: dict) -> None:
        """Non-empty log returns correct counts and averages."""
        from src.feedback.acceptance import aggregate_feedback

        mock_state["feedback_log"] = [
            {
                "timestamp": "2026-03-19T10:00:00",
                "event_id": "E1",
                "speaker_id": "S1",
                "match_score": 0.90,
                "decision": "accept",
                "decline_reason": None,
                "factor_scores": "{}",
            },
            {
                "timestamp": "2026-03-19T11:00:00",
                "event_id": "E2",
                "speaker_id": "S2",
                "match_score": 0.60,
                "decision": "decline",
                "decline_reason": "Topic mismatch",
                "factor_scores": "{}",
            },
            {
                "timestamp": "2026-03-19T12:00:00",
                "event_id": "E3",
                "speaker_id": "S3",
                "match_score": 0.70,
                "decision": "decline",
                "decline_reason": "Topic mismatch",
                "factor_scores": "{}",
            },
        ]
        mock_state["feedback_decisions"] = {}

        result = aggregate_feedback()
        assert result["total"] == 3
        assert result["accepted"] == 1
        assert result["declined"] == 2
        assert abs(result["acceptance_rate"] - 1 / 3) < 0.01
        assert result["decline_reasons"]["Topic mismatch"] == 2
        assert result["avg_score_accepted"] == 0.9
        assert result["avg_score_declined"] == 0.65


# ---------- Weight suggestions ----------


class TestGenerateWeightSuggestions:
    """generate_weight_suggestions() must produce advice from patterns."""

    @patch("streamlit.session_state", new_callable=dict)
    def test_generate_weight_suggestions_below_threshold(
        self, mock_state: dict
    ) -> None:
        """No suggestions when decline count below threshold."""
        from src.feedback.acceptance import generate_weight_suggestions

        mock_state["feedback_log"] = [
            {
                "timestamp": "2026-03-19T10:00:00",
                "event_id": "E1",
                "speaker_id": "S1",
                "match_score": 0.80,
                "decision": "decline",
                "decline_reason": "Topic mismatch",
                "factor_scores": "{}",
            },
        ]
        mock_state["feedback_decisions"] = {}

        suggestions = generate_weight_suggestions(min_declines_for_suggestion=3)
        assert suggestions == []

    @patch("streamlit.session_state", new_callable=dict)
    def test_generate_weight_suggestions_above_threshold(
        self, mock_state: dict
    ) -> None:
        """Suggestions generated when decline count meets threshold."""
        from src.feedback.acceptance import generate_weight_suggestions

        mock_state["feedback_log"] = [
            {
                "timestamp": f"2026-03-19T{10+i}:00:00",
                "event_id": f"E{i}",
                "speaker_id": f"S{i}",
                "match_score": 0.80,
                "decision": "decline",
                "decline_reason": "Too far (geographic distance)",
                "factor_scores": "{}",
            }
            for i in range(4)
        ]
        mock_state["feedback_decisions"] = {}

        suggestions = generate_weight_suggestions(min_declines_for_suggestion=3)
        assert len(suggestions) >= 1
        assert "geographic_proximity" in suggestions[0]
        assert "0.20" in suggestions[0]  # current weight
        assert "0.25" in suggestions[0]  # suggested weight


# ---------- UI rendering ----------


class TestRenderFeedbackButtons:
    """render_feedback_buttons() must show correct UI state."""

    @patch("streamlit.session_state", new_callable=dict)
    @patch("streamlit.success")
    def test_render_feedback_buttons_shows_accepted_badge(
        self, mock_success: MagicMock, mock_state: dict
    ) -> None:
        """Already-accepted match shows success badge instead of buttons."""
        from src.feedback.acceptance import render_feedback_buttons

        mock_state["feedback_log"] = []
        mock_state["feedback_decisions"] = {
            ("AI Hackathon", "Travis Miller"): "accept"
        }

        render_feedback_buttons(
            event_id="AI Hackathon",
            speaker_id="Travis Miller",
            match_score=0.87,
            factor_scores={"topic_relevance": 0.9},
        )
        mock_success.assert_called_once_with("Accepted", icon="\u2705")
