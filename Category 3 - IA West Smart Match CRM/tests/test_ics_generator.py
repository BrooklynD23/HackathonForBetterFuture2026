"""Tests for calendar invite .ics generation (A2.5)."""

from __future__ import annotations

import pytest


class TestGenerateIcsValidRfc5545:
    """Generated .ics content must conform to RFC 5545 structure."""

    def test_generate_ics_valid_rfc5545(self) -> None:
        """Output contains required RFC 5545 markers."""
        from src.outreach.ics_generator import generate_ics

        result = generate_ics(
            event_name="AI Hackathon",
            date_str="2026-04-15",
            location="Cal Poly Pomona",
            description="A hackathon event",
        )

        assert "BEGIN:VCALENDAR" in result
        assert "BEGIN:VEVENT" in result
        assert "END:VEVENT" in result
        assert "END:VCALENDAR" in result


class TestIcsVeventFields:
    """VEVENT must contain required fields."""

    def test_ics_contains_vevent_fields(self) -> None:
        """Output contains SUMMARY, DTSTART, LOCATION, DESCRIPTION."""
        from src.outreach.ics_generator import generate_ics

        result = generate_ics(
            event_name="AI Hackathon",
            date_str="2026-04-15",
            location="Cal Poly Pomona",
            description="A hackathon event",
        )

        assert "SUMMARY:AI Hackathon" in result
        assert "DTSTART:" in result
        assert "LOCATION:Cal Poly Pomona" in result
        assert "DESCRIPTION:A hackathon event" in result


class TestIcsMissingDate:
    """Graceful handling when date is missing or unparseable."""

    def test_ics_handles_missing_date_gracefully(self) -> None:
        """None date still produces valid .ics with DTSTART."""
        from src.outreach.ics_generator import generate_ics

        result = generate_ics(
            event_name="AI Hackathon",
            date_str=None,
            location="Cal Poly Pomona",
            description="A hackathon event",
        )

        assert "BEGIN:VCALENDAR" in result
        assert "DTSTART:" in result

    def test_ics_handles_unparseable_date(self) -> None:
        """Non-date string like 'Every Tuesday' still produces valid .ics."""
        from src.outreach.ics_generator import generate_ics

        result = generate_ics(
            event_name="Weekly Seminar",
            date_str="Every Tuesday",
            location="UCLA",
            description="Recurring seminar",
        )

        assert "BEGIN:VCALENDAR" in result
        assert "DTSTART:" in result


class TestIcsMissingLocation:
    """LOCATION field should be omitted when location is None."""

    def test_ics_handles_missing_location(self) -> None:
        """When location is None, LOCATION line must not appear."""
        from src.outreach.ics_generator import generate_ics

        result = generate_ics(
            event_name="AI Hackathon",
            date_str="2026-04-15",
            location=None,
            description="A hackathon event",
        )

        assert "LOCATION" not in result
        assert "BEGIN:VEVENT" in result


class TestIcsUidUnique:
    """Each event should get a unique, deterministic UID."""

    def test_ics_uid_unique_per_event(self) -> None:
        """Different event_name + date_str combos produce different UIDs."""
        from src.outreach.ics_generator import generate_ics

        ics_a = generate_ics(
            event_name="Event A",
            date_str="2026-04-15",
            location="Place A",
            description="Desc A",
        )
        ics_b = generate_ics(
            event_name="Event B",
            date_str="2026-04-16",
            location="Place B",
            description="Desc B",
        )

        # Extract UID lines
        uid_a = [line for line in ics_a.splitlines() if line.startswith("UID:")]
        uid_b = [line for line in ics_b.splitlines() if line.startswith("UID:")]

        assert len(uid_a) == 1
        assert len(uid_b) == 1
        assert uid_a[0] != uid_b[0]

    def test_ics_uid_deterministic(self) -> None:
        """Same inputs always produce the same UID."""
        from src.outreach.ics_generator import generate_ics

        ics_1 = generate_ics(
            event_name="Event A",
            date_str="2026-04-15",
            location="Place",
            description="Desc",
        )
        ics_2 = generate_ics(
            event_name="Event A",
            date_str="2026-04-15",
            location="Place",
            description="Desc",
        )

        uid_1 = [line for line in ics_1.splitlines() if line.startswith("UID:")]
        uid_2 = [line for line in ics_2.splitlines() if line.startswith("UID:")]

        assert uid_1 == uid_2


class TestIcsContentType:
    """The MIME type for .ics files must be text/calendar."""

    def test_ics_content_type_correct(self) -> None:
        """get_ics_content_type returns 'text/calendar'."""
        from src.outreach.ics_generator import ICS_CONTENT_TYPE

        assert ICS_CONTENT_TYPE == "text/calendar"
