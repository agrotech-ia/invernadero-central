# HU-OPS-SENSOR-LIVENESS-001 - Validacion Raspberry

Fecha: 2026-09-22  
Estado: PASS_WITH_TEST_THRESHOLD_OBSERVATION  
Host: Raspberry `chuchosam`  
DB: `var/edge/greenhouse.db`

## Resultado

La prueba en Raspberry valido:

- Timer systemd activo para `greenhouse-edge-liveness.timer`.
- Tabla `device_health` creada y actualizada.
- Eventos de liveness persistidos en `edge_events`.
- Transiciones detectadas:
  - `sensor_warning`
  - `sensor_critical`
  - `sensor_offline`
  - `sensor_recovered`

## Evidencia de conteos

```text
mqtt_messages: 13716
telemetry_readings: 41727
recovery_summaries: 140
recovery_summary_readings: 980
reconstructed_readings: 980
edge_events: 734
device_liveness: 1
device_health: 1
```

## Evidencia offline

Comando ejecutado con umbrales cortos:

```bash
python3 tools/edge_liveness_check.py \
  --db var/edge/greenhouse.db \
  --warning-after-s 10 \
  --critical-after-s 20 \
  --offline-after-s 30
```

Salida:

```text
dev-zfert01-soil-01 offline age=297s last_received=2026-09-22T23:51:09.483092+00:00 last_sequence=4007 mqtt_connected=True
```

Evento persistido:

```text
type=sensor_offline
previous_state=warning
state=offline
age_seconds=297
warning_after_s=10
critical_after_s=20
offline_after_s=30
```

## Evidencia recovery

Evento observado previamente durante la misma sesion:

```text
type=sensor_recovered
previous_state=critical
state=online
age_seconds=71
```

## Observacion importante

Despues de ejecutar una prueba manual con umbrales cortos, el timer normal volvio a evaluar con umbrales productivos de laboratorio:

```text
warning_after_s=90
critical_after_s=600
offline_after_s=1800
```

Por eso el estado paso de `offline` a `warning` sin que necesariamente hubiera una recuperacion real de datos nuevos. Esto es esperado si se mezclan perfiles de umbrales sobre la misma base.

## Accion recomendada

Para pruebas futuras:

- Usar una base temporal para simulaciones de umbrales cortos, o
- detener el timer mientras se hacen pruebas manuales con umbrales cortos, o
- agregar modo `--dry-run` para no persistir estados de prueba.

## Criterio

La HU queda validada funcionalmente en Raspberry. Pendiente menor: mejorar ergonomia de pruebas para no contaminar estado real con umbrales cortos.
