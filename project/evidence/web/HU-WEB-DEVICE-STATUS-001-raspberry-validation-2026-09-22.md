# HU-WEB-DEVICE-STATUS-001 - Validacion Raspberry/Web

Fecha local: 2026-09-22  
Ambiente: Raspberry `192.168.1.15`, Mosquitto local, SQLite edge, web en computador de desarrollo.

## Objetivo

Validar que la pagina `/project/dispositivos` muestre el estado real de sensores desde la Raspberry sin depender de consola.

## Flujo Validado

```text
ESP -> Mosquitto -> greenhouse-edge-ingestor -> SQLite -> liveness/export -> HTTP snapshot -> Web
```

## Resultado

PASS. La pagina mostro datos reales de Raspberry y el sensor quedo en estado `online`.

## Evidencia Observada

Snapshot HTTP:

```text
curl -i http://192.168.1.15:8088/device-health.json
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *
```

Conteos observados durante la validacion:

```text
mqtt_messages: 13934
telemetry_readings: 41832
recovery_summaries: 153
reconstructed_readings: 1071
device_health: 1
```

Durante el incidente intermedio el sistema reporto correctamente `critical` porque el ingestor no estaba escribiendo nuevos mensajes:

```text
state=critical
last_received=2026-09-23T00:30:11.157579+00:00
last_sequence=77
```

Tras corregir el servicio `greenhouse-edge-ingestor.service`, el usuario confirmo:

```text
ya esta online
y en la pagina ya esta mirando
```

## Incidente Resuelto

Problema:

```text
greenhouse-edge-ingestor.service: Failed at step CHDIR
WorkingDirectory=/home/chuchosam/Documentos/github/invernadero-central
```

Causa:

El unit file instalado en Raspberry conservaba la ruta del computador de desarrollo.

Correccion:

```text
WorkingDirectory=/home/chuchosam/greenhouse/invernadero-central
```

Validacion recomendada:

```bash
systemctl cat greenhouse-edge-ingestor.service
systemctl status greenhouse-edge-ingestor.service --no-pager -l
python3 tools/edge_sqlite_status.py --db var/edge/greenhouse.db
```

## Criterios De Aceptacion

- Ruta `/project/dispositivos` carga: PASS.
- UI consume snapshot real desde Raspberry: PASS.
- HTTP snapshot tiene CORS para navegador: PASS.
- Liveness muestra `online/warning/critical/offline`: PASS.
- Estado `online` visible en pagina tras recuperar ingestor: PASS.

## Notas

- Para web local usar:

```bash
VITE_EDGE_HEALTH_URL=http://192.168.1.15:8088/device-health.json npm run dev
```

- Para evitar reincidencia, siempre validar `WorkingDirectory` de units systemd despues de copiar desde repositorio.
