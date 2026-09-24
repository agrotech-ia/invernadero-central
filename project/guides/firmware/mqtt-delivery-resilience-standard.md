# MQTT Delivery Resilience Standard

Estado: APPROVED_BASELINE  
Fecha: 2026-09-02  
Aplica a: nodos ESP32/XIAO que publiquen `greenhouse/#`

## Objetivo

Evitar perdida silenciosa de telemetria en cualquier sensor MQTT del invernadero.

## Requisitos minimos por firmware

- Cada payload de telemetria debe incluir `sequence` monotono por dispositivo.
- La cadencia base de campo debe evitar publicar demasiado rapido sensores lentos; para suelo se recomienda `LAB_MODE=0`, telemetria cada `60000 ms` y status cada `300000 ms`.
- El `status` debe reportar `lab_mode`, `telemetry_interval_ms` y `status_interval_ms`.
- Si MQTT esta desconectado o `publish()` falla, el firmware debe registrar el fallo.
- El `status` debe reportar contadores de entrega MQTT.
- El firmware debe conservar una cola volatil corta de telemetria pendiente.
- La cola debe usar buffers fijos para topic/payload y evitar fragmentacion de heap por `String` retenidos.
- Al reintentar una telemetria, debe conservar el `sequence` original y agregar `replayed=true`.
- Si la cola se llena, debe descartar explicitamente y reportar `dropped_telemetry_count`.

## Campos minimos de status

```json
{
  "mqtt_connected": true,
  "lab_mode": false,
  "telemetry_interval_ms": 60000,
  "status_interval_ms": 300000,
  "mqtt_state": 0,
  "mqtt_host": "192.168.1.4",
  "mqtt_port": 1883,
  "mqtt_publish_attempt_count": 10,
  "mqtt_publish_success_count": 9,
  "mqtt_publish_failed_count": 1,
  "mqtt_retry_queue_count": 0,
  "mqtt_retry_queue_size": 6,
  "mqtt_topic_buffer_size": 160,
  "mqtt_payload_buffer_size": 2048,
  "dropped_telemetry_count": 0,
  "oldest_dropped_sequence": 0,
  "last_published_sequence": 25,
  "last_failed_sequence": 24,
  "last_mqtt_error": "none"
}
```

## Edge/Raspberry

- Capturar `received_at` local.
- Persistir topic completo y payload original.
- Detectar gaps por `device_id + sequence`.
- No duplicar payloads reintentados con `replayed=true`.

## Firmwares cubiertos inicialmente

| Firmware | Estado |
| --- | --- |
| `xiao-esp32c3-soil` | Implementado y compila |
| `esp32-sht40` | Implementado y compila |
| `esp32d-outside` | Implementado y compila |

## Validacion recomendada

1. Encender nodo con MQTT activo.
2. Confirmar `sequence` creciente en telemetria.
3. Confirmar contadores en `status`.
4. Apagar Mosquitto o bloquear puerto `1883`.
5. Esperar varias lecturas.
6. Restaurar Mosquitto.
7. Confirmar `replayed=true`, cola drenada y gaps detectables en Raspberry.

## Retencion offline adaptativa

La cola volatil corta cubre cortes breves. Para desconexiones mas largas, crear una politica adaptativa:

| Tiempo desconectado | Retencion recomendada |
| --- | --- |
| 0-10 min | muestras crudas cada 60 s |
| 10-60 min | resumen cada 5 min con `avg`, `min`, `max`, `sample_count` |
| >60 min | resumen cada 15 min |

Esto conserva una traza visual util sin saturar RAM con JSON completos.
