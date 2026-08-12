# HU-008 — Consolidar inventario técnico y estado real del proyecto

## 1. Información general

**ID:** HU-008
**Título:** Consolidar inventario técnico y estado real del proyecto
**Épica:** EP-001 — Foundation / Project Recovery
**Dominio:** Knowledge / Hardware / Firmware / Platform / Data
**Owner Role:** Technical Writer / Knowledge Manager
**Accountable:** Project Manager
**Reviewer:** Solution Architect
**Supporting Roles:** Hardware, Firmware, Backend, Data, DevOps, QA, Frontend, AI/ML
**Prioridad:** P0
**Target:** FOUNDATION
**Tipo:** ENABLER
**Effort:** M
**Risk:** MEDIUM
**Estado:** REFINEMENT

---

# 2. Historia

**Como** responsable del proyecto,

**quiero** consolidar el estado real de todos los componentes físicos y digitales existentes,

**para** reutilizar correctamente el trabajo realizado, detectar brechas frente al MVP y construir el nuevo backlog desde evidencia y no desde supuestos.

---

# 3. Fuentes de evidencia

La recuperación utilizará, en este orden:

```
1. green-house / qa
2. agrotechia-web-ui
3. hardware físico disponible
4. pruebas realizadas
5. documentación existente
6. conversaciones históricas
7. conocimiento del propietario

```

Una conversación no convierte automáticamente algo en hecho técnico validado.

---

# 4. Estado recuperado — Arquitectura

Existe una arquitectura inicial:

```
                         WEB / CLIENT
                              │
                              ▼
                       RASPBERRY PI 5
                 ┌────────────┼─────────────┐
                 │            │             │
               MQTT          API        PostgreSQL
                 │                          +
                 │                      TimescaleDB
                 │
       ┌─────────┼───────────────┐
       ▼         ▼               ▼
    ESP32      ESP32           ESP32
   Climate     Soil          Water/Process

                              ▲
                              │ REST metadata
                              │
                        VISION PC
                              │
                       USB CAMERAS
                              │
                           YOLO

```

La arquitectura existente es compatible conceptualmente con HU-007.

No se considera todavía arquitectura final aprobada.

Deberá pasar posteriormente por Architecture Review.

---

# 5. Infraestructura Edge

## Raspberry Pi 5

**Estado:** PARCIALMENTE IMPLEMENTADO / PROBADO

Existe:

- Raspberry Pi 5 definida como gateway;
- Mosquitto;
- configuración MQTT;
- scripts de instalación;
- prueba MQTT local;
- logger MQTT;
- almacenamiento JSONL inicial;
- estructura para PostgreSQL + TimescaleDB.

### Evidencia conocida

ESP32 → WiFi → MQTT → Raspberry ha sido probado.

### Pendiente

Validar:

```
PostgreSQL + TimescaleDB real
        ↓
MQTT ingestor
        ↓
persistencia

```

---

# 6. Nodo ambiental interno

## Hardware

```
Seeed XIAO ESP32-C3
+
SHT40

```

**Estado:** PROBADO

Cableado documentado:

```
SHT40
VCC → 3V3
GND → GND
SDA → D4 / GPIO6
SCL → D5 / GPIO7

```

Existe firmware PlatformIO.

Existe comunicación WiFi.

Existe publicación MQTT probada.

---

# 7. Distribución ambiental planeada

Actualmente el inventario define:

```
z-grow-01
  2 × SHT40 nivel planta

z-grow-02
  2 × SHT40 nivel planta
  2 × SHT40 techo

z-grow-03
  2 × SHT40 nivel planta

```

Total planeado interior:

```
8 × SHT40

```

Esta cantidad se considera:

**PLANNED / INVENTORIED**

y no automáticamente:

**INSTALLED**

La instalación física deberá verificarse.

---

# 8. Nodo climático exterior

Arquitectura planeada:

```
ESP32 Dev Module
      │
      ├── SHT40
      │
      └── MAX485
             │
           RS485
             │
      Solar Radiation Sensor

```

Existe firmware específico:

```
esp32d-outside/

```

Existe configuración Modbus parametrizable.

### Estado

```
SHT40 exterior → IMPLEMENTATION EXISTS
RS485 stack     → IMPLEMENTATION EXISTS
Sensor solar    → REQUIRES FIELD VALIDATION

```

---

# 9. Nodo de suelo

Inventario:

```
DEVICE
dev-zfert01-soil-01

SENSOR
sns-zfert01-soil7in1-01

```

Sensor previsto:

```
7-in-1 RS485

```

Variables:

```
soil_moisture_pct
soil_temperature_c
soil_ph
soil_ec_us_cm
soil_n_mg_kg
soil_p_mg_kg
soil_k_mg_kg

```

### Estado

Hardware conocido/adquirido previamente.

Conexión RS485/MAX485 trabajada.

Debe clasificarse provisionalmente:

```
INTEGRATION IN PROGRESS

```

hasta realizar prueba end-to-end reproducible.

---

# 10. Nodo agua/proceso

Inventario existente:

```
dev-zfert01-water-01

```

Sensores definidos:

```
flow sensor
water EC
water pH

```

Métricas previstas:

```
water_flow_l_min
water_volume_total_l
water_ec_us_cm
water_ph

```

### Estado

```
ARCHITECTURE DEFINED
HARDWARE PARTIALLY AVAILABLE
INTEGRATION PENDING

```

El sensor pH requiere además proceso formal de:

```
storage
hydration
calibration
validation
maintenance

```

antes de tratar sus datos como confiables.

---

# 11. Actuadores

Inventario actual:

```
4 × bombas peristálticas

1 × bomba mezcla

1 × bomba principal

1 × válvula riego

1 × válvula nebulización

```

IDs ya definidos.

### Estado

```
PLANNED / INVENTORIED

```

No se consideran todavía automatizados.

El roadmap existente correctamente propone:

```
ACTUATOR
    ↓
TEST WITHOUT CRITICAL LOAD
    ↓
LOG ACTION
    ↓
VALIDATE
    ↓
AUTOMATIC RULE

```

Esto se mantiene alineado con HU-007.

---

# 12. MQTT

Existe contrato MQTT V1.

Topics:

```
greenhouse/{greenhouse}/zone/{zone}/device/{device}/telemetry

greenhouse/{greenhouse}/zone/{zone}/device/{device}/status

greenhouse/{greenhouse}/zone/{zone}/device/{device}/event

```

### Estado

```
CONTRACT DEFINED
BROKER TESTED
ESP32 PUBLISH TESTED

```

Esto constituye uno de los activos técnicos más maduros del proyecto.

---

# 13. Contrato de telemetría

Ya existe un modelo que contempla:

```
schema_version
greenhouse_id
zone_id
device_id
device_time
sequence
readings[]

```

y cada reading:

```
sensor_id
metric
value
unit

```

Esto se reutilizará.

Pero deberá evolucionarse para HU-007 porque allí definimos explícitamente calidad de lectura.

Debe evaluarse incorporar:

```
quality
error/status
ingested_at

```

sin romper compatibilidad innecesariamente.

---

# 14. Base de datos

Existe implementación inicial:

```
PostgreSQL
+
TimescaleDB

```

con:

```
schema_v1.sql
seed_v1.sql
bootstrap.sh
docker-compose.yml

```

El modelo contempla:

- zonas;
- dispositivos;
- sensores;
- actuadores;
- cámaras;
- telemetría;
- estados;
- eventos;
- riego;
- dosificación;
- visión.

### Estado

```
DESIGNED
IMPLEMENTATION EXISTS
RUNTIME VALIDATION REQUIRED

```

No debe rediseñarse desde cero.

Debe revisarse contra HU-001 → HU-007.

---

# 15. Visión artificial

Existe un subsistema independiente:

```
PC
 │
USB Cameras
 │
Capture Service
 │
Local Image Storage
 │
YOLO
 │
Metadata
 │
REST
 ▼
Raspberry

```

Existe código Python inicial.

Existe configuración.

Existen contratos REST.

Inventario:

```
cam-zgrow01-01
cam-zgrow03-01

```

### Estado

```
SOFTWARE PROTOTYPE EXISTS
FIELD VALIDATION REQUIRED
MODEL VALIDATION PENDING

```

Por HU-007:

```
AI ≠ MVP blocker

```

por lo que esta línea podrá avanzar en paralelo sin bloquear MVP.

---

# 16. Imágenes

Decisión existente:

```
NO images over MQTT

```

Las imágenes:

```
CAMERA
 ↓
VISION PC
 ↓
LOCAL STORAGE

```

y únicamente metadata/inferencias llegan a Raspberry.

Esta decisión deberá ser revisada posteriormente por Architecture Agent, pero es técnicamente coherente y se preserva provisionalmente.

---

# 17. Frontend existente

Repositorio:

```
agrotechia-web-ui

```

Existe:

- React;
- Vite;
- Tailwind;
- estructura modular;
- tests;
- linting;
- SonarQube;
- CI/CD;
- infraestructura AWS;
- landing;
- dashboard conceptual.

### Estado

```
REUSABLE FOUNDATION

```

Pero:

```
dashboard data = simulated

```

Por tanto:

```
UI EXISTS
REAL DATA INTEGRATION DOES NOT

```

---

# 18. Funcionalidades conceptuales del frontend

El frontend existente ya contempla:

```
clima
suelo
riego/fertirriego
visión
productividad
recursos
offline

```

Esto coincide ampliamente con la nueva visión.

No debe eliminarse automáticamente.

Debe hacerse:

```
UX/Product Review
       ↓
reuse / refactor / discard

```

por componente.

---

# 19. Inventario lógico recuperado

El proyecto ya tiene definido:

```
1 greenhouse
5 zones
11 devices
14 sensors
8 actuators
2 cameras

```

aproximadamente según inventario V1.

Estos valores representan inventario lógico previsto, no necesariamente hardware físicamente instalado.

---

# 20. Estados oficiales del inventario

Desde HU-008 se utilizarán:

```
UNKNOWN
PLANNED
AVAILABLE
ASSEMBLED
CONNECTED
TESTED
INTEGRATED
INSTALLED
OPERATIONAL
FAILED
RETIRED

```

Esto evita expresiones ambiguas como:

```
"creo que ya lo probamos"

```

---

# 21. Estado técnico resumido

## Firmware ambiental

```
TESTED

```

## WiFi ESP32

```
TESTED

```

## MQTT ESP32 → Raspberry

```
TESTED

```

## MQTT broker

```
TESTED

```

## MQTT logging

```
IMPLEMENTED / TESTED

```

## PostgreSQL/TimescaleDB

```
IMPLEMENTATION EXISTS
VALIDATION REQUIRED

```

## Soil RS485

```
INTEGRATION IN PROGRESS

```

## Exterior solar RS485

```
IMPLEMENTATION EXISTS
VALIDATION REQUIRED

```

## Water pH

```
AVAILABLE / INTEGRATION PENDING

```

## Water EC

```
PLANNED / VERIFY HARDWARE

```

## Flow

```
PLANNED / VERIFY HARDWARE

```

## Actuation

```
PLANNED

```

## Vision

```
SOFTWARE PROTOTYPE

```

## Web

```
SOFTWARE FOUNDATION

```

## Real dashboard

```
NOT INTEGRATED

```

---

# 22. Información que NO puede inferirse del repositorio

El repositorio no demuestra de forma suficiente:

```
cantidad física real disponible
estado físico de cada componente
sensores dañados
cableado actualmente montado
fuentes disponibles
relés disponibles
bombas compradas
válvulas compradas
gabinetes
conectores
cables
tubería
red física
estado actual de Raspberry
estado actual de cámaras

```

Esto requiere inspección física.

---

# 23. Gap Inventory

HU-008 generará un segundo inventario:

```
EXPECTED
vs
AVAILABLE
vs
WORKING
vs
MISSING

```

Ejemplo:

```
SHT40
Expected: 9
Available: ?
Working: ?
Installed: ?
Missing: ?

```

---

# 24. Reconciliation

Cada componente del repositorio deberá compararse con hardware físico.

Resultado:

```
repository inventory
       +
physical inventory
       ↓
reconciliation
       ↓
master inventory v2

```

---

# 25. Información física pendiente

Antes de cerrar HU-008 necesitamos confirmar principalmente:

### Compute

- Raspberry Pi 5 disponible y operativa;
- almacenamiento;
- PC destinado a visión.

### Controllers

- cantidad real XIAO ESP32-C3;
- cantidad real ESP32 Dev Module.

### Sensors

- cantidad SHT40;
- sensor suelo 7-en-1;
- sensor radiación;
- pH agua;
- EC agua;
- caudalímetro.

### Actuators

- bombas peristálticas;
- bomba mezcla;
- bomba principal;
- válvulas;
- relés/SSR.

### Power

- fuentes 12 V;
- fuentes 5 V;
- convertidores;
- protecciones.

### Communication

- MAX485;
- cable RS485;
- conectores.

### Vision

- PC;
- cámaras;
- soportes.

---

# 26. Clasificación de reutilización

Todo software existente será marcado:

```
KEEP
KEEP_AND_REFACTOR
MIGRATE
REPLACE
ARCHIVE
UNKNOWN

```

No eliminaremos trabajo simplemente por haber cambiado la planificación.

---

# 27. Principio de recuperación

> El objetivo no es adaptar la nueva arquitectura a todo lo viejo ni desechar lo viejo para construir todo de nuevo.

Se evaluará cada activo contra las baselines HU-001 → HU-007.

---

# 28. Criterios de decisión

Un componente existente se mantiene cuando:

```
ALIGNED
+
WORKING
+
MAINTAINABLE
+
USEFUL FOR MVP

```

Si no cumple, se genera trabajo explícito.

---

# 29. Gherkin

```
Feature: Recuperación del estado técnico del proyecto

  Scenario: Encontrar un componente documentado
    Given que un dispositivo existe en el inventario del repositorio
    When se realiza el inventario físico
    Then debe registrarse su estado real
    And no debe asumirse que está disponible solamente porque aparece documentado

  Scenario: Encontrar hardware no documentado
    Given que existe hardware físico
    And no aparece en el inventario
    When se realiza la reconciliación
    Then debe incorporarse al inventario maestro
    And debe determinarse su función potencial

  Scenario: Encontrar software existente
    Given que existe una implementación anterior
    When se compara con las baselines del proyecto
    Then debe clasificarse como Keep, Refactor, Migrate, Replace, Archive o Unknown

  Scenario: Encontrar una prueba anterior
    Given que documentación indica que un componente fue probado
    When existe evidencia suficiente
    Then su estado puede registrarse como Tested
    But no debe registrarse como Operational si no está actualmente desplegado

  Scenario: Finalizar recuperación
    Given que repositorios y hardware físico fueron revisados
    When se completa la reconciliación
    Then debe existir un inventario maestro V2
    And deben identificarse las brechas del MVP

```

---

# 30. Criterios de aceptación

HU-008 estará completa cuando:

- ambos repositorios estén revisados;
- arquitectura existente esté documentada;
- firmware existente esté clasificado;
- infraestructura Raspberry esté clasificada;
- base de datos esté clasificada;
- frontend esté clasificado;
- visión esté clasificada;
- inventario lógico esté recuperado;
- inventario físico esté confirmado;
- cada componente tenga estado;
- las diferencias estén registradas;
- exista Master Inventory V2;
- las brechas frente a HU-007 estén identificadas.

---

# 31. Definition of Done

HU-008 NO podrá cerrarse solamente con la revisión GitHub.

Falta:

```
PHYSICAL INVENTORY

```

Una vez completado:

```
GitHub
+
Physical Inventory
+
Previous Evidence
       ↓
MASTER INVENTORY V2
       ↓
MVP GAP ANALYSIS
       ↓
BACKLOG

```

---

# 32. Decisiones propuestas

## DEC-062 — Recuperar antes de reconstruir

Todo activo existente será evaluado antes de reemplazarse.

## DEC-063 — QA como referencia técnica actual

Mientras se realiza la recuperación, `green-house/qa` representa la rama con el estado técnico existente relevante.

## DEC-064 — Estados normalizados de hardware

El inventario utilizará estados explícitos desde UNKNOWN hasta OPERATIONAL.

## DEC-065 — Inventario documental no equivale a inventario físico

Un dispositivo documentado no se considera físicamente disponible hasta confirmarlo.

## DEC-066 — Arquitectura existente se preserva provisionalmente

La arquitectura Raspberry + ESP32 + Vision PC será considerada baseline técnica candidata y será sometida posteriormente a Architecture Review.

## DEC-067 — Reutilización del frontend

`agrotechia-web-ui` será tratado como activo reutilizable y no como producto descartable.

## DEC-068 — Contratos V1 como punto de partida

Los contratos MQTT/REST existentes serán evolucionados en lugar de reemplazados sin justificación.

## DEC-069 — Base de datos existente como punto de partida

El esquema PostgreSQL/TimescaleDB existente deberá revisarse contra las nuevas baselines antes de diseñar uno nuevo.