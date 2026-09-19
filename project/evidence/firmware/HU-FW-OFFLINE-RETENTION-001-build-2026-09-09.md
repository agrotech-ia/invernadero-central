# Evidencia build HU-FW-OFFLINE-RETENTION-001

Fecha: 2026-09-09  
Objetivo: dejar defaults de campo para cadencia de telemetria y documentar retencion offline adaptativa.

## Cambios validados

- `TELEMETRY_INTERVAL_MS` default pasa de `5000` a `60000`.
- `STATUS_INTERVAL_MS` default pasa de `30000` a `300000`.
- Se agrega `LAB_MODE` como bandera unica de perfil:
  - `LAB_MODE=1`: telemetria 5s, status 30s.
  - `LAB_MODE=0`: telemetria 60s, status 300s.
- Los payloads `status` reportan:
  - `lab_mode`
  - `telemetry_interval_ms`
  - `status_interval_ms`
- `xiao-esp32c3-soil/include/secrets.h` local mantiene `LAB_MODE=1` para laboratorio.
- Se creo estandar de retencion offline adaptativa.
- Se sube `MQTT_RETRY_QUEUE_SIZE` de 6 a 20 en `xiao-esp32c3-soil`.
- En `xiao-esp32c3-soil` se implementa downsampling offline:
  - `LAB_MODE=1`: 0-1min retiene cada 10s, 1-3min cada 30s, >3min cada 60s.
  - `LAB_MODE=0`: 0-10min retiene cada 60s, 10-60min cada 5min, >60min cada 15min.
- Se agregan contadores de retencion/compactacion offline en `status`.

## Builds

```text
xiao-esp32c3-soil: SUCCESS
RAM: 27.0%
Flash: 65.7%

esp32-sht40: SUCCESS
RAM: 12.0%
Flash: 57.5%

esp32d-outside: SUCCESS
RAM: 14.0%
Flash: 60.4%
```

## Estado

Resultado: `READY_FOR_LAB_VALIDATION`

Pendiente: validar en monitor/MQTT que el status publique los intervalos activos y ejecutar laboratorio de desconexion larga para definir implementacion compactada.
