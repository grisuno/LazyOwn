"""MCP tool ``lazyown_parquet_query`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_parquet_query",
    description=(
        "Query the LazyOwn Parquet knowledge base. "
        "Two modes:\n"
        "  1. Session knowledge: filter by phase (recon/scanning/exploit/privesc/"
        "credential/lateral/persistence/exfil/c2/reporting/other) and target IP "
        "to see what commands succeeded or failed in the past.\n"
        "  2. Keyword search: find relevant entries across ALL parquets "
        "(GTFOBins, LOLBAS, MITRE ATT&CK techniques, session history).\n"
        "Use 'context' mode to get a full phase-aware briefing that combines "
        "session history + GTFOBins + MITRE techniques for planning."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["session", "keyword", "context", "stats", "list"],
                "description": (
                    "Query mode: "
                    "'session' = filter session_knowledge by phase/target; "
                    "'keyword' = search all parquets for a keyword; "
                    "'context' = full phase briefing (session+GTFOBins+MITRE); "
                    "'stats' = show session_knowledge statistics; "
                    "'list' = list available parquets."
                ),
                "default": "context",
            },
            "phase": {
                "type": "string",
                "description": (
                    "Attack phase filter. One of: recon, scanning, exploit, "
                    "post_exploit, privesc, credential, lateral, persistence, "
                    "exfil, c2, reporting, other. Required for 'session' and 'context' modes."
                ),
            },
            "target": {
                "type": "string",
                "description": "Target IP to filter by (default: rhost from config).",
            },
            "keyword": {
                "type": "string",
                "description": "Search keyword for 'keyword' mode (e.g. 'smb', 'kerberos', 'sudo').",
            },
            "parquet": {
                "type": "string",
                "description": (
                    "Restrict keyword search to one parquet. "
                    "Options: binarios, detalles, lolbas_index, lolbas_details, "
                    "techniques, session_knowledge. Default: all."
                ),
            },
            "success_only": {
                "type": "boolean",
                "description": "In session mode: only return rows where success=True.",
                "default": False,
            },
            "limit": {
                "type": "integer",
                "description": "Max rows per result set.",
                "default": 15,
            },
            "sync": {
                "type": "boolean",
                "description": "Re-ingest CSV before querying (default false).",
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_parquet_query MCP tool."""
    try:
        from lazyown_parquet_db import get_pdb as _get_pdb

        _pdb = _get_pdb()
    except Exception:
        return ctx.text(tool_name, "ParquetDB unavailable. Run: pip install pandas pyarrow")
    mode = arguments.get("mode", "context")
    cfg = ctx.load_payload()
    target = arguments.get("target") or cfg.get("rhost") or None
    phase = arguments.get("phase", "recon")
    keyword = arguments.get("keyword", "")
    parquet_name = arguments.get("parquet")
    success_only = bool(arguments.get("success_only", False))
    limit = int(arguments.get("limit", 15))
    do_sync = bool(arguments.get("sync", False))

    def _run_parquet_query() -> str:
        if do_sync:
            _pdb.sync()

        if mode == "stats":
            return _pdb.stats()

        if mode == "list":
            return "Available parquets:\n" + "\n".join(f"  • {p}" for p in _pdb.list_parquets())

        if mode == "keyword":
            if not keyword:
                return "keyword mode requires 'keyword' argument."
            results = _pdb.query_knowledge(keyword, parquet_name, limit=limit)
            if not results:
                return f"No results for keyword '{keyword}'."
            out_parts: list = []
            for stem, rows in results.items():
                out_parts.append(f"\n── {stem} ({len(rows)} matches) ──")
                for r in rows[:5]:
                    out_parts.append(json.dumps({k: str(v)[:100] for k, v in r.items()}, ensure_ascii=False))
            return "\n".join(out_parts)

        if mode == "session":
            rows = _pdb.query_session(
                phase=phase,
                target=target,
                success_only=success_only,
                limit=limit,
            )
            if not rows:
                return f"No session rows for phase='{phase}' target='{target}'."
            return json.dumps(rows, indent=2, default=str)

        # mode == "context" (default)
        ctx = _pdb.context_for_phase(phase, target, limit=limit)
        return json.dumps(ctx, indent=2, default=str)

    result = await asyncio.get_event_loop().run_in_executor(None, _run_parquet_query)
    return ctx.text(tool_name, result)
