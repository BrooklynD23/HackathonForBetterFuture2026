"""REST endpoints exposing static CRM data files."""

from typing import Any, Callable

from fastapi import APIRouter, HTTPException

from src.api.demo_db import (
    load_demo_cpp_events,
    load_demo_event_calendar,
    load_demo_pipeline,
    load_demo_specialists,
)
from src.ui.data_helpers import (
    load_cpp_events,
    load_event_calendar,
    load_pipeline_data,
    load_poc_contacts,
    load_specialists,
)

router = APIRouter()


def _server_error(exc: Exception) -> HTTPException:
    return HTTPException(status_code=500, detail=str(exc))


def _demo_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**row, "source": "demo"} for row in rows]


def _load_rows_with_fallback(
    loader: Callable[[], list[dict[str, Any]]],
    demo_loader: Callable[[], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    try:
        rows = loader()
        if rows:
            return rows
    except Exception:
        pass
    return _demo_rows(demo_loader())


@router.get("/specialists")
async def specialists() -> list[dict]:
    """Return the specialist roster consumed by the frontend."""
    return _load_rows_with_fallback(load_specialists, load_demo_specialists)


@router.get("/events")
async def events() -> list[dict]:
    """Return the CPP events dataset."""
    return _load_rows_with_fallback(load_cpp_events, load_demo_cpp_events)


@router.get("/pipeline")
async def pipeline() -> list[dict]:
    """Return pipeline sample rows for dashboard views."""
    return _load_rows_with_fallback(load_pipeline_data, load_demo_pipeline)


@router.get("/calendar")
async def calendar() -> list[dict]:
    """Return IA event calendar rows."""
    return _load_rows_with_fallback(load_event_calendar, load_demo_event_calendar)


@router.get("/contacts")
async def contacts() -> list[dict]:
    """Return point-of-contact records."""
    try:
        return load_poc_contacts()
    except Exception as exc:  # pragma: no cover - defensive API boundary
        raise _server_error(exc) from exc
