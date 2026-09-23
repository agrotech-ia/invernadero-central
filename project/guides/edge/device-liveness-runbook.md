# Laboratorio Edge Device Liveness

Objetivo: detectar desde Raspberry si un sensor ESP esta `online`, `warning`, `critical` u `offline` usando SQLite, sin depender de Serial ni de IP fija del ESP.

## Reglas iniciales de laboratorio

- `online`: ultimo mensaje recibido hace menos de 90 segundos.
- `warning`: ultimo mensaje recibido hace 90 segundos o mas.
- `critical`: ultimo mensaje recibido hace 10 minutos o mas.
- `offline`: ultimo mensaje recibido hace 30 minutos o mas.

## Ejecutar chequeo manual

Desde la raiz del repo:

```bash
python3 tools/edge_liveness_check.py --db var/edge/greenhouse.db
```

Salida esperada:

```text
dev-zfert01-soil-01 online age=12s last_received=... last_sequence=3535 mqtt_connected=True
```

Ver estado completo:

```bash
python3 tools/edge_sqlite_status.py --db var/edge/greenhouse.db
```

## Simular alerta

Para validar transiciones sin esperar 30 minutos se pueden usar umbrales cortos. Durante esta prueba conviene detener temporalmente el timer para que no mezcle umbrales normales con umbrales de laboratorio rapido:

```bash
sudo systemctl stop greenhouse-edge-liveness.timer
```

```bash
python3 tools/edge_liveness_check.py \
  --db var/edge/greenhouse.db \
  --warning-after-s 10 \
  --critical-after-s 20 \
  --offline-after-s 30
```

Al terminar, restaurar el timer normal:

```bash
sudo systemctl start greenhouse-edge-liveness.timer
```

Si no se detiene el timer, puede aparecer una transicion como `offline -> warning` porque el timer normal usa umbrales mas largos.

## Ejecutar como timer systemd

```bash
sudo cp deploy/systemd/greenhouse-edge-liveness.service /etc/systemd/system/
sudo cp deploy/systemd/greenhouse-edge-liveness.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greenhouse-edge-liveness.timer
sudo systemctl start greenhouse-edge-liveness.timer
```

Ver estado:

```bash
systemctl status greenhouse-edge-liveness.timer
journalctl -u greenhouse-edge-liveness.service -n 80
```

## Criterio PASS

- `device_health` tiene una fila por dispositivo.
- El estado cambia a `warning/critical/offline` cuando `last_received_at` envejece.
- `edge_events` guarda eventos `sensor_warning`, `sensor_critical`, `sensor_offline` y `sensor_recovered`.
- `tools/edge_sqlite_status.py` muestra `device_health`.
