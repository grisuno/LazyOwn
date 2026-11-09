"""MCP tool ``lazyown_daemon_pause`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_pause",
    description=(
        "Convenience wrapper that sets the daemon mode to paused. "
        "The daemon polls between steps and will block until resume."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_pause MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        state = _DC(ctx.sessions_dir).pause()
        return ctx.text(
            tool_name,
            json.dumps(
                {"ok": True, "mode": state.mode},
                ensure_ascii=False,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_pause error] {exc}")
