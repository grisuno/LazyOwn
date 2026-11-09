"""MCP tool ``lazyown_lazy_finding``: report a finding into the loop engine."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_MAX_NAME = 200
_MAX_SUMMARY = 1000
_MAX_POC = 2000

TOOL = types.Tool(
    name="lazyown_lazy_finding",
    description="Report a finding into the loop engine with evidence, auto-binding recent traffic and proxy body hits.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "name": {"type": "string"},
            "evidence": {"type": "string"},
            "severity": {"type": "string", "enum": ["critical", "high", "medium", "low", "info"]},
            "intent_id": {"type": "integer", "description": "Intent node id when known"},
            "traffic_refs": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["task_id", "name", "evidence"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Persist a finding node and return its record as JSON."""
    try:
        from modules.lazy_engine import (
            ActivityLog,
            ExplorationGraph,
            FindingService,
            LazyEngine,
        )

        task_id = str(arguments.get("task_id", "")).strip()
        if not task_id:
            return ctx.text(
                tool_name,
                json.dumps({"error": "task_id is required; findings live in the loop engine"}, indent=2),
            )
        evidence = str(arguments.get("evidence", ""))
        intent_id = int(arguments.get("intent_id", 0) or arguments.get("node_id", 0) or 0)
        graph = ExplorationGraph(task_id)
        service = FindingService(task_id, graph, ActivityLog(task_id), LazyEngine().store)
        finding = service.report(
            str(arguments.get("name", "") or "agent finding")[:_MAX_NAME],
            summary=evidence[:_MAX_SUMMARY],
            poc=evidence[:_MAX_POC],
            severity=str(arguments.get("severity", "")),
            intent_id=intent_id,
            traffic_refs=[str(ref) for ref in (arguments.get("traffic_refs", []) or [])],
        )
        record = {
            "node_id": finding.node_id,
            "text": finding.text,
            "severity": finding.meta.get("severity"),
            "status": finding.meta.get("status"),
            "evidence_version": finding.meta.get("evidence_version"),
            "intent_id": intent_id,
        }
        return ctx.text(tool_name, json.dumps(record, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
