"""MCP tool ``lazyown_delete_param`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_delete_param",
    description=("Delete an operator parameter from the shared catalog. Builtin payload keys cannot be deleted."),
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the operator parameter to remove.",
            },
        },
        "required": ["name"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_delete_param MCP tool."""
    try:
        from core.param_registry import delete_param

        delete_param(str(arguments["name"]))
    except KeyError as e:
        return ctx.text(tool_name, f"error: {e} (builtin parameters cannot be deleted)")
    except Exception as e:
        return ctx.text(tool_name, f"error deleting parameter: {e}")
    return ctx.text(tool_name, f"[+] parameter '{arguments['name']}' deleted")
