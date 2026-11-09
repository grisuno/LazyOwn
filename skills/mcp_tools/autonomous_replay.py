"""MCP tool ``lazyown_autonomous_replay`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_autonomous_replay",
    description=(
        "Replay the recorded autonomous_events.jsonl decision sequence "
        "between two event ids. In 'trace' mode (default) no command is "
        "re-executed: the report lists the recorded STEP_START decisions "
        "and flags any divergence where the recorded decision_seed does "
        "not match the recomputed one. In 'execute' mode each command is "
        "rerun through the same ICommandRunner chain the live daemon "
        "uses, so harness permissions and hooks still apply."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "from_event_id": {
                "type": "string",
                "description": "Inclusive lower bound on event id; empty replays from the start.",
                "default": "",
            },
            "to_event_id": {
                "type": "string",
                "description": "Inclusive upper bound on event id; empty replays to the end.",
                "default": "",
            },
            "mode": {
                "type": "string",
                "description": "Replay mode.",
                "enum": ["trace", "execute"],
                "default": "trace",
            },
            "timeout": {
                "type": "integer",
                "description": "Per-command timeout in seconds, execute mode only.",
                "default": 60,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_autonomous_replay MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "skills"))
        from autonomous_replay import replay as _replay

        mode = str(arguments.get("mode", "trace")).strip().lower() or "trace"
        from_event_id = arguments.get("from_event_id") or None
        to_event_id = arguments.get("to_event_id") or None
        timeout = int(arguments.get("timeout", 60))
        report = _replay(
            from_event_id=from_event_id,
            to_event_id=to_event_id,
            mode=mode,
            timeout=timeout,
        )
        return ctx.text(tool_name, json.dumps(report, indent=2, ensure_ascii=False))
    except ValueError as exc:
        return ctx.text(tool_name, f"[autonomous_replay error] {exc}")
    except Exception as exc:
        return ctx.text(tool_name, f"[autonomous_replay error] {exc}")
