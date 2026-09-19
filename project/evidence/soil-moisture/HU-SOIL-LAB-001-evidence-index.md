# Evidence index - HU-SOIL-LAB-001

Estado: CLOSED  
Fecha: 2026-09-01  
HU: HU-SOIL-LAB-001  
Tipo de evidencia esperado: L4_FIELD_LAB + L1_STATIC

## Objetivo de evidencia

Demostrar que el banco de pruebas del sensor de suelo 7-en-1 esta preparado de forma segura antes de capturar lecturas crudas.

## Checklist

| Item | Estado | Evidencia / nota |
| --- | --- | --- |
| Modelo exacto del sensor identificado | PENDIENTE |  |
| Protocolo real identificado | OBSERVADO | RS485/Modbus: `read @0x0 count=7 id=1 4800 8N1`, device status reporta `soil_modbus_id=1`, `soil_register_start=0`, `soil_register_count=7`. |
| Voltaje verificado con multimetro | PENDIENTE |  |
| Interfaz de datos disponible | OBSERVADO | Lecturas Modbus y payload MQTT capturados desde `dev-zfert01-soil-01`. |
| Cableado revisado antes de energizar | PENDIENTE |  |
| Agua separada de fuente/puertos | PENDIENTE |  |
| Ruta de logs definida | OBSERVADO | `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl` |

## Materiales

| Material | Estado | Nota |
| --- | --- | --- |
| Sensor de suelo 7-en-1 | OBSERVADO | Entrega humedad, temperatura, pH, EC y N/P/K. Modelo exacto sigue pendiente. |
| Raspberry Pi o microcontrolador | OBSERVADO | Fuente del log indica emision por MQTT; device status registra firmware `0.1.0`. |
| Fuente compatible | PENDIENTE |  |
| Interfaz RS485/USB o equivalente | OBSERVADO | Hay lectura Modbus estable en `4800 8N1`. |
| Cables / borneras | PENDIENTE |  |
| Multimetro | PENDIENTE |  |
| Recipiente y muestra de suelo | PENDIENTE |  |

## Resultado

Resultado recomendado: PASS_WITH_LIMITATIONS  
Reviewer: pendiente  
Limitaciones: Laboratorio fisico inicial cerrado con evidencia suficiente para continuar; siguen pendientes modelo exacto, verificacion formal de voltaje/cableado, timestamp real por lectura, calibracion agronomica y resiliencia MQTT.

## Cierre del laboratorio

- Fecha de cierre: 2026-09-01
- Alcance cerrado: preparacion operativa, captura cruda, respuesta por humedad incremental y caracterizacion seco/humedo/saturado/extendido.
- Resultado: el sensor responde de forma coherente a los aportes de agua; humedad y EC suben progresivamente, y NPK pasa de cero a valores altos cuando la muestra alcanza humedad/EC alta.
- Decision: cerrar `HU-SOIL-LAB-001`, `HU-SOIL-LAB-002` y `HU-SOIL-LAB-003` como laboratorio inicial finalizado.
- Trabajos derivados: `HU-FW-MQTT-RESILIENCE-001`, `HU-FW-CONFIG-001`, `HU-FW-OTA-001` y `HU-SOIL-DATA-001`.

## Observacion de campo

- La tierra del recipiente aparece muy seca, casi polvo.
- Esta condicion es valida como punto P0 (suelo seco de referencia) para la serie de pruebas.
- Se recomienda registrar masa inicial y peso de suelo seco antes de agregar agua medida.

## Primera lectura registrada

- Fecha: 2026-09-01
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Fuente: Raspberry Pi emitido por MQTT
- Resultado: `soil_moisture_pct = 16.6%`, `soil_temperature_c = 24.4C`, `soil_ph = 5.7`, `soil_ec_us_cm = 0`, `N/P/K = 0`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie de lectura cruda - muestra 3

- Fecha: 2026-09-01
- Condicion: `sample_3_after_8_min`
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 19.5-19.6%`, `soil_temperature_c = 24.1-24.6C`, `soil_ph = 5.5-5.7`, `soil_ec_us_cm = 1`, `N/P/K = 0`.
- Secuencias registradas: `534` a `539`.
- Evidencia adicional: status `online` en `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/status`, firmware `0.1.0`, IP `192.168.1.6`, RSSI `-75 dBm`.
- MQTT: se observaron publicaciones `ok`, pero tambien fallos intermitentes de conexion `rc=-2` contra `192.168.1.4:1883`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie de estabilizacion - antes de otros 25 ml

- Fecha: 2026-09-01
- Condicion: `sample_3_plus_8_min_before_next_25ml`
- Contexto: ultima lectura 8 minutos despues de la muestra 3, antes de agregar otros 25 ml.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 18.1-19.7%`, `soil_temperature_c = 23.9-24.5C`, `soil_ph = 5.2-5.7`, `soil_ec_us_cm = 1`, `N/P/K = 0`.
- Lectura de cierre antes del siguiente aporte: `sequence=611`, `soil_moisture_pct=19.6%`, `soil_temperature_c=24.1C`, `soil_ph=5.6`, `soil_ec_us_cm=1`.
- Secuencias registradas: `604` a `611`.
- Evidencia adicional: status `online`, firmware `0.1.0`, IP `192.168.1.6`, RSSI `-74 dBm`.
- MQTT: hubo `publish: failed` en status `device_time=4766`, fallos `rc=-2`, reconexion posterior y publishes `ok`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie humeda - 10 min despues de 2 x 25 ml

- Fecha: 2026-09-01
- Condicion: `after_two_25ml_plus_10_min`
- Contexto: lectura tomada 10 minutos despues de agregar dos aportes de 25 ml.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 23.7-23.8%`, `soil_temperature_c = 23.9C`, `soil_ph = 4.7-4.9`, `soil_ec_us_cm = 70`, `N/P/K = 0`.
- Secuencias registradas: `706` a `710`.
- Registros Modbus observados: `Reg0=237-238`, `Reg1=239`, `Reg2=70`, `Reg3=47-48`, `Reg4=0`, `Reg5=0`, `Reg6=0`.
- MQTT: hubo publishes `ok`, un `publish: failed`, status con `mqtt_connected=false`, `mqtt_state=-4`, y reconexion posterior.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie humeda - 20 min despues de 2 x 25 ml

- Fecha: 2026-09-01
- Condicion: `after_two_25ml_plus_20_min`
- Contexto: segunda lectura 10 minutos despues de la muestra humeda previa, sin agregar mas agua.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 24.0-24.1%`, `soil_temperature_c = 23.9C`, `soil_ph = 4.7`, `soil_ec_us_cm = 71`, `N/P/K = 0`.
- Secuencias registradas: `786` a `792`.
- Registros Modbus observados: `Reg0=240-241`, `Reg1=239`, `Reg2=71`, `Reg3=47`, `Reg4=0`, `Reg5=0`, `Reg6=0`.
- MQTT: al inicio hubo `mqtt_connected=false`, `mqtt_state=-2`, varios intentos `rc=-2` y payloads sin confirmacion de entrega; desde `sequence=789` hay `MQTT publish: ok`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie recuperada - 15 min despues de 50 ml adicionales

- Fecha: 2026-09-01
- Condicion: `after_extra_50ml_plus_15_min_recovered`
- Contexto: el sensor se habia desconectado tras agregar 50 ml adicionales; luego se recupero y se registro lectura 15 minutos despues del aporte.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 30.1%`, `soil_temperature_c = 23.8C`, `soil_ph = 5.3`, `soil_ec_us_cm = 138`, `N = 0`, `P = 23`, `K = 15`.
- Secuencias registradas: `826` a `831`.
- Registros Modbus observados: `Reg0=301`, `Reg1=238`, `Reg2=138`, `Reg3=53`, `Reg4=0`, `Reg5=23`, `Reg6=15`.
- MQTT: hubo publishes `ok`; en `sequence=829` aparece `WiFiClient write fail errno 104 Connection reset by peer`, `MQTT publish: failed`, reconexion posterior y publishes/status `ok`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie estable - 25 min despues de 50 ml adicionales

- Fecha: 2026-09-01
- Condicion: `after_extra_50ml_plus_25_min_stability`
- Contexto: lectura 10 minutos despues de la serie recuperada, sin agregar mas agua.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 29.2-29.5%`, `soil_temperature_c = 23.7C`, `soil_ph = 5.3`, `soil_ec_us_cm = 136`, `N = 0`, `P = 22`, `K = 14`.
- Secuencias registradas: `922` a `926`.
- Registros Modbus observados: `Reg0=294-295`, `Reg1=237`, `Reg2=136`, `Reg3=53`, `Reg4=0`, `Reg5=22`, `Reg6=14`.
- MQTT: `sequence=923` tuvo `MQTT publish: failed` y reconexion; status posterior `online` y publishes `ok`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie humeda alta - 10 min despues de ultimos 50 ml

- Fecha: 2026-09-01
- Condicion: `after_final_50ml_plus_10_min`
- Contexto: lectura 10 minutos despues de agregar los ultimos 50 ml.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 56.0%`, `soil_temperature_c = 23.7C`, `soil_ph = 5.3`, `soil_ec_us_cm = 192-193`, `N = 1`, `P = 49-50`, `K = 42`.
- Secuencias registradas: `1032` a `1036`.
- Registros Modbus observados: `Reg0=560`, `Reg1=237`, `Reg2=192-193`, `Reg3=53`, `Reg4=1`, `Reg5=49-50`, `Reg6=42`.
- MQTT: primer payload sin confirmacion por intento `rc=-2`; secuencias `1033` a `1035` con `publish: ok`; `sequence=1036` tuvo `MQTT publish: failed`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie humeda alta - 20 min despues de ultimos 50 ml

- Fecha: 2026-09-01
- Condicion: `after_final_50ml_plus_20_min_stability`
- Contexto: segunda lectura 10 minutos despues de la serie humeda alta, sin agregar mas agua.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 54.6-54.8%`, `soil_temperature_c = 23.6-23.7C`, `soil_ph = 5.3`, `soil_ec_us_cm = 186`, `N = 0`, `P = 46`, `K = 39`.
- Secuencias registradas: `1129` a `1135`.
- Registros Modbus observados: `Reg0=546-548`, `Reg1=236-237`, `Reg2=186`, `Reg3=53`, `Reg4=0`, `Reg5=46`, `Reg6=39`.
- MQTT: `sequence=1129` tuvo `MQTT publish: failed` y `rc=-2`; status `device_time=9162` reporto `mqtt_connected=false`; desde `sequence=1131` hasta `1134` hubo `publish: ok`.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Serie extendida - 5 min despues de 200 ml totales

- Fecha: 2026-09-01
- Condicion: `after_total_200ml_plus_5_min_extended`
- Contexto: se agregaron 50 ml adicionales para terminar con aproximadamente 200 ml totales; el protocolo original solo contemplaba hasta 150 ml, por lo que esta lectura se registra como extension de laboratorio.
- Canal: `greenhouse/gh-lab-01/zone/z-fert-01/device/dev-zfert01-soil-01/telemetry`
- Rango observado: `soil_moisture_pct = 86.4-86.7%`, `soil_temperature_c = 23.5C`, `soil_ph = 5.4`, `soil_ec_us_cm = 315-319`, `N = 27-28`, `P = 109-111`, `K = 101-103`.
- Secuencias registradas: `1264` a `1268`.
- Registros Modbus observados: `Reg0=864-867`, `Reg1=235`, `Reg2=315-318`, `Reg3=54`, `Reg4=27`, `Reg5=109-110`, `Reg6=101-103`.
- MQTT: status `device_time=10132` reporto `mqtt_connected=true`, `mqtt_state=0`, RSSI `-71 dBm`; la mayoria de publishes aparecen `ok`, aunque `sequence=1265` se marca como `not_confirmed` por reconexion entre payload y confirmacion.
- Archivo de evidencia: `project/evidence/soil-moisture/HU-SOIL-LAB-002-first-reading-2026-09-01.jsonl`

## Interpretacion

- El sensor responde y entrega datos de forma consistente con un ambiente de suelo seco a moderadamente seco.
- El valor de humedad 16.6% encaja con una muestra visualmente seca, pero no es una lectura de calibracion definitiva.
- La muestra 3, despues de 8 minutos, mantiene lecturas estables alrededor de 19.5-19.6% de humedad; esto sugiere respuesta incremental frente al punto seco inicial, pero aun no caracteriza una curva de calibracion.
- La estabilizacion previa al siguiente aporte de 25 ml oscila entre 18.1% y 19.7%, cerrando en 19.6%; se debe tratar como variacion de contacto/estabilizacion hasta repetir con condiciones mas controladas.
- Luego de dos aportes de 25 ml y 10 minutos de espera, humedad sube a 23.7-23.8% y EC sube de 1 a 70 us/cm; esto confirma que el sensor responde al cambio de condicion.
- Diez minutos despues, sin agregar mas agua, humedad se estabiliza en 24.0-24.1% y EC en 71 us/cm; el punto humedo queda suficientemente estable para avanzar al siguiente aporte.
- Luego de agregar 50 ml adicionales y recuperarse de una desconexion, la humedad sube a 30.1% y EC a 138 us/cm; P y K aparecen por primera vez con valores repetibles (`P=23`, `K=15`), mientras N permanece en `0`.
- Diez minutos despues de la recuperacion, el punto se mantiene estable: humedad `29.2-29.5%`, EC `136`, `P=22`, `K=14`, `N=0`; se considera suficiente para avanzar al siguiente aporte de 50 ml si el montaje esta seguro.
- Diez minutos despues del ultimo aporte de 50 ml, la humedad sube a `56.0%`, EC a `192-193`, P/K a `49-50/42`, y N aparece por primera vez como `1`; esto refuerza que el mapeo `Reg4/5/6 = N/P/K` es plausible, aunque N requiere validacion adicional.
- Diez minutos despues, sin agregar mas agua, humedad baja levemente a `54.6-54.8%`, EC a `186`, P/K se mantienen altos (`46/39`) y N vuelve a `0`; esto sugiere que N esta cerca del umbral/ruido del sensor o requiere mayor estabilizacion.
- Cinco minutos despues de extender el laboratorio a 200 ml totales, humedad sube a `86.4-86.7%`, EC a `315-319`, y NPK responde de forma clara (`N=27-28`, `P=109-111`, `K=101-103`); esto fortalece la hipotesis de mapeo correcto `Reg4/5/6 = N/P/K`.
- La lectura a 200 ml debe tratarse como punto de sobresaturacion/extension, no como condicion agronomica final, porque excede el alcance original de 150 ml.
- EC=0 y N/P/K=0 fueron coherentes con el suelo base seco; con mayor humedad/EC, P/K comienzan a reportar valores, por lo que no se debe concluir que todos los registros NPK estaban mal mapeados.
- La evidencia acumulada cumple el criterio cuantitativo de `HU-SOIL-LAB-002` de al menos 5 lecturas crudas, con limitacion de timestamp: el log pegado no incluye hora real por lectura, solo `device_time` y `sequence`.
- La conectividad MQTT debe tratarse como `PARTIAL`: hay publish `ok`, pero tambien reconexiones fallidas `rc=-2`; el firmware actual no reencola payloads no publicados.
- El dump de Raspberry con `mosquitto_sub` contiene 65 telemetrias entre `sequence=40` y `sequence=1015`, con 42 saltos internos y 911 secuencias faltantes dentro del rango observado. Sin timestamp local de recepcion no se puede probar que todos los huecos sean perdida de broker, pero si se confirma la necesidad de logger persistente y deteccion de gaps por `sequence`.

## Diagnostico NPK - activacion por humedad/EC alta

- Observacion: `soil_n_mg_kg` permanecio en `0` hasta humedad aproximada de `30%`; despues del ultimo aporte aparece una vez como `1` cuando humedad sube a `56.0%` y EC a `192-193 us/cm`, pero vuelve a `0` en la segunda lectura estable.
- Evidencia cruda: antes del aporte adicional, `Reg4`, `Reg5` y `Reg6` eran `0`; despues de 50 ml adicionales, `Reg4=0`, `Reg5=22-23`, `Reg6=14-15`; despues del ultimo aporte, `Reg4=1`, `Reg5=49-50`, `Reg6=42`; diez minutos despues, `Reg4=0`, `Reg5=46`, `Reg6=39`.
- Evidencia extendida: con 200 ml totales, `Reg4=27`, `Reg5=109-110`, `Reg6=101-103`; N deja de estar cerca de cero cuando la muestra llega a humedad/EC muy alta.
- Firmware observado: `xiao-esp32c3-soil/src/main.cpp` lee `SOIL_REGISTER_START=0x0000`, `SOIL_REGISTER_COUNT=7`, usando holding registers, y mapea `raw[4]`, `raw[5]`, `raw[6]` como N/P/K.
- Hipotesis A: el mapa de registros `Reg4/Reg5/Reg6` para N/P/K parece plausible para este sensor.
- Hipotesis B: N esta cerca de un umbral bajo y puede alternar entre `0` y `1` por estabilizacion, contacto, EC o resolucion del sensor.
- Hipotesis C: el modelo fisico vendido como 7-en-1 no entrega NPK real util, o los entrega como valor derivado no confiable.
- Siguiente validacion recomendada: ejecutar un escaneo de registros holding e input en bloques, por ejemplo `0x0000-0x0030`, y guardar todos los valores crudos antes de cambiar el mapeo.

## Siguiente accion

1. Confirmar modelo exacto y voltaje real del sensor de suelo 7-en-1.
2. Registrar hora real del laboratorio para cada nueva muestra, ademas de `device_time` y `sequence`.
3. Formalizar contrato de datos MQTT V1 para medicion de suelo usando la evidencia cerrada.
4. Revisar causa de MQTT `rc=-2`: broker apagado, red, IP `192.168.1.4`, puerto `1883` o reconexion del cliente.
5. Preparar tabla comparativa final de laboratorio si se requiere reporte externo.
6. Validar mapa Modbus de NPK antes de interpretar `soil_n_mg_kg`, `soil_p_mg_kg` y `soil_k_mg_kg`.
7. Implementar mitigacion de `HU-FW-MQTT-RESILIENCE-001`: contadores MQTT, cola corta de reintento, timestamp local en Raspberry y deteccion de huecos por `sequence`.
