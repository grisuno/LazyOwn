"""MCP tool ``lazyown_c2_vuln_analysis`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_vuln_analysis",
    description=(
        "Ask the LazyOwn C2 AI (Groq) to analyse a vulnerability or CVE. "
        "Requires the C2 server to be running. "
        "Example: 'Analyse CVE-2024-1234 and suggest exploitation steps'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Vulnerability description or CVE to analyse.",
            }
        },
        "required": ["query"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_vuln_analysis MCP tool."""
    query = arguments["query"]
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/vuln", method="POST", body={"query": query})
    )
    if "_error" in result:
        return ctx.text(tool_name, f"C2 unreachable or error: {result['_error']}")
    return ctx.text(tool_name, result.get("result", result.get("response", json.dumps(result))))
