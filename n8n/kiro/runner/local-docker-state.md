# Local Docker State - agent-runner

Estado observado: 2026-08-12

## Archivos locales fuera de este repositorio

```text
/home/chuchosam/docker/n8n/docker-compose.yml
/home/chuchosam/docker/n8n/agent-runner/Dockerfile
```

## Cambios aplicados

`agent-runner/Dockerfile`:

- Instala `unzip`.
- Instala Kiro CLI con `curl -fsSL https://cli.kiro.dev/install | bash`.
- Copia `kiro-cli*` desde `/home/agent/.local/bin` hacia `/usr/local/bin`.
- Arranca `python3 /workspace/work/kiro-runner/kiro_runner.py` como comando principal.

Motivo: el volumen `agent_home:/home/agent` oculta lo instalado bajo `/home/agent`
durante el build; por eso los binarios deben quedar disponibles en `/usr/local/bin`.

`docker-compose.yml`:

- Monta el repo central en `/home/chuchosam/Documentos/github/invernadero-central`.
- Monta sensores/edge en `/home/chuchosam/Documentos/github/invernadero/green-house`.
- Monta web UI en `/home/chuchosam/Documentos/github/agrotechia-web-ui`.

## Validacion

```text
docker compose build agent-runner
docker compose up -d agent-runner
docker exec agent-runner kiro-cli --version
docker exec agent-runner curl -s http://127.0.0.1:8080/health
curl -s -X POST -H 'Content-Type: application/json' \
  --data @n8n/workflows/inputs/AGENT-REF-001-example.json \
  http://localhost:5678/webhook/project-refinement
```

Resultados:

```text
kiro-cli 2.18.0
runner health: OK
AGENT-REF-001 dry_run: SUCCESS
repos mounted: OK
```

## Pendiente

`KIRO_API_KEY` dentro de `agent-runner` sigue como placeholder. No ejecutar
`dry_run: false` hasta configurar una key real en `/home/chuchosam/docker/n8n/.env`
o enviar `Authorization: Bearer <KIRO_API_KEY>` desde n8n.

El workflow `AGENT-REF-001` referencia la credencial n8n `n8n` de tipo
`httpHeaderAuth`.

```text
Name: Authorization
Value: Bearer <KIRO_API_KEY>
```

Validacion posterior:

```text
auth.source: authorization_header
kiro-cli: project-refinement workspace agent discovered
live execution: SUCCESS
```

Nota: en modo no interactivo, la persistencia directa por `fs_write` fue rechazada.
Esto es deseable para AGENT-REF-001: el agente devuelve el DRAFT y la escritura final
debe pasar por aprobación humana/n8n.
