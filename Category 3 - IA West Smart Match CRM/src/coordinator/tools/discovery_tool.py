"""Discovery tool wrapper — thin adapter over scrape_university().

No Streamlit imports. Exceptions propagate to result_bus for error capture.
"""

from __future__ import annotations

import logging
from typing import Any

from src.extraction.llm_extractor import extract_events
from src.scraping.scraper import UNIVERSITY_TARGETS, scrape_university

TOOL_NAME: str = "discover_events"

_DEFAULT_UNIVERSITY: str = next(iter(UNIVERSITY_TARGETS))
logger = logging.getLogger(__name__)


def run(params: dict[str, Any]) -> dict[str, Any]:
    """Run university event discovery.

    Args:
        params: Optional dict with key "university" (e.g. "UCLA").
                Defaults to the first UNIVERSITY_TARGETS key.

    Returns:
        {"status": "ok", "events": [...], "source": "cache"|"live"|...}

    Raises:
        PermissionError: Propagated when the target blocks automated access.
    """
    university_key = params.get("university", _DEFAULT_UNIVERSITY)
    target = UNIVERSITY_TARGETS.get(university_key, UNIVERSITY_TARGETS[_DEFAULT_UNIVERSITY])
    try:
        result = scrape_university(url=target["url"], method=target["method"])  # type: ignore[arg-type]
    except PermissionError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.warning("Discovery scrape failed for %s: %s", target["url"], exc)
        return {"status": "ok", "events": [], "source": "live"}

    source = str(result.get("source", "live"))
    html = str(result.get("html", "") or "")
    try:
        events = extract_events(
            raw_html=html,
            university=str(university_key),
            url=str(target["url"]),
            prefer_cache=True,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Discovery extraction failed for %s: %s", target["url"], exc)
        events = []

    return {
        "status": "ok",
        "events": events,
        "source": source,
    }
