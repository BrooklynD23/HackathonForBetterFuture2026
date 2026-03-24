"""
Page router for IA SmartMatch — manages session_state navigation.

Supports navigation between: landing, login, coordinator, match_engine.
Also tracks user role and authentication state.
"""

from __future__ import annotations

import streamlit as st

# Ordered tuple of all valid page names.
PAGES: tuple[str, ...] = ("landing", "login", "coordinator", "match_engine")


def init_page_state() -> None:
    """
    Initialise required session_state keys if not already set.

    Sets current_page to "landing" and user_role to None on first run.
    """
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None


def get_current_page() -> str:
    """Return the name of the currently active page."""
    return st.session_state.get("current_page", "landing")


def navigate_to(page: str) -> None:
    """
    Navigate to a page by name and trigger a Streamlit rerun.

    Args:
        page: One of the values in PAGES.
    """
    st.session_state["current_page"] = page
    st.rerun()


def set_user_role(role: str) -> None:
    """
    Set the authenticated user's role.

    Args:
        role: Role string (e.g. "coordinator", "admin").
    """
    st.session_state["user_role"] = role


def get_user_role() -> str | None:
    """Return the current user's role, or None if not authenticated."""
    return st.session_state.get("user_role")


def is_authenticated() -> bool:
    """Return True if a user role has been set (i.e. user is logged in)."""
    return st.session_state.get("user_role") is not None
