# MQTT Gap Logger Runbook

Estado: DRAFT  
Fecha: 2026-09-01  
Relacionado: `HU-FW-MQTT-RESILIENCE-001`

## Objetivo

Capturar telemetria MQTT en Raspberry con timestamp local y detectar huecos por `device_id + sequence`.

## Comando recomendado

Desde el repo `invernadero-central` en la Raspberry:

```bash
mosquitto_sub -h localhost -t 'greenhouse/#' -v \
  | python3 tools/mqtt_gap_logger.py \
      --out project/evidence/soil-moisture/mqtt-received-$(date -u +%Y%m%dT%H%M%SZ).jsonl \
      --gaps-out project/evidence/soil-moisture/mqtt-gaps-$(date -u +%Y%m%dT%H%M%SZ).jsonl
```

## Salidas

- `mqtt-received-*.jsonl`: cada mensaje recibido con `received_at`, `topic` y `payload` original.
- `mqtt-gaps-*.jsonl`: eventos `telemetry_gap_detected`.

Ejemplo de gap:

```json
{
  "event_type": "telemetry_gap_detected",
  "received_at": "2026-09-02T02:35:01.275610+00:00",
  "device_id": "dev-zfert01-soil-01",
  "topic": "greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry",
  "from_sequence": 42,
  "to_sequence": 49,
  "missing_count": 6
}
```

## Validacion de laboratorio

1. Iniciar el logger antes de encender o reiniciar el nodo.
2. Confirmar que llegan `status` y `telemetry`.
3. Apagar Mosquitto o bloquear temporalmente el puerto `1883`.
4. Esperar al menos 3 intervalos de telemetria.
5. Restaurar Mosquitto.
6. Verificar si llegan payloads con `replayed=true`.
7. Revisar `mqtt-gaps-*.jsonl` y compararlo contra los contadores del `status`.

## Interpretacion

- Si hay gaps y `mqtt_publish_failed_count` sube, hubo perdida o reintento detectado por firmware.
- Si hay gaps pero los contadores del dispositivo no suben, puede haber captura incompleta, reinicio del subscriber o perdida entre broker y logger.
- Si `dropped_telemetry_count` sube, la cola volatil se lleno y el firmware descarto lecturas antiguas.

