# Laboratorio OTA WiFi - HU-FW-OTA-001

Estado: DRAFT
Fecha: 2026-09-24
Firmware objetivo inicial: `xiao-esp32c3-soil`

## Objetivo

Validar que un nodo instalado puede recibir una actualizacion de firmware por WiFi sin desmontarlo ni conectarlo por USB, manteniendo control operativo y plan de recuperacion.

## Precondiciones

- El nodo esta en banco, con alimentacion estable.
- WiFi y MQTT estan configurados y funcionando.
- `config_source=nvs` o `build_defaults` esta claro antes de iniciar.
- El firmware compila con OTA habilitado:
  - `OTA_ENABLED=1`
  - `OTA_PASSWORD` definido.
- El dispositivo y la maquina de desarrollo estan en la misma red.
- El monitor serial esta disponible para abrir la ventana OTA con `ota start`.

## Variables a registrar

Antes de actualizar:

- `firmware_version`
- `boot_count`
- `reset_reason`
- `ip_address`
- `mqtt_connected`
- `ota_enabled`
- `ota_ready`
- `ota_window_active`

Despues de actualizar:

- `firmware_version`
- `boot_count`
- `reset_reason`
- `mqtt_connected`
- primera telemetria publicada tras reinicio.

## Procedimiento

1. Compilar firmware version actual y confirmar telemetria MQTT.
2. Registrar payload `/status` antes de OTA.
3. Cambiar `FIRMWARE_VERSION` a una version de prueba controlada.
4. Compilar sin subir por USB.
5. En monitor serial ejecutar:

```text
ota start
```

6. Confirmar en status o serial:

```text
ota_window_active=true
ota_ready=true
```

7. Subir firmware por OTA usando PlatformIO en el entorno correspondiente.
8. Esperar reinicio.
9. Confirmar por MQTT que el nodo vuelve online y reporta nueva `firmware_version`.
10. Confirmar que telemetria sigue publicando y que no se pierden credenciales WiFi/MQTT.

## Criterios de aprobacion

- OTA solo se habilita cuando `OTA_ENABLED=1`.
- OTA requiere password.
- La ventana OTA es temporal y controlada por comando.
- El nodo reinicia y reporta nueva `firmware_version`.
- MQTT vuelve a publicar status/telemetria despues de la actualizacion.
- Si falla OTA, queda documentado el paso de recuperacion por USB.

## Criterios para detener prueba

- Alimentacion inestable.
- WiFi RSSI muy bajo o desconexiones repetidas.
- MQTT no esta estable antes de iniciar.
- No se puede confirmar IP actual del nodo.

## Evidencia esperada

- Payload `/status` antes de OTA.
- Comando usado para build/upload OTA.
- Payload `/status` despues de OTA.
- Registro de version anterior y version nueva.
- Nota de recuperacion si falla.

## Limitaciones

- Esta primera iteracion valida OTA local en la misma red.
- No cubre firma criptografica ni gestion centralizada de flota.
- No reemplaza recuperacion por USB ante firmware corrupto.
