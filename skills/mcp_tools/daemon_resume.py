"""MCP tool ``lazyown_daemon_resume`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_resume",
    description=(
        "Convenience wrapper that sets the daemon mode back to auto. Any paused objective continues with its next step."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_resume MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        state = _DC(ctx.sessions_dir).resume()
        return ctx.text(
            tool_name,
            json.dumps(
                {"ok": True, "mode": state.mode},
                ensure_ascii=False,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_resume error] {exc}")
