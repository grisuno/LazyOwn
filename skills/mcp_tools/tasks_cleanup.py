"""MCP tool ``lazyown_tasks_cleanup`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from lazyown_mcp_helpers import audit_tasks
from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_tasks_cleanup",
    description=(
        "Audit sessions/tasks.json: detect bogus task entries (timestamps misclassified "
        "as credentials, URLs as credentials, IP-only values, duplicates) and optionally "
        "remove them. Always returns the audit; pass dry_run=false to actually rewrite tasks.json."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "dry_run": {
                "type": "boolean",
                "description": "If true (default) only reports what would be removed; no write.",
                "default": True,
            },
            "min_confidence": {
                "type": "number",
                "description": "Minimum credential-likelihood score to keep (0.0..1.0, default 0.5).",
                "default": 0.5,
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_tasks_cleanup MCP tool."""
    dry_run_tc = arguments.get("dry_run", True)
    if isinstance(dry_run_tc, str):
        dry_run_tc = dry_run_tc.lower() != "false"
    else:
        dry_run_tc = bool(dry_run_tc)
    min_conf = float(arguments.get("min_confidence", 0.5))
    tasks_path_tc = ctx.sessions_dir / "tasks.json"
    if not tasks_path_tc.exists():
        return ctx.text(tool_name, json.dumps({"error": "sessions/tasks.json not found"}))
    try:
        current_tasks = json.loads(tasks_path_tc.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return ctx.text(tool_name, json.dumps({"error": f"cannot parse tasks.json: {exc}"}))

    audits = audit_tasks(current_tasks, min_confidence=min_conf)
    keep_ids = {a.task_id for a in audits if a.keep}
    kept = [t for t in current_tasks if t.get("id") in keep_ids]
    dropped = [
        {
            "id": a.task_id,
            "status": a.status,
            "reason": a.reason,
            "confidence": a.confidence,
            "title": a.title[:120],
            "parsed_value": a.parsed_value,
        }
        for a in audits
        if not a.keep
    ]

    result = {
        "dry_run": dry_run_tc,
        "total_before": len(current_tasks),
        "total_after": len(kept),
        "dropped_count": len(dropped),
        "dropped": dropped[:50],
        "min_confidence": min_conf,
    }
    if not dry_run_tc and dropped:
        backup = ctx.sessions_dir / "tasks.json.bak"
        try:
            backup.write_text(json.dumps(current_tasks, indent=2))
            tasks_path_tc.write_text(json.dumps(kept, indent=2))
            result["backup_written"] = str(backup)
        except OSError as exc:
            result["error"] = f"write failed: {exc}"
    return ctx.text(tool_name, json.dumps(result, indent=2, default=str))
