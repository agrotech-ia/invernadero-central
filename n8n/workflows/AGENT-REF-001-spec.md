# AGENT-REF-001 - Kiro Refinement Workflow

Estado: DRAFT

## Objetivo

Conectar n8n con `project-refinement`, el agente Kiro encargado de convertir una HU/enabler
seleccionada en trabajo granular, verificable y revisable.

## Flujo

```text
Webhook /project-refinement
-> Build Kiro Refinement Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-refinement
```

Payload:

```json
{
  "backlog_id": "EN-AGENT-001",
  "depth": "detallado",
  "dry_run": true
}
```

## Runner esperado desde n8n Docker

```text
http://agent-runner:8080/kiro/run
```

## Nota

El workflow inicia con `dry_run: true` por defecto para validar conectividad sin consumir Kiro.
Cuando `kiro-cli` este instalado en `agent-runner` y `KIRO_API_KEY` este disponible, se puede enviar
`dry_run: false`.

Para ejecucion real, la API key de Kiro puede vivir en el entorno del runner o pasar desde n8n como
header `Authorization: Bearer <KIRO_API_KEY>`. No guardar secretos en este repositorio.
