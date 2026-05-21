"""Non-blocking inline hint renderer for the LazyOwn cmd2 shell.

After each command executes, a single dim line is printed with the top-N
graph-based next-step suggestions derived from the graphify knowledge graph.
The GraphLoader caches by (path, mtime) so rendering is sub-millisecond after
the first graph load; subsequent calls return from memory.

Design notes:
- Zero coupling to cmd2, lazyown.py or Flask — this module is a pure renderer.
- The caller decides whether hints are enabled (reads payload.json flag).
- Output goes to stdout via rich so ANSI is handled correctly on all terminals.
- Commands on SKIP_COMMANDS never produce hints (noise-free UX).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.text import Text

if TYPE_CHECKING:
    from cli.graph_advisor import GraphAdvisor

SKIP_COMMANDS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "shell",
        "dashboard",
        "suggest_next",
        "graph_search",
        "neighbors",
        "god_nodes",
        "set",
        "show",
        "palette",
        "assign",
        "edit",
        "run_script",
        "shortcuts",
        "_relative_run",
    }
)

# Ordered kill-chain: after running X, suggest Y (phase-agnostic sensible defaults)
_KILL_CHAIN_NEXT: dict[str, list[str]] = {
    "ping":          ["lazynmap", "arpscan", "hosts_discovery"],
    "lazynmap":      ["gobuster", "ffuf", "enum4linux", "searchsploit"],
    "rustscan":      ["gobuster", "ffuf", "enum4linux", "searchsploit"],
    "nmap":          ["gobuster", "ffuf", "enum4linux", "searchsploit"],
    "gobuster":      ["ffuf", "nikto", "whatweb", "feroxbuster"],
    "ffuf":          ["nikto", "whatweb", "burpsuite", "sqlmap"],
    "enum4linux":    ["crackmapexec", "secretsdump", "kerbrute"],
    "crackmapexec":  ["secretsdump", "evil-winrm", "psexec"],
    "secretsdump":   ["evil-winrm", "psexec", "hashcat"],
    "linpeas":       ["pspy64", "find_suid", "sudo_privesc"],
    "winpeas":       ["printspoofer", "juicypotato", "whoami_priv"],
    "searchsploit":  ["lazynmap", "gobuster", "exploit_db"],
    "kerbrute":      ["GetNPUsers", "GetUserSPNs", "crackmapexec"],
    "nikto":         ["sqlmap", "burpsuite", "ffuf"],
    "whatweb":       ["gobuster", "nikto", "burpsuite"],
    "feroxbuster":   ["ffuf", "nikto", "whatweb"],
    "sqlmap":        ["burpsuite", "ffuf", "wfuzz"],
    "hashcat":       ["evil-winrm", "ssh", "crackmapexec"],
    "john":          ["evil-winrm", "ssh", "crackmapexec"],
    "evil-winrm":    ["winpeas", "secretsdump", "mimikatz"],
    "ssh":           ["linpeas", "pspy64", "sudo_privesc"],
    "ftp":           ["gobuster", "enum4linux", "searchsploit"],
    "smb":           ["enum4linux", "crackmapexec", "secretsdump"],
    "responder":     ["crackmapexec", "hashcat", "secretsdump"],
}

_PHASE_PRIORITY: dict[str, list[str]] = {
    "recon":   ["ping", "lazynmap", "rustscan", "arpscan", "whois"],
    "enum":    ["gobuster", "ffuf", "enum4linux", "nikto", "whatweb", "feroxbuster", "kerbrute"],
    "exploit": ["searchsploit", "crackmapexec", "sqlmap", "burpsuite", "evil-winrm"],
    "privesc": ["linpeas", "winpeas", "pspy64", "sudo_privesc", "printspoofer"],
    "lateral": ["crackmapexec", "evil-winrm", "chisel", "secretsdump", "psexec"],
    "cred":    ["hashcat", "john", "responder", "kerbrute", "secretsdump"],
    "postexp": ["linpeas", "winpeas", "mimikatz", "secretsdump", "whoami_priv"],
    "exfil":   ["download_c2", "nc", "curl", "scp", "rsync"],
}

_MAX_LABEL_LEN: int = 24
_HINT_CONSOLE: Console = Console(stderr=False, highlight=False, soft_wrap=True)


def render_inline_hints(
    advisor: GraphAdvisor,
    last_command: str,
    limit: int = 3,
    enabled: bool = True,
) -> None:
    """Print a single dim hint line below the command output and return immediately.

    The line format is:
        ↳ label_a · label_b · label_c

    This renders between the command output and the next cmd2 prompt so it
    never blocks the operator from typing the next command.

    Args:
        advisor: GraphAdvisor instance (reuses its internal mtime-keyed cache).
        last_command: Raw command string that just executed (first token used).
        limit: Maximum number of suggestions to display.
        enabled: When False the function is a no-op. Controlled by the
            ``enable_inline_hints`` key in payload.json.

    Returns:
        None — side effect is at most one line written to stdout.
    """
    if not enabled:
        return
    cmd = _first_token(last_command)
    if not cmd or cmd in SKIP_COMMANDS:
        return
    try:
        suggestions = advisor.suggest_next(recent_commands=[cmd], limit=limit)
    except Exception:
        return
    if not suggestions:
        return
    labels = _extract_labels(suggestions, limit)
    if not labels:
        return
    _render(labels)


def _first_token(raw: str) -> str:
    parts = (raw or "").split()
    return parts[0] if parts else ""


def _extract_labels(suggestions: list[dict], limit: int) -> list[str]:
    out: list[str] = []
    for s in suggestions:
        label = s.get("label") or s.get("id") or ""
        if label:
            out.append(_truncate(label, _MAX_LABEL_LEN))
        if len(out) >= limit:
            break
    return out


def _truncate(value: str, max_len: int) -> str:
    return value if len(value) <= max_len else value[: max_len - 1] + "…"


def _render(labels: list[str]) -> None:
    hint = Text()
    hint.append("  ↳ ", style="bold dim cyan")
    hint.append(" · ".join(labels), style="dim white italic")
    _HINT_CONSOLE.print(hint)


def _read_run_commands(sessions_dir: str = "sessions") -> set[str]:
    """Return the set of command names already executed this session."""
    import csv
    from pathlib import Path

    path = Path(sessions_dir) / "LazyOwn_session_report.csv"
    seen: set[str] = set()
    if not path.exists():
        return seen
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                for col in ("tool", "command", "name"):
                    val = (row.get(col) or "").strip().split()[0]
                    if val:
                        seen.add(val)
                        break
    except Exception:
        pass
    return seen


def render_command_hints(
    last_command: str,
    phase: str = "",
    sessions_dir: str = "sessions",
    limit: int = 3,
    enabled: bool = True,
) -> None:
    """Print phase-aware, history-filtered command hints after each step.

    Uses kill-chain adjacency (``_KILL_CHAIN_NEXT``) first, then falls back
    to phase priority (``_PHASE_PRIORITY``).  Commands already in the session
    CSV are skipped so the hint is always forward-looking.

    Args:
        last_command: The command that just ran (first token used).
        phase:        Current engagement phase (from payload.json / world_model).
        sessions_dir: Path to sessions/ directory.
        limit:        Maximum labels to display.
        enabled:      When False this is a no-op.

    Returns:
        None — prints at most one dim line.
    """
    if not enabled:
        return
    cmd = _first_token(last_command)
    if not cmd or cmd in SKIP_COMMANDS:
        return

    already_run = _read_run_commands(sessions_dir)

    # 1. Kill-chain adjacency: known follow-up for this specific command
    candidates: list[str] = [
        c for c in _KILL_CHAIN_NEXT.get(cmd, [])
        if c not in already_run
    ]

    # 2. Phase priority fallback
    if len(candidates) < limit:
        phase_key = phase.lower() if phase else "recon"
        for c in _PHASE_PRIORITY.get(phase_key, _PHASE_PRIORITY.get("recon", [])):
            if c not in already_run and c not in candidates and c != cmd:
                candidates.append(c)
            if len(candidates) >= limit * 2:
                break

    labels = [_truncate(c, _MAX_LABEL_LEN) for c in candidates[:limit]]
    if labels:
        _render(labels)


def command_hints(
    last_command: str,
    phase: str = "",
    sessions_dir: str = "sessions",
    limit: int = 3,
) -> list[str]:
    """Return the top next-step command verbs without printing them.

    Mirrors the logic of :func:`render_command_hints` but separates the
    suggestion engine from the I/O side effect so other UI surfaces (the
    persistent status bar in :mod:`cli.status_bar`, future TUI widgets)
    can consume the exact same data the inline hints use.

    Args:
        last_command: Raw command string that most recently executed.
            Only the first token is considered.
        phase: Current engagement phase identifier. Falls back to
            ``recon`` when empty.
        sessions_dir: Path to ``sessions/`` used to filter out commands
            that already appear in the CSV transcript.
        limit: Maximum number of verbs to return.

    Returns:
        Ordered list of suggested command verbs, length ``<= limit``.
        Returns an empty list when ``last_command`` is empty, falls in
        :data:`SKIP_COMMANDS`, or no candidates remain after filtering.
    """
    cmd = _first_token(last_command)
    if not cmd or cmd in SKIP_COMMANDS:
        cmd = ""
    already_run = _read_run_commands(sessions_dir)
    candidates: list[str] = []
    if cmd:
        candidates = [c for c in _KILL_CHAIN_NEXT.get(cmd, []) if c not in already_run]
    if len(candidates) < limit:
        phase_key = phase.lower().strip() if phase else "recon"
        priority = _PHASE_PRIORITY.get(phase_key) or _PHASE_PRIORITY.get("recon", [])
        for verb in priority:
            if verb == cmd or verb in already_run or verb in candidates:
                continue
            candidates.append(verb)
            if len(candidates) >= limit:
                break
    return candidates[:limit]


__all__ = ["SKIP_COMMANDS", "render_inline_hints", "render_command_hints", "command_hints"]
