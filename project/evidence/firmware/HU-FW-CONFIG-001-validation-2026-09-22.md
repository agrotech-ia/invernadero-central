# HU-FW-CONFIG-001 - Validacion Final

Fecha local: 2026-09-22

## Resultado

PASS_WITH_LIMITATIONS. La configuracion WiFi/MQTT sin reflashear quedo validada en el sensor de suelo `dev-zfert01-soil-01`.

## Alcance Validado

- Persistencia NVS/Preferences para configuracion de campo.
- Cambio de broker MQTT desde portal AP temporal.
- Cambio de red WiFi desde portal AP temporal.
- Apertura automatica del portal por fallo WiFi.
- Reconexión posterior usando `config_source=nvs`.
- Publicación MQTT recuperada sin recompilar ni desmontar el sensor.
- Status no expone contraseña WiFi.
- Incidente de `mqtt_host` corrupto documentado y mitigado con validacion defensiva.

## Evidencia Principal

Laboratorio portal:

```text
Portal config activo por 600s reason=wifi_failure_threshold
AP SSID=dev-zfert01-soil-01-setup
AP IP=192.168.4.1
```

Reconexión tras guardar configuración:

```text
Portal config cerrado.
Conectando WiFi SSID=Sampied
WiFi conectado. IP=192.168.1.13
Conectando MQTT 192.168.1.15:1883
MQTT conectado.
```

Status final:

```json
{"wifi_connected":true,"config_portal_active":false,"mqtt_connected":true,"mqtt_host":"192.168.1.15","mqtt_port":1883,"mqtt_retry_queue_count":0,"config_source":"nvs"}
```

## Incidente Relacionado

Se documento `INC-FW-CONFIG-NVS-001` por `mqtt_host` corrupto en NVS. Mitigacion implementada:

- Rechazar `mqtt_host` invalido por Serial/portal.
- Validar `mqtt_host` al arrancar.
- Si NVS contiene host invalido, borrar solo esa clave y volver a defaults de build.

## Limitaciones

- Validado fisicamente en `xiao-esp32c3-soil`.
- Portar el mismo patron a `esp32-sht40` y `esp32d-outside` queda dentro de `HU-FW-MQTT-RESILIENCE-ALL-001`.
- OTA se mantiene en HU separada.

## Decision

Cerrar `HU-FW-CONFIG-001` para MVP del sensor de suelo. El patron queda como estandar firmware en `project/guides/firmware/wifi-mqtt-config-portal-standard.md`.
