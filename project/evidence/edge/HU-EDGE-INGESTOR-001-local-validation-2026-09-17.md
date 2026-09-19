# HU-EDGE-INGESTOR-001 - Validacion local

Fecha: 2026-09-17  
Estado: PASS_LOCAL_SYNTHETIC  
Scope: Ingestor MQTT stdin -> SQLite y herramienta de diagnostico.

## Cambios validados

- `edge.ingestor.main` consume lineas formato `mosquitto_sub -v`.
- `SqliteStorage` crea/aplica migracion SQLite.
- `tools/edge_sqlite_status.py` consulta conteos y liveness sin depender del binario `sqlite3`.
- `deploy/systemd/greenhouse-edge-ingestor.service` queda como unidad base para Raspberry.

## Comando de prueba

Se enviaron dos mensajes sinteticos:

- `/status`
- `/telemetry` con `sequence=1`

Resultado del ingestor:

```text
ingested processed=1 bad_json=0 ignored=0
ingested processed=2 bad_json=0 ignored=0
ingested processed=2 bad_json=0 ignored=0
```

## Resultado diagnostico SQLite

```text
counts
  mqtt_messages: 2
  telemetry_readings: 1
  recovery_summaries: 0
  recovery_summary_readings: 0
  reconstructed_readings: 0
  edge_events: 0
  device_liveness: 1
liveness
  device=dev-zfert01-soil-01 last_sequence=1 mqtt_connected=True
recent_recovery
  no recovery summaries
recent_events
  no events
```

## Comprobaciones

- `python3 -m py_compile edge/ingestor/*.py tools/edge_sqlite_status.py`: PASS.
- `python3 tools/edge_sqlite_status.py --db /tmp/greenhouse-edge-raspberry-test.db`: PASS.

## Pendiente en Raspberry

- Instalar servicio systemd.
- Ejecutar ingesta con Mosquitto real.
- Detener/restaurar Mosquitto para generar replay/recovery.
- Capturar `systemctl status`, `journalctl` y `tools/edge_sqlite_status.py`.
