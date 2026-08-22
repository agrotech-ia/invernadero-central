#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = os.environ.get("KIRO_RUNNER_HOST", "0.0.0.0")
PORT = int(os.environ.get("KIRO_RUNNER_PORT", "8080"))
KIRO_CLI_BIN = os.environ.get("KIRO_CLI_BIN", "kiro-cli")
KIRO_TRUST_TOOLS = os.environ.get("KIRO_TRUST_TOOLS", "fs_read,grep")
MAX_PROMPT_LENGTH = 20000

WORKSPACES = {
    "central": "/home/chuchosam/Documentos/github/invernadero-central",
    "sensors": "/home/chuchosam/Documentos/github/invernadero/green-house",
    "web": "/home/chuchosam/Documentos/github/agrotechia-web-ui",
}

AGENTS = {
    "project-backlog",
    "project-contract",
    "project-discovery",
    "project-documentation",
    "project-orchestrator",
    "project-knowledge",
    "project-pmo",
    "project-planning",
    "project-refinement",
    "project-reviewer-safety",
    "project-architecture",
    "project-engineering",
    "project-qa-evidence",
    "project-product",
    "project-market-intelligence",
    "project-growth-content",
    "project-edge",
    "project-web",
    "project-hardware",
}


def kiro_status():
    if not shutil.which(KIRO_CLI_BIN):
        return {
            "cli_bin": KIRO_CLI_BIN,
            "available": False,
            "version": None,
            "error": "kiro-cli_not_found",
        }

    try:
        result = subprocess.run(
            [KIRO_CLI_BIN, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except Exception as exc:
        return {
            "cli_bin": KIRO_CLI_BIN,
            "available": False,
            "version": None,
            "error": str(exc),
        }

    return {
        "cli_bin": KIRO_CLI_BIN,
        "available": result.returncode == 0,
        "version": (result.stdout or result.stderr).strip() if result.returncode == 0 else None,
        "error": None if result.returncode == 0 else (result.stderr or "kiro_cli_failed").strip(),
    }


def send_json(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def resolve_workspace(value):
    if not value:
        return WORKSPACES["central"]
    if value in WORKSPACES:
        return WORKSPACES[value]
    if value in WORKSPACES.values():
        return value
    return None


def validate_payload(payload):
    errors = []
    agent = str(payload.get("agent", "")).strip()
    prompt = str(payload.get("prompt", "")).strip()
    workspace = resolve_workspace(payload.get("workspace", "central"))

    if agent not in AGENTS:
        errors.append("agent_not_allowed")
    if not workspace:
        errors.append("workspace_not_allowed")
    if not prompt:
        errors.append("prompt_required")
    if len(prompt) > MAX_PROMPT_LENGTH:
        errors.append("prompt_too_large")

    return errors, agent, prompt, workspace


def auth_api_key(handler):
    header = handler.headers.get("Authorization", "")
    prefix = "Bearer "
    return header[len(prefix):].strip() if header.startswith(prefix) else ""


def normalize_api_key(value):
    api_key = str(value or "").strip()
    if not api_key or api_key == "TU_KIRO_API_KEY":
        return ""
    return api_key


def get_kiro_api_key(handler):
    header_key = normalize_api_key(auth_api_key(handler))
    if header_key:
        return header_key, "authorization_header"

    env_key = normalize_api_key(os.environ.get("KIRO_API_KEY", ""))
    if env_key:
        return env_key, "environment"

    return "", "missing"


def run_kiro(agent, prompt, workspace, api_key):
    started = time.time()
    env = os.environ.copy()
    env["KIRO_API_KEY"] = api_key

    try:
        result = subprocess.run(
            [KIRO_CLI_BIN, "chat", "--agent", agent, "--no-interactive", f"--trust-tools={KIRO_TRUST_TOOLS}", prompt],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except Exception as exc:
        return {
            "status": "FAILED",
            "exit_code": None,
            "duration_ms": int((time.time() - started) * 1000),
            "stdout": "",
            "stderr": "",
            "error": str(exc),
        }

    return {
        "status": "SUCCESS" if result.returncode == 0 else "FAILED",
        "exit_code": result.returncode,
        "duration_ms": int((time.time() - started) * 1000),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "error": None if result.returncode == 0 else "kiro_cli_failed",
    }


class KiroRunnerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path != "/health":
            send_json(self, 404, {"status": "FAILED", "error": "not_found"})
            return

        send_json(self, 200, {
            "status": "OK",
            "service": "kiro-runner",
            "runtime": "python",
            "kiro": kiro_status(),
            "agents": sorted(AGENTS),
            "workspaces": WORKSPACES,
        })

    def do_POST(self):
        if self.path != "/kiro/run":
            send_json(self, 404, {"status": "FAILED", "error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1024 * 256:
                send_json(self, 413, {"status": "FAILED", "error": "request_body_too_large"})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception as exc:
            send_json(self, 400, {"status": "FAILED", "error": "invalid_json", "detail": str(exc)})
            return

        errors, agent, prompt, workspace = validate_payload(payload)
        if errors:
            send_json(self, 400, {"status": "FAILED", "errors": errors})
            return

        api_key, api_key_source = get_kiro_api_key(self)
        if not api_key and not payload.get("dry_run"):
            send_json(self, 401, {"status": "FAILED", "error": "kiro_api_key_required"})
            return

        command = {
            "bin": KIRO_CLI_BIN,
            "args": ["chat", "--agent", agent, "--no-interactive", f"--trust-tools={KIRO_TRUST_TOOLS}", prompt],
            "cwd": workspace,
        }

        if payload.get("dry_run"):
            send_json(self, 200, {
                "status": "SUCCESS",
                "dry_run": True,
                "agent": agent,
                "workspace": workspace,
                "command": command,
                "auth": {
                    "kiro_api_key_present": bool(api_key),
                    "source": api_key_source,
                },
                "requires_human_review": payload.get("approval_required") is not False,
            })
            return

        result = run_kiro(agent, prompt, workspace, api_key)
        send_json(self, 200 if result["status"] == "SUCCESS" else 500, {
            **result,
            "agent": agent,
            "workspace": workspace,
            "auth": {
                "kiro_api_key_present": bool(api_key),
                "source": api_key_source,
            },
            "requires_human_review": payload.get("approval_required") is not False,
        })


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), KiroRunnerHandler)
    print(f"kiro-runner listening on http://{HOST}:{PORT}")
    server.serve_forever()
