"""Discovery tool wrapper — thin adapter over scrape_university().

No Streamlit imports. Exceptions propagate to result_bus for error capture.
"""

from __future__ import annotations

from typing import Any

from src.scraping.scraper import UNIVERSITY_TARGETS, scrape_university

TOOL_NAME: str = "discover_events"

_DEFAULT_UNIVERSITY: str = next(iter(UNIVERSITY_TARGETS))


def run(params: dict[str, Any]) -> dict[str, Any]:
    """Run university event discovery.

    Args:
        params: Optional dict with key "university" (e.g. "UCLA").
                Defaults to the first UNIVERSITY_TARGETS key.

    Returns:
        {"status": "ok", "events": [...], "source": "cache"|"live"|...}

    Raises:
        Any exception from scrape_university() — caught by result_bus thread.
    """
    university_key = params.get("university", _DEFAULT_UNIVERSITY)
    target = UNIVERSITY_TARGETS.get(university_key, UNIVERSITY_TARGETS[_DEFAULT_UNIVERSITY])
    result = scrape_university(url=target["url"], method=target["method"])  # type: ignore[arg-type]
    return {
        "status": "ok",
        "events": result.get("events", []),
        "source": result.get("source", "live"),
    }
