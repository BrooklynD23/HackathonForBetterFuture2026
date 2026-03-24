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
