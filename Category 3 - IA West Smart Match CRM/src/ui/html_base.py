"""
HTML base wrapper for IA SmartMatch UI pages.

Wraps an HTML body string into a complete standalone document with
Tailwind CDN, Google Fonts, Material Symbols, and the Academic Curator
Tailwind config, then renders via st.components.v1.html().
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from src.ui.design_system import (
    FONT_LINKS,
    HIDE_STREAMLIT_CHROME,
    SHARED_CSS,
    TAILWIND_CDN,
    TAILWIND_CONFIG,
)


def wrap_html(
    body: str,
    *,
    title: str = "IA SmartMatch",
    height: int = 2000,
    hide_chrome: bool = False,
) -> None:
    """
    Construct a full HTML document from a body string and render it.

    Assembles: DOCTYPE + head (fonts, Tailwind CDN, Tailwind config,
    shared CSS) + body, then calls st.components.v1.html().

    Args:
        body: Inner HTML content for the <body> element.
        title: Page title for the <title> tag.
        height: Pixel height passed to st.components.v1.html().
        hide_chrome: If True, also injects HIDE_STREAMLIT_CHROME via
            st.markdown() before rendering the component.
    """
    if hide_chrome:
        st.markdown(HIDE_STREAMLIT_CHROME, unsafe_allow_html=True)

    html_string: str = (
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        f"<meta charset='utf-8'/>"
        f"<meta name='viewport' content='width=device-width, initial-scale=1.0'/>"
        f"<title>{title}</title>"
        f"{FONT_LINKS}"
        f"{TAILWIND_CDN}"
        f"{TAILWIND_CONFIG}"
        f"{SHARED_CSS}"
        "</head>"
        '<body class="bg-surface font-body text-on-surface antialiased">'
        f"{body}"
        "</body>"
        "</html>"
    )

    components.html(html_string, height=height, scrolling=True)


def render_html_page(
    body: str,
    *,
    title: str = "IA SmartMatch",
    height: int = 4000,
    hide_chrome: bool = False,
) -> None:
    """
    Alias for wrap_html with a larger default height suited to full pages.

    Args:
        body: Inner HTML content for the <body> element.
        title: Page title for the <title> tag.
        height: Pixel height passed to st.components.v1.html(). Defaults to 4000.
        hide_chrome: If True, also injects HIDE_STREAMLIT_CHROME before rendering.
    """
    wrap_html(body, title=title, height=height, hide_chrome=hide_chrome)
