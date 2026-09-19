# Evidencia laboratorio HU-FW-CONFIG-PORTAL-001

Fecha: 2026-09-09  
Nodo: `dev-zfert01-soil-01`  
Firmware: `xiao-esp32c3-soil`

## Observacion

Durante la prueba manual del portal se recibio por serial:

```text
MQTT publish: skipped disconnected
Portal config activo por 600s reason=serial_command
AP SSID=dev-zfert01-soil-01-setup
AP IP=192.168.4.1
Conectando MQTT 192.168.1.4:1883
```

Desde el celular/navegador no se pudo acceder a `http://192.168.4.1/` y se observo `ERR_ADDRESS_UNREACHABLE` / connection timeout.

## Analisis

El portal AP si inicio y reporto IP local `192.168.4.1`. Sin embargo, el loop continuo intentando reconectar MQTT contra la IP anterior del broker. Esos intentos pueden bloquear el ciclo principal y retrasar la atencion del servidor web del portal.

Tambien se debe descartar que el celular no haya quedado conectado al AP, que use datos moviles/VPN/DNS privado, o que no haya recibido una IP `192.168.4.x`.

## Mitigacion aplicada

- Se agrego `MQTT_CONNECT_RETRY_INTERVAL_MS=10000`.
- `connectMqtt()` ahora retorna mientras `configPortalActive=true`.
- Al iniciar el portal se desconecta MQTT de forma explicita.
- El status reporta `mqtt_connect_retry_interval_ms`.
- La compilacion PlatformIO fue exitosa.

## Segunda observacion

Despues de iniciar el portal manualmente, el AP reporto:

```text
Portal config activo por 600s reason=serial_command
AP SSID=dev-zfert01-soil-01-setup
AP IP=192.168.4.1
```

El acceso desde navegador siguio dando timeout.

## Segunda mitigacion aplicada

- El portal ahora corta el intento WiFi STA antes de abrir AP.
- El portal inicia en modo `WIFI_AP` puro, no `WIFI_AP_STA`.
- La IP del AP se fija explicitamente con `WiFi.softAPConfig(192.168.4.1, 192.168.4.1, 255.255.255.0)`.
- La compilacion PlatformIO fue exitosa.

## Resultado

Estado: `PASS`

El cambio a portal `WIFI_AP` puro permitio abrir `http://192.168.4.1/`, cambiar la configuracion MQTT y recuperar publicacion.

Evidencia recibida despues del cambio:

```text
"config_source":"nvs"
MQTT publish: ok
sequence=115
MQTT publish: ok
sequence=116
MQTT publish: ok
sequence=117
```

Lectura estable posterior:

```text
Suelo: humedad=26.7% temp=23.9C pH=6.6 EC=112us/cm N=0 P=11 K=3mg/kg
```

La primera validacion permitio cambiar MQTT desde el portal y recuperar publicacion.

## Validacion de apertura automatica por fallo WiFi

Se borro NVS con `config clear` y el nodo reinicio tomando defaults de build:

```text
Configuracion NVS borrada. Se usaran defaults de build/secrets.h.
source=build_defaults
wifi_ssid=Sampied19
```

El SSID configurado no fue encontrado:

```text
No se pudo conectar a WiFi. status=1 WL_NO_SSID_AVAIL
```

Despues de fallos consecutivos, el portal abrio automaticamente:

```text
Portal config activo por 600s reason=wifi_failure_threshold
AP SSID=dev-zfert01-soil-01-setup
AP IP=192.168.4.1
```

Status asociado:

```json
{"config_portal_active":true,"config_source":"build_defaults"}
```

Resultado parcial: `PASS` para apertura automatica del portal por fallo WiFi.

## Validacion de cambio de red y broker

Desde el portal se corrigio la red WiFi y el broker MQTT. El nodo cerro el portal, reconecto a la red y publico en el broker nuevo:

```text
Portal config cerrado.
Conectando WiFi SSID=Sampied
SSID encontrado. RSSI=-73dBm canal=1 cifrado=WPA2
WiFi conectado. IP=192.168.1.13
Conectando MQTT 192.168.1.15:1883
MQTT conectado.
```

La cola MQTT pendiente se reenvio con marca de replay:

```json
{"sequence":25,"replayed":true,"replayed_at_device_time":"315"}
{"sequence":26,"replayed":true,"replayed_at_device_time":"315"}
{"sequence":27,"replayed":true,"replayed_at_device_time":"315"}
{"sequence":28,"replayed":true,"replayed_at_device_time":"315"}
{"sequence":29,"replayed":true,"replayed_at_device_time":"315"}
{"sequence":30,"replayed":true,"replayed_at_device_time":"315"}
```

Status final recibido:

```json
{"wifi_connected":true,"config_portal_active":false,"mqtt_connected":true,"mqtt_host":"192.168.1.15","mqtt_port":1883,"mqtt_retry_queue_count":0,"config_source":"nvs"}
```

Resultado final: `PASS`.
