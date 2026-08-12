#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const CENTRAL_REPO = '/home/chuchosam/Documentos/github/invernadero-central';
const SENSOR_REPO = '/home/chuchosam/Documentos/github/invernadero/green-house';
const WEB_REPO = '/home/chuchosam/Documentos/github/agrotechia-web-ui';

function readText(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    return `__READ_ERROR__: ${error.message}`;
  }
}

function readRepoFile(repo, relativePath) {
  return {
    path: path.join(repo, relativePath),
    relative_path: relativePath,
    content: readText(path.join(repo, relativePath)),
  };
}

function readJson(filePath, fallback) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (_error) {
    return fallback;
  }
}

const defaultRequest = {
  task_id: 'WF-BACKLOG-RECOMMEND-001',
  request: 'Recomendar siguiente trabajo del backlog',
  requested_by: 'human',
  available_time: 'unknown',
  preferred_mode: 'any',
  max_options: 3,
  respect_wip: true,
};

const requestPath = path.join(
  CENTRAL_REPO,
  'n8n/workflows/inputs/WF-BACKLOG-RECOMMEND-001-request.json',
);

const payload = {
  generated_at: new Date().toISOString(),
  request: readJson(requestPath, defaultRequest),
  repositories: {
    central: CENTRAL_REPO,
    sensors_edge_data: SENSOR_REPO,
    web: WEB_REPO,
  },
  central_context: [
    readRepoFile(CENTRAL_REPO, 'agents/shared/project-rules.yaml'),
    readRepoFile(CENTRAL_REPO, 'agents/shared/contracts.yaml'),
    readRepoFile(CENTRAL_REPO, 'agents/registry.yaml'),
    readRepoFile(CENTRAL_REPO, 'agents/orchestrator/agent.yaml'),
    readRepoFile(CENTRAL_REPO, 'agents/backlog/agent.yaml'),
    readRepoFile(CENTRAL_REPO, 'agents/knowledge/agent.yaml'),
    readRepoFile(CENTRAL_REPO, 'agents/refinement/agent.yaml'),
    readRepoFile(CENTRAL_REPO, 'project/backlog/master-backlog.yaml'),
    readRepoFile(CENTRAL_REPO, 'project/kanban/board.yaml'),
    readRepoFile(CENTRAL_REPO, 'project/roles/expert-role-catalog.yaml'),
    readRepoFile(CENTRAL_REPO, 'project/agents-operating-model.md'),
    readRepoFile(CENTRAL_REPO, 'project/context/conversation-context-2026-08-11.md'),
  ],
  sensor_context_refs: [
    path.join(SENSOR_REPO, 'docs/data-contracts.md'),
    path.join(SENSOR_REPO, 'docs/device-inventory.md'),
    path.join(SENSOR_REPO, 'xiao-esp32c3-soil/README.md'),
  ],
  web_context_refs: [
    path.join(WEB_REPO, 'src/data/mockDashboard.js'),
    path.join(WEB_REPO, 'src/App.jsx'),
  ],
};

process.stdout.write(JSON.stringify(payload, null, 2));
