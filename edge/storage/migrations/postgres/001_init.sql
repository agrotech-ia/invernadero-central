-- DRAFT: target production schema equivalent to sqlite/001_init.sql.
-- The ingestor writes through a storage adapter so this migration can replace
-- SQLite without changing MQTT parsing or recovery reconstruction logic.

CREATE TABLE IF NOT EXISTS mqtt_messages (
    id BIGSERIAL PRIMARY KEY,
    received_at TIMESTAMPTZ NOT NULL,
    topic TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    message_type TEXT NOT NULL,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT,
    device_time TEXT,
    sequence INTEGER,
    replayed BOOLEAN NOT NULL DEFAULT FALSE,
    recovery_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_mqtt_messages_device_received
    ON mqtt_messages (device_id, received_at);

CREATE INDEX IF NOT EXISTS idx_mqtt_messages_type
    ON mqtt_messages (message_type);

CREATE TABLE IF NOT EXISTS telemetry_readings (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL REFERENCES mqtt_messages(id) ON DELETE CASCADE,
    received_at TIMESTAMPTZ NOT NULL,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT NOT NULL,
    device_time TEXT,
    sequence INTEGER NOT NULL,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value DOUBLE PRECISION,
    unit TEXT,
    quality TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_telemetry_reading_device_seq_metric UNIQUE (device_id, sequence, sensor_id, metric)
);

CREATE INDEX IF NOT EXISTS idx_telemetry_readings_metric_time
    ON telemetry_readings (metric, received_at);

CREATE TABLE IF NOT EXISTS recovery_summaries (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT NOT NULL REFERENCES mqtt_messages(id) ON DELETE CASCADE,
    received_at TIMESTAMPTZ NOT NULL,
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
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_recovery_summary_window UNIQUE (device_id, recovery_id, sequence_start, sequence_end)
);

CREATE TABLE IF NOT EXISTS recovery_summary_readings (
    id BIGSERIAL PRIMARY KEY,
    summary_id BIGINT NOT NULL REFERENCES recovery_summaries(id) ON DELETE CASCADE,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    unit TEXT,
    avg_value DOUBLE PRECISION,
    min_value DOUBLE PRECISION,
    max_value DOUBLE PRECISION,
    first_value DOUBLE PRECISION,
    last_value DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_recovery_summary_reading_metric UNIQUE (summary_id, sensor_id, metric)
);

CREATE TABLE IF NOT EXISTS reconstructed_readings (
    id BIGSERIAL PRIMARY KEY,
    summary_id BIGINT NOT NULL REFERENCES recovery_summaries(id) ON DELETE CASCADE,
    greenhouse_id TEXT,
    zone_id TEXT,
    device_id TEXT NOT NULL,
    recovery_id TEXT,
    reconstructed_device_time TEXT,
    sequence_start INTEGER,
    sequence_end INTEGER,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value DOUBLE PRECISION,
    unit TEXT,
    quality TEXT NOT NULL,
    window_s INTEGER,
    sample_count INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_reconstructed_reading_metric UNIQUE (summary_id, sensor_id, metric)
);

CREATE TABLE IF NOT EXISTS edge_events (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    received_at TIMESTAMPTZ NOT NULL,
    device_id TEXT,
    topic TEXT,
    payload_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_edge_events_type_time
    ON edge_events (event_type, received_at);

CREATE TABLE IF NOT EXISTS device_liveness (
    device_id TEXT PRIMARY KEY,
    last_received_at TIMESTAMPTZ NOT NULL,
    last_telemetry_at TIMESTAMPTZ,
    last_status_at TIMESTAMPTZ,
    last_sequence INTEGER,
    mqtt_connected BOOLEAN,
    last_message_id BIGINT REFERENCES mqtt_messages(id) ON DELETE SET NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
