"""MCP tool ``lazyown_autonomous_events`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_autonomous_events",
    description=(
        "Lee los últimos N eventos del stream autónomo (autonomous_events.jsonl): "
        "STEP_START, STEP_DONE, HIGH_VALUE, DRONE_SPAWNED, PHASE_CHANGE, "
        "OBJECTIVE_AUTO_INJECTED, HEARTBEAT."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "last_n": {"type": "integer", "default": 20, "description": "Número de eventos a leer"},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_autonomous_events MCP tool."""
    try:
        from autonomous_daemon import mcp_autonomous_events as _auto_events
    except Exception:
        return ctx.text(tool_name, "[auto] autonomous_daemon.py no importable")
    try:
        return ctx.text(tool_name, _auto_events(last_n=int(arguments.get("last_n", 20))))
    except Exception as exc:
        return ctx.text(tool_name, f"[autonomous_events error] {exc}")
