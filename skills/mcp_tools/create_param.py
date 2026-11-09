"""MCP tool ``lazyown_create_param`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_create_param",
    description=(
        "Declare a shared parameter once and reuse it in every addon. The "
        "declaration is stored as data in params/operator.yaml; the payload "
        "schema and the addon creator pick it up automatically, so no source "
        "edit is needed. Use a generic name (url, target, profile), never a "
        "tool name."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Parameter name: lowercase, letters/digits/underscores, max 48 chars.",
            },
            "kind": {
                "type": "string",
                "description": "Payload kind: string, integer, boolean, url, path, ip, port, hostname.",
                "default": "string",
            },
            "default": {
                "type": "string",
                "description": "Default value used when the parameter is not set.",
                "default": "",
            },
            "description": {
                "type": "string",
                "description": "Short help text shown to the operator.",
                "default": "",
            },
        },
        "required": ["name"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_create_param MCP tool."""
    try:
        from core.param_registry import create_param

        param = create_param(
            str(arguments["name"]),
            kind=str(arguments.get("kind") or "string"),
            default=arguments.get("default", ""),
            description=str(arguments.get("description") or ""),
        )
    except KeyError:
        return ctx.text(tool_name, "error: name is required")
    except ValueError as e:
        return ctx.text(tool_name, f"error: {e}")
    except Exception as e:
        return ctx.text(tool_name, f"error creating parameter: {e}")
    return ctx.text(
        tool_name,
        f"[+] parameter '{param.name}' created (kind={param.kind}, default={param.default!r}).\n"
        f"Usable now as {{{param.name}}} in any addon, alias or pipeline. "
        f"Set it with 'assign {param.name} <value>'.",
    )
