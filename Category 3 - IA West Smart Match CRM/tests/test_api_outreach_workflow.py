"""Integration tests for POST /api/outreach/workflow endpoint."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

# Known event and speaker from pipeline_sample_data.csv
KNOWN_EVENT = "AI for a Better Future Hackathon"
KNOWN_SPEAKER = "Dr. Yufan Lin"

_MOCK_EMAIL_RESULT = {
    "subject_line": "Test Subject",
    "greeting": "Dear Dr. Lin,",
    "body": "Body text.",
    "closing": "Best,",
    "full_email": "Dear Dr. Lin,\nBody text.\nBest,",
}


@pytest.fixture(autouse=True)
def patch_pipeline_update():
    """Patch update_pipeline_status to avoid writing to the real CSV in all tests."""
    with patch(
        "src.api.routers.outreach.update_pipeline_status", return_value=True
    ) as mock_update:
        yield mock_update


def test_workflow_returns_all_three_results() -> None:
    """POST /workflow returns 200 with email, ics_content, pipeline_updated, steps, dispatch_mode."""
    with patch(
        "src.api.routers.outreach.generate_outreach_email",
        return_value=_MOCK_EMAIL_RESULT,
    ):
        response = client.post(
            "/api/outreach/workflow",
            json={"speaker_name": KNOWN_SPEAKER, "event_name": KNOWN_EVENT},
        )

    assert response.status_code == 200
    payload = response.json()

    assert "email" in payload
    assert "email_data" in payload
    assert "ics_content" in payload
    assert "pipeline_updated" in payload
    assert "steps" in payload
    assert "dispatch_mode" in payload


def test_workflow_step_statuses() -> None:
    """Response steps dict has keys 'email', 'ics', 'pipeline', each with a 'status' field."""
    with patch(
        "src.api.routers.outreach.generate_outreach_email",
        return_value=_MOCK_EMAIL_RESULT,
    ):
        response = client.post(
            "/api/outreach/workflow",
            json={"speaker_name": KNOWN_SPEAKER, "event_name": KNOWN_EVENT},
        )

    assert response.status_code == 200
    steps = response.json()["steps"]

    assert "email" in steps
    assert "ics" in steps
    assert "pipeline" in steps

    assert "status" in steps["email"]
    assert "status" in steps["ics"]
    assert "status" in steps["pipeline"]

    assert steps["email"]["status"] == "ok"
    assert steps["ics"]["status"] == "ok"
    assert steps["pipeline"]["status"] == "ok"


def test_workflow_partial_failure() -> None:
    """When email generation raises, ics and pipeline still succeed; steps.email.status == 'error'."""
    with patch(
        "src.api.routers.outreach.generate_outreach_email",
        side_effect=RuntimeError("API down"),
    ):
        response = client.post(
            "/api/outreach/workflow",
            json={"speaker_name": KNOWN_SPEAKER, "event_name": KNOWN_EVENT},
        )

    assert response.status_code == 200
    payload = response.json()
    steps = payload["steps"]

    assert steps["email"]["status"] == "error"
    assert "API down" in steps["email"]["error"]

    assert steps["ics"]["status"] == "ok"
    assert payload["ics_content"]  # ICS was still generated

    assert steps["pipeline"]["status"] == "ok"
    assert payload["pipeline_updated"] is True


def test_workflow_404_unknown_speaker() -> None:
    """POST with non-existent speaker returns 404."""
    response = client.post(
        "/api/outreach/workflow",
        json={
            "speaker_name": "Nonexistent Person 12345",
            "event_name": KNOWN_EVENT,
        },
    )
    assert response.status_code == 404
