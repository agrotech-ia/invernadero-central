# AGENT-KNOW-001 - Kiro Knowledge Query Workflow

Estado: DRAFT

## Objetivo

Invocar `project-knowledge`, el agente Kiro encargado de recuperar contexto
versionado del proyecto, responder con fuentes, detectar contradicciones y señalar
contexto faltante.

## Flujo

```text
Webhook /project-knowledge
-> Build Kiro Knowledge Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-knowledge
```

Payload:

```json
{
  "knowledge_query": "que sabemos del estado actual del proyecto?",
  "scope": "project",
  "include_sources": true,
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
`dry_run: false`. La salida es consulta contextual DRAFT; no persiste ni cambia
estado del proyecto.
