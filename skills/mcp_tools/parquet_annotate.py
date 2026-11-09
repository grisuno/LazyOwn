"""MCP tool ``lazyown_parquet_annotate`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_parquet_annotate",
    description=(
        "Annotate a session row in session_knowledge.parquet with the actual "
        "outcome of a command after it has executed. "
        "Use the row 'id' from lazyown_parquet_query results. "
        "This is how the knowledge base learns: MCP runs a command, observes "
        "the output, then calls annotate to record whether it succeeded. "
        "Over time this builds a high-quality training dataset."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "row_id": {
                "type": "string",
                "description": "The 16-char hex id from session_knowledge.parquet.",
            },
            "success": {
                "type": "boolean",
                "description": "Whether the command succeeded.",
            },
            "category": {
                "type": "string",
                "description": (
                    "Override the attack category. One of: recon, scanning, exploit, "
                    "post_exploit, privesc, credential, lateral, persistence, exfil, "
                    "c2, reporting, other."
                ),
            },
            "outcome": {
                "type": "string",
                "description": "Detailed outcome string (e.g. 'success', 'failure', 'partial').",
            },
        },
        "required": ["row_id"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_parquet_annotate MCP tool."""
    try:
        from lazyown_parquet_db import get_pdb as _get_pdb

        _pdb = _get_pdb()
    except Exception:
        return ctx.text(tool_name, "ParquetDB unavailable. Run: pip install pandas pyarrow")
    row_id = arguments.get("row_id", "")
    success = arguments.get("success")  # may be None
    category = arguments.get("category")
    outcome = arguments.get("outcome")

    if not row_id:
        return ctx.text(tool_name, "row_id is required.")

    ok = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: _pdb.annotate(row_id, success=success, category=category, outcome=outcome),
    )
    if ok:
        return ctx.text(tool_name, f"Annotated row {row_id}: success={success} category={category} outcome={outcome}")
    return ctx.text(tool_name, f"Row id not found: {row_id}. Run lazyown_parquet_query(mode='session') to list ids.")
