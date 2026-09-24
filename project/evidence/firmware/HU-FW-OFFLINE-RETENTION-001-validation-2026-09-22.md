# HU-FW-OFFLINE-RETENTION-001 - Validacion de retencion offline adaptativa

Fecha: 2026-09-22
Resultado: PASS_WITH_LIMITATIONS

## Alcance validado

- Se definio una bandera unica de perfil operativo:
  - `LAB_MODE=1`: telemetria 5s, status 30s.
  - `LAB_MODE=0`: telemetria 60s, status 300s.
- El firmware reporta en `status` los campos requeridos:
  - `lab_mode`
  - `telemetry_interval_ms`
  - `status_interval_ms`
- Los firmwares MQTT actuales compilaron con la cadencia configurable:
  - `xiao-esp32c3-soil`: SUCCESS
  - `esp32-sht40`: SUCCESS
  - `esp32d-outside`: SUCCESS
- El sensor de suelo implemento downsampling offline:
  - laboratorio: 0-1min cada 10s, 1-3min cada 30s, >3min cada 60s.
  - campo: 0-10min cada 60s, 10-60min cada 5min, >60min cada 15min.
- La recuperacion offline posterior valido que la estrategia conserva trazas compactas:
  - `offline_retained_telemetry_count=18`
  - `offline_compacted_telemetry_count=23`
  - `offline_summary_queue_count=7`
- En retest posterior al drenaje por tandas, el nodo reconecto sin reset watchdog y dreno colas:
  - `mqtt_retry_queue_count=0`
  - `offline_summary_queue_count=0`
  - `offline_recovery_publish_count=7`
  - `offline_summary_dropped_count=0`
- Raspberry valido ingestion y reconstruccion de recuperacion offline:
  - `recovery_summaries=153`
  - `recovery_summary_readings=1071`
  - `reconstructed_readings=1071`

## Evidencia relacionada

- `project/evidence/firmware/HU-FW-OFFLINE-RETENTION-001-build-2026-09-09.md`
- `project/evidence/firmware/HU-FW-OFFLINE-RECOVERY-PROTOCOL-001-build-2026-09-09.md`
- `project/evidence/edge/EN-EDGE-001-raspberry-runtime-validation-2026-09-22.md`
- `project/guides/firmware/offline-retention-adaptive-standard.md`
- `project/contracts/mqtt/offline-recovery-v1.md`

## Criterios de aceptacion

- Firmwares MQTT actuales compilan con defaults de campo: PASS.
- Laboratorio puede mantener telemetria a 5s mediante `LAB_MODE=1`: PASS.
- `status` reporta `lab_mode`, `telemetry_interval_ms` y `status_interval_ms`: PASS.
- Existe estandar de retencion offline adaptativa con payload de resumen: PASS.
- Los descartes se interpretan como perdida de granularidad y quedan visibles en contadores: PASS_WITH_LIMITATIONS.

## Limitaciones

- La retencion sigue siendo volatil; no sobrevive a perdida de energia del microcontrolador.
- La prueba confirma recuperacion offline real, pero no reemplaza una prueba fisica continua de 4-5 horas en campo.
- La granularidad reconstruida por resumen es apta para visualizacion y tendencia, no para auditoria exacta muestra a muestra.

## Decision

Cerrar `HU-FW-OFFLINE-RETENTION-001` como DONE. La continuidad completa de datos queda cubierta por la combinacion firmware recovery + edge SQLite; la persistencia durable en nodo queda como mejora futura.
