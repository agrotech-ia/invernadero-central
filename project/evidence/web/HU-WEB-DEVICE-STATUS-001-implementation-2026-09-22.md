# HU-WEB-DEVICE-STATUS-001 - Implementacion

Fecha: 2026-09-22  
Estado: IMPLEMENTED_AND_VALIDATED

## Cambios

Edge/Raspberry:

- `tools/edge_export_device_health.py` exporta `device_health`, conteos y eventos recientes desde SQLite a JSON.
- `deploy/systemd/greenhouse-edge-health-export.service` ejecuta export.
- `deploy/systemd/greenhouse-edge-health-export.timer` programa export periodico.
- `tools/edge_health_http_server.py` sirve el snapshot con CORS para consumo desde navegador.
- `deploy/systemd/greenhouse-edge-health-http.service` mantiene activo el HTTP de snapshots.
- `project/guides/edge/device-health-web-export-runbook.md` documenta uso.

Web:

- Ruta `/project/dispositivos`.
- Pagina `ProjectDeviceStatusPage.jsx`.
- Navbar con acceso a Dispositivos.
- Snapshot inicial en `public/edge/device-health.json`.
- `VITE_EDGE_HEALTH_URL` permite consumir snapshot real desde Raspberry remota.

## Validacion local

Exportador:

```text
exported 1 devices to /tmp/device-health.json
```

Build web:

```text
npm run build
✓ built in 2.56s
```

## Validacion Raspberry

- Export contra `var/edge/greenhouse.db`: PASS.
- HTTP snapshot en `http://192.168.1.15:8088/device-health.json`: PASS.
- Header CORS `Access-Control-Allow-Origin: *`: PASS.
- Web local con `VITE_EDGE_HEALTH_URL=http://192.168.1.15:8088/device-health.json`: PASS.
- `/project/dispositivos` mostro datos reales y finalmente estado `online`: PASS.

Ver evidencia final:

- `project/evidence/web/HU-WEB-DEVICE-STATUS-001-raspberry-validation-2026-09-22.md`
