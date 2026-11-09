"""MCP tool ``lazyown_reactive_suggest`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_reactive_suggest",
    description=(
        "Parse raw command output and return prioritised reactive decisions. "
        "Detects: AV/EDR blocks (evasion via amsi.yaml/darkarmour), "
        "privesc hints (SUID/sudo/polkit → adversary_yaml/lazypwn), "
        "credentials found, new hosts discovered, service versions, "
        "and shell errors (switch-tool recommendations). "
        "Priority 1-2 decisions are auto-injected into the next auto_loop step."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "output": {
                "type": "string",
                "description": "Raw command output to analyse.",
            },
            "command": {
                "type": "string",
                "description": "The command that produced the output.",
                "default": "",
            },
            "platform": {
                "type": "string",
                "description": "Target platform: 'linux', 'windows', or 'unknown'.",
                "enum": ["linux", "windows", "unknown"],
                "default": "unknown",
            },
            "max_decisions": {
                "type": "integer",
                "description": "Maximum decisions to return (default 5).",
                "default": 5,
            },
        },
        "required": ["output"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_reactive_suggest MCP tool."""
    raw_output = arguments.get("output", "")
    command = arguments.get("command", "")
    platform = arguments.get("platform", "unknown")
    max_decisions = int(arguments.get("max_decisions", 5))
    if not raw_output.strip():
        return ctx.text(tool_name, "[reactive_suggest] 'output' field is required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from reactive_engine import get_engine as _get_react_engine

        engine = _get_react_engine()
        decisions = engine.analyse(
            output=raw_output,
            command=command,
            platform=platform,
        )
        if not decisions:
            return ctx.text(tool_name, "No reactive signals detected in the provided output.")
        lines = [
            f"Reactive analysis — {len(decisions)} decision(s) found:",
            "",
        ]
        for i, d in enumerate(decisions[:max_decisions], 1):
            sigs = ", ".join(f"{s.kind}({s.value[:30]})" for s in d.signals[:3])
            lines.append(f"  {i}. [{d.action:12s}] priority={d.priority}")
            lines.append(f"       Command : {d.command}")
            lines.append(f"       Reason  : {d.reason}")
            lines.append(f"       MITRE   : {d.mitre_tactic}")
            lines.append(f"       Signals : {sigs}")
            lines.append("")
        if decisions and decisions[0].priority <= 2:
            lines.append(
                f"AUTO-INJECT: top decision (priority {decisions[0].priority}) will be used as next auto_loop step."
            )
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[reactive_suggest error] {exc}")
