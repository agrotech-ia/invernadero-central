# AGENT-ORCH-001 - Kiro Orchestrator Workflow

Estado: DRAFT

## Objetivo

Invocar `project-orchestrator`, agente encargado de clasificar solicitudes y enrutar al agente competente con guardas de autoridad.

## Flujo

```text
Webhook /project-orchestrator
-> Build Kiro ORCH Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-orchestrator
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
