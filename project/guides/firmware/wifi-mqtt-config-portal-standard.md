# Estandar de configuracion WiFi/MQTT en campo

Estado: DRAFT  
Fecha: 2026-09-04  
HU: `HU-FW-CONFIG-001`

## Objetivo

Todo nodo de campo con WiFi/MQTT debe poder recuperar conectividad sin reflashear cuando cambie el router, proveedor, SSID, clave WiFi, IP del broker Mosquitto o puerto MQTT.

## Configuracion persistente

Cada firmware debe soportar estos valores persistidos en NVS/Preferences:

- `wifi_ssid`
- `wifi_password`
- `mqtt_host`
- `mqtt_port`

Los valores compilados en `secrets.h` o `platformio.ini` son defaults. Si existe configuracion NVS, tiene prioridad y debe sobrevivir reinicios.

## Canales de recuperacion

### Serial local

Comandos minimos:

```text
config show
config set wifi_ssid <ssid>
config set wifi_password <password>
config set mqtt_host <host-or-ip>
config set mqtt_port <port>
config clear
config reboot
```

`config show` nunca debe imprimir la clave WiFi.

### Portal AP temporal

El portal debe estar apagado por defecto y solo activarse con build flag o secreto local:

```cpp
#define CONFIG_PORTAL_ENABLED 1
#define CONFIG_PORTAL_AP_PASSWORD "clave-segura"
```

Reglas:

- La clave del AP debe tener minimo 8 caracteres.
- El portal inicia por comando `config portal start` o por fallos WiFi repetidos.
- El portal cierra automaticamente por ventana temporal.
- El formulario permite guardar WiFi SSID/password y MQTT host/port.
- Al guardar, el firmware recarga NVS y reintenta conexion.

## Status requerido

El payload de status debe incluir:

- `config_source`: `nvs` o `build_defaults`
- `wifi_connected`
- `wifi_status`
- `mqtt_connected`
- `mqtt_host`
- `mqtt_port`
- `config_portal_enabled`
- `config_portal_active`
- `config_portal_ap_ssid`

No publicar secretos.

## Aplicacion por firmware

- `xiao-esp32c3-soil`: Serial/NVS y portal AP temporal implementados; pendiente prueba fisica.
- `esp32-sht40`: pendiente portar Serial/NVS y portal AP; resiliencia MQTT ya portada.
- `esp32d-outside`: pendiente portar Serial/NVS y portal AP; resiliencia MQTT ya portada.

## Prueba minima

1. Compilar con `CONFIG_PORTAL_ENABLED=1` y `CONFIG_PORTAL_AP_PASSWORD` definido.
2. Cargar firmware en banco.
3. Configurar una red WiFi valida y broker MQTT valido.
4. Confirmar `config_source=nvs` y `mqtt_connected=true`.
5. Cambiar a un SSID o clave invalida.
6. Confirmar que el portal AP inicia despues del umbral de fallos.
7. Desde celular/laptop, entrar al AP y guardar la nueva red.
8. Confirmar reconexion y status actualizado sin reflashear.
