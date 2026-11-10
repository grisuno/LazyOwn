"""MCP tool ``lazyown_session_init`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from lazyown_mcp_helpers import DEFAULT_FRESHNESS_THRESHOLD_SECONDS
from lazyown_mcp_helpers import evidence_freshness
from lazyown_mcp_helpers import take_snapshot
import sys
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_session_init",
    description=(
        "SITREP — Call this FIRST in every new session. "
        "Returns a full situation report: "
        "(1) active config: rhost, domain, lhost, lport, os_id. "
        "(2) OS cross-reference: compares payload.json os_id vs OS detected in nmap scan — "
        "flags conflicts so you know whether to trust the config or update it. "
        "(3) Nmap evidence: checks if sessions/scan_{rhost}.nmap and "
        "sessions/vulns_{rhost}.nmap already exist — lists open ports from them. "
        "(4) Pwntomate evidence: checks sessions/{rhost}/{port}/{tool}/ dirs. "
        "If scans already exist DO NOT re-run them — read the files instead. "
        "(5) Tasks from sessions/tasks.json — pending vs done. "
        "(6) Active objectives from sessions/objectives.jsonl. "
        "(7) World model state for rhost: services, credentials, vulnerabilities. "
        "(8) Engagement phase + top commands for current phase. "
        "(9) Gap analysis: what's missing and recommended next steps. "
        "Pass format='json' to get structured output (preferred for agents). "
        "Pass include_recommend=true to embed top-3 ranked next-step suggestions."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "Output format: 'pretty' (human banner, default) or 'json' (structured dict).",
                "enum": ["pretty", "json"],
                "default": "pretty",
            },
            "include_recommend": {
                "type": "boolean",
                "description": "Embed top-3 ranked next-step suggestions from the recommender.",
                "default": False,
            },
            "freshness_threshold_seconds": {
                "type": "integer",
                "description": "Mark scan/pwntomate evidence as stale beyond this age (default 7d).",
                "default": DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_session_init MCP tool."""
    import json as _json
    from pathlib import Path as _Path

    out_format = (arguments.get("format") or "pretty").lower()
    include_recommend = bool(arguments.get("include_recommend", False))
    freshness_threshold = int(
        arguments.get(
            "freshness_threshold_seconds",
            DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
        )
    )

    # ── 1. Payload config ────────────────────────────────────────────────
    cfg = ctx.load_payload()
    rhost = cfg.get("rhost", "")
    domain = cfg.get("domain", "")
    lhost = cfg.get("lhost", "")
    lport = str(cfg.get("lport", ""))
    os_id_cfg = cfg.get("os_id", "unknown")  # what payload.json says

    # ── 2. World model ───────────────────────────────────────────────────
    wm_path = ctx.lazyown_dir / "sessions" / "world_model.json"
    phase = "recon"
    wm_host_state = "unscanned"
    wm_services: list[str] = []
    wm_creds: list[str] = []
    wm_vulns: list[str] = []
    try:
        if wm_path.exists():
            wm = _json.loads(wm_path.read_text())
            from modules.killchain import KillChain

            phase = KillChain.current_phase(world_model_path=wm_path)
            h = wm.get("hosts", {}).get(rhost, {})
            wm_host_state = h.get("state", "unscanned")
            for svc in h.get("services", {}).values():
                wm_services.append(
                    f"    {svc.get('port', '?')}/{svc.get('protocol', 'tcp')} "
                    f"{svc.get('name', '?')} {svc.get('version', '')}"
                )
            for c in wm.get("credentials", [])[:5]:
                wm_creds.append(f"    {c.get('username', '?')}:{c.get('secret', '?')[:20]} ({c.get('type', '?')})")
            for v in wm.get("vulnerabilities", [])[:5]:
                wm_vulns.append(f"    {v.get('cve', '?')} {v.get('severity', '?')} — {v.get('description', '')[:60]}")
    except Exception:
        pass

    # ── 3. Nmap scan evidence ────────────────────────────────────────────
    # lazynmap.sh creates: sessions/scan_{TARGET}.nmap + sessions/vulns_{TARGET}.nmap
    scan_files: list[str] = []
    open_ports: list[str] = []
    os_from_nmap = ""
    nmap_done = False
    vulns_done = False

    if rhost:
        nmap_scan = ctx.lazyown_dir / "sessions" / f"scan_{rhost}.nmap"
        nmap_xml = ctx.lazyown_dir / "sessions" / f"scan_{rhost}.nmap.xml"
        nmap_vulns = ctx.lazyown_dir / "sessions" / f"vulns_{rhost}.nmap"

        nmap_done = nmap_scan.exists() and nmap_scan.stat().st_size > 100
        vulns_done = nmap_vulns.exists() and nmap_vulns.stat().st_size > 100

        if nmap_done:
            scan_files.append(f"  [OK] scan_{rhost}.nmap   ({nmap_scan.stat().st_size:,} bytes)")
            # Parse open ports + OS hint
            try:
                for line in nmap_scan.read_text(errors="replace").splitlines():
                    stripped = line.strip()
                    if "/tcp" in stripped and "open" in stripped:
                        open_ports.append(f"      {stripped}")
                    if not os_from_nmap:
                        low = stripped.lower()
                        if "os details:" in low or "running:" in low or "aggressive os guesses:" in low:
                            os_from_nmap = stripped
                        # Banner-based fallback
                        elif (
                            "microsoft" in low
                            or "windows" in low
                            and any(x in low for x in ("smb", "iis", "rdp", "winrm"))
                        ):
                            os_from_nmap = f"Windows (service banner: {stripped[:80]})"
            except Exception:
                pass

        if vulns_done:
            scan_files.append(f"  [OK] vulns_{rhost}.nmap  ({nmap_vulns.stat().st_size:,} bytes)")
        if nmap_xml.exists() and nmap_xml.stat().st_size > 100:
            scan_files.append(f"  [OK] scan_{rhost}.nmap.xml ({nmap_xml.stat().st_size:,} bytes)")

    # ── 4. OS cross-reference ────────────────────────────────────────────
    os_verdict = os_id_cfg
    os_conflict = ""
    os_evidence = ""
    if os_from_nmap:
        low = os_from_nmap.lower()
        nmap_says_win = "windows" in low or "microsoft" in low
        nmap_says_lnx = "linux" in low or "unix" in low
        if nmap_says_win and os_id_cfg in ("linux", "unknown", ""):
            os_conflict = (
                f"  [CONFLICT] payload.json os_id='{os_id_cfg}' "
                f"but nmap suggests Windows → update: "
                f"lazyown_set_config(key='os_id', value='windows')"
            )
            os_verdict = "windows"
        elif nmap_says_lnx and os_id_cfg in ("windows", "unknown", ""):
            os_conflict = (
                f"  [CONFLICT] payload.json os_id='{os_id_cfg}' "
                f"but nmap suggests Linux → update: "
                f"lazyown_set_config(key='os_id', value='linux')"
            )
            os_verdict = "linux"
        os_evidence = f"  os_nmap : {os_from_nmap[:120]}"

    # ── 5. Pwntomate output evidence ─────────────────────────────────────
    # pwntomate writes to {basedir}/{ip}/{port}/{toolname}/
    # LazyOwn uses sessions/{ip}/ and ~/.pwntomate/{ip}/
    pwntomate_lines: list[str] = []
    if rhost:
        for base in [
            ctx.lazyown_dir / "sessions" / rhost,
            _Path.home() / ".pwntomate" / rhost,
        ]:
            if base.exists() and base.is_dir():
                for port_dir in sorted(base.iterdir()):
                    if port_dir.is_dir():
                        for tool_dir in sorted(port_dir.iterdir()):
                            if tool_dir.is_dir():
                                fcount = len(list(tool_dir.rglob("*")))
                                if fcount:
                                    pwntomate_lines.append(
                                        f"  [OK] {rhost}/{port_dir.name}/{tool_dir.name}/ ({fcount} files)"
                                    )

    # ── 6. Tasks ─────────────────────────────────────────────────────────
    tasks_path = ctx.lazyown_dir / "sessions" / "tasks.json"
    tasks_pending: list[str] = []
    tasks_done: list[str] = []
    try:
        if tasks_path.exists():
            for t in _json.loads(tasks_path.read_text()):
                s = t.get("status", "New")
                title = t.get("title", "")[:80]
                tid = t.get("id", "?")
                if s in ("Done", "Qa"):
                    tasks_done.append(f"  [#{tid} {s}] {title}")
                else:
                    tasks_pending.append(f"  [#{tid} {s:8s}] {title}")
    except Exception:
        pass

    # ── 7. Active objectives ─────────────────────────────────────────────
    obj_path = ctx.lazyown_dir / "sessions" / "objectives.jsonl"
    objectives: list[str] = []
    try:
        if obj_path.exists():
            for line in obj_path.read_text().splitlines()[-10:]:
                try:
                    o = _json.loads(line)
                    if o.get("status") == "pending":
                        objectives.append(f"  [{o.get('priority', 'normal'):8s}] {o.get('text', '')[:80]}")
                except Exception:
                    pass
    except Exception:
        pass

    # ── 8. Phase commands from bridge catalog ────────────────────────────
    phase_commands: list[str] = []
    kill_chain: list[str] = [
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
    ]
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from lazyown_bridge import get_dispatcher as _bd_si

        _disp_si = _bd_si()
        kill_chain = _disp_si.phase_kill_chain()
        for e in _disp_si.list_phase(phase)[:10]:
            svc = ",".join(e.services[:3]) if getattr(e, "services", None) else "any"
            desc = getattr(e, "description", "") or ""
            mit = getattr(e, "mitre_tactic", "") or ""
            phase_commands.append(f"  {e.command:<22} [{mit:<7}] {svc:<14} {desc[:50]}")
    except Exception as _ex_bridge:
        phase_commands = [f"  (bridge unavailable: {_ex_bridge})"]

    # ── 9. What's missing / next steps ──────────────────────────────────
    missing: list[str] = []
    next_steps: list[str] = []

    if not rhost:
        missing.append("  [!] rhost not set in payload.json")
        next_steps.append("  A. lazyown_set_config(key='rhost', value='<target_ip>')")
    else:
        if not nmap_done:
            missing.append(f"  [!] sessions/scan_{rhost}.nmap not found — lazynmap not run yet")
            next_steps.append(f"  A. lazyown_run_command('nmap')   → builds sessions/scan_{rhost}.nmap")
        else:
            if not vulns_done:
                missing.append(f"  [-] sessions/vulns_{rhost}.nmap not found — vuln scan pending")
            if not pwntomate_lines:
                missing.append(f"  [-] No pwntomate output for {rhost} — run after nmap finishes")
                next_steps.append("  B. lazyown_run_command('pyautomate')  → pwntomate from latest XML")
            if os_conflict:
                next_steps.append(f"  C. {os_conflict.strip()}")

        if tasks_pending:
            next_steps.append(f"  D. {len(tasks_pending)} pending task(s) in tasks.json — review and execute")
        if objectives:
            next_steps.append(f"  E. {len(objectives)} pending objective(s) — lazyown_auto_loop() to execute")

    if not missing:
        missing = ["  [OK] Scan evidence present — proceed to analysis and exploitation"]
        if not next_steps:
            next_steps = [
                f"  A. lazyown_read_session_file('scan_{rhost}.nmap')    — analyse scan",
                f"  B. lazyown_discover_commands(phase='{phase}')         — phase commands",
                "  C. lazyown_facts_show()                               — structured findings",
                f"  D. lazyown_auto_loop(objective='exploit {rhost}')     — autonomous run",
            ]

    # ── 10. Build output ─────────────────────────────────────────────────
    out = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║   LazyOwn — SITREP (Situation Report)  call once/session    ║",
        "╚══════════════════════════════════════════════════════════════╝",
        "",
        "## ACTIVE CONFIG",
        f"  rhost        : {rhost or '(not set)'}",
        f"  domain       : {domain or '(not set)'}",
        f"  lhost/lport  : {lhost or '?'}:{lport or '?'}",
        f"  os_id(cfg)   : {os_id_cfg}",
    ]
    if os_evidence:
        out.append(os_evidence)
    if os_conflict:
        out.append(os_conflict)
    out.append(f"  os_verdict   : {os_verdict}  (use this for tool selection)")

    out += [
        f"  wm_state     : {wm_host_state}",
        "",
        f"## ENGAGEMENT PHASE: {phase.upper()}",
        f"  Kill chain: {' → '.join(kill_chain)}",
        "",
        "## NMAP SCAN EVIDENCE",
    ]
    out += scan_files or [f"  [--] No nmap files found for '{rhost or 'rhost not set'}'"]

    if open_ports:
        out.append(f"\n  Open ports ({len(open_ports)}):")
        out += open_ports[:20]

    if wm_services:
        out.append(f"\n  World-model services ({len(wm_services)}):")
        out += wm_services[:15]

    out.append("\n## PWNTOMATE OUTPUT")
    out += pwntomate_lines or [f"  [--] No pwntomate output for '{rhost or 'rhost not set'}'"]

    out.append("\n## TASKS (sessions/tasks.json)")
    if tasks_pending:
        out.append("  Pending:")
        out += tasks_pending[:8]
    if tasks_done:
        out.append(f"  Done: {len(tasks_done)} task(s) completed already")
    if not tasks_pending and not tasks_done:
        out.append("  (empty)")

    if wm_creds:
        out.append("\n## CREDENTIALS (world model)")
        out += wm_creds
    if wm_vulns:
        out.append("\n## VULNERABILITIES (world model)")
        out += wm_vulns

    out.append("\n## ACTIVE OBJECTIVES (objectives.jsonl)")
    out += objectives or ["  (none pending)"]

    out += ["", "## WHAT'S MISSING / GAPS"]
    out += missing

    # Build inline phase guide for current phase
    _phase_aliases_si = {
        "recon": "nmap=lazynmap | hosts_discover=sweep | arpscan=arp-scan | ping=OS-detect(TTL)",
        "enum": "ww=whatweb | gobuster=dirbust | ffuf=fuzz | ss=exploit-search | dig=DNS | enum4linux=SMB",
        "exploit": "sqlmap=SQLi | ss=searchsploit+NVD+8src | msf=msf-handler | venom=msfvenom",
        "postexp": "creds=cat-creds | hash=cat-hashes | loot=copy-msf-loot | ssh_cmd=SSH-exec",
        "privesc": "linpeas=linux-enum | winpeas=win-enum | getcap=capabilities | lazypwn=LazyPwn",
        "cred": "secretsdump=dump-hashes | hashcat=GPU-crack | john2hash=john | unshadow=shadow-prep",
        "lateral": "evil=evil-winrm | cme=crackmapexec | psexec=impacket-psexec | bloodhound=AD-graph",
        "exfil": "loot=copy-loot | scp=SCP-transfer | ftpd=python-ftp-server",
        "c2": "cc=open-dashboard | msf=handler | venom=payload | download_c2=implant",
        "report": "report=AI-report | lazyreport=C2-report | man=README",
    }
    out += (
        [
            "",
            "## ABSTRACTION MODEL — never write raw tool commands",
            "  Every LazyOwn command is a high-level abstraction.",
            "  payload.json auto-injects ALL parameters (rhost, domain, wordlist, creds, etc.)",
            "  You only need the command name. Examples:",
            "    lazynmap      → nmap -sC -sV -p- -T4 -Pn --script vuln {rhost}",
            "    ww            → whatweb http://{domain} -a 3",
            "    gobuster      → gobuster dir -u http://{rhost} -w {dirwordlist} -t 30",
            "    evil          → evil-winrm -i {rhost} -u {user} -p {pass}",
            "    bloodhound    → bloodhound-python -d {domain} -u {user} -p {pass} -c All",
            "    dig           → dig @{rhost} {domain} axfr",
            "    secretsdump   → impacket-secretsdump {domain}/{user}:{pass}@{rhost}",
            "    ss <term>     → searchsploit+NVD+ExploitAlert+PacketStorm+MSF+Pompem+creds_py",
            "",
            f"## PHASE ALIASES — {phase.upper()}",
            f"  {_phase_aliases_si.get(phase, '(see lazyown_phase_guide)')}",
            "",
            f"## TOP COMMANDS FOR PHASE: {phase.upper()}",
            f"  {'Command':<24} {'MITRE':<10} {'Creds?':<7} {'Services':<18} Description",
            f"  {'-' * 24} {'-' * 10} {'-' * 7} {'-' * 18} {'-' * 40}",
        ]
        + phase_commands
        + [
            f"  → lazyown_phase_guide(phase='{phase}') for FULL guide with payload keys",
            f"  → lazyown_discover_commands(phase='{phase}') for plain command list",
            "",
            "## RECOMMENDED NEXT STEPS",
        ]
        + (next_steps or [f"  lazyown_phase_guide(phase='{phase}')"])
    )

    # ── Optional recommender embedding ───────────────────────────────────
    recommend_top: list[dict[str, Any]] = []
    if include_recommend:
        recommend_top = ctx.sitrep_recommendations()
        if recommend_top and not any("error" in r for r in recommend_top):
            out.append("\n## TOP-3 RECOMMENDED ACTIONS")
            for i, r in enumerate(recommend_top, 1):
                out.append(f"  {i}. {r['command']:<24} score={r['score']:.2f} — {(r['reasoning'] or '')[:80]}")

    if out_format == "json":
        sitrep_dict: dict[str, Any] = {
            "config": {
                "rhost": rhost,
                "domain": domain,
                "lhost": lhost,
                "lport": lport,
                "os_id": os_id_cfg,
                "os_verdict": os_verdict,
            },
            "engagement": {
                "phase": phase,
                "kill_chain": kill_chain,
                "host_state": wm_host_state,
            },
            "evidence": {
                "scan": evidence_freshness(
                    ctx.lazyown_dir / "sessions" / f"scan_{rhost}.nmap",
                    threshold_seconds=freshness_threshold,
                )
                if rhost
                else {},
                "vulns": evidence_freshness(
                    ctx.lazyown_dir / "sessions" / f"vulns_{rhost}.nmap",
                    threshold_seconds=freshness_threshold,
                )
                if rhost
                else {},
                "xml": evidence_freshness(
                    ctx.lazyown_dir / "sessions" / f"scan_{rhost}.nmap.xml",
                    threshold_seconds=freshness_threshold,
                )
                if rhost
                else {},
                "open_ports": [s.strip() for s in open_ports[:50]],
                "pwntomate": [s.strip() for s in pwntomate_lines],
            },
            "tasks": {
                "pending_count": len(tasks_pending),
                "done_count": len(tasks_done),
                "pending_preview": [s.strip() for s in tasks_pending[:8]],
            },
            "objectives": [s.strip() for s in objectives],
            "world_model": {
                "services": [s.strip() for s in wm_services],
                "credentials": [s.strip() for s in wm_creds],
                "vulnerabilities": [s.strip() for s in wm_vulns],
            },
            "missing": [s.strip() for s in missing],
            "next_steps": [s.strip() for s in next_steps],
            "recommend_top": recommend_top,
        }
        try:
            take_snapshot(
                ctx.sessions_dir,
                cfg,
                locals().get("wm") or {},
                _json.loads((ctx.lazyown_dir / "sessions" / "tasks.json").read_text())
                if (ctx.lazyown_dir / "sessions" / "tasks.json").exists()
                else [],
            )
        except Exception:
            pass
        return ctx.text(tool_name, _json.dumps(sitrep_dict, indent=2, default=str))

    return ctx.text(tool_name, "\n".join(out))
