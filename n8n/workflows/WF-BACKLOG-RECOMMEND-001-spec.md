# WF-BACKLOG-RECOMMEND-001 - Recomendacion de siguiente trabajo

Estado: DRAFT  
Proposito: permitir que el humano elija rapidamente que HU/enabler tomar segun prioridad,
tiempo disponible, tipo de trabajo y estado real del proyecto.

## Objetivo

El workflow debe responder:

```text
Que deberia trabajar ahora?
```

No debe ejecutar cambios todavia. Solo recomienda opciones y pide una decision humana.

## Flujo actual

```text
Webhook /project-backlog
-> Build Kiro Backlog Request
-> Call Kiro Runner
```

El workflow llama al workspace agent Kiro `project-backlog`; debe leer backlog y
Kanban en vivo desde Git, no usar snapshots quemados en el workflow.

## Input

```json
{
  "available_time": "short|medium|long|unknown",
  "preferred_mode": "quick_win|deep_work|physical_lab|coding|docs_governance|market_growth|any",
  "max_options": 3,
  "respect_wip": true
}
```

## Contexto a leer

```text
agents/shared/project-rules.yaml
agents/shared/contracts.yaml
agents/registry.yaml
agents/backlog/agent.yaml
agents/knowledge/agent.yaml
agents/refinement/agent.yaml
project/backlog/master-backlog.yaml
project/kanban/board.yaml
project/backlog/templates/hu-template.yaml
project/roles/expert-role-catalog.yaml
project/roadmap/roadmap-6-months.yaml
project/validation/master-vv-matrix.yaml
project/inventory/master-inventory-v2.yaml
project/context/conversation-context-2026-08-11.md
project/agents-operating-model.md
```

## Agentes

Primario:

```text
AGENT-BKL-001
```

Soporte:

```text
AGENT-KNOW-001
AGENT-REF-001
AGENT-ARCH-001 cuando haya impacto tecnico/arquitectonico
AGENT-QA-001 cuando exista o falte evidencia
```

## Salida esperada

```yaml
task_id: WF-BACKLOG-RECOMMEND-001
agent_id: AGENT-BKL-001
status: SUCCESS
summary: string
recommended_options:
- backlog_id: string
  title: string
  current_status: string
  priority: P0/P1/P2
  role: string
  why_now: string
  estimated_effort: XS/S/M/L
  mode_fit:
  - quick_win|deep_work|physical_lab|coding|docs_governance|market_growth
  dependencies:
  - string
  blockers:
  - string
  next_step: string
requires_human_selection: true
question_for_human: "Cual opcion quieres tomar ahora?"
```

## Regla de interaccion

El workflow debe hacer una sola pregunta al humano al final.

No debe preguntar 20 cosas en una misma salida.

## Criterios de aceptacion

- Devuelve maximo 3 opciones.
- Respeta WIP.
- Explica por que recomienda cada opcion.
- Distingue trabajo humano, trabajo autonomo de agente y trabajo mixto.
- Advierte si una opcion necesita desglose granular antes de ejecucion.
- Usa rol experto y rol revisor para cada recomendacion.
- No mueve estados del backlog.
- No crea commits.
- No toca HU congeladas.
