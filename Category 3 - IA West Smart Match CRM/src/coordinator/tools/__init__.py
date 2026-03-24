"""Tool wrapper package for the Coordinator agent.

Exports TOOL_REGISTRY mapping intent names to tool run() callables.
"""

from __future__ import annotations

from typing import Any, Callable

from src.coordinator.tools.contacts_tool import run as _contacts_run
from src.coordinator.tools.discovery_tool import run as _discovery_run
from src.coordinator.tools.matching_tool import run as _matching_run
from src.coordinator.tools.outreach_tool import run as _outreach_run

TOOL_REGISTRY: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "discover_events": _discovery_run,
    "rank_speakers": _matching_run,
    "generate_outreach": _outreach_run,
    "check_contacts": _contacts_run,
}

__all__ = ["TOOL_REGISTRY"]
