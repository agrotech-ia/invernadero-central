# Evidencia build HU-FW-OFFLINE-RECOVERY-PROTOCOL-001

Fecha: 2026-09-09  
Firmware: `xiao-esp32c3-soil`

## Implementacion

Se implemento emision de recuperacion offline compacta en el sensor de suelo:

- Topic nuevo: `/telemetry/recovery`.
- Payload `message_type=offline_recovery`.
- Registros `summary` con:
  - `sequence_start`
  - `sequence_end`
  - `device_time_start`
  - `device_time_end`
  - `window_s`
  - `sample_count`
  - `quality=summary_replayed`
  - metricas con `avg`, `min`, `max`, `first`, `last`.
- Los registros `raw` recientes se siguen reenviando por `/telemetry` con `replayed=true`.
- La recuperacion publica un resumen por payload para reducir riesgo de superar `MQTT_MAX_PACKET_SIZE=2048`.
- `status` agrega:
  - `offline_summary_queue_count`
  - `offline_summary_queue_size`
  - `offline_recovery_publish_count`
  - `offline_summary_dropped_count`

## Build

```text
xiao-esp32c3-soil: SUCCESS
RAM: 29.5%
Flash: 66.1%
```

## Estado

Resultado: `PASS`

## Laboratorio 2026-09-16

Durante una prueba con Mosquitto detenido, el firmware acumulo datos offline correctamente:

```json
{
  "mqtt_retry_queue_count": 9,
  "mqtt_retry_queue_size": 20,
  "offline_summary_queue_count": 7,
  "offline_summary_queue_size": 48,
  "offline_retained_telemetry_count": 18,
  "offline_compacted_telemetry_count": 23,
  "offline_recovery_publish_count": 0
}
```

Al restaurar Mosquitto se observaron telemetrias con `replayed=true`, pero el nodo reinicio por watchdog:

```json
{"reset_reason":"task_wdt","boot_count":58}
```

Analisis: el drenaje de cola intentaba publicar varios mensajes replay/recovery en un mismo ciclo. Si el broker acababa de volver o la red estaba inestable, eso podia bloquear el loop y disparar watchdog.

Mitigacion aplicada:

- `MQTT_REPLAY_FLUSH_MAX_PER_LOOP=3`
- `MQTT_RECOVERY_FLUSH_MAX_PER_LOOP=1`
- `flushMqttRetryQueue()` y `flushOfflineRecoveryQueue()` alimentan watchdog.
- `connectMqtt()` ya no drena colas inmediatamente; solo conecta y deja que `loop()` drene por tandas.

Build posterior:

```text
xiao-esp32c3-soil: SUCCESS
RAM: 29.5%
Flash: 66.1%
```

## Retest 2026-09-16

Despues de aplicar drenaje por tandas, se repitio prueba con Mosquitto detenido/restaurado. Resultado contado desde log de `mosquitto_sub`:

```text
recovery_count=7
replayed_telemetry_count=5
first_recovery_id=dev-zfert01-soil-01-60-23-23
last_recovery_id=dev-zfert01-soil-01-60-35-37
summary_sample_counts=[1, 1, 1, 1, 1, 2, 3]
```

Status posterior:

```json
{
  "reset_reason": "unknown",
  "mqtt_connected": true,
  "mqtt_retry_queue_count": 0,
  "offline_summary_queue_count": 0,
  "offline_recovery_publish_count": 7,
  "offline_compacted_telemetry_count": 10,
  "offline_summary_dropped_count": 0,
  "last_mqtt_error": "none"
}
```

Se confirmo recepcion de topic `/telemetry/recovery` con `message_type=offline_recovery` y records `summary` con `avg`, `min`, `max`, `first`, `last`, `sample_count`, `sequence_start` y `sequence_end`.

Estado final firmware: `PASS`.
