# AGENT-PMO-001 - Kiro PMO Flow Control Workflow

Estado: DRAFT

## Objetivo

Invocar `project-pmo`, el agente Kiro encargado de revisar roadmap, backlog,
Kanban, WIP, dependencias, bloqueos y evidencias para recomendar la siguiente
mejor accion y el agente correcto para continuar.

## Flujo

```text
Webhook /project-pmo
-> Build Kiro PMO Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-pmo
```

Payload:

```json
{
  "pmo_request": "revisar flujo y recomendar siguiente accion",
  "available_time": "unknown",
  "preferred_mode": "any",
  "max_options": 3,
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
`dry_run: false`. La salida es DRAFT; mover estados, crear items o asignar trabajo
requiere aprobacion humana.
