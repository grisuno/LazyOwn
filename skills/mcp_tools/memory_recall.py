"""MCP tool ``lazyown_memory_recall`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_memory_recall",
    description=(
        "Query the episodic memory store for past command executions. "
        "Returns the most relevant past sessions matching the query — including "
        "what command was run, against which host, what findings were produced, "
        "and whether it succeeded. Use this before choosing a tool to avoid "
        "repeating failed approaches and to reuse proven techniques."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Free-text query: service name, CVE, technique, host IP.",
            },
            "host": {
                "type": "string",
                "description": "Filter results to a specific host IP.",
                "default": "",
            },
            "top_k": {
                "type": "string",
                "description": "Number of results to return (default 5).",
                "default": "5",
            },
        },
        "required": ["query"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_memory_recall MCP tool."""
    query = arguments.get("query", "").strip()
    host = arguments.get("host", "").strip()
    top_k = int(arguments.get("top_k", "5") or "5")
    if not query and not host:
        return ctx.text(tool_name, "[memory_recall] 'query' or 'host' is required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from memory_store import get_memory_store

        ms = get_memory_store()
        entries = ms.recall_by_host(host, top_k=top_k) if (host and not query) else ms.recall(query, top_k=top_k)
        if not entries:
            return ctx.text(tool_name, "No matching memories found.")
        lines = [f"Memory recall: {len(entries)} results for '{query or host}'", ""]
        for e in entries:
            status = "OK" if e.success else "FAIL"
            lines.append(f"[{status}] host={e.host} tool={e.tool}")
            lines.append(f"  cmd: {e.command[:100]}")
            lines.append(f"  out: {e.output_snippet[:120]}")
            if e.findings_json and e.findings_json != "[]":
                lines.append(f"  findings: {e.findings_json[:120]}")
            lines.append("")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[memory_recall error] {exc}")
