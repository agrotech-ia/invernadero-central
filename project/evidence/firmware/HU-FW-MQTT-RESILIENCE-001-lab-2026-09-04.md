# Evidencia laboratorio MQTT resiliente

HU: `HU-FW-MQTT-RESILIENCE-001`  
Fecha: 2026-09-04  
Dispositivo: `dev-zfert01-soil-01`  
Firmware repo: `/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil`

## Muestra recibida

Fuente sensor serial:

- Modbus: `@0x0 count=7 id=1 4800 8N1`
- Registros observados: `Reg0=486`, `Reg1=231`, `Reg2=253`, `Reg3=57`, `Reg4=14`, `Reg5=79`, `Reg6=71`
- Lectura interpretada: humedad `48.6%`, temperatura `23.1C`, pH `5.7`, EC `253us/cm`, N `14`, P `79`, K `71mg/kg`

Fuente Mosquitto:

- Topico: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Secuencias recibidas en muestra pegada: `4`, `5`, `6`, `7`, `8`
- Secuencias `4`, `5`, `6` llegaron con `replayed=true` y `replayed_at_device_time=55`.
- Secuencias `7`, `8` llegaron como publicacion normal.

## Analisis

- La cola volatil de reintento funciono para telemetria: las secuencias `4`, `5` y `6` fueron retenidas durante desconexion MQTT y reenviadas al reconectar.
- No se observan saltos dentro del tramo recibido por Mosquitto `4..8`.
- Las secuencias `0..3` aparecen con `MQTT publish: ok` en serial, pero no estan en el bloque Mosquitto pegado. Esto puede deberse a que `mosquitto_sub` empezo despues o a una captura parcial.
- Los payloads de telemetria calzan con los registros Modbus y la interpretacion esperada.
- Los payloads `status` impresos por serial fallaron con `MQTT publish: failed`; la causa probable es tamano de paquete. El firmware estaba con `MQTT_MAX_PACKET_SIZE=1024` y el `status` crecio por contadores, OTA y portal.

## Correccion aplicada

- `xiao-esp32c3-soil/platformio.ini`: `MQTT_MAX_PACKET_SIZE` sube de `1024` a `2048`.
- `xiao-esp32c3-soil/src/main.cpp`: `lastMqttError` vuelve a `none` cuando MQTT reconecta correctamente.
- `xiao-esp32c3-soil/src/main.cpp`: la cola MQTT cambia de `String` retenidos a buffers fijos `char` para evitar fragmentacion de heap durante desconexiones repetidas.
- El status reporta `mqtt_topic_buffer_size` y `mqtt_payload_buffer_size`.

## Verificacion local

- `pio run`: SUCCESS
- RAM: 17.5% (`57404` bytes de `327680`)
- Flash: 64.0% (`838924` bytes de `1310720`)

## Resultado parcial

Estado: `PASS_WITH_LIMITATIONS`

La resiliencia de telemetria queda validada para una desconexion corta. Falta cargar el firmware corregido y confirmar que los mensajes `status` llegan por Mosquitto sin `MQTT publish: failed`.

## Reprueba con firmware corregido

Entrada: bloques serial y Mosquitto compartidos durante prueba posterior a `MQTT_MAX_PACKET_SIZE=2048` y cola MQTT con buffers fijos.

Observaciones serial:

- Arranque con WiFi inicialmente desconectado: `wifi_connected=false`, `mqtt_connected=false`.
- El firmware mantuvo telemetrias pendientes en cola: `mqtt_retry_queue_count` subio de `1` a `3`.
- El nodo encontro SSID `Sampied`, RSSI entre `-74dBm` y `-69dBm`, y finalmente conecto con IP `192.168.1.6`.
- MQTT reconecto contra `192.168.1.4:1883`.
- Las secuencias `0`, `1` y `2` se reenviaron con `replayed=true` y `replayed_at_device_time=106`.
- Luego las secuencias `3..10` publicaron normal por serial con `MQTT publish: ok`.
- El status de `device_time=120` publico correctamente: `MQTT publish: ok`.

Observaciones Mosquitto:

- Re-copia completa confirma que Mosquitto recibio telemetrias `sequence=0..5` sin gaps.
- Mosquitto recibio `sequence=0`, `1` y `2` con `replayed=true` y `replayed_at_device_time=106`.
- Mosquitto recibio `sequence=3`, `4` y `5` como telemetrias normales posteriores a la reconexion.
- Mosquitto recibio `status` en `device_time=120`.
- El status recibido reporto:
  - `wifi_connected=true`
  - `mqtt_connected=true`
  - `mqtt_state=0`
  - `mqtt_retry_queue_count=0`
  - `mqtt_payload_buffer_size=2048`
  - `dropped_telemetry_count=0`
  - `last_mqtt_error=none`

Conclusion de reprueba:

- El ajuste de `MQTT_MAX_PACKET_SIZE=2048` resolvio la publicacion de `status`.
- La cola de buffers fijos dreno correctamente al reconectar.
- No hubo descartes por overflow en esta muestra.
- La evidencia Mosquitto confirma entrega ordenada `sequence=0..5`; el tramo recuperado `0..2` llego marcado como replay.

## Siguiente prueba recomendada

1. Cargar firmware corregido en el XIAO.
2. Ejecutar `mosquitto_sub -h localhost -t 'greenhouse/#' -v`.
3. Confirmar llegada de `telemetry` y `status`.
4. Apagar Mosquitto 20-30 segundos.
5. Encender Mosquitto.
6. Confirmar `replayed=true` en telemetrias pendientes.
7. Confirmar que `status` publica `mqtt_publish_failed_count`, `mqtt_retry_queue_count` y `last_mqtt_error`.
