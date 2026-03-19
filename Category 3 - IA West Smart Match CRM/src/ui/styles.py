"""
Custom CSS for IA SmartMatch.
Inject at the top of the main app file via st.markdown(..., unsafe_allow_html=True).
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

import streamlit as st

# ── IA West Brand Colors ────────────────────────────────────────────
BRAND_NAVY: str = "#1E3A5F"
BRAND_GOLD: str = "#F59E0B"
BRAND_BLUE: str = "#2563EB"

# ── Custom CSS ──────────────────────────────────────────────────────
CUSTOM_CSS: str = """
<style>
/* ---------- IA West Brand Colors ---------- */
:root {
    --ia-primary:    #1E3A5F;   /* Dark navy */
    --ia-secondary:  #2563EB;   /* Bright blue */
    --ia-accent:     #F59E0B;   /* Amber accent */
    --ia-success:    #059669;   /* Green */
    --ia-danger:     #DC2626;   /* Red */
    --ia-gray-100:   #F3F4F6;
    --ia-gray-200:   #E5E7EB;
    --ia-gray-500:   #6B7280;
    --ia-gray-700:   #374151;
    --ia-gray-900:   #111827;
}

/* ---------- Match Card Styling ---------- */
div[data-testid="stExpander"] {
    border: 1px solid var(--ia-gray-200);
    border-radius: 8px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

div[data-testid="stExpander"] summary {
    font-weight: 600;
    color: var(--ia-primary);
}

/* ---------- Metric Card Enhancement ---------- */
div[data-testid="stMetric"] {
    background-color: var(--ia-gray-100);
    border-radius: 8px;
    padding: 12px 16px;
    border-left: 4px solid var(--ia-secondary);
}

div[data-testid="stMetric"] label {
    color: var(--ia-gray-500);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--ia-primary);
    font-size: 1.5rem;
    font-weight: 700;
}

/* ---------- Sidebar Branding ---------- */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
    border-right: 2px solid var(--ia-secondary);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--ia-primary);
}

/* ---------- Tab Styling ---------- */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: var(--ia-gray-500);
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--ia-secondary);
    border-bottom: 3px solid var(--ia-secondary);
}

/* ---------- Button Styling ---------- */
button[kind="primary"] {
    background-color: var(--ia-secondary);
    border-color: var(--ia-secondary);
}

button[kind="primary"]:hover {
    background-color: var(--ia-primary);
    border-color: var(--ia-primary);
}

/* ---------- Email Preview Card ---------- */
.email-preview {
    background-color: #FFFBEB;
    border: 1px solid var(--ia-accent);
    border-radius: 8px;
    padding: 16px;
    font-family: Georgia, serif;
    line-height: 1.6;
}

.email-preview .subject-line {
    font-weight: 700;
    color: var(--ia-primary);
    font-size: 1.1rem;
    margin-bottom: 8px;
    border-bottom: 1px solid var(--ia-gray-200);
    padding-bottom: 8px;
}

/* ---------- Score Badge ---------- */
.score-badge {
    display: inline-block;
    background-color: var(--ia-secondary);
    color: white;
    font-size: 1.8rem;
    font-weight: 800;
    padding: 8px 16px;
    border-radius: 12px;
    text-align: center;
    min-width: 80px;
}

.score-badge.high   { background-color: var(--ia-success); }
.score-badge.medium { background-color: var(--ia-accent);  }
.score-badge.low    { background-color: var(--ia-danger);  }

/* ---------- Explanation Card ---------- */
.explanation-card {
    background-color: var(--ia-gray-100);
    border-left: 4px solid var(--ia-secondary);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-style: italic;
    color: var(--ia-gray-700);
    line-height: 1.5;
}

/* ---------- Loading State ---------- */
.stSpinner {
    color: var(--ia-secondary);
}

/* ---------- Mobile Responsive ---------- */
@media (max-width: 768px) {
    div[data-testid="stMetric"] {
        padding: 8px 12px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.2rem;
    }
    .score-badge {
        font-size: 1.4rem;
        padding: 6px 12px;
    }
}
</style>
"""


def inject_custom_css() -> None:
    """Inject the CUSTOM_CSS into the Streamlit app via st.markdown."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@contextmanager
def api_call_spinner(message: str = "Processing...") -> Generator[None, None, None]:
    """
    Wrap any API call (Gemini, scraping) with a branded spinner.

    Usage:
        with api_call_spinner("Generating match explanation..."):
            result = generate_text(...)
    """
    with st.spinner(message):
        try:
            yield
        except Exception as e:
            st.error(
                f"An error occurred: {str(e)[:200]}. "
                "Please try again or switch to Demo Mode."
            )
            raise


def render_error_card(title: str, message: str, suggestion: str = "") -> None:
    """Display a styled error card with optional recovery suggestion."""
    st.error(f"**{title}**")
    st.markdown(f"> {message}")
    if suggestion:
        st.info(f"Suggestion: {suggestion}")
