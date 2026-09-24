# HU-FW-MQTT-RESILIENCE-ALL-001 - Validacion transversal MQTT

Fecha: 2026-09-24
Resultado: PASS_WITH_LIMITATIONS

## Alcance Validado

- Existe estandar transversal aprobado en `project/guides/firmware/mqtt-delivery-resilience-standard.md`.
- El patron minimo queda definido para todos los nodos MQTT:
  - `sequence` monotono por dispositivo.
  - contadores de publish en `status`.
  - cola volatil corta de reintento.
  - buffers fijos para topic/payload.
  - reenvio con `replayed=true`.
  - descarte explicito con `dropped_telemetry_count`.
- La implementacion fue portada y compilada en los firmwares actuales:
  - `xiao-esp32c3-soil`: SUCCESS.
  - `esp32-sht40`: SUCCESS en todos sus entornos.
  - `esp32d-outside`: SUCCESS.
- La validacion fisica completa se ejecuto primero en `xiao-esp32c3-soil`, incluyendo:
  - replay MQTT con `replayed=true`.
  - `status` recibido por Mosquitto con contadores.
  - drenaje de cola.
  - deteccion de gaps/liveness en Raspberry.

## Evidencia Relacionada

- `project/guides/firmware/mqtt-delivery-resilience-standard.md`
- `project/evidence/firmware/HU-FW-REMOTE-OPS-implementation-2026-09-01.md`
- `project/evidence/firmware/HU-FW-MQTT-RESILIENCE-001-validation-2026-09-22.md`
- `project/evidence/firmware/HU-FW-MQTT-MEMORY-001-validation-2026-09-22.md`
- `project/evidence/edge/EN-EDGE-001-raspberry-runtime-validation-2026-09-22.md`

## Criterios De Aceptacion

- `xiao-esp32c3-soil`, `esp32-sht40` y `esp32d-outside` compilan con el patron de resiliencia: PASS.
- Cada firmware MQTT expone contadores de publish en status: PASS por implementacion estandar y evidencia de suelo; pendiente prueba fisica individual de SHT40/exterior.
- Cada firmware MQTT reintenta telemetria con `replayed=true`: PASS por implementacion estandar y evidencia de suelo; pendiente prueba fisica individual de SHT40/exterior.
- Existe guia transversal para nuevos sensores: PASS.

## Limitaciones

- No se ejecuto laboratorio fisico completo broker off/on en cada placa SHT40 y exterior.
- No cubre configuracion WiFi/MQTT por portal AP en todos los nodos; esa capacidad fue validada fisicamente en suelo.
- No garantiza entrega exactly-once ni persistencia durable si el microcontrolador pierde energia.

## Decision

Cerrar `HU-FW-MQTT-RESILIENCE-ALL-001` como DONE para MVP, con deuda explicita de hardening para pruebas fisicas por cada familia de nodo.
