# HU-OPS-SENSOR-LIVENESS-001 - Validacion local

Fecha: 2026-09-22  
Estado: PASS_LOCAL_SYNTHETIC  
Scope: chequeo de liveness desde SQLite, persistencia de `device_health` y eventos de transicion.

## Cambios validados

- Migracion SQLite `002_device_health.sql`.
- Migracion PostgreSQL DRAFT `002_device_health.sql`.
- CLI `tools/edge_liveness_check.py`.
- `tools/edge_sqlite_status.py` muestra tabla `device_health`.
- Timer systemd propuesto para ejecutar chequeo cada minuto.

## Prueba sintetica

Se creo una base SQLite temporal con un mensaje `/status` para `dev-zfert01-soil-01`.

Comandos ejecutados:

```bash
python3 -m edge.ingestor.main --db /tmp/greenhouse-liveness-test.db --print-stats-every 1
python3 tools/edge_liveness_check.py --db /tmp/greenhouse-liveness-test.db --warning-after-s 90 --critical-after-s 600 --offline-after-s 1800
python3 tools/edge_liveness_check.py --db /tmp/greenhouse-liveness-test.db --warning-after-s 0 --critical-after-s 0 --offline-after-s 0
python3 tools/edge_sqlite_status.py --db /tmp/greenhouse-liveness-test.db
```

Resultado:

```text
dev-zfert01-soil-01 online age=0s last_received=... mqtt_connected=True
dev-zfert01-soil-01 offline age=0s last_received=... mqtt_connected=True
```

Estado SQLite:

```text
device_health: 1
edge_events: 2
```

Eventos generados:

- `sensor_online`
- `sensor_offline`

## Comprobaciones

- `python3 -m py_compile edge/ingestor/*.py tools/edge_sqlite_status.py tools/edge_liveness_check.py`: PASS.
- YAML de backlog/kanban: PASS.

## Pendiente en Raspberry

- Ejecutar `python3 tools/edge_liveness_check.py --db var/edge/greenhouse.db` contra la base real.
- Instalar `greenhouse-edge-liveness.timer`.
- Validar transicion real apagando Mosquitto o el ESP.
