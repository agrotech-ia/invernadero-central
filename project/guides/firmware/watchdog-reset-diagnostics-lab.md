# Laboratorio: watchdog y diagnostico de reinicio

HU: `HU-FW-WATCHDOG-001`  
Estado: READY_FOR_LAB_VALIDATION  
Firmware objetivo inicial: `xiao-esp32c3-soil`  
Fecha de guia: 2026-09-04

## Objetivo

Validar que el nodo reporta salud de firmware y memoria, y que el watchdog queda activo para recuperar bloqueos del loop principal en campo.

## Resultado esperado

- El arranque imprime `boot_count`, `reset_reason` y watchdog activo.
- El comando `diag show` muestra memoria libre y memoria minima observada.
- El payload `status` publica diagnostico remoto.
- Durante operacion normal no hay reinicios inesperados.
- `heap_warn=false` con el firmware actual.

## Materiales

- XIAO ESP32-C3 con firmware de suelo.
- Sensor de suelo 7-en-1 conectado.
- Raspberry con Mosquitto activo.
- Cable USB-C de datos.
- Monitor serial a `115200`.

## Preparacion

1. Confirmar que el firmware compila:

```bash
cd /home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil
pio run
```

2. Cargar firmware:

```bash
pio run -t upload
pio device monitor -b 115200
```

3. En Raspberry escuchar MQTT:

```bash
mosquitto_sub -h localhost -t 'greenhouse/#' -v
```

## Prueba A: diagnostico de arranque

1. Reiniciar el XIAO.
2. Registrar las lineas iniciales:

```text
Boot count=...
Reset reason=...
Watchdog activo timeout_s=30
```

3. Criterio esperado:

- `boot_count` aumenta frente al arranque anterior.
- `reset_reason` es coherente con la accion ejecutada, por ejemplo `poweron` o `software`.
- Watchdog queda activo.

## Prueba B: comando serial

1. En monitor serial enviar:

```text
diag show
```

2. Registrar:

- `boot_count`
- `reset_reason`
- `watchdog_enabled`
- `watchdog_ready`
- `free_heap_bytes`
- `min_free_heap_bytes`

3. Criterio esperado:

- `watchdog_enabled=true`
- `watchdog_ready=true`
- `min_free_heap_bytes` tiene un valor estable y no cae progresivamente.

## Prueba C: status MQTT

1. Esperar el siguiente payload `/status`.
2. Confirmar campos:

- `boot_count`
- `reset_reason`
- `watchdog_enabled`
- `watchdog_ready`
- `watchdog_timeout_s`
- `free_heap_bytes`
- `min_free_heap_bytes`
- `heap_warn`

3. Criterio esperado:

- `watchdog_ready=true`
- `heap_warn=false`
- `mqtt_connected=true`
- `mqtt_retry_queue_count=0` en operacion normal.

## Prueba D: estabilidad durante reconexion MQTT

1. Apagar Mosquitto durante 20 a 30 segundos.
2. Encender Mosquitto.
3. Confirmar que el nodo no reinicia inesperadamente.
4. Confirmar que drena la cola MQTT y conserva `watchdog_ready=true`.
5. Revisar si `min_free_heap_bytes` cae de forma significativa.

## Evidencia a guardar

Crear evidencia en:

```text
project/evidence/firmware/HU-FW-WATCHDOG-001-lab-YYYY-MM-DD.md
```

Registrar:

- Fecha/hora.
- Firmware cargado.
- Bloque serial de arranque.
- Salida de `diag show`.
- Payload `/status`.
- Resultado de prueba MQTT off/on.
- Resultado final: `PASS`, `PASS_WITH_LIMITATIONS` o `FAIL`.

## Criterios de cierre

La HU puede pasar a `DONE` cuando:

- Watchdog inicia correctamente.
- `diag show` funciona.
- `/status` reporta diagnostico.
- No hay reinicios inesperados durante prueba MQTT off/on.
- `heap_warn=false` y no se observa caida progresiva de heap.

## Limitaciones

- Esta guia no fuerza un bloqueo intencional para disparar watchdog; esa prueba debe hacerse solo si hay recuperacion fisica facil.
- El diagnostico historico no se persiste completo; `boot_count` se guarda en NVS y la memoria minima se mide desde el arranque actual.
