"""MCP meta-tool ``lazyown_discover`` — progressive disclosure search.

Progressive disclosure layer: instead of advertising 190+ tool schemas in
``list_tools`` (which burns context in every client), agents call this
search surface to find the tool they need by name or keyword, then
inspect it with ``lazyown_inspect_tool_schema`` and run it with
``lazyown_execute_verb``.
"""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_discover",
    description=(
        "Search the LazyOwn MCP tool catalogue by keyword, returning matching "
        "tool names with one-line descriptions. The catalogue is not fully "
        "advertised (progressive disclosure): use this to find tools, "
        "lazyown_inspect_tool_schema for a schema, lazyown_execute_verb to run."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Keyword matched against tool names and descriptions (empty = list everything).",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum matches returned (default 25).",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext):
    """Handle the discover request.

    Args:
        arguments: Tool arguments (``query``, ``limit``).
        tool_name: Invoked tool name.
        ctx: Injected runtime context.

    Returns:
        TextContent list with the match table.
    """
    query = str(arguments.get("query", "") or "").strip().lower()
    try:
        limit = max(1, int(arguments.get("limit", 25) or 25))
    except (TypeError, ValueError):
        limit = 25
    tools = await ctx.list_tools()
    matches = []
    for tool in tools:
        name = getattr(tool, "name", "")
        description = str(getattr(tool, "description", "") or "").splitlines()[0][:110]
        if query and query not in name.lower() and query not in description.lower():
            continue
        matches.append((name, description))
        if len(matches) >= limit:
            break
    header = f"{len(matches)} tool(s) matching '{query or '*'}':"
    body = "\n".join(f"  {name} — {description}" for name, description in matches)
    return ctx.text(tool_name, f"{header}\n{body}")
