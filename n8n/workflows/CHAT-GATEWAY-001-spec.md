# CHAT-GATEWAY-001 - Project Agent Chat

Estado: DRAFT

Objetivo: crear una entrada conversacional acotada al proyecto para interactuar con
los agentes desde el contexto versionado del repo central.

## Flujo

```text
Webhook
-> Build Project PMO Chat Request
-> Call Kiro PMO Runner
-> Format Chat Response
```

## Endpoint esperado

```text
POST /webhook/project-agent-chat
```

Payload minimo:

```json
{
  "message": "recomienda siguiente trabajo"
}
```

## Responsabilidad

El chat gateway no es un asistente general. Solo responde o trabaja con contexto de:

- sensores, edge, datos y web del invernadero;
- n8n, Kiro y sistema multiagente;
- backlog, Kanban, roadmap, HUs, evidencia, arquitectura y decisiones versionadas.

Responsabilidades:

- recibe mensaje del humano;
- llama a `AGENT-PMO-001` como gateway contextual;
- permite que PMO clasifique intencion y recomiende agente;
- responde con una sola pregunta siguiente;
- mantiene restricciones de gobernanza.

## Limitacion actual

Esta version recibe `conversation_state` desde el cliente si existe, pero todavia no
persiste memoria conversacional automatica en Git o base de datos.

## Siguiente evolucion

- Permitir que el PMO dispare sub-workflows aprobados, no solo recomendar rutas.
- Guardar conversaciones relevantes en `project/context/`.
- Persistir decisiones del chat como eventos auditables.
