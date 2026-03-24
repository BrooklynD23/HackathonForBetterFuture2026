"""
Shared design system for IA SmartMatch — Academic Curator Design System.

Exports Tailwind config, shared CSS, font links, and color constants used
by all Phase 8 UI pages rendered via st.components.v1.html().
"""

from __future__ import annotations

# ── Font Links ────────────────────────────────────────────────────────────────
FONT_LINKS: str = (
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600'
    "&family=Inter+Tight:wght@600;700;800&display=swap"
    '" rel="stylesheet"/>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined'
    ':wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>'
)

# ── Tailwind CDN ──────────────────────────────────────────────────────────────
TAILWIND_CDN: str = (
    '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>'
)

# ── Tailwind Config ───────────────────────────────────────────────────────────
# Exact config from the Academic Curator landing page mockup (lines 10-73 of code.html).
TAILWIND_CONFIG: str = """<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "secondary-container": "#d5e0f7",
              "on-tertiary-fixed-variant": "#693c00",
              "on-primary": "#ffffff",
              "on-secondary": "#ffffff",
              "on-error-container": "#93000a",
              "secondary-fixed": "#d8e3fa",
              "error": "#ba1a1a",
              "outline-variant": "#c1c7d2",
              "on-secondary-fixed": "#111c2c",
              "on-surface": "#191c1e",
              "inverse-primary": "#a2c9ff",
              "surface-dim": "#d8dadd",
              "surface-container-low": "#f2f4f7",
              "on-background": "#191c1e",
              "primary-container": "#2b6cb0",
              "on-secondary-container": "#586377",
              "inverse-on-surface": "#eff1f4",
              "on-secondary-fixed-variant": "#3c475a",
              "background": "#f7f9fc",
              "on-primary-container": "#e1ecff",
              "primary-fixed": "#d3e4ff",
              "tertiary-container": "#9a5b00",
              "tertiary-fixed-dim": "#ffb86e",
              "on-error": "#ffffff",
              "secondary-fixed-dim": "#bcc7dd",
              "tertiary-fixed": "#ffdcbd",
              "secondary": "#545f72",
              "on-primary-fixed-variant": "#004881",
              "surface-container-highest": "#e0e3e6",
              "surface-bright": "#f7f9fc",
              "surface-tint": "#1960a3",
              "on-primary-fixed": "#001c38",
              "on-tertiary": "#ffffff",
              "inverse-surface": "#2d3133",
              "surface-container-lowest": "#ffffff",
              "on-tertiary-container": "#ffe7d2",
              "error-container": "#ffdad6",
              "on-tertiary-fixed": "#2c1600",
              "primary": "#005394",
              "surface-container-high": "#e6e8eb",
              "surface-container": "#eceef1",
              "on-surface-variant": "#414750",
              "tertiary": "#784600",
              "outline": "#727782",
              "surface": "#f7f9fc",
              "primary-fixed-dim": "#a2c9ff",
              "surface-variant": "#e0e3e6"
            },
            fontFamily: {
              "headline": ["Inter Tight"],
              "body": ["Inter"],
              "label": ["Inter"]
            },
            borderRadius: {"DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "2xl": "1.5rem", "full": "9999px"},
          },
        },
      }
    </script>"""

# ── Shared CSS ────────────────────────────────────────────────────────────────
SHARED_CSS: str = """<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .hero-gradient {
            background: linear-gradient(135deg, #005394 0%, #2b6cb0 100%);
        }
        .glass-panel {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(24px);
        }
        .bg-primary-gradient {
            background: linear-gradient(135deg, #005394 0%, #2b6cb0 100%);
        }
    </style>"""

# ── Hide Streamlit Chrome ─────────────────────────────────────────────────────
HIDE_STREAMLIT_CHROME: str = """<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
div[data-testid="stSidebarCollapsedControl"] {display: none;}
.stDeployButton {display: none;}
</style>"""

# ── Color Constants ───────────────────────────────────────────────────────────
PRIMARY: str = "#005394"
PRIMARY_CONTAINER: str = "#2b6cb0"
ON_PRIMARY: str = "#ffffff"
ON_SURFACE: str = "#191c1e"
ON_SURFACE_VARIANT: str = "#414750"
SURFACE: str = "#f7f9fc"
SURFACE_CONTAINER_LOW: str = "#f2f4f7"
SURFACE_CONTAINER: str = "#eceef1"
SURFACE_CONTAINER_LOWEST: str = "#ffffff"
