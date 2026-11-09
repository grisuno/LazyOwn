"""MCP tool ``lazyown_autonomous_start`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_autonomous_start",
    description=(
        "Inicia el daemon autónomo de LazyOwn — loop raíz que ejecuta objetivos "
        "SIN esperar a Claude entre pasos. Cierra la brecha OpenClaw: "
        "observa objectives.jsonl, ejecuta comandos, actualiza WorldModel, "
        "lanza drones Hive en paralelo, inyecta nuevos objetivos derivados. "
        "Claude solo necesita inyectar el objetivo inicial."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "max_steps": {
                "type": "integer",
                "description": "Pasos máximos por objetivo (default 10)",
                "default": 10,
            },
            "backend": {
                "type": "string",
                "enum": ["groq", "ollama"],
                "description": "Backend para drones Hive",
                "default": "groq",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_autonomous_start MCP tool."""
    try:
        from autonomous_daemon import mcp_autonomous_start as _auto_start
    except Exception:
        return ctx.text(tool_name, "[auto] autonomous_daemon.py no importable — verifica skills/autonomous_daemon.py")
    try:
        return ctx.text(
            tool_name,
            _auto_start(
                max_steps=int(arguments.get("max_steps", 10)),
                backend=arguments.get("backend", "groq"),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[autonomous_start error] {exc}")
