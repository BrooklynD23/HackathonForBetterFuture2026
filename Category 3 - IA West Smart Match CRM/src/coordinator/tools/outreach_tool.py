"""Outreach tool wrapper — thin adapter over generate_outreach_email().

No Streamlit imports.
"""

from __future__ import annotations

from typing import Any

from src.outreach.email_gen import generate_outreach_email

TOOL_NAME: str = "generate_outreach"

_REQUIRED_KEYS: tuple[str, ...] = ("speaker", "event", "match_scores")


def run(params: dict[str, Any]) -> dict[str, Any]:
    """Run outreach email generation for a speaker-event match.

    Args:
        params: Must contain "speaker", "event", "match_scores".

    Returns:
        {"status": "ok", "email": {...}} on success.
        {"status": "error", "error": "Missing required param: <key>"} if a
        required param is absent.
    """
    for key in _REQUIRED_KEYS:
        if key not in params:
            return {"status": "error", "error": f"Missing required param: {key}"}

    email = generate_outreach_email(
        speaker=params["speaker"],
        event=params["event"],
        match_scores=params["match_scores"],
    )
    return {"status": "ok", "email": email}
