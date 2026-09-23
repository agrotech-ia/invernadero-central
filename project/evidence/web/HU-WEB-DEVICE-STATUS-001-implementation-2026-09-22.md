# HU-WEB-DEVICE-STATUS-001 - Implementacion

Fecha: 2026-09-22  
Estado: READY_FOR_RASPBERRY_VALIDATION

## Cambios

Edge/Raspberry:

- `tools/edge_export_device_health.py` exporta `device_health`, conteos y eventos recientes desde SQLite a JSON.
- `deploy/systemd/greenhouse-edge-health-export.service` ejecuta export.
- `deploy/systemd/greenhouse-edge-health-export.timer` programa export periodico.
- `project/guides/edge/device-health-web-export-runbook.md` documenta uso.

Web:

- Ruta `/project/dispositivos`.
- Pagina `ProjectDeviceStatusPage.jsx`.
- Navbar con acceso a Dispositivos.
- Snapshot inicial en `public/edge/device-health.json`.

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

## Pendiente Raspberry

- Ejecutar export contra `var/edge/greenhouse.db`.
- Copiar/crear JSON en el repo web de Raspberry.
- Activar timer `greenhouse-edge-health-export.timer`.
- Abrir `/project/dispositivos` y verificar estado real.
