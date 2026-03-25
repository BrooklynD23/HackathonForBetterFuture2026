"""IA SmartMatch CRM — Streamlit application entry point."""

import logging

import numpy as np
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="IA SmartMatch CRM",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.ui.styles import inject_custom_css  # noqa: E402
inject_custom_css()

from src.config import CACHE_DIR, has_gemini_api_key, validate_config  # noqa: E402
from src.data_loader import load_all  # noqa: E402
from src.embeddings import (  # noqa: E402
    EMBEDDING_CACHE_FILES,
    generate_embedding_lookup_dicts,
    load_embedding_lookup_dicts,
)
from src.feedback.acceptance import render_feedback_sidebar  # noqa: E402
from src.demo_mode import init_demo_mode  # noqa: E402
from src.runtime_state import (  # noqa: E402
    get_match_results_df,
    get_matching_events_df,
    init_runtime_state,
)
from src.utils import format_course_identifier, summarize_missing_keys  # noqa: E402

logger = logging.getLogger(__name__)

DATASET_FILE_NAMES = {
    "speakers": "data_speaker_profiles.csv",
    "events": "data_cpp_events_contacts.csv",
    "courses": "data_cpp_course_schedule.csv",
    "calendar": "data_event_calendar.csv",
}


def _embedding_cache_issues(
    datasets,
    speaker_embeddings: dict[str, np.ndarray],
    event_embeddings: dict[str, np.ndarray],
    course_embeddings: dict[str, np.ndarray],
) -> list[str]:
    """Return human-readable validation issues for the on-disk embedding cache."""
    issues: list[str] = []

    missing_files = [
        file_name for file_name in EMBEDDING_CACHE_FILES
        if not (CACHE_DIR / file_name).exists()
    ]
    if missing_files:
        issues.append(f"Missing cache files: {', '.join(missing_files)}.")

    speaker_missing_count, speaker_examples = summarize_missing_keys(
        datasets.speakers["Name"],
        speaker_embeddings.keys(),
    )
    if speaker_missing_count:
        issues.append(
            "Speaker embedding coverage is incomplete: "
            f"{speaker_missing_count} missing"
            f"{' (examples: ' + ', '.join(speaker_examples) + ')' if speaker_examples else ''}."
        )

    event_missing_count, event_examples = summarize_missing_keys(
        datasets.events["Event / Program"],
        event_embeddings.keys(),
    )
    if event_missing_count:
        issues.append(
            "Event embedding coverage is incomplete: "
            f"{event_missing_count} missing"
            f"{' (examples: ' + ', '.join(event_examples) + ')' if event_examples else ''}."
        )

    expected_course_keys = (
        format_course_identifier(row.get("Course"), row.get("Section"))
        for _, row in datasets.courses.iterrows()
    )
    course_missing_count, course_examples = summarize_missing_keys(
        expected_course_keys,
        course_embeddings.keys(),
    )
    if course_missing_count:
        issues.append(
            "Course embedding coverage is incomplete: "
            f"{course_missing_count} missing"
            f"{' (examples: ' + ', '.join(course_examples) + ')' if course_examples else ''}."
        )

    return issues


def _resolve_embedding_lookup_dicts(
    datasets,
) -> tuple[
    dict[str, np.ndarray],
    dict[str, np.ndarray],
    dict[str, np.ndarray],
    list[str],
    str | None,
    bool,
]:
    """Load embedding caches and bootstrap them on demand when possible."""
    speaker_embeddings, event_embeddings, course_embeddings = load_embedding_lookup_dicts()
    embedding_issues = _embedding_cache_issues(
        datasets=datasets,
        speaker_embeddings=speaker_embeddings,
        event_embeddings=event_embeddings,
        course_embeddings=course_embeddings,
    )
    embedding_bootstrap_error = None
    cache_generated = False

    if _should_attempt_embedding_bootstrap(embedding_issues):
        try:
            speaker_embeddings, event_embeddings, course_embeddings = generate_embedding_lookup_dicts(
                speakers_df=datasets.speakers,
                events_df=datasets.events,
                courses_df=datasets.courses,
            )
            cache_generated = True
        except Exception as exc:
            logger.exception("Failed to bootstrap embedding cache.")
            embedding_bootstrap_error = str(exc)

        embedding_issues = _embedding_cache_issues(
            datasets=datasets,
            speaker_embeddings=speaker_embeddings,
            event_embeddings=event_embeddings,
            course_embeddings=course_embeddings,
        )

    return (
        speaker_embeddings,
        event_embeddings,
        course_embeddings,
        embedding_issues,
        embedding_bootstrap_error,
        cache_generated and not embedding_issues,
    )


def _empty_dataset_issues(datasets) -> list[str]:
    """Return file-specific errors for headers-only or empty datasets."""
    issues: list[str] = []
    for attr_name, file_name in DATASET_FILE_NAMES.items():
        dataset = getattr(datasets, attr_name)
        if len(dataset) == 0:
            issues.append(f"No {attr_name} found in data file. Please check {file_name}.")
    return issues


def _should_attempt_embedding_bootstrap(embedding_issues: list[str]) -> bool:
    """Skip live Gemini cache generation when the app is intentionally offline."""
    if not embedding_issues:
        return False
    if st.session_state.get("demo_mode", False):
        return False
    return has_gemini_api_key()


def _matches_tab_can_render(embedding_issues: list[str]) -> bool:
    """Allow non-topic matching to remain usable in demo/offline conditions."""
    if not embedding_issues:
        return True
    return st.session_state.get("demo_mode", False) or not has_gemini_api_key()


# ── Sidebar ─────────────────────────────────────────────────────────────────

def render_sidebar():
    """Render the sidebar with IA West branding and navigation."""
    with st.sidebar:
        st.markdown("## IA SmartMatch")
        st.markdown("**AI-Orchestrated Speaker-Event Matching**")
        st.markdown("*Insights Association — West Chapter*")
        st.divider()

        st.markdown("### About")
        st.markdown(
            "SmartMatch uses AI to discover university engagement "
            "opportunities, match them with the right IA West board "
            "member volunteers, and track the engagement-to-membership pipeline."
        )
        st.divider()

        st.markdown("### Data Summary")
        data_container = st.container()
        st.divider()
        init_demo_mode()
        st.checkbox(
            "Demo Mode (offline fixtures)",
            key="demo_mode",
            help="Toggle to use cached fixture data instead of live API calls.",
        )

        return data_container


WORKSPACE_NAV_ITEMS = (
    ("Dashboard", "dashboard"),
    ("Matches", "matches"),
    ("Discovery", "discovery"),
    ("Pipeline", "pipeline"),
    ("Analytics", "analytics"),
    ("Match Engine", "match_engine"),
)


def _render_workspace_navigation(current_page: str) -> None:
    """Render the primary workspace navigation row for authenticated pages."""
    from src.ui.page_router import navigate_to  # noqa: E402

    cols = st.columns(len(WORKSPACE_NAV_ITEMS) + 1)
    for (label, page), col in zip(WORKSPACE_NAV_ITEMS, cols, strict=False):
        with col:
            if st.button(
                label,
                key=f"workspace_nav_{page}",
                use_container_width=True,
                disabled=current_page == page,
            ):
                navigate_to(page)
    with cols[-1]:
        if st.button("Sign Out", key="workspace_nav_sign_out", use_container_width=True):
            navigate_to("landing", role=None, demo=False)
    st.divider()


def _render_matches_workspace(
    *,
    available_events,
    datasets,
    speaker_embeddings,
    event_embeddings,
    course_embeddings,
    embedding_issues,
    embedding_bootstrap_error,
    matches_tab_available: bool,
) -> None:
    """Render the matches workspace page with embedding warnings."""
    st.header("Matches")
    if embedding_issues:
        if matches_tab_available:
            st.warning(
                "Embedding cache missing or incomplete. Matches remain available, but "
                "topic relevance is using fallback scoring until embeddings are regenerated."
            )
        else:
            st.error(
                "Embedding cache missing or incomplete. Matches can run after the app "
                "successfully generates speaker, event, and course embeddings."
            )
        with st.expander("Embedding cache validation details", expanded=True):
            for issue in embedding_issues:
                st.write(f"- {issue}")
            if embedding_bootstrap_error:
                st.write(f"- Automatic generation failed: {embedding_bootstrap_error}")
            elif st.session_state.get("demo_mode", False):
                st.write("- Automatic generation is skipped while Demo Mode is enabled.")
            elif not has_gemini_api_key():
                st.write("- Automatic generation is unavailable until `GEMINI_API_KEY` is configured.")
    if matches_tab_available:
        from src.ui.matches_tab import render_matches_tab as render_matches_tab_ui  # noqa: E402

        render_matches_tab_ui(
            events=available_events,
            courses=datasets.courses,
            speakers=datasets.speakers,
            speaker_embeddings=speaker_embeddings,
            event_embeddings=event_embeddings,
            course_embeddings=course_embeddings,
            ia_event_calendar=datasets.calendar,
        )


def _render_analytics_workspace(datasets, available_events) -> None:
    """Render expansion and volunteer analytics in a reachable routed page."""
    from src.feedback.acceptance import init_feedback_state  # noqa: E402
    from src.ui.expansion_map import render_expansion_map  # noqa: E402
    from src.ui.volunteer_dashboard import render_volunteer_dashboard  # noqa: E402

    st.header("Analytics")
    st.caption("Coverage, expansion readiness, and volunteer engagement analytics.")

    threshold = st.slider(
        "Proximity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.30,
        step=0.05,
        key="expansion_threshold",
    )
    figure = render_expansion_map(datasets.speakers, threshold)
    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": False},
        key="expansion_map",
    )

    init_feedback_state()
    feedback_log = st.session_state.get("feedback_log", [])
    render_volunteer_dashboard(
        speakers_df=datasets.speakers,
        match_results=get_match_results_df(),
        events_df=available_events,
        feedback_log=feedback_log,
    )


# ── Main App ────────────────────────────────────────────────────────────────

def main() -> None:
    """Main application entry point."""
    init_runtime_state()
    config_errors = validate_config()
    if config_errors:
        st.error("Configuration errors detected:")
        for error in config_errors:
            st.error(f"  - {error}")
        st.stop()

    # ── V2 Page Routing ──────────────────────────────────────────────────────
    from src.ui.page_router import init_page_state, get_current_page  # noqa: E402
    init_page_state()
    current_page = get_current_page()

    if current_page == "landing":
        from src.ui.landing_page_v2 import render_landing_page_v2  # noqa: E402
        render_landing_page_v2()
        return

    if current_page == "login":
        from src.ui.login_page import render_login_page  # noqa: E402
        render_login_page()
        return

    sidebar_container = render_sidebar()

    with st.spinner("Loading data..."):
        try:
            datasets = load_all()
        except Exception:
            logger.exception("Failed to load datasets.")
            st.error("Failed to load data. Please check the application logs for details.")
            st.stop()
            return

    with sidebar_container:
        st.metric("Speakers", len(datasets.speakers))
        st.metric("Events", len(datasets.events))
        st.metric("Courses", len(datasets.courses))
        st.metric("Calendar Entries", len(datasets.calendar))
        total = sum(len(df) for df in [
            datasets.speakers, datasets.events,
            datasets.courses, datasets.calendar,
        ])
        st.metric("Total Records", total)

    empty_dataset_issues = _empty_dataset_issues(datasets)
    if empty_dataset_issues:
        with st.sidebar:
            for issue in empty_dataset_issues:
                st.error(issue)
        st.stop()
        return

    all_issues = []
    for qr in datasets.quality_results:
        all_issues.extend(qr.issues)
    if all_issues:
        with st.sidebar:
            with st.expander("Data Quality Warnings", expanded=False):
                for issue in all_issues:
                    st.warning(issue)

    available_events = get_matching_events_df(datasets.events)

    with st.spinner("Preparing embedding cache..."):
        (
            speaker_embeddings,
            event_embeddings,
            course_embeddings,
            embedding_issues,
            embedding_bootstrap_error,
            cache_generated,
        ) = _resolve_embedding_lookup_dicts(datasets)

    if cache_generated:
        with st.sidebar:
            st.success("Embedding cache generated successfully for Matches.")

    matches_tab_available = _matches_tab_can_render(embedding_issues)

    if embedding_issues:
        logger.error("Embedding cache validation failed: %s", "; ".join(embedding_issues))
        with st.sidebar:
            if matches_tab_available:
                st.warning(
                    "Embedding cache missing or incomplete. Matches will continue with fallback "
                    "scoring until speaker, event, and course embeddings are regenerated."
                )
            elif embedding_bootstrap_error:
                st.error(
                    "Embedding cache generation failed. Matching remains disabled until "
                    "the cache can be regenerated."
                )
            elif has_gemini_api_key():
                st.error(
                    "Embedding cache is still incomplete after automatic generation. "
                    "Matching remains disabled until the cache is regenerated."
                )
            else:
                st.error(
                    "Embedding cache missing or incomplete. Configure `GEMINI_API_KEY` "
                    "to let the app generate it automatically."
                )

    _render_workspace_navigation(current_page)

    if current_page == "dashboard":
        from src.ui.coordinator_dashboard import render_coordinator_dashboard  # noqa: E402

        show_dashboard_command_center = st.checkbox(
            "Show Jarvis Command Center",
            key="show_dashboard_command_center",
            help="Keep Jarvis close to the workspace nav during demos and live coordinator reviews.",
        )
        render_coordinator_dashboard(datasets.speakers)
        if show_dashboard_command_center:
            from src.ui.command_center import render_command_center_tab  # noqa: E402

            st.divider()
            render_command_center_tab()
    elif current_page == "matches":
        _render_matches_workspace(
            available_events=available_events,
            datasets=datasets,
            speaker_embeddings=speaker_embeddings,
            event_embeddings=event_embeddings,
            course_embeddings=course_embeddings,
            embedding_issues=embedding_issues,
            embedding_bootstrap_error=embedding_bootstrap_error,
            matches_tab_available=matches_tab_available,
        )
    elif current_page == "discovery":
        from src.ui.discovery_tab import render_discovery_tab  # noqa: E402

        render_discovery_tab(datasets)
    elif current_page == "pipeline":
        from src.ui.pipeline_tab import render_pipeline_tab  # noqa: E402

        render_pipeline_tab()
    elif current_page == "analytics":
        _render_analytics_workspace(datasets, available_events)
    elif current_page == "match_engine":
        from src.ui.match_engine_page import render_match_engine_page  # noqa: E402

        render_match_engine_page()
    else:
        from src.ui.page_router import navigate_to  # noqa: E402

        navigate_to("landing")
        return

    render_feedback_sidebar()


if __name__ == "__main__":
    main()
