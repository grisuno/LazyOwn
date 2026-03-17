#!/usr/bin/env python3
"""
LazyOwn MCP Server
Exposes LazyOwn framework capabilities as MCP tools for Claude Code and Claude web.

Usage:
    python3 skills/lazyown_mcp.py

Configuration via environment variables:
    LAZYOWN_DIR      - Path to LazyOwn directory (default: parent of this file)
    LAZYOWN_C2_HOST  - C2 server host (default: from payload.json)
    LAZYOWN_C2_PORT  - C2 server port (default: from payload.json)
    LAZYOWN_C2_USER  - C2 username (default: from payload.json)
    LAZYOWN_C2_PASS  - C2 password (default: from payload.json)
"""

import asyncio
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── Paths ─────────────────────────────────────────────────────────────────────
SKILLS_DIR = Path(__file__).parent
LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"
SESSIONS_DIR = LAZYOWN_DIR / "sessions"

# ── MCP server ────────────────────────────────────────────────────────────────
server = Server("lazyown")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_payload() -> dict:
    """Load payload.json, return empty dict on failure."""
    try:
        with open(PAYLOAD_FILE) as f:
            return json.load(f)
    except Exception as e:
        return {"_error": str(e)}


def _save_payload(data: dict) -> str:
    try:
        with open(PAYLOAD_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return "ok"
    except Exception as e:
        return f"error: {e}"


def _c2_creds():
    """Return (host, port, user, password) from env or payload.json."""
    cfg = _load_payload()
    host = os.environ.get("LAZYOWN_C2_HOST", cfg.get("lhost", "127.0.0.1"))
    port = int(os.environ.get("LAZYOWN_C2_PORT", cfg.get("c2_port", 4444)))
    user = os.environ.get("LAZYOWN_C2_USER", cfg.get("c2_user", "LazyOwn"))
    passwd = os.environ.get("LAZYOWN_C2_PASS", cfg.get("c2_pass", "LazyOwn"))
    return host, port, user, passwd


def _c2_request(path: str, method: str = "GET", body: dict | None = None) -> dict:
    """Make an authenticated HTTP request to the C2 server."""
    host, port, user, passwd = _c2_creds()
    url = f"https://{host}:{port}{path}"

    import base64
    token = base64.b64encode(f"{user}:{passwd}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    # Skip SSL verification for self-signed certs (common in lab environments)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def _run_lazyown_command(command: str, timeout: int = 30) -> str:
    """
    Execute one or more LazyOwn shell commands non-interactively.
    Multiple commands separated by newlines are all sent to stdin.
    """
    cmd_input = command.strip() + "\nexit\n"
    try:
        result = subprocess.run(
            [sys.executable, str(LAZYOWN_DIR / "lazyown.py")],
            input=cmd_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(LAZYOWN_DIR),
        )
        output = result.stdout + result.stderr
        # Strip ANSI escape codes for readability
        import re
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", output).strip()
    except subprocess.TimeoutExpired:
        return f"[timeout] Command exceeded {timeout}s"
    except Exception as e:
        return f"[error] {e}"


# ── Tool definitions ──────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="lazyown_run_command",
            description=(
                "Execute one or more commands in the LazyOwn interactive shell. "
                "Separate multiple commands with newlines. "
                "Examples: 'list', 'set rhost 10.10.11.78', 'lazynmap'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "LazyOwn shell command(s) to execute (newline-separated).",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Max seconds to wait for output (default 30).",
                        "default": 30,
                    },
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="lazyown_get_config",
            description="Read the current LazyOwn configuration (payload.json). Returns all settings.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_set_config",
            description=(
                "Update one or more values in LazyOwn's payload.json configuration. "
                "Pass a dict of key-value pairs to update. "
                "Example: {\"lhost\": \"10.10.14.5\", \"rhost\": \"10.10.11.78\"}."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "updates": {
                        "type": "object",
                        "description": "Key-value pairs to set in payload.json.",
                    }
                },
                "required": ["updates"],
            },
        ),
        types.Tool(
            name="lazyown_list_modules",
            description="List all available LazyOwn modules and scripts in the modules/ directory.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_get_beacons",
            description="Query the LazyOwn C2 server for currently connected beacons/implants.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_c2_command",
            description=(
                "Issue a tasking command to a specific beacon connected to the LazyOwn C2 server. "
                "Available beacon commands include: whoami, download:<file>, upload:<file>, "
                "rev, exfil, stealth_on, stealth_off, discover, portscan, softenum, "
                "persist, cleanlogs, amsi, escalatelin, terminate, and more."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {
                        "type": "string",
                        "description": "The beacon/client ID to task.",
                    },
                    "command": {
                        "type": "string",
                        "description": "Command to send to the beacon.",
                    },
                },
                "required": ["client_id", "command"],
            },
        ),
        types.Tool(
            name="lazyown_run_api",
            description=(
                "Execute a shell command on the C2 server host via the /api/run endpoint. "
                "Requires the C2 server to be running."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Shell command to run on the C2 host.",
                    }
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="lazyown_list_sessions",
            description="List files in the LazyOwn sessions directory (logs, exfil data, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "subdir": {
                        "type": "string",
                        "description": "Optional subdirectory under sessions/ to list.",
                        "default": "",
                    }
                },
            },
        ),
        types.Tool(
            name="lazyown_read_session_file",
            description="Read the contents of a file in the LazyOwn sessions directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Relative path inside sessions/ (e.g. 'logs/beacon1.log').",
                    }
                },
                "required": ["filepath"],
            },
        ),
        types.Tool(
            name="lazyown_c2_status",
            description="Check if the LazyOwn C2 server is reachable and return dashboard data.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ── Tool handlers ─────────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:

    def text(content: str) -> list[types.TextContent]:
        return [types.TextContent(type="text", text=content)]

    # ── run_command ──────────────────────────────────────────────────────────
    if name == "lazyown_run_command":
        command = arguments["command"]
        timeout = int(arguments.get("timeout", 30))
        output = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _run_lazyown_command(command, timeout)
        )
        return text(output)

    # ── get_config ───────────────────────────────────────────────────────────
    elif name == "lazyown_get_config":
        cfg = _load_payload()
        return text(json.dumps(cfg, indent=2))

    # ── set_config ───────────────────────────────────────────────────────────
    elif name == "lazyown_set_config":
        updates: dict = arguments["updates"]
        cfg = _load_payload()
        if "_error" in cfg:
            return text(f"Cannot load payload.json: {cfg['_error']}")
        cfg.update(updates)
        result = _save_payload(cfg)
        if result == "ok":
            return text(f"Updated {len(updates)} key(s): {', '.join(updates.keys())}")
        return text(result)

    # ── list_modules ─────────────────────────────────────────────────────────
    elif name == "lazyown_list_modules":
        modules_dir = LAZYOWN_DIR / "modules"
        try:
            files = sorted(modules_dir.iterdir())
            lines = []
            for f in files:
                if f.is_file():
                    lines.append(f"  {f.name} ({f.stat().st_size:,} bytes)")
                elif f.is_dir():
                    lines.append(f"  {f.name}/  [dir]")
            return text("\n".join(lines))
        except Exception as e:
            return text(f"error: {e}")

    # ── get_beacons ──────────────────────────────────────────────────────────
    elif name == "lazyown_get_beacons":
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/get_connected_clients")
        )
        return text(json.dumps(result, indent=2))

    # ── c2_command ───────────────────────────────────────────────────────────
    elif name == "lazyown_c2_command":
        client_id = arguments["client_id"]
        command = arguments["command"]
        body = {"client_id": client_id, "command": command}
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/issue_command", method="POST", body=body)
        )
        return text(json.dumps(result, indent=2))

    # ── run_api ──────────────────────────────────────────────────────────────
    elif name == "lazyown_run_api":
        command = arguments["command"]
        body = {"command": command}
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/api/run", method="POST", body=body)
        )
        return text(json.dumps(result, indent=2))

    # ── list_sessions ─────────────────────────────────────────────────────────
    elif name == "lazyown_list_sessions":
        subdir = arguments.get("subdir", "").strip("/")
        target = SESSIONS_DIR / subdir if subdir else SESSIONS_DIR
        try:
            lines = []
            for item in sorted(target.rglob("*")):
                rel = item.relative_to(SESSIONS_DIR)
                if item.is_file():
                    lines.append(f"{rel}  ({item.stat().st_size:,} bytes)")
                else:
                    lines.append(f"{rel}/")
            return text("\n".join(lines) if lines else "(empty)")
        except Exception as e:
            return text(f"error: {e}")

    # ── read_session_file ─────────────────────────────────────────────────────
    elif name == "lazyown_read_session_file":
        filepath = arguments["filepath"].lstrip("/")
        target = SESSIONS_DIR / filepath
        # Safety: ensure path stays inside sessions/
        try:
            target.resolve().relative_to(SESSIONS_DIR.resolve())
        except ValueError:
            return text("error: path traversal not allowed")
        try:
            content = target.read_text(errors="replace")
            if len(content) > 8000:
                content = content[:8000] + "\n... [truncated]"
            return text(content)
        except Exception as e:
            return text(f"error: {e}")

    # ── c2_status ─────────────────────────────────────────────────────────────
    elif name == "lazyown_c2_status":
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/api/data")
        )
        return text(json.dumps(result, indent=2))

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
