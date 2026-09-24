#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml


CAMEL_OVERRIDES = {
    "acceptance_criteria": "acceptanceCriteria",
    "child_story_ids": "childStoryIds",
    "definition_of_done": "definitionOfDone",
    "definition_of_ready": "definitionOfReady",
    "evidence_expected": "evidenceExpected",
    "expert_role": "expertRole",
    "gherkin_scenarios": "gherkinScenarios",
    "gherkin_status": "gherkinStatus",
    "guide_path": "guidePath",
    "is_parent": "isParent",
    "mode_fit": "modeFit",
    "next_action": "nextAction",
    "parent_id": "parentId",
    "parent_note": "parentNote",
    "reviewer_role": "reviewerRole",
    "selection_modes": "selectionModes",
    "wip_limits": "wipLimits",
    "web_path": "webPath",
}


def camelize(key):
    if key in CAMEL_OVERRIDES:
        return CAMEL_OVERRIDES[key]
    return re.sub(r"_([a-zA-Z])", lambda match: match.group(1).upper(), key)


def convert_keys(value):
    if isinstance(value, dict):
        return {camelize(str(key)): convert_keys(item) for key, item in value.items()}
    if isinstance(value, list):
        return [convert_keys(item) for item in value]
    return value


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def normalize_card(card_id, raw_card, lane_by_id):
    card = convert_keys(raw_card or {})
    card["id"] = card_id
    card.setdefault("title", card_id)
    card.setdefault("type", "STORY")
    card.setdefault("priority", "P2")
    card["status"] = card.get("status") or lane_by_id.get(card_id) or "BACKLOG"
    card.setdefault("expertRole", card.get("ownerRole", "Unassigned"))
    card.setdefault("reviewerRole", "Unassigned")
    card.setdefault("effort", "M")
    card.setdefault("modeFit", [])
    card.setdefault("granularity", "needs_refinement")
    card.setdefault("dependencies", [])
    card.setdefault("evidence", [])
    card.setdefault("progress", [])
    card.setdefault("nextAction", "")
    card.setdefault("isParent", False)
    card.setdefault("childStoryIds", [])
    card.setdefault("acceptanceCriteria", [])
    card.setdefault("definitionOfReady", [])
    card.setdefault("definitionOfDone", [])
    card.setdefault("evidenceExpected", [])
    card.setdefault("gherkinScenarios", [])
    card.setdefault("tasks", [])
    return card


def build_snapshot(board_path):
    board_text = board_path.read_text(encoding="utf-8")
    board = yaml.safe_load(board_text)
    lane_by_id = {}
    for lane, ids in (board.get("lanes") or {}).items():
        for card_id in ids or []:
            lane_by_id[str(card_id)] = lane

    cards = [
        normalize_card(str(card_id), raw_card, lane_by_id)
        for card_id, raw_card in (board.get("cards") or {}).items()
    ]

    source_hash = hashlib.sha256(board_text.encode("utf-8")).hexdigest()[:12]
    return {
        "version": str(board.get("version", "1.0")),
        "status": board.get("status", "ACTIVE"),
        "sourceBacklog": board.get("source_backlog"),
        "snapshotId": source_hash,
        "generatedAt": utc_now(),
        "workflow": board.get("workflow", []),
        "wipLimits": board.get("wip_limits", {}),
        "selectionModes": convert_keys(board.get("selection_modes", {})),
        "cards": cards,
    }


def main():
    parser = argparse.ArgumentParser(description="Export project Kanban YAML to the web UI projectBoard.js snapshot.")
    parser.add_argument("--board", default="project/kanban/board.yaml", help="Source Kanban YAML path.")
    parser.add_argument("--out", required=True, help="Output JS module path.")
    args = parser.parse_args()

    payload = build_snapshot(Path(args.board))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    js = "export const projectBoard = "
    js += json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False)
    js += ";\n"
    out_path.write_text(js, encoding="utf-8")
    print(f"exported {len(payload['cards'])} cards to {out_path} snapshot={payload['snapshotId']}")


if __name__ == "__main__":
    main()
