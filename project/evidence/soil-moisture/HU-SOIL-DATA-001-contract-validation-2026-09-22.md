# HU-SOIL-DATA-001 - Validacion Contrato MQTT V1

Fecha local: 2026-09-22

## Resultado

PASS. El contrato `soil.telemetry.v1` coincide con payloads reales publicados por el ESP y recibidos por Raspberry/Mosquitto.

## Contrato Validado

Archivos:

- `project/contracts/mqtt/soil-telemetry-v1.md`
- `project/contracts/mqtt/soil-telemetry-v1.schema.json`

Estado:

```text
APPROVED
```

## Topic Real Validado

```text
greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry
```

## Payload Real Normal

Ejemplo recibido en Raspberry:

```json
{
  "schema_version": "1.0",
  "greenhouse_id": "gh-lab-01",
  "zone_id": "z-fert-01",
  "device_id": "dev-zfert01-soil-01",
  "device_time": "4762",
  "sequence": 604,
  "readings": [
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_moisture_pct", "value": 19.5, "unit": "%"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_temperature_c", "value": 24.5, "unit": "C"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_ph", "value": 5.6, "unit": "pH"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_ec_us_cm", "value": 1, "unit": "us/cm"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_n_mg_kg", "value": 0, "unit": "mg/kg"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_p_mg_kg", "value": 0, "unit": "mg/kg"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_k_mg_kg", "value": 0, "unit": "mg/kg"}
  ]
}
```

## Payload Real Replayed

Ejemplo recibido tras reconexion:

```json
{
  "schema_version": "1.0",
  "greenhouse_id": "gh-lab-01",
  "zone_id": "z-fert-01",
  "device_id": "dev-zfert01-soil-01",
  "device_time": "337",
  "sequence": 25,
  "readings": [
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_moisture_pct", "value": 26.9, "unit": "%"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_temperature_c", "value": 22.1, "unit": "C"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_ph", "value": 6.6, "unit": "pH"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_ec_us_cm", "value": 113, "unit": "us/cm"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_n_mg_kg", "value": 0, "unit": "mg/kg"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_p_mg_kg", "value": 11, "unit": "mg/kg"},
    {"sensor_id": "sns-zfert01-soil7in1-01", "metric": "soil_k_mg_kg", "value": 3, "unit": "mg/kg"}
  ],
  "replayed": true,
  "replayed_at_device_time": "363"
}
```

## Cobertura

- Campos requeridos presentes: PASS.
- `schema_version = 1.0`: PASS.
- `sequence` entero monotono por dispositivo: PASS.
- Las 7 metricas de suelo estan cubiertas: PASS.
- Unidades permitidas coinciden con payload real: PASS.
- `replayed` y `replayed_at_device_time` estan definidos como opcionales: PASS.
- Edge conserva payload original y normaliza lecturas: PASS, validado por `EN-EDGE-001`.

## Decision

`soil.telemetry.v1` queda aprobado para MVP/laboratorio y como base de ingesta edge. Cambios futuros de payload deben crear version nueva o ampliacion compatible.
