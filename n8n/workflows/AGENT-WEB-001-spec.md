# AGENT-WEB-001 - Kiro Web Frontend Workflow

Estado: DRAFT

## Objetivo

Invocar `project-web`, agente encargado de trabajar dashboard web, UX, datos reales y validacion frontend.

## Flujo

```text
Webhook /project-web
-> Build Kiro WEB Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-web
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
