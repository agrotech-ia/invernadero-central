#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def parse_mosquitto_line(line):
    topic, separator, payload = line.strip().partition(" ")
    if not separator or not topic.startswith("greenhouse/"):
        return None
    data = json.loads(payload)
    return topic, data


def gap_event(device_id, previous_sequence, current_sequence, topic):
    return {
        "event_type": "telemetry_gap_detected",
        "received_at": utc_now(),
        "device_id": device_id,
        "topic": topic,
        "from_sequence": previous_sequence,
        "to_sequence": current_sequence,
        "missing_count": current_sequence - previous_sequence - 1,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Add received_at timestamps to mosquitto_sub -v output and detect sequence gaps."
    )
    parser.add_argument("--out", required=True, help="JSONL file for received MQTT events.")
    parser.add_argument("--gaps-out", required=True, help="JSONL file for gap events.")
    args = parser.parse_args()

    out_path = Path(args.out)
    gaps_path = Path(args.gaps_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gaps_path.parent.mkdir(parents=True, exist_ok=True)

    last_sequence_by_device = {}

    with out_path.open("a", encoding="utf-8") as out_file, gaps_path.open("a", encoding="utf-8") as gaps_file:
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                parsed = parse_mosquitto_line(line)
            except json.JSONDecodeError as error:
                print(f"bad_json: {error}", file=sys.stderr)
                continue

            if parsed is None:
                continue

            topic, payload = parsed
            received = {
                "received_at": utc_now(),
                "topic": topic,
                "payload": payload,
            }
            out_file.write(json.dumps(received, separators=(",", ":")) + "\n")
            out_file.flush()

            if not topic.endswith("/telemetry") or "sequence" not in payload:
                continue

            device_id = payload.get("device_id", "unknown")
            sequence = int(payload["sequence"])
            previous_sequence = last_sequence_by_device.get(device_id)
            if previous_sequence is not None and sequence > previous_sequence + 1:
                event = gap_event(device_id, previous_sequence, sequence, topic)
                gaps_file.write(json.dumps(event, separators=(",", ":")) + "\n")
                gaps_file.flush()
                print(
                    f"gap device={device_id} from={previous_sequence} to={sequence} missing={event['missing_count']}",
                    file=sys.stderr,
                )

            if previous_sequence is None or sequence > previous_sequence:
                last_sequence_by_device[device_id] = sequence


if __name__ == "__main__":
    main()
