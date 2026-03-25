"""Tests for the Match Engine page."""

import importlib
import sys
from types import ModuleType
from unittest.mock import MagicMock, patch


def _setup_mock_st(mock_st: MagicMock) -> None:
    """Provide Streamlit context-manager columns for page rendering tests."""

    def make_cols(spec):
        count = len(spec) if isinstance(spec, (list, tuple)) else spec
        cols = []
        for _ in range(count):
            col = MagicMock()
            col.__enter__ = MagicMock(return_value=col)
            col.__exit__ = MagicMock(return_value=False)
            cols.append(col)
        return cols

    mock_st.columns.side_effect = make_cols
    mock_st.button.return_value = False


def _import_match_engine_page():
    """Import the page module with a minimal fake Streamlit package tree."""
    streamlit_module = ModuleType("streamlit")
    streamlit_module.markdown = MagicMock()

    components_module = ModuleType("streamlit.components")
    components_v1_module = ModuleType("streamlit.components.v1")
    components_v1_module.html = MagicMock()
    components_module.v1 = components_v1_module
    streamlit_module.components = components_module

    sys.modules.pop("src.ui.match_engine_page", None)
    sys.modules.pop("src.ui.html_base", None)

    with patch.dict(
        sys.modules,
        {
            "streamlit": streamlit_module,
            "streamlit.components": components_module,
            "streamlit.components.v1": components_v1_module,
        },
    ):
        return importlib.import_module("src.ui.match_engine_page")


def test_render_match_engine_page_shows_explicit_empty_state() -> None:
    """An empty pipeline should render intentional primary content, not a blank pane."""
    page = _import_match_engine_page()
    mock_st = MagicMock()
    _setup_mock_st(mock_st)

    with (
        patch.object(page, "st", mock_st),
        patch.object(page, "load_specialists", return_value=[]),
        patch.object(page, "load_pipeline_data", return_value=[]),
        patch.object(page, "load_poc_contacts", return_value=[]),
        patch.object(page, "get_top_specialists_for_event", return_value=[]),
        patch.object(page, "render_html_page") as mock_render_html,
    ):
        page.render_match_engine_page()

    body_html = mock_render_html.call_args.args[0]
    assert "No ranked specialists available yet" in body_html
    assert "Match Queue Empty" in body_html
    assert mock_render_html.call_args.kwargs["height"] == page._SPARSE_PAGE_HEIGHT


def test_render_match_engine_page_adds_summary_card_for_shortlists() -> None:
    """Sparse match data should still render a meaningful above-the-fold summary."""
    page = _import_match_engine_page()
    mock_st = MagicMock()
    _setup_mock_st(mock_st)

    shortlist = [
        {
            "name": "Alex Rivera",
            "title": "VP Insights",
            "company": "Acme Research",
            "match_score": 0.91,
            "initials": "AR",
        }
    ]

    with (
        patch.object(page, "st", mock_st),
        patch.object(page, "load_specialists", return_value=[]),
        patch.object(page, "load_pipeline_data", return_value=[
            {
                "event_name": "CPP Career Center — Career Fairs",
                "speaker_name": "Alex Rivera",
                "match_score": "0.91",
            }
        ]),
        patch.object(page, "load_poc_contacts", return_value=[]),
        patch.object(page, "get_top_specialists_for_event", return_value=shortlist),
        patch.object(page, "render_html_page") as mock_render_html,
    ):
        page.render_match_engine_page()

    body_html = mock_render_html.call_args.args[0]
    assert "Shortlist ready for review" in body_html
    assert "Ranked Specialists" in body_html
    assert mock_render_html.call_args.kwargs["height"] == page._DEFAULT_PAGE_HEIGHT
