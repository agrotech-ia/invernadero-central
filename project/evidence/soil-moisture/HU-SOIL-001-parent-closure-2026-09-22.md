# HU-SOIL-001 - Cierre Parent Sensor Suelo 7-en-1

Fecha local: 2026-09-22

## Resultado

PASS_WITH_LIMITATIONS. La historia parent se cierra porque sus entregables MVP quedaron cubiertos por laboratorios, contrato de datos e ingesta edge.

## Evidencia Cerrada

- `HU-SOIL-LAB-001`: banco de pruebas y evidencia inicial.
- `HU-SOIL-LAB-002`: lectura cruda estable con telemetrias reales.
- `HU-SOIL-LAB-003`: caracterizacion seco/humedo/saturado y extension a 200 ml.
- `HU-SOIL-DATA-001`: contrato MQTT V1 aprobado contra payload real.
- `EN-EDGE-001`: ingesta SQLite, replay/recovery, liveness y visualizacion web validados.

## Conclusiones Tecnicas

- El sensor responde a cambios de humedad de forma coherente.
- EC aumenta con humedad/condicion de muestra.
- NPK no debe interpretarse en seco; P/K aparecen al subir humedad/EC y N aparece claramente en sobresaturacion.
- El mapeo Modbus observado es plausible:
  - `Reg0`: humedad `* 0.1`
  - `Reg1`: temperatura `* 0.1`
  - `Reg2`: EC
  - `Reg3`: pH `* 0.1`
  - `Reg4/5/6`: N/P/K
- El payload MQTT V1 cubre las 7 metricas y casos `replayed=true`.

## Limitaciones Declaradas

- Modelo exacto del sensor sigue pendiente.
- Verificacion formal de voltaje/cableado con multimetro sigue pendiente.
- No hay calibracion agronomica certificada.
- La lectura extendida a 200 ml se trata como sobresaturacion/extension, no como recomendacion agronomica.
- NPK requiere validacion adicional si se usara para decisiones agronomicas.
- Resiliencia MQTT/config/OTA quedan en HUs firmware separadas.

## Decision

Cerrar `HU-SOIL-001` como parent MVP. Las limitaciones quedan como follow-ups y no bloquean el avance al dashboard con telemetria real ni al bloque firmware de campo.

## Follow-ups

- Validar modelo exacto y voltaje real del sensor.
- Crear protocolo de calibracion agronomica si el producto decide usar NPK para recomendaciones.
- Cerrar HUs firmware de resiliencia/configuracion/OTA.
