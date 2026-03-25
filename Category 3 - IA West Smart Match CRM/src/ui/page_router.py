"""
Page router for IA SmartMatch.

Keeps Streamlit session state and URL query params aligned so both native
Streamlit controls and iframe-rendered HTML controls can navigate the app.
"""

from __future__ import annotations

from typing import Any

import streamlit as st
from streamlit.errors import StreamlitAPIException

LANDING_PAGE = "landing"
LOGIN_PAGE = "login"
DASHBOARD_PAGE = "dashboard"
MATCHES_PAGE = "matches"
DISCOVERY_PAGE = "discovery"
PIPELINE_PAGE = "pipeline"
ANALYTICS_PAGE = "analytics"
MATCH_ENGINE_PAGE = "match_engine"

PAGES: tuple[str, ...] = (
    LANDING_PAGE,
    LOGIN_PAGE,
    DASHBOARD_PAGE,
    MATCHES_PAGE,
    DISCOVERY_PAGE,
    PIPELINE_PAGE,
    ANALYTICS_PAGE,
    MATCH_ENGINE_PAGE,
)
PAGE_ALIASES: dict[str, str] = {
    "coordinator": DASHBOARD_PAGE,
    "crm": DASHBOARD_PAGE,
}
AUTHENTICATED_PAGES: frozenset[str] = frozenset(
    page for page in PAGES if page not in {LANDING_PAGE, LOGIN_PAGE}
)
_UNSET = object()
_PENDING_DEMO_MODE_KEY = "_pending_demo_mode"


def _first_param_value(value: Any) -> str | None:
    """Return the first string value from a query-param field."""
    if isinstance(value, list):
        return str(value[0]) if value else None
    if value is None:
        return None
    return str(value)


def _prefer_experimental_query_params() -> bool:
    """Use the legacy experimental API only when the modern mapping is absent."""
    return (
        not hasattr(st, "query_params")
        and hasattr(st, "experimental_get_query_params")
        and hasattr(st, "experimental_set_query_params")
    )


def _get_query_params() -> dict[str, str]:
    """Return query params as a plain string dict."""
    if hasattr(st, "query_params"):
        params = getattr(st, "query_params")
        normalized: dict[str, str] = {}
        for key in params.keys():
            value = _first_param_value(params[key])
            if value is not None:
                normalized[str(key)] = str(value)
        return normalized
    if _prefer_experimental_query_params():
        raw = st.experimental_get_query_params()
        return {
            str(key): str(_first_param_value(value) or "")
            for key, value in raw.items()
            if _first_param_value(value) is not None
        }
    return {}


def _set_query_params(**params: str) -> None:
    """Write a clean query-param set through the available Streamlit API."""
    clean = {key: value for key, value in params.items() if value}
    if hasattr(st, "query_params"):
        query_params = getattr(st, "query_params")
        query_params.clear()
        for key, value in clean.items():
            query_params[key] = value
        return
    if _prefer_experimental_query_params():
        st.experimental_set_query_params(**clean)


def _normalize_page(page: str | None) -> str:
    """Normalize aliases and unknown values to a supported page name."""
    candidate = (page or LANDING_PAGE).strip().lower()
    candidate = PAGE_ALIASES.get(candidate, candidate)
    if candidate not in PAGES:
        return LANDING_PAGE
    return candidate


def _as_query_flag(value: bool) -> str:
    """Encode a bool for query-param transport."""
    return "1" if value else ""


def _is_truthy_flag(value: str | None) -> bool:
    """Interpret common truthy flag values from query params."""
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _effective_demo_mode() -> bool:
    """Return the current demo mode, including any pending navigation override."""
    if _PENDING_DEMO_MODE_KEY in st.session_state:
        return bool(st.session_state[_PENDING_DEMO_MODE_KEY])
    return bool(st.session_state.get("demo_mode", False))


def _apply_pending_demo_mode() -> None:
    """Apply any deferred demo-mode change before widgets are instantiated."""
    if _PENDING_DEMO_MODE_KEY not in st.session_state:
        return
    st.session_state["demo_mode"] = bool(st.session_state.pop(_PENDING_DEMO_MODE_KEY))


def _set_demo_mode_for_navigation(value: bool) -> None:
    """Stage a demo-mode change and apply it immediately when Streamlit allows it."""
    st.session_state[_PENDING_DEMO_MODE_KEY] = value
    try:
        st.session_state["demo_mode"] = value
    except StreamlitAPIException:
        return
    st.session_state.pop(_PENDING_DEMO_MODE_KEY, None)


def _sync_query_params() -> None:
    """Mirror current session routing state into the URL."""
    current_page = _normalize_page(st.session_state.get("current_page"))
    role = st.session_state.get("user_role")
    demo_mode = _effective_demo_mode()
    target_params = {
        "route": current_page,
        "role": str(role) if role else "",
        "demo": _as_query_flag(demo_mode),
    }
    current_params = _get_query_params()
    if all(current_params.get(key, "") == value for key, value in target_params.items()):
        return
    _set_query_params(
        route=current_page,
        role=str(role) if role else "",
        demo=_as_query_flag(demo_mode),
    )


def init_page_state() -> None:
    """Initialize session state from defaults and URL query params."""
    _apply_pending_demo_mode()

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = LANDING_PAGE
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None

    params = _get_query_params()
    st.session_state["current_page"] = _normalize_page(
        params.get("route", st.session_state.get("current_page"))
    )

    role = params.get("role")
    if role:
        st.session_state["user_role"] = role

    if "demo" in params:
        st.session_state["demo_mode"] = _is_truthy_flag(params.get("demo"))

    _sync_query_params()


def get_current_page() -> str:
    """Return the normalized currently active page."""
    return _normalize_page(st.session_state.get("current_page"))


def navigate_to(page: str, *, role: str | None | object = _UNSET, demo: bool | None = None) -> None:
    """Navigate to a page and keep query params synchronized."""
    st.session_state["current_page"] = _normalize_page(page)
    if role is not _UNSET:
        st.session_state["user_role"] = role
    if demo is not None:
        _set_demo_mode_for_navigation(demo)
    _sync_query_params()
    st.rerun()


def set_user_role(role: str | None) -> None:
    """Set the authenticated user's role."""
    st.session_state["user_role"] = role
    _sync_query_params()


def get_user_role() -> str | None:
    """Return the current user's role, or None if not authenticated."""
    return st.session_state.get("user_role")


def is_authenticated() -> bool:
    """Return True if a user role has been set."""
    return st.session_state.get("user_role") is not None
