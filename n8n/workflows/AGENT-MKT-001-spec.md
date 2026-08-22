# AGENT-MKT-001 - Kiro Market Intelligence Workflow

Estado: DRAFT

## Objetivo

Invocar `project-market-intelligence`, agente encargado de investigar nichos, keywords, competidores e hipotesis de demanda.

## Flujo

```text
Webhook /project-market-intelligence
-> Build Kiro MKT Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-market-intelligence
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
