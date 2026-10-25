"""Full CLI catalog for the Lazy autonomous loop.

The loop historically routed only seven ``auto_*`` verbs plus a handful of
hardcoded probes. This module discovers every ``do_<verb>`` command of the
cmd2 shell (``cli/commands/*.py`` plus ``lazyown.py``) so the planner and
the workers can propose and execute any of the 800+ Lazy commands through
the same Guard and scope path as the built-in verbs.

Stdlib only. Lazy imports keep ``auto_registry`` cycle-free.
"""

from __future__ import annotations

import re
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "cli" / "commands"
LEGACY_SHELL = REPO_ROOT / "lazyown.py"

_DO_RE = re.compile(r"^\s*def (do_[a-z][a-z0-9_]*)\s*\(", re.MULTILINE)
_VERB_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")

CACHE_TTL_SEC = 5.0
_CACHE_LOCK = threading.Lock()
_CACHE: dict = {"at": 0.0, "mtimes": (), "verbs": ()}

FULL_CLI_DEFAULT = True

NO_TARGET_VERBS = frozenset(
    {
        "help",
        "apropos",
        "back",
        "quit",
        "exit",
        "banner",
        "version",
        "alias",
        "aliass",
        "addalias",
        "history",
        "set",
        "assign",
        "unassign",
        "reload",
        "shell",
        "py",
        "pyscript",
        "run_script",
        "shortcuts",
    }
)

_PHASE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("recon", ("scan", "nmap", "enum", "discover", "amass", "dns", "arp", "ping", "fuzz", "gobuster", "ffuf", "nikto", "whatweb", "host", "dig", "traceroute", "snmp", "smbmap", "ldap")),
    ("exploit", ("pwn", "exploit", "msf", "spray", "inject", "rce", "sqli", "lfi", "payload", "shell", "metasploit", "brute", "hydra", "crack")),
    ("cred", ("cred", "dump", "hash", "secret", "password", "kerb", "ticket", "vault", "domaindump")),
    ("lateral", ("pivot", "lateral", "winrm", "smb", "ssh", "rdp", "wmi", "psexec", "socks", "tunnel", "relay", "coerce")),
    ("privesc", ("peas", "privesc", "escalat", "suid", "sudo", "bypass", "uac", "token", "mimikatz", "seatbelt")),
    ("persist", ("persist", "backdoor", "implant", "beacon", "stager", "autorun", "cron")),
    ("exfil", ("exfil", "loot", "download", "siphon", "extract")),
    ("c2", ("c2", "beacon", "listener", "handler", "redirector", "malleable")),
    ("report", ("report", "note", "loot", "export", "evidence", "timeline")),
    ("ai", ("lazy_", "auto_", "ask", "agent", "swan", "groq", "ai_")),
)

_RISK_SAFE_PREFIXES = ("lazy_", "auto_", "list", "show", "help", "status", "ping", "dig", "host", "whatweb", "curl")
_RISK_HIGH_KEYWORDS = ("wipe", "shred", "format", "destroy", "rm_rf", "ransom", "wiper", "drop_table")
_RISK_EXPLOIT_KEYWORDS = ("pwn", "exploit", "msf", "payload", "inject", "rce", "brute", "spray", "bypass", "disable_defender", "auditd_disable")


def _source_files() -> list[Path]:
    """Return shell sources that may declare commands."""
    files = sorted(COMMANDS_DIR.glob("*.py")) if COMMANDS_DIR.is_dir() else []
    if LEGACY_SHELL.is_file():
        files.append(LEGACY_SHELL)
    return files


def _source_mtimes() -> tuple:
    """Return mtimes of command sources for cache invalidation."""
    marks = []
    for path in _source_files():
        try:
            marks.append((str(path), path.stat().st_mtime_ns))
        except OSError:
            continue
    return tuple(marks)


def _discover() -> tuple[str, ...]:
    """Scan shell sources for do_<verb> definitions."""
    found: set[str] = set()
    for path in _source_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in _DO_RE.finditer(text):
            found.add(match.group(1)[3:])
    return tuple(sorted(found))


def cli_verbs() -> tuple[str, ...]:
    """Return every discovered shell verb, cached by source mtime."""
    import time as _time

    mtimes = _source_mtimes()
    with _CACHE_LOCK:
        fresh = _CACHE["verbs"] and _CACHE["mtimes"] == mtimes and (_time.monotonic() - _CACHE["at"]) < CACHE_TTL_SEC
        if fresh:
            return _CACHE["verbs"]
    verbs = _discover()
    with _CACHE_LOCK:
        _CACHE["verbs"] = verbs
        _CACHE["mtimes"] = mtimes
        import time as _time_inner

        _CACHE["at"] = _time_inner.monotonic()
    return verbs


def is_cli_verb(name: str) -> bool:
    """Return True when name is a real shell command."""
    clean = (name or "").strip().split()[0] if (name or "").strip() else ""
    return bool(clean) and clean in set(cli_verbs())


def phase_for(verb: str) -> str:
    """Map a verb to its kill-chain phase via keyword affinity."""
    lowered = (verb or "").lower()
    for phase, keywords in _PHASE_KEYWORDS:
        if any(keyword in lowered for keyword in keywords):
            return phase
    return "other"


def risk_for(verb: str) -> str:
    """Classify a verb as safe, exploit or high risk."""
    lowered = (verb or "").lower()
    if any(keyword in lowered for keyword in _RISK_HIGH_KEYWORDS):
        return "high"
    if any(keyword in lowered for keyword in _RISK_EXPLOIT_KEYWORDS):
        return "exploit"
    return "safe"


def needs_target_for(verb: str) -> bool:
    """Return whether the verb usually carries a target argument."""
    clean = (verb or "").strip().split()[0] if (verb or "").strip() else ""
    if not clean or clean in NO_TARGET_VERBS:
        return False
    return True


def build_cli_command(verb: str, target: str = "") -> str:
    """Build a shell line for any CLI verb bound to target.

    Args:
        verb: Canonical shell verb without parameters.
        target: Optional target appended when the verb takes one.

    Returns:
        Command line ready for the shell executor.

    Raises:
        KeyError: Unknown verb.
        ValueError: Empty verb name.
    """
    clean = (verb or "").strip().split()[0] if (verb or "").strip() else ""
    if not clean:
        raise ValueError("verb name is required")
    if not _VERB_RE.match(clean):
        raise ValueError(f"invalid verb name: {clean!r}")
    if not is_cli_verb(clean):
        raise KeyError(f"unknown shell verb: {clean!r}")
    tail = (target or "").strip()
    if tail and needs_target_for(clean):
        return f"{clean} {tail}".strip()
    return clean


def search_cli_verbs(query: str = "", phase: str = "", limit: int = 30) -> list[dict]:
    """Search the full CLI catalog by keyword and phase.

    Args:
        query: Substring filter over verb names.
        phase: Optional kill-chain phase filter.
        limit: Max entries returned.

    Returns:
        List of verb descriptors with name, phase and risk.
    """
    needle = (query or "").lower()
    wanted_phase = (phase or "").lower()
    out = []
    for verb in cli_verbs():
        if needle and needle not in verb:
            continue
        verb_phase = phase_for(verb)
        if wanted_phase and verb_phase != wanted_phase:
            continue
        out.append({"name": verb, "phase": verb_phase, "risk": risk_for(verb)})
        if len(out) >= max(1, int(limit or 30)):
            break
    return out


def cli_catalog_for_phase(phase: str, limit: int = 40) -> str:
    """Return a compact verb list for LLM prompt injection."""
    names = [entry["name"] for entry in search_cli_verbs(phase=phase, limit=limit)]
    if not names:
        names = [verb for verb in cli_verbs()[: max(1, int(limit or 40))]]
    return ", ".join(names)


def catalog_cli_for_phase(limit: int = 24) -> str:
    """Return enabled catalog commands for the current kill-chain phase.

    The operator's verb catalog is the routing truth, so the planner
    prompt only advertises commands the catalog lets the loop execute.
    The current phase comes from the canonical kill chain; a missing
    catalog view degrades to an empty string so the prompt never hands
    the planner a command the loop cannot route (fail closed).

    Args:
        limit: Maximum commands included in one line.

    Returns:
        Comma-separated enabled command names, empty when the view or
        the phase is unavailable.
    """
    try:
        from modules.killchain import KillChain
        from modules.verb_catalog import entries

        phase = str(KillChain.current_phase() or "").strip().lower()
        view = entries()
        names = [
            name
            for name, row in view.items()
            if bool(row.get("enabled")) and str(row.get("phase") or "") == phase
        ]
        if not names:
            names = [name for name, row in view.items() if bool(row.get("enabled"))]
        return ", ".join(names[: max(1, int(limit or 24))])
    except Exception:
        return ""


def full_cli_enabled() -> bool:
    """Return whether the loop may route any CLI verb.

    Reads ``payload.json`` -> ``orchestrator`` -> ``full_cli``. Any load
    failure falls back to the default so a broken payload never widens
    the loop silently in the wrong direction.
    """
    try:
        from core.config import load_payload

        payload = load_payload() or {}
    except Exception:
        return FULL_CLI_DEFAULT
    try:
        section = payload.get("orchestrator") or {}
        value = section.get("full_cli")
    except AttributeError:
        return FULL_CLI_DEFAULT
    if value is None:
        return FULL_CLI_DEFAULT
    return bool(value)


def set_full_cli(enabled: bool) -> bool:
    """Persist the full-CLI routing flag and return the new value.

    Args:
        enabled: New flag value.

    Returns:
        Stored value after persisting.
    """
    from core.config import load_payload, save_payload

    payload = dict(load_payload() or {})
    section = dict(payload.get("orchestrator") or {})
    section["full_cli"] = bool(enabled)
    payload["orchestrator"] = section
    save_payload(payload)
    with _CACHE_LOCK:
        _CACHE["at"] = 0.0
    return bool(enabled)


__all__ = [
    "FULL_CLI_DEFAULT",
    "build_cli_command",
    "cli_catalog_for_phase",
    "cli_verbs",
    "full_cli_enabled",
    "is_cli_verb",
    "needs_target_for",
    "phase_for",
    "risk_for",
    "search_cli_verbs",
    "set_full_cli",
]
