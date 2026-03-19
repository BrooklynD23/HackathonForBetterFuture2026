"""Pipeline funnel visualization tab for IA SmartMatch CRM."""

import logging
from collections import OrderedDict
from pathlib import Path
from typing import Final

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import DATA_DIR

logger = logging.getLogger(__name__)

# Ordered mapping: stage name -> minimum stage_order value that qualifies.
# "Discovered" is synthetic (all rows count); remaining stages use
# cumulative filtering: a row at stage_order >= N counts for that stage.
FUNNEL_STAGES: Final[OrderedDict[str, int]] = OrderedDict([
    ("Discovered", -1),       # all rows
    ("Matched", 0),           # stage_order >= 0
    ("Contacted", 1),         # stage_order >= 1
    ("Confirmed", 2),         # stage_order >= 2
    ("Attended", 3),          # stage_order >= 3
    ("Member Inquiry", 4),    # stage_order >= 4
])

PIPELINE_CSV: Final[str] = "pipeline_sample_data.csv"


def load_pipeline_data(csv_path: str | None = None) -> pd.DataFrame:
    """Load pipeline data from CSV, returning an empty DataFrame on error."""
    path = Path(csv_path) if csv_path else DATA_DIR / PIPELINE_CSV
    try:
        df = pd.read_csv(path)
        return df
    except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError, OSError) as exc:
        logger.warning("Could not load pipeline data from %s: %s", path, exc)
        return pd.DataFrame(
            columns=["event_name", "speaker_name", "match_score", "rank", "stage", "stage_order"]
        )


def aggregate_funnel_stages(df: pd.DataFrame) -> OrderedDict[str, int]:
    """Aggregate row counts for each funnel stage (cumulative, monotonically decreasing).

    Every row is "Discovered". A row with stage_order >= N counts toward
    stage N and all stages below N.
    """
    result: OrderedDict[str, int] = OrderedDict()
    for stage_name, min_order in FUNNEL_STAGES.items():
        if stage_name == "Discovered":
            result[stage_name] = len(df)
        else:
            if df.empty or "stage_order" not in df.columns:
                result[stage_name] = 0
            else:
                result[stage_name] = int((df["stage_order"] >= min_order).sum())
    return result


def _build_hover_text(df: pd.DataFrame, stage_name: str, min_order: int) -> str:
    """Build a hover tooltip listing speaker/event pairs for a funnel stage."""
    if df.empty or "stage_order" not in df.columns:
        return "No data"
    if stage_name == "Discovered":
        subset = df
    else:
        subset = df[df["stage_order"] >= min_order]
    if subset.empty:
        return "No records"
    lines: list[str] = []
    for _, row in subset.head(8).iterrows():
        speaker = row.get("speaker_name", "Unknown")
        event = row.get("event_name", "Unknown")
        lines.append(f"{speaker} — {event}")
    if len(subset) > 8:
        lines.append(f"... and {len(subset) - 8} more")
    return "<br>".join(lines)


def create_funnel_chart(
    df: pd.DataFrame,
    stage_counts: OrderedDict[str, int],
) -> go.Figure:
    """Create a Plotly Funnel chart for the engagement pipeline."""
    stage_names = list(stage_counts.keys())
    counts = list(stage_counts.values())

    hover_texts = [
        _build_hover_text(df, name, FUNNEL_STAGES[name])
        for name in stage_names
    ]

    fig = go.Figure()
    fig.add_trace(go.Funnel(
        y=stage_names,
        x=counts,
        text=[str(c) for c in counts],
        textposition="inside",
        hovertext=hover_texts,
        hoverinfo="text+name",
        marker=dict(
            color=[
                "#3182bd", "#6baed6", "#9ecae1",
                "#c6dbef", "#e6550d", "#fd8d3c",
            ],
        ),
        connector=dict(line=dict(color="royalblue", width=1)),
    ))

    fig.update_layout(
        title="Engagement Pipeline Funnel",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        height=420,
    )

    return fig


def _has_real_data(datasets: object) -> bool:
    """Check whether *datasets* carries enough real prototype data."""
    if datasets is None:
        return False
    mr = getattr(datasets, "match_results", None)
    if mr is None or (isinstance(mr, pd.DataFrame) and mr.empty):
        return False
    return True


def compute_real_funnel_data(
    scraped_events: list[dict],
    match_results: pd.DataFrame,
    feedback_log: list[dict],
    emails_generated: int,
) -> dict:
    """Compute funnel stage counts from real prototype data.

    Stages:
    1. Discovered — CPP events (15 known) + scraped university events.
    2. Matched — top-3 speaker-event pairs per event.
    3. Contacted — emails generated (or 80 % of matched as fallback).
    4. Confirmed — accepted feedback entries (or 45 % of contacted).
    5. Attended — 75 % of confirmed.
    6. Member Inquiry — 15 % of attended.

    Returns dict with ``stages``, ``counts``, ``hover_text``, and
    ``annotations`` keys.
    """
    cpp_event_count = 15
    scraped_count = len(scraped_events)
    discovered = cpp_event_count + scraped_count

    # Stage 2: Matched (top-3 per event)
    matched = 0
    match_annotations: list[str] = []
    if not match_results.empty and "event_id" in match_results.columns:
        for event_id in match_results["event_id"].unique():
            event_top3 = match_results[
                match_results["event_id"] == event_id
            ].nlargest(3, "total_score")
            matched += len(event_top3)
            for _, row in event_top3.iterrows():
                match_annotations.append(
                    f"{row['speaker_id']} -> {event_id} "
                    f"({row['total_score']:.0%})"
                )

    # Stage 3: Contacted
    contacted = emails_generated if emails_generated > 0 else int(matched * 0.80)

    # Stage 4: Confirmed
    accepted_from_feedback = sum(
        1 for f in feedback_log if f.get("decision") == "accept"
    )
    confirmed = (
        accepted_from_feedback
        if accepted_from_feedback > 0
        else int(contacted * 0.45)
    )

    # Stage 5: Attended
    attended = int(confirmed * 0.75)

    # Stage 6: Member Inquiry
    member_inquiry = int(attended * 0.15)

    universities = set(e.get("university", "") for e in scraped_events)

    return {
        "stages": [
            "Discovered", "Matched", "Contacted",
            "Confirmed", "Attended", "Member Inquiry",
        ],
        "counts": [
            discovered, matched, contacted,
            confirmed, attended, member_inquiry,
        ],
        "hover_text": [
            (
                f"{cpp_event_count} CPP events + {scraped_count} scraped "
                f"from {len(universities)} universities"
            ),
            (
                f"Top-3 matches per event<br>"
                + "<br>".join(match_annotations[:5])
                + (
                    f"<br>...and {len(match_annotations) - 5} more"
                    if len(match_annotations) > 5
                    else ""
                )
            ),
            f"{contacted} outreach emails generated",
            (
                f"{confirmed} volunteers confirmed "
                f"({'real feedback' if accepted_from_feedback > 0 else 'projected at 45%'})"
            ),
            f"{attended} events attended (projected at 75% of confirmed)",
            f"{member_inquiry} membership inquiries (projected at 15% of attended)",
        ],
        "annotations": match_annotations,
    }


def render_pipeline_tab(datasets: object) -> None:
    """Render the Pipeline tab with engagement funnel tracking.

    Prefers real prototype data from *datasets* when available;
    falls back to CSV-based pipeline data otherwise.
    """
    st.header("Engagement Pipeline")

    if _has_real_data(datasets):
        funnel = compute_real_funnel_data(
            scraped_events=getattr(datasets, "scraped_events", []),
            match_results=getattr(datasets, "match_results", pd.DataFrame()),
            feedback_log=getattr(datasets, "feedback_log", []),
            emails_generated=getattr(datasets, "emails_generated", 0),
        )
        stage_counts: OrderedDict[str, int] = OrderedDict(
            zip(funnel["stages"], funnel["counts"])
        )
        # Build a slim DataFrame for the data table / hover helpers
        df = pd.DataFrame({
            "stage": funnel["stages"],
            "count": funnel["counts"],
        })
        fig = create_funnel_chart(df, stage_counts)
    else:
        df = load_pipeline_data()
        stage_counts = aggregate_funnel_stages(df)
        fig = create_funnel_chart(df, stage_counts)

    st.plotly_chart(fig, use_container_width=True, key="pipeline_funnel")

    st.subheader("Pipeline Data")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No pipeline data available. Place pipeline_sample_data.csv in the data/ directory.")
