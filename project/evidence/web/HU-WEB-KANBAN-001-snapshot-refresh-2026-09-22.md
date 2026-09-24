# HU-WEB-KANBAN-001 - Refresh De Snapshot Kanban

Fecha local: 2026-09-22

## Problema

La web `/project/kanban` no mostraba las HUs cerradas recientemente aunque `project/kanban/board.yaml` y `project/backlog/master-backlog.yaml` ya estaban actualizados.

## Causa

La pagina Kanban no lee el YAML vivo del repo central. Lee un snapshot compilado:

```text
web:src/data/projectBoard.js
```

Ademas, la vista guarda columnas movidas localmente en `localStorage`, por lo que un navegador podia conservar un tablero viejo aunque el snapshot cambiara.

## Cambio

- Se agrego `tools/export_project_board_for_web.py` para regenerar `web:src/data/projectBoard.js` desde `project/kanban/board.yaml`.
- El snapshot incluye `snapshotId`.
- `ProjectKanbanPage.jsx` descarta `localStorage` viejo cuando cambia `snapshotId`.
- Se regenero el snapshot con las HUs cerradas:
  - `HU-WEB-DEVICE-STATUS-001`
  - `EN-EDGE-001`
  - `HU-EDGE-OFFLINE-RECOVERY-001`
  - `HU-OPS-SENSOR-LIVENESS-001`

## Validacion

```text
python3 tools/export_project_board_for_web.py --board project/kanban/board.yaml --out /home/chuchosam/Documentos/github/agrotechia-web-ui/src/data/projectBoard.js
exported 37 cards ... snapshot=793dbf5bc863
```

```text
npm run build
✓ built
```

## Limitacion Vigente

El Kanban web sigue siendo snapshot build-time. Si se actualiza el YAML central, hay que regenerar `src/data/projectBoard.js` o crear una HU posterior para servir el Kanban vivo por API/HTTP desde el repo central.
