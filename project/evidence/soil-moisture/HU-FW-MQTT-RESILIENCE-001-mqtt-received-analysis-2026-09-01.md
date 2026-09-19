# Analisis MQTT recibido en Raspberry - HU-FW-MQTT-RESILIENCE-001

Estado: DRAFT  
Fecha: 2026-09-01  
Fuente: `mosquitto_sub -h localhost -t 'greenhouse/#' -v`  
Dispositivo: `dev-zfert01-soil-01`  
Broker observado por status: `192.168.1.4:1883`

## Objetivo

Revisar los paquetes recibidos por Raspberry para identificar posible perdida de telemetria y alimentar la mitigacion de `HU-FW-MQTT-RESILIENCE-001`.

## Resultado del parseo

| Metrica | Valor |
| --- | ---: |
| Lineas MQTT JSON validas | 85 |
| Mensajes `telemetry` | 65 |
| Mensajes `status` | 20 |
| JSON invalido | 0 |
| Secuencia minima/maxima recibida | `40` / `1015` |
| Secuencias unicas de telemetria | 65 |
| Secuencias duplicadas | 0 |
| Saltos internos detectados | 42 |
| Secuencias faltantes dentro del rango observado | 911 |

Saltos mas grandes observados:

| Desde | Hasta | Secuencias faltantes |
| ---: | ---: | ---: |
| 620 | 739 | 118 |
| 147 | 227 | 79 |
| 439 | 518 | 78 |
| 769 | 830 | 60 |
| 909 | 966 | 56 |
| 368 | 419 | 50 |
| 590 | 620 | 29 |
| 107 | 135 | 27 |
| 247 | 275 | 27 |
| 307 | 335 | 27 |

## Observaciones

- Todos los mensajes `status` recibidos por MQTT reportan `mqtt_connected=true` y `mqtt_state=0`.
- Aun con status conectado, la telemetria recibida por `mosquitto_sub` no es continua por `sequence`.
- El dump no incluye timestamp real de recepcion en Raspberry; solo `device_time` del dispositivo. Por eso no se puede separar con certeza si cada salto fue perdida de MQTT, desconexion del subscriber, pausa manual de captura o salida pegada incompleta.
- La comparacion contra evidencia serial muestra que `sequence=830` si llego al broker, pero muchas secuencias seriales de laboratorio no aparecen en este dump. Esto refuerza que la captura MQTT no debe tratarse como historial completo.
- El firmware observado imprime por serial aunque MQTT falle, pero no reencola payloads no publicados. Si `mqttClient.publish()` falla, esa lectura queda en riesgo de perderse en broker/storage.
- El dump incluye secuencias altas no registradas antes por serial, como `966`, `971`, `972`, `977-982`, `988`, `997`, `1002`, `1007-1009` y `1015`, con humedad `56.2-57.0%`, EC `194-196 us/cm`, `N=2`, `P=50-51`, `K=43-44`.

## Conclusion

Hay evidencia suficiente para tratar MQTT como canal `PARTIAL` en laboratorio. No se puede afirmar que las 911 secuencias faltantes fueron perdidas por el broker, pero si queda comprobado que el sistema actual no permite distinguir captura incompleta de perdida real sin un mecanismo formal de reconciliacion.

Para MVP, cada dispositivo debe publicar telemetria con `sequence` monotono, contadores de intento/exito/fallo y estado de reintento. El edge/backend debe detectar huecos por dispositivo y registrar rangos faltantes, incluso cuando el status reporte MQTT conectado.

## Mitigacion propuesta

1. Firmware: agregar contadores `mqtt_publish_attempt_count`, `mqtt_publish_success_count`, `mqtt_publish_failed_count`, `last_failed_sequence`, `last_published_sequence` y `last_mqtt_error`.
2. Firmware: agregar cola volatil corta de payloads no publicados y reintentar al reconectar, conservando el `sequence` original y marcando `replayed=true`.
3. Firmware: cuando una lectura se descarte por overflow de cola, publicar en status `dropped_telemetry_count` y `oldest_dropped_sequence`.
4. Edge/Raspberry: guardar todos los mensajes recibidos con timestamp local de recepcion.
5. Edge/Raspberry: detectar huecos por `device_id + sequence` y emitir un evento `telemetry_gap_detected` con rango faltante.
6. Prueba QA: apagar broker o bloquear puerto `1883` por una ventana controlada, volver a conectarlo y comparar serial, broker y storage.
