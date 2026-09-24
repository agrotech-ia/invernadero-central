# HU-FW-MQTT-RESILIENCE-001 - Validacion Final

Fecha local: 2026-09-22

## Resultado

PASS_WITH_LIMITATIONS. La resiliencia MQTT base quedo validada para el sensor de suelo y el runtime edge.

## Alcance Validado

- `sequence` monotono por dispositivo.
- Contadores MQTT en `status`.
- Cola volatil corta para telemetria pendiente.
- Reenvio con `replayed=true` y `replayed_at_device_time`.
- `MQTT_MAX_PACKET_SIZE=2048` permite publicar `status` completo.
- Cola drena al reconectar.
- `dropped_telemetry_count=0` en la muestra validada.
- Edge/Raspberry persiste payload original con timestamp local.
- Edge detecta gaps por `device_id + sequence`.
- Liveness y web evidencian ausencia/recuperacion de datos.

## Evidencia Firmware

Reprueba documentada:

```text
Secuencias 0, 1 y 2 reenviadas con replayed=true.
Secuencias 3..10 publicadas normal.
Status device_time=120 publicado correctamente.
mqtt_retry_queue_count=0
mqtt_payload_buffer_size=2048
dropped_telemetry_count=0
last_mqtt_error=none
```

Fuente:

```text
project/evidence/firmware/HU-FW-MQTT-RESILIENCE-001-lab-2026-09-04.md
```

## Evidencia Edge

El runtime Raspberry quedo validado con:

```text
mqtt_messages: 13934
telemetry_readings: 41832
edge_events: 755
device_liveness: 1
device_health: 1
```

Fuente:

```text
project/evidence/edge/EN-EDGE-001-raspberry-runtime-validation-2026-09-22.md
```

## Decision

Cerrar `HU-FW-MQTT-RESILIENCE-001` como base de entrega MQTT resiliente para MVP del sensor de suelo.

## Limitaciones

- No cubre desconexiones largas con downsampling; eso queda en `HU-FW-OFFLINE-RETENTION-001`.
- No certifica todos los firmwares/nodos; eso queda en `HU-FW-MQTT-RESILIENCE-ALL-001`.
- No garantiza exactly-once ni QoS productivo; se conserva estrategia de secuencia, replay y reconciliacion edge.
- La cola es volatil; si el nodo pierde energia, no recupera mediciones no enviadas.

## Trabajo Siguiente

1. Cerrar `HU-FW-MQTT-MEMORY-001` sobre buffers fijos y diagnostico de heap.
2. Cerrar `HU-FW-OFFLINE-RETENTION-001` para desconexiones largas.
3. Cerrar `HU-FW-MQTT-RESILIENCE-ALL-001` al validar/portar en otros sensores.
