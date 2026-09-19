# Evidencia laboratorio watchdog y diagnostico

HU: `HU-FW-WATCHDOG-001`  
Fecha: 2026-09-09  
Dispositivo: `dev-zfert01-soil-01`  
Firmware repo: `/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil`

## Entrada observada

Fuente: monitor serial compartido por usuario.

## Resultado observado

- El status incluye campos de diagnostico:
  - `boot_count=1`
  - `reset_reason=unknown`
  - `watchdog_enabled=true`
  - `watchdog_ready=true`
  - `watchdog_timeout_s=30`
  - `heap_warn=false`
- Durante una desconexion WiFi/MQTT prolongada, el nodo siguio leyendo Modbus y publicando por serial.
- No se observo reinicio inesperado entre `device_time=27` y `device_time=267`.
- La cola MQTT llego a `mqtt_retry_queue_count=6`.
- Al exceder la cola, se registro descarte explicito:
  - `dropped_telemetry_count=1`
  - `oldest_dropped_sequence=0`
- Al reconectar WiFi/MQTT:
  - IP del nodo: `192.168.1.3`
  - MQTT: `192.168.1.4:1883`
  - Secuencias `1..6` se reenviaron con `replayed=true`.
  - La cola dreno a `mqtt_retry_queue_count=0`.
  - `last_mqtt_error=none`.
- El status posterior a reconexion llego por MQTT/serial con `watchdog_ready=true` y `heap_warn=false`.

## Observaciones tecnicas

- RSSI durante fallos WiFi fue debil: entre `-83dBm` y `-89dBm`; esto explica los intentos prolongados de conexion.
- `config_portal_enabled=false`; el firmware intento abrir portal tras el umbral de fallos, pero lo rechazo correctamente por build flag.
- `reset_reason=unknown` queda aceptable como primer arranque observado, pero debe revisarse tras `config reboot` o power cycle.
- En el primer firmware probado, `min_free_heap_bytes` podia reportarse mayor que `free_heap_bytes` porque el status media el minimo antes de crear el JSON y `free_heap_bytes` despues. Se ajusto firmware para medir ambos en el mismo punto antes de construir el payload.

## Resultado parcial

Estado: `PASS_WITH_LIMITATIONS`

El watchdog esta activo y el nodo no reinicio inesperadamente durante una desconexion larga. Falta ejecutar `diag show` y una prueba de reinicio controlado para confirmar `boot_count` incremental y `reset_reason` coherente.

## Reprueba con firmware ajustado

Fuente: monitor serial compartido por usuario despues de subir firmware con ajuste de medicion de heap.

Observaciones:

- WiFi conecto correctamente:
  - SSID: `Sampied`
  - RSSI escaneo: `-74dBm`
  - IP: `192.168.1.3`
- MQTT conecto contra `192.168.1.4:1883`.
- El primer `/status` publico correctamente por MQTT con:
  - `free_heap_bytes=206976`
  - `min_free_heap_bytes=206976`
  - `heap_warn=false`
  - `boot_count=4`
  - `reset_reason=unknown`
  - `watchdog_enabled=true`
  - `watchdog_ready=true`
  - `watchdog_timeout_s=30`
  - `mqtt_connected=true`
  - `mqtt_retry_queue_count=0`
- Las telemetrias `sequence=0..3` publicaron con `MQTT publish: ok`.

Conclusion de reprueba:

- La correccion de heap queda validada: `min_free_heap_bytes <= free_heap_bytes` en el status observado.
- `boot_count` ya demuestra persistencia entre reinicios (`boot_count=4`).
- Watchdog reporta listo y no hay alerta de heap.
- Sigue pendiente obtener salida explicita de `diag show`.
- `reset_reason=unknown` queda como limitacion tecnica a revisar; no bloquea la proteccion watchdog, pero conviene mejorar el mapeo/diagnostico si el SDK no entrega una causa clara.

## Validacion `diag show`

Salida compartida por usuario:

```text
Diagnostico:
  boot_count=4
  reset_reason=unknown
  watchdog_enabled=true
  watchdog_ready=true
  free_heap_bytes=207104
  min_free_heap_bytes=201316
```

Conclusion:

- `diag show` funciona por Serial.
- `watchdog_ready=true` confirma watchdog activo.
- `heap_warn=false` ya habia sido confirmado por status MQTT.
- `min_free_heap_bytes=201316` es menor que `free_heap_bytes=207104`, por lo que la metrica de minimo queda coherente.
- `boot_count=4` confirma persistencia NVS.
- `reset_reason=unknown` queda como limitacion menor para revisar despues.

## Resultado final de laboratorio

Estado: `PASS_WITH_LIMITATIONS`

La HU cumple los criterios funcionales de MVP: watchdog activo, diagnostico por Serial, diagnostico por MQTT status, heap estable y sin reinicios inesperados durante reconexion. La unica limitacion abierta es mejorar la interpretacion de `reset_reason`.

## Siguiente paso

1. Subir firmware con ajuste de medicion de heap.
2. Ejecutar `diag show`.
3. Ejecutar `config reboot`.
4. Confirmar que `boot_count` aumenta y que `reset_reason` cambia a `software` si el SDK lo reporta correctamente.
5. Confirmar en `/status` que `watchdog_ready=true`, `heap_warn=false` y `min_free_heap_bytes <= free_heap_bytes`.
