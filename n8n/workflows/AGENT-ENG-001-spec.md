# AGENT-ENG-001 - Kiro Engineering Execution Workflow

Estado: DRAFT

## Objetivo

Invocar `project-engineering`, agente encargado de preparar o ejecutar cambios de codigo acotados y reversibles.

## Flujo

```text
Webhook /project-engineering
-> Build Kiro ENG Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-engineering
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
