# AGENT-REV-001 - Kiro Reviewer Safety Workflow

Estado: DRAFT

## Objetivo

Invocar `project-reviewer-safety`, agente encargado de revisar seguridad, autoridad, evidencia, claims y baseline guard.

## Flujo

```text
Webhook /project-reviewer-safety
-> Build Kiro REV Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-reviewer-safety
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
