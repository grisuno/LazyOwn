"""MCP tool ``lazyown_daemon_veto`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_veto",
    description=(
        "Manage the command veto list. action=add appends a first-token "
        "name (e.g. nmap), action=remove drops it, action=clear empties "
        "the list, action=list returns the current entries."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["add", "remove", "clear", "list"],
                "default": "list",
            },
            "command": {
                "type": "string",
                "description": "Command first-token (required for add and remove).",
                "default": "",
            },
        },
        "required": ["action"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_veto MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        control = _DC(ctx.sessions_dir)
        action = str(arguments.get("action", "list")).strip().lower()
        command = str(arguments.get("command", "")).strip()
        if action == "add":
            state = control.add_veto(command)
        elif action == "remove":
            state = control.remove_veto(command)
        elif action == "clear":
            state = control.clear_vetoes()
        elif action == "list":
            state = control.load()
        else:
            return ctx.text(tool_name, f"[daemon_veto error] unknown action '{action}'; expected add|remove|clear|list")
        return ctx.text(
            tool_name,
            json.dumps(
                {"ok": True, "vetoed_commands": state.vetoed_commands},
                ensure_ascii=False,
            ),
        )
    except ValueError as exc:
        return ctx.text(tool_name, f"[daemon_veto error] {exc}")
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_veto error] {exc}")
