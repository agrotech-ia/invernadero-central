import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQLITE_MIGRATIONS = PROJECT_ROOT / "edge" / "storage" / "migrations" / "sqlite"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class Storage:
    def migrate(self):
        raise NotImplementedError

    def ingest_message(self, topic, payload, message_type, received_at):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class SqliteStorage(Storage):
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")

    def migrate(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version TEXT PRIMARY KEY,
                    applied_at TEXT NOT NULL
                )
                """
            )
            for migration_path in sorted(SQLITE_MIGRATIONS.glob("*.sql")):
                version = migration_path.stem
                applied = self.connection.execute(
                    "SELECT 1 FROM schema_migrations WHERE version = ?", (version,)
                ).fetchone()
                if applied:
                    continue
                self.connection.executescript(migration_path.read_text(encoding="utf-8"))
                self.connection.execute(
                    "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                    (version, utc_now()),
                )

    def ingest_message(self, topic, payload, message_type, received_at):
        with self.connection:
            message_id = self._insert_mqtt_message(topic, payload, message_type, received_at)
            self._update_liveness(message_id, topic, payload, message_type, received_at)

            if message_type == "telemetry":
                self._ingest_telemetry(message_id, payload, received_at)
                self._detect_sequence_gap(topic, payload, received_at)
            elif message_type == "telemetry_recovery":
                self._ingest_recovery(message_id, topic, payload, received_at)

        return message_id

    def _insert_mqtt_message(self, topic, payload, message_type, received_at):
        cursor = self.connection.execute(
            """
            INSERT INTO mqtt_messages (
                received_at, topic, payload_json, message_type, greenhouse_id, zone_id,
                device_id, device_time, sequence, replayed, recovery_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                received_at,
                topic,
                json.dumps(payload, separators=(",", ":"), sort_keys=True),
                message_type,
                payload.get("greenhouse_id"),
                payload.get("zone_id"),
                payload.get("device_id"),
                payload.get("device_time"),
                payload.get("sequence"),
                1 if payload.get("replayed") else 0,
                payload.get("recovery_id"),
            ),
        )
        return cursor.lastrowid

    def _update_liveness(self, message_id, topic, payload, message_type, received_at):
        device_id = payload.get("device_id")
        if not device_id:
            return

        existing = self.connection.execute(
            "SELECT * FROM device_liveness WHERE device_id = ?", (device_id,)
        ).fetchone()
        last_telemetry_at = received_at if message_type == "telemetry" else (
            existing["last_telemetry_at"] if existing else None
        )
        last_status_at = received_at if message_type == "status" else (
            existing["last_status_at"] if existing else None
        )
        last_sequence = payload.get("sequence")
        if last_sequence is None and existing:
            last_sequence = existing["last_sequence"]

        mqtt_connected = payload.get("mqtt_connected")
        if mqtt_connected is None and existing:
            mqtt_connected = existing["mqtt_connected"]

        self.connection.execute(
            """
            INSERT INTO device_liveness (
                device_id, last_received_at, last_telemetry_at, last_status_at,
                last_sequence, mqtt_connected, last_message_id, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                last_received_at = excluded.last_received_at,
                last_telemetry_at = COALESCE(excluded.last_telemetry_at, device_liveness.last_telemetry_at),
                last_status_at = COALESCE(excluded.last_status_at, device_liveness.last_status_at),
                last_sequence = COALESCE(excluded.last_sequence, device_liveness.last_sequence),
                mqtt_connected = COALESCE(excluded.mqtt_connected, device_liveness.mqtt_connected),
                last_message_id = excluded.last_message_id,
                updated_at = excluded.updated_at
            """,
            (
                device_id,
                received_at,
                last_telemetry_at,
                last_status_at,
                last_sequence,
                _bool_to_int(mqtt_connected),
                message_id,
                utc_now(),
            ),
        )

    def _ingest_telemetry(self, message_id, payload, received_at):
        device_id = payload.get("device_id")
        sequence = payload.get("sequence")
        quality = "raw_replayed" if payload.get("replayed") else "raw"
        for reading in payload.get("readings", []):
            self.connection.execute(
                """
                INSERT OR IGNORE INTO telemetry_readings (
                    message_id, received_at, greenhouse_id, zone_id, device_id,
                    device_time, sequence, sensor_id, metric, value, unit, quality
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    message_id,
                    received_at,
                    payload.get("greenhouse_id"),
                    payload.get("zone_id"),
                    device_id,
                    payload.get("device_time"),
                    sequence,
                    reading.get("sensor_id"),
                    reading.get("metric"),
                    reading.get("value"),
                    reading.get("unit"),
                    quality,
                ),
            )

    def _ingest_recovery(self, message_id, topic, payload, received_at):
        recovery_id = payload.get("recovery_id")
        device_id = payload.get("device_id")
        for record in _recovery_records(payload):
            if record.get("record_type") == "raw":
                self._ingest_recovery_raw_record(message_id, payload, record, received_at)
                continue
            summary = record
            cursor = self.connection.execute(
                """
                INSERT OR IGNORE INTO recovery_summaries (
                    message_id, received_at, greenhouse_id, zone_id, device_id, recovery_id,
                    offline_reason, sequence_start, sequence_end, device_time_start,
                    device_time_end, window_s, sample_count, quality
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    message_id,
                    received_at,
                    payload.get("greenhouse_id"),
                    payload.get("zone_id"),
                    device_id,
                    recovery_id,
                    payload.get("offline_reason"),
                    summary.get("sequence_start"),
                    summary.get("sequence_end"),
                    summary.get("device_time_start"),
                    summary.get("device_time_end"),
                    summary.get("window_s"),
                    summary.get("sample_count"),
                    summary.get("quality", "summary_replayed"),
                ),
            )
            summary_id = cursor.lastrowid
            if summary_id == 0:
                existing = self.connection.execute(
                    """
                    SELECT id FROM recovery_summaries
                    WHERE device_id = ? AND recovery_id = ? AND sequence_start = ? AND sequence_end = ?
                    """,
                    (
                        device_id,
                        recovery_id,
                        summary.get("sequence_start"),
                        summary.get("sequence_end"),
                    ),
                ).fetchone()
                summary_id = existing["id"] if existing else None
            if summary_id is None:
                continue

            self._insert_summary_readings(summary_id, summary)
            self._insert_reconstructed_readings(summary_id, payload, summary)
            self._insert_gap_covered_event(topic=topic, payload=payload, summary=summary, received_at=received_at)

    def _ingest_recovery_raw_record(self, message_id, payload, record, received_at):
        for reading in record.get("readings", []):
            self.connection.execute(
                """
                INSERT OR IGNORE INTO telemetry_readings (
                    message_id, received_at, greenhouse_id, zone_id, device_id,
                    device_time, sequence, sensor_id, metric, value, unit, quality
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    message_id,
                    received_at,
                    payload.get("greenhouse_id"),
                    payload.get("zone_id"),
                    payload.get("device_id"),
                    record.get("device_time"),
                    record.get("sequence"),
                    reading.get("sensor_id"),
                    reading.get("metric"),
                    reading.get("value"),
                    reading.get("unit"),
                    record.get("quality", "raw_replayed"),
                ),
            )

    def _insert_summary_readings(self, summary_id, summary):
        for reading in summary.get("readings", []):
            self.connection.execute(
                """
                INSERT OR IGNORE INTO recovery_summary_readings (
                    summary_id, sensor_id, metric, unit, avg_value, min_value, max_value,
                    first_value, last_value
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    summary_id,
                    reading.get("sensor_id"),
                    reading.get("metric"),
                    reading.get("unit"),
                    reading.get("avg"),
                    reading.get("min"),
                    reading.get("max"),
                    reading.get("first"),
                    reading.get("last"),
                ),
            )

    def _insert_reconstructed_readings(self, summary_id, payload, summary):
        midpoint = _midpoint_device_time(summary.get("device_time_start"), summary.get("device_time_end"))
        for reading in summary.get("readings", []):
            self.connection.execute(
                """
                INSERT OR IGNORE INTO reconstructed_readings (
                    summary_id, greenhouse_id, zone_id, device_id, recovery_id,
                    reconstructed_device_time, sequence_start, sequence_end,
                    sensor_id, metric, value, unit, quality, window_s, sample_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    summary_id,
                    payload.get("greenhouse_id"),
                    payload.get("zone_id"),
                    payload.get("device_id"),
                    payload.get("recovery_id"),
                    midpoint,
                    summary.get("sequence_start"),
                    summary.get("sequence_end"),
                    reading.get("sensor_id"),
                    reading.get("metric"),
                    reading.get("avg"),
                    reading.get("unit"),
                    "reconstructed_from_summary",
                    summary.get("window_s"),
                    summary.get("sample_count"),
                ),
            )

    def _insert_gap_covered_event(self, topic, payload, summary, received_at):
        event = {
            "event_type": "gap_covered_by_summary",
            "device_id": payload.get("device_id"),
            "recovery_id": payload.get("recovery_id"),
            "sequence_start": summary.get("sequence_start"),
            "sequence_end": summary.get("sequence_end"),
            "sample_count": summary.get("sample_count"),
        }
        self.connection.execute(
            """
            INSERT INTO edge_events (
                event_type, received_at, device_id, topic, payload_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event["event_type"],
                received_at,
                payload.get("device_id"),
                topic,
                json.dumps(event, separators=(",", ":"), sort_keys=True),
            ),
        )

    def _detect_sequence_gap(self, topic, payload, received_at):
        device_id = payload.get("device_id")
        sequence = payload.get("sequence")
        if not device_id or sequence is None:
            return

        previous = self.connection.execute(
            """
            SELECT sequence FROM telemetry_readings
            WHERE device_id = ? AND sequence < ?
            ORDER BY sequence DESC
            LIMIT 1
            """,
            (device_id, sequence),
        ).fetchone()
        if not previous:
            return
        previous_sequence = previous["sequence"]
        if sequence <= previous_sequence + 1:
            return

        event = {
            "event_type": "telemetry_gap_detected",
            "device_id": device_id,
            "from_sequence": previous_sequence,
            "to_sequence": sequence,
            "missing_count": sequence - previous_sequence - 1,
        }
        self.connection.execute(
            """
            INSERT INTO edge_events (
                event_type, received_at, device_id, topic, payload_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event["event_type"],
                received_at,
                device_id,
                topic,
                json.dumps(event, separators=(",", ":"), sort_keys=True),
            ),
        )

    def close(self):
        self.connection.close()


def _bool_to_int(value):
    if value is None:
        return None
    return 1 if bool(value) else 0


def _midpoint_device_time(start, end):
    try:
        return str((int(start) + int(end)) // 2)
    except (TypeError, ValueError):
        return start or end


def _recovery_records(payload):
    records = payload.get("records")
    if records is not None:
        return records
    return [
        {
            **summary,
            "record_type": "summary",
        }
        for summary in payload.get("summaries", [])
    ]
