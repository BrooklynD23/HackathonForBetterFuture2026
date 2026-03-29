"""Tests for the FastAPI data router."""

from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from src.api.routers import data as data_router
from src.api.main import app

client = TestClient(app)


def test_get_specialists_returns_json_array() -> None:
    response = client.get("/api/data/specialists")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert "name" in payload[0]


def test_get_events_returns_json_array() -> None:
    response = client.get("/api/data/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_pipeline_returns_json_array() -> None:
    response = client.get("/api/data/pipeline")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_calendar_returns_json_array() -> None:
    response = client.get("/api/data/calendar")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_contacts_returns_json_array() -> None:
    response = client.get("/api/data/contacts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_cors_allows_localhost_5173() -> None:
    response = client.options(
        "/api/data/specialists",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_specialists_fall_back_to_demo_db_when_live_rows_are_empty(monkeypatch) -> None:
    monkeypatch.setattr(data_router, "load_specialists", lambda: [])
    monkeypatch.setattr(
        data_router,
        "load_demo_specialists",
        lambda: [
            {
                "name": "Demo Speaker",
                "board_role": "President",
                "metro_region": "Los Angeles - West",
                "company": "Demo Co",
                "title": "VP Data Science",
                "expertise_tags": "AI, analytics",
                "initials": "DS",
            }
        ],
    )

    payload = asyncio.run(data_router.specialists())

    assert payload[0]["name"] == "Demo Speaker"
    assert payload[0]["source"] == "demo"


def test_pipeline_falls_back_to_demo_db_when_live_loader_errors(monkeypatch) -> None:
    def _boom():
        raise RuntimeError("pipeline missing")

    monkeypatch.setattr(data_router, "load_pipeline_data", _boom)
    monkeypatch.setattr(
        data_router,
        "load_demo_pipeline",
        lambda: [
            {
                "event_name": "Demo Event",
                "speaker_name": "Demo Speaker",
                "match_score": "0.91",
                "rank": "1",
                "stage": "Matched",
                "stage_order": "0",
            }
        ],
    )

    payload = asyncio.run(data_router.pipeline())

    assert payload[0]["event_name"] == "Demo Event"
    assert payload[0]["source"] == "demo"
