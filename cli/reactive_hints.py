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
        "palette_k",
        "browse",
        "timeline_browser",
        "form",
        "graph_overlay",
        "toast_clear",
        "assign",
        "edit",
        "run_script",
        "shortcuts",
        "_relative_run",
    }
)

# Ordered kill-chain: after running X, suggest Y (phase-agnostic sensible defaults)
_KILL_CHAIN_NEXT: dict[str, list[str]] = {
    "ping": ["lazynmap", "arpscan", "hosts_discovery", "auto_pwn"],
    "lazynmap": ["gobuster", "ffuf", "enum4linux", "searchsploit", "auto_populate", "auto_pwn", "chain"],
    "rustscan": ["gobuster", "ffuf", "enum4linux", "searchsploit", "chain"],
    "nmap": ["gobuster", "ffuf", "enum4linux", "searchsploit", "chain", "nuclei"],
    "gobuster": ["ffuf", "nikto", "whatweb", "feroxbuster", "nuclei", "wfuzz"],
    "ffuf": ["nikto", "whatweb", "burpsuite", "sqlmap", "nuclei"],
    "enum4linux": ["crackmapexec", "secretsdump", "kerbrute", "hunt", "auto_pwn"],
    "crackmapexec": ["secretsdump", "evil-winrm", "psexec", "l00t", "sitrep"],
    "secretsdump": ["evil-winrm", "psexec", "hashcat", "l00t", "encrypt"],
    "linpeas": ["pspy64", "find_suid", "sudo_privesc", "gtfo", "les", "whoami_priv"],
    "winpeas": ["printspoofer", "juicypotato", "whoami_priv", "mimikatz"],
    "whoami_priv": ["linpeas", "winpeas", "crystal_ball", "sudo_privesc", "gtfo"],
    "sudo_privesc": ["gtfo", "les", "crystal_ball", "linpeas"],
    "printspoofer": ["whoami_priv", "juicypotato", "mimikatz"],
    "juicypotato": ["whoami_priv", "printspoofer", "mimikatz"],
    "crystal_ball": ["sudo_privesc", "gtfo", "les", "printspoofer", "juicypotato"],
    "searchsploit": ["lazynmap", "gobuster", "exploit_db", "chain", "hunt"],
    "kerbrute": ["GetNPUsers", "GetUserSPNs", "crackmapexec", "hashcat"],
    "nikto": ["sqlmap", "burpsuite", "ffuf", "nuclei", "whatweb"],
    "whatweb": ["gobuster", "nikto", "burpsuite", "nuclei", "ffuf"],
    "feroxbuster": ["ffuf", "nikto", "whatweb", "nuclei"],
    "sqlmap": ["burpsuite", "ffuf", "wfuzz"],
    "hashcat": ["evil-winrm", "ssh", "crackmapexec", "l00t"],
    "john": ["evil-winrm", "ssh", "crackmapexec", "l00t"],
    "evil-winrm": ["winpeas", "secretsdump", "mimikatz", "whoami_priv"],
    "ssh": ["linpeas", "pspy64", "sudo_privesc", "yara_scan"],
    "ftp": ["gobuster", "enum4linux", "searchsploit"],
    "smb": ["enum4linux", "crackmapexec", "secretsdump"],
    "responder": ["crackmapexec", "hashcat", "secretsdump"],
    "arpscan": ["lazynmap", "hosts_discovery"],
    "auto_populate": ["sitrep", "ask", "phase", "auto_pwn"],
    "auto_pwn": ["hunt", "l00t", "sitrep", "note", "dashboard"],
    "chain": ["hunt", "auto_pwn", "nuclei", "playbook_generate"],
    "hunt": ["auto_pwn", "l00t", "sitrep", "linpeas", "winpeas"],
    "nuclei": ["lazynmap", "gobuster", "sitrep", "auto_pwn"],
    "lazynuclei": ["sitrep", "auto_pwn"],
    "yara_scan": ["l00t", "note", "sitrep"],
    "playbook_generate": ["playbook_run", "auto_pwn", "hunt"],
    "playbook_run": ["l00t", "sitrep", "note"],
    "campaign": ["sitrep", "phase", "note"],
    "collab_join": ["sitrep", "note"],
    "dashboard": ["sitrep", "phase", "tasks"],
    "phase": ["lazynmap", "auto_pwn", "sitrep"],
    "dotnet_payload": ["staged_delivery", "polymorphic", "payload"],
    "staged_delivery": ["dotnet_payload", "polymorphic", "createrevshell"],
    "polymorphic": ["dotnet_payload", "evasive_payload", "mutate_shellcode"],
    "macos_payload": ["timestomp", "log_tamper", "memory_clean"],
    "linux_advanced_payload": ["log_tamper", "timestomp", "forensic_clean"],
    "kerberos_ticket": ["kerberoast", "delegation_enum", "dacl_abuse"],
    "delegation_enum": ["delegation_attack", "kerberos_ticket", "dacl_abuse"],
    "delegation_attack": ["kerberos_ticket", "secretsdump", "evil-winrm"],
    "dacl_abuse": ["delegation_enum", "gpo_abuse", "kerberoast"],
    "gpo_abuse": ["dacl_abuse", "delegation_enum", "forensic_clean"],
    "kerberoast": ["hashcat", "kerberos_ticket", "secretsdump"],
    "adcs_check": ["kerberos_ticket", "certipy_ad", "delegation_attack"],
    "entra_attack": ["cross_cloud", "saas_enum", "opsec_score"],
    "aws_privesc": ["cross_cloud", "entra_attack", "opsec_score"],
    "gcp_privesc": ["cross_cloud", "aws_privesc", "entra_attack"],
    "k8s_attack": ["cross_cloud", "container_escape", "opsec_score"],
    "cross_cloud": ["aws_privesc", "entra_attack", "gcp_privesc"],
    "saas_enum": ["entra_attack", "cross_cloud", "sitrep"],
    "opsec_score": ["log_tamper", "forensic_clean", "memory_clean"],
    "log_tamper": ["forensic_clean", "timestomp", "memory_clean"],
    "forensic_clean": ["log_tamper", "timestomp", "memory_clean"],
    "timestomp": ["forensic_clean", "log_tamper", "memory_clean"],
    "memory_clean": ["forensic_clean", "log_tamper", "timestomp"],
    "network_opsec": ["opsec_score", "log_tamper", "timestomp"],
    "auditd_disable": ["log_tamper", "forensic_clean", "network_opsec"],
    "sysmon_disable": ["log_tamper", "forensic_clean", "network_opsec"],
}

_PHASE_PRIORITY: dict[str, list[str]] = {
    "recon": ["ping", "lazynmap", "rustscan", "arpscan", "whois", "hosts_discovery", "auto_populate"],
    "enum": [
        "gobuster", "ffuf", "enum4linux", "nikto", "whatweb", "feroxbuster", "kerbrute",
        "nuclei", "lazynuclei", "wfuzz", "dnsenum", "snmpwalk",
    ],
    "exploit": [
        "searchsploit", "crackmapexec", "sqlmap", "burpsuite", "evil-winrm",
        "auto_pwn", "chain", "hunt", "exploit_db", "hydra",
    ],
    "privesc": ["linpeas", "winpeas", "pspy64", "sudo_privesc", "printspoofer", "juicypotato", "whoami_priv", "gtfo", "les", "crystal_ball", "kerberos_ticket", "adcs_check"],
    "lateral": [
        "crackmapexec", "evil-winrm", "chisel", "secretsdump", "psexec",
        "ssh", "xfreerdp", "collab_join", "kerberos_ticket", "delegation_attack",
    ],
    "cred": [
        "hashcat", "john", "responder", "kerbrute", "secretsdump",
        "l00t", "mimikatz", "lazagne", "kerberoast", "dacl_abuse",
    ],
    "postexp": [
        "linpeas", "winpeas", "mimikatz", "secretsdump", "whoami_priv",
        "yara_scan", "note", "sitrep", "dashboard", "encrypt",
        "opsec_score", "log_tamper", "forensic_clean", "timestomp", "memory_clean",
    ],
    "exfil": ["download_c2", "nc", "curl", "scp", "rsync", "l00t", "encrypt", "network_opsec"],
    "persist": [
        "campaign", "sitrep", "note", "encrypt", "gpo_abuse", "dacl_abuse",
        "macos_payload", "linux_advanced_payload", "dotnet_payload",
    ],
    "cloud": [
        "entra_attack", "aws_privesc", "gcp_privesc", "k8s_attack",
        "cross_cloud", "saas_enum", "opsec_score",
    ],
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
    candidates: list[str] = [c for c in _KILL_CHAIN_NEXT.get(cmd, []) if c not in already_run]

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
