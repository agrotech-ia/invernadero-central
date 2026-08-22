# AGENT-PROD-001 - Kiro Product Workflow

Estado: DRAFT

## Objetivo

Invocar `project-product`, agente encargado de convertir vision/evidencia en producto, epicas, roadmap e historias candidatas.

## Flujo

```text
Webhook /project-product
-> Build Kiro PROD Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-product
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
