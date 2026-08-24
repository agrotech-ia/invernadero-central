# Auditoria de gates de estado - 2026-08-24

## Motivo

Se detectaron tarjetas en `READY`, `IN_PROGRESS` y `VALIDATION` sin que el Mini Jira
mostrara criterios, Gherkin, Definition of Ready o Definition of Done. Esto revelo
dos problemas:

- La UI no estaba agregando detalles desde roadmaps/backlogs secundarios.
- Las reglas de agentes no tenian una compuerta comun obligatoria por estado.

## Acciones aplicadas

- Se creo `project/validation/state-gates.yaml` como fuente comun de compuertas.
- Se conecto el gate a Orchestrator, Backlog, Refinement, QA, Reviewer, PMO,
  Planning, Engineering y Web Agent.
- Se agregaron criterios/Gherkin/DoR/DoD/evidencia esperada a items avanzados que
  ya tenian trabajo real:
  - `EN-AGENT-001`
  - `HU-WEB-ROLE-001`
  - `HU-WEB-KANBAN-001`
  - `EN-AWS-ARCH-001`
  - `HU-SOIL-LAB-001`
- Se corrigieron inconsistencias de estado:
  - `EN-EDGE-001`: `READY` -> `REFINEMENT`
  - `EN-MKT-001`: `READY` -> `REFINEMENT`
  - `EN-GROW-001`: `READY` -> `REFINEMENT`
- Se alinearon columna y `status` interno para `HU-SOIL-001` y `HU-SOIL-LAB-001`.

## Resultado de auditoria final

Todos los items en estados avanzados pasaron gate:

| Item | Estado | Gate | Observacion |
|---|---|---|---|
| `HU-SOIL-001` | READY | PASS | Parent valida: ejecucion por HUs hijas. |
| `HU-SOIL-LAB-001` | READY | PASS | Tiene criterios, Gherkin, DoR, DoD y evidencia esperada. |
| `EN-AWS-ARCH-001` | READY | PASS | Enabler documental listo para revision/decision siguiente. |
| `EN-AGENT-001` | IN_PROGRESS | PASS | Tiene criterios, Gherkin, DoR, DoD y evidencia esperada. |
| `HU-WEB-ROLE-001` | VALIDATION | PASS | Tiene criterios, Gherkin, DoR, DoD y evidencia. |
| `HU-WEB-KANBAN-001` | VALIDATION | PASS | Tiene criterios, Gherkin, DoR, DoD y evidencia. |

## Regla operativa

Si una tarjeta en `READY`, `IN_PROGRESS`, `VALIDATION` o `DONE` falla el gate, el
siguiente paso obligatorio es `REFINEMENT` o `QA`; no ejecucion.
