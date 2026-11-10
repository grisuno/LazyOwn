"""MCP tool ``lazyown_search_tools`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_search_tools",
    description=(
        "Search for LazyOwn MCP tools by keyword. "
        "Use this to discover tools when you know what capability you need "
        "but not the exact tool name. "
        "Example: query='smb' returns all SMB-related tools."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Keyword to search in tool names and descriptions.",
            },
            "limit": {
                "type": "integer",
                "description": "Max results to return (default 15).",
                "default": 15,
            },
        },
        "required": ["query"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_search_tools MCP tool."""
    query = arguments.get("query", "").lower().strip()
    limit = int(arguments.get("limit", 15))
    if not query:
        return ctx.text(tool_name, "Provide a 'query' keyword to search tools.")
    # Gather all tool definitions from ctx.list_tools
    try:
        all_tools = await ctx.list_tools()
    except Exception as e:
        return ctx.text(tool_name, f"[search_tools error] {e}")
    matches = [t for t in all_tools if query in t.name.lower() or query in (t.description or "").lower()]
    if not matches:
        return ctx.text(tool_name, f"No tools found matching '{query}'.")
    lines = [f"Found {len(matches)} tool(s) matching '{query}':"]
    for t in matches[:limit]:
        req = []
        try:
            req = t.inputSchema.get("required", [])
        except Exception:
            pass
        lines.append(f"\n  {t.name}")
        lines.append(f"    {(t.description or '').splitlines()[0][:90]}")
        if req:
            lines.append(f"    required: {', '.join(req)}")
    return ctx.text(tool_name, "\n".join(lines))
