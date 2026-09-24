# Offline Retention Adaptive Standard

Estado: APPROVED_BASELINE  
Fecha: 2026-09-09  
Aplica a: nodos ESP32/XIAO con MQTT

## Objetivo

Reducir perdida de informacion durante desconexiones largas sin saturar RAM. La telemetria en tiempo real puede ser granular, pero el modo offline debe compactar progresivamente.

## Cadencia base recomendada

| Contexto | Telemetria | Status |
| --- | --- | --- |
| Laboratorio | 5 s | 30 s |
| Campo suelo | 60 s | 300 s |
| Campo clima interior/exterior | 60 s | 300 s |

Los firmwares deben exponer en `status`:

```json
{"lab_mode":false,"telemetry_interval_ms":60000,"status_interval_ms":300000}
```

El cambio operativo debe hacerse preferiblemente con una sola bandera:

```cpp
#define LAB_MODE 1
```

`LAB_MODE=1` selecciona telemetria 5s/status 30s. `LAB_MODE=0` selecciona telemetria 60s/status 300s. Los intervalos especificos se pueden sobrescribir solo para pruebas especiales.

## Politica offline recomendada

| Tiempo desconectado | Accion |
| --- | --- |
| 0-10 min | Guardar muestras crudas cada 60 s |
| 10-60 min | Compactar retencion a una muestra/resumen cada 5 min |
| >60 min | Compactar retencion a una muestra/resumen cada 15 min |

Para laboratorio con `LAB_MODE=1`, las ventanas se aceleran:

| Tiempo desconectado | Accion |
| --- | --- |
| 0-1 min | Retener cada 10 s |
| 1-3 min | Retener cada 30 s |
| >3 min | Retener cada 60 s |

## Payload de resumen propuesto

El payload normativo vive en:

- `project/contracts/mqtt/offline-recovery-v1.md`
- `project/contracts/mqtt/offline-recovery-v1.schema.json`

Ejemplo abreviado:

```json
{
  "schema_version": "1.0",
  "message_type": "offline_recovery",
  "device_id": "dev-zfert01-soil-01",
  "recovery_id": "dev-zfert01-soil-01-14-315",
  "offline_reason": "mqtt_disconnected",
  "records": [
    {"record_type":"raw","sequence":25,"quality":"raw_replayed"},
    {"record_type":"summary","sequence_start":31,"sequence_end":90,"quality":"summary_replayed"}
  ]
}
```

## Principios

- No guardar JSON completo para retencion larga.
- Guardar estructuras compactas o acumuladores por metrica.
- Mantener `sequence` para detectar gaps.
- Reportar descartes explicitos cuando se pierde granularidad.
- Al reconectar, reenviar primero muestras crudas recientes y luego resumenes.
- Primera implementacion aceptada: downsampling offline con contadores de compactacion.
- Segunda implementacion esperada: payload `offline_recovery` con records `raw` y `summary`.
- El backend debe marcar puntos reconstruidos como `quality=reconstructed_from_summary`.

## Laboratorio esperado

1. Configurar telemetria de laboratorio a 5 s.
2. Cortar MQTT durante 15 min.
3. Confirmar que se guardan muestras crudas al inicio y resumenes despues.
4. Restaurar MQTT.
5. Confirmar `replayed=true`, cola drenada y resumenes recibidos.
6. Confirmar que memoria libre no cae de forma continua.
