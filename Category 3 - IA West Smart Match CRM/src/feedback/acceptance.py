"""
Match Acceptance Feedback Loop

Captures accept/decline decisions on match cards, stores in session state,
optionally persists to CSV, and generates weight adjustment suggestions
based on aggregated feedback patterns.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import streamlit as st

from src.config import DEFAULT_WEIGHTS

# ---------- Data Structures ----------

DECLINE_REASONS: List[str] = [
    "Too far (geographic distance)",
    "Schedule conflict",
    "Topic mismatch",
    "Speaker already committed",
    "Other",
]

DEFAULT_CSV_PATH: str = "data/feedback_log.csv"


@dataclass
class FeedbackEntry:
    """Single accept/decline decision."""

    timestamp: str  # ISO format
    event_id: str  # Event name or ID
    speaker_id: str  # Speaker name
    match_score: float  # Composite score at time of decision
    decision: str  # "accept" or "decline"
    decline_reason: Optional[str] = None  # One of DECLINE_REASONS
    decline_notes: Optional[str] = None  # Free-text for "Other"
    factor_scores: Dict[str, float] = field(default_factory=dict)


def init_feedback_state() -> None:
    """Initialize session state for feedback tracking."""
    if "feedback_log" not in st.session_state:
        st.session_state["feedback_log"] = []
    if "feedback_decisions" not in st.session_state:
        st.session_state["feedback_decisions"] = {}


def record_feedback(entry: FeedbackEntry) -> None:
    """Record a feedback decision in session state and persist to CSV."""
    init_feedback_state()
    entry_dict = asdict(entry)
    # Convert factor_scores dict to JSON string for CSV storage
    entry_dict["factor_scores"] = json.dumps(entry_dict["factor_scores"])
    st.session_state["feedback_log"].append(entry_dict)
    st.session_state["feedback_decisions"][
        (entry.event_id, entry.speaker_id)
    ] = entry.decision
    # Persist to CSV
    _persist_to_csv(entry_dict)


def _persist_to_csv(
    entry_dict: Dict,
    csv_path: str = DEFAULT_CSV_PATH,
) -> None:
    """Append feedback entry to CSV file."""
    df_new = pd.DataFrame([entry_dict])
    if os.path.exists(csv_path):
        df_new.to_csv(csv_path, mode="a", header=False, index=False)
    else:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df_new.to_csv(csv_path, index=False)


def get_decision(event_id: str, speaker_id: str) -> Optional[str]:
    """Check if a decision has already been made for this match."""
    init_feedback_state()
    return st.session_state["feedback_decisions"].get(
        (event_id, speaker_id), None
    )


# ---------- Feedback UI Components ----------


def render_feedback_buttons(
    event_id: str,
    speaker_id: str,
    match_score: float,
    factor_scores: Dict[str, float],
) -> None:
    """
    Render accept/decline buttons on a match card.
    If already decided, show the decision badge instead.
    """
    init_feedback_state()
    existing = get_decision(event_id, speaker_id)
    card_key = f"fb_{event_id}_{speaker_id}".replace(" ", "_")

    if existing == "accept":
        st.success("Accepted", icon="\u2705")
        return
    elif existing == "decline":
        st.error("Declined", icon="\u274C")
        return

    col_accept, col_decline = st.columns(2)
    with col_accept:
        if st.button(
            "Accept Match",
            key=f"{card_key}_accept",
            type="primary",
            use_container_width=True,
        ):
            entry = FeedbackEntry(
                timestamp=datetime.now().isoformat(),
                event_id=event_id,
                speaker_id=speaker_id,
                match_score=match_score,
                decision="accept",
                factor_scores=factor_scores,
            )
            record_feedback(entry)
            st.rerun()

    with col_decline:
        if st.button(
            "Decline Match",
            key=f"{card_key}_decline",
            use_container_width=True,
        ):
            st.session_state[f"{card_key}_show_reason"] = True
            st.rerun()

    # Decline reason prompt
    if st.session_state.get(f"{card_key}_show_reason", False):
        st.markdown("**Why are you declining this match?**")
        reason = st.radio(
            "Select reason:",
            DECLINE_REASONS,
            key=f"{card_key}_reason_radio",
            label_visibility="collapsed",
        )
        notes = ""
        if reason == "Other":
            notes = st.text_input(
                "Please specify:",
                key=f"{card_key}_other_notes",
            )
        if st.button("Submit Decline", key=f"{card_key}_submit_decline"):
            entry = FeedbackEntry(
                timestamp=datetime.now().isoformat(),
                event_id=event_id,
                speaker_id=speaker_id,
                match_score=match_score,
                decision="decline",
                decline_reason=reason,
                decline_notes=notes if reason == "Other" else None,
                factor_scores=factor_scores,
            )
            record_feedback(entry)
            del st.session_state[f"{card_key}_show_reason"]
            st.rerun()


# ---------- Feedback Aggregation & Weight Suggestions ----------

# Weight factor mapping: decline reason -> scoring factor to adjust
REASON_TO_FACTOR: Dict[str, str] = {
    "Too far (geographic distance)": "geographic_proximity",
    "Schedule conflict": "calendar_fit",
    "Topic mismatch": "topic_relevance",
    "Speaker already committed": "historical_conversion",
}


def aggregate_feedback() -> Dict:
    """
    Aggregate all feedback entries into summary statistics.

    Returns:
        {
            "total": int,
            "accepted": int,
            "declined": int,
            "acceptance_rate": float,
            "decline_reasons": {reason: count},
            "avg_score_accepted": float,
            "avg_score_declined": float,
        }
    """
    init_feedback_state()
    log = st.session_state["feedback_log"]
    if not log:
        return {
            "total": 0,
            "accepted": 0,
            "declined": 0,
            "acceptance_rate": 0.0,
            "decline_reasons": {},
            "avg_score_accepted": 0.0,
            "avg_score_declined": 0.0,
        }

    df = pd.DataFrame(log)
    total = len(df)
    accepted = len(df[df["decision"] == "accept"])
    declined = len(df[df["decision"] == "decline"])
    acceptance_rate = accepted / total if total > 0 else 0.0

    decline_reasons: Dict[str, int] = {}
    declined_df = df[df["decision"] == "decline"]
    if not declined_df.empty and "decline_reason" in declined_df.columns:
        decline_reasons = declined_df["decline_reason"].value_counts().to_dict()

    avg_accepted = (
        df[df["decision"] == "accept"]["match_score"].mean()
        if accepted > 0
        else 0.0
    )
    avg_declined = (
        df[df["decision"] == "decline"]["match_score"].mean()
        if declined > 0
        else 0.0
    )

    return {
        "total": total,
        "accepted": accepted,
        "declined": declined,
        "acceptance_rate": acceptance_rate,
        "decline_reasons": decline_reasons,
        "avg_score_accepted": round(avg_accepted, 3),
        "avg_score_declined": round(avg_declined, 3),
    }


def generate_weight_suggestions(
    min_declines_for_suggestion: int = 3,
    weight_bump: float = 0.05,
) -> List[str]:
    """
    Analyze decline reasons and suggest weight adjustments.

    Rule: If a decline reason appears >= min_declines_for_suggestion times,
    suggest increasing the corresponding scoring factor weight.

    Returns list of human-readable suggestion strings.
    """
    summary = aggregate_feedback()
    suggestions: List[str] = []

    for reason, count in summary["decline_reasons"].items():
        if count >= min_declines_for_suggestion and reason in REASON_TO_FACTOR:
            factor = REASON_TO_FACTOR[reason]
            current_w = DEFAULT_WEIGHTS.get(factor, 0.0)
            suggested_w = round(current_w + weight_bump, 2)
            suggestions.append(
                f"Based on {count} declines citing "
                f'"{reason}", consider increasing '
                f"`{factor}` weight from {current_w:.2f} to "
                f"{suggested_w:.2f}."
            )

    if (
        summary["accepted"] > 0
        and summary["declined"] > 0
        and summary["avg_score_declined"] > summary["avg_score_accepted"]
    ):
        suggestions.append(
            "Note: Declined matches have a higher average score "
            f"({summary['avg_score_declined']:.3f}) than accepted matches "
            f"({summary['avg_score_accepted']:.3f}). The scoring formula "
            "may not be capturing the decision criteria that matter most "
            "to chapter leadership."
        )

    return suggestions


# ---------- Sidebar Feedback Summary ----------


def render_feedback_sidebar() -> None:
    """Render feedback summary in the Streamlit sidebar."""
    init_feedback_state()
    summary = aggregate_feedback()

    if summary["total"] == 0:
        st.sidebar.markdown("---")
        st.sidebar.caption("No match feedback recorded yet.")
        return

    st.sidebar.markdown("---")
    st.sidebar.subheader("Match Feedback Summary")

    col1, col2, col3 = st.sidebar.columns(3)
    col1.metric("Total", summary["total"])
    col2.metric("Accepted", summary["accepted"])
    col3.metric("Declined", summary["declined"])

    st.sidebar.metric(
        "Acceptance Rate",
        f"{summary['acceptance_rate']:.0%}",
    )

    if summary["decline_reasons"]:
        st.sidebar.markdown("**Decline Reasons:**")
        for reason, count in sorted(
            summary["decline_reasons"].items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            st.sidebar.markdown(f"- {reason}: **{count}**")

    suggestions = generate_weight_suggestions()
    if suggestions:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Weight Adjustment Suggestions:**")
        for s in suggestions:
            st.sidebar.info(s)
