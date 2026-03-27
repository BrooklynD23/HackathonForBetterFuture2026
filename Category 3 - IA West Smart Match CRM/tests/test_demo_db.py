"""Tests for the Phase 14 demo SQLite fallback data."""

from __future__ import annotations

from pathlib import Path

from src.api.demo_db import (
    load_demo_calendar_assignments,
    load_demo_calendar_events,
    load_demo_cpp_events,
    load_demo_event_calendar,
    load_demo_feedback_stats,
    load_demo_pipeline,
    load_demo_qr_stats,
    load_demo_specialists,
)


def test_demo_db_file_exists() -> None:
    demo_db = Path(__file__).resolve().parent.parent / "data" / "demo.db"
    assert demo_db.exists()


def test_demo_db_loaders_return_non_empty_seed_data() -> None:
    assert len(load_demo_specialists()) >= 10
    assert len(load_demo_cpp_events()) >= 5
    assert len(load_demo_pipeline()) >= 40
    assert len(load_demo_event_calendar()) >= 5
    assert len(load_demo_calendar_events()) >= 5
    assert len(load_demo_calendar_assignments()) >= 3


def test_demo_feedback_stats_match_frontend_contract_shape() -> None:
    payload = load_demo_feedback_stats()

    assert payload["total_feedback"] == 8
    assert payload["current_weights"]
    assert payload["trend"]
    assert payload["weight_history"]
    assert payload["recommended_adjustments"]


def test_demo_qr_stats_match_frontend_contract_shape() -> None:
    payload = load_demo_qr_stats()

    assert payload["generated_count"] == 5
    assert payload["scan_count"] == 42
    assert payload["membership_interest_count"] == 12
    assert payload["referral_codes"]
