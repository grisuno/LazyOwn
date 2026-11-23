"""MCP meta-tool ``lazyown_inspect_tool_schema`` — one tool's full schema."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_inspect_tool_schema",
    description=(
        "Return the complete JSON schema of one LazyOwn MCP tool (input "
        "fields, required keys, description). Pair with lazyown_discover "
        "and lazyown_execute_verb."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "tool_name": {
                "type": "string",
                "description": "Exact tool name to inspect (e.g. lazyown_auto_populate).",
            },
        },
        "required": ["tool_name"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext):
    """Handle the inspect request.

    Args:
        arguments: Tool arguments (``tool_name``).
        tool_name: Invoked tool name.
        ctx: Injected runtime context.

    Returns:
        TextContent list with the full schema or an error note.
    """
    import json

    wanted = str(arguments.get("tool_name", "") or "").strip()
    if not wanted:
        return ctx.text(tool_name, "Pass a tool_name, e.g. lazyown_inspect_tool_schema(tool_name='lazyown_auto_populate')")
    tools = await ctx.list_tools()
    for tool in tools:
        if getattr(tool, "name", "") == wanted:
            schema = getattr(tool, "inputSchema", None)
            body = json.dumps({"name": wanted, "description": getattr(tool, "description", ""), "inputSchema": schema}, indent=2, default=str)
            return ctx.text(tool_name, body)
    return ctx.text(tool_name, f"Unknown tool: {wanted}. Use lazyown_discover to list valid names.")
