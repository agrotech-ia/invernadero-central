# CHAT-GATEWAY-001 - Project Agent Chat

Estado: DRAFT

Objetivo: crear una entrada conversacional simple para interactuar con los agentes del proyecto.

## Flujo

```text
Webhook
-> Chat Router
-> JSON response
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

El chat gateway no ejecuta trabajo especializado. Solo:

- recibe mensaje del humano;
- clasifica intencion;
- enruta al agente/workflow sugerido;
- responde con una sola pregunta siguiente;
- mantiene restricciones de gobernanza.

## Limitacion actual

Esta primera version no conserva memoria conversacional persistente.

La memoria debe guardarse despues en Git o en una tabla local cuando se implemente `agent-runner`
o un backend de chat.

## Siguiente evolucion

- Conectar con `AGENT-BKL-001`.
- Conectar con `AGENT-REF-001`.
- Guardar conversaciones relevantes en `project/context/`.
- Crear una interfaz web local sencilla para enviar mensajes al webhook.
