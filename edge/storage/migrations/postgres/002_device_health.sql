-- DRAFT: production equivalent of sqlite/002_device_health.sql.

CREATE TABLE IF NOT EXISTS device_health (
    device_id TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    previous_state TEXT,
    last_received_at TIMESTAMPTZ,
    last_telemetry_at TIMESTAMPTZ,
    last_status_at TIMESTAMPTZ,
    last_sequence INTEGER,
    mqtt_connected BOOLEAN,
    age_seconds INTEGER NOT NULL,
    warning_after_s INTEGER NOT NULL,
    critical_after_s INTEGER NOT NULL,
    offline_after_s INTEGER NOT NULL,
    checked_at TIMESTAMPTZ NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_device_health_state
    ON device_health (state, checked_at);
