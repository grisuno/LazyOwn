"""MCP tool ``lazyown_list_targets`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_targets",
    description=(
        "List all targets stored in payload.json. "
        "Shows IP, domain, ports, status, tags, and notes for each target. "
        "Use this to decide which target to attack next."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "status_filter": {
                "type": "string",
                "description": "Filter by status: pending, in_progress, owned, blocked, done, or 'all' (default).",
                "default": "all",
            }
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_targets MCP tool."""
    cfg = ctx.load_payload()
    targets = cfg.get("targets", [])
    status_filter = arguments.get("status_filter", "all")

    if status_filter != "all":
        targets = [t for t in targets if t.get("status") == status_filter]

    if not targets:
        return ctx.text(tool_name, f"No targets{' with status=' + status_filter if status_filter != 'all' else ''}.")

    status_icon = {"pending": "⏳", "in_progress": "🔄", "owned": "✅", "blocked": "🚫", "done": "☑️"}
    lines = [f"Targets ({len(targets)}):\n"]
    for t in targets:
        icon = status_icon.get(t.get("status", ""), "❓")
        ports_str = ",".join(str(p) for p in t.get("ports", [])) or "unknown"
        lines.append(
            f"{icon} {t['ip']:<18} {t.get('domain', ''):<25} ports:[{ports_str}]  "
            f"tags:{t.get('tags', [])}  status:{t.get('status', '?')}"
        )
        if t.get("notes"):
            lines.append(f"   notes: {t['notes']}")
    return ctx.text(tool_name, "\n".join(lines))
