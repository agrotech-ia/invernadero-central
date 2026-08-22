import http from 'node:http';
import { spawn, spawnSync } from 'node:child_process';

const HOST = process.env.KIRO_RUNNER_HOST || '127.0.0.1';
const PORT = Number(process.env.KIRO_RUNNER_PORT || 8080);
const KIRO_CLI_BIN = process.env.KIRO_CLI_BIN || 'kiro-cli';
const KIRO_TRUST_TOOLS = process.env.KIRO_TRUST_TOOLS || 'fs_read,grep';
const MAX_PROMPT_LENGTH = 20000;

const WORKSPACES = new Map([
  ['central', '/home/chuchosam/Documentos/github/invernadero-central'],
  ['sensors', '/home/chuchosam/Documentos/github/invernadero/green-house'],
  ['web', '/home/chuchosam/Documentos/github/agrotechia-web-ui'],
]);

const AGENTS = new Set([
  'project-backlog',
  'project-orchestrator',
  'project-knowledge',
  'project-pmo',
  'project-planning',
  'project-refinement',
  'project-reviewer-safety',
  'project-architecture',
  'project-engineering',
  'project-qa-evidence',
  'project-product',
  'project-market-intelligence',
  'project-growth-content',
  'project-edge',
  'project-web',
  'project-hardware',
]);

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
  });
  response.end(JSON.stringify(payload));
}

function readBody(request) {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1024 * 256) {
        request.destroy();
        reject(new Error('request_body_too_large'));
      }
    });
    request.on('end', () => resolve(body));
    request.on('error', reject);
  });
}

function getAuthApiKey(request) {
  const header = request.headers.authorization || '';
  const match = header.match(/^Bearer\s+(.+)$/i);
  return match ? match[1].trim() : '';
}

function normalizeApiKey(value) {
  const apiKey = String(value || '').trim();
  if (!apiKey || apiKey === 'TU_KIRO_API_KEY') {
    return '';
  }
  return apiKey;
}

function getKiroApiKey(request) {
  const headerKey = normalizeApiKey(getAuthApiKey(request));
  if (headerKey) {
    return { apiKey: headerKey, source: 'authorization_header' };
  }

  const envKey = normalizeApiKey(process.env.KIRO_API_KEY);
  if (envKey) {
    return { apiKey: envKey, source: 'environment' };
  }

  return { apiKey: '', source: 'missing' };
}

function getKiroStatus() {
  const result = spawnSync(KIRO_CLI_BIN, ['--version'], {
    encoding: 'utf8',
    timeout: 5000,
  });

  return {
    cli_bin: KIRO_CLI_BIN,
    available: result.status === 0,
    version: result.status === 0 ? String(result.stdout || result.stderr).trim() : null,
    error: result.status === 0 ? null : String(result.stderr || result.error?.message || '').trim(),
  };
}

function resolveWorkspace(value) {
  if (!value) {
    return WORKSPACES.get('central');
  }

  if (WORKSPACES.has(value)) {
    return WORKSPACES.get(value);
  }

  for (const allowedPath of WORKSPACES.values()) {
    if (value === allowedPath) {
      return allowedPath;
    }
  }

  return null;
}

function validatePayload(payload) {
  const errors = [];
  const agent = String(payload.agent || '').trim();
  const prompt = String(payload.prompt || '').trim();
  const workspace = resolveWorkspace(payload.workspace || 'central');

  if (!AGENTS.has(agent)) {
    errors.push('agent_not_allowed');
  }

  if (!workspace) {
    errors.push('workspace_not_allowed');
  }

  if (!prompt) {
    errors.push('prompt_required');
  }

  if (prompt.length > MAX_PROMPT_LENGTH) {
    errors.push('prompt_too_large');
  }

  return {
    valid: errors.length === 0,
    errors,
    agent,
    prompt,
    workspace,
  };
}

function runKiro({ agent, prompt, workspace, apiKey }) {
  return new Promise((resolve) => {
    const startedAt = Date.now();
    const child = spawn(KIRO_CLI_BIN, ['chat', '--agent', agent, '--no-interactive', `--trust-tools=${KIRO_TRUST_TOOLS}`, prompt], {
      cwd: workspace,
      env: {
        ...process.env,
        KIRO_API_KEY: apiKey,
      },
      shell: false,
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    child.on('error', (error) => {
      resolve({
        status: 'FAILED',
        exit_code: null,
        duration_ms: Date.now() - startedAt,
        stdout,
        stderr,
        error: error.message,
      });
    });

    child.on('close', (exitCode) => {
      resolve({
        status: exitCode === 0 ? 'SUCCESS' : 'FAILED',
        exit_code: exitCode,
        duration_ms: Date.now() - startedAt,
        stdout,
        stderr,
        error: exitCode === 0 ? null : 'kiro_cli_failed',
      });
    });
  });
}

async function handleRun(request, response) {
  let payload;

  try {
    payload = JSON.parse(await readBody(request));
  } catch (error) {
    sendJson(response, 400, {
      status: 'FAILED',
      error: 'invalid_json',
      detail: error.message,
    });
    return;
  }

  const validation = validatePayload(payload);
  if (!validation.valid) {
    sendJson(response, 400, {
      status: 'FAILED',
      errors: validation.errors,
    });
    return;
  }

  const { apiKey, source: apiKeySource } = getKiroApiKey(request);
  if (!apiKey && !payload.dry_run) {
    sendJson(response, 401, {
      status: 'FAILED',
      error: 'kiro_api_key_required',
    });
    return;
  }

  const command = {
    bin: KIRO_CLI_BIN,
    args: ['chat', '--agent', validation.agent, '--no-interactive', `--trust-tools=${KIRO_TRUST_TOOLS}`, validation.prompt],
    cwd: validation.workspace,
  };

  if (payload.dry_run) {
    sendJson(response, 200, {
      status: 'SUCCESS',
      dry_run: true,
      agent: validation.agent,
      workspace: validation.workspace,
      command,
      auth: {
        kiro_api_key_present: Boolean(apiKey),
        source: apiKeySource,
      },
      requires_human_review: payload.approval_required !== false,
    });
    return;
  }

  const result = await runKiro({
    agent: validation.agent,
    prompt: validation.prompt,
    workspace: validation.workspace,
    apiKey,
  });

  sendJson(response, result.status === 'SUCCESS' ? 200 : 500, {
    ...result,
    agent: validation.agent,
    workspace: validation.workspace,
    auth: {
      kiro_api_key_present: Boolean(apiKey),
      source: apiKeySource,
    },
    requires_human_review: payload.approval_required !== false,
  });
}

function createServer() {
  return http.createServer(async (request, response) => {
    const url = new URL(request.url, `http://${request.headers.host || `${HOST}:${PORT}`}`);

    if (request.method === 'GET' && url.pathname === '/health') {
      sendJson(response, 200, {
        status: 'OK',
        service: 'kiro-runner',
        kiro: getKiroStatus(),
        agents: Array.from(AGENTS),
        workspaces: Object.fromEntries(WORKSPACES),
      });
      return;
    }

    if (request.method === 'POST' && url.pathname === '/kiro/run') {
      await handleRun(request, response);
      return;
    }

    sendJson(response, 404, {
      status: 'FAILED',
      error: 'not_found',
    });
  });
}

if (process.argv.includes('--check')) {
  console.log(JSON.stringify({
    status: 'OK',
    service: 'kiro-runner',
    kiro: getKiroStatus(),
    agents: Array.from(AGENTS),
    workspaces: Object.fromEntries(WORKSPACES),
  }, null, 2));
} else {
  createServer().listen(PORT, HOST, () => {
    console.log(`kiro-runner listening on http://${HOST}:${PORT}`);
  });
}
