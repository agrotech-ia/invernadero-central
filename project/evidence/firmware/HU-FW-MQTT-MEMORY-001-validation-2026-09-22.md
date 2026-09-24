# HU-FW-MQTT-MEMORY-001 - Validacion de cola MQTT con buffers fijos

Fecha: 2026-09-22
Resultado: PASS_WITH_LIMITATIONS

## Alcance validado

- La cola de reintento MQTT del firmware de suelo dejo de depender de `String` retenidos y usa buffers fijos para `topic` y `payload`.
- El `status` del dispositivo expone los limites activos:
  - `mqtt_topic_buffer_size=160`
  - `mqtt_payload_buffer_size=2048`
- En pruebas de desconexion/reconexion, los mensajes retenidos se reenviaron con `replayed=true` y la cola volvio a `mqtt_retry_queue_count=0`.
- En desconexion prolongada se observo descarte explicito por cola llena, sin perdida silenciosa:
  - `dropped_telemetry_count=1`
  - `oldest_dropped_sequence=0`
- El diagnostico de memoria se mantuvo estable durante el laboratorio:
  - `heap_warn=false`
  - `free_heap_bytes=207104`
  - `min_free_heap_bytes=201316`
- No se observaron resets inesperados por watchdog durante la recuperacion de conectividad.

## Evidencia relacionada

- `project/evidence/firmware/HU-FW-MQTT-RESILIENCE-001-lab-2026-09-04.md`
- `project/evidence/firmware/HU-FW-WATCHDOG-001-lab-2026-09-09.md`
- `project/evidence/firmware/HU-FW-REMOTE-OPS-implementation-2026-09-01.md`
- `project/guides/firmware/mqtt-delivery-resilience-standard.md`

## Criterios de aceptacion

- Firmware compila con cola MQTT de buffers fijos: PASS.
- Slots drenados quedan disponibles para reutilizacion: PASS.
- Payload/topic fuera de limite incrementa descarte y error observable: PASS_WITH_LIMITATIONS, validado por descarte de cola llena; mantener vigilancia si el contrato MQTT crece.
- `status` reporta tamanos de buffer: PASS.

## Limitaciones

- Esta HU no cubre retencion offline de 4-5 horas ni compactacion por ventanas; eso queda en `HU-FW-OFFLINE-RETENTION-001`.
- La cola es volatil; una perdida de energia del nodo puede perder mensajes retenidos en RAM.
- Si el payload MQTT crece por nuevas metricas, debe revisarse `MQTT_PAYLOAD_BUFFER_SIZE` y observar `dropped_telemetry_count`.

## Decision

Cerrar `HU-FW-MQTT-MEMORY-001` como DONE. El riesgo residual pasa a las HUs de retencion offline y recuperacion compacta.
