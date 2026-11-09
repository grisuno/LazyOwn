"""MCP tool ``lazyown_atomic_shell`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_atomic_shell",
    description=(
        "Verify a live multiplexed root shell session on the target. "
        "Read-only check: reports live/via plus the attach hint. "
        "Interactive REPL is foreground-terminal only and NEVER runs "
        "through MCP — attach from the LazyOwn shell with "
        "atomic_shell --interactive <target>."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP. Defaults to rhost from payload.json.",
                "default": "",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_atomic_shell MCP tool."""
    _cfg = ctx.load_payload()
    sh_target = (arguments.get("target", "") or "").strip() or str(_cfg.get("rhost", "") or "").strip()
    if not sh_target:
        return ctx.text(tool_name, "[atomic_shell] target is required (or set rhost).")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from atomic_exploit_bridge import interactive_shell as _shell_check

        result = _shell_check(sh_target, interactive=False)
    except Exception as exc:
        return ctx.text(tool_name, f"[atomic_shell error] {exc}")
    if result.get("live"):
        return ctx.text(
            tool_name,
            f"[atomic_shell] live session on {sh_target} via {result.get('via')}. "
            f"Attach from a foreground terminal: atomic_shell --interactive {sh_target}",
        )
    return ctx.text(tool_name, f"[atomic_shell] no live session on {sh_target}: {result.get('error', 'unknown')}")
