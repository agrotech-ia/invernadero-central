import argparse
import json
import sys

from edge.ingestor.mqtt_line import message_type_for_topic, parse_mosquitto_line
from edge.ingestor.storage import SqliteStorage, utc_now


def build_parser():
    parser = argparse.ArgumentParser(
        description="Ingest `mosquitto_sub -v` greenhouse MQTT lines into edge storage."
    )
    parser.add_argument("--db", default="var/edge/greenhouse.db", help="SQLite database path.")
    parser.add_argument("--print-stats-every", type=int, default=25, help="Print progress every N messages.")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    storage = SqliteStorage(args.db)
    storage.migrate()

    stats = {
        "processed": 0,
        "bad_json": 0,
        "ignored": 0,
    }
    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                parsed = parse_mosquitto_line(line)
            except json.JSONDecodeError as error:
                stats["bad_json"] += 1
                print(f"bad_json: {error}", file=sys.stderr)
                continue

            if parsed is None:
                stats["ignored"] += 1
                continue

            topic, payload = parsed
            storage.ingest_message(
                topic=topic,
                payload=payload,
                message_type=message_type_for_topic(topic),
                received_at=utc_now(),
            )
            stats["processed"] += 1

            if args.print_stats_every > 0 and stats["processed"] % args.print_stats_every == 0:
                print(
                    "ingested processed={processed} bad_json={bad_json} ignored={ignored}".format(**stats),
                    file=sys.stderr,
                )
    finally:
        storage.close()

    print(
        "ingested processed={processed} bad_json={bad_json} ignored={ignored}".format(**stats),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
