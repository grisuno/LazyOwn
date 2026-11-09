"""MCP tool ``lazyown_report_update`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_report_update",
    description=(
        "Read or update the PDF/HTML pentest report data in static/body_report.json. "
        "Fields: assessment_information, engagement_overview, service_description, "
        "campaign_objectives, process_and_methodology, scoping_and_rules, "
        "executive_summary_findings, executive_summary_narrative, "
        "summary_vulnerability_overview, security_labs_toolkit, appendix_a_changes. "
        "action='read' — returns all current field values. "
        "action='write' — updates a single field by key+value. "
        "action='auto_fill' — uses session facts/timeline to auto-generate executive_summary_findings "
        "and summary_vulnerability_overview from the current session data."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["read", "write", "auto_fill"],
                "default": "read",
            },
            "key": {
                "type": "string",
                "description": "Report field key to update (required for action=write).",
            },
            "value": {
                "type": "string",
                "description": "New content for the field (required for action=write).",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_report_update MCP tool."""
    report_file = ctx.lazyown_dir / "static" / "body_report.json"
    action = arguments.get("action", "read")
    REPORT_FIELDS = [
        "assessment_information",
        "engagement_overview",
        "service_description",
        "campaign_objectives",
        "process_and_methodology",
        "scoping_and_rules",
        "executive_summary_findings",
        "executive_summary_narrative",
        "summary_vulnerability_overview",
        "security_labs_toolkit",
        "appendix_a_changes",
    ]
    try:
        body = json.loads(report_file.read_text()) if report_file.exists() else {}
    except Exception:
        body = {}

    if action == "read":
        lines = ["Report fields in static/body_report.json:", ""]
        for k in REPORT_FIELDS:
            v = str(body.get(k, "(empty)"))[:200]
            lines.append(f"[{k}]\n  {v}\n")
        return ctx.text(tool_name, "\n".join(lines))

    elif action == "write":
        key = arguments.get("key", "")
        value = arguments.get("value", "")
        if not key:
            return ctx.text(tool_name, "key parameter required for action=write")
        body[key] = value
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(json.dumps(body, indent=4, ensure_ascii=False))
        return ctx.text(tool_name, f"Report field '{key}' updated ({len(value)} chars).")

    elif action == "auto_fill":
        # Auto-generate executive summary from session facts and world model
        summary_parts = []
        wm_file = ctx.sessions_dir / "world_model.json"
        if wm_file.exists():
            try:
                wm = json.loads(wm_file.read_text())
                hosts = wm.get("hosts", {})
                owned = [ip for ip, h in hosts.items() if h.get("state") in ("exploited", "owned")]
                scanned = [ip for ip, h in hosts.items() if h.get("state") == "scanned"]
                creds = wm.get("credentials", [])
                summary_parts.append(
                    f"Hosts discovered: {len(hosts)} | Compromised: {len(owned)} | Scanned only: {len(scanned)}"
                )
                if owned:
                    summary_parts.append(f"Compromised hosts: {', '.join(owned)}")
                if creds:
                    summary_parts.append(f"Credentials captured: {len(creds)}")
            except Exception:
                pass
        obj_file = ctx.sessions_dir / "objectives.jsonl"
        if obj_file.exists():
            try:
                objs = [json.loads(line) for line in obj_file.read_text().splitlines() if line.strip()]
                done = [o for o in objs if o.get("status") == "done"]
                summary_parts.append(f"Objectives completed: {len(done)}/{len(objs)}")
            except Exception:
                pass
        lessons_file = ctx.sessions_dir / "campaign_lessons.jsonl"
        if lessons_file.exists():
            try:
                lessons = [json.loads(line) for line in lessons_file.read_text().splitlines() if line.strip()]
                for les in lessons[-5:]:
                    summary_parts.append(f"- [{les.get('topic', '?')}] {les.get('lesson', '')[:100]}")
            except Exception:
                pass
        auto_text = "\n".join(summary_parts) or "(insufficient session data)"
        body["executive_summary_findings"] = auto_text
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(json.dumps(body, indent=4, ensure_ascii=False))
        return ctx.text(tool_name, f"executive_summary_findings auto-filled:\n{auto_text}")

    return ctx.text(tool_name, f"Unknown action: {action}")
