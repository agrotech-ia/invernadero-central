# Soil Telemetry MQTT Contract V1

Estado: APPROVED  
HU: HU-SOIL-DATA-001  
Fecha: 2026-09-01  
Schema: `soil.telemetry.v1`

## Topic

```text
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/telemetry
```

Ejemplo:

```text
greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry
```

## Payload minimo

```json
{
  "schema_version": "1.0",
  "greenhouse_id": "gh-lab-01",
  "zone_id": "z-fert-01",
  "device_id": "dev-zfert01-soil-01",
  "device_time": "10136",
  "sequence": 1268,
  "readings": [
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_moisture_pct",
      "value": 86.4,
      "unit": "%"
    },
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_temperature_c",
      "value": 23.5,
      "unit": "C"
    },
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_ph",
      "value": 5.4,
      "unit": "pH"
    },
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_ec_us_cm",
      "value": 315,
      "unit": "us/cm"
    },
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_n_mg_kg",
      "value": 27,
      "unit": "mg/kg"
    },
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_p_mg_kg",
      "value": 109,
      "unit": "mg/kg"
    },
    {
      "sensor_id": "sns-zfert01-soil7in1-01",
      "metric": "soil_k_mg_kg",
      "value": 101,
      "unit": "mg/kg"
    }
  ]
}
```

## Campos

| Campo | Tipo | Requerido | Nota |
| --- | --- | --- | --- |
| `schema_version` | string | si | Version del payload. Para V1 usar `1.0`. |
| `greenhouse_id` | string | si | Invernadero o laboratorio. |
| `zone_id` | string | si | Zona logica/fisica. |
| `device_id` | string | si | Nodo que publica. |
| `device_time` | string | si | Tiempo relativo del dispositivo en segundos. No reemplaza timestamp local del edge. |
| `sequence` | integer | si | Monotono por dispositivo; sirve para detectar huecos. |
| `readings` | array | si | Lista de metricas medidas. |
| `replayed` | boolean | no | `true` si el firmware reenvio un payload tras reconexion. |
| `replayed_at_device_time` | string | no | Tiempo relativo cuando se reintento la entrega. |

## Metricas permitidas

| Metric | Unit | Fuente firmware |
| --- | --- | --- |
| `soil_moisture_pct` | `%` | `Reg0 * 0.1` |
| `soil_temperature_c` | `C` | `Reg1 * 0.1` |
| `soil_ph` | `pH` | `Reg3 * 0.1` |
| `soil_ec_us_cm` | `us/cm` | `Reg2` |
| `soil_n_mg_kg` | `mg/kg` | `Reg4` |
| `soil_p_mg_kg` | `mg/kg` | `Reg5` |
| `soil_k_mg_kg` | `mg/kg` | `Reg6` |

## Reglas de ingestion edge

- El edge debe agregar timestamp local de recepcion, por ejemplo `received_at`.
- El edge debe persistir `topic` completo y payload original.
- El edge debe detectar saltos por `device_id + sequence`.
- Si observa salto, debe registrar evento `telemetry_gap_detected` con `from_sequence`, `to_sequence` y `missing_count`.
- Si recibe `replayed=true`, debe conservar el `sequence` original y no duplicar lecturas ya persistidas.

## Referencias

- `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`
- `project/evidence/soil-moisture/HU-SOIL-LAB-001-evidence-index.md`
- `project/evidence/soil-moisture/HU-FW-MQTT-RESILIENCE-001-mqtt-received-analysis-2026-09-01.md`
- `project/evidence/soil-moisture/HU-SOIL-DATA-001-contract-validation-2026-09-22.md`
