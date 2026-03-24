"""Proactive staleness suggestion engine.

Pure Python — no Streamlit imports. Fully testable in isolation.
"""

from __future__ import annotations

import datetime
import logging

from src.coordinator.approval import ActionProposal

logger = logging.getLogger(__name__)

STALENESS_HOURS: int = 24


def check_staleness_conditions(
    scraped_events: list,
    scraped_at: str | None,
) -> list[ActionProposal]:
    """Return proactive suggestions based on data staleness. Pure function.

    Returns a list containing one ActionProposal if data is stale or empty,
    otherwise returns an empty list.

    Per ORCH-04: Jarvis proactively suggests actions when data is stale.
    """
    if not scraped_events or _is_stale(scraped_at, hours=STALENESS_HOURS):
        return [
            ActionProposal(
                intent="discover_events",
                agent="Discovery Agent",
                description="Re-run event discovery scraper",
                reasoning="Discovery data is stale or empty — re-running will surface new events.",
                source="proactive",
            )
        ]
    return []


def _is_stale(timestamp_str: str | None, hours: int) -> bool:
    """Return True if timestamp_str is None, empty, unparseable, or older than hours."""
    if not timestamp_str:
        return True
    try:
        ts = datetime.datetime.fromisoformat(timestamp_str)
        return (datetime.datetime.now() - ts).total_seconds() > hours * 3600
    except ValueError:
        return True


def check_overdue_contacts(poc_contacts: list[dict]) -> list[ActionProposal]:
    """Return a proactive ActionProposal if any POC contacts are overdue for follow-up.

    Args:
        poc_contacts: List of contact dicts, each optionally containing a
            ``follow_up_due`` key in ISO date format (YYYY-MM-DD).

    Returns:
        A one-element list containing an ActionProposal when at least one
        contact has a ``follow_up_due`` date in the past, otherwise [].
    """
    today = datetime.date.today()
    overdue = [
        c for c in poc_contacts
        if c.get("follow_up_due")
        and datetime.date.fromisoformat(c["follow_up_due"]) < today
    ]
    if not overdue:
        return []
    names = ", ".join(c["name"] for c in overdue[:3])
    suffix = f" and {len(overdue) - 3} more" if len(overdue) > 3 else ""
    description = (
        f"{len(overdue)} contact(s) overdue for follow-up: "
        f"{names}{suffix} -- review now?"
    )
    return [
        ActionProposal(
            intent="check_contacts",
            agent="Contacts Agent",
            description=description,
            reasoning="POC contacts have passed their follow_up_due date.",
            source="proactive",
        )
    ]
