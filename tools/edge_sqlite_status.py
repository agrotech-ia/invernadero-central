#!/usr/bin/env python3
import argparse
import sqlite3
from pathlib import Path


TABLES = [
    "mqtt_messages",
    "telemetry_readings",
    "recovery_summaries",
    "recovery_summary_readings",
    "reconstructed_readings",
    "edge_events",
    "device_liveness",
    "device_health",
]


def table_count(connection, table):
    try:
        return connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
    except sqlite3.OperationalError:
        return "missing"


def print_counts(connection):
    print("counts")
    for table in TABLES:
        print(f"  {table}: {table_count(connection, table)}")


def print_liveness(connection):
    rows = connection.execute(
        """
        SELECT device_id, last_received_at, last_telemetry_at, last_status_at,
               last_sequence, mqtt_connected
        FROM device_liveness
        ORDER BY last_received_at DESC
        LIMIT 10
        """
    ).fetchall()
    print("liveness")
    if not rows:
        print("  no devices")
        return
    for row in rows:
        values = dict(row)
        mqtt_connected = "unknown" if row["mqtt_connected"] is None else bool(row["mqtt_connected"])
        values["mqtt_connected_label"] = mqtt_connected
        print(
            "  device={device_id} last_received={last_received_at} "
            "last_telemetry={last_telemetry_at} last_status={last_status_at} "
            "last_sequence={last_sequence} mqtt_connected={mqtt_connected_label}".format(**values)
        )


def print_recent_recovery(connection):
    rows = connection.execute(
        """
        SELECT device_id, recovery_id, sequence_start, sequence_end, sample_count,
               quality, received_at
        FROM recovery_summaries
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()
    print("recent_recovery")
    if not rows:
        print("  no recovery summaries")
        return
    for row in rows:
        print(
            "  device={device_id} recovery={recovery_id} seq={sequence_start}-{sequence_end} "
            "samples={sample_count} quality={quality} received={received_at}".format(**dict(row))
        )


def print_recent_events(connection):
    rows = connection.execute(
        """
        SELECT event_type, received_at, device_id, payload_json
        FROM edge_events
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()
    print("recent_events")
    if not rows:
        print("  no events")
        return
    for row in rows:
        print(
            "  type={event_type} device={device_id} received={received_at} payload={payload_json}".format(
                **dict(row)
            )
        )


def print_device_health(connection):
    try:
        rows = connection.execute(
            """
            SELECT device_id, state, age_seconds, last_received_at, last_sequence,
                   mqtt_connected, checked_at, changed_at
            FROM device_health
            ORDER BY checked_at DESC
            LIMIT 10
            """
        ).fetchall()
    except sqlite3.OperationalError:
        print("device_health")
        print("  table missing; run tools/edge_liveness_check.py once")
        return

    print("device_health")
    if not rows:
        print("  no health checks")
        return
    for row in rows:
        values = dict(row)
        mqtt_connected = "unknown" if row["mqtt_connected"] is None else bool(row["mqtt_connected"])
        values["mqtt_connected_label"] = mqtt_connected
        print(
            "  device={device_id} state={state} age={age_seconds}s "
            "last_received={last_received_at} last_sequence={last_sequence} "
            "mqtt_connected={mqtt_connected_label} checked_at={checked_at}".format(**values)
        )


def main():
    parser = argparse.ArgumentParser(description="Show greenhouse edge SQLite ingestion status.")
    parser.add_argument("--db", default="var/edge/greenhouse.db", help="SQLite database path.")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"database not found: {db_path}")

    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    try:
        print_counts(connection)
        print_liveness(connection)
        print_device_health(connection)
        print_recent_recovery(connection)
        print_recent_events(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
