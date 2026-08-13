# AGENT-PLAN-001 - Kiro Project Planning Workflow

Estado: DRAFT

## Objetivo

Invocar `project-planning`, el agente Kiro encargado de planear desde el estado actual
del proyecto, detectar huecos y proponer backlog macro por fases.

## Flujo

```text
Webhook /project-planning
-> Build Kiro Planning Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-planning
```

Payload:

```json
{
  "planning_request": "planificar desde estado actual",
  "depth": "macro",
  "max_items": 10,
  "dry_run": true
}
```

## Runner esperado desde n8n Docker

```text
http://agent-runner:8080/kiro/run
```

El nodo HTTP Request V1 usa `authentication: headerAuth` con la credencial n8n
`httpHeaderAuth` llamada `n8n` para enviar la API key de Kiro al runner.

## Nota

El workflow inicia con `dry_run: true` por defecto. Para ejecucion real, enviar
`dry_run: false`. La salida es DRAFT; persistencia y cambios al backlog requieren
aprobacion humana.
