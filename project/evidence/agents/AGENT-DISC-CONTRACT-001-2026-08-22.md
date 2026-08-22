# Evidencia: Discovery y Shared Contract Agents

Fecha: 2026-08-22

## Resultado

Se agregaron y dejaron operativos dos agentes de calidad previa al refinamiento:

- `AGENT-DISC-001` Technical Discovery Agent.
- `AGENT-CONTRACT-001` Shared Contract Agent.

## Cambios funcionales

- `agent-runner` reconoce `project-discovery` y `project-contract`.
- n8n tiene workflows dedicados:
  - `/webhook/project-discovery`
  - `/webhook/project-contract`
- `CHAT-GATEWAY-001` enruta solicitudes de discovery/impacto tecnico a `project-discovery`.
- `CHAT-GATEWAY-001` enruta solicitudes de contrato/API/MQTT/schema/persistencia a `project-contract`.
- `AGENT-ORCH-001` contempla Discovery y Contract Decision antes de Refinement para trabajo tecnico.
- `AGENT-REF-001` exige Discovery y Shared Contract cuando apliquen antes de finalizar HUs tecnicas.

## Validaciones realizadas

- `docker exec n8n wget -qO- http://agent-runner:8080/health`
  - Resultado: `project-discovery` y `project-contract` aparecen en `agents`.
- `POST /webhook/project-discovery`
  - Payload: `{"message":"descubre el alcance tecnico para EN-EDGE-001","backlog_id":"EN-EDGE-001","dry_run":true}`
  - Resultado: `SUCCESS`, agente `project-discovery`.
- `POST /webhook/project-contract`
  - Payload: `{"message":"define contrato compartido para EN-EDGE-001","backlog_id":"EN-EDGE-001","dry_run":true}`
  - Resultado: `SUCCESS`, agente `project-contract`.
- `POST /webhook/project-agent-chat`
  - Mensaje: `haz discovery de EN-EDGE-001 y analiza impacto tecnico`
  - Resultado: route `primary_agent=project-discovery`.
- `POST /webhook/project-agent-chat`
  - Mensaje: `necesito contrato MQTT y API para EN-EDGE-001`
  - Resultado: route `primary_agent=project-contract`.

## Guardas

- Discovery no redacta HU final ni disena contratos especulativos.
- Contract no crea interfaces sin evidencia de Discovery.
- Refinement no debe finalizar HUs tecnicas sin Discovery y Contract cuando aplique.
- Persistencia, Kanban, compras, despliegues criticos y control fisico siguen bajo aprobacion humana.
