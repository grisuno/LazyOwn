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

import csv
import logging
import math
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.text import Text

from cli.noise_verbs import BASE_NOISE_VERBS, HINTS_EXTRA_VERBS

if TYPE_CHECKING:
    from cli.graph_advisor import GraphAdvisor

SKIP_COMMANDS: frozenset[str] = BASE_NOISE_VERBS | HINTS_EXTRA_VERBS

_log = logging.getLogger(__name__)

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
    "privesc": [
        "linpeas", "winpeas", "pspy64", "sudo_privesc", "printspoofer", "juicypotato",
        "whoami_priv", "gtfo", "les", "crystal_ball", "kerberos_ticket", "adcs_check",
    ],
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
    except Exception as exc:
        _log.warning("Graph advisor hints failed for '%s': %s", cmd, exc)
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


_CONFIDENCE_HALF_SCORE: float = 1.0
_EVIDENCE_VERB_MAX: int = 22
_EVIDENCE_REASON_MAX: int = 54
_CONFIDENCE_HIGH_THRESHOLD: int = 50
_SOURCE_SEP: str = "+"


@dataclass(frozen=True)
class EvidenceHint:
    """A next-step suggestion enriched with its justification and confidence.

    The bare inline hint prints only command names, forcing the operator to
    trust an unexplained list. This value object carries the *why* and *how
    sure* so the hint line reads like advice rather than a menu.

    Attributes:
        verb: The command (or copy-paste preview) to run next.
        confidence: Display confidence in ``[0, 100]`` derived from the fused
            recommendation score via :func:`confidence_from_score`.
        reason: One-line English justification, stripped of the ``[source]``
            provenance tag and truncated for the inline hint line.
        sources: Names of the signals that agreed on this action.
    """

    verb: str
    confidence: int
    reason: str
    sources: tuple[str, ...]


def confidence_from_score(score: float) -> int:
    """Map an unbounded fused recommendation score to a 0-100 display confidence.

    :class:`cli.recommendation.RecommendationEngine` produces scores that are
    unbounded above because multiple agreeing signals add up, so a raw
    percentage would be meaningless. This applies a saturating map
    ``100 * s / (s + K)`` where ``K`` (:data:`_CONFIDENCE_HALF_SCORE`) is the
    score at which confidence reaches 50%. The map is monotonic — more signal
    agreement yields higher confidence — and floors at 99 so the display never
    claims a dishonest 100%.

    Args:
        score: The fused recommendation score. Negative values are floored at
            zero.

    Returns:
        Integer confidence in ``[0, 99]``.
    """
    positive = score if score > 0.0 else 0.0
    return min(math.floor(100.0 * positive / (positive + _CONFIDENCE_HALF_SCORE)), 99)


def _clean_reason(reasons: Sequence[str]) -> str:
    """Return the primary reason without its ``[source]`` tag, truncated.

    Args:
        reasons: The ordered provenance lines from a fused recommendation, each
            shaped ``"[signal] justification"`` by the engine accumulator.

    Returns:
        The first justification with any leading ``[signal] `` tag removed and
        truncated to :data:`_EVIDENCE_REASON_MAX`. Empty when no reason exists.
    """
    if not reasons:
        return ""
    first = reasons[0]
    if first.startswith("[") and "] " in first:
        first = first.split("] ", 1)[1]
    return _truncate(first.strip(), _EVIDENCE_REASON_MAX)


def build_evidence_hints(recommendations: Sequence[Any], limit: int) -> list[EvidenceHint]:
    """Convert fused recommendations into display-ready evidence hints.

    A recommendation without a usable verb or without a justification is
    skipped so the operator never sees a bare, unexplained suggestion — an
    explained shorter list beats a padded opaque one.

    Args:
        recommendations: Ranked objects exposing ``action``, ``score``,
            ``reasons``, ``sources`` and optional ``command_preview`` (a
            :class:`cli.recommendation.Recommendation` or any duck-typed
            equivalent), best first.
        limit: Maximum number of hints to return.

    Returns:
        Up to ``limit`` :class:`EvidenceHint` items preserving input order.
    """
    out: list[EvidenceHint] = []
    for rec in recommendations:
        verb_raw = str(
            getattr(rec, "command_preview", "") or getattr(rec, "action", "") or ""
        ).strip()
        if not verb_raw:
            continue
        reason = _clean_reason(tuple(getattr(rec, "reasons", ()) or ()))
        if not reason:
            continue
        out.append(
            EvidenceHint(
                verb=_truncate(verb_raw, _EVIDENCE_VERB_MAX),
                confidence=confidence_from_score(float(getattr(rec, "score", 0.0) or 0.0)),
                reason=reason,
                sources=tuple(getattr(rec, "sources", ()) or ()),
            )
        )
        if len(out) >= limit:
            break
    return out


def render_evidence_hints(hints: Sequence[EvidenceHint]) -> None:
    """Print evidence-backed hint lines: verb, confidence, reason, provenance.

    The first hint carries the ``↳`` arrow; the rest are indented to align, so
    a glance reads as one ranked block of advice.

    Args:
        hints: The hints to render, already truncated and ranked.

    Returns:
        None — writes one dim line per hint to stdout.
    """
    for index, hint in enumerate(hints):
        line = Text()
        line.append("  ↳ " if index == 0 else "    ", style="bold dim cyan")
        line.append(hint.verb, style="cyan")
        confidence_style = (
            "dim green" if hint.confidence >= _CONFIDENCE_HIGH_THRESHOLD else "dim yellow"
        )
        line.append(f"  {hint.confidence}%  ", style=confidence_style)
        line.append(hint.reason, style="dim white italic")
        if hint.sources:
            line.append(f"  {_SOURCE_SEP.join(hint.sources)}", style="dim")
        _HINT_CONSOLE.print(line)


def read_run_commands(sessions_dir: str = "sessions") -> set[str]:
    """Return the set of command names already executed this session.

    Reads the CSV transcript and extracts the first token of the first
    populated column (``tool``, ``command``, or ``name``). Shared by the
    inline hint renderer, the tips engine, and any other surface that must
    filter already-run commands out of its suggestions.

    Args:
        sessions_dir: Directory containing ``LazyOwn_session_report.csv``.

    Returns:
        A set of command verbs, empty when the transcript is missing or
        unreadable.
    """
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


def _collect_command_hints(
    cmd: str,
    phase: str,
    already_run: set[str],
    limit: int,
) -> list[str]:
    """Collect forward-looking hint verbs from adjacency then phase priority.

    Kill-chain adjacency (``_KILL_CHAIN_NEXT``) feeds the list first; when it
    falls short of ``limit`` the phase-priority table fills the remainder.
    Commands already executed this session and the predecessor itself are
    excluded so the hint always looks forward.

    Args:
        cmd: The command that just ran. Empty disables the adjacency lookup
            and collects phase priority only.
        phase: Current engagement phase identifier.
        already_run: Set of verbs already present in the transcript.
        limit: Maximum number of verbs to return.

    Returns:
        Ordered candidate verbs, length at most ``limit``.
    """
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

    candidates = _collect_command_hints(cmd, phase, read_run_commands(sessions_dir), limit)
    labels = [_truncate(c, _MAX_LABEL_LEN) for c in candidates]
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
            Only the first token is considered. When empty or in
            :data:`SKIP_COMMANDS` the adjacency lookup is skipped and the
            phase priority table feeds the result.
        phase: Current engagement phase identifier. Falls back to
            ``recon`` when empty.
        sessions_dir: Path to ``sessions/`` used to filter out commands
            that already appear in the CSV transcript.
        limit: Maximum number of verbs to return.

    Returns:
        Ordered list of suggested command verbs, length ``<= limit``.
        Returns an empty list when no candidates remain after filtering.
    """
    cmd = _first_token(last_command)
    if not cmd or cmd in SKIP_COMMANDS:
        cmd = ""
    return _collect_command_hints(cmd, phase, read_run_commands(sessions_dir), limit)


__all__ = [
    "SKIP_COMMANDS",
    "render_inline_hints",
    "render_command_hints",
    "command_hints",
    "read_run_commands",
    "EvidenceHint",
    "confidence_from_score",
    "build_evidence_hints",
    "render_evidence_hints",
]
