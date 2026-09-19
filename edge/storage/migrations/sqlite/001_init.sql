CREATE TABLE mqtt_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    received_at TEXT NOT NULL,
    topic TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    message_type TEXT NOT NULL,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT,
    device_time TEXT,
    sequence INTEGER,
    replayed INTEGER NOT NULL DEFAULT 0,
    recovery_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mqtt_messages_device_received
    ON mqtt_messages (device_id, received_at);

CREATE INDEX idx_mqtt_messages_type
    ON mqtt_messages (message_type);

CREATE TABLE telemetry_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL REFERENCES mqtt_messages(id) ON DELETE CASCADE,
    received_at TEXT NOT NULL,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT NOT NULL,
    device_time TEXT,
    sequence INTEGER NOT NULL,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL,
    unit TEXT,
    quality TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uq_telemetry_reading_device_seq_metric
    ON telemetry_readings (device_id, sequence, sensor_id, metric);

CREATE INDEX idx_telemetry_readings_metric_time
    ON telemetry_readings (metric, received_at);

CREATE TABLE recovery_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL REFERENCES mqtt_messages(id) ON DELETE CASCADE,
    received_at TEXT NOT NULL,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT NOT NULL,
    recovery_id TEXT,
    offline_reason TEXT,
    sequence_start INTEGER,
    sequence_end INTEGER,
    device_time_start TEXT,
    device_time_end TEXT,
    window_s INTEGER,
    sample_count INTEGER,
    quality TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uq_recovery_summary_window
    ON recovery_summaries (device_id, recovery_id, sequence_start, sequence_end);

CREATE TABLE recovery_summary_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    summary_id INTEGER NOT NULL REFERENCES recovery_summaries(id) ON DELETE CASCADE,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    unit TEXT,
    avg_value REAL,
    min_value REAL,
    max_value REAL,
    first_value REAL,
    last_value REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uq_recovery_summary_reading_metric
    ON recovery_summary_readings (summary_id, sensor_id, metric);

CREATE TABLE reconstructed_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    summary_id INTEGER NOT NULL REFERENCES recovery_summaries(id) ON DELETE CASCADE,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT NOT NULL,
    recovery_id TEXT,
    reconstructed_device_time TEXT,
    sequence_start INTEGER,
    sequence_end INTEGER,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL,
    unit TEXT,
    quality TEXT NOT NULL,
    window_s INTEGER,
    sample_count INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uq_reconstructed_reading_metric
    ON reconstructed_readings (summary_id, sensor_id, metric);

CREATE TABLE edge_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    received_at TEXT NOT NULL,
    device_id TEXT,
    topic TEXT,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_edge_events_type_time
    ON edge_events (event_type, received_at);

CREATE TABLE device_liveness (
    device_id TEXT PRIMARY KEY,
    last_received_at TEXT NOT NULL,
    last_telemetry_at TEXT,
    last_status_at TEXT,
    last_sequence INTEGER,
    mqtt_connected INTEGER,
    last_message_id INTEGER REFERENCES mqtt_messages(id) ON DELETE SET NULL,
    updated_at TEXT NOT NULL
);
