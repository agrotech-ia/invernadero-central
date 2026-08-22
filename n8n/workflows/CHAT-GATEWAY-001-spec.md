# CHAT-GATEWAY-001 - Project Agent Chat

Estado: DRAFT

Objetivo: crear una entrada conversacional acotada al proyecto para interactuar con
los agentes desde el contexto versionado del repo central.

## Flujo

```text
Webhook
-> Build Project Agent Chat Request
-> Call Kiro Agent Runner
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
- usa `AGENT-PMO-001` como gateway contextual por defecto;
- enruta directo a Knowledge, Backlog, Orchestrator, Product, Market, Growth,
  Planning, Discovery, Contract, Refinement, Architecture, Engineering, QA, Edge,
  Web, Hardware o Reviewer cuando la intencion del humano es clara;
- aplica el pipeline tecnico Intake -> Knowledge -> Discovery -> Contract Decision
  -> Refinement -> Review -> QA -> Human Gate cuando la solicitud lo requiere;
- responde con una sola pregunta siguiente;
- mantiene restricciones de gobernanza.

## Limitacion actual

Esta version recibe `conversation_state` desde el cliente si existe, pero todavia no
persiste memoria conversacional automatica en Git o base de datos.

## Siguiente evolucion

- Persistir aprobaciones humanas y decisiones del chat como eventos auditables.
- Guardar conversaciones relevantes en `project/context/`.
- Conectar una memoria conversacional local para evitar depender del cliente.
