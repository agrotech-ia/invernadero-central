# Arquitectura n8n local

n8n es la capa de orquestación. Git es la fuente de verdad.

Manual/Webhook Trigger
→ Load project rules
→ Load agent registry
→ Orchestrator
→ Context Builder
→ Specialized Agent
→ Reviewer
→ Human Approval when required
→ Persist draft/final to repository
→ Knowledge update

## Primer caso de aceptación

Solicitud: `Construir backlog de validación del sensor de suelo 7-en-1`.

Debe:
- reconocer `OPERATIONAL / VALIDATION PENDING`;
- no reimplementar RS485/firmware existente;
- proponer T-SOIL-001..009;
- generar materiales/procurement;
- producir borrador revisable.
