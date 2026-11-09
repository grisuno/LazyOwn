"""MCP tool ``lazyown_daemon_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_status",
    description=(
        "Return the full operator-steering state for the autonomous daemon "
        "from sessions/daemon_control.json: mode, vetoed_commands, "
        "focus_targets, and any pending approval request."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_status MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        state = _DC(ctx.sessions_dir).load()
        return ctx.text(tool_name, json.dumps(state.to_dict(), indent=2, ensure_ascii=False))
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_status error] {exc}")
