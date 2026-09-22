CREATE TABLE device_health (
    device_id TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    previous_state TEXT,
    last_received_at TEXT,
    last_telemetry_at TEXT,
    last_status_at TEXT,
    last_sequence INTEGER,
    mqtt_connected INTEGER,
    age_seconds INTEGER NOT NULL,
    warning_after_s INTEGER NOT NULL,
    critical_after_s INTEGER NOT NULL,
    offline_after_s INTEGER NOT NULL,
    checked_at TEXT NOT NULL,
    changed_at TEXT NOT NULL
);

CREATE INDEX idx_device_health_state
    ON device_health (state, checked_at);
