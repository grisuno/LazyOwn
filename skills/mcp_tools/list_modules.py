"""MCP tool ``lazyown_list_modules``: list modules and scripts in modules/.

Migrated out of the ``lazyown_mcp`` god-file. Demonstrates a tool that
needs a repo-relative resource: it takes the repository root from the
injected :class:`mcp_tools._context.MCPContext` rather than importing the
runtime.
"""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_MAX_MODULES = 200

TOOL = types.Tool(
    name="lazyown_list_modules",
    description="List all available LazyOwn modules and scripts in the modules/ directory.",
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return discovered modules as JSON, optionally filtered by type.

    Args:
        arguments: May carry a ``type`` key to filter by module type.
        tool_name: The dispatched tool name, used for the text envelope.
        ctx: Injected runtime helpers, including the repository root.

    Returns:
        A one-element ``TextContent`` list holding the module summaries.
    """
    from modules.module_registry import ModuleRegistry

    registry = ModuleRegistry.get_instance(ctx.lazyown_dir)
    modules = registry.search("", filter_type=arguments.get("type"))
    summaries = [
        {
            "name": module.get("name", module.get("type", "")),
            "type": module.get("type", ""),
            "description": module.get("description", ""),
        }
        for module in modules[:_MAX_MODULES]
    ]
    return ctx.text(tool_name, json.dumps(summaries))
