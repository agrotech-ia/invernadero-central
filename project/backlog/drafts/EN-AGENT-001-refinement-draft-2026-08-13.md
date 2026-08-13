# DRAFT - Refinamiento EN-AGENT-001

generated_observed: 2026-08-13  
source: CHAT-GATEWAY-001 -> project-refinement  
source_request:

```json
{"message":"refinar EN-AGENT-001 en modo corto","chat_id":"local-project-chat","dry_run":false}
```

status: DRAFT - requiere aprobacion humana para persistir en backlog, Kanban o tareas ejecutables.

## Resumen Del Item

| Campo | Valor |
|---|---|
| id | EN-AGENT-001 |
| type | ENABLER |
| priority | P0 |
| target | FOUNDATION |
| status actual | READY |
| effort | M |
| source | HU-009, seccion 23 |
| expert_role | Solution / IoT Architect |
| reviewer_role | QA Engineer |

## Problema

No existe plataforma de ejecucion para agentes versionados. Sin ella, cada agente
se configura ad-hoc, sin registry ni contexto compartido, y la orquestacion depende
de un chat humano sin trazabilidad.

## Resultado Esperado

n8n local orquesta agentes con registry versionado en Git, donde Knowledge Agent
alimenta contexto a los demas, el Orchestrator enruta por capacidad, y toda
persistencia pasa por gate humano.

## Tareas Propuestas

### Opcion A - Entrega incremental en 5 tareas

Recomendada por el agente.

| Tarea | Titulo | Rol | Agente | Evidencia esperada |
|---|---|---|---|---|
| T-AGT-001 | Definir Agent Registry en YAML versionado | Solution Architect | AGENT-REF-001 | `agents/registry.yaml` con schema validable |
| T-AGT-002 | Implementar Knowledge Agent: carga de HU/DEC/inventario desde Git | Solution Architect | Mixto | Workflow n8n que responde consultas del proyecto sin depender del chat |
| T-AGT-003 | Implementar Orchestrator minimo en n8n con routing por capacidad | Solution Architect | Mixto | Workflow n8n con router que despacha a >= 2 agentes segun intent |
| T-AGT-004 | Integrar Backlog, Refinement, Market y Growth Agents como consumers | Solution Architect | Mixto | Cada agente recibe contexto de Knowledge y responde en su dominio |
| T-AGT-005 | Validacion E2E: caso de prueba sensor de suelo | QA Engineer | Mixto | Log de ejecucion donde Backlog Agent no propone reimplementar suelo |

### Opcion B - Comprimida en 3 tareas

Agrupa T-AGT-001 + T-AGT-002 y T-AGT-003 + T-AGT-004, dejando T-AGT-005 como
validacion.

### Opcion C - Spike exploratorio primero

Una sola tarea timeboxed de 2h para probar el routing de n8n con Knowledge + 1
agente consumer, y luego refinar el resto con hallazgos.

## Criterios De Aceptacion

1. Agent Registry cargado desde repositorio Git.
2. Knowledge Agent recupera HU/DEC/inventario sin depender del chat.
3. Orchestrator enruta por capacidad y no actua como agente universal.
4. Backlog Agent no propone reimplementar el sensor de suelo.
5. Refinement Agent genera V&V y procurement para suelo.
6. Market/Growth respetan politica de claims.
7. Toda persistencia final pasa por revision humana.

## Definition Of Ready

- Contexto minimo: HU-009 seccion 23, `project/backlog/EN-AGENT-001.yaml` y `master-backlog.yaml`.
- Criterios de aceptacion verificables.
- Riesgos conocidos.
- Evidencia esperada definida por tarea.
- Roles asignados.

## Definition Of Done

- Los 7 criterios de aceptacion cumplidos con evidencia en repositorio.
- Log de ejecucion del caso de prueba sensor de suelo guardado.
- Revision de QA Engineer completada.
- Estado actualizado con aprobacion humana.

## Riesgos

| Riesgo | Mitigacion |
|---|---|
| n8n community no soporta sub-workflows complejos | Validar con spike antes de comprometerse |
| Contexto del Knowledge Agent crece y excede ventana | Cargar solo resumen + refs; lazy-load detalle bajo demanda |
| Agentes se solapan o contradicen | Routing estricto por intent y politica de no actuar fuera de dominio |

## Dependencias

Ninguna bloqueante segun `master-backlog.yaml`. EN-QA-001 es complementaria pero
no bloqueante para el bootstrap.

## Aprobacion Humana Requerida

- Persistir el registry final en Git.
- Desplegar workflows n8n como produccion local.
- Cambios de arquitectura mayor si el spike revela limitaciones.

## Decision Pendiente

```text
Cual opcion de granularidad prefieres para ejecutar EN-AGENT-001:
A (5 tareas incrementales), B (3 tareas comprimidas), o C (spike exploratorio primero)?
```

Hasta aprobacion humana, este archivo no actualiza `master-backlog.yaml`,
`board.yaml` ni estados Kanban.
