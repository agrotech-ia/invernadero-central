# Importar workflows en n8n local

## Orchestrator

Workflow preparado:

```text
n8n/workflows/imports/AGENT-ORCH-001.workflow.json
```

Nombre esperado en n8n:

```text
AGENT-ORCH-001 - Orchestrator
```

## Importacion manual

1. Abrir n8n local:

```text
http://localhost:5678
```

2. Entrar al workflow destino o crear uno nuevo.
3. Usar la opcion de importar desde archivo.
4. Seleccionar:

```text
/home/chuchosam/Documentos/github/invernadero-central/n8n/workflows/imports/AGENT-ORCH-001.workflow.json
```

5. Ejecutar el workflow manualmente.

## Requisito de filesystem

El nodo `Load Project Context` ejecuta:

```text
cd /home/chuchosam/Documentos/github/invernadero-central && node n8n/scripts/agent_orchestrator_context.js
```

Por tanto, el contenedor de n8n debe poder ver esa ruta.

Si n8n corre dentro de Docker y no tiene montado el repo central, montar el repositorio en el
contenedor o ajustar el comando/ruta al path visible dentro del contenedor.

## Importacion por API

La API local requiere header:

```text
X-N8N-API-KEY
```

Durante la prueba, n8n respondio `unauthorized` con la key disponible. Para importar por API se
requiere una API key valida de la instancia actual.

Comando base, sin incluir secrets:

```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: <N8N_API_KEY>" \
  -H "Content-Type: application/json" \
  --data-binary @n8n/workflows/imports/AGENT-ORCH-001.workflow.json
```

## Validacion local

Desde el repo central:

```bash
jq . n8n/workflows/imports/AGENT-ORCH-001.workflow.json
node n8n/scripts/agent_orchestrator_context.js | jq '.request, .repositories, (.central_context | length)'
```
