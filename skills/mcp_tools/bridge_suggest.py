"""MCP tool ``lazyown_bridge_suggest`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_bridge_suggest",
    description=(
        "Query the full LazyOwn command catalog (347 commands, 11 phases) "
        "for the best command to run given engagement phase, services, "
        "credential state, and OS target. "
        "Args are auto-filled from the WorldModel (target IP, open port, creds). "
        "Catalog phases: recon (35), enum (71), exploit (61), postexp (40), "
        "cred (32), lateral (28), privesc (2), persist (30), exfil (19), "
        "c2 (14), report (15). "
        "Also accepts WorldModel phases: scanning, enumeration, exploitation, "
        "post_exploitation, lateral_movement, exfiltration. "
        "Use list_all=true to see every command for a phase. "
        "Use sequence=true to get the next 5 commands in priority order. "
        "Use tag_hint for technique-specific filtering: 'kerberos', 'smb', "
        "'web', 'ad', 'impacket', 'ldap', 'bruteforce', 'tunnel', 'av_bypass'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "phase": {
                "type": "string",
                "description": (
                    "Engagement phase: recon, scanning, enum, enumeration, "
                    "exploit, exploitation, postexp, post_exploitation, "
                    "cred, credential_access, lateral, lateral_movement, "
                    "privesc, privilege_escalation, persist, persistence, "
                    "exfil, exfiltration, c2, command_and_control, report, reporting."
                ),
                "default": "recon",
            },
            "target": {
                "type": "string",
                "description": "Target IP or hostname (used for arg substitution).",
                "default": "",
            },
            "services": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Discovered services (e.g. ['http:80','ssh:22','smb:445',"
                    "'ldap:389','kerberos:88','winrm:5985']). "
                    "Filters catalog to commands relevant to those services."
                ),
                "default": [],
            },
            "excluded": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Command names to skip.",
                "default": [],
            },
            "mitre_hint": {
                "type": "string",
                "description": "Prefer commands matching this MITRE technique (e.g. 'T1046', 'T1110').",
                "default": "",
            },
            "tag_hint": {
                "type": "string",
                "description": (
                    "Filter by technique tag: 'kerberos', 'ad', 'smb', 'web', "
                    "'ldap', 'impacket', 'bruteforce', 'spray', 'tunnel', "
                    "'webshell', 'av_bypass', 'osint', 'dns', 'snmp', 'ssh'."
                ),
                "default": "",
            },
            "os_hint": {
                "type": "string",
                "description": "Target OS: 'linux', 'windows', or 'any' (default).",
                "enum": ["any", "linux", "windows"],
                "default": "any",
            },
            "list_all": {
                "type": "boolean",
                "description": "List ALL commands for the phase (sorted by priority).",
                "default": False,
            },
            "sequence": {
                "type": "boolean",
                "description": "Return next 5 commands in kill-chain order.",
                "default": False,
            },
            "catalog_summary": {
                "type": "boolean",
                "description": "Show full catalog summary (all phases + command counts).",
                "default": False,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_bridge_suggest MCP tool."""
    bs_phase = arguments.get("phase", "recon").strip() or "recon"
    bs_target = arguments.get("target", "").strip()
    bs_services = arguments.get("services", [])
    bs_excluded = set(arguments.get("excluded", []))
    bs_mitre = arguments.get("mitre_hint", "").strip()
    bs_tag = arguments.get("tag_hint", "").strip()
    bs_os = arguments.get("os_hint", "any").strip() or "any"
    bs_list_all = bool(arguments.get("list_all", False))
    bs_sequence = bool(arguments.get("sequence", False))
    bs_cat_summary = bool(arguments.get("catalog_summary", False))
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from lazyown_bridge import get_dispatcher as _bridge_dispatcher

        dispatcher = _bridge_dispatcher()

        # ── catalog_summary mode ──────────────────────────────────────
        if bs_cat_summary:
            summary = dispatcher.catalog_summary()
            lines = [
                f"LazyOwn Bridge Catalog — {dispatcher.catalog_count()} commands",
                f"Kill chain order: {' -> '.join(dispatcher.phase_kill_chain())}",
                "",
            ]
            for phase, cmds in summary.items():
                lines.append(
                    f"  {phase:12s} ({len(cmds):3d}): {', '.join(cmds[:8])}" + (" ..." if len(cmds) > 8 else "")
                )
            return ctx.text(tool_name, "\n".join(lines))

        # ── list_all mode ─────────────────────────────────────────────
        if bs_list_all:
            entries = dispatcher.list_phase(bs_phase)
            if not entries:
                return ctx.text(tool_name, f"[bridge_suggest] No commands catalogued for phase '{bs_phase}'.")
            lines = [
                f"Commands for phase '{bs_phase}' ({len(entries)} total):",
                f"  Catalog total: {dispatcher.catalog_count()} commands",
                "",
            ]
            for e in entries:
                cred_tag = " [creds]" if e.requires_creds else ""
                svc_tag = f" [{','.join(e.services[:3])}]" if e.services else ""
                os_tag = f" [{e.os_target}]" if e.os_target != "any" else ""
                tag_str = f" #{','.join(e.tags[:2])}" if e.tags else ""
                lines.append(f"  {e.priority}. {e.command:30s}{cred_tag}{svc_tag}{os_tag}{tag_str}  {e.mitre_tactic}")
                lines.append(f"       {e.description}")
            return ctx.text(tool_name, "\n".join(lines))

        # ── Load WorldModel snapshot for arg enrichment ───────────────
        _wm_snapshot = None
        try:
            from world_model import WorldModel

            _wm_snapshot = WorldModel().snapshot()
            if not bs_target and _wm_snapshot:
                _hosts = list(_wm_snapshot.get("hosts", {}).keys())
                if _hosts:
                    bs_target = _wm_snapshot.get("primary_target") or _hosts[0]
        except Exception:
            pass

        _has_creds = bool(_wm_snapshot.get("credentials")) if _wm_snapshot else False
        _eff_target = bs_target or ctx.load_payload().get("rhost", "")

        # ── sequence mode ─────────────────────────────────────────────
        if bs_sequence:
            seq = dispatcher.suggest_sequence(
                phase=bs_phase,
                target=_eff_target,
                services=bs_services,
                has_creds=_has_creds,
                excluded=bs_excluded,
                world_snapshot=_wm_snapshot,
                limit=5,
            )
            if not seq:
                return ctx.text(tool_name, f"[bridge_suggest] No sequence found for phase='{bs_phase}'.")
            lines = [f"Next {len(seq)} commands for phase '{bs_phase}':", ""]
            for i, (cmd_s, ent) in enumerate(seq, 1):
                lines.append(f"  {i}. {cmd_s}")
                lines.append(f"       [{ent.mitre_tactic}] {ent.description}")
            return ctx.text(tool_name, "\n".join(lines))

        # ── single suggest mode ───────────────────────────────────────
        result = dispatcher.suggest(
            phase=bs_phase,
            target=_eff_target,
            services=bs_services,
            has_creds=_has_creds,
            excluded=bs_excluded,
            world_snapshot=_wm_snapshot,
            mitre_hint=bs_mitre,
            tag_hint=bs_tag,
            os_hint=bs_os,
        )
        if result is None:
            return ctx.text(
                tool_name,
                f"[bridge_suggest] No suitable command for phase='{bs_phase}' "
                f"services={bs_services} tag='{bs_tag}' os='{bs_os}'. "
                f"Try list_all=true or catalog_summary=true.",
            )
        cmd_str, entry = result
        tag_str = f" #{', #'.join(entry.tags)}" if entry.tags else ""
        os_str = f" [{entry.os_target}]" if entry.os_target != "any" else ""
        lines = [
            f"Suggested: {cmd_str}",
            f"  Phase:       {entry.phase}",
            f"  MITRE:       {entry.mitre_tactic}",
            f"  Description: {entry.description}",
            f"  Priority:    {entry.priority}{os_str}{tag_str}",
        ]
        if entry.services:
            lines.append(f"  Services:    {', '.join(entry.services)}")
        if entry.requires_creds:
            lines.append("  Note: requires credentials in WorldModel")
        lines.append("")
        lines.append(f"Run: lazyown_run_command  command='{cmd_str}'")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[bridge_suggest error] {exc}")
