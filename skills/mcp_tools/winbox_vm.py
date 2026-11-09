"""MCP tool ``lazyown_winbox_vm``: drive the WinBox lab VM lifecycle."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_winbox_vm",
    description=(
        "Drive the WinBox lab VM lifecycle: bootstrap (idempotent full setup: deps, ISO, "
        "VM build, boot, rhost bind), up, down (graceful or --force), suspend, status. "
        "The lab VM must stay isolated from production networks."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["bootstrap", "up", "down", "suspend", "status"],
                "description": "Lifecycle action (default status). bootstrap = one-command full setup.",
            },
            "reboot": {"type": "boolean", "description": "With up: shutdown then start.", "default": False},
            "force": {"type": "boolean", "description": "With down: hard power-off.", "default": False},
            "timeout": {"type": "integer", "description": "Wall-clock seconds (default 900 for up)."},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Drive WinBox VM lifecycle: bootstrap, up, down, suspend, status."""
    action = str(arguments.get("action") or "status").strip().lower()
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        if action == "status":
            return ctx.text(tool_name, json.dumps(winbox_gym.vm_status(), indent=2))
        if action == "bootstrap":
            result = winbox_gym.ensure_lab_ready(ctx.load_payload())
            return ctx.text(tool_name, json.dumps(result, indent=2))
        if action not in ("up", "down", "suspend"):
            return ctx.text(tool_name, json.dumps({"error": f"unsupported action: {action}"}))
        argv = [action]
        if arguments.get("reboot") and action == "up":
            argv.append("--reboot")
        if arguments.get("force") and action == "down":
            argv.append("--force")
        default_timeout = winbox_gym.UP_TIMEOUT_SEC if action == "up" else winbox_gym.CLI_TIMEOUT_SEC
        timeout = int(arguments.get("timeout", default_timeout))
        result = winbox_gym.run_cli(argv, timeout=timeout)
        if result.get("ok") and action == "up":
            result["ip"] = winbox_gym.vm_ip()
        return ctx.text(tool_name, json.dumps(result, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
