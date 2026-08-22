# AGENT-DISC-001 - Kiro Technical Discovery

## Purpose

Run an evidence-first technical discovery before a story/enabler is refined or implemented.

## Endpoint

- Method: `POST`
- Path: `/webhook/project-discovery`

## Input

- `message` or `discovery_request`
- `backlog_id`
- `repositories`
- `dry_run`

## Output

The workflow calls `project-discovery` through `agent-runner` and returns a DRAFT/read-only response containing impact map, affected files, entry points, dependencies, reverse dependencies, test surface, infra surface, docs, risks, unknowns, and shared contract recommendation.

## Guardrails

- No final HU writing.
- No speculative contracts.
- No invented paths, endpoints, schemas, services, dependencies, or commands.
- No Kanban/backlog/code changes without human approval.
