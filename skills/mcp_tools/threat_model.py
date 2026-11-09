"""MCP tool ``lazyown_threat_model`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_threat_model",
    description=(
        "Build or load the blue team threat model from LazyOwn session data. "
        "Reads LazyOwn_session_report.csv, maps commands to MITRE ATT&CK techniques, "
        "and produces assets with risk scores, TTP catalogue, IOC registry, "
        "and Sigma-lite detection rules. "
        "Output saved to sessions/reports/threat_model.json. "
        "action='build' (re)generates the model. "
        "action='load' returns the last saved model. "
        "action='ttps' returns only the TTP list. "
        "action='rules' returns only detection rules. "
        "action='iocs' returns only the IOC registry. "
        "action='purple' returns the full purple team mapping (red TTP + blue detection side-by-side). "
        "action='gaps' returns TTPs with no detection rule (coverage gaps)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["build", "load", "ttps", "rules", "iocs", "purple", "gaps"],
                "description": "What to return.",
                "default": "build",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_threat_model MCP tool."""
    tm_action = arguments.get("action", "build")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from threat_model import get_builder as _get_tm_builder

        _tmb = _get_tm_builder()
        if tm_action == "load":
            model = _tmb.load()
            if model is None:
                return ctx.text(tool_name, "No threat model found — run with action='build' first.")
        else:
            model = await asyncio.get_event_loop().run_in_executor(None, _tmb.build)

        if tm_action in ("build", "load"):
            s = model.get("summary", {})
            lines = [
                f"Threat Model  generated_at={model.get('generated_at', '')}",
                f"  Assets:          {len(model.get('assets', []))}  (highest risk: {s.get('highest_risk_asset', '')})",
                f"  TTPs:            {len(model.get('ttps', []))}  (dominant tactic: {s.get('dominant_tactic', '')})",
                f"  IOCs:            {len(model.get('ioc_registry', []))}",
                f"  Detection rules: {len(model.get('detection_rules', []))}",
                f"  Total events:    {s.get('total_events', 0)}",
                "",
                "Top 5 TTPs:",
            ]
            for t in model.get("ttps", [])[:5]:
                lines.append(
                    f"  {t['technique_id']:12s} [{t['severity']:8s}] {t['tactic']:28s} "
                    f"{t['technique_name']}  (x{t['occurrences']})"
                )
            lines.append("")
            lines.append("Full model: sessions/reports/threat_model.json")
            return ctx.text(tool_name, "\n".join(lines))
        elif tm_action == "ttps":
            ttps = model.get("ttps", [])
            lines = [f"TTPs ({len(ttps)}):"]
            for t in ttps:
                lines.append(
                    f"  {t['technique_id']:12s} [{t['severity']:8s}]  {t['technique_name']}  (x{t['occurrences']})"
                )
            return ctx.text(tool_name, "\n".join(lines))
        elif tm_action == "rules":
            rules = model.get("detection_rules", [])
            lines = [f"Detection Rules ({len(rules)}):"]
            for r in rules:
                lines.append(f"  {r['rule_id']}  [{r['severity']:8s}]  {r['name']}")
                lines.append(f"    log_source: {r['log_source']}  |  condition: {r['condition']}")
                lines.append(f"    response: {r['response']}")
            return ctx.text(tool_name, "\n".join(lines))
        elif tm_action == "iocs":
            iocs = model.get("ioc_registry", [])
            lines = [f"IOC Registry ({len(iocs)}):"]
            for ioc in iocs[:50]:
                lines.append(f"  {ioc['type']:12s}  {ioc['value']}")
            if len(iocs) > 50:
                lines.append(f"  ... and {len(iocs) - 50} more")
            return ctx.text(tool_name, "\n".join(lines))
        elif tm_action == "purple":
            purple = model.get("purple_team", [])
            lines = [f"Purple Team Mapping ({len(purple)} TTPs)\n"]
            for p in purple:
                gap_str = "  [COVERAGE GAP]" if p["gap"] else ""
                lines.append(f"{p['technique_id']:12s} [{p['severity']:8s}]  {p['technique_name']}{gap_str}")
                r = p["red"]
                lines.append(
                    f"  RED : {', '.join(r['commands'])}  "
                    f"(x{r['occurrences']}  {r['first_seen'][:10]} – {r['last_seen'][:10]})"
                )
                b = p["blue"]
                if b:
                    lines.append(f"  BLUE: {b['rule_id']} {b['name']}")
                    lines.append(f"        {b['response']}")
                else:
                    lines.append("  BLUE: no detection rule")
                lines.append("")
            return ctx.text(tool_name, "\n".join(lines))
        elif tm_action == "gaps":
            purple = model.get("purple_team", [])
            gaps = [p for p in purple if p["gap"]]
            covered = len(purple) - len(gaps)
            pct = round(covered / len(purple) * 100) if purple else 0
            lines = [
                f"Detection Coverage: {covered}/{len(purple)} TTPs covered ({pct}%)",
                f"Coverage gaps: {len(gaps)}\n",
            ]
            for p in gaps:
                lines.append(f"  {p['technique_id']:12s} [{p['severity']:8s}]  {p['technique_name']}")
                lines.append(f"    Commands: {', '.join(p['red']['commands'])}")
            if not gaps:
                lines.append("  All detected TTPs have a detection rule.")
            return ctx.text(tool_name, "\n".join(lines))
        return ctx.text(tool_name, json.dumps(model, indent=2, default=str))
    except Exception as exc:
        return ctx.text(tool_name, f"[threat_model error] {exc}")
