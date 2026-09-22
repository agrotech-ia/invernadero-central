#!/usr/bin/env python3
import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from edge.ingestor.storage import SqliteStorage


STATE_ORDER = ["online", "warning", "critical", "offline"]


def parse_utc(value):
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def utc_now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.isoformat()


def classify(age_seconds, warning_after_s, critical_after_s, offline_after_s):
    if age_seconds >= offline_after_s:
        return "offline"
    if age_seconds >= critical_after_s:
        return "critical"
    if age_seconds >= warning_after_s:
        return "warning"
    return "online"


def event_type_for_transition(previous_state, current_state):
    if previous_state and previous_state != "online" and current_state == "online":
        return "sensor_recovered"
    return f"sensor_{current_state}"


def upsert_health(connection, row, state, age_seconds, checked_at, thresholds):
    existing = connection.execute(
        "SELECT state, changed_at FROM device_health WHERE device_id = ?",
        (row["device_id"],),
    ).fetchone()
    previous_state = existing["state"] if existing else None
    changed_at = checked_at
    if existing and previous_state == state:
        changed_at = parse_utc(existing["changed_at"]) or checked_at

    connection.execute(
        """
        INSERT INTO device_health (
            device_id, state, previous_state, last_received_at, last_telemetry_at,
            last_status_at, last_sequence, mqtt_connected, age_seconds,
            warning_after_s, critical_after_s, offline_after_s, checked_at, changed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(device_id) DO UPDATE SET
            state = excluded.state,
            previous_state = excluded.previous_state,
            last_received_at = excluded.last_received_at,
            last_telemetry_at = excluded.last_telemetry_at,
            last_status_at = excluded.last_status_at,
            last_sequence = excluded.last_sequence,
            mqtt_connected = excluded.mqtt_connected,
            age_seconds = excluded.age_seconds,
            warning_after_s = excluded.warning_after_s,
            critical_after_s = excluded.critical_after_s,
            offline_after_s = excluded.offline_after_s,
            checked_at = excluded.checked_at,
            changed_at = excluded.changed_at
        """,
        (
            row["device_id"],
            state,
            previous_state,
            row["last_received_at"],
            row["last_telemetry_at"],
            row["last_status_at"],
            row["last_sequence"],
            row["mqtt_connected"],
            age_seconds,
            thresholds["warning_after_s"],
            thresholds["critical_after_s"],
            thresholds["offline_after_s"],
            iso(checked_at),
            iso(changed_at),
        ),
    )

    if previous_state != state:
        write_transition_event(connection, row, previous_state, state, age_seconds, checked_at, thresholds)


def write_transition_event(connection, row, previous_state, state, age_seconds, checked_at, thresholds):
    payload = {
        "event_type": event_type_for_transition(previous_state, state),
        "device_id": row["device_id"],
        "previous_state": previous_state,
        "state": state,
        "age_seconds": age_seconds,
        "last_received_at": row["last_received_at"],
        "last_telemetry_at": row["last_telemetry_at"],
        "last_status_at": row["last_status_at"],
        "last_sequence": row["last_sequence"],
        "mqtt_connected": None if row["mqtt_connected"] is None else bool(row["mqtt_connected"]),
        **thresholds,
    }
    connection.execute(
        """
        INSERT INTO edge_events (event_type, received_at, device_id, topic, payload_json)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload["event_type"],
            iso(checked_at),
            row["device_id"],
            "edge/liveness",
            json.dumps(payload, separators=(",", ":"), sort_keys=True),
        ),
    )


def print_health(rows):
    if not rows:
        print("no devices")
        return
    for row in rows:
        values = dict(row)
        mqtt_connected = "unknown" if row["mqtt_connected"] is None else bool(row["mqtt_connected"])
        values["mqtt_connected_label"] = mqtt_connected
        print(
            "{device_id} {state} age={age_seconds}s last_received={last_received_at} "
            "last_sequence={last_sequence} mqtt_connected={mqtt_connected_label}".format(**values)
        )


def run_check(db_path, thresholds):
    storage = SqliteStorage(db_path)
    storage.migrate()
    storage.close()

    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    now = utc_now()
    try:
        rows = connection.execute(
            """
            SELECT device_id, last_received_at, last_telemetry_at, last_status_at,
                   last_sequence, mqtt_connected
            FROM device_liveness
            ORDER BY device_id
            """
        ).fetchall()

        with connection:
            for row in rows:
                last_received = parse_utc(row["last_received_at"])
                age_seconds = int((now - last_received).total_seconds()) if last_received else thresholds["offline_after_s"]
                state = classify(age_seconds, **thresholds)
                upsert_health(connection, row, state, age_seconds, now, thresholds)

        health_rows = connection.execute(
            """
            SELECT device_id, state, age_seconds, last_received_at, last_sequence,
                   mqtt_connected, checked_at, changed_at
            FROM device_health
            ORDER BY
                CASE state
                    WHEN 'offline' THEN 0
                    WHEN 'critical' THEN 1
                    WHEN 'warning' THEN 2
                    ELSE 3
                END,
                age_seconds DESC
            """
        ).fetchall()
        print_health(health_rows)
        return max((STATE_ORDER.index(row["state"]) for row in health_rows), default=0)
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description="Check greenhouse device liveness from edge SQLite.")
    parser.add_argument("--db", default="var/edge/greenhouse.db", help="SQLite database path.")
    parser.add_argument("--warning-after-s", type=int, default=90)
    parser.add_argument("--critical-after-s", type=int, default=600)
    parser.add_argument("--offline-after-s", type=int, default=1800)
    parser.add_argument("--exit-nonzero", action="store_true", help="Exit nonzero for critical/offline devices.")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"database not found: {db_path}")

    thresholds = {
        "warning_after_s": args.warning_after_s,
        "critical_after_s": args.critical_after_s,
        "offline_after_s": args.offline_after_s,
    }
    worst_state_index = run_check(db_path, thresholds)
    if args.exit_nonzero and worst_state_index >= STATE_ORDER.index("critical"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
