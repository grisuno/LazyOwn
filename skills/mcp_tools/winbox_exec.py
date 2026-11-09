"""MCP tool ``lazyown_winbox_exec``: run a command inside the WinBox guest."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_TIMEOUT_SEC = 120
_RUN_GRACE_SEC = 30
_JOBS_LIST_TIMEOUT_SEC = 30
_JOBS_TAIL_CHARS = 500

TOOL = types.Tool(
    name="lazyown_winbox_exec",
    description=(
        "Execute a cmd.exe command inside the WinBox Windows guest as SYSTEM or a local "
        "user (--user/--password), optionally in the background (--bg). Part of the "
        "isolated Windows vulnerability-research lab; never use against production."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Guest command line, e.g. 'whoami'."},
            "user": {"type": "string", "description": "Optional local Windows user."},
            "password": {"type": "string", "description": "Password for --user."},
            "background": {"type": "boolean", "description": "Run as a background job.", "default": False},
            "timeout": {"type": "integer", "description": "Per-command seconds (default 120, max 600)."},
        },
        "required": ["command"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Execute a command inside the WinBox guest as SYSTEM or a local user."""
    command = str(arguments.get("command") or "").strip()
    if not command:
        return ctx.text(tool_name, "command is required")
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        timeout = int(arguments.get("timeout", _DEFAULT_TIMEOUT_SEC))
        timeout = max(winbox_gym.MIN_TIMEOUT_SEC, min(winbox_gym.EXE_TIMEOUT_MAX, timeout))
        argv = ["exec", "--timeout", str(timeout)]
        if arguments.get("user"):
            argv += ["--user", str(arguments["user"])]
        if arguments.get("password"):
            argv += ["--password", str(arguments["password"])]
        if arguments.get("background"):
            argv.append("--bg")
        argv += command.split()
        result = winbox_gym.run_cli(argv, timeout=min(winbox_gym.EXE_TIMEOUT_MAX, timeout + _RUN_GRACE_SEC))
        if arguments.get("background"):
            jobs = winbox_gym.run_cli(["jobs", "list"], timeout=_JOBS_LIST_TIMEOUT_SEC)
            result["jobs"] = (jobs.get("output") or "").strip()[-_JOBS_TAIL_CHARS:]
        return ctx.text(tool_name, json.dumps(result, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
