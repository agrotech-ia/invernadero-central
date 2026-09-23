# Laboratorio Edge Device Health Web Export

Objetivo: publicar un snapshot JSON de `device_health` desde la Raspberry para que la web pueda mostrar estado real de sensores sin conectar directamente el frontend a SQLite.

Arquitectura validada:

```text
ESP -> Mosquitto Raspberry -> SQLite Raspberry -> JSON HTTP Raspberry -> Web
```

## Export manual

Desde la raiz de `invernadero-central`:

```bash
python3 tools/edge_export_device_health.py \
  --db var/edge/greenhouse.db \
  --out /home/chuchosam/greenhouse/edge-public/device-health.json
```

Servir el JSON para pruebas manuales:

```bash
python3 tools/edge_health_http_server.py \
  --directory /home/chuchosam/greenhouse/edge-public \
  --host 0.0.0.0 \
  --port 8088
```

Validar desde otro computador de la red:

```bash
curl http://192.168.1.15:8088/device-health.json
```

## Export automatico

```bash
sudo cp deploy/systemd/greenhouse-edge-health-export.service /etc/systemd/system/
sudo cp deploy/systemd/greenhouse-edge-health-export.timer /etc/systemd/system/
sudo cp deploy/systemd/greenhouse-edge-health-http.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greenhouse-edge-health-export.timer
sudo systemctl start greenhouse-edge-health-export.timer
sudo systemctl enable greenhouse-edge-health-http.service
sudo systemctl start greenhouse-edge-health-http.service
```

Verificar:

```bash
systemctl status greenhouse-edge-health-export.timer --no-pager -l
journalctl -u greenhouse-edge-health-export.service -n 80 --no-pager -l
systemctl status greenhouse-edge-health-http.service --no-pager -l
journalctl -u greenhouse-edge-health-http.service -n 80 --no-pager -l
```

## Web

La web lee por defecto:

```text
/edge/device-health.json
```

Cuando la web corre en este computador y la Raspberry esta en `192.168.1.15`, arrancar Vite asi:

```bash
VITE_EDGE_HEALTH_URL=http://192.168.1.15:8088/device-health.json npm run dev
```

Ruta esperada:

```text
/project/dispositivos
```

## Criterio PASS

- `curl http://192.168.1.15:8088/device-health.json` responde JSON.
- El JSON contiene `devices`, `counts` y `recent_events`.
- La web muestra estado `online/warning/critical/offline` y ultimo visto.
