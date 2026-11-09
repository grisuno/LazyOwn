"""MCP tool ``lazyown_lazysearch`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazysearch",
    description=(
        "Search the engagement SQLite workspace with the Shodan-lite grammar: "
        "'port:3389 -host:vpn tech:\"apache tomcat\" sev:critical user:svc'. "
        "Spot keys: host|ip, port, service, product|tech, version, os, state, "
        "sev|severity (crit|hi|med aliases), cve, user; bare words run as free "
        "text; '-' prefix excludes. Queries hosts/services/vulns/creds through "
        "the public database API of the current workspace."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Grammar query, e.g. 'port:3389 -host:vpn sev:high'.",
            },
            "workspace": {
                "type": "string",
                "description": "Workspace name (default 'default').",
                "default": "default",
            },
            "db_path": {
                "type": "string",
                "description": "Optional database path override (default sessions/db/lazyown.db).",
                "default": "",
            },
            "json": {
                "type": "boolean",
                "description": "Emit raw machine-readable rows instead of the compact listing.",
                "default": False,
            },
        },
        "required": ["query"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_lazysearch MCP tool."""
    from modules.lazy_search import execute as _search_execute

    ls_query = str(arguments.get("query", "") or "").strip()
    if not ls_query:
        return ctx.text(tool_name, "[lazysearch] query is required (e.g. 'port:3389 -host:vpn sev:high').")
    ls_workspace = str(arguments.get("workspace", "default") or "default")
    ls_db_path = (arguments.get("db_path", "") or "").strip() or None
    try:
        result = _search_execute(None, ls_query, workspace_name=ls_workspace, db_path=ls_db_path)
    except Exception as exc:
        return ctx.text(tool_name, f"[lazysearch error] {exc}")
    if arguments.get("json"):
        import json as _json

        return ctx.text(tool_name, _json.dumps(result, indent=2, default=str)[-10000:])
    lines = [f"[lazysearch '{ls_query}'] workspace={ls_workspace}"]
    for error in result.get("errors") or []:
        lines.append(f"  error {error}")
    lines.append(
        "matches hosts="
        f"{len(result.get('hosts') or [])} services={len(result.get('services') or [])} "
        f"vulns={len(result.get('vulns') or [])} creds={len(result.get('creds') or [])}"
    )
    for host in (result.get("hosts") or [])[:8]:
        lines.append(f"  host {host.get('address')} os={host.get('os') or '?'} state={host.get('state') or '?'}")
    for service in (result.get("services") or [])[:8]:
        label = " ".join(str(service.get(k) or "") for k in ("name", "product", "version")).strip()
        lines.append(f"  svc {service.get('host')}:{service.get('port')} {label}")
    for vuln in (result.get("vulns") or [])[:8]:
        lines.append(f"  vuln {vuln.get('name')} sev={vuln.get('severity')}")
    for cred in (result.get("creds") or [])[:8]:
        lines.append(f"  cred {cred.get('username')}@{cred.get('address')} type={cred.get('cred_type')}")
    return ctx.text(tool_name, "\n".join(lines))
