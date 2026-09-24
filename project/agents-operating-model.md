# Modelo operativo multiagente del proyecto

Estado: DRAFT  
Proposito: definir como los agentes ayudan a dirigir, refinar, ejecutar, revisar y evidenciar
trabajo de todo el proyecto, no solo de una historia puntual.

## Intencion

El proyecto debe operar como una organizacion pequena asistida por agentes.

Una sola persona puede tomar trabajo de cualquier rol, pero el sistema debe ayudarle a:

- saber como va cada HU o enabler;
- elegir que trabajar segun prioridad, riesgo, dependencia, tiempo disponible y energia del momento;
- mantener WIP controlado;
- refinar historias antes de ejecutarlas;
- generar tareas tecnicas por rol;
- permitir que agentes avancen partes de bajo riesgo;
- exigir aprobacion humana en decisiones fisicas, economicas, arquitectura mayor, despliegues criticos
  o cambios de baseline;
- dejar evidencia suficiente para validar progreso real.

Objetivo aspiracional:

- reducir el calendario mediante paralelizacion asistida y automatizacion responsable;
- no sacrificar trazabilidad, seguridad ni calidad por velocidad.

## Principios

- Git es fuente de verdad.
- Kanban pull-based.
- WIP recomendado: maximo 2 historias en `IN_PROGRESS`.
- Primero refinar, luego ejecutar.
- Si aparece una nueva HU durante una conversacion o laboratorio, primero se arma
  la HU completa y luego se ejecuta.
- Los agentes proponen y preparan; el humano aprueba cambios de impacto.
- Trabajo operativo no equivale a validado.
- No se marca `DONE` sin evidencia.
- Las HU congeladas no se editan silenciosamente.

## Flujo de trabajo completo

```text
Backlog Intake
-> Knowledge Sync
-> Technical Discovery
-> Shared Contract Decision
-> Portfolio / Priority Review
-> Work Selection
-> Refinement
-> Role Task Breakdown
-> Execution Plan
-> Agent/Human Execution
-> Evidence Capture
-> Review / QA
-> Human Decision Gate
-> Persist / Update Backlog
-> Next Work Recommendation
```

## Estados Kanban

Estados existentes:

```text
IDEA -> BACKLOG -> REFINEMENT -> READY -> IN_PROGRESS -> VALIDATION -> DONE
```

Reglas:

- `BACKLOG`: idea o necesidad conocida, aun no lista para ejecutar.
- `REFINEMENT`: se estan definiendo criterios, tareas, riesgos, evidencia y DoR/DoD.
- `READY`: puede ser tomada por humano/agente sin aclaraciones mayores.
- `IN_PROGRESS`: alguien o un agente esta ejecutando.
- `VALIDATION`: requiere prueba, revision, evidencia o aprobacion.
- `DONE`: terminado con evidencia suficiente y decision persistida cuando aplique.

## Gates obligatorios de estado

La fuente operativa de compuertas es `project/validation/state-gates.yaml`.

Regla fuerte:

- Frases como `nueva HU`, `creemos una HU`, `salio otra HU`, `trabajemos esta HU`,
  `refinemos la HU` o `primero armemos la HU` obligan a enrutar a refinamiento.
  El resultado minimo debe ser una HU con problema, resultado, alcance,
  criterios, Gherkin, DoR, DoD, evidencia esperada, riesgos, dependencias y
  siguiente accion.
- Ningun item ejecutable puede estar en `READY`, `IN_PROGRESS`, `VALIDATION` o `DONE`
  sin criterios de aceptacion, escenarios Gherkin o excepcion aprobada, DoR, DoD,
  evidencia esperada y granularidad clara.
- Una HU parent puede estar en `READY` solo como contenedor de coordinacion. No se
  ejecuta directamente; debe listar HUs hijas y la siguiente accion debe apuntar a
  una HU hija ejecutable.
- Si una tarjeta ya esta en `IN_PROGRESS` o `VALIDATION` y falla el gate, el siguiente
  trabajo no es seguir ejecutando: es corregir refinamiento/evidencia con
  `AGENT-REF-001` o `AGENT-QA-001`.
- `granularity=needs_task_breakdown` es incompatible con `READY`, `IN_PROGRESS`,
  `VALIDATION` y `DONE`, salvo que el item sea marcado explicitamente como parent y
  tenga HUs hijas ejecutables.

## Como pedirlo en conversacion

Para activar el flujo correcto, el humano puede decir cualquiera de estas frases:

- "Nueva HU: ..."
- "Creemos una HU para ..."
- "Antes de seguir, refinemos esta HU"
- "Trabajemos esta HU, primero criterios y Gherkin"
- "Esto es una HU nueva, armemos el contrato"

La respuesta esperada de agentes y asistentes es preparar o actualizar la HU antes
de ejecutar codigo, laboratorio, despliegues o movimientos de estado.

## Seleccion de trabajo

El agente de backlog debe recomendar trabajo considerando:

- prioridad `P0/P1/P2`;
- dependencias;
- riesgo;
- impacto en el MVP E2E;
- tiempo disponible del humano;
- tipo de trabajo deseado por el humano;
- estado actual;
- posibilidad de avance autonomo;
- necesidad de hardware fisico o aprobacion;
- evidencia faltante.

Ejemplos de perfiles de seleccion:

```yaml
selection_modes:
  quick_win:
    description: Trabajo corto, bajo riesgo, deja avance visible.
  deep_work:
    description: Trabajo largo que desbloquea ruta critica.
  physical_lab:
    description: Trabajo con sensores, cableado, medicion o pruebas fisicas.
  coding:
    description: Trabajo implementable por agente con revision humana.
  docs_governance:
    description: Refinamiento, decisiones, evidencia, backlog y arquitectura.
  market_growth:
    description: Mercado, contenido, claims y descubrimiento comercial.
```

## Roles y agentes existentes

Agentes ya definidos:

- `AGENT-ORCH-001`: Orchestrator.
- `AGENT-KNOW-001`: Knowledge Agent.
- `AGENT-PROD-001`: Product Agent.
- `AGENT-PLAN-001`: Project Planning Agent.
- `AGENT-PMO-001`: PMO / Flow Control Agent.
- `AGENT-BKL-001`: Project / Backlog Agent.
- `AGENT-REF-001`: Refinement Agent.
- `AGENT-ARCH-001`: Architecture Agent.
- `AGENT-DISC-001`: Technical Discovery Agent.
- `AGENT-CONTRACT-001`: Shared Contract Agent.
- `AGENT-DOC-001`: Documentation Agent.
- `AGENT-MKT-001`: Market Intelligence & Demand Agent.
- `AGENT-GROW-001`: Growth, Content & Education Agent.
- `AGENT-REV-001`: Reviewer / Safety Agent.
- `AGENT-ENG-001`: Engineering Execution Agent.
- `AGENT-QA-001`: QA / Evidence Agent.

## Matriz de madurez de agentes

| Agente | Definicion | Kiro | n8n dedicado | Chat routing | Estado |
|---|---|---|---|---|---|
| `AGENT-KNOW-001` | si | `project-knowledge` | `AGENT-KNOW-001` | si | operativo DRAFT |
| `AGENT-PMO-001` | si | `project-pmo` | `AGENT-PMO-001` | si | operativo DRAFT |
| `AGENT-PLAN-001` | si | `project-planning` | `AGENT-PLAN-001` | si | operativo DRAFT |
| `AGENT-REF-001` | si | `project-refinement` | `AGENT-REF-001` | si | operativo DRAFT |
| `AGENT-BKL-001` | si | `project-backlog` | `AGENT-BKL-001` | si | operativo DRAFT |
| `AGENT-DISC-001` | si | `project-discovery` | `AGENT-DISC-001` | si | operativo DRAFT |
| `AGENT-CONTRACT-001` | si | `project-contract` | `AGENT-CONTRACT-001` | si | operativo DRAFT |
| `AGENT-DOC-001` | si | `project-documentation` | `AGENT-DOC-001` | si | operativo DRAFT |
| `AGENT-ARCH-001` | si | `project-architecture` | `AGENT-ARCH-001` | si | operativo DRAFT |
| `AGENT-ENG-001` | si | `project-engineering` | `AGENT-ENG-001` | si | operativo DRAFT |
| `AGENT-QA-001` | si | `project-qa-evidence` | `AGENT-QA-001` | si | operativo DRAFT |
| `AGENT-REV-001` | si | `project-reviewer-safety` | `AGENT-REV-001` | si | operativo DRAFT |
| `AGENT-ORCH-001` | si | `project-orchestrator` | `AGENT-ORCH-001` | si | operativo DRAFT |
| `AGENT-PROD-001` | si | `project-product` | `AGENT-PROD-001` | si | operativo DRAFT |
| `AGENT-MKT-001` | si | `project-market-intelligence` | `AGENT-MKT-001` | si | operativo DRAFT |
| `AGENT-GROW-001` | si | `project-growth-content` | `AGENT-GROW-001` | si | operativo DRAFT |
| `AGENT-EDGE-001` | si | `project-edge` | `AGENT-EDGE-001` | si | operativo DRAFT |
| `AGENT-WEB-001` | si | `project-web` | `AGENT-WEB-001` | si | operativo DRAFT |
| `AGENT-HW-001` | si | `project-hardware` | `AGENT-HW-001` | si | operativo DRAFT |

## Agentes especializados agregados

Las especializaciones edge, web y hardware quedan registradas como agentes propios.

### DevOps / Edge Agent

ID sugerido:

```text
AGENT-EDGE-001
```

Rol:

- DevOps / Platform / Edge Engineer.

Responsabilidad:

- Raspberry Pi;
- Mosquitto;
- PostgreSQL/TimescaleDB;
- ingestion runtime;
- logs;
- servicios locales;
- respaldos.

### Frontend Agent

ID sugerido:

```text
AGENT-WEB-001
```

Rol:

- Frontend Engineer / UX.

Responsabilidad:

- dashboard real;
- reemplazo progresivo de mocks;
- estados de carga/error;
- visualizacion de telemetria;
- ergonomia de flujos.

### Hardware / Lab Agent

ID sugerido:

```text
AGENT-HW-001
```

Rol:

- Hardware / Lab Engineer.

Responsabilidad:

- cableado;
- potencia;
- protecciones;
- bombas;
- valvulas;
- pruebas fisicas;
- procurement tecnico.

Restriccion:

- no ejecutar compras ni control fisico critico sin aprobacion humana.

## Ciclo por HU

Cada HU o enabler debe pasar por esta estructura minima:

```yaml
story_lifecycle:
  intake:
    owner: AGENT-BKL-001
    output: historia ubicada en backlog con prioridad y dependencias
  knowledge_check:
    owner: AGENT-KNOW-001
    output: contexto y evidencia existente
  technical_discovery:
    owner: AGENT-DISC-001
    output: repos, entry points, impacto, dependencias, pruebas, riesgos y unknowns
  contract_decision:
    owner: AGENT-DISC-001
    output: sharedContract.recommended true/false
  shared_contract:
    owner: AGENT-CONTRACT-001
    output: contrato compartido cuando aplique
  refinement:
    owner: AGENT-REF-001
    output: criterios, tareas, DoR, DoD, riesgos, evidencia esperada
  state_gate_check:
    owner: AGENT-QA-001
    output: PASS/FAIL del estado objetivo contra `project/validation/state-gates.yaml`
  architecture_review:
    owner: AGENT-ARCH-001
    output: impacto y decisiones requeridas
  execution:
    owner: role_specific_agent_or_human
    output: cambios, pruebas, notas y evidencias
  qa_validation:
    owner: AGENT-QA-001
    output: resultados V&V y recomendacion de estado
  human_gate:
    owner: human
    output: aprobacion, rechazo o ajustes
  persistence:
    owner: AGENT-BKL-001
    output: backlog actualizado y artefactos versionados
  documentation:
    owner: AGENT-DOC-001
    output: guia, ejemplo, runbook o troubleshooting trazable cuando aplique
```

## Artefactos intermedios por HU

Para evitar depender de memoria conversacional, los agentes deben intercambiar contexto mediante
artefactos versionables cuando el trabajo sea tecnico o de alto impacto.

Ruta recomendada:

```text
project/agent-work/<backlog_id>/
```

Archivos:

```text
request.yaml
discovery.yaml
shared-contract.yaml
story-draft.md
review.yaml
qa-readiness.yaml
```

Reglas:

- `discovery.yaml` es obligatorio antes de finalizar HUs tecnicas que toquen codigo, repos, API,
  MQTT, DB, eventos, frontend/backend, infraestructura o CI/CD.
- `shared-contract.yaml` solo existe cuando `AGENT-DISC-001` recomienda contrato compartido.
- `AGENT-REF-001` consume Discovery y Contract; no debe inventarlos ni modificarlos.
- `AGENT-REV-001` audita trazabilidad entre requerimiento, Discovery, Contract y HU.
- `AGENT-QA-001` valida evidencia y readiness; no reemplaza review tecnico.

## Clasificacion de evidencia tecnica

Toda afirmacion tecnica de Discovery o Contract debe estar marcada como:

- `CONFIRMED`: suministrada explicitamente por el humano o requerimiento.
- `DISCOVERED`: encontrada en codigo, configuracion o documentacion.
- `INFERRED`: inferencia razonable basada en evidencia citada.
- `PROPOSED`: cambio recomendado que aun no existe.
- `UNKNOWN`: no pudo determinarse.

Nunca convertir `INFERRED` o `PROPOSED` en `DISCOVERED`.

## Trabajo autonomo permitido

Un agente puede avanzar autonomamente cuando:

- la tarea esta refinada;
- el alcance es reversible;
- no toca control fisico critico;
- no compra nada;
- no expone secrets;
- no modifica HU congeladas;
- tiene pruebas o validacion local posible;
- deja evidencia.

Ejemplos:

- crear scripts de ingesta;
- agregar pruebas unitarias;
- refactorizar frontend acotado;
- generar borradores de backlog;
- crear casos de prueba;
- preparar docs tecnicas;
- validar JSON/YAML;
- ejecutar builds locales.

## Trabajo que requiere aprobacion humana

- compras;
- control de bombas, valvulas o potencia;
- cambios de arquitectura mayor;
- despliegues criticos;
- cambios sobre baseline congelada;
- claims comerciales fuertes;
- uso de presupuesto;
- manejo de credenciales;
- decisiones de seguridad.

## Evidencia minima

Tipos de evidencia:

```yaml
evidence_types:
  code:
    examples:
    - commit hash
    - diff summary
    - test output
    - build output
  sensor:
    examples:
    - payload MQTT
    - logs seriales
    - archivo JSONL
    - captura de lectura
  database:
    examples:
    - query result
    - migration applied
    - row count
  web:
    examples:
    - screenshot
    - build output
    - API response
  hardware:
    examples:
    - foto o nota de cableado
    - medicion con instrumento
    - checklist de seguridad
  decision:
    examples:
    - ADR
    - decision register entry
    - aprobacion humana
```

## Artefactos recomendados

```text
project/kanban/board.yaml
project/backlog/master-backlog.yaml
project/backlog/drafts/
project/backlog/templates/hu-template.yaml
project/roles/expert-role-catalog.yaml
project/tasks/
project/validation/
project/evidence/
project/decisions/
project/context/
agents/
n8n/workflows/
```

## Workflow n8n principal recomendado

```text
Manual/Chat Trigger
-> Load Project State
-> Ask Work Preference
-> Backlog Agent recommends candidates
-> Human selects work
-> Knowledge Agent builds context
-> Refinement Agent prepares story/task plan
-> Architecture/QA/Reviewer gates as needed
-> Execution Agent or human performs work
-> QA/Evidence Agent validates
-> Human approves status transition
-> Backlog Agent updates state
```

## Pregunta unica del sistema al humano

El sistema debe evitar hacer muchas preguntas al tiempo.

Patron recomendado:

```text
Tengo estas 3 opciones recomendadas segun prioridad y contexto. Cual quieres tomar ahora?
```

Luego preguntar una cosa por vez segun la opcion elegida.

## Primeros workflows a implementar

1. `WF-BACKLOG-RECOMMEND-001`: recomendar siguiente trabajo segun estado, prioridad y modo.
2. `WF-REFINE-STORY-001`: refinar una HU/enabler seleccionada.
3. `WF-EXECUTE-TASK-001`: ejecutar trabajo acotado con agente o preparar instrucciones humanas.
4. `WF-QA-EVIDENCE-001`: revisar evidencia y recomendar cambio de estado.
5. `WF-PERSIST-STATE-001`: persistir cambios revisados en Git.

## Ajuste sobre el caso de suelo

El sensor de suelo 7-en-1 sigue siendo un buen primer caso de aceptacion porque ya tiene evidencia
tecnica y permite probar el ciclo completo.

Pero no representa el alcance total del sistema.

El alcance real es:

```text
Sistema multiagente de gestion y ejecucion del backlog completo del proyecto.
```

## Granularidad de HU

Una HU lista para ejecucion debe ser pequena y verificable.

Reglas:

- Si mezcla mas de un dominio experto principal, dividir.
- Si requiere mas de una o dos sesiones claras, dividir.
- Si no se puede demostrar con evidencia concreta, refinar antes de ejecutar.
- Si depende de una compra, aprobacion o prueba fisica bloqueante, separar preparacion de ejecucion.
- Si una historia existe como tema grande, crear HUs hijas o tareas pequenas antes de mover a `READY`.

Plantilla oficial:

```text
project/backlog/templates/hu-template.yaml
```

Catalogo de roles:

```text
project/roles/expert-role-catalog.yaml
```

Tablero Kanban:

```text
project/kanban/board.yaml
```
