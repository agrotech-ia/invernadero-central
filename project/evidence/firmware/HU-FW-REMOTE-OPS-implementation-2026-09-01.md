# Firmware remote ops implementation

Estado: READY_FOR_LAB_VALIDATION  
Fecha: 2026-09-01  
Firmware repo: `/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil`

## HUs cubiertas

- `HU-FW-CONFIG-001`
- `HU-FW-CONFIG-PORTAL-001`
- `HU-FW-MQTT-MEMORY-001`
- `HU-FW-WATCHDOG-001`
- `HU-FW-MQTT-RESILIENCE-001`
- `HU-FW-OTA-001`
- `HU-SOIL-DATA-001`
- `HU-FW-MQTT-RESILIENCE-ALL-001`

## Cambios de firmware

- Configuracion persistente en NVS/Preferences para `wifi_ssid`, `wifi_password`, `mqtt_host` y `mqtt_port`.
- Comandos Serial: `config show`, `config set ...`, `config clear`, `config reboot`.
- `status` publica `config_source` sin exponer secretos.
- Contadores MQTT: intentos, exitos, fallos, descartes, ultima secuencia publicada/fallida y ultimo error.
- Cola volatil corta de reintento para telemetria no publicada, con buffers fijos para reducir fragmentacion de heap.
- Payload reintentado conserva `sequence` original y agrega `replayed=true`.
- OTA local controlado: compilado, apagado por defecto, requiere `OTA_ENABLED=1`, `OTA_PASSWORD` y comando Serial `ota start`.
- Resiliencia MQTT portada tambien a `esp32-sht40` y `esp32d-outside`.
- Portal WiFi/AP temporal de rescate en `xiao-esp32c3-soil` para cambiar `wifi_ssid`, `wifi_password`, `mqtt_host` y `mqtt_port` sin reflashear.
- Watchdog de aplicacion, `boot_count`, `reset_reason`, `min_free_heap_bytes`, `heap_warn` y comando Serial `diag show`.

## Cambios edge/contrato

- Contrato DRAFT `soil.telemetry.v1` en `project/contracts/mqtt/soil-telemetry-v1.md`.
- JSON Schema en `project/contracts/mqtt/soil-telemetry-v1.schema.json`.
- Logger de gaps MQTT en `tools/mqtt_gap_logger.py`.
- Runbook de Raspberry en `project/guides/sensors/mqtt-gap-logger-runbook.md`.
- Estandar de configuracion WiFi/MQTT en campo en `project/guides/firmware/wifi-mqtt-config-portal-standard.md`.
- Guia de laboratorio del portal WiFi/MQTT en `project/guides/firmware/wifi-mqtt-config-portal-lab.md`.
- Guia de laboratorio de watchdog/reset en `project/guides/firmware/watchdog-reset-diagnostics-lab.md`.

## Verificacion local

- `pio run`: SUCCESS.
- Uso de memoria final con OTA compilado, portal WiFi/AP disponible, cola MQTT con buffers fijos y watchdog:
  - RAM: 17.5% (`57428` bytes de `327680`)
  - Flash: 64.2% (`841564` bytes de `1310720`)
- `pio run` en todos los entornos `esp32-sht40`: SUCCESS.
  - `dev-zgrow01-air-01`
  - `dev-zgrow01-air-02`
  - `dev-zgrow02-air-01`
  - `dev-zgrow02-air-02`
  - `dev-zgrow02-roof-01`
  - `dev-zgrow02-roof-02`
  - `dev-zgrow03-air-01`
  - `dev-zgrow03-air-02`
  - RAM: 12.0% (`39188` bytes de `327680`)
  - Flash: 57.5% (`754072` bytes de `1310720`)
- `pio run` en `esp32d-outside`: SUCCESS.
  - RAM: 14.0% (`45760` bytes de `327680`)
  - Flash: 60.4% (`791533` bytes de `1310720`)
- `python3 tools/mqtt_gap_logger.py` contra dump real: genera 85 eventos recibidos y 42 gaps.
- `python3 -m json.tool project/contracts/mqtt/soil-telemetry-v1.schema.json`: OK.
- Laboratorio MQTT 2026-09-04: telemetrias `sequence=4..6` recuperadas con `replayed=true`; se detecto `status` demasiado grande para `MQTT_MAX_PACKET_SIZE=1024` y se ajusto a `2048`.
- Laboratorio watchdog 2026-09-09: `watchdog_ready=true`, `heap_warn=false`, sin reinicios inesperados durante desconexion WiFi/MQTT prolongada; cola dreno al reconectar y se registro descarte explicito por overflow.
- Incidente 2026-09-16: `mqtt_host` quedo corrupto en NVS con texto invalido, causando `hostByName(): DNS Failed` y `connect_rc_-2` aunque WiFi seguia conectado. Se documento en `project/evidence/firmware/INC-FW-CONFIG-NVS-001-mqtt-host-corrupt-2026-09-16.md` y se implemento validacion defensiva de `mqtt_host`.

## Validacion pendiente en laboratorio

1. Cargar firmware en XIAO ESP32-C3.
2. Usar `config set mqtt_host <ip-raspberry>` y reiniciar.
3. Confirmar `config_source=nvs` en status.
4. Apagar/restaurar Mosquitto y verificar contadores + `replayed=true`.
5. Cargar firmware con `MQTT_MAX_PACKET_SIZE=2048` y confirmar que `status` llega por Mosquitto.
6. Validar `diag show`, `boot_count`, `reset_reason`, `watchdog_ready` y `min_free_heap_bytes`.
7. Activar OTA solo con `OTA_ENABLED=1` y `OTA_PASSWORD`, abrir ventana con `ota start`, subir firmware y confirmar nueva version/status.
8. Compilar con `CONFIG_PORTAL_ENABLED=1`, provocar fallo WiFi y validar que el AP temporal permite cargar nueva red y broker.
9. Portar Serial/NVS + portal AP a `esp32-sht40` y `esp32d-outside`.
10. Compilar/subir fix de validacion `mqtt_host` y repetir prueba de host invalido.
