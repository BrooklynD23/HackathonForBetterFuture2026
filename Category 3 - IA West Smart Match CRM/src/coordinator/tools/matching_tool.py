"""Matching tool wrapper — thin adapter over rank_speakers_for_event().

No Streamlit imports.
"""

from __future__ import annotations

from typing import Any

from src.matching.engine import rank_speakers_for_event

TOOL_NAME: str = "rank_speakers"

_REQUIRED_KEYS: tuple[str, ...] = (
    "event_row",
    "speakers_df",
    "speaker_embeddings",
    "event_embedding",
    "ia_event_calendar",
)


def run(params: dict[str, Any]) -> dict[str, Any]:
    """Run speaker ranking for an event.

    Args:
        params: Must contain "event_row", "speakers_df", "speaker_embeddings",
                "event_embedding", "ia_event_calendar". Optional: "top_n",
                "weights", "conversion_overrides", "student_interest_override".

    Returns:
        {"status": "ok", "rankings": [...]} on success.
        {"status": "error", "error": "Missing required param: <key>"} if a
        required param is absent.
    """
    for key in _REQUIRED_KEYS:
        if key not in params:
            return {"status": "error", "error": f"Missing required param: {key}"}

    rankings = rank_speakers_for_event(
        event_row=params["event_row"],
        speakers_df=params["speakers_df"],
        speaker_embeddings=params["speaker_embeddings"],
        event_embedding=params["event_embedding"],
        ia_event_calendar=params["ia_event_calendar"],
        top_n=params.get("top_n", 10),
        weights=params.get("weights"),
        conversion_overrides=params.get("conversion_overrides"),
        student_interest_override=params.get("student_interest_override"),
    )
    return {"status": "ok", "rankings": rankings}
