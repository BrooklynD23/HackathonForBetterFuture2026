"""Vercel serverless function entry point for the IA West SmartMatch FastAPI backend.

Vercel's Python runtime invokes `handler` for all requests routed to this file.
`mangum` bridges the ASGI interface (FastAPI) to the Lambda-style invocation
that Vercel's Python runtime uses internally.
"""
from __future__ import annotations

import os
import sys

# ---------------------------------------------------------------------------
# Path bootstrap — make 'src.*' importable from the category subdirectory.
# On Vercel, __file__ is /var/task/api/index.py, so repo root is one level up.
# ---------------------------------------------------------------------------
_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_category_dir = os.path.join(_repo_root, "Category 3 - IA West Smart Match CRM")
if _category_dir not in sys.path:
    sys.path.insert(0, _category_dir)

# ---------------------------------------------------------------------------
# Import the FastAPI app and wrap with mangum for Vercel's runtime.
# ---------------------------------------------------------------------------
from mangum import Mangum  # noqa: E402
from src.api.main import app  # noqa: E402

handler = Mangum(app, lifespan="off")
