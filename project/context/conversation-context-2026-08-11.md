# Contexto operativo de conversacion - 2026-08-11

Este documento guarda contexto relevante identificado durante la lectura inicial de repositorios.
No modifica las HU congeladas ni reemplaza decisiones formales. Sirve como memoria operativa
para continuar el trabajo sin depender del chat.

## Repositorios relacionados

### Repositorio central

Ruta local:

```text
/home/chuchosam/Documentos/github/invernadero-central
```

Rol:

- Fuente de gobierno del proyecto.
- Contiene baseline local V1, HU congeladas, decisiones, agentes, backlog, inventario fisico V2,
  roadmap, matriz V&V y arquitectura objetivo.

Observacion git:

- Durante la lectura inicial, todos los archivos aparecian como `untracked`.
- Este repo debe convertirse en fuente de verdad versionada antes de automatizar persistencia final.

### Repositorio de sensores, edge y datos

Ruta local:

```text
/home/chuchosam/Documentos/github/invernadero/green-house
```

Rol:

- Contiene trabajos adelantados reales de sensores, firmware, Raspberry, MQTT, base de datos,
  vision y contratos de datos.

Rama observada:

```text
feauture/test-chucho
```

Estado git observado:

- Sin cambios pendientes al momento de lectura.

Elementos importantes existentes:

- Firmware SHT40 en `esp32-sht40/`.
- Firmware nodo exterior en `esp32d-outside/`.
- Firmware de suelo 7-en-1 RS485/Modbus en `xiao-esp32c3-soil/`.
- Configuracion y scripts de Raspberry/Mosquitto en `raspberry-pi/`.
- Logger MQTT JSONL en `raspberry-pi/mqtt_logger.py`.
- Esquema PostgreSQL + TimescaleDB en `db/schema_v1.sql`.
- Seed de inventario en `db/seed_v1.sql`.
- Contratos MQTT/REST en `docs/data-contracts.md`.
- Inventario logico V1 en `docs/device-inventory.md`.
- Flujo del sistema en `docs/system-flow.md`.
- Servicio/prototipo de vision en `vision/pc/`.

### Repositorio web

Ruta local:

```text
/home/chuchosam/Documentos/github/agrotechia-web-ui
```

Rol:

- Contiene landing React + Vite + Tailwind para AgroTechIA.
- Incluye un demo visual de dashboard con datos simulados.

Rama observada:

```text
main
```

Estado git observado:

- `README.md` aparecia modificado al momento de lectura.
- Ese cambio debe tratarse como trabajo existente del usuario y no revertirse sin instruccion explicita.

Elementos importantes existentes:

- App principal en `src/App.jsx`.
- Datos simulados en `src/data/mockDashboard.js`.
- Secciones de landing en `src/sections/`.
- Componentes reutilizables en `src/components/`.
- Scripts disponibles: `dev`, `build`, `preview`, `lint`, `test`, `audit`, `sonar`.

## Contexto tecnico consolidado

MVP objetivo definido en el repo central:

```text
REAL SENSOR -> TELEMETRY -> STORAGE -> WEB -> RULE/ALERT -> CONTROLLED ACTION -> TRACE
```

Arquitectura objetivo:

- ESP32/XIAO leen sensores y publican telemetria por MQTT.
- Raspberry Pi 5 actua como edge gateway:
  - Mosquitto
  - ingestion
  - PostgreSQL + TimescaleDB
  - API
  - rules/events
- Web UI consume datos reales desde API.
- PC Lenovo/vision captura imagenes, guarda archivos localmente y envia metadata/inferencias por REST.
- Las imagenes no deben viajar por MQTT.

## n8n local

El usuario informa que n8n ya esta implementado localmente.

Implicacion operativa:

- El trabajo de agentes puede comenzar sobre la instancia local existente.
- El foco ya no debe ser instalar n8n desde cero, sino configurar/orquestar los agentes versionados
  desde el repositorio central.
- `EN-AGENT-001` debe interpretarse como bootstrap funcional de la plataforma multiagente local,
  usando n8n ya disponible.
- La ejecucion debe respetar el flujo definido en `n8n/docs/architecture.md`:
  - cargar reglas del proyecto;
  - cargar registro de agentes;
  - enrutar con Orchestrator;
  - construir contexto minimo;
  - invocar agente especializado;
  - pasar por Reviewer;
  - solicitar aprobacion humana cuando corresponda;
  - persistir borrador/final en repositorio;
  - actualizar conocimiento.

Primer caso de aceptacion para agentes:

```text
Construir backlog de validacion del sensor de suelo 7-en-1
```

Debe reconocer que el sensor de suelo esta `OPERATIONAL / VALIDATION PENDING`, no reimplementar
RS485/firmware existente, proponer tareas de validacion, generar materiales/procurement y producir
un borrador revisable.

## Sensor de suelo 7-en-1

El repo central indica que el sensor de suelo 7-en-1 esta `OPERATIONAL`, pero con validacion pendiente.
El repo `green-house` confirma que ya existe firmware operativo en:

```text
/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil
```

Capacidades observadas:

- Lectura RS485/Modbus usando MAX485.
- Escaneo automatico de baudios `4800`, `9600`, `19200`.
- Escaneo de modos seriales `8N1`, `8E1`, `8O1`.
- Escaneo de IDs Modbus `1..10`.
- Lectura de holding registers o input registers.
- Payloads de telemetria/status con `schema_version: 1.0`.
- MQTT opcional mediante `MQTT_ENABLED`.

Metricas publicadas:

- `soil_moisture_pct`
- `soil_temperature_c`
- `soil_ph`
- `soil_ec_us_cm`
- `soil_n_mg_kg`
- `soil_p_mg_kg`
- `soil_k_mg_kg`

Regla operativa:

- No reimplementar el sensor de suelo por defecto.
- El siguiente trabajo debe enfocarse en validacion, caracterizacion, calibracion, evidencia y V&V.

Riesgo tecnico observado:

- En el firmware de suelo, `device_time()` usa `millis() / 1000`.
- Para persistencia historica confiable, el gateway debe agregar `ingested_at` y/o se debe definir
  sincronizacion de tiempo del dispositivo antes de depender de `device_time` como timestamp real.

## Contratos de datos existentes

Topicos MQTT V1:

```text
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/telemetry
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/status
greenhouse/{greenhouse_id}/zone/{zone_id}/device/{device_id}/event
```

Endpoints REST previstos para vision:

```text
POST /api/v1/images/captures
POST /api/v1/images/inferences
```

Reglas:

- Cada mensaje debe incluir `schema_version`.
- La Raspberry agrega `ingested_at` al persistir.
- Una captura puede generar muchas inferencias.
- Imagenes por filesystem/local storage; metadata e inferencias por REST.

## Web actual

La web actual es una landing con dashboard demo.

Dato importante:

- `src/data/mockDashboard.js` contiene datos simulados.
- Todavia no hay evidencia observada de conexion a API real ni a TimescaleDB.

Brecha principal:

- Falta el puente entre telemetria real persistida y dashboard web:
  - ingesta MQTT -> PostgreSQL/TimescaleDB robusta;
  - API de consulta;
  - reemplazo progresivo de mocks en frontend;
  - estados de carga/error/desconexion;
  - definicion de metricas agregadas para vista web.

## Backlog relacionado

Items del repo central que se conectan directamente con estos repos:

- `EN-AGENT-001`: Bootstrap plataforma multiagente local en n8n.
- `EN-QA-001`: Framework V&V y persistencia de evidencia.
- `HU-SOIL-001`: Validar y caracterizar sensor de suelo 7-en-1.
- `EN-EDGE-001`: Validar runtime Raspberry MQTT->DB.
- `HU-WEB-001`: Integrar dashboard con telemetria real.
- `EXP-E2E-001`: Ejecutar prueba end-to-end del MVP.

## Proximo trabajo recomendado

Secuencia conservadora sugerida:

1. Versionar el contexto operativo en el repo central.
2. Configurar en n8n el flujo minimo de `EN-AGENT-001` usando agentes YAML del repo central.
3. Ejecutar el primer caso de aceptacion: backlog de validacion del sensor de suelo 7-en-1.
4. Crear o refinar backlog de validacion para `HU-SOIL-001` sin reimplementar firmware.
5. Levantar `EN-EDGE-001`: ingesta MQTT hacia PostgreSQL/TimescaleDB usando contratos V1.
6. Definir API minima para dashboard real.
7. Convertir una parte de `agrotechia-web-ui` de mock a datos reales.
8. Ejecutar una prueba E2E trazable desde sensor real hasta visualizacion web.

## Notas de gobernanza

- Las HU `HU-001` a `HU-009` estan congeladas.
- No modificar baselines silenciosamente.
- Compras, control fisico, despliegues criticos y gasto pagado requieren aprobacion humana.
- Claims de mercado deben respetar `project/market/claim-policy.yaml`.
- Conversacion no equivale a documentacion; este archivo existe para persistir contexto operativo.
