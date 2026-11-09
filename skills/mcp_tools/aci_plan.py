"""MCP tool ``lazyown_aci_plan`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_aci_plan",
    description=(
        "AUTONOMOUS CAMPAIGN INTELLIGENCE — decompose a natural-language engagement goal "
        "into a MITRE ATT&CK-aligned tactical plan. "
        "Generates phase-by-phase objectives (recon → exploit → privesc → lateral → cred → report), "
        "injects them into the ObjectiveStore, and persists the plan to sessions/aci_plan.json. "
        "Uses Groq LLM when api_key is set; falls back to static ATT&CK kill-chain template. "
        "After calling this, run lazyown_auto_loop() to start autonomous execution. "
        "Example: goal='Compromise the domain controller at corp.internal starting from a web foothold', target='10.10.11.5'"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "Natural-language engagement goal (what you want to accomplish).",
            },
            "target": {
                "type": "string",
                "description": "Primary target IP or hostname (default: rhost from payload.json).",
                "default": "",
            },
            "scope": {
                "type": "array",
                "items": {"type": "string"},
                "description": "CIDR ranges or IPs in scope (e.g. ['10.10.11.0/24']).",
                "default": [],
            },
            "domain": {
                "type": "string",
                "description": "Target domain (e.g. 'corp.internal'). Optional.",
                "default": "",
            },
            "os_hint": {
                "type": "string",
                "description": "Target OS hint: 'linux', 'windows', or 'unknown'.",
                "enum": ["linux", "windows", "unknown"],
                "default": "unknown",
            },
            "phase_filter": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Only include these phase slugs (e.g. ['recon','exploit','privesc']). Default: all phases.",
                "default": None,
            },
        },
        "required": ["goal"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_aci_plan MCP tool."""
    try:
        from aci_planner import mcp_aci_plan as _aci_plan
    except Exception:
        return ctx.text(tool_name, "[aci_plan] aci_planner module unavailable.")
    try:
        result = _aci_plan(
            goal=arguments.get("goal", ""),
            target=arguments.get("target", ""),
            scope=arguments.get("scope") or [],
            domain=arguments.get("domain", ""),
            os_hint=arguments.get("os_hint", "unknown"),
            phase_filter=arguments.get("phase_filter") or None,
        )
        return ctx.text(tool_name, result)
    except Exception as exc:
        return ctx.text(tool_name, f"[aci_plan error] {exc}")
