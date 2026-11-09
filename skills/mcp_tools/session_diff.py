"""MCP tool ``lazyown_session_diff`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from lazyown_mcp_helpers import diff_snapshot, take_snapshot
from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_session_diff",
    description=(
        "Diff between sessions: returns added/modified/removed files in sessions/, "
        "new credentials, new tasks since the last snapshot. Pass take=true to overwrite "
        "the snapshot after diffing (e.g. at the start of a new shift)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "take": {
                "type": "boolean",
                "description": "Overwrite the snapshot after diffing (default false).",
                "default": False,
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_session_diff MCP tool."""
    take_snap = bool(arguments.get("take", False))
    wm_path_sd = ctx.sessions_dir / "world_model.json"
    wm_data_sd: dict = {}
    if wm_path_sd.exists():
        try:
            wm_data_sd = json.loads(wm_path_sd.read_text())
        except (OSError, json.JSONDecodeError):
            wm_data_sd = {}
    tasks_path_sd = ctx.sessions_dir / "tasks.json"
    tasks_data_sd: list = []
    if tasks_path_sd.exists():
        try:
            tasks_data_sd = json.loads(tasks_path_sd.read_text())
        except (OSError, json.JSONDecodeError):
            tasks_data_sd = []
    diff_result = diff_snapshot(
        sessions_dir=ctx.sessions_dir,
        payload=ctx.load_payload(),
        world_model=wm_data_sd,
        tasks=tasks_data_sd,
    )
    if take_snap:
        take_snapshot(ctx.sessions_dir, ctx.load_payload(), wm_data_sd, tasks_data_sd)
        diff_result["snapshot_overwritten"] = True
    return ctx.text(tool_name, json.dumps(diff_result, indent=2, default=str))
