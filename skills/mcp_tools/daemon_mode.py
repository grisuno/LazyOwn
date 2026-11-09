"""MCP tool ``lazyown_daemon_mode`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_mode",
    description=(
        "Switch the autonomous daemon mode: auto (no gating), approval "
        "(operator approves every command), or paused (loop halts before "
        "the next step). Persists to sessions/daemon_control.json so the "
        "running daemon picks it up before its next step."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["auto", "approval", "paused"],
                "description": "Target mode for the daemon control loop.",
            },
        },
        "required": ["mode"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_mode MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        mode = str(arguments.get("mode", "")).strip().lower()
        state = _DC(ctx.sessions_dir).set_mode(mode)
        return ctx.text(
            tool_name,
            json.dumps(
                {"ok": True, "mode": state.mode},
                ensure_ascii=False,
            ),
        )
    except ValueError as exc:
        return ctx.text(tool_name, f"[daemon_mode error] {exc}")
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_mode error] {exc}")
