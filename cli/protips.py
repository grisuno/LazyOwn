"""Pro tips system for the LazyOwn shell.

Two surfaces:
  - Session-start tip: one contextual tip printed after the banner when
    the shell first starts (reads phase, os_id, rhost).
  - Post-command tip: a single dim line printed after graph hints when
    the just-executed command makes a related tool especially relevant.

Design constraints:
  - Zero imports from lazyown.py or lazyc2.py.
  - Never blocks the prompt — all rendering is non-interactive.
  - Respects enable_inline_hints=false (caller checks before calling).
  - Tips rotate; the same tip is never shown twice in a row.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.text import Text

_console = Console(highlight=False, soft_wrap=True)

# Commands after which we NEVER show a tip (noise-free zone)
_SKIP_COMMANDS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "shell",
        "dashboard",
        "sitrep",
        "ctx",
        "phase",
        "note",
        "l00t",
        "pivot",
        "tasks",
        "scans",
        "wizard",
        "palette",
        "show",
        "set",
        "assign",
        "shortcuts",
        "_relative_run",
    }
)


@dataclass(frozen=True)
class ProTip:
    """A single contextual tip with a trigger condition and display text."""

    text: str
    command: str
    trigger: Callable[[dict[str, Any]], bool]
    category: str = "general"


def _os_linux(ctx: dict) -> bool:
    return str(ctx.get("os_id", "")) == "1"


def _os_windows(ctx: dict) -> bool:
    return str(ctx.get("os_id", "")) == "2"


def _has_rhost(ctx: dict) -> bool:
    return bool(ctx.get("rhost"))


def _has_domain(ctx: dict) -> bool:
    return bool(ctx.get("domain"))


def _has_api_key(ctx: dict) -> bool:
    return bool(ctx.get("api_key"))


def _phase_in(ctx: dict, *phases: str) -> bool:
    return ctx.get("phase", "").lower() in phases


def _last_cmd_is(ctx: dict, *cmds: str) -> bool:
    return ctx.get("last_cmd", "").split()[0] if ctx.get("last_cmd") else "" in cmds


def _after(ctx: dict, *cmds: str) -> bool:
    first = (ctx.get("last_cmd") or "").split()
    return bool(first) and first[0] in cmds


# ── Tip registry ─────────────────────────────────────────────────────────────

TIPS: list[ProTip] = [
    # PrivEsc — Linux
    ProTip(
        text="Got a shell? Upload and run linPEAS to find privesc vectors automatically.",
        command="linpeas",
        trigger=lambda ctx: _os_linux(ctx) and _phase_in(ctx, "exploit", "privesc", "post-exploitation"),
        category="privesc",
    ),
    ProTip(
        text="Watch processes without root — pspy catches cron jobs and suid calls in real time.",
        command="pspy",
        trigger=lambda ctx: _os_linux(ctx) and _phase_in(ctx, "privesc", "exploit"),
        category="privesc",
    ),
    ProTip(
        text="After finding a SUID binary, look it up: gtfo <binary> — instant GTFOBins result.",
        command="gtfo sudo",
        trigger=lambda ctx: _os_linux(ctx) and _after(ctx, "suid_check", "linpeas"),
        category="privesc",
    ),
    ProTip(
        text="Check kernel exploits for this host with les (Linux Exploit Suggester).",
        command="les",
        trigger=lambda ctx: _os_linux(ctx) and _phase_in(ctx, "privesc"),
        category="privesc",
    ),
    # PrivEsc — Windows
    ProTip(
        text="On Windows: run winpeas to enumerate all local privesc vectors in one shot.",
        command="winpeas",
        trigger=lambda ctx: _os_windows(ctx) and _phase_in(ctx, "exploit", "privesc"),
        category="privesc",
    ),
    ProTip(
        text="Windows target with a domain? Run bloodhound to map AD attack paths.",
        command="bloodhound",
        trigger=lambda ctx: _os_windows(ctx) and _has_domain(ctx),
        category="privesc",
    ),
    # AI copilot
    ProTip(
        text="Ask the AI with session context pre-loaded: ask what privesc paths exist for this Linux host?",
        command="ask",
        trigger=lambda ctx: _has_api_key(ctx) and _phase_in(ctx, "privesc", "exploit"),
        category="ai",
    ),
    ProTip(
        text="Let Groq analyze your scan and suggest the next move: ask what services look exploitable?",
        command="ask",
        trigger=lambda ctx: _has_api_key(ctx) and _after(ctx, "lazynmap", "ping", "auto_populate"),
        category="ai",
    ),
    ProTip(
        text="Generate a full attack playbook from your scan results: ai_playbook",
        command="ai_playbook",
        trigger=lambda ctx: _has_api_key(ctx) and _phase_in(ctx, "recon", "scan", "enum"),
        category="ai",
    ),
    # Operational
    ProTip(
        text="After getting creds, run l00t for a unified table of everything captured.",
        command="l00t",
        trigger=lambda ctx: _after(ctx, "createcredentials", "responder", "secretsdump", "mimikatzpy"),
        category="ops",
    ),
    ProTip(
        text="Record the next reachable host: pivot <new-ip>  — tracks your lateral movement chain.",
        command="pivot",
        trigger=lambda ctx: _phase_in(ctx, "lateral", "privesc") and _has_rhost(ctx),
        category="ops",
    ),
    ProTip(
        text="Run sitrep for a full operational picture: scans, loot, tasks, notes, pivots in one view.",
        command="sitrep",
        trigger=lambda ctx: _phase_in(ctx, "exploit", "privesc", "lateral"),
        category="ops",
    ),
    ProTip(
        text="After finding a domain, run auto_populate to extract all facts into the world model.",
        command="auto_populate",
        trigger=lambda ctx: _has_domain(ctx) and _after(ctx, "lazynmap", "ping"),
        category="ops",
    ),
    # Ecosystem
    ProTip(
        text="Need a modern C2? run adaptixc2 — it speaks the same beacon protocol as LazyOwn.",
        command="run adaptixc2",
        trigger=lambda ctx: _phase_in(ctx, "command & control", "c2", "lateral") and _has_rhost(ctx),
        category="ecosystem",
    ),
    ProTip(
        text="Serving payloads? beacon and blacksandbeacon are lighter alternatives to the Go stub.",
        command="run beacon",
        trigger=lambda ctx: _phase_in(ctx, "exploit", "c2"),
        category="ecosystem",
    ),
    # Automation
    ProTip(
        text="After recon, auto_pwn fully exploits the target autonomously from scan to shell.",
        command="auto_pwn",
        trigger=lambda ctx: _after(ctx, "lazynmap", "auto_populate", "nmap") and _has_rhost(ctx),
        category="automation",
    ),
    ProTip(
        text="Build an exploit chain with chain <target> — maps nmap services to CVEs automatically.",
        command="chain",
        trigger=lambda ctx: _after(ctx, "lazynmap", "nmap", "rustscan") and _has_rhost(ctx),
        category="automation",
    ),
    ProTip(
        text="hunt <target> profiles and auto-exploits the most promising vulnerability.",
        command="hunt",
        trigger=lambda ctx: _phase_in(ctx, "exploit", "enum") and _has_rhost(ctx),
        category="automation",
    ),
    ProTip(
        text="Run Nuclei templates against the web target: nuclei <url> or lazynuclei.",
        command="nuclei",
        trigger=lambda ctx: _after(ctx, "gobuster", "ffuf", "whatweb", "lazynmap"),
        category="automation",
    ),
    ProTip(
        text="Generate a playbook from scan results: playbook_generate <target>.",
        command="playbook_generate",
        trigger=lambda ctx: _after(ctx, "lazynmap", "nmap") and _has_rhost(ctx),
        category="automation",
    ),
    # Security
    ProTip(
        text="Encrypt sensitive session data when stepping away: encrypt.",
        command="encrypt",
        trigger=lambda ctx: _after(ctx, "secretsdump", "mimikatz", "l00t", "hashcat"),
        category="security",
    ),
    ProTip(
        text="Scan for malware and backdoors on the compromised host: yara_scan <path>.",
        command="yara_scan",
        trigger=lambda ctx: _phase_in(ctx, "postexp", "privesc") and _has_rhost(ctx),
        category="security",
    ),
    ProTip(
        text="Browse community YARA rules: yara_marketplace search ransomware.",
        command="yara_marketplace search",
        trigger=lambda ctx: _after(ctx, "yara_scan"),
        category="security",
    ),
    ProTip(
        text="Unlock your session data when resuming: decrypt.",
        command="decrypt",
        trigger=lambda ctx: True,  # always relevant at session start
        category="security",
    ),
    # Collaboration
    ProTip(
        text="Working with a team? Start a tracked campaign: campaign new <name> --scope <CIDR>.",
        command="campaign new",
        trigger=lambda ctx: _after(ctx, "ping", "arpscan", "lazynmap") and _has_rhost(ctx),
        category="collab",
    ),
    ProTip(
        text="Share your session in real-time with the team: collab_join.",
        command="collab_join",
        trigger=lambda ctx: _has_rhost(ctx),
        category="collab",
    ),
    ProTip(
        text="Open the live dashboard with topology and engagement stats: dashboard.",
        command="dashboard",
        trigger=lambda ctx: _phase_in(ctx, "exploit", "lateral", "privesc"),
        category="collab",
    ),
    ProTip(
        text="Browse community plugins and YARA/Nuclei templates: marketplace config.",
        command="marketplace config",
        trigger=lambda ctx: True,
        category="collab",
    ),
    # Discovery
    ProTip(
        text="Discover all available Nuclei templates: nuclei_marketplace list.",
        command="nuclei_marketplace list",
        trigger=lambda ctx: _after(ctx, "lazynmap", "nuclei", "lazynuclei"),
        category="discovery",
    ),
    ProTip(
        text="Browse the full command palette for this phase: palette <phase>.",
        command="palette",
        trigger=lambda ctx: True,
        category="discovery",
    ),
]

# Session-start tips (shown once at boot, independent of trigger)
_SESSION_TIPS: list[str] = [
    "Run [bold]sitrep[/] at the start of every shift for a unified operational picture.",
    "Use [bold]phase <name>[/] to advance the kill chain — the dashboard updates in real time.",
    "Use [bold]auto_pwn <target>[/] for fully-automated exploitation from recon to shell.",
    "Use [bold]chain <target>[/] to build an exploit chain from your nmap scan results.",
    "Use [bold]hunt <target>[/] to auto-exploit the most promising vulnerability rank.",
    "Use [bold]tgrep <pattern>[/] to search everything you've run this session. Try: tgrep password",
    "Use [bold]nuclei <url>[/] to run vulnerability templates against a web service.",
    "Use [bold]yara_scan <path>[/] to scan for malware and backdoors on compromised hosts.",
    "Use [bold]encrypt[/] to lock sensitive session data when you step away.",
    "Use [bold]collab_join[/] to work with your team in real time via shared events.",
    "Use [bold]campaign new <name> --scope <CIDR>[/] to start a tracked operation.",
    "Use [bold]dashboard[/] for a live Textual TUI with topology and engagement stats.",
    "Use [bold]marketplace config[/] to browse and enable 76+ YAML addons interactively.",
    "Use [bold]nuclei_marketplace list[/] to browse installable Nuclei vulnerability templates.",
    "Use [bold]yara_marketplace list[/] to browse and install community malware detection rules.",
    "Use [bold]playbook_generate <target>[/] to derive an attack playbook from your scans.",
    "Use [bold]palette privesc[/] to browse all privilege escalation commands.",
    "Use [bold]l00t[/] to see all captured credentials across all sessions files at once.",
    "Use [bold]note <text>[/] to capture findings with rhost+phase context — survives restarts.",
    "Use [bold]wizard --check[/] to see your current readiness score at any time.",
]

_last_tip_index: int = -1


def get_session_tip(ctx: dict[str, Any]) -> str | None:
    """Return a single tip to show at session start.

    Prefers tips that match the current context. Falls back to rotating
    through the session tip list so the operator sees something fresh each
    session.

    Args:
        ctx: Context dict with keys: phase, os_id, rhost, domain, api_key.

    Returns:
        Rich-formatted string, or None if tips are disabled.
    """
    global _last_tip_index
    matched = [t for t in TIPS if _safe_trigger(t, ctx)]
    if matched:
        tip = random.choice(matched)
        return f"[bold]★ tip:[/] {tip.text}  [dim bold]→ {tip.command}[/]"
    idx = (_last_tip_index + 1) % len(_SESSION_TIPS)
    _last_tip_index = idx
    return f"[bold]★ tip:[/] {_SESSION_TIPS[idx]}"


_last_shown_tip: str = ""


def render_contextual_tip(last_cmd: str, ctx: dict[str, Any]) -> None:
    """Print a single dim tip line when the last command triggers one.

    Called from the postcmd hook. Does nothing when no tip matches or when
    the same tip would repeat.

    Args:
        last_cmd: Raw string of the command just executed.
        ctx: Context dict with current session state.
    """
    global _last_shown_tip
    first = (last_cmd or "").split()
    if not first or first[0] in _SKIP_COMMANDS:
        return
    ctx = {**ctx, "last_cmd": last_cmd}
    matched = [t for t in TIPS if _safe_trigger(t, ctx)]
    if not matched:
        return
    tip = random.choice(matched)
    tip_key = tip.command
    if tip_key == _last_shown_tip:
        return
    _last_shown_tip = tip_key
    t = Text()
    t.append("  ★ ", style="bold dim yellow")
    t.append(tip.text[:80], style="dim white italic")
    t.append(f"  → {tip.command}", style="bold dim cyan")
    _console.print(t)


def print_session_tip(ctx: dict[str, Any]) -> None:
    """Print the session-start tip (called once after the banner).

    Args:
        ctx: Context dict with current session state.
    """
    msg = get_session_tip(ctx)
    if msg:
        _console.print(f"    {msg}")
        _console.print()


def _safe_trigger(tip: ProTip, ctx: dict[str, Any]) -> bool:
    try:
        return tip.trigger(ctx)
    except Exception:
        return False


__all__ = [
    "ProTip",
    "TIPS",
    "get_session_tip",
    "print_session_tip",
    "render_contextual_tip",
]
