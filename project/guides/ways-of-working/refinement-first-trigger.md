# Refinement First Trigger

Estado: ACTIVE
Fecha: 2026-09-24

## Para que sirve

Cuando durante una conversacion, laboratorio o implementacion aparece una nueva HU, el proyecto debe detener ejecucion y refinar primero. Esto evita trabajar sin lineamientos, sin criterios, sin Gherkin o sin evidencia esperada.

## Frases que activan el flujo

El humano puede decir:

- "Nueva HU: ..."
- "Creemos una HU para ..."
- "Salio otra HU ..."
- "Trabajemos esta HU, primero criterios y Gherkin"
- "Antes de seguir, refinemos esta HU"
- "Primero armemos la HU"

## Respuesta esperada del asistente/agentes

1. Identificar o crear el ID de HU.
2. Dejar la HU en `REFINEMENT` o `BACKLOG`, no en ejecucion.
3. Completar como minimo:
   - problema;
   - resultado esperado;
   - alcance in/out;
   - rol experto;
   - rol revisor;
   - criterios de aceptacion;
   - escenarios Gherkin o excepcion aprobada;
   - DoR;
   - DoD;
   - evidencia esperada;
   - riesgos;
   - dependencias o bloqueos;
   - siguiente accion.
4. Solo despues recomendar READY o ejecucion.

## Regla corta

Si no hay criterios y Gherkin, no hay implementacion. Primero contrato de HU, despues codigo/laboratorio.
