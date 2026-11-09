"""MCP tool ``lazyown_get_config``: read the current payload.json config.

First tool migrated out of the ``lazyown_mcp`` god-file into the
one-file-per-tool registry. It is the reference implementation: a ``TOOL``
schema plus a ``handle`` function that takes its dependencies from the
injected :class:`mcp_tools._context.MCPContext` and imports nothing from
the runtime.
"""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_get_config",
    description="Read the current LazyOwn configuration (payload.json). Returns all settings.",
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return the full ``payload.json`` as pretty-printed JSON text.

    Args:
        arguments: Unused; the tool takes no parameters.
        tool_name: The dispatched tool name, used for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A one-element ``TextContent`` list holding the config JSON.
    """
    cfg = ctx.load_payload()
    return ctx.text(tool_name, json.dumps(cfg, indent=2))
