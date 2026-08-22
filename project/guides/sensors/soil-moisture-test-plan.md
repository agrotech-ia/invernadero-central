# Guia de pruebas - sensor de suelo 7-en-1

Estado: DRAFT  
Fecha: 2026-08-22  
Backlog parent: HU-SOIL-001  
Ruta web propuesta: `/project/guides/sensors/soil-moisture-test-plan`

## Objetivo

Planear y ejecutar el primer ciclo verificable de pruebas del sensor de suelo 7-en-1, dejando evidencia suficiente para decidir si el sensor puede integrarse al flujo SENSOR -> MQTT -> STORAGE -> WEB.

## Alcance

Incluye:

- Preparar banco de pruebas fisico y lista de materiales.
- Validar alimentacion, conexion y lectura cruda.
- Registrar lecturas en condiciones controladas de suelo seco, humedo y saturado.
- Definir evidencia minima para V&V.
- Preparar el siguiente paso hacia MQTT, persistencia y visualizacion web.

No incluye:

- Automatizar riego.
- Cerrar una calibracion agronomica definitiva.
- Ejecutar control fisico sin aprobacion humana.
- Marcar HU-SOIL-001 como DONE.

## Materiales

Minimos:

- Sensor de suelo 7-en-1.
- Raspberry Pi o microcontrolador usado por el proyecto.
- Fuente de alimentacion compatible con el sensor.
- Convertidor RS485/USB o interfaz requerida por el modelo real del sensor.
- Cables Dupont o borneras segun conexion.
- Multimetro.
- Recipiente para muestra de suelo.
- Suelo seco.
- Agua limpia para humedecer muestra.
- Etiquetas o notas para identificar cada muestra.
- Laptop con acceso al repo `green-house`.

Deseables:

- Termometro o referencia ambiental.
- Balanza para registrar masa de agua agregada.
- Libreta fisica o archivo CSV/JSONL para observaciones.
- Foto del montaje para evidencia L4_FIELD_LAB.

## Seguridad y cuidado

- Verificar voltaje antes de energizar el sensor.
- No conectar o desconectar cables con alimentacion activa si el fabricante no lo permite.
- Mantener agua lejos de fuentes, regletas y puertos USB.
- No accionar bombas, valvulas ni riego automatico durante estas pruebas.

## Historias refinadas

| ID | Titulo | Estado propuesto | Rol experto | Evidencia principal |
| --- | --- | --- | --- | --- |
| HU-SOIL-LAB-001 | Preparar banco de pruebas y materiales del sensor de suelo | READY | QA Engineer | checklist, fotos/notas, multimetro |
| HU-SOIL-LAB-002 | Capturar lectura cruda estable del sensor de suelo | BACKLOG | Firmware Engineer | log serial/RS485, payload crudo |
| HU-SOIL-LAB-003 | Caracterizar lecturas en seco, humedo y saturado | BACKLOG | QA Engineer | tabla de mediciones, condiciones |
| HU-SOIL-DATA-001 | Definir payload MQTT V1 para medicion de suelo | BACKLOG | Backend / IoT Engineer | contrato payload, ejemplo JSON |
| HU-SOIL-WEB-001 | Publicar guia y ruta web de pruebas de suelo | DONE | Frontend Engineer | ruta web, build |

## Paso a paso inicial

### 1. Antes de conectar

1. Identificar modelo exacto del sensor, voltaje, protocolo y pines.
2. Revisar si usa RS485/Modbus, salida analogica u otro protocolo.
3. Registrar foto o descripcion del sensor y etiqueta visible.
4. Validar fuente con multimetro.
5. Crear archivo de evidencia inicial en `project/evidence/soil-moisture/`.

Resultado esperado:

- Banco de pruebas preparado.
- Riesgos conocidos.
- Sensor sin energizar hasta verificar conexion.

### 2. Conexion minima

1. Conectar alimentacion segun especificacion del sensor.
2. Conectar interfaz de datos al equipo de prueba.
3. Verificar que el sistema operativo detecta el adaptador si aplica.
4. Registrar comando usado y salida.

Resultado esperado:

- Interfaz detectada.
- No hay sobrecalentamiento, olor, corto o comportamiento anormal.

### 3. Primera lectura cruda

1. Ejecutar script o herramienta disponible en `green-house`.
2. Guardar salida cruda sin transformaciones.
3. Repetir al menos 5 lecturas con intervalo fijo.
4. Registrar si hay errores, timeouts o valores fuera de rango.

Resultado esperado:

- Se obtiene una lectura cruda reproducible o se documenta el fallo.

### 4. Tres condiciones de muestra

1. Medir suelo seco.
2. Medir suelo humedo.
3. Medir suelo saturado.
4. Registrar timestamp, condicion, lectura cruda y observaciones.

Resultado esperado:

- Las lecturas cambian de forma coherente entre condiciones.
- Si no cambian, se abre blocker de cableado, protocolo o sensor.

### 5. Decision de avance

1. QA revisa evidencia.
2. Solution / IoT Architect decide si se habilita integracion MQTT V1.
3. Si hay datos suficientes, se toma HU-SOIL-DATA-001.

## Evidencia esperada

Guardar evidencia pequena y segura en:

- `project/evidence/soil-moisture/HU-SOIL-LAB-001-evidence-index.md`
- `project/evidence/soil-moisture/HU-SOIL-LAB-002-raw-readings.jsonl`
- `project/evidence/soil-moisture/HU-SOIL-LAB-003-characterization.csv`

No guardar:

- Secretos.
- Tokens.
- Fotos con informacion sensible.
- Datos externos no trazables.

## Prompt recomendado para el chat

```text
Quiero comenzar HU-SOIL-LAB-001. Dame el checklist de banco de pruebas, materiales, evidencias y una sola pregunta para iniciar.
```

## Pregunta pendiente

Confirmar el modelo/protocolo real del sensor de suelo 7-en-1 antes de ejecutar lectura cruda.
