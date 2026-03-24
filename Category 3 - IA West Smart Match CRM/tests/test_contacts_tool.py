"""Tests for contacts_tool wrapper."""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from unittest.mock import patch

import pytest


def _make_contacts(overdue_count: int = 2) -> list[dict]:
    today = datetime.date.today()
    past = (today - datetime.timedelta(days=30)).isoformat()
    future = (today + datetime.timedelta(days=30)).isoformat()
    contacts = []
    for i in range(overdue_count):
        contacts.append({
            "name": f"Overdue Contact {i}",
            "email": f"overdue{i}@example.com",
            "org": "Test Org",
            "role": "Director",
            "comm_history": [],
            "last_contact": past,
            "follow_up_due": past,
        })
    contacts.append({
        "name": "Future Contact",
        "email": "future@example.com",
        "org": "Future Org",
        "role": "Manager",
        "comm_history": [],
        "last_contact": past,
        "follow_up_due": future,
    })
    return contacts


class TestContactsToolRun:
    """Tests for contacts_tool.run()."""

    def test_run_returns_contacts_and_overdue(self):
        contacts = _make_contacts(overdue_count=2)
        with patch("src.coordinator.tools.contacts_tool._load_contacts", return_value=contacts):
            from src.coordinator.tools import contacts_tool
            result = contacts_tool.run({})
        assert result["status"] == "ok"
        assert result["total"] == 3
        assert result["overdue_count"] == 2
        assert len(result["overdue"]) == 2
        assert len(result["contacts"]) == 3

    def test_run_overdue_detection_with_past_dates(self):
        today = datetime.date.today()
        yesterday = (today - datetime.timedelta(days=1)).isoformat()
        contacts = [
            {"name": "A", "email": "a@x.com", "org": "Org", "role": "R",
             "comm_history": [], "last_contact": yesterday, "follow_up_due": yesterday},
        ]
        with patch("src.coordinator.tools.contacts_tool._load_contacts", return_value=contacts):
            from src.coordinator.tools import contacts_tool
            result = contacts_tool.run({})
        assert result["overdue_count"] == 1

    def test_run_empty_file_returns_graceful_empty(self):
        with patch("src.coordinator.tools.contacts_tool._load_contacts", return_value=[]):
            from src.coordinator.tools import contacts_tool
            result = contacts_tool.run({})
        assert result["status"] == "ok"
        assert result["total"] == 0
        assert result["overdue_count"] == 0
        assert result["contacts"] == []
        assert result["overdue"] == []

    def test_load_contacts_missing_file_returns_empty(self, tmp_path):
        from src.coordinator.tools import contacts_tool
        with patch.object(contacts_tool, "_CONTACTS_PATH", tmp_path / "nonexistent.json"):
            result = contacts_tool._load_contacts()
        assert result == []

    def test_load_contacts_invalid_json_returns_empty(self, tmp_path):
        bad_file = tmp_path / "contacts.json"
        bad_file.write_text("NOT VALID JSON")
        from src.coordinator.tools import contacts_tool
        with patch.object(contacts_tool, "_CONTACTS_PATH", bad_file):
            result = contacts_tool._load_contacts()
        assert result == []

    def test_tool_name_is_check_contacts(self):
        from src.coordinator.tools import contacts_tool
        assert contacts_tool.TOOL_NAME == "check_contacts"

    def test_no_streamlit_import(self):
        import inspect
        import src.coordinator.tools.contacts_tool as mod
        source = inspect.getsource(mod)
        assert "import streamlit" not in source
