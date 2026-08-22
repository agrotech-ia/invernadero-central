# Agent Work Artifacts

Esta carpeta contiene artefactos intermedios por HU/enabler para que los agentes no dependan de
memoria conversacional.

Ruta por item:

```text
project/agent-work/<backlog_id>/
```

Archivos recomendados:

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
- `shared-contract.yaml` solo debe existir cuando Discovery recomiende contrato compartido.
- Los artefactos son DRAFT hasta que pasen review y aprobacion humana.
- No se debe marcar una HU como `READY`, `VALIDATION` o `DONE` solo por existir estos archivos.
