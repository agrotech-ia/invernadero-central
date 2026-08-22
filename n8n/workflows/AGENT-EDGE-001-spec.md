# AGENT-EDGE-001 - Kiro Edge Platform Workflow

Estado: DRAFT

## Objetivo

Invocar `project-edge`, agente encargado de trabajar runtime edge, MQTT, DB, ingesta, logs y observabilidad.

## Flujo

```text
Webhook /project-edge
-> Build Kiro EDGE Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-edge
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
