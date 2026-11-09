"""MCP tool ``lazyown_hive_spawn`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_spawn",
    description=(
        "Spawn one or more hive-mind drones (Groq/Ollama) in PARALLEL for a goal. "
        "When n_drones>1 or role='auto', the Queen decomposes the goal into specialised "
        "tasks (recon, exploit, analyze, cred, lateral, report) and fires them all at once. "
        "All drones share a unified ChromaDB+SQLite+Parquet memory. "
        "Returns drone_ids to poll with lazyown_hive_result / lazyown_hive_collect."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {"type": "string", "description": "High-level objective"},
            "role": {
                "type": "string",
                "description": "Drone role: auto|recon|exploit|analyze|cred|lateral|report|generic",
                "default": "auto",
            },
            "n_drones": {"type": "integer", "description": "Drones to spawn (0=template)", "default": 0},
            "backend": {"type": "string", "enum": ["groq", "ollama"], "default": "groq"},
            "max_iterations": {"type": "integer", "default": 10},
            "api_key": {"type": "string", "default": ""},
        },
        "required": ["goal"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_spawn MCP tool."""
    try:
        from hive_mind import mcp_hive_spawn as _hive_spawn
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable — check skills/hive_mind.py")
    try:
        result = _hive_spawn(
            goal=arguments.get("goal", ""),
            role=arguments.get("role", "auto"),
            n_drones=int(arguments.get("n_drones", 0)),
            backend=arguments.get("backend", "groq"),
            max_iterations=int(arguments.get("max_iterations", 10)),
            api_key=arguments.get("api_key", ""),
        )
        return ctx.text(tool_name, result)
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_spawn error] {exc}")
