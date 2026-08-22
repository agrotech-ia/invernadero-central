# AGENT-HW-001 - Kiro Hardware Lab Workflow

Estado: DRAFT

## Objetivo

Invocar `project-hardware`, agente encargado de preparar trabajo de hardware/lab, potencia, protecciones y procurement tecnico.

## Flujo

```text
Webhook /project-hardware
-> Build Kiro HW Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-hardware
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
