#!/usr/bin/env python3
import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def table_count(connection, table):
    try:
        return connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
    except sqlite3.OperationalError:
        return 0


def read_devices(connection):
    try:
        return connection.execute(
            """
            SELECT
                h.device_id,
                h.state,
                h.previous_state,
                h.age_seconds,
                h.last_received_at,
                h.last_telemetry_at,
                h.last_status_at,
                h.last_sequence,
                h.mqtt_connected,
                h.warning_after_s,
                h.critical_after_s,
                h.offline_after_s,
                h.checked_at,
                h.changed_at
            FROM device_health h
            ORDER BY
                CASE h.state
                    WHEN 'offline' THEN 0
                    WHEN 'critical' THEN 1
                    WHEN 'warning' THEN 2
                    ELSE 3
                END,
                h.age_seconds DESC
            """
        ).fetchall()
    except sqlite3.OperationalError:
        return []


def read_recent_events(connection):
    return connection.execute(
        """
        SELECT event_type, received_at, device_id, payload_json
        FROM edge_events
        WHERE event_type LIKE 'sensor_%'
        ORDER BY id DESC
        LIMIT 12
        """
    ).fetchall()


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def decode_event(row):
    event = row_to_dict(row)
    try:
        event["payload"] = json.loads(event.pop("payload_json"))
    except json.JSONDecodeError:
        event["payload"] = {"raw": event.pop("payload_json")}
    return event


def build_payload(connection):
    counts = {
        "mqtt_messages": table_count(connection, "mqtt_messages"),
        "telemetry_readings": table_count(connection, "telemetry_readings"),
        "recovery_summaries": table_count(connection, "recovery_summaries"),
        "reconstructed_readings": table_count(connection, "reconstructed_readings"),
        "edge_events": table_count(connection, "edge_events"),
        "device_liveness": table_count(connection, "device_liveness"),
        "device_health": table_count(connection, "device_health"),
    }
    devices = []
    for row in read_devices(connection):
        device = row_to_dict(row)
        if device["mqtt_connected"] is not None:
            device["mqtt_connected"] = bool(device["mqtt_connected"])
        devices.append(device)

    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "source": "edge_sqlite",
        "counts": counts,
        "devices": devices,
        "recent_events": [decode_event(row) for row in read_recent_events(connection)],
    }


def main():
    parser = argparse.ArgumentParser(description="Export edge device health from SQLite to JSON for the web UI.")
    parser.add_argument("--db", default="var/edge/greenhouse.db", help="SQLite database path.")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"database not found: {db_path}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    try:
        payload = build_payload(connection)
    finally:
        connection.close()

    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp_path.replace(out_path)
    print(f"exported {len(payload['devices'])} devices to {out_path}")


if __name__ == "__main__":
    main()
