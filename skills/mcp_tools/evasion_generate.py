"""MCP tool ``lazyown_evasion_generate``: generate a C2 malleable profile."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_OS_FAMILY = "windows"

TOOL = types.Tool(
    name="lazyown_evasion_generate",
    description=(
        "Generate a new C2 malleable profile with randomized user-agent, "
        "JA4 fingerprint, TLS ciphers, domain front, and jitter. "
        "Profiles are persisted to sessions/evasion_profiles.jsonl."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "os_family": {
                "type": "string",
                "description": "Target OS family: windows, linux, or mac.",
                "enum": ["windows", "linux", "mac"],
                "default": _DEFAULT_OS_FAMILY,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Generate an evasion profile for the requested OS family as JSON."""
    os_family = str(arguments.get("os_family", _DEFAULT_OS_FAMILY))
    try:
        from modules.evasion_engine import EvasionEngine

        engine = EvasionEngine(ctx.load_payload())
        profile = engine.generate_profile(os_family)
        return ctx.text(tool_name, engine.profile_to_json(profile))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
