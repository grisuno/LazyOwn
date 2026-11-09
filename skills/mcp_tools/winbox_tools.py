"""MCP tool ``lazyown_winbox_tools``: manage tools staged in the WinBox guest."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_winbox_tools",
    description=(
        "Manage tools staged into the WinBox guest at Z:\\tools: list, add (comma-separated "
        "host paths) or remove by name."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "add", "remove"], "description": "Default list."},
            "paths": {"type": "string", "description": "Comma-separated paths or names."},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Manage tools staged into the WinBox guest (list, add, remove)."""
    action = str(arguments.get("action") or "list").strip().lower()
    paths = str(arguments.get("paths") or "").strip()
    if action not in ("list", "add", "remove"):
        return ctx.text(tool_name, "action must be list, add or remove")
    if action != "list" and not paths:
        return ctx.text(tool_name, "paths is required for add/remove (comma-separated)")
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        argv = ["tools", action]
        if paths:
            argv += [path.strip() for path in paths.split(",") if path.strip()]
        result = winbox_gym.run_cli(argv, timeout=winbox_gym.CLI_TIMEOUT_SEC)
        return ctx.text(tool_name, json.dumps(result, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
