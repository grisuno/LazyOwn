"""MCP tool ``lazyown_campaign_tasks`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_campaign_tasks",
    description=(
        "Manage campaign tasks in sessions/tasks.json. "
        "Statuses: New -> Refined -> Started -> Review -> Qa -> Done | Blocked. "
        "Use for campaign reporting beyond vulnbot's markdown — full task board "
        "with operator assignments and status tracking."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list", "add", "update"],
                "description": (
                    "'list' = show all tasks; 'add' = create a new task; 'update' = change a task's status."
                ),
                "default": "list",
            },
            "title": {
                "type": "string",
                "description": "Task title (required for action='add').",
                "default": "",
            },
            "description": {
                "type": "string",
                "description": "Task description (used for action='add').",
                "default": "",
            },
            "operator": {
                "type": "string",
                "description": "Operator assigned to the task (default: 'agent').",
                "default": "agent",
            },
            "task_id": {
                "type": "integer",
                "description": "Task ID (required for action='update').",
            },
            "status": {
                "type": "string",
                "enum": ["New", "Refined", "Started", "Review", "Qa", "Done", "Blocked"],
                "description": "New status (required for action='update').",
                "default": "New",
            },
            "filter_status": {
                "type": "string",
                "description": "Filter listed tasks by status (default: all).",
                "default": "",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_campaign_tasks MCP tool."""
    action = arguments.get("action", "list")
    filter_status = arguments.get("filter_status", "").strip()
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from session_reader import TaskReader as _TaskReader
        from session_reader import TaskWriter as _TaskWriter

        if action == "list":
            tasks = _TaskReader().read(ctx.sessions_dir)
            if filter_status:
                tasks = [t for t in tasks if t.status.lower() == filter_status.lower()]
            if not tasks:
                return ctx.text(
                    tool_name,
                    f"No tasks found{' with status=' + filter_status if filter_status else ''}."
                    " Use action='add' to create one.",
                )
            lines = [f"Campaign tasks ({len(tasks)}):"]
            for t in tasks:
                lines.append(f"  #{t.id:3d} [{t.status:8s}] {t.title} (op={t.operator})")
                if t.description:
                    lines.append(f"         {t.description[:100]}")
            return ctx.text(tool_name, "\n".join(lines))

        elif action == "add":
            title = arguments.get("title", "").strip()
            if not title:
                return ctx.text(tool_name, "[campaign_tasks] 'title' is required for action='add'.")
            desc = arguments.get("description", "")
            operator = arguments.get("operator", "agent")
            status = arguments.get("status", "New")
            writer = _TaskWriter(ctx.sessions_dir)
            task = writer.append(
                title=title,
                description=desc,
                operator=operator,
                status=status,
            )
            return ctx.text(tool_name, f"Task #{task.id} created: [{task.status}] {task.title} (op={task.operator})")

        elif action == "update":
            task_id = arguments.get("task_id")
            if task_id is None:
                return ctx.text(tool_name, "[campaign_tasks] 'task_id' is required for action='update'.")
            status = arguments.get("status", "")
            if not status:
                return ctx.text(tool_name, "[campaign_tasks] 'status' is required for action='update'.")
            writer = _TaskWriter(ctx.sessions_dir)
            ok = writer.update_status(int(task_id), status)
            if ok:
                return ctx.text(tool_name, f"Task #{task_id} updated to status '{status}'.")
            return ctx.text(tool_name, f"Task #{task_id} not found.")
        else:
            return ctx.text(tool_name, f"[campaign_tasks] Unknown action '{action}'. Use: list, add, update.")
    except Exception as exc:
        return ctx.text(tool_name, f"[campaign_tasks error] {exc}")
