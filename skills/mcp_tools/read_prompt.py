"""MCP tool ``lazyown_read_prompt`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_read_prompt",
    description=(
        "Read the LazyOwn developer reference (prompt.md). "
        "Contains the full architecture reference: MCP tools, command categories, "
        "payload.json schema, session file layout, C2 routes, addon/tool/plugin schemas, "
        "auto-loop algorithm, policy engine, FactStore, ObjectiveStore, ParquetDB API, "
        "and development rules (DO / DO NOT). "
        "Call this whenever you need to understand how a LazyOwn component works, "
        "what parameters it accepts, or how to add new capabilities without breaking "
        "existing integrations."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "section": {
                "type": "string",
                "description": (
                    "Optional section filter. Pass a heading keyword to get only that "
                    "section (e.g. 'MCP tool', 'payload.json', 'auto-loop', 'FactStore', "
                    "'reglas', 'campaign'). Leave empty to get the full document."
                ),
                "default": "",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_read_prompt MCP tool."""
    section = arguments.get("section", "").strip().lower()
    prompt_path = ctx.lazyown_dir / "prompt.md"

    def _read_prompt() -> str:
        if not prompt_path.exists():
            return (
                "prompt.md no encontrado en la raíz del proyecto. "
                "El archivo documenta la arquitectura de LazyOwn. "
                "Puede haberse excluido del repositorio (está en .gitignore)."
            )
        content = prompt_path.read_text(errors="replace")
        if not section:
            return content
        # Filter to the requested section only
        lines = content.splitlines()
        result_lines: list = []
        in_section = False
        for line in lines:
            if line.startswith("## ") or line.startswith("# "):
                in_section = section in line.lower()
            if in_section:
                result_lines.append(line)
            # Stop at next same-level heading after section found
            elif result_lines and (line.startswith("## ") or line.startswith("# ")):
                break
        if result_lines:
            return "\n".join(result_lines)
        return f"Sección '{section}' no encontrada. Llama sin 'section' para ver el índice completo."

    result = await asyncio.get_event_loop().run_in_executor(None, _read_prompt)
    return ctx.text(tool_name, result)
