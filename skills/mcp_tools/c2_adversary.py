"""MCP tool ``lazyown_c2_adversary`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_adversary",
    description=(
        "Emulate a MITRE ATT&CK adversary or technique via the LazyOwn C2 AI (Groq). "
        "Requires the C2 server to be running. "
        "Pass a technique ID (e.g. T1059) or adversary group name."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "technique": {
                "type": "string",
                "description": "MITRE ATT&CK technique ID or adversary name (e.g. 'T1059', 'APT29').",
            }
        },
        "required": ["technique"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_adversary MCP tool."""
    technique = arguments["technique"]
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/adversary", method="POST", body={"technique": technique})
    )
    if "_error" in result:
        return ctx.text(tool_name, f"C2 unreachable or error: {result['_error']}")
    return ctx.text(tool_name, result.get("result", result.get("response", json.dumps(result))))
