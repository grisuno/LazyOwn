"""MCP tool ``lazyown_autonomous_inject`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_autonomous_inject",
    description=(
        "Inyecta un objetivo de alto nivel en la cola del daemon autónomo. "
        "El daemon lo tomará en el próximo ciclo y lo ejecutará sin intervención. "
        "Claude solo necesita llamar esto UNA VEZ por objetivo."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Texto del objetivo"},
            "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "high"},
            "target": {
                "type": "string",
                "description": "IP target (opcional, default: payload.json rhost)",
                "default": "",
            },
        },
        "required": ["text"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_autonomous_inject MCP tool."""
    try:
        from autonomous_daemon import mcp_autonomous_inject as _auto_inject
    except Exception:
        return ctx.text(tool_name, "[auto] autonomous_daemon.py no importable")
    try:
        return ctx.text(
            tool_name,
            _auto_inject(
                text=arguments.get("text", ""),
                priority=arguments.get("priority", "high"),
                target=arguments.get("target", ""),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[autonomous_inject error] {exc}")
