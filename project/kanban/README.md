# Kanban del proyecto

Este directorio contiene el tablero operativo del proyecto.

El tablero no reemplaza `project/backlog/master-backlog.yaml`; lo complementa con una vista de
ejecucion diaria para seleccionar, refinar, tomar, validar y cerrar trabajo.

## Principios

- Las HU deben ser pequenas, granulares y verificables.
- Cada HU debe tener un rol experto responsable y un rol revisor.
- Una persona puede tomar historias de cualquier rol, pero el rol define la perspectiva experta.
- No se mueve una HU a `READY` sin refinamiento suficiente.
- Refinamiento suficiente significa cumplir `project/validation/state-gates.yaml`.
- Si durante una conversacion aparece una HU nueva o el humano dice "nueva HU",
  "creemos una HU", "trabajemos esta HU" o "primero armemos la HU", el siguiente
  paso obligatorio es refinamiento, no ejecucion.
- Una HU refinada debe tener problema, resultado, alcance, criterios de aceptacion,
  escenarios Gherkin o excepcion aprobada, DoR, DoD, evidencia esperada, riesgos,
  dependencias/bloqueos y siguiente accion.
- No se mueve ni se conserva una HU ejecutable en `READY`, `IN_PROGRESS`,
  `VALIDATION` o `DONE` si falta criterios, Gherkin/exception, DoR, DoD o evidencia esperada.
- Si el tablero muestra una tarjeta avanzada que falla gate, debe tratarse como
  `gate_violation` y volver a refinamiento/QA antes de ejecutar.
- No se mueve una HU a `DONE` sin evidencia.
- No se editan HU congeladas; se crean nuevas historias, enmiendas o decisiones.
- WIP recomendado: maximo 2 items en `IN_PROGRESS`.

## Estados

```text
IDEA -> BACKLOG -> REFINEMENT -> READY -> IN_PROGRESS -> VALIDATION -> DONE
```

## Uso diario

1. Revisar `project/kanban/board.yaml`.
2. Elegir modo de trabajo:
   - `quick_win`
   - `deep_work`
   - `physical_lab`
   - `coding`
   - `docs_governance`
   - `market_growth`
3. Tomar maximo una HU nueva si el WIP lo permite.
4. Refinar la HU si no esta lista.
5. Si aparece una HU nueva, crear/refinar la HU antes de ejecutar.
6. Ejecutar o pedir ejecucion a un agente competente.
7. Guardar evidencia.
8. Pedir revision.
9. Solo despues mover estado.

## Relacion con agentes

El agente de backlog debe leer este tablero antes de recomendar trabajo.

El Refinement Agent debe usar:

```text
project/backlog/templates/hu-template.yaml
project/roles/expert-role-catalog.yaml
```

El Reviewer / QA Agent debe verificar:

- granularidad;
- rol experto;
- criterios de aceptacion;
- evidencia esperada;
- riesgos;
- DoR;
- DoD;
- dependencias;
- aprobaciones humanas.
