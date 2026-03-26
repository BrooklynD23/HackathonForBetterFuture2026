"""Unit tests for pipeline_updater.py — CSV write and LRU cache invalidation."""

from __future__ import annotations

import csv
import importlib
from pathlib import Path

import pytest


CSV_FIELDNAMES = ["event_name", "speaker_name", "match_score", "rank", "stage", "stage_order"]

SAMPLE_ROWS = [
    {
        "event_name": "AI for a Better Future Hackathon",
        "speaker_name": "Dr. Yufan Lin",
        "match_score": "0.4608",
        "rank": "1",
        "stage": "Matched",
        "stage_order": "0",
    },
    {
        "event_name": "AI for a Better Future Hackathon",
        "speaker_name": "Amber Jawaid",
        "match_score": "0.4408",
        "rank": "2",
        "stage": "Contacted",
        "stage_order": "1",
    },
]


def _write_sample_csv(csv_path: Path, rows: list[dict]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


@pytest.fixture()
def pipeline_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temp pipeline CSV and redirect pipeline_updater to use it."""
    csv_path = tmp_path / "pipeline_sample_data.csv"
    _write_sample_csv(csv_path, SAMPLE_ROWS)

    # Patch _data_dir in data_helpers so any reload picks up the tmp path
    import src.ui.data_helpers as dh

    monkeypatch.setattr(dh, "_data_dir", lambda: tmp_path)

    # Clear the LRU cache so the patched _data_dir is used on next call
    dh._load_pipeline_data_cached.cache_clear()

    # Import (or reload) pipeline_updater AFTER patching so PIPELINE_CSV resolves
    # to the temp dir.  We re-import each time via importlib to pick up new path.
    import src.outreach.pipeline_updater as pu

    importlib.reload(pu)
    monkeypatch.setattr(pu, "PIPELINE_CSV", csv_path)

    yield csv_path

    # Cleanup: clear cache after test
    dh._load_pipeline_data_cached.cache_clear()


def test_update_stage_matched_to_contacted(pipeline_csv: Path) -> None:
    """update_pipeline_status transitions stage from Matched to Contacted and returns True."""
    import src.outreach.pipeline_updater as pu

    result = pu.update_pipeline_status(
        "AI for a Better Future Hackathon", "Dr. Yufan Lin", "Contacted"
    )

    assert result is True

    # Read back the CSV and verify the row was updated
    with pipeline_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    updated_row = next(
        (r for r in rows if r["speaker_name"] == "Dr. Yufan Lin"
         and r["event_name"] == "AI for a Better Future Hackathon"),
        None,
    )
    assert updated_row is not None
    assert updated_row["stage"] == "Contacted"
    assert updated_row["stage_order"] == "1"


def test_upsert_new_speaker(pipeline_csv: Path) -> None:
    """update_pipeline_status appends new row when speaker not found, returns False."""
    import src.outreach.pipeline_updater as pu

    result = pu.update_pipeline_status("New Event", "New Speaker", "Contacted")

    assert result is False

    with pipeline_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    new_row = next(
        (r for r in rows if r["speaker_name"] == "New Speaker" and r["event_name"] == "New Event"),
        None,
    )
    assert new_row is not None
    assert new_row["stage"] == "Contacted"
    assert new_row["stage_order"] == "1"


def test_cache_cleared_after_write(pipeline_csv: Path) -> None:
    """After update_pipeline_status, the LRU cache is cleared (currsize == 0)."""
    import src.outreach.pipeline_updater as pu
    from src.ui.data_helpers import _load_pipeline_data_cached

    # Warm the cache first
    _ = _load_pipeline_data_cached()
    assert _load_pipeline_data_cached.cache_info().currsize == 1

    pu.update_pipeline_status(
        "AI for a Better Future Hackathon", "Dr. Yufan Lin", "Contacted"
    )

    assert _load_pipeline_data_cached.cache_info().currsize == 0


def test_idempotent_update(pipeline_csv: Path) -> None:
    """Calling update_pipeline_status twice for the same speaker produces exactly one row."""
    import src.outreach.pipeline_updater as pu

    pu.update_pipeline_status(
        "AI for a Better Future Hackathon", "Dr. Yufan Lin", "Contacted"
    )
    pu.update_pipeline_status(
        "AI for a Better Future Hackathon", "Dr. Yufan Lin", "Contacted"
    )

    with pipeline_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    matching = [
        r for r in rows
        if r["speaker_name"] == "Dr. Yufan Lin"
        and r["event_name"] == "AI for a Better Future Hackathon"
    ]
    assert len(matching) == 1
