# Kiro Runner

HTTP bridge for n8n to invoke Kiro CLI workspace agents.

## Endpoints

```text
GET /health
POST /kiro/run
```

## Start

Node runtime:

```bash
cd /home/chuchosam/Documentos/github/invernadero-central/n8n/kiro/runner
KIRO_API_KEY=ksk_xxxxx npm start
```

Python runtime, useful for the current `agent-runner` container:

```bash
KIRO_RUNNER_HOST=0.0.0.0 KIRO_API_KEY=ksk_xxxxx python3 kiro_runner.py
```

If running inside the existing Docker Compose network, start it from the `agent-runner`
service and keep port `8080` listening inside the container:

```bash
KIRO_RUNNER_HOST=0.0.0.0 KIRO_API_KEY=ksk_xxxxx python3 /workspace/work/kiro-runner/kiro_runner.py
```

n8n should call:

```text
http://agent-runner:8080/kiro/run
```

For live execution, the Kiro key can be provided either as `KIRO_API_KEY` in the
runner environment or as an `Authorization: Bearer <KIRO_API_KEY>` header from n8n.

The local Docker image promotes the installed `kiro-cli*` binaries to `/usr/local/bin`
because the Compose volume `agent_home:/home/agent` hides files installed under
`/home/agent` during image build.

The local Compose service mounts the three project repositories at their host paths:

```text
/home/chuchosam/Documentos/github/invernadero-central
/home/chuchosam/Documentos/github/invernadero/green-house
/home/chuchosam/Documentos/github/agrotechia-web-ui
```

For a safe connectivity check without a key or Kiro CLI execution:

```bash
npm run check
```

## Run Request

```bash
curl -X POST http://127.0.0.1:8080/kiro/run \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <KIRO_API_KEY>' \
  --data @../requests/refine-en-agent-001.json
```

## Dry Run

Set `dry_run: true` in the payload to validate routing and command construction without executing Kiro.

## Security

- The API key must come from `KIRO_API_KEY` env or `Authorization: Bearer ...`.
- `Authorization: Bearer ...` takes precedence over `KIRO_API_KEY` so n8n credentials
  can override local placeholders safely.
- The placeholder value `TU_KIRO_API_KEY` is treated as missing.
- API keys are not stored in Git.
- Agents and workspaces are whitelisted.
- Kiro headless runs with `--trust-tools=read,grep` by default. Override with
  `KIRO_TRUST_TOOLS` only after explicit human approval.
- The runner uses `spawn` with argument arrays, not shell interpolation.
- Physical control, purchases, critical deployments, and final approvals remain human-gated.
