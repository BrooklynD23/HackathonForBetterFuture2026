"""Tests for the FastAPI matching and outreach routers."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_rank_endpoint_returns_normalized_matches() -> None:
    response = client.post(
        "/api/matching/rank",
        json={"event_name": "AI for a Better Future Hackathon", "limit": 3},
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    first = payload[0]
    assert "name" in first
    assert "score" in first
    assert "rank" in first
    assert "factor_scores" in first


def test_rank_endpoint_requires_event_name() -> None:
    response = client.post("/api/matching/rank", json={"limit": 3})
    assert response.status_code == 422


def test_ics_endpoint_returns_calendar_text() -> None:
    response = client.post(
        "/api/outreach/ics",
        json={
            "event_name": "Test Event",
            "event_date": "2026-04-15",
            "location": "CPP",
            "description": "Career event",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "ics_content" in payload
    assert "BEGIN:VCALENDAR" in payload["ics_content"]


def test_email_endpoint_returns_generated_email_text() -> None:
    ranking_response = client.post(
        "/api/matching/rank",
        json={"event_name": "AI for a Better Future Hackathon", "limit": 1},
    )
    assert ranking_response.status_code == 200
    top_match = ranking_response.json()[0]

    response = client.post(
        "/api/outreach/email",
        json={
            "speaker_name": top_match["name"],
            "event_name": "AI for a Better Future Hackathon",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "email" in payload
    assert isinstance(payload["email"], str)
    assert payload["email"]
