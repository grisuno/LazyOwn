"""MCP tool ``lazyown_cron_schedule`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_cron_schedule",
    description=(
        "Schedule a LazyOwn command to run at a specific time using the built-in "
        "cron system. LazyOwn's cron acts as a time-motor for autonomous activities: "
        "schedule recon at intervals, privesc attempts, lateral movement, or any "
        "command from the bridge catalog. Format: HH:MM. "
        "List scheduled crons or remove one by ID."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["add", "list", "remove"],
                "description": "'add' schedules a command; 'list' shows all; 'remove' deletes by ID.",
                "default": "list",
            },
            "time": {
                "type": "string",
                "description": "Execution time as HH:MM (required for action='add').",
                "default": "",
            },
            "command": {
                "type": "string",
                "description": "LazyOwn command to schedule (required for action='add').",
                "default": "",
            },
            "args": {
                "type": "string",
                "description": "Optional arguments for the command.",
                "default": "",
            },
            "cron_id": {
                "type": "string",
                "description": "Cron entry ID to remove (required for action='remove').",
                "default": "",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_cron_schedule MCP tool."""
    action = arguments.get("action", "list")
    cron_dir = ctx.sessions_dir / "crons"

    def _load_crons() -> list[dict]:
        path = cron_dir / "scheduled.json"
        if not path.exists():
            return []
        try:
            import json as _json

            return _json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save_crons(entries: list[dict]) -> None:
        cron_dir.mkdir(parents=True, exist_ok=True)
        path = cron_dir / "scheduled.json"
        import json as _json

        tmp = str(path) + ".tmp"
        Path(tmp).write_text(_json.dumps(entries, indent=2), encoding="utf-8")
        import os as _os

        _os.replace(tmp, str(path))

    if action == "list":
        entries = _load_crons()
        if not entries:
            return ctx.text(
                tool_name,
                "No cron entries scheduled. Use action='add' time='HH:MM' command='...' "
                "to schedule a command. LazyOwn cron: cron HH:MM <command> [args]",
            )
        lines = [f"Scheduled crons ({len(entries)}):"]
        for e in entries:
            lines.append(f"  [{e.get('id', '?')}] {e.get('time', '?')} -> {e.get('command', '')} {e.get('args', '')}")
        return ctx.text(tool_name, "\n".join(lines))

    elif action == "add":
        cron_time = arguments.get("time", "").strip()
        command = arguments.get("command", "").strip()
        if not cron_time or not command:
            return ctx.text(tool_name, "[cron_schedule] 'time' (HH:MM) and 'command' are required.")
        import re as _re

        if not _re.match(r"^\d{2}:\d{2}$", cron_time):
            return ctx.text(tool_name, f"[cron_schedule] Invalid time format '{cron_time}'. Use HH:MM.")
        cron_args = arguments.get("args", "").strip()
        entries = _load_crons()
        import uuid as _uuid

        new_id = str(_uuid.uuid4())[:8]
        entries.append(
            {
                "id": new_id,
                "time": cron_time,
                "command": command,
                "args": cron_args,
            }
        )
        _save_crons(entries)
        # Also run via LazyOwn cron system
        full_cron_cmd = f"cron {cron_time} {command}"
        if cron_args:
            full_cron_cmd += f" {cron_args}"
        ctx.run_command(full_cron_cmd, timeout=10)
        return ctx.text(
            tool_name,
            f"Cron #{new_id} added: {cron_time} -> {command} {cron_args}\nLazyOwn cron registered: {full_cron_cmd}",
        )

    elif action == "remove":
        cron_id = arguments.get("cron_id", "").strip()
        if not cron_id:
            return ctx.text(tool_name, "[cron_schedule] 'cron_id' is required for action='remove'.")
        entries = _load_crons()
        before = len(entries)
        entries = [e for e in entries if e.get("id") != cron_id]
        if len(entries) == before:
            return ctx.text(tool_name, f"Cron ID '{cron_id}' not found.")
        _save_crons(entries)
        return ctx.text(tool_name, f"Cron #{cron_id} removed.")
    else:
        return ctx.text(tool_name, f"[cron_schedule] Unknown action '{action}'. Use: add, list, remove.")
