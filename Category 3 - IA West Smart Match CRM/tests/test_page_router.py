"""Tests for the V2 page router."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from streamlit.errors import StreamlitAPIException


@patch("streamlit.session_state", new_callable=dict)
def test_init_page_state_normalizes_alias_and_flags(mock_state: dict) -> None:
    """Legacy aliases and query flags should hydrate normalized session state."""
    import src.ui.page_router as router

    with (
        patch.object(router, "_get_query_params", return_value={
            "route": "coordinator",
            "role": "coordinator",
            "demo": "1",
        }),
        patch.object(router, "_set_query_params") as mock_set,
    ):
        router.init_page_state()

    assert mock_state["current_page"] == "dashboard"
    assert mock_state["user_role"] == "coordinator"
    assert mock_state["demo_mode"] is True
    mock_set.assert_called_once_with(route="dashboard", role="coordinator", demo="1")


@patch("streamlit.session_state", new_callable=dict)
def test_init_page_state_falls_back_to_landing_for_unknown_route(mock_state: dict) -> None:
    """Unknown routes should fall back to landing."""
    import src.ui.page_router as router

    with (
        patch.object(router, "_get_query_params", return_value={"route": "unknown"}),
        patch.object(router, "_set_query_params") as mock_set,
    ):
        router.init_page_state()

    assert mock_state["current_page"] == "landing"
    mock_set.assert_called_once_with(route="landing", role="", demo="")


@patch("streamlit.session_state", new_callable=dict)
def test_navigate_to_updates_session_and_triggers_rerun(mock_state: dict) -> None:
    """navigate_to should persist page, role, demo state, and rerun."""
    import src.ui.page_router as router

    mock_state["current_page"] = "landing"
    mock_state["user_role"] = None
    mock_state["demo_mode"] = False

    with (
        patch.object(router, "_get_query_params", return_value={}),
        patch.object(router, "_set_query_params") as mock_set,
        patch.object(router.st, "rerun") as mock_rerun,
    ):
        router.navigate_to("coordinator", role="coordinator", demo=True)

    assert mock_state["current_page"] == "dashboard"
    assert mock_state["user_role"] == "coordinator"
    assert mock_state["demo_mode"] is True
    mock_set.assert_called_once_with(route="dashboard", role="coordinator", demo="1")
    mock_rerun.assert_called_once()


def test_get_query_params_prefers_query_params_mapping_when_available() -> None:
    """The pinned Streamlit runtime should prefer the modern query-param mapping."""
    import src.ui.page_router as router

    fake_st = SimpleNamespace(
        experimental_get_query_params=MagicMock(return_value={"route": ["landing"]}),
        experimental_set_query_params=lambda **_: None,
        query_params={"route": "matches", "demo": "1"},
    )

    with patch.object(router, "st", fake_st):
        assert router._get_query_params() == {"route": "matches", "demo": "1"}
        fake_st.experimental_get_query_params.assert_not_called()


def test_get_query_params_falls_back_to_experimental_api_without_query_params() -> None:
    """Older Streamlit builds should still use experimental query params."""
    import src.ui.page_router as router

    fake_st = SimpleNamespace(
        experimental_get_query_params=lambda: {"route": ["matches"], "demo": ["1"]},
        experimental_set_query_params=lambda **_: None,
    )

    with patch.object(router, "st", fake_st):
        assert router._get_query_params() == {"route": "matches", "demo": "1"}


@patch("streamlit.session_state", new_callable=dict)
def test_navigate_to_clears_role_and_demo_query_state(mock_state: dict) -> None:
    """Sign-out style navigation should clear stale role/demo params."""
    import src.ui.page_router as router

    mock_state["current_page"] = "dashboard"
    mock_state["user_role"] = "coordinator"
    mock_state["demo_mode"] = True

    with (
        patch.object(router, "_get_query_params", return_value={
            "route": "dashboard",
            "role": "coordinator",
            "demo": "1",
        }),
        patch.object(router, "_set_query_params") as mock_set,
        patch.object(router.st, "rerun") as mock_rerun,
    ):
        router.navigate_to("landing", role=None, demo=False)

    assert mock_state["current_page"] == "landing"
    assert mock_state["user_role"] is None
    assert mock_state["demo_mode"] is False
    assert router._PENDING_DEMO_MODE_KEY not in mock_state
    mock_set.assert_called_once_with(route="landing", role="", demo="")
    mock_rerun.assert_called_once()


def test_navigate_to_defers_demo_reset_when_widget_state_is_locked() -> None:
    """Sign-out should still clear URL state when the demo-mode widget is already mounted."""
    import src.ui.page_router as router

    class LockedSessionState(dict):
        lock_demo_mode = False

        def __setitem__(self, key, value) -> None:
            if key == "demo_mode" and self.lock_demo_mode:
                raise StreamlitAPIException("demo_mode is widget-managed")
            super().__setitem__(key, value)

    locked_state = LockedSessionState(
        current_page="dashboard",
        user_role="coordinator",
        demo_mode=True,
    )
    locked_state.lock_demo_mode = True
    fake_st = SimpleNamespace(session_state=locked_state, rerun=MagicMock())

    with (
        patch.object(router, "st", fake_st),
        patch.object(router, "_get_query_params", return_value={
            "route": "dashboard",
            "role": "coordinator",
            "demo": "1",
        }),
        patch.object(router, "_set_query_params") as mock_set,
    ):
        router.navigate_to("landing", role=None, demo=False)

    assert locked_state["current_page"] == "landing"
    assert locked_state["user_role"] is None
    assert locked_state["demo_mode"] is True
    assert locked_state[router._PENDING_DEMO_MODE_KEY] is False
    mock_set.assert_called_once_with(route="landing", role="", demo="")
    fake_st.rerun.assert_called_once()


@patch("streamlit.session_state", new_callable=dict)
def test_init_page_state_applies_pending_demo_override_before_widget_render(mock_state: dict) -> None:
    """Deferred demo-mode changes should hydrate before the sidebar checkbox is created."""
    import src.ui.page_router as router

    mock_state[router._PENDING_DEMO_MODE_KEY] = False

    with (
        patch.object(router, "_get_query_params", return_value={"route": "landing"}),
        patch.object(router, "_set_query_params") as mock_set,
    ):
        router.init_page_state()

    assert mock_state["demo_mode"] is False
    assert router._PENDING_DEMO_MODE_KEY not in mock_state
    mock_set.assert_not_called()
