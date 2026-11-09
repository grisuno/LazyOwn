"""MCP tool ``lazyown_daemon_focus`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_focus",
    description=(
        "Restrict the daemon to a list of focus targets. Pass targets=[] "
        "to disable focus (run anywhere). Replaces the existing list on "
        "every call."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "targets": {
                "type": "array",
                "items": {"type": "string"},
                "description": "IP addresses or hostnames to focus on.",
                "default": [],
            },
        },
        "required": ["targets"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_focus MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        targets_raw = arguments.get("targets", [])
        if not isinstance(targets_raw, list):
            return ctx.text(tool_name, "[daemon_focus error] targets must be a list of strings")
        targets = [str(t) for t in targets_raw if isinstance(t, (str, int))]
        state = _DC(ctx.sessions_dir).set_focus(targets)
        return ctx.text(
            tool_name,
            json.dumps(
                {"ok": True, "focus_targets": state.focus_targets},
                ensure_ascii=False,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_focus error] {exc}")
