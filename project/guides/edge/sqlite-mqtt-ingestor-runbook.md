# Laboratorio Edge MQTT -> SQLite

Objetivo: persistir en Raspberry los mensajes MQTT del invernadero usando SQLite hoy, con modelo compatible para migrar a PostgreSQL sin cambiar el protocolo MQTT ni la logica de reconstruccion.

## Arquitectura

- Mosquitto sigue siendo el broker.
- `mosquitto_sub -v` entrega cada mensaje como `topic payload`.
- `python3 -m edge.ingestor.main` consume stdin, guarda payload crudo y normaliza datos.
- SQLite queda en `var/edge/greenhouse.db` para laboratorio.
- PostgreSQL queda preparado como migracion equivalente en `edge/storage/migrations/postgres/001_init.sql`.

## Ejecutar en Raspberry

Desde la raiz del repo:

```bash
mosquitto_sub -h localhost -t 'greenhouse/#' -v \
  | python3 -m edge.ingestor.main --db var/edge/greenhouse.db --print-stats-every 10
```

Dejar corriendo esa terminal durante la prueba. En otra terminal se puede mirar Mosquitto o reiniciar el broker.

## Ejecutar como servicio systemd

Para que Raspberry lo levante automaticamente y reinicie el proceso si falla:

```bash
sudo cp deploy/systemd/greenhouse-edge-ingestor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greenhouse-edge-ingestor
sudo systemctl start greenhouse-edge-ingestor
```

Ver estado:

```bash
systemctl status greenhouse-edge-ingestor
```

Ver logs:

```bash
journalctl -u greenhouse-edge-ingestor -f
```

Detener para mantenimiento:

```bash
sudo systemctl stop greenhouse-edge-ingestor
```

## Que se guarda

- `mqtt_messages`: mensaje original completo con `received_at`, topic y payload JSON.
- `telemetry_readings`: lecturas reales o replayed del sensor, sin duplicar por `device_id + sequence + metric`.
- `recovery_summaries`: ventanas compactadas offline recibidas en `/telemetry/recovery`.
- `recovery_summary_readings`: estadisticos `avg/min/max/first/last` por metrica.
- `reconstructed_readings`: punto visual reconstruido en el centro de la ventana, con `quality=reconstructed_from_summary`.
- `edge_events`: gaps detectados y gaps cubiertos por resumen.
- `device_liveness`: ultimo visto por dispositivo.

## Prueba recomendada

1. Borrar base de laboratorio si se quiere una corrida limpia:

```bash
rm -f var/edge/greenhouse.db var/edge/greenhouse.db-wal var/edge/greenhouse.db-shm
```

2. Iniciar ingestor:

```bash
mosquitto_sub -h localhost -t 'greenhouse/#' -v \
  | python3 -m edge.ingestor.main --db var/edge/greenhouse.db --print-stats-every 10
```

3. Confirmar que entran telemetrias normales.

4. Detener Mosquitto entre 3 y 5 minutos para generar cola y resumen offline:

```bash
sudo systemctl stop mosquitto
```

5. Restaurar Mosquitto:

```bash
sudo systemctl start mosquitto
```

6. Esperar a que el firmware publique replay y recovery.

7. Consultar conteos:

```bash
sqlite3 var/edge/greenhouse.db \
  "select 'mqtt_messages', count(*) from mqtt_messages
   union all select 'telemetry_readings', count(*) from telemetry_readings
   union all select 'recovery_summaries', count(*) from recovery_summaries
   union all select 'reconstructed_readings', count(*) from reconstructed_readings
   union all select 'edge_events', count(*) from edge_events;"
```

Si `sqlite3` no esta instalado, usar la herramienta Python incluida:

```bash
python3 tools/edge_sqlite_status.py --db var/edge/greenhouse.db
```

8. Validar recuperacion:

```bash
sqlite3 var/edge/greenhouse.db \
  "select device_id, recovery_id, sequence_start, sequence_end, sample_count, quality
   from recovery_summaries
   order by id desc
   limit 10;"
```

## Criterio PASS

- `mqtt_messages` sube con cada mensaje recibido.
- `telemetry_readings` contiene datos `raw` y/o `raw_replayed`.
- `recovery_summaries` tiene al menos una fila despues de reconectar.
- `reconstructed_readings` tiene puntos con `quality=reconstructed_from_summary`.
- `device_liveness` muestra `last_received_at` reciente para el sensor.

## Evidencia para cerrar HU

Guardar en evidencia:

- Salida de `systemctl status greenhouse-edge-ingestor`.
- Salida de `python3 tools/edge_sqlite_status.py --db var/edge/greenhouse.db`.
- Fragmento de `journalctl -u greenhouse-edge-ingestor -n 80`.
- Resultado de prueba Mosquitto off/on con al menos un `recovery_summaries` o, si la desconexion fue corta, telemetrias `raw_replayed`.

## Migracion futura a PostgreSQL

La migracion debe ser transparente para el flujo:

- Mantener el mismo parseo MQTT.
- Mantener las mismas tablas logicas y campos de calidad.
- Cambiar `SqliteStorage` por un `PostgresStorage` con los mismos metodos.
- Aplicar `edge/storage/migrations/postgres/001_init.sql`.
- La UI y analitica deben consultar `telemetry_readings` y `reconstructed_readings` sin depender del motor.
