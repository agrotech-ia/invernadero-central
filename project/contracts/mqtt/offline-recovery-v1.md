# Offline Recovery MQTT Contract V1

Estado: DRAFT  
HU: HU-FW-OFFLINE-RECOVERY-PROTOCOL-001  
Fecha: 2026-09-09  
Schema: `offline.recovery.v1`

## Objetivo

Permitir que un nodo ESP32/XIAO conserve informacion util durante desconexiones largas y que Raspberry/backend pueda reconstruir una serie temporal visual sin exigir que el firmware guarde JSON completos durante horas.

El contrato separa tres conceptos:

- `raw`: lectura real retenida por el dispositivo.
- `summary`: resumen por ventana offline con `avg`, `min`, `max`, `first`, `last`.
- `reconstructed`: punto derivado por Raspberry/backend a partir de un resumen.

## Topics

Telemetria normal:

```text
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/telemetry
```

Paquetes de recuperacion offline:

```text
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/telemetry/recovery
```

Eventos edge derivados:

```text
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/events
```

## Payload de recuperacion

La primera implementacion en `xiao-esp32c3-soil` envia los `raw` retenidos por el topic normal `/telemetry` con `replayed=true`, y envia los registros compactados como `summary` por `/telemetry/recovery`. El contrato permite incluir `raw` dentro de `/telemetry/recovery` si un firmware futuro decide empaquetar ambos tipos en un solo lote.

```json
{
  "schema_version": "1.0",
  "message_type": "offline_recovery",
  "greenhouse_id": "gh-lab-01",
  "zone_id": "z-fert-01",
  "device_id": "dev-zfert01-soil-01",
  "recovery_id": "dev-zfert01-soil-01-14-315",
  "boot_count": 14,
  "replayed_at_device_time": "315",
  "offline_reason": "mqtt_disconnected",
  "retention_policy": {
    "lab_mode": false,
    "raw_until_s": 600,
    "summary_until_s": 3600,
    "raw_interval_s": 60,
    "summary_interval_s": 300,
    "long_summary_interval_s": 900
  },
  "records": [
    {
      "record_type": "raw",
      "sequence": 25,
      "device_time": "271",
      "quality": "raw_replayed",
      "readings": [
        {"sensor_id":"sns-zfert01-soil7in1-01","metric":"soil_moisture_pct","value":26.6,"unit":"%"}
      ]
    },
    {
      "record_type": "summary",
      "sequence_start": 31,
      "sequence_end": 90,
      "device_time_start": "600",
      "device_time_end": "3600",
      "window_s": 300,
      "sample_count": 60,
      "quality": "summary_replayed",
      "readings": [
        {
          "sensor_id": "sns-zfert01-soil7in1-01",
          "metric": "soil_moisture_pct",
          "unit": "%",
          "avg": 26.7,
          "min": 26.4,
          "max": 27.1,
          "first": 26.5,
          "last": 26.9
        }
      ]
    }
  ]
}
```

## Reglas del firmware

- Mantener `sequence` monotono aunque MQTT/WiFi este caido.
- Para `raw`, conservar la lectura compacta con su `sequence` original.
- Para `summary`, acumular `sample_count`, `sum`, `min`, `max`, `first`, `last` por metrica.
- No guardar JSON completo para ventanas largas.
- Publicar primero `raw` reciente y luego `summary` al reconectar.
- Reportar en `status`:
  - `offline_retention_enabled`
  - `offline_retention_capacity`
  - `offline_raw_records_count`
  - `offline_summary_records_count`
  - `offline_compacted_telemetry_count`
  - `offline_dropped_record_count`

## Reglas de ingestion en Raspberry/backend

- Persistir el payload original de recuperacion.
- Para `raw`, insertar como telemetria historica con:
  - `quality=raw_replayed`
  - `source_message_type=offline_recovery`
  - `received_at` local de Raspberry
  - `device_time` original
- Para `summary`, persistir la ventana agregada y generar puntos reconstruidos para visualizacion con:
  - `quality=reconstructed_from_summary`
  - `window_s`
  - `sample_count`
  - `sequence_start`
  - `sequence_end`
- No marcar como perdida total un gap cubierto por `summary`; marcarlo como `covered_by_summary`.
- No duplicar si llega de nuevo el mismo `recovery_id + record_type + sequence/window`.

## Reconstruccion visual recomendada

Para cada `summary`, Raspberry/backend debe crear al menos un punto visual en el centro de la ventana:

```text
reconstructed_device_time = device_time_start + (window_s / 2)
value = avg
quality = reconstructed_from_summary
```

Opcionalmente puede guardar banda visual:

```text
min_band = min
max_band = max
first_value = first
last_value = last
```

Esto permite graficar continuidad durante desconexiones sin afirmar que se recuperaron lecturas exactas.

## Limite de exactitud

Una lectura exacta solo existe si fue guardada como `raw`. Un `summary` permite reconstruir tendencia, promedio y rango, pero no cada valor individual de la ventana.
