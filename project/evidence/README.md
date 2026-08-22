# Evidencia Del Proyecto

Esta carpeta guarda evidencia verificable para avanzar HUs, enablers, tareas,
experimentos y decisiones del proyecto.

La regla principal es simple: no se marca `DONE` sin evidencia proporcional al tipo de
trabajo y sin revision.

## Como Guardar Evidencia

Cada evidencia debe indicar, como minimo:

- item relacionado: `EN-EDGE-001`, `HU-SOIL-001`, `T-QA-001`, etc.;
- fecha;
- responsable o agente;
- comando, fuente o procedimiento usado;
- resultado;
- limitaciones conocidas;
- siguiente accion si el resultado es `FAIL` o `PARTIAL`.

## Tipos De Evidencia

### Codigo

Usar para scripts, firmware, frontend, backend, workflows o configuracion ejecutable.

Ejemplos:

- commit hash;
- resumen de diff;
- salida de tests;
- salida de build;
- logs de ejecucion local.

### Sensor

Usar para lecturas, payloads, logs seriales o archivos generados por sensores.

Ejemplos:

- payload MQTT;
- archivo JSONL;
- log serial;
- captura o nota de lectura.

### Database

Usar para schema, migraciones, inserts, queries o persistencia.

Ejemplos:

- query ejecutada;
- row count;
- resultado de `docker compose ps`;
- salida de bootstrap/migration.

### Edge

Usar para Raspberry, Mosquitto, Docker, ingesta, servicios y health checks.

Ejemplos:

- salida de pub/sub MQTT;
- log del ingestor;
- estado de contenedores;
- healthcheck.

### Web

Usar para dashboard, UI, integracion API, build y pruebas frontend.

Ejemplos:

- salida de `npm run build`;
- salida de tests;
- screenshot;
- respuesta API usada por la UI.

### Hardware

Usar para cableado, potencia, bombas, valvulas, actuadores o mediciones fisicas.

Ejemplos:

- checklist de seguridad;
- nota de cableado;
- medicion con instrumento;
- aprobacion humana antes de control fisico.

### Documentacion

Usar para guias, runbooks, ADRs, troubleshooting y manuales de uso.

Ejemplos:

- guia con `source_refs`;
- runbook validado;
- ADR;
- lista de `UNKNOWN` o limitaciones.

### Agentes

Usar para workflows n8n, agentes Kiro, runner y chat routing.

Ejemplos:

- respuesta de webhook en `dry_run`;
- respuesta live;
- `agent-runner /health`;
- ID de workflow n8n publicado.

### Decision

Usar para aprobaciones humanas, decisiones tecnicas, alcance o seguridad.

Ejemplos:

- entrada en `project/decisions/decision-register.yaml`;
- nota de aprobacion humana;
- ADR;
- decision de scope.

## Niveles De Evidencia

- `L0_NOTE`: nota o contexto. No basta para `DONE`.
- `L1_STATIC`: archivo, schema, documento o captura versionada.
- `L2_LOCAL_RUN`: comando local, test, build o dry-run reproducible.
- `L3_INTEGRATION`: prueba entre componentes conectados.
- `L4_FIELD_LAB`: prueba con hardware, sensores o actuadores.
- `L5_OPERATIONAL`: evidencia de operacion continua o estabilidad.

## Reglas De Seguridad

- No guardar secretos, tokens, passwords, `.env` reales ni credenciales.
- No guardar datos sensibles innecesarios.
- Para archivos grandes, guardar una referencia y no copiar el binario al repo.
- Para control fisico, compras o despliegues criticos, registrar aprobacion humana.

## Relacion Con QA/V&V

La taxonomia formal vive en:

```text
project/validation/evidence-taxonomy.yaml
```

Las plantillas viven en:

```text
project/validation/templates/
```

Cada HU/enabler deberia tener un evidence index y, antes de `DONE`, un validation report.
