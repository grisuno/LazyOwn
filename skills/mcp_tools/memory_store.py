"""MCP tool ``lazyown_memory_store`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_memory_store",
    description=(
        "Explicitly save a command execution to episodic memory. "
        "The auto_loop saves automatically, but use this tool to manually "
        "record important findings that should be recalled in future sessions."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "host": {"type": "string", "description": "Target host IP."},
            "tool": {"type": "string", "description": "Tool or technique name."},
            "command": {"type": "string", "description": "Command that was executed."},
            "output": {"type": "string", "description": "Command output (will be trimmed to 2000 chars)."},
            "success": {"type": "boolean", "description": "Whether it succeeded.", "default": True},
        },
        "required": ["host", "tool", "command", "output"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_memory_store MCP tool."""
    m_host = arguments.get("host", "").strip()
    m_tool = arguments.get("tool", "").strip()
    m_command = arguments.get("command", "").strip()
    m_output = arguments.get("output", "").strip()
    m_success = bool(arguments.get("success", True))
    if not all([m_host, m_tool, m_command]):
        return ctx.text(tool_name, "[memory_store] host, tool, command are required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        import uuid as _uuid

        from memory_store import get_memory_store

        ms = get_memory_store()
        ms.remember(
            session_id=_uuid.uuid4().hex[:8],
            host=m_host,
            tool=m_tool,
            command=m_command,
            output=m_output,
            findings=[],
            success=m_success,
        )
        stats = ms.stats()
        return ctx.text(tool_name, f"Stored. Memory total: {stats.get('total', '?')} entries.")
    except Exception as exc:
        return ctx.text(tool_name, f"[memory_store error] {exc}")
