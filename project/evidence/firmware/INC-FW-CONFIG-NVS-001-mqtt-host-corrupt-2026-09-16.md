# INC-FW-CONFIG-NVS-001 - mqtt_host corrupto en NVS

Fecha: 2026-09-16  
Dispositivo: `dev-zfert01-soil-01`  
Firmware: `xiao-esp32c3-soil`  
Severidad: ALTA  
Estado: FIX_IMPLEMENTED_PENDING_BUILD_UPLOAD

## Resumen

Durante una prueba de larga duracion con el ESP conectado, el sensor siguio leyendo Modbus correctamente y mantuvo WiFi conectado, pero dejo de publicar en MQTT. El problema no fue el sensor de suelo ni Mosquitto: el valor persistido de `mqtt_host` en NVS quedo invalido.

Valor observado en `status`:

```json
"mqtt_host": "<host  config set   config set wifi_ssid <ssid>  config set wifi_pass  config port  config portal stop  diag sh  config clear"
```

Error observado:

```text
hostByName(): DNS Failed
No se pudo conectar MQTT, rc=-2
MQTT publish: skipped disconnected
```

## Impacto

- El firmware intento resolver por DNS un texto invalido como si fuera hostname.
- MQTT quedo desconectado aunque WiFi estaba conectado.
- La cola volatil de reintento se lleno.
- La retencion offline siguio funcionando, pero empezo a descartar datos por saturacion prolongada.

Indicadores del log:

```json
"wifi_connected": true,
"mqtt_connected": false,
"mqtt_state": -2,
"config_source": "nvs",
"mqtt_publish_success_count": 0,
"mqtt_retry_queue_count": 20,
"mqtt_retry_queue_size": 20,
"dropped_telemetry_count": 110,
"offline_summary_dropped_count": 78,
"last_mqtt_error": "connect_rc_-2"
```

## Diagnostico

El firmware aceptaba `mqtt_host` sin validacion desde Serial/portal y luego confiaba en cualquier valor leido desde NVS al arrancar.

La evidencia apunta a una configuracion persistente contaminada con texto de ayuda/comandos. Aunque no se haya cambiado manualmente durante la prueba, el firmware no tenia defensas contra valores invalidos en NVS.

## Recuperacion inmediata sin reflashear

1. Confirmar IP actual de Raspberry:

```bash
hostname -I
```

2. En monitor serial del ESP:

```text
config set mqtt_host <IP_REAL_RASPBERRY>
config set mqtt_port 1883
config reboot
```

3. Verificar:

```json
"mqtt_host": "<IP_REAL_RASPBERRY>",
"mqtt_connected": true,
"last_mqtt_error": "none"
```

Nota: en el incidente el ESP tenia `ip_address=192.168.1.4`, por lo tanto la Raspberry no podia seguir usando esa misma IP.

## Fix permanente implementado

Archivo:

```text
/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil/src/main.cpp
```

Cambios:

- Agregada validacion de `mqtt_host`.
- Se rechazan hosts vacios, demasiado largos o con espacios/caracteres invalidos.
- `config set mqtt_host ...` ya no guarda valores invalidos.
- El portal ya no guarda `mqtt_host` invalido.
- En arranque, si NVS trae `mqtt_host` invalido, el firmware borra solo esa clave y vuelve al valor de `secrets.h`.

## Validacion pendiente

- Compilar `xiao-esp32c3-soil` con PlatformIO local.
- Subir firmware.
- Probar que un `mqtt_host` invalido por Serial sea rechazado.
- Probar que un `mqtt_host` invalido precargado en NVS sea descartado al arrancar.
- Confirmar que tras corregir host, se drena cola/recovery sin reinicio watchdog.

## Aprendizaje

La configuracion persistente en campo debe tratarse como entrada no confiable. Toda clave operativa que pueda dejar el nodo sin comunicacion debe validarse antes de guardar y tambien al arrancar.
