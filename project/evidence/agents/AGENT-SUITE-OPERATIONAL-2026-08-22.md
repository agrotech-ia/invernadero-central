# Evidencia: suite multiagente operativa

Fecha: 2026-08-22

## Resultado

Se dejo operativa la suite local de agentes del proyecto Invernadero Central sobre n8n + agent-runner + Kiro CLI.

## Validaciones realizadas

- `agent-runner` reiniciado y validado desde n8n por `http://agent-runner:8080/health`.
- Kiro CLI disponible en runner: `kiro-cli 2.18.0`.
- Workspaces disponibles en runner:
  - `/home/chuchosam/Documentos/github/invernadero-central`
  - `/home/chuchosam/Documentos/github/invernadero/green-house`
  - `/home/chuchosam/Documentos/github/agrotechia-web-ui`
- Workflows n8n importados y publicados.
- Webhooks de agentes validados en `dry_run`.
- Chat gateway validado con enrutamiento a backlog, refinement/edge, knowledge y web.

## Agentes validados

- `AGENT-ORCH-001` -> `/webhook/project-orchestrator`
- `AGENT-KNOW-001` -> `/webhook/project-knowledge`
- `AGENT-BKL-001` -> `/webhook/project-backlog`
- `AGENT-PLAN-001` -> `/webhook/project-planning`
- `AGENT-PMO-001` -> `/webhook/project-pmo`
- `AGENT-REF-001` -> `/webhook/project-refinement`
- `AGENT-ARCH-001` -> `/webhook/project-architecture`
- `AGENT-ENG-001` -> `/webhook/project-engineering`
- `AGENT-QA-001` -> `/webhook/project-qa-evidence`
- `AGENT-REV-001` -> `/webhook/project-reviewer-safety`
- `AGENT-PROD-001` -> `/webhook/project-product`
- `AGENT-MKT-001` -> `/webhook/project-market-intelligence`
- `AGENT-GROW-001` -> `/webhook/project-growth-content`
- `AGENT-EDGE-001` -> `/webhook/project-edge`
- `AGENT-WEB-001` -> `/webhook/project-web`
- `AGENT-HW-001` -> `/webhook/project-hardware`

## Chat gateway

Endpoint: `/webhook/project-agent-chat`

Rutas probadas en `dry_run`:

- "recomienda siguiente trabajo del backlog" -> `project-backlog`
- "necesito refinar EN-EDGE-001" -> `project-edge`
- "que sabemos del estado actual del proyecto" -> `project-knowledge`
- "prepara trabajo para el dashboard web con telemetria real" -> `project-web`

## Guardas

- Los workflows trabajan en modo DRAFT por defecto.
- La persistencia, cambios de Kanban, cambios de backlog, compras, despliegues criticos y control fisico requieren aprobacion humana.
- La API key de Kiro se consume desde credencial n8n o entorno del runner; no se guarda en Git.

## Observaciones

- Planning y Refinement ya existian en n8n con IDs historicos. Se corrigieron los imports para conservar esos IDs en futuras importaciones.
- n8n no expone comando `delete:workflow` en este runtime; los duplicados creados por una importacion previa quedan sin usar y los workflows correctos fueron publicados.
