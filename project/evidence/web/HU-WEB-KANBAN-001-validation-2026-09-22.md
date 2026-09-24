# HU-WEB-KANBAN-001 - Validacion Final

Fecha local: 2026-09-22

## Resultado

PASS. El usuario confirmo:

```text
1 validado y funcional.
```

## Alcance Aceptado

La HU se cierra como tablero Kanban basado en snapshot versionado:

- Ruta `/project/kanban`.
- Columnas por estado.
- Tarjetas con detalle.
- Drag and drop local.
- Reset al snapshot.
- Snapshot regenerable desde `project/kanban/board.yaml`.
- Invalidacion de `localStorage` cuando cambia `snapshotId`.

## Validacion Tecnica

```text
python3 tools/export_project_board_for_web.py --board project/kanban/board.yaml --out /home/chuchosam/Documentos/github/agrotechia-web-ui/src/data/projectBoard.js
```

```text
npm run build
PASS
```

## Decision

Se acepta que esta HU no implemente Kanban vivo por API ni escritura persistente en Git.

Trabajo futuro:

- `HU-WEB-KANBAN-002`: propuesta trazable de cambio de estado.
- HU futura opcional: consumir Kanban vivo por API/HTTP.
