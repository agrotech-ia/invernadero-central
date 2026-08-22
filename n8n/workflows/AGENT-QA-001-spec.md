# AGENT-QA-001 - Kiro QA Evidence Workflow

Estado: DRAFT

## Objetivo

Invocar `project-qa-evidence`, agente encargado de definir pruebas, revisar evidencia y bloquear DONE si falta prueba.

## Flujo

```text
Webhook /project-qa-evidence
-> Build Kiro QA Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-qa-evidence
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
