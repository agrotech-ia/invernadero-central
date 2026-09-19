import json


def parse_mosquitto_line(line):
    """Parse one `mosquitto_sub -v` line into topic and JSON payload."""
    topic, separator, payload_text = line.strip().partition(" ")
    if not separator or not topic.startswith("greenhouse/"):
        return None

    return topic, json.loads(payload_text)


def message_type_for_topic(topic):
    if topic.endswith("/telemetry/recovery"):
        return "telemetry_recovery"
    if topic.endswith("/telemetry"):
        return "telemetry"
    if topic.endswith("/status"):
        return "status"
    return "other"
