"""MCP tool ``lazyown_set_config``: set one key in payload.json."""

from __future__ import annotations

import json
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
    """Coerce and persist one payload key, refusing to null an existing value."""
    key = arguments.get("key")
    value = arguments.get("value")
    if not key:
        return ctx.text(tool_name, "key and value are required")
    try:
        from core.payload_schema import coerce_value
    except ImportError:

        def coerce_value(coerce_key, coerce_value_in):
            return coerce_value_in

    cfg = ctx.load_payload()
    coerced = coerce_value(key, value)
    if coerced is None or (isinstance(coerced, str) and not coerced.strip()):
        return ctx.text(tool_name, f"Refused: refusing to null out '{key}' (pass a real value)")
    cfg[key] = coerced
    result = ctx.save_payload(cfg)
    return ctx.text(tool_name, json.dumps({"key": key, "value": coerced, "result": result}))
