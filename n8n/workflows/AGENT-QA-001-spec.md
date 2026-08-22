# AGENT-QA-001 - Kiro QA Evidence Workflow

Estado: DRAFT

## Objetivo

Invocar `project-qa-evidence`, agente encargado de definir pruebas, revisar evidencia y bloquear DONE si falta prueba.

Para sensores y laboratorio debe aplicar `project/validation/sensor-test-rigor.yaml`:

- separar respuesta funcional, caracterizacion y calibracion;
- no aceptar respuesta funcional como exactitud o calibracion;
- exigir referencia independiente cuando se pida calibracion, precision o "que tan bien mide";
- registrar condiciones, repeticiones, evidencia esperada y limitaciones.

## Flujo

```text
Webhook /project-qa-evidence
-> Build Kiro QA Request
-> Call Kiro Runner
```

## Endpoint n8n

```text
POST /webhook/project-qa-evidence
```

## Nota

La salida es DRAFT y requiere aprobacion humana para persistencia, cambios de estado, compras, despliegues criticos o control fisico.
