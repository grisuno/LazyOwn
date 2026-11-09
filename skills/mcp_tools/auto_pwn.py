"""MCP tool ``lazyown_auto_pwn``: run the full autonomous exploitation chain."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_STEALTH = "low"

TOOL = types.Tool(
    name="lazyown_auto_pwn",
    description=(
        "Execute the full autonomous exploitation chain against a target. "
        "Runs recon, vulnerability scanning, exploit selection, exploitation, "
        "and optionally privilege escalation and auto-pivoting. "
        "Returns comprehensive results with summary."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP or hostname (defaults to payload.json rhost)",
            },
            "enable_pivot": {
                "type": "boolean",
                "description": "Enable automatic pivoting after exploitation",
            },
            "enable_privesc": {
                "type": "boolean",
                "description": "Enable automatic privilege escalation after getting shell",
            },
            "stealth": {
                "type": "string",
                "description": "Stealth level: low, medium, high, or paranoid",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Run the full auto-pwn chain and return results with a summary."""
    target = arguments.get("target") or ctx.load_payload().get("rhost", "")
    enable_pivot = bool(arguments.get("enable_pivot", False))
    enable_privesc = bool(arguments.get("enable_privesc", False))
    stealth = str(arguments.get("stealth", _DEFAULT_STEALTH))
    try:
        from modules.autonomous_exploit_engine import AutonomousExploitEngine

        engine = AutonomousExploitEngine()
        engine.enable_stealth(stealth)
        result = engine.full_auto_pwn(
            target,
            enable_pivot=enable_pivot,
            enable_privesc=enable_privesc,
            stealth=stealth,
        )
        exploits = result.get("exploit_results", [])
        result["summary"] = {
            "target": target,
            "vulnerabilities_found": len(result.get("vulnerabilities", [])),
            "exploits_attempted": len(exploits),
            "exploits_succeeded": len([e for e in exploits if e.get("success")]),
            "shells_obtained": len([e for e in exploits if e.get("shell_obtained")]),
            "privesc_attempts": len(result.get("privesc_results", [])),
            "pivot_chains": len(result.get("pivot_info", {}).get("chains", [])),
            "stealth_level": stealth,
        }
        return ctx.text(tool_name, json.dumps(result, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
