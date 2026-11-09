"""MCP tool ``lazyown_lazy_intel`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_intel",
    description=(
        "Run the lazy exploitation-intelligence exposure report for one target: "
        "binds the target's discovered world-model services to the local exploit "
        "feed with hard-evidence policy (product + version inside a bounded "
        "affected range; actively exploited without a bound stays a review item), "
        "ranks matches by exploitation heat (fire/smoke/ice), scores the host "
        "0-100 with an audited breakdown, renders read-only confirmation checks "
        "and publishes one lazy_intel outcome into the world model, the SQLite "
        "store and the C2 surfaces. Securing the chain runs via lazyown_apt_chain "
        "lazy_autofire_<target> only when the operator armed 'autofire'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP. Defaults to rhost from payload.json.",
                "default": "",
            },
            "feed_path": {
                "type": "string",
                "description": "Exploit-intelligence feed JSON (lazy schema or a CISA KEV dump). Defaults to sessions/intel/exploit_feed.json.",
                "default": "",
            },
            "check": {
                "type": "boolean",
                "description": "Also render the read-only validation commands for the top matches.",
                "default": False,
            },
            "json": {
                "type": "boolean",
                "description": "Emit the full machine-readable report instead of the compact summary.",
                "default": False,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_lazy_intel MCP tool."""
    from modules.lazy_exposure import (
        generate_report as _generate_report,
    )
    from modules.lazy_exposure import (
        publish_report as _publish_report,
    )
    from modules.lazy_exposure import (
        save_report as _save_report,
    )

    li_cfg = ctx.load_payload()
    li_target = (arguments.get("target", "") or "").strip() or str(li_cfg.get("rhost", "") or "").strip()
    if not li_target:
        return ctx.text(tool_name, "[lazy_intel] target is required (or set rhost).")
    li_feed = (arguments.get("feed_path", "") or "").strip() or str(
        li_cfg.get("intel_feed", "") or "sessions/intel/exploit_feed.json"
    )
    sys.path.insert(0, str(ctx.modules_dir))
    from modules import lazy_feedmatch as _fm

    entries = _fm.load_feed(li_feed)
    report = _generate_report(li_target, entries)
    path = _save_report(report)
    _publish_report(report)
    if not entries:
        lines_head = f"[lazy_intel {li_target}] no local feed staged, live keyless feeds used"
    else:
        lines_head = f"[lazy_intel {li_target}]"
    if arguments.get("json"):
        import json as _json

        return ctx.text(tool_name, _json.dumps(report, indent=2, default=str)[-10000:])
    lines = [
        lines_head,
        f"temperature={report.get('temperature')} score={report.get('score')}",
    ]
    for detail_line in report.get("score_detail") or []:
        lines.append(f"  [{detail_line['points']:>2}p] {detail_line['label']}")
    for match in report.get("matches") or []:
        lines.append(
            f"  {match['tier'].upper():<5} {match['cve_id']:<16} {match['product']:<20} "
            f"v{match['version']:<9} port {match['port']} ({match['evidence']})"
        )
    for review in report.get("version_unknown") or []:
        lines.append(f"  review {review['cve_id']} (actively exploited, unbounded version)")
    for lead in report.get("leads") or []:
        lines.append(f"  lead {lead['product']} (unversioned product)")
    if arguments.get("check"):
        for renders in report.get("checks") or []:
            lines.append(f"  check {renders['cve_id']}: {renders['command']}")
    if path is not None:
        lines.append(f"report at {path}")
    from modules import lazy_autofire as _af

    view = _af.status(li_cfg)
    lines.append(
        f"autofire armed={view['armed']} cooldown={view['cooldown']} (assign autofire true writes lazy_autofire chains)"
    )
    return ctx.text(tool_name, "\n".join(lines))
