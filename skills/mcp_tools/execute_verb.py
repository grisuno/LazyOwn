"""MCP meta-tool ``lazyown_execute_verb`` — run any registered tool by name.

The dispatch goes through the runtime's ``call_tool`` so the invocation
keeps the full permission gate, pre-tool hooks, transcript audit and the
dynamic addon/tool/plugin routing of a direct call. Only the
``tools/list`` advertisement is reduced (progressive disclosure).
"""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_execute_verb",
    description=(
        "Execute any registered LazyOwn MCP tool by name with its argument "
        "object. Runs the same permission gate, hooks and audit as a direct "
        "call. Find valid names with lazyown_discover and their schemas with "
        "lazyown_inspect_tool_schema."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "tool_name": {
                "type": "string",
                "description": "Exact registered tool name to invoke.",
            },
            "arguments": {
                "type": "object",
                "description": "Arguments object forwarded verbatim to the target tool.",
            },
        },
        "required": ["tool_name"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext):
    """Handle the execute request by delegating to the runtime dispatcher.

    Args:
        arguments: Tool arguments (``tool_name``, ``arguments``).
        tool_name: Invoked tool name (the meta tool itself).
        ctx: Injected runtime context.

    Returns:
        TextContent list produced by the target tool, or an error note.
    """
    wanted = str(arguments.get("tool_name", "") or "").strip()
    if not wanted:
        return ctx.text(tool_name, "Pass a tool_name (see lazyown_discover).")
    if wanted == tool_name:
        return ctx.text(tool_name, "Refusing to execute the meta tool through itself.")
    if ctx.call_tool is None:
        return ctx.text(tool_name, "Runtime does not expose call_tool; direct invocation unavailable.")
    try:
        return await ctx.call_tool(wanted, dict(arguments.get("arguments") or {}))
    except Exception as exc:
        return ctx.text(tool_name, f"Execution failed for {wanted}: {exc}")
