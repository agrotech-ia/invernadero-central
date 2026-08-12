# KIRO-BRIDGE-001 - n8n to Kiro runner bridge

Estado: DRAFT

## Objetivo

Permitir que n8n invoque agentes Kiro de workspace usando Kiro CLI en modo headless.

Segun la documentacion oficial de Kiro CLI, la API key se usa configurando `KIRO_API_KEY`
y ejecutando:

```bash
kiro-cli chat --no-interactive "your prompt here"
```

## Arquitectura recomendada

```text
n8n Chat Gateway
-> Orchestrator
-> Backlog/Refinement workflow
-> HTTP Request to agent-runner
-> agent-runner sets KIRO_API_KEY
-> kiro-cli chat --agent <agent> --no-interactive <prompt>
-> response to n8n
-> draft artifact / human approval
```

## Por que no llamar Kiro directo desde n8n

- Kiro documenta el modo headless mediante CLI y variable `KIRO_API_KEY`.
- El nodo `Execute Command` no esta disponible en la instancia local de n8n.
- Por seguridad, la API key no debe guardarse en Git.
- El `agent-runner` puede aislar permisos, directorio de trabajo y escritura.

## Variables esperadas

```text
KIRO_API_KEY
KIRO_WORKSPACE=/home/chuchosam/Documentos/github/invernadero-central
KIRO_AGENT=project-refinement
```

## Endpoint sugerido del runner

```text
POST /kiro/run
```

Payload:

```json
{
  "agent": "project-refinement",
  "workspace": "/home/chuchosam/Documentos/github/invernadero-central",
  "prompt": "Refina EN-AGENT-001 como DRAFT usando project/backlog/templates/hu-template.yaml",
  "mode": "draft",
  "approval_required": true
}
```

Respuesta:

```json
{
  "status": "SUCCESS|PARTIAL|BLOCKED|FAILED",
  "agent": "project-refinement",
  "summary": "string",
  "stdout": "string",
  "stderr": "string",
  "artifacts": ["path"],
  "requires_human_review": true
}
```

## Primer caso

Invocar:

```text
project-refinement
```

Con objetivo:

```text
Refinar EN-AGENT-001 en HUs/tareas granulares para completar el ciclo multiagente.
```
