# Kanban del proyecto

Este directorio contiene el tablero operativo del proyecto.

El tablero no reemplaza `project/backlog/master-backlog.yaml`; lo complementa con una vista de
ejecucion diaria para seleccionar, refinar, tomar, validar y cerrar trabajo.

## Principios

- Las HU deben ser pequenas, granulares y verificables.
- Cada HU debe tener un rol experto responsable y un rol revisor.
- Una persona puede tomar historias de cualquier rol, pero el rol define la perspectiva experta.
- No se mueve una HU a `READY` sin refinamiento suficiente.
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
5. Ejecutar o pedir ejecucion a un agente competente.
6. Guardar evidencia.
7. Pedir revision.
8. Solo despues mover estado.

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
