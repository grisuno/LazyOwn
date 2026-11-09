"""MCP tool ``lazyown_metrics_summary`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_metrics_summary",
    description=(
        "Aggregate the durable command-execution telemetry log "
        "(sessions/metrics.jsonl). Returns total count, per-command "
        "success rate, mean and p95 duration, and the top failing "
        "commands. Optionally restricted to events from the last "
        "window_seconds."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "window_seconds": {
                "type": "integer",
                "description": "Window in seconds; 0 or absent aggregates the whole log.",
                "default": 0,
            },
            "top_n": {
                "type": "integer",
                "description": "Maximum per-command rows to keep in by_command.",
                "default": 10,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_metrics_summary MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from metrics import get_recorder as _get_recorder

        window_raw = int(arguments.get("window_seconds", 0) or 0)
        window = window_raw if window_raw > 0 else None
        top_n = max(1, int(arguments.get("top_n", 10)))
        summary = _get_recorder().summarize(window_seconds=window)
        by_command = summary.get("by_command", {})
        if isinstance(by_command, dict) and len(by_command) > top_n:
            ranked = sorted(
                by_command.items(),
                key=lambda item: item[1].get("count", 0),
                reverse=True,
            )[:top_n]
            summary["by_command"] = dict(ranked)
        return ctx.text(tool_name, json.dumps(summary, indent=2, ensure_ascii=False))
    except Exception as exc:
        return ctx.text(tool_name, f"[metrics_summary error] {exc}")
