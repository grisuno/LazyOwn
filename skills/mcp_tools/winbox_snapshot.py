"""MCP tool ``lazyown_winbox_snapshot``: manage WinBox lab snapshots."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_winbox_snapshot",
    description=(
        "Manage WinBox lab snapshots: list, create (auto-shuts the VM down first) or "
        "restore a rollback point for containment and repeatability."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "create", "restore"], "description": "Default list."},
            "name": {"type": "string", "description": "Snapshot name for create/restore."},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Manage WinBox snapshots: list, create or restore a rollback point."""
    action = str(arguments.get("action") or "list").strip().lower()
    name = str(arguments.get("name") or "").strip()
    if action not in ("list", "create", "restore"):
        return ctx.text(tool_name, "action must be list, create or restore")
    if action != "list" and not name:
        return ctx.text(tool_name, "name is required for create/restore")
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        argv = ["snapshot"] if action == "list" else ["snapshot" if action == "create" else "restore", name]
        result = winbox_gym.run_cli(argv, timeout=winbox_gym.UP_TIMEOUT_SEC)
        return ctx.text(tool_name, json.dumps(result, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
