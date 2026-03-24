"""Contacts tool — loads POC contact data and identifies overdue follow-ups.

No Streamlit imports. No external service calls.
"""

from __future__ import annotations

import datetime
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

TOOL_NAME: str = "check_contacts"

_CONTACTS_PATH: Path = Path(__file__).resolve().parents[3] / "data" / "poc_contacts.json"


def _load_contacts() -> list[dict[str, Any]]:
    """Load POC contacts from disk. Returns [] on missing/invalid file."""
    try:
        return json.loads(_CONTACTS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logger.warning("poc_contacts.json not found at %s", _CONTACTS_PATH)
        return []
    except json.JSONDecodeError as exc:
        logger.warning("poc_contacts.json is invalid JSON: %s", exc)
        return []


def run(params: dict[str, Any]) -> dict[str, Any]:
    """Return all POC contacts and identify overdue follow-ups.

    A contact is overdue when its follow_up_due date (ISO 8601) is strictly
    before today.

    Args:
        params: Unused — reserved for future filtering options.

    Returns:
        {
            "status": "ok",
            "contacts": [...],
            "overdue": [...],
            "total": N,
            "overdue_count": M,
        }
    """
    contacts = _load_contacts()
    today = datetime.date.today()
    overdue = [
        c for c in contacts
        if c.get("follow_up_due") and datetime.date.fromisoformat(c["follow_up_due"]) < today
    ]
    return {
        "status": "ok",
        "contacts": contacts,
        "overdue": overdue,
        "total": len(contacts),
        "overdue_count": len(overdue),
    }
