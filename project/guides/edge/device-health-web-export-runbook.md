# Laboratorio Edge Device Health Web Export

Objetivo: publicar un snapshot JSON de `device_health` para que la web pueda mostrar estado real de sensores sin conectar directamente el frontend a SQLite.

## Export manual

Desde la raiz de `invernadero-central`:

```bash
python3 tools/edge_export_device_health.py \
  --db var/edge/greenhouse.db \
  --out /home/chuchosam/greenhouse/agrotechia-web-ui/public/edge/device-health.json
```

## Export automatico

```bash
sudo cp deploy/systemd/greenhouse-edge-health-export.service /etc/systemd/system/
sudo cp deploy/systemd/greenhouse-edge-health-export.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greenhouse-edge-health-export.timer
sudo systemctl start greenhouse-edge-health-export.timer
```

Verificar:

```bash
systemctl status greenhouse-edge-health-export.timer --no-pager -l
journalctl -u greenhouse-edge-health-export.service -n 80 --no-pager -l
```

## Web

La web lee:

```text
/edge/device-health.json
```

Ruta esperada:

```text
/project/dispositivos
```

## Criterio PASS

- El archivo `public/edge/device-health.json` existe en el repo web.
- El JSON contiene `devices`, `counts` y `recent_events`.
- La web muestra estado `online/warning/critical/offline` y ultimo visto.
