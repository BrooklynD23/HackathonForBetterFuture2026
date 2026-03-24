"""Tests for staleness suggestion engine (suggestions.py)."""

import datetime

import pytest

from src.coordinator.suggestions import (
    STALENESS_HOURS,
    _is_stale,
    check_overdue_contacts,
    check_staleness_conditions,
)


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


class TestOverdueContacts:
    """Tests for check_overdue_contacts() proactive suggestion function."""

    # Synthetic contact fixtures
    _OVERDUE = {"name": "Dr. Smith", "follow_up_due": "2026-03-01"}
    _FUTURE = {"name": "Prof. Future", "follow_up_due": "2099-01-01"}

    def _overdue_contact(self, name: str, days_ago: int = 10) -> dict:
        due = (datetime.date.today() - datetime.timedelta(days=days_ago)).isoformat()
        return {"name": name, "follow_up_due": due}

    def test_check_overdue_contacts_returns_proposal_when_overdue(self) -> None:
        contacts = [self._OVERDUE]
        result = check_overdue_contacts(contacts)
        assert len(result) == 1

    def test_check_overdue_contacts_returns_empty_when_no_overdue(self) -> None:
        contacts = [self._FUTURE]
        result = check_overdue_contacts(contacts)
        assert result == []

    def test_check_overdue_contacts_returns_empty_on_empty_list(self) -> None:
        result = check_overdue_contacts([])
        assert result == []

    def test_check_overdue_contacts_message_format(self) -> None:
        contacts = [self._OVERDUE]
        result = check_overdue_contacts(contacts)
        description = result[0].description
        assert "1" in description
        assert "Dr. Smith" in description
        assert "review now?" in description
        assert "contact(s) overdue for follow-up:" in description

    def test_check_overdue_contacts_message_truncates_at_3_names(self) -> None:
        # 5 overdue contacts: shows first 3 names + "and 2 more"
        contacts = [
            self._overdue_contact(f"Name {i}") for i in range(5)
        ]
        result = check_overdue_contacts(contacts)
        description = result[0].description
        assert "and 2 more" in description
        # Only first 3 names should appear explicitly
        assert "Name 0" in description
        assert "Name 1" in description
        assert "Name 2" in description

    def test_check_overdue_contacts_source_is_proactive(self) -> None:
        contacts = [self._OVERDUE]
        result = check_overdue_contacts(contacts)
        assert result[0].source == "proactive"

    def test_check_overdue_contacts_intent_is_check_contacts(self) -> None:
        contacts = [self._OVERDUE]
        result = check_overdue_contacts(contacts)
        assert result[0].intent == "check_contacts"

    def test_check_overdue_contacts_ignores_contact_without_follow_up_due(self) -> None:
        contacts = [{"name": "No Due Date"}]
        result = check_overdue_contacts(contacts)
        assert result == []
