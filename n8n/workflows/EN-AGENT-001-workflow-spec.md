# EN-AGENT-001 - Workflow n8n para plataforma multiagente local

Estado: DRAFT  
Objetivo: configurar en n8n un flujo minimo funcional que use agentes versionados desde Git
y permita operar el backlog completo del proyecto con seleccion, refinamiento, ejecucion,
evidencia, revision y persistencia controlada.

## Alcance

Este workflow no instala n8n. El usuario ya informo que n8n esta implementado localmente.

El alcance de `EN-AGENT-001` es:

- cargar reglas del proyecto desde el repo central;
- cargar registry y definiciones YAML de agentes;
- construir contexto minimo desde repositorios locales;
- enrutar la solicitud con Orchestrator;
- ejecutar el agente especializado correcto;
- revisar salida contra reglas del proyecto;
- solicitar aprobacion humana cuando corresponda;
- persistir borradores en Git como artefactos revisables.

El sensor de suelo 7-en-1 se usa como primer caso de aceptacion, pero no define el alcance total.
El alcance total es crear el sistema operativo multiagente del backlog completo.

## Repositorios locales

Repositorio central:

```text
/home/chuchosam/Documentos/github/invernadero-central
```

Repositorio sensores/edge/datos:

```text
/home/chuchosam/Documentos/github/invernadero/green-house
```

Repositorio web:

```text
/home/chuchosam/Documentos/github/agrotechia-web-ui
```

## Workflow minimo

```text
Manual/Chat Trigger
-> Load Project State
-> Load Agent Registry
-> Ask/Read Work Preference
-> Backlog Recommendation
-> Human Selects Work
-> Context Builder
-> Orchestrator
-> Specialized Agent
-> Reviewer / QA Gate
-> Human Approval Gate
-> Persist Draft or State Update
-> Git Status Summary
```

## Nodos n8n sugeridos

### 1. Manual/Chat Trigger

Uso:

- pedir recomendacion de siguiente trabajo;
- refinar una HU/enabler;
- ejecutar un caso de aceptacion;
- recibir un JSON con la solicitud o preferencia de trabajo.

Input inicial recomendado:

```json
{
  "task_id": "WF-BACKLOG-RECOMMEND-001",
  "request": "Recomendar siguiente trabajo del backlog",
  "requested_by": "human",
  "available_time": "unknown",
  "preferred_mode": "any",
  "max_options": 3
}
```

### 2. Load Project Rules

Tipo sugerido:

- Execute Command, Read Binary File, Code node o filesystem integration local.

Archivos:

```text
agents/shared/project-rules.yaml
agents/shared/contracts.yaml
project/context/conversation-context-2026-08-11.md
project/agents-operating-model.md
```

Salida esperada:

```json
{
  "source_of_truth": "Git repository",
  "frozen_baselines": ["HU-001", "HU-002", "HU-003", "HU-004", "HU-005", "HU-006", "HU-007", "HU-008", "HU-009"],
  "authority_rules_loaded": true,
  "contracts_loaded": true,
  "conversation_context_loaded": true
}
```

### 3. Load Agent Registry

Archivos:

```text
agents/registry.yaml
agents/orchestrator/agent.yaml
agents/refinement/agent.yaml
agents/backlog/agent.yaml
agents/knowledge/agent.yaml
agents/architecture/agent.yaml
agents/product/agent.yaml
```

Para recomendar trabajo, el agente principal esperado es:

```text
AGENT-BKL-001 - Project / Backlog Agent
```

El Orchestrator no debe ejecutar trabajo especializado si existe un agente competente.

### 4. Load Task Input

Archivo recomendado para prueba:

```text
n8n/workflows/inputs/EN-AGENT-001-soil-validation-request.json
```

Ese archivo prueba el caso de suelo. Para el ciclo completo, tambien implementar:

```text
n8n/workflows/WF-BACKLOG-RECOMMEND-001-spec.md
```

Si el input llega directamente desde Manual Trigger, este nodo puede normalizarlo al contrato comun:

```yaml
input:
  task_id: string
  agent_id: string
  role: string
  objective: string
  context_refs:
  - string
  constraints:
  - string
  permissions: A0/A1/A2/A3
  expected_output: string
  review_required: bool
```

### 5. Context Builder

Responsabilidad:

- leer solamente el contexto necesario;
- no cargar todas las HU completas por defecto;
- priorizar reglas, inventario, backlog, V&V y evidencia del repo de sensores.

Contexto minimo para el primer caso:

Repositorio central:

```text
agents/shared/project-rules.yaml
agents/shared/contracts.yaml
agents/registry.yaml
agents/orchestrator/agent.yaml
agents/refinement/agent.yaml
project/backlog/EN-AGENT-001.yaml
project/backlog/master-backlog.yaml
project/inventory/master-inventory-v2.yaml
project/validation/master-vv-matrix.yaml
project/backlog/procurement-template.yaml
project/context/conversation-context-2026-08-11.md
project/agents-operating-model.md
n8n/docs/architecture.md
```

Repositorio sensores:

```text
/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil/README.md
/home/chuchosam/Documentos/github/invernadero/green-house/xiao-esp32c3-soil/src/main.cpp
/home/chuchosam/Documentos/github/invernadero/green-house/docs/data-contracts.md
/home/chuchosam/Documentos/github/invernadero/green-house/docs/device-inventory.md
/home/chuchosam/Documentos/github/invernadero/green-house/docs/system-flow.md
```

No leer por defecto:

- todas las HU congeladas completas;
- archivos de la web no relacionados con el caso de suelo;
- credenciales, secrets o archivos locales sensibles.

### 6. Orchestrator

Entrada:

- solicitud normalizada;
- registry;
- resumen de capacidades de agentes;
- contexto minimo.

Decision esperada para recomendacion general de backlog:

```yaml
route:
  primary_agent: AGENT-BKL-001
  supporting_agents:
  - AGENT-KNOW-001
  - AGENT-REF-001
  reason: La solicitud requiere evaluar estado, prioridad, dependencias, WIP y siguiente accion recomendada.
  authority: A1
  review_required: true
```

Decision esperada para refinamiento del sensor de suelo:

```yaml
route:
  primary_agent: AGENT-REF-001
  supporting_agents:
  - AGENT-KNOW-001
  - AGENT-BKL-001
  reason: La solicitud requiere refinamiento de backlog, pruebas V&V, materiales y DoR/DoD.
  authority: A1
  review_required: true
```

Restricciones:

- no aprobar el resultado como final;
- no marcar items como DONE;
- no modificar HU congeladas;
- no proponer reimplementar firmware RS485 ya existente.

### 7. Specialized Agent

Agente:

```text
AGENT-REF-001 - Refinement Agent
```

Objetivo:

```text
Refinar HU-SOIL-001 en tareas de validacion, criterios, pruebas, materiales,
riesgos, evidencias y DoR/DoD.
```

Debe producir:

- backlog de tareas `T-SOIL-001..T-SOIL-009`;
- criterios de aceptacion;
- pruebas V&V;
- materiales/procurement;
- supuestos;
- riesgos;
- preguntas abiertas;
- evidencia consultada;
- recomendacion de siguiente accion.

Debe reconocer explicitamente:

```text
El sensor de suelo 7-en-1 esta OPERATIONAL, pero VALIDATION PENDING.
```

Debe evitar:

```text
Reimplementar firmware, pinout, RS485, Modbus o contrato MQTT ya existente sin evidencia de falla.
```

### 8. Reviewer

Responsabilidad:

- validar estructura contra `agents/shared/contracts.yaml`;
- validar reglas contra `agents/shared/project-rules.yaml`;
- detectar claims no soportados;
- detectar cambios indebidos sobre baselines congeladas;
- verificar que la salida sea borrador revisable.

Checklist minimo:

```yaml
checks:
  frozen_baselines_not_modified: true
  no_reimplementation_of_operational_soil_sensor: true
  validation_focus: true
  evidence_references_present: true
  procurement_requires_human_approval: true
  review_required_preserved: true
  output_contract_valid: true
```

### 9. Human Approval Gate

Regla:

- El workflow puede persistir borradores.
- El workflow no debe convertir borradores en artefactos finales sin aprobacion humana.

Estados permitidos:

```text
DRAFT
REVIEW_REQUESTED
APPROVED_BY_HUMAN
REJECTED
NEEDS_CHANGES
```

Para el primer caso:

```text
Estado esperado: DRAFT o REVIEW_REQUESTED
```

### 10. Persist Draft Artifact

Ruta recomendada del primer borrador:

```text
project/backlog/drafts/HU-SOIL-001-validation-backlog-draft.yaml
```

El archivo debe incluir:

```yaml
task_id: EN-AGENT-001-AC-001
status: DRAFT
source_story: HU-SOIL-001
generated_by: AGENT-REF-001
review_required: true
human_approval_required_for_final: true
```

### 11. Git Status Summary

Al final, n8n debe devolver:

```json
{
  "draft_created": true,
  "artifact_path": "project/backlog/drafts/HU-SOIL-001-validation-backlog-draft.yaml",
  "requires_human_review": true,
  "git_status_summary": "modified/untracked files listed here"
}
```

No hacer commit automatico en este primer workflow.

## Primer caso de aceptacion

Solicitud:

```text
Construir backlog de validacion del sensor de suelo 7-en-1
```

Criterios:

- reconoce `OPERATIONAL / VALIDATION PENDING`;
- no reimplementa RS485/firmware existente;
- propone `T-SOIL-001..T-SOIL-009`;
- genera materiales/procurement;
- produce borrador revisable;
- conserva revision humana;
- referencia evidencia de repos central y sensores;
- no toca HU congeladas.

## Caso principal del sistema

Solicitud:

```text
Recomendar siguiente trabajo del backlog segun prioridad, WIP, tiempo disponible y modo de trabajo.
```

Criterios:

- lee estado del backlog completo;
- devuelve maximo 3 opciones;
- explica por que cada opcion es conveniente;
- distingue trabajo humano, autonomo de agente y mixto;
- no mueve estados sin aprobacion humana;
- permite elegir una opcion y continuar hacia refinamiento;
- pregunta una sola cosa al humano.

## Salida esperada del agente

Contrato:

```yaml
output:
  task_id: EN-AGENT-001-AC-001
  agent_id: AGENT-REF-001
  status: SUCCESS|PARTIAL|BLOCKED|FAILED
  summary: string
  artifacts:
  - project/backlog/drafts/HU-SOIL-001-validation-backlog-draft.yaml
  decisions: []
  assumptions:
  - string
  risks:
  - string
  evidence:
  - string
  open_questions:
  - string
  recommended_next_action: string
```

## Riesgos

- n8n puede tener acceso local amplio; aplicar minimo privilegio por carpeta/comando.
- No exponer secrets de firmware ni credenciales de MQTT/WiFi.
- No mezclar borrador con final aprobado.
- No permitir que Orchestrator sustituya al agente especializado.
- No hacer commits automaticos hasta que el flujo de revision este probado.

## Definition of Done para EN-AGENT-001 minimo

- Workflow creado en n8n local.
- Workflow lee reglas, registry, backlog y modelo operativo desde Git.
- Workflow puede recomendar siguiente trabajo del backlog completo.
- Humano puede seleccionar una opcion.
- Workflow puede enrutar a Refinement Agent, Backlog Agent u otro agente competente.
- Workflow puede generar borradores revisables.
- Reviewer valida reglas principales.
- Humano puede aprobar/rechazar o pedir cambios.
- Git queda como fuente de verdad de los artefactos persistidos.
