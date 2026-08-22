# AGENT-DOC-001 - Kiro Documentation

## Purpose

Create source-traceable documentation, examples, usage guides, runbooks, onboarding notes, workflow docs, and troubleshooting material for the project.

## Endpoint

- Method: `POST`
- Path: `/webhook/project-documentation`

## Input

- `message` or `documentation_request`
- `topic`
- `audience`
- `dry_run`

## Output

The workflow calls `project-documentation` through `agent-runner` and returns DRAFT documentation with `source_refs`, claim classification, examples, unknowns, and one question when needed.

## Guardrails

- No invented existing features, commands, endpoints, environment variables, or workflows.
- Unverified material must be marked `UNKNOWN` or `PROPOSED`.
- Persistence requires human approval.
