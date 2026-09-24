# EN-EDGE-001 - Validacion Runtime Raspberry

Fecha local: 2026-09-22  
Ambiente: Raspberry `192.168.1.15`, Mosquitto local, SQLite `var/edge/greenhouse.db`.

## Objetivo

Validar que el runtime edge en Raspberry ingiere MQTT, persiste SQLite, reconstruye recovery offline y alimenta liveness para la web.

## Resultado

PASS con incidente operacional resuelto.

## Conteos Observados

```text
mqtt_messages: 13934
telemetry_readings: 41832
recovery_summaries: 153
recovery_summary_readings: 1071
reconstructed_readings: 1071
edge_events: 755
device_liveness: 1
device_health: 1
```

## Liveness Observado Durante Incidente

El sistema detecto correctamente ausencia de datos nuevos:

```text
state=critical
age=1761s
last_received=2026-09-23T00:30:11.157579+00:00
last_sequence=77
mqtt_connected=True
```

Esto confirmo que Mosquitto podia seguir activo mientras el ingestor no escribia a SQLite.

## Incidente Operacional

Sintoma:

```text
greenhouse-edge-ingestor.service: Failed at step CHDIR
status=200/CHDIR
```

Causa:

```text
WorkingDirectory=/home/chuchosam/Documentos/github/invernadero-central
```

Correccion:

```text
WorkingDirectory=/home/chuchosam/greenhouse/invernadero-central
```

Despues de corregir el unit file, el usuario confirmo que el sistema volvio a `online` y que la pagina web ya estaba mirando el dato real.

## Criterios Cubiertos

- Ingesta MQTT hacia SQLite: PASS.
- Persistencia de payload crudo y lecturas normalizadas: PASS.
- Recovery offline persistido: PASS.
- Puntos reconstruidos disponibles: PASS.
- `device_liveness` y `device_health` alimentan estado operativo: PASS.
- Web consume el snapshot generado desde Raspberry: PASS.

## Comandos De Verificacion

```bash
systemctl cat greenhouse-edge-ingestor.service
systemctl status greenhouse-edge-ingestor.service --no-pager -l
python3 tools/edge_sqlite_status.py --db var/edge/greenhouse.db
curl -i http://192.168.1.15:8088/device-health.json
```
