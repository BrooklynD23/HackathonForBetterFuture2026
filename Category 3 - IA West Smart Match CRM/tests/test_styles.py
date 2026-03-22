"""Tests for src/ui/styles.py – IA West brand CSS, spinners, error cards."""

import pytest


class TestBrandColors:
    """Brand color constants are defined and correct."""

    def test_brand_colors_constants_defined(self) -> None:
        from src.ui.styles import BRAND_PRIMARY, BRAND_PRIMARY_CONTAINER, BRAND_ON_PRIMARY

        assert BRAND_PRIMARY == "#005394"
        assert BRAND_PRIMARY_CONTAINER == "#2b6cb0"
        assert BRAND_ON_PRIMARY == "#ffffff"


class TestCustomCSS:
    """CUSTOM_CSS string is valid and contains brand tokens."""

    def test_custom_css_is_valid_css_string(self) -> None:
        from src.ui.styles import CUSTOM_CSS

        assert isinstance(CUSTOM_CSS, str)
        assert "<style>" in CUSTOM_CSS
        assert "</style>" in CUSTOM_CSS

    def test_custom_css_contains_academic_curator_colors(self) -> None:
        from src.ui.styles import CUSTOM_CSS

        assert "#005394" in CUSTOM_CSS  # primary (IA West blue)
        assert "#2b6cb0" in CUSTOM_CSS  # primary-container
        assert "#191c1e" in CUSTOM_CSS  # on-surface (not pure black)

    def test_custom_css_contains_root_variables(self) -> None:
        from src.ui.styles import CUSTOM_CSS

        assert "--primary" in CUSTOM_CSS
        assert "--on-surface" in CUSTOM_CSS
        assert "--surface" in CUSTOM_CSS


class TestInjectCustomCSS:
    """inject_custom_css() is callable and invokes st.markdown."""

    def test_inject_custom_css_callable(self) -> None:
        from src.ui.styles import inject_custom_css

        assert callable(inject_custom_css)

    def test_inject_custom_css_calls_st_markdown(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.ui.styles as styles_mod

        calls: list[tuple] = []

        def fake_markdown(html: str, unsafe_allow_html: bool = False) -> None:
            calls.append((html, unsafe_allow_html))

        import types
        fake_st = types.ModuleType("streamlit")
        fake_st.markdown = fake_markdown  # type: ignore[attr-defined]
        monkeypatch.setattr(styles_mod, "st", fake_st)

        styles_mod.inject_custom_css()
        assert len(calls) == 1
        assert calls[0][1] is True  # unsafe_allow_html=True


class TestApiCallSpinner:
    """api_call_spinner is a context manager wrapping st.spinner."""

    def test_api_call_spinner_is_context_manager(self) -> None:
        from src.ui.styles import api_call_spinner
        import contextlib

        assert callable(api_call_spinner)
        # Should return a context manager
        cm = api_call_spinner("test")
        assert hasattr(cm, "__enter__") and hasattr(cm, "__exit__")

    def test_api_call_spinner_yields(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.ui.styles as styles_mod
        import types
        from contextlib import contextmanager

        fake_st = types.ModuleType("streamlit")

        @contextmanager
        def fake_spinner(msg: str):
            yield

        fake_st.spinner = fake_spinner  # type: ignore[attr-defined]
        fake_st.error = lambda msg: None  # type: ignore[attr-defined]
        monkeypatch.setattr(styles_mod, "st", fake_st)

        with styles_mod.api_call_spinner("Loading...") as ctx:
            # Should enter without error
            pass


class TestRenderErrorCard:
    """render_error_card() displays styled error information."""

    def test_render_error_card_callable(self) -> None:
        from src.ui.styles import render_error_card

        assert callable(render_error_card)

    def test_render_error_card_includes_title(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.ui.styles as styles_mod
        import types

        error_calls: list[str] = []
        markdown_calls: list[str] = []
        info_calls: list[str] = []

        fake_st = types.ModuleType("streamlit")
        fake_st.error = lambda msg: error_calls.append(msg)  # type: ignore[attr-defined]
        fake_st.markdown = lambda msg, **kw: markdown_calls.append(msg)  # type: ignore[attr-defined]
        fake_st.info = lambda msg: info_calls.append(msg)  # type: ignore[attr-defined]
        monkeypatch.setattr(styles_mod, "st", fake_st)

        styles_mod.render_error_card("API Error", "Connection timed out", "Try demo mode")

        assert any("API Error" in c for c in error_calls)
        assert any("Connection timed out" in c for c in markdown_calls)
        assert any("demo mode" in c for c in info_calls)

    def test_render_error_card_no_suggestion(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.ui.styles as styles_mod
        import types

        info_calls: list[str] = []

        fake_st = types.ModuleType("streamlit")
        fake_st.error = lambda msg: None  # type: ignore[attr-defined]
        fake_st.markdown = lambda msg, **kw: None  # type: ignore[attr-defined]
        fake_st.info = lambda msg: info_calls.append(msg)  # type: ignore[attr-defined]
        monkeypatch.setattr(styles_mod, "st", fake_st)

        styles_mod.render_error_card("Error", "Something broke")

        assert len(info_calls) == 0


class TestStreamlitConfigToml:
    """Streamlit config.toml exists with theme section."""

    def test_streamlit_config_toml_exists(self) -> None:
        from pathlib import Path

        config_path = Path(__file__).resolve().parent.parent / ".streamlit" / "config.toml"
        assert config_path.exists(), f"Expected {config_path} to exist"

    def test_streamlit_config_toml_has_theme(self) -> None:
        from pathlib import Path

        config_path = Path(__file__).resolve().parent.parent / ".streamlit" / "config.toml"
        content = config_path.read_text()
        assert "[theme]" in content
        assert 'primaryColor = "#005394"' in content
