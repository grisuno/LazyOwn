"""MCP tool ``lazyown_session_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_session_status",
    description=(
        "Show live C2 session state: active implants, their OS/user/hostname/IPs, "
        "privileged vs unprivileged status, discovered hosts, and open campaign tasks. "
        "Reads sessions/{client_id}.log CSV files, sessions/hostsdiscovery.txt, "
        "and sessions/tasks.json without touching lazyc2.py."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "client_id": {
                "type": "string",
                "description": "Filter to a specific client_id (default: all).",
                "default": "",
            },
            "show_tasks": {
                "type": "boolean",
                "description": "Include campaign task board (default true).",
                "default": True,
            },
            "show_outputs": {
                "type": "boolean",
                "description": "Include latest command outputs per implant (default false).",
                "default": False,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_session_status MCP tool."""
    filter_id = arguments.get("client_id", "").strip()
    show_tasks = bool(arguments.get("show_tasks", True))
    show_outputs = bool(arguments.get("show_outputs", False))
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from session_reader import get_aggregator as _get_session_agg

        summary = _get_session_agg().aggregate(ctx.sessions_dir)

        lines: list[str] = []

        # -- Active implants --
        client_ids = summary.active_client_ids
        if filter_id:
            client_ids = [c for c in client_ids if filter_id in c]
        lines.append(f"Active implants: {len(client_ids)}")
        for cid in client_ids:
            rec = summary.latest_for(cid)
            if rec is None:
                continue
            priv = "PRIVILEGED" if rec.is_privileged else "user"
            lines.append(f"  [{priv}] {cid} | {rec.hostname} | {rec.platform} | user={rec.user} | ips={rec.ips}")
            if rec.result_portscan:
                lines.append(f"    portscan: {rec.result_portscan[:120]}")
            if show_outputs and rec.output:
                lines.append(f"    last output: {rec.output[:200]}")

        # -- Privileged vs unprivileged summary --
        priv_count = len(summary.privileged_sessions)
        unpriv_count = len(summary.unprivileged_sessions)
        lines.append("")
        lines.append(f"Privileged sessions: {priv_count} | Unprivileged: {unpriv_count}")

        # -- Discovered hosts --
        if summary.discovered_hosts:
            lines.append("")
            lines.append(f"Discovered hosts ({len(summary.discovered_hosts)}):")
            for h in summary.discovered_hosts[:30]:
                lines.append(f"  {h}")

        # -- Command outputs --
        if show_outputs and summary.command_outputs:
            lines.append("")
            lines.append(f"Recent command outputs ({len(summary.command_outputs)} files):")
            for stem, content in list(summary.command_outputs.items())[-5:]:
                lines.append(f"  [{stem}] {content[:150]}")

        # -- Campaign tasks --
        if show_tasks and summary.tasks:
            lines.append("")
            lines.append(f"Campaign tasks ({len(summary.tasks)}):")
            for t in summary.tasks:
                lines.append(f"  [{t.status:8s}] #{t.id} {t.title} (op={t.operator})")

        if not lines or (len(client_ids) == 0 and not summary.discovered_hosts):
            lines.append("No active sessions found. Start lazyc2.py and wait for implants.")

        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[session_status error] {exc}")
