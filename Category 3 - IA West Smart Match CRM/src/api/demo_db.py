"""Helpers for loading demo fallback data from the seeded SQLite database."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

_DEMO_DB_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "demo.db"
)


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(str(_DEMO_DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def _decode_json_fields(
    record: dict[str, Any],
    *,
    fields: tuple[str, ...] = (),
) -> dict[str, Any]:
    decoded = dict(record)
    for field in fields:
        value = decoded.get(field)
        if not isinstance(value, str) or not value:
            continue
        try:
            decoded[field] = json.loads(value)
        except json.JSONDecodeError:
            continue
    return decoded


def _load_rows(
    query: str,
    *,
    json_fields: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(query).fetchall()
    return [_decode_json_fields(dict(row), fields=json_fields) for row in rows]


def _load_json_payload(query: str) -> dict[str, Any]:
    with _connect() as connection:
        row = connection.execute(query).fetchone()
    if row is None:
        return {}
    payload = dict(row).get("payload_json")
    if not isinstance(payload, str) or not payload:
        return {}
    return json.loads(payload)


def load_demo_specialists() -> list[dict[str, Any]]:
    return _load_rows("SELECT * FROM specialists ORDER BY name")


def load_demo_cpp_events() -> list[dict[str, Any]]:
    return _load_rows('SELECT * FROM cpp_events ORDER BY "Event / Program"')


def load_demo_pipeline() -> list[dict[str, Any]]:
    return _load_rows(
        "SELECT * FROM pipeline ORDER BY CAST(stage_order AS INTEGER), CAST(rank AS INTEGER), speaker_name"
    )


def load_demo_event_calendar() -> list[dict[str, Any]]:
    return _load_rows('SELECT * FROM event_calendar ORDER BY "IA Event Date"')


def load_demo_calendar_events() -> list[dict[str, Any]]:
    return _load_rows(
        "SELECT * FROM calendar_events ORDER BY event_date, event_name",
        json_fields=("nearby_universities", "assigned_volunteers"),
    )


def load_demo_calendar_assignments() -> list[dict[str, Any]]:
    return _load_rows(
        "SELECT * FROM calendar_assignments ORDER BY event_date, event_name, rank"
    )


def load_demo_qr_stats() -> dict[str, Any]:
    return _load_json_payload(
        "SELECT payload_json FROM qr_stats ORDER BY id DESC LIMIT 1"
    )


def load_demo_feedback_stats() -> dict[str, Any]:
    return _load_json_payload(
        "SELECT payload_json FROM feedback_stats ORDER BY id DESC LIMIT 1"
    )

