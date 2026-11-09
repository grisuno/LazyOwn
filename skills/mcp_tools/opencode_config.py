"""MCP tool ``lazyown_opencode_config``: point opencode/hermes at llama.cpp."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_opencode_config",
    description=(
        "Point the operator's opencode (~/.config/opencode/opencode.json) "
        "and/or hermes (~/.hermes/config.yaml) at the Lazy llama.cpp "
        "local server. Backs files up first; idempotent (no-op when "
        "already patched). Target opencode|hermes|both."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Which config to patch (default both).",
                "default": "both",
            },
            "set_default": {
                "type": "boolean",
                "description": "Also set opencode's top-level model to llamacpp/local-model.",
                "default": False,
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Patch opencode/hermes configs to the local llama.cpp server."""
    target = str(arguments.get("target", "both") or "both").strip().lower()
    set_default = bool(arguments.get("set_default", False))
    try:
        import sys

        scripts = str(ctx.lazyown_dir / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        from lazy_opencode_config import patch_hermes, patch_opencode
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    results = []
    if target in ("opencode", "both"):
        results.append(patch_opencode(set_default=set_default))
    if target in ("hermes", "both"):
        results.append(patch_hermes())
    return ctx.text(tool_name, json.dumps(results, indent=2))
