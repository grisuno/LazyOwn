"""MCP tool ``lazyown_stealth``: toggle stealth mode for later operations."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_VALID_LEVELS = ("low", "medium", "high", "paranoid", "off")

TOOL = types.Tool(
    name="lazyown_stealth",
    description=(
        "Enable or disable stealth mode for subsequent operations. "
        "Stealth levels: low (normal), medium (2-8s delays, limited concurrency), "
        "high (10-30s delays, single-threaded), paranoid (30-120s delays, minimal traffic), "
        "off (disable stealth)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "level": {
                "type": "string",
                "description": "Stealth level: low, medium, high, paranoid, or off",
            },
        },
        "required": ["level"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Set the stealth level on the exploit engine and persist it to config."""
    level = str(arguments.get("level", "medium")).lower()
    if level not in _VALID_LEVELS:
        return ctx.text(tool_name, json.dumps({"error": f"Invalid level: {level}"}, indent=2))
    try:
        from modules.autonomous_exploit_engine import AutonomousExploitEngine

        engine = AutonomousExploitEngine.get_instance()
        if level == "off":
            engine.enable_stealth("low")
            cfg = ctx.load_payload()
            cfg["stealth_mode"] = "off"
            ctx.save_payload(cfg)
            return ctx.text(tool_name, json.dumps({"stealth": "off"}, indent=2))
        config = engine.enable_stealth(level)
        cfg = ctx.load_payload()
        cfg["stealth_mode"] = level
        ctx.save_payload(cfg)
        return ctx.text(tool_name, json.dumps({"stealth": level, "config": config}, indent=2, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
