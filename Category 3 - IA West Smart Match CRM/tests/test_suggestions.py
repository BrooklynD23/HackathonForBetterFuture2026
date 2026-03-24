"""Tests for staleness suggestion engine (suggestions.py)."""

import datetime

import pytest

from src.coordinator.suggestions import STALENESS_HOURS, _is_stale, check_staleness_conditions


class TestStalenessCheck:
    """Staleness condition tests."""

    def test_returns_one_suggestion_when_events_empty_and_scraped_at_none(self) -> None:
        suggestions = check_staleness_conditions(scraped_events=[], scraped_at=None)
        assert len(suggestions) == 1

    def test_returns_one_suggestion_when_scraped_at_is_25_hours_ago(self) -> None:
        stale_ts = (datetime.datetime.now() - datetime.timedelta(hours=25)).isoformat()
        suggestions = check_staleness_conditions(scraped_events=["event1"], scraped_at=stale_ts)
        assert len(suggestions) == 1

    def test_returns_empty_when_fresh_and_events_present(self) -> None:
        fresh_ts = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
        suggestions = check_staleness_conditions(scraped_events=["event1"], scraped_at=fresh_ts)
        assert suggestions == []

    def test_suggestion_has_correct_intent_and_agent(self) -> None:
        suggestions = check_staleness_conditions(scraped_events=[], scraped_at=None)
        s = suggestions[0]
        assert s.intent == "discover_events"
        assert s.agent == "Discovery Agent"

    def test_suggestion_has_proactive_source(self) -> None:
        suggestions = check_staleness_conditions(scraped_events=[], scraped_at=None)
        assert suggestions[0].source == "proactive"

    def test_suggestion_has_proposed_status(self) -> None:
        suggestions = check_staleness_conditions(scraped_events=[], scraped_at=None)
        assert suggestions[0].status == "proposed"

    def test_is_stale_returns_true_for_none(self) -> None:
        assert _is_stale(None, hours=24) is True

    def test_is_stale_returns_true_for_invalid_timestamp(self) -> None:
        assert _is_stale("not-a-timestamp", hours=24) is True

    def test_is_stale_returns_false_for_timestamp_one_hour_ago(self) -> None:
        recent_ts = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
        assert _is_stale(recent_ts, hours=24) is False

    def test_staleness_hours_equals_24(self) -> None:
        assert STALENESS_HOURS == 24
