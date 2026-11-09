"""MCP tool ``lazyown_db``: query and mutate the LazyOwn SQLite database."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_db",
    description=(
        "Query and mutate the LazyOwn SQLite database (sessions/db/lazyown.db). "
        "Operations: status, workspace_list, workspace_create, host_list, host_add, "
        "host_find, service_list, service_add, vuln_list, vuln_add, cred_list, "
        "cred_add, loot_list, loot_add, note_list, note_add, import_nmap, export_csv. "
        "Entity lists are filtered by the active workspace; creds come back decrypted."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "operation": {"type": "string", "description": "DB operation to perform (see description)"},
            "workspace": {"type": "string", "description": "Workspace name (default 'default')"},
            "workspace_id": {"type": "integer", "description": "Numeric workspace id (overrides workspace name)"},
            "host_id": {"type": "integer", "description": "Host id for service/vuln/cred operations"},
            "address": {"type": "string", "description": "Host IP address for host_add / host_find"},
            "hostname": {"type": "string", "description": "Host name for host_add"},
            "os": {"type": "string", "description": "Operating system for host_add"},
            "mac": {"type": "string", "description": "MAC address for host_add"},
            "query": {"type": "string", "description": "Search string for host_find"},
            "port": {"type": "integer", "description": "Port for service_add"},
            "protocol": {"type": "string", "description": "Protocol for service_add (tcp/udp)"},
            "name": {"type": "string", "description": "Entity name (service/vuln/loot/workspace)"},
            "product": {"type": "string", "description": "Service product"},
            "version": {"type": "string", "description": "Service version"},
            "severity": {
                "type": "string",
                "description": "Vuln severity filter or value (critical/high/medium/low/unknown)",
            },
            "description": {"type": "string", "description": "Description for vuln_add or workspace_create"},
            "refs": {"type": "string", "description": "Vuln references"},
            "username": {"type": "string", "description": "Credential username"},
            "password": {"type": "string", "description": "Credential password"},
            "realm": {"type": "string", "description": "Credential realm/domain"},
            "cred_type": {"type": "string", "description": "Credential type (password/hash/ticket)"},
            "loot_type": {"type": "string", "description": "Loot type (file/hash/creds/artifact)"},
            "path": {"type": "string", "description": "Loot path"},
            "notes": {"type": "string", "description": "Loot or note text"},
            "xml_path": {"type": "string", "description": "Path to nmap XML for import_nmap"},
            "table": {
                "type": "string",
                "description": "Table for export_csv (hosts/services/vulns/creds/loot/notes)",
            },
        },
        "required": ["operation"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Dispatch one SQLite campaign-database operation and return its result.

    Args:
        arguments: Tool arguments with an ``operation`` key and per-operation
            fields.
        tool_name: MCP tool name for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A ``TextContent`` payload with the operation result as JSON.
    """
    from modules.db import get_db

    operation = str(arguments.get("operation", "")).strip().lower()
    if not operation:
        return ctx.text(tool_name, "Missing required 'operation' argument.")

    db = get_db()
    ws_name = arguments.get("workspace") or "default"
    wid = arguments.get("workspace_id") or db.workspace_get(ws_name)["id"]

    def _result(payload: Any) -> list:
        return ctx.text(tool_name, json.dumps(payload, indent=2, default=str))

    try:
        if operation == "status":
            return _result({"db_path": db.db_path, "counts": db.status(wid)})
        if operation == "workspace_list":
            return _result(db.workspace_list())
        if operation == "workspace_create":
            return _result({"workspace_id": db.workspace_create(ws_name, arguments.get("description", ""))})
        if operation == "host_list":
            return _result(db.host_list(wid))
        if operation == "host_find":
            return _result(db.host_find(wid, arguments.get("query", "")))
        if operation == "host_add":
            return _result(
                {
                    "host_id": db.host_add(
                        wid,
                        arguments["address"],
                        arguments.get("mac", ""),
                        arguments.get("hostname", ""),
                        arguments.get("os", ""),
                        arguments.get("state", "unknown"),
                    )
                }
            )
        if operation == "service_list":
            return _result(db.service_list(int(arguments.get("host_id", 0))))
        if operation == "service_add":
            return _result(
                {
                    "service_id": db.service_add(
                        int(arguments["host_id"]),
                        int(arguments["port"]),
                        arguments.get("protocol", "tcp"),
                        arguments.get("state", "open"),
                        arguments.get("name", ""),
                        arguments.get("product", ""),
                        arguments.get("version", ""),
                    )
                }
            )
        if operation == "vuln_list":
            return _result(db.vuln_list(wid, arguments.get("severity") or None))
        if operation == "vuln_add":
            return _result(
                {
                    "vuln_id": db.vuln_add(
                        int(arguments["host_id"]),
                        arguments["name"],
                        arguments.get("severity", "unknown"),
                        arguments.get("description", ""),
                        arguments.get("refs", ""),
                    )
                }
            )
        if operation == "cred_list":
            return _result(db.cred_list(wid))
        if operation == "cred_add":
            return _result(
                {
                    "cred_id": db.cred_add(
                        int(arguments["host_id"]),
                        arguments.get("username", ""),
                        arguments.get("password", ""),
                        arguments.get("realm", ""),
                        arguments.get("cred_type", "password"),
                        arguments.get("origin", "manual"),
                    )
                }
            )
        if operation == "loot_list":
            return _result(db.loot_list(wid))
        if operation == "loot_add":
            return _result(
                {
                    "loot_id": db.loot_add(
                        wid,
                        arguments["name"],
                        arguments.get("loot_type", "file"),
                        arguments.get("path", ""),
                        arguments.get("notes", ""),
                        int(arguments["host_id"]) if arguments.get("host_id") else None,
                    )
                }
            )
        if operation == "note_list":
            return _result(db.note_list(wid))
        if operation == "note_add":
            return _result(
                {
                    "note_id": db.note_add(
                        wid,
                        arguments.get("notes", arguments.get("data", "")),
                        arguments.get("note_type", "general"),
                        int(arguments["host_id"]) if arguments.get("host_id") else None,
                    )
                }
            )
        if operation == "import_nmap":
            return _result(db.import_nmap_xml(wid, arguments.get("xml_path", "")))
        if operation == "export_csv":
            return _result({"csv": db.export_csv(arguments.get("table", ""), wid)})
        return ctx.text(tool_name, f"Unknown operation '{operation}'.")
    except KeyError as error:
        return ctx.text(tool_name, f"Missing required argument for {operation}: {error}")
    except Exception as error:
        return ctx.text(tool_name, f"lazyown_db {operation} failed: {error}")
