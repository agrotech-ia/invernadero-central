# Laboratorio: portal WiFi/MQTT de rescate

HU: `HU-FW-CONFIG-PORTAL-001`  
Estado: READY_FOR_LAB_VALIDATION  
Firmware objetivo inicial: `xiao-esp32c3-soil`  
Fecha de guia: 2026-09-04

## Objetivo

Validar que el sensor puede recuperar conectividad sin reflashear cuando cambia la red WiFi o el broker MQTT. La prueba simula un caso real de campo: router nuevo, clave nueva, proveedor nuevo o IP nueva de Mosquitto.

## Resultado esperado

- El nodo levanta un AP temporal `dev-zfert01-soil-01-setup`.
- Desde celular/laptop se abre `http://192.168.4.1/`.
- Se guardan `wifi_ssid`, `wifi_password`, `mqtt_host` y `mqtt_port`.
- El nodo cierra el portal y reconecta usando configuracion NVS.
- MQTT vuelve a publicar telemetria/status sin recompilar.
- El status reporta `config_source=nvs` y no expone la clave WiFi.

## Materiales

- XIAO ESP32-C3 con firmware de suelo.
- Sensor de suelo 7-en-1 conectado por RS485.
- Raspberry con Mosquitto activo.
- Celular o laptop con WiFi.
- Cable USB-C de datos para monitor serial.
- Red WiFi 2.4 GHz de prueba.
- IP o hostname del broker MQTT.

## Preparacion

1. Confirmar IP de Mosquitto en Raspberry:

```bash
hostname -I
```

2. Confirmar que Mosquitto recibe mensajes:

```bash
mosquitto_sub -h localhost -t 'greenhouse/#' -v
```

3. En el firmware `xiao-esp32c3-soil`, crear o editar `include/secrets.h`:

```cpp
#pragma once

#undef WIFI_ENABLED
#define WIFI_ENABLED 1

#undef WIFI_SSID
#define WIFI_SSID "WIFI_INICIAL"

#undef WIFI_PASSWORD
#define WIFI_PASSWORD "CLAVE_INICIAL"

#undef MQTT_ENABLED
#define MQTT_ENABLED 1

#undef MQTT_HOST
#define MQTT_HOST "IP_RASPBERRY"

#undef MQTT_PORT
#define MQTT_PORT 1883

#undef CONFIG_PORTAL_ENABLED
#define CONFIG_PORTAL_ENABLED 1

#undef CONFIG_PORTAL_AP_PASSWORD
#define CONFIG_PORTAL_AP_PASSWORD "clave-lab-123"
```

4. Compilar y cargar:

```bash
cd /home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil
pio run
pio run -t upload
pio device monitor -b 115200
```

## Prueba A: configuracion inicial por Serial

1. En monitor serial enviar:

```text
config show
```

2. Registrar:

- `source`
- `wifi_ssid`
- `mqtt_host`
- `mqtt_port`

3. Si se desea forzar configuracion NVS desde el inicio:

```text
config set wifi_ssid WIFI_VALIDO
config set wifi_password CLAVE_VALIDA
config set mqtt_host IP_RASPBERRY
config set mqtt_port 1883
config reboot
```

4. Confirmar en status:

- `config_source=nvs`
- `wifi_connected=true`
- `mqtt_connected=true`

## Prueba B: portal manual

1. En monitor serial enviar:

```text
config portal start
```

2. Confirmar en serial:

```text
Portal config activo
AP SSID=dev-zfert01-soil-01-setup
AP IP=192.168.4.1
```

Mientras el portal esta activo, el firmware debe pausar los reintentos MQTT. Si en serial siguen apareciendo lineas repetidas `Conectando MQTT ...` despues de abrir el portal, cargar una version nueva del firmware antes de continuar.

3. En celular/laptop conectarse al WiFi:

```text
SSID: dev-zfert01-soil-01-setup
Password: clave-lab-123
```

4. Abrir navegador:

```text
http://192.168.4.1/
```

5. Guardar:

- WiFi SSID: red 2.4 GHz valida.
- WiFi password: clave valida.
- MQTT host: IP/hostname de Raspberry.
- MQTT port: `1883`.

6. Confirmar que el portal cierra y el nodo intenta reconectar.

7. En Raspberry confirmar nuevos mensajes:

```bash
mosquitto_sub -h localhost -t 'greenhouse/#' -v
```

8. Registrar un status donde aparezca:

- `config_source`: `nvs`
- `config_portal_enabled`: `true`
- `config_portal_active`: `false`
- `wifi_connected`: `true`
- `mqtt_connected`: `true`
- `mqtt_host`: valor nuevo

## Prueba C: recuperacion por fallo WiFi

1. Configurar una red incorrecta:

```text
config set wifi_ssid WIFI_QUE_NO_EXISTE
config set wifi_password clave-invalida
config reboot
```

2. Esperar los reintentos WiFi. El firmware abre el portal tras `CONFIG_PORTAL_WIFI_FAILURE_THRESHOLD` fallos consecutivos.

3. Confirmar en serial:

```text
No se pudo conectar a WiFi
Portal config activo
```

4. Conectarse al AP desde celular/laptop y corregir la red WiFi y broker MQTT.

5. Confirmar reconexion sin reflashear.

## Prueba D: cambio de broker MQTT

1. Cambiar `mqtt_host` desde el portal a una IP invalida.

2. Confirmar que WiFi sigue conectado pero MQTT no conecta:

- `wifi_connected=true`
- `mqtt_connected=false`
- `last_mqtt_error=connect_rc_...`

3. Volver al portal y guardar la IP correcta de Raspberry.

4. Confirmar que MQTT vuelve a publicar.

## Evidencia a guardar

Crear evidencia en:

```text
project/evidence/firmware/HU-FW-CONFIG-PORTAL-001-lab-YYYY-MM-DD.md
```

Registrar:

- Fecha/hora.
- Firmware cargado.
- Red inicial y red final, sin claves.
- IP/hostname MQTT inicial y final.
- Fragmentos de serial donde inicia/cierra portal.
- Payload status antes/despues.
- Captura o texto de `mosquitto_sub`.
- Resultado final: `PASS`, `PASS_WITH_LIMITATIONS` o `FAIL`.

## Criterios de cierre

La HU puede pasar a `DONE` cuando:

- El portal inicia manualmente.
- El portal inicia por fallo WiFi repetido.
- Se cambia WiFi desde portal y reconecta.
- Se cambia MQTT host desde portal y publica.
- No se imprimen ni publican claves.
- Quedan limitaciones registradas.

## Limitaciones conocidas

- El portal inicial esta implementado solo en `xiao-esp32c3-soil`.
- `esp32-sht40` y `esp32d-outside` deben recibir el mismo patron despues de validar esta prueba.
- El AP es local y temporal; no sirve para gestion remota por internet.
- ESP32-C3 requiere red WiFi 2.4 GHz.

## Troubleshooting

### El AP aparece, pero `http://192.168.4.1/` da timeout

1. Confirmar en serial que aparezca:

```text
Portal config activo
AP IP=192.168.4.1
```

2. Confirmar que el celular/laptop quedo conectado al AP `dev-zfert01-soil-01-setup`.
3. Verificar que el equipo recibio IP `192.168.4.x` y gateway `192.168.4.1`.
4. Desactivar datos moviles, VPN o DNS privado durante la prueba si el navegador intenta salir por internet.
5. Si el log sigue mostrando `Conectando MQTT ...` mientras el portal esta activo, cargar el firmware con pausa MQTT durante portal y reintentar.
