"""MCP tool ``lazyown_read_session_file``: read a sessions/ artefact.

Migrated to consume the SDK facade: the path-traversal defence and the
bounded read now live once in :class:`sdk.facade.Lazy.sessions`, not
hand-rolled here.
"""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_read_session_file",
    description="Read the contents of a file in the LazyOwn sessions directory.",
    inputSchema={
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Relative path inside sessions/ (e.g. 'logs/beacon1.log').",
            }
        },
        "required": ["filepath"],
    },
)

_MAX_DISPLAY_CHARS = 8000


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return a bounded view of a sessions artefact via the SDK facade.

    Args:
        arguments: Tool arguments; ``filepath`` relative to sessions/.
        tool_name: The dispatched tool name for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A one-element ``TextContent`` list with the file content, a
        truncation marker when long, or a traversal rejection message.
    """
    if str(ctx.lazyown_dir) not in sys.path:
        sys.path.insert(0, str(ctx.lazyown_dir))
    from sdk import Lazy, SessionPathError

    lazy = Lazy(sessions_dir=ctx.sessions_dir)
    try:
        content = lazy.sessions.read(arguments["filepath"])
    except SessionPathError:
        return ctx.text(tool_name, "error: path traversal not allowed")
    if len(content) > _MAX_DISPLAY_CHARS:
        content = content[:_MAX_DISPLAY_CHARS] + "\n... [truncated]"
    return ctx.text(tool_name, content)
