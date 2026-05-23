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
from dataclasses import dataclass
from typing import Any, Callable

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
]

# Session-start tips (shown once at boot, independent of trigger)
_SESSION_TIPS: list[str] = [
    "Run [bold]sitrep[/] at the start of every shift for a unified operational picture.",
    "Use [bold]phase <name>[/] to advance the kill chain — the dashboard updates in real time.",
    "Use [bold]tgrep <pattern>[/] to search everything you've run this session. Try: tgrep password",
    "Use [bold]ask <question>[/] to query the AI with your live session context pre-loaded.",
    "Use [bold]l00t[/] to see all captured credentials across all sessions files at once.",
    "Use [bold]note <text>[/] to capture findings with rhost+phase context — survives restarts.",
    "Use [bold]tasks[/] to see the autonomous agent's task queue and add your own.",
    "Use [bold]palette privesc[/] to browse all privilege escalation commands.",
    "Use [bold]gtfo <binary>[/] to look up GTFOBins for any binary you find with SUID.",
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
