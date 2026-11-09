"""MCP tool ``lazyown_misp_export`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_misp_export",
    description=(
        "Export current session findings as a MISP-compatible event JSON. "
        "Converts WorldModel hosts, services, credentials, and CVEs into "
        "typed MISP attributes. Saves to sessions/misp_event.json."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Filter to a specific target (default: all).",
                "default": "",
            },
            "output": {
                "type": "string",
                "description": "Output file path (default: sessions/misp_event.json).",
                "default": "",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_misp_export MCP tool."""
    misp_target = arguments.get("target", "").strip() or None
    misp_output = arguments.get("output", "").strip() or None
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from integrations.misp_export import get_exporter as _misp_get

        exporter = _misp_get()
        event = await asyncio.get_event_loop().run_in_executor(
            None, lambda: exporter.export_session(ctx.lazyown_dir / "sessions", target=misp_target)
        )
        out_path = misp_output or str(ctx.lazyown_dir / "sessions" / "misp_event.json")
        saved = await asyncio.get_event_loop().run_in_executor(None, lambda: exporter.save(event, out_path))
        return ctx.text(
            tool_name,
            f"MISP event saved: {saved}\n"
            f"Attributes: {len(event.attributes)}  "
            f"Threat level: {event.threat_level_id}  "
            f"Tags: {', '.join(event.tags) or 'none'}",
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[misp_export error] {exc}")
