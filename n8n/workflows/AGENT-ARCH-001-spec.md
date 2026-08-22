# AGENT-ARCH-001 - Kiro Architecture Review Workflow

Estado: DRAFT

## Objetivo

Invocar `project-architecture`, agente encargado de revisar arquitectura, impacto tecnico, contratos y ADRs.

## Flujo

```text
Webhook /project-architecture
-> Build Kiro ARCH Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-architecture
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
