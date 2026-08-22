# AGENT-GROW-001 - Kiro Growth Content Workflow

Estado: DRAFT

## Objetivo

Invocar `project-growth-content`, agente encargado de crear contenido educativo, calendario y piezas build-in-public claim-safe.

## Flujo

```text
Webhook /project-growth-content
-> Build Kiro GROW Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-growth-content
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
