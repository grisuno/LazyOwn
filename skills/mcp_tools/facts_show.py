"""MCP tool ``lazyown_facts_show``: show structured facts from the session."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_facts_show",
    description=(
        "Show all structured facts extracted from nmap scans and tool output. "
        "Facts include: open ports, detected services, discovered credentials, "
        "accessible shares, and achieved access level per target. "
        "Optionally re-parse all sessions/ files before displaying. "
        "These facts drive context-aware command selection in auto_loop."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Filter to a specific target IP (default: all targets).",
            },
            "refresh": {
                "type": "boolean",
                "description": "Re-parse sessions/ before displaying (default false).",
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return the fact-store summary for a target, optionally re-parsing first."""
    try:
        from lazyown_facts import FactStore
    except Exception:
        return ctx.text(tool_name, "FactStore unavailable. Run: python3 skills/lazyown_facts.py parse")
    facts = FactStore()
    target = arguments.get("target") or ctx.load_payload().get("rhost") or None
    refresh = bool(arguments.get("refresh", False))

    def _do_facts() -> str:
        if refresh:
            facts.parse_all(target=target)
        return facts.summary(target)

    summary = await asyncio.get_event_loop().run_in_executor(None, _do_facts)
    return ctx.text(tool_name, summary or "No facts found. Run with refresh=true to ingest sessions/ files.")
