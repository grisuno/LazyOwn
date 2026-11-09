"""MCP tool ``lazyown_atomic_clean`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_atomic_clean",
    description=(
        "Clean up engagement artefacts. Soft mode (default) kills the "
        "target agent, wipes drop files and test outputs via the live "
        "session, and clears local staging; loot, reports and logs are "
        "always kept. Hard mode (--hard, needs confirm=true) also stops "
        "and removes the lab gym container."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP. Defaults to rhost from payload.json.",
                "default": "",
            },
            "hard": {
                "type": "boolean",
                "description": "Also destroy the gym container (requires confirm=true).",
                "default": False,
            },
            "confirm": {
                "type": "boolean",
                "description": "Required true when hard=true.",
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_atomic_clean MCP tool."""
    if bool(arguments.get("hard", False)) and not bool(arguments.get("confirm", False)):
        return ctx.text(tool_name, "[atomic_clean] hard=true destroys the lab gym: re-call with confirm=true.")
    _cfg = ctx.load_payload()
    cl_target = (arguments.get("target", "") or "").strip() or str(_cfg.get("rhost", "") or "").strip()
    if not cl_target:
        return ctx.text(tool_name, "[atomic_clean] target is required (or set rhost).")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from atomic_exploit_bridge import cleanup_target as _cleanup

        report = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _cleanup(cl_target, hard=bool(arguments.get("hard", False)))
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[atomic_clean error] {exc}")
    lines = [f"[atomic_clean {report.get('mode')}] target={cl_target}"]
    for step in report.get("remote", []):
        lines.append(
            f"  remote/{'ok' if step.get('ok') else 'FAIL'}: {step.get('step')}: {str(step.get('detail', ''))[:120]}"
        )
    for path in report.get("local", [])[:10]:
        lines.append(f"  local: removed {path}")
    if report.get("gym"):
        lines.append(f"  gym: {'removed' if report['gym'].get('ok') else report['gym'].get('detail', 'failed')}")
    lines.append("Loot, reports and logs are always kept.")
    return ctx.text(tool_name, "\n".join(lines))
