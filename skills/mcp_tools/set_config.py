"""MCP tool ``lazyown_set_config``: set one key in payload.json."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_set_config",
    description=(
        "Set a single key-value pair in LazyOwn's payload.json. "
        "Call multiple times to update several keys. "
        "Common keys: lhost, rhost, lport, rport, domain, wordlist, api_key."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "key": {
                "type": "string",
                "description": "The payload.json key to update (e.g. 'rhost', 'lhost', 'lport').",
            },
            "value": {
                "type": "string",
                "description": "The value to set (always pass as string; numbers are auto-converted).",
            },
        },
        "required": ["key", "value"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Coerce, validate and persist one payload key via the SDK facade.

    The coercion, schema validation and write now live once in
    :class:`sdk.facade.Lazy.config`; this handler keeps only the tool
    policy of refusing to null out an existing value.

    Args:
        arguments: Tool arguments; ``key`` and ``value``.
        tool_name: The dispatched tool name for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A one-element ``TextContent`` list with the write result, the
        null refusal, or a schema validation error.
    """
    key = arguments.get("key")
    value = arguments.get("value")
    if not key:
        return ctx.text(tool_name, "key and value are required")
    if str(ctx.lazyown_dir) not in sys.path:
        sys.path.insert(0, str(ctx.lazyown_dir))
    from core.payload_schema import coerce_value

    from sdk import ConfigValidationError, Lazy

    coerced = coerce_value(key, value)
    if coerced is None or (isinstance(coerced, str) and not coerced.strip()):
        return ctx.text(tool_name, f"Refused: refusing to null out '{key}' (pass a real value)")
    try:
        persisted = Lazy(payload_path=ctx.lazyown_dir / "payload.json").config.set(key, value)
    except ConfigValidationError as exc:
        return ctx.text(tool_name, f"error: {exc}")
    return ctx.text(tool_name, json.dumps({"key": key, "value": persisted, "result": "payload.json"}))
