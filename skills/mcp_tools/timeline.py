"""MCP tool ``lazyown_timeline`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_timeline",
    description=(
        "Generate or return the AI-written red-team timeline narrative. "
        "Groq reads all session events and produces a prose summary "
        "suitable for an executive report. Written to sessions/timeline.md. "
        "Cached for 5 minutes; pass force=true to regenerate immediately."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "force": {
                "type": "boolean",
                "description": "Regenerate even if cached (default false).",
                "default": False,
            }
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_timeline MCP tool."""
    try:
        from timeline_narrator import load_timeline as _load_timeline
        from timeline_narrator import narrate as _narrate
    except Exception:
        return ctx.text(tool_name, "Timeline narrator not available — check modules/timeline_narrator.py")
    force = arguments.get("force", False)
    cfg = ctx.load_payload()
    api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
    # No api_key and not force → try cache first
    if not api_key and not force:
        cached = await asyncio.get_event_loop().run_in_executor(None, _load_timeline)
        if cached:
            return ctx.text(tool_name, cached)
    # ai_fallback handles missing key / quota / Ollama fallback internally
    result = await asyncio.get_event_loop().run_in_executor(None, lambda: _narrate(api_key=api_key, force=force))
    return ctx.text(tool_name, result)
