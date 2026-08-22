# AGENT-CONTRACT-001 - Kiro Shared Contract

## Purpose

Define an evidence-based shared contract for API, MQTT, event, schema, persistence, and cross-layer changes after technical discovery.

## Endpoint

- Method: `POST`
- Path: `/webhook/project-contract`

## Input

- `message` or `contract_request`
- `backlog_id`
- `discovery_ref`
- `dry_run`

## Output

The workflow calls `project-contract` through `agent-runner` and returns a DRAFT/read-only shared contract with applicable deltas, compatibility, error contract, persistence contract, non-functional constraints, and unresolved decisions.

## Guardrails

- Existing contract first.
- No invented fields, endpoints, events, tables, DTOs, SLA, or commands.
- Breaking changes require human decision.
- No Kanban/backlog/code changes without human approval.
