"""MCP tool ``lazyown_phase_guide`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_phase_guide",
    description=(
        "COMPLETE OPERATOR GUIDE for a specific pentest phase. "
        "Returns everything needed to operate autonomously in that phase: "
        "(1) ALL commands available from the bridge catalog for this phase — "
        "    name, description, MITRE tactic, OS target, required services, needs-creds flag; "
        "(2) Payload.json keys that must be set for each command (rhost/domain/wordlist/creds); "
        "(3) Key aliases for the phase (e.g. 'ww' = whatweb, 'nmap' = lazynmap); "
        "(4) Phase-specific kill-chain order (which commands to run first vs last); "
        "(5) Current payload.json state — which keys are set vs empty; "
        "(6) Abstraction reminder: commands auto-inject all params from payload.json — "
        "    NEVER write raw tool flags, just the command name. "
        "Use this at the START of each phase and whenever the autonomous loop needs context."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "phase": {
                "type": "string",
                "description": "Pentest phase to get guide for.",
                "enum": [
                    "recon",
                    "enum",
                    "exploit",
                    "postexp",
                    "persist",
                    "privesc",
                    "cred",
                    "lateral",
                    "exfil",
                    "c2",
                    "report",
                ],
            },
            "os_hint": {
                "type": "string",
                "description": "Filter commands by OS: 'linux', 'windows', or 'any' (default).",
                "default": "any",
            },
            "services": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Discovered services to filter commands (e.g. ['http', 'smb', 'ldap']).",
                "default": [],
            },
        },
        "required": ["phase"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_phase_guide MCP tool."""
    pg_phase = arguments.get("phase", "recon").strip().lower()
    pg_os = arguments.get("os_hint", "any").strip().lower()
    pg_services = arguments.get("services", [])

    # Key aliases per phase (subset of the full aliases dict — most useful ones)
    _PHASE_ALIASES: dict = {
        "recon": {
            "nmap": "lazynmap (full TCP scan)",
            "hosts_discover": "hostdiscover.sh sweep",
            "arpscan": "arp-scan -l",
            "ping": "TTL-based OS detection",
        },
        "enum": {
            "ww": "whatweb domain fingerprint",
            "gobuster": "dir brute-force",
            "ffuf": "fast web fuzzer",
            "ss": "multi-source exploit search",
            "dig": "DNS zone transfer/records",
            "enum4linux": "SMB/LDAP enum",
            "nxcridbrute": "RID cycling via nxc",
            "ntlmrelayx": "NTLM relay",
        },
        "exploit": {
            "sqlmap": "SQL injection",
            "ss": "searchsploit+NVD+8 sources",
            "msf": "metasploit listener",
            "venom": "msfvenom payload",
        },
        "postexp": {
            "creds": "cat all sessions/credentials*",
            "hash": "cat all sessions/hash*",
            "loot": "copy msf loot to sessions/",
            "ssh_cmd": "SSH command exec",
        },
        "privesc": {
            "linpeas": "linpeas.sh enum",
            "winpeas": "winpeas.exe enum",
            "getcap": "find capabilities",
            "lazypwn": "LazyPwn script",
        },
        "cred": {
            "secretsdump": "impacket secretsdump",
            "hashcat": "GPU cracking",
            "john2hash": "john + hash format",
            "unshadow": "combine passwd+shadow",
        },
        "lateral": {
            "evil": "evil-winrm -i rhost -u user -p pass",
            "cme": "crackmapexec smb/winrm",
            "psexec": "impacket psexec",
            "bloodhound": "bloodhound-python collector",
        },
        "exfil": {
            "loot": "copy loot to sessions/",
            "scp": "scp from remote host",
            "ftpd": "python ftpd server on 2121",
        },
        "c2": {
            "cc": "open C2 dashboard",
            "msf": "metasploit handler",
            "venom": "generate payload",
            "download_c2": "pull implant",
        },
        "report": {
            "report": "generate AI report via report.py",
            "lazyreport": "POST to C2 /lazyreport",
            "man": "README.md in gum",
        },
    }
    # Payload keys needed per command category
    _PAYLOAD_KEYS = {
        "recon": ["rhost", "lhost", "device"],
        "enum": ["rhost", "domain", "wordlist", "dirwordlist", "dnswordlist"],
        "exploit": ["rhost", "lhost", "lport", "start_user", "start_pass"],
        "postexp": ["rhost", "lhost", "start_user", "start_pass"],
        "privesc": ["rhost", "lhost", "start_user", "start_pass"],
        "cred": ["rhost", "start_user", "start_pass", "wordlist"],
        "lateral": ["rhost", "domain", "start_user", "start_pass", "lhost"],
        "exfil": ["rhost", "lhost", "lport", "start_user", "start_pass"],
        "c2": ["lhost", "c2_port", "c2_user", "c2_pass"],
        "report": ["api_key", "rhost", "domain"],
    }

    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from lazyown_bridge import get_dispatcher as _bd_pg

        _disp_pg = _bd_pg()
        all_entries = _disp_pg.list_phase(pg_phase)
    except Exception as e:
        return ctx.text(tool_name, f"Bridge catalog unavailable: {e}")

    # Filter by OS and services if requested
    if pg_os != "any":
        all_entries = [e for e in all_entries if e.os_target in (pg_os, "any")]
    if pg_services:
        svc_set = set(s.lower() for s in pg_services)
        filtered = [e for e in all_entries if not e.services or any(s.lower() in svc_set for s in e.services)]
        if filtered:
            all_entries = filtered  # only filter if results remain

    # Current payload state
    try:
        payload_now = json.loads((ctx.lazyown_dir / "payload.json").read_text())
    except Exception:
        payload_now = {}

    needed_keys = _PAYLOAD_KEYS.get(pg_phase, [])
    key_status = []
    for k in needed_keys:
        v = payload_now.get(k, "")
        status = f"✓ {k}={str(v)[:30]}" if v else f"✗ {k}=(not set)"
        key_status.append(status)

    out = (
        [
            f"{'=' * 60}",
            f"PHASE GUIDE: {pg_phase.upper()}  (OS: {pg_os}  Services: {pg_services or 'any'})",
            f"{'=' * 60}",
            "",
            "▶ ABSTRACTION MODEL",
            "  LazyOwn commands are HIGH-LEVEL ABSTRACTIONS over real tools.",
            "  payload.json auto-injects ALL parameters — NEVER write raw flags.",
            "  Examples:",
            "    lazynmap          → nmap -sC -sV -p- -T4 -Pn --script vuln {rhost}",
            "    gobuster          → gobuster dir -u http://{rhost} -w {dirwordlist} ...",
            "    bloodhound        → bloodhound-python -d {domain} -u {user} -p {pass} -c All",
            "    evil              → evil-winrm -i {rhost} -u {user} -p {pass}",
            "    ww                → whatweb http://{domain} -a 3",
            "    dig               → dig @{rhost} {domain} axfr",
            "",
            "▶ PAYLOAD.JSON KEYS FOR THIS PHASE",
        ]
        + [f"  {s}" for s in key_status]
        + [
            "",
            f"▶ KEY ALIASES FOR PHASE '{pg_phase}'",
        ]
        + [f"  {k:<20} → {v}" for k, v in _PHASE_ALIASES.get(pg_phase, {}).items()]
        + [
            "",
            f"▶ AVAILABLE COMMANDS ({len(all_entries)} from bridge catalog)",
            f"  {'Command':<24} {'MITRE':<10} {'OS':<8} {'Creds?':<7} {'Services':<18} Description",
            f"  {'-' * 24} {'-' * 10} {'-' * 8} {'-' * 7} {'-' * 18} {'-' * 40}",
        ]
    )
    for e in all_entries:
        svc = ",".join((e.services or [])[:3]) or "any"
        os_t = e.os_target or "any"
        mit = e.mitre_tactic or ""
        cred = "yes" if e.requires_creds else "no"
        desc = (e.description or "")[:50]
        out.append(f"  {e.command:<24} [{mit:<8}] {os_t:<8} {cred:<7} {svc:<18} {desc}")

    # Kill-chain tip
    try:
        kc = _disp_pg.phase_kill_chain()
        idx = kc.index(pg_phase) if pg_phase in kc else -1
        next_phase = kc[idx + 1] if idx >= 0 and idx + 1 < len(kc) else "(end)"
        out += [
            "",
            "▶ KILL-CHAIN POSITION",
            f"  Current: {pg_phase}  →  Next: {next_phase}",
            f"  Full chain: {' → '.join(kc)}",
        ]
    except Exception:
        pass

    out += [
        "",
        "▶ QUICK START FOR THIS PHASE",
        "  1. Verify payload keys above are set (lazyown_get_config / lazyown_set_config)",
        "  2. Run first command: lazyown_run_command('<command_name>')",
        "  3. Parse output: lazyown_reactive_suggest(output=..., command=...)",
        "  4. Loop: lazyown_auto_loop(target=rhost, max_steps=10)",
        f"{'=' * 60}",
    ]
    return ctx.text(tool_name, "\n".join(out))
