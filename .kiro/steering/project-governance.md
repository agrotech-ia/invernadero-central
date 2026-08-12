# Invernadero Central - Project Governance

Use this steering file for every Kiro workspace agent in this repository.

## Source of truth

- Git is the source of truth.
- Frozen baselines `HU-001` through `HU-009` must not be silently modified.
- Important changes after the baseline must be represented as new decisions, explicit amendments,
  new HUs, or draft artifacts.

## Authority

- A0: read/analyze.
- A1: propose/generate.
- A2: authorized reversible local execution.
- A3: human approval required.

## Hard rules

- Do not invent pinouts, voltages, protocols, registers, agronomic rules, implementation status,
  or validation status.
- Do not recreate existing implementation by default when evidence exists.
- Operational does not mean calibrated or validated.
- Do not mark DONE without evidence.
- Purchases, physical control, paid media, critical deployment, secrets, and high-risk hardware
  changes require human approval.
- Ask one question at a time when clarification is needed.

## Repositories

- Central/governance: `/home/chuchosam/Documentos/github/invernadero-central`
- Sensors/edge/data: `/home/chuchosam/Documentos/github/invernadero/green-house`
- Web UI: `/home/chuchosam/Documentos/github/agrotechia-web-ui`

## Current operating model

- n8n orchestrates chat, routing, backlog recommendation, and handoffs.
- Kiro acts as the execution/refinement/review engine through custom workspace agents.
- A human approves status transitions, critical changes, and final persistence.
