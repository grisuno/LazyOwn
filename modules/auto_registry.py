"""Registry of loop-ready automation verbs (the ``auto_*`` family plus
read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).

Every entry is a LazyOwn shell command that is already fully automated
(``auto_pwn``, ``autopivot``, ``automsf``, ``autoblody``,
``auto_populate``, ``pyautomate`` — the ``pwntomate`` engine underneath).
The autonomous loop consults this registry in two places:

- planning: :func:`propose_intents` turns scope + goal keywords into
  ``auto <verb>`` intents the planner can claim like any other intent;
- execution: :func:`steps_for` translates those intents back into the
  concrete shell command line, and :func:`execute_shell_verb` runs shell
  verbs with captured output inside the loop executor.

Stdlib only: ``lazy_loop`` may import this without dependency cycles.
"""

from __future__ import annotations

import contextlib
import io
import os
import queue
import re
import shlex
import shutil
import signal
import subprocess
import threading
from dataclasses import dataclass

DEFAULT_SHELL_TIMEOUT_SEC = 600.0

AUTO_VERB_PARAMS_LOCK = threading.Lock()


def _looks_like_target(value: str) -> bool:
    """Check whether a token is a plausible network target.

    Args:
        value: Raw command token.

    Returns:
        True for IPv4/IPv6 addresses, CIDR ranges, and hostnames.
    """
    import ipaddress
    import re

    if not value or value.startswith("-"):
        return False
    host = value.split("/")[0]
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass
    if "/" in value:
        try:
            ipaddress.ip_network(value, strict=False)
            return True
        except ValueError:
            return False
    return bool(re.match(r"^(?=.{1,253}$)[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$", value))


def auto_verb_target(command: str) -> str:
    """Return the target an ``auto <verb> <target>`` line carries, else ''.

    Auto verbs historically read ``payload.json`` (rhost); the loop
    binds each intent to its own target, so the executor overrides the
    payload for the duration of the verb under a lock. Routable verbs
    like ``lazynmap`` carry the target the same way. Subcommand tokens
    such as ``run`` are never targets and yield no override.
    """
    parts = (command or "").strip().split()
    if len(parts) < 2:
        return ""
    candidate = parts[1]
    if candidate.startswith("-"):
        return ""
    if not _looks_like_target(candidate):
        return ""
    first = parts[0]
    entry = _verb_row(first)
    if entry is not None:
        return candidate if entry.needs_target else ""
    if first in ROUTABLE_VERBS:
        return candidate
    try:
        from modules.lazy_cli_bridge import full_cli_enabled, is_cli_verb, needs_target_for

        if full_cli_enabled() and is_cli_verb(first):
            if len(parts) != 2:
                return ""
            return candidate if needs_target_for(first) else ""
    except Exception:
        pass
    return ""


@dataclass(frozen=True)
class AutoVerb:
    """One automation verb the loop may invoke autonomously.

    Args:
        verb: Canonical shell verb (``do_<verb>`` must exist).
        phases: Kill-chain phases this verb serves.
        keywords: Intent/goal signals that select this verb.
        needs_target: When True the built line carries the loop target.
        extra_args: Fixed tail args appended after the target.
        description: Human/operators note shown in intent text.
    """

    verb: str
    phases: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    needs_target: bool = True
    extra_args: str = ""
    description: str = ""


AUTO_VERBS: tuple[AutoVerb, ...] = (
    AutoVerb(
        verb="auto_pwn",
        phases=("exploit",),
        keywords=("exploit", "pwn", "gain access", "initial access", "own the", "compromise", "get shell", "foothold"),
        description="full autonomous exploitation chain (recon, scan, exploit)",
    ),
    AutoVerb(
        verb="autopivot",
        phases=("lateral",),
        keywords=("pivot", "tunnel", "socks", "internal network", "lateral"),
        description="auto-detect internal networks and set up pivot tunnels",
    ),
    AutoVerb(
        verb="automsf",
        phases=("exploit", "c2"),
        keywords=("metasploit", "msf", "meterpreter", "listener"),
        needs_target=False,
        extra_args="",
        description="automated Metasploit exploitation and listener setup",
    ),
    AutoVerb(
        verb="autoblody",
        phases=("privesc", "cred"),
        keywords=("privesc", "privilege escalation", "active directory", "domain", "bloody", "dacl", "kerberos"),
        description="automated AD privilege-escalation path finder",
    ),
    AutoVerb(
        verb="auto_populate",
        phases=("recon",),
        keywords=("populate", "world model", "context", "facts about"),
        needs_target=True,
        description="parse the target's nmap XML into payload context",
    ),
    AutoVerb(
        verb="pyautomate",
        phases=("exploit",),
        keywords=("web exploit", "pwntomate", "auto exploit", "mass exploit", "nmap xml"),
        description="pwntomate automated exploitation workflow over nmap XML",
    ),
    AutoVerb(
        verb="exfil_auto",
        phases=("exfil",),
        keywords=("exfil", "exfiltrate", "flag", "root.txt", "user.txt", "sensitive files"),
        needs_target=False,
        description="auto-detect flags and sensitive files, then exfiltrate",
    ),
    AutoVerb(
        verb="atomic_tests",
        phases=("c2",),
        keywords=(
            "atomic test",
            "atomic_tests",
            "adversary emulation",
            "emulate technique",
            "ttp chain",
        ),
        needs_target=False,
        extra_args="--non-interactive",
        description="stage an Atomic Red Team test by MITRE technique ID (read-only staging)",
    ),
    AutoVerb(
        verb="atomic_gen",
        phases=("c2",),
        keywords=("atomic_gen", "generate test script", "stage test script"),
        needs_target=False,
        extra_args="--non-interactive",
        description="generate test + cleanup scripts for a MITRE technique or GUID",
    ),
    AutoVerb(
        verb="apt_playbook",
        phases=("c2",),
        keywords=("apt playbook", "emulate apt", "run playbook", "adversary playbook"),
        needs_target=False,
        extra_args="",
        description="generate an attack plan from a named APT playbook (read-only staging)",
    ),
    AutoVerb(
        verb="apt_chain",
        phases=("recon", "exploit", "c2"),
        keywords=(
            "full apt chain",
            "end-to-end emulation",
            "prove the chain",
            "run everything",
            "apt chain",
        ),
        needs_target=True,
        extra_args="",
        description="one-command full chain: assign, scan, sweep, validate, plan, stage",
    ),
    AutoVerb(
        verb="atomic_shell",
        phases=("exploit", "c2"),
        keywords=(
            "interactive shell",
            "attach shell",
            "drop into shell",
            "spawn shell",
            "open shell",
        ),
        needs_target=True,
        extra_args="",
        description="verify live shell session (interactive REPL only in foreground terminal)",
    ),
    AutoVerb(
        verb="atomic_clean",
        phases=("c2",),
        keywords=(
            "cleanup artefacts",
            "clean up lab",
            "tear down gym",
            "remove lab",
        ),
        needs_target=True,
        extra_args="",
        description="soft-clean target artefacts, or --hard tear down the gym",
    ),
)


def _verb_rows() -> list:
    """Merged auto-verb rows (built-ins + operator overrides) as objects.

    Each row exposes the historical ``AutoVerb`` attributes (``verb``,
    ``phases``, ``keywords``, ``needs_target``, ``extra_args``,
    ``description``) plus ``enabled`` and ``source`` so existing callers
    keep working while the orchestrator config decides what is live.
    """
    from types import SimpleNamespace

    try:
        from modules.orchestrator_config import effective_verbs

        rows = effective_verbs()
    except Exception:
        rows = [
            {
                "name": entry.verb,
                "enabled": True,
                "phases": list(entry.phases),
                "keywords": list(entry.keywords),
                "needs_target": entry.needs_target,
                "extra_args": entry.extra_args,
                "description": entry.description,
                "source": "builtin",
            }
            for entry in AUTO_VERBS
        ]
    return [
        SimpleNamespace(
            verb=str(row.get("name", "")),
            enabled=bool(row.get("enabled", True)),
            phases=tuple(row.get("phases") or ()),
            keywords=tuple(row.get("keywords") or ()),
            needs_target=bool(row.get("needs_target", True)),
            extra_args=str(row.get("extra_args") or ""),
            description=str(row.get("description") or ""),
            source=str(row.get("source", "builtin")),
        )
        for row in rows
        if str(row.get("name", "")).strip()
    ]


def _verb_row(name: str):
    """Return one merged auto-verb row by name, or None."""
    wanted = str(name or "").strip()
    for row in _verb_rows():
        if row.verb == wanted:
            return row
    return None


def verb_enabled(name: str) -> bool:
    """Return whether one auto verb may be proposed or executed."""
    row = _verb_row(name)
    return bool(row and row.enabled)


REQUIRED_BINARIES: dict[str, tuple[str, ...]] = {
    "automsf": ("msfconsole",),
}

ALTERNATIVE_BINARIES: dict[str, tuple[str, ...]] = {
    "autopivot": ("chisel", "ssh", "socat"),
}

BINARY_EXEMPT = frozenset(
    {
        "echo",
        "cd",
        "export",
        "true",
        "false",
        "test",
        "sleep",
        "cat",
        "grep",
        "awk",
        "sed",
        "head",
        "tail",
        "sort",
        "uniq",
        "wc",
        "tr",
        "cut",
        "xargs",
        "bash",
        "sh",
        "zsh",
        "env",
        "nohup",
        "tee",
        "which",
        "find",
        "ls",
        "mkdir",
        "rm",
        "cp",
        "mv",
        "chmod",
        "touch",
        "whoami",
        "id",
        "ps",
        "kill",
        "sudo",
        "python",
        "python3",
        "pip",
        "pip3",
        "timeout",
        "date",
        "printf",
        "set",
    }
)

SCRIPT_SUFFIXES = (".py", ".sh", ".rb", ".pl", ".js")

SHELL_TIMEOUT_MESSAGE = "TIMEOUT"

ROUTABLE_PREFIXES = ("lazy_addon ", "custom tool ", "lazy_workspace ")

ROUTABLE_VERBS = frozenset({"lazynmap"})

ADDON_TRIGGER_CAP = 4

_SERVICE_ALIASES: dict[str, tuple[str, ...]] = {
    "ssl": ("https",),
    "https": ("ssl",),
    "microsoft-ds": ("smb",),
    "smb": ("microsoft-ds", "netbios-ssn"),
    "netbios-ssn": ("smb",),
}


def _repo_base():
    """Return repository root without importing engine modules."""
    from pathlib import Path as _Path

    return _Path(__file__).resolve().parent.parent


def binary_available(name: str) -> bool:
    """Return True when a command token can actually execute here.

    Shell builtins, repo-local scripts and explicit paths pass so the
    check only flags standalone offensive tools missing from ``PATH``.
    """
    token = (name or "").strip()
    if not token:
        return True
    if token in BINARY_EXEMPT or token.endswith(SCRIPT_SUFFIXES):
        return True
    if "/" in token or "=" in token or token.startswith("-"):
        return True
    return shutil.which(token) is not None


def missing_binary(command: str) -> str:
    """Return the first binary a shell command needs but PATH lacks."""
    try:
        parts = shlex.split(command or "")
    except ValueError:
        return ""
    if not parts:
        return ""
    token = parts[0]
    return "" if binary_available(token) else token


def verb_gap(verb: str) -> str:
    """Return a human reason when an automation verb cannot run, else ''."""
    name = (verb or "").strip()
    missing = [tool for tool in REQUIRED_BINARIES.get(name, ()) if not binary_available(tool)]
    if missing:
        return f"missing tool(s): {', '.join(missing)}"
    alternatives = ALTERNATIVE_BINARIES.get(name, ())
    if alternatives and not any(binary_available(tool) for tool in alternatives):
        return f"no pivot tool installed (need one of: {', '.join(alternatives)})"
    return ""


def verb_available(verb: str) -> bool:
    """Return True when every binary an automation verb needs is installed."""
    return not verb_gap(verb)


def service_tokens(service_text: str) -> set[str]:
    """Normalize a service asset value into matchable tokens."""
    import re as _re

    tokens = set(_re.findall(r"[a-z0-9]+", (service_text or "").lower()))
    for token in list(tokens):
        for alias in _SERVICE_ALIASES.get(token, ()):
            tokens.add(alias)
    return tokens


def _parse_trigger_lines(lines: list[str], start: int) -> tuple[list[str], int]:
    """Parse a YAML trigger value starting at line index.

    Handles inline ``[a, b]`` / ``["a"]`` / scalar forms plus dash
    lists on the following lines. Returns tokens and next index.
    """
    import re as _re

    head = lines[start].split(":", 1)[1].strip() if ":" in lines[start] else ""
    if head.startswith("["):
        inner = head[1 : head.find("]") + 1 if "]" in head else len(head)]
        inner = inner.strip("[]")
        return [t.strip().strip("\"'").lower() for t in inner.split(",") if t.strip().strip("\"'")], start + 1
    if head and not head.startswith("-"):
        return [head.strip().strip("\"'").lower()], start + 1
    tokens: list[str] = []
    idx = start if not head else start
    if head.startswith("-"):
        tokens.append(head[1:].strip().strip("\"'").lower())
        idx = start + 1
    else:
        idx = start + 1
    while idx < len(lines):
        match = _re.match(r"\s*-\s*(\S+)", lines[idx])
        if not match:
            break
        tokens.append(match.group(1).strip().strip("\"'").lower())
        idx += 1
    return [t for t in tokens if t], idx


def iter_addon_triggers() -> list[tuple[str, list[str]]]:
    """Scan enabled lazyaddons for (name, trigger tokens) pairs."""
    import re as _re

    out: list[tuple[str, list[str]]] = []
    try:
        paths = sorted(_repo_base().joinpath("lazyaddons").glob("*.yaml"))
    except OSError:
        return out
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        name = path.stem
        enabled = True
        triggers: list[str] = []
        idx = 0
        while idx < len(lines):
            stripped = lines[idx].strip()
            name_match = _re.match(r"name\s*:\s*(.+)", stripped)
            if name_match and not triggers:
                name = name_match.group(1).strip().strip("\"'")
            enabled_match = _re.match(r"enabled\s*:\s*(.+)", stripped, _re.IGNORECASE)
            if enabled_match:
                enabled = enabled_match.group(1).strip().lower() not in ("false", "no", "0", "off")
            if _re.match(r"trigger\s*:", stripped):
                parsed, idx = _parse_trigger_lines(lines, idx)
                triggers = parsed
                continue
            idx += 1
        if enabled and triggers:
            out.append((name, triggers))
    return out


def iter_tool_triggers() -> list[tuple[str, list[str]]]:
    """Scan active pwntomate tools for (toolname, trigger tokens) pairs."""
    import json as _json

    out: list[tuple[str, list[str]]] = []
    try:
        paths = sorted(_repo_base().joinpath("tools").glob("*.tool"))
    except OSError:
        return out
    for path in paths:
        try:
            data = _json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict) or not data.get("active", False):
            continue
        raw = data.get("trigger", [])
        tokens = [str(t).strip().lower() for t in (raw if isinstance(raw, list) else [raw]) if str(t).strip()]
        if tokens:
            out.append((str(data.get("toolname", path.stem)), tokens))
    return out


def addon_hits_for(service_text: str, limit: int = 50) -> list[tuple[str, str]]:
    """Rank addon/tool names matching one service value.

    Specific trigger matches rank before ``all`` wildcards so generic
    packs never crowd out service-tailored modules.
    """
    tokens = service_tokens(service_text)
    specific: list[tuple[str, str]] = []
    generic: list[tuple[str, str]] = []
    for name, triggers in iter_addon_triggers():
        lowered = [t.lower() for t in triggers]
        if "all" in lowered:
            generic.append((name, "lazyaddon"))
        elif any(t in tokens for t in lowered):
            specific.append((name, "lazyaddon"))
    for toolname, triggers in iter_tool_triggers():
        lowered = [t.lower() for t in triggers]
        if "all" in lowered:
            generic.append((toolname, "tool"))
        elif any(t in tokens for t in lowered):
            specific.append((toolname, "tool"))
    specific.sort()
    generic.sort()
    return (specific + generic)[: max(1, limit)]


def propose_addon_intents(service_texts: list[str], target: str = "", limit: int = ADDON_TRIGGER_CAP) -> list[str]:
    """Propose addon intents for discovered services.

    Lazyaddons run one-to-one via ``lazy addon <name>``; pwntomate tool
    hits collapse into a single ``auto pyautomate`` intent since tools
    only execute as a batch over nmap XML.
    """
    seen: list[str] = []
    tool_hit = False
    for service in service_texts or []:
        for name, source in addon_hits_for(service, limit=limit):
            if source == "tool":
                tool_hit = True
                continue
            line = f"lazy addon {name} {(target or '').strip()}".strip()
            if line not in seen:
                seen.append(line)
            if len(seen) >= max(1, limit):
                return seen
    if tool_hit:
        line = f"auto pyautomate {(target or '').strip()}".strip()
        if line not in seen and len(seen) < max(1, limit):
            seen.append(line)
    return seen


def is_routable_command(line: str) -> bool:
    """Return True when the loop executor must route via the shell."""
    text = (line or "").strip()
    if is_shell_verb(text):
        return True
    first = text.split(maxsplit=1)[0] if text else ""
    if first in ROUTABLE_VERBS:
        return True
    try:
        from modules.lazy_cli_bridge import full_cli_enabled, is_cli_verb

        if full_cli_enabled() and is_cli_verb(first):
            return True
    except Exception:
        pass
    return any(text.startswith(prefix) for prefix in ROUTABLE_PREFIXES)


def verbs() -> tuple[str, ...]:
    """Return every canonical automation verb name."""
    return tuple(row.verb for row in _verb_rows())


def is_shell_verb(token: str) -> bool:
    """Return True when ``token`` names a loop-routable shell verb.

    Built-in auto verbs always route. When full-CLI mode is enabled any
    real ``do_<verb>`` shell command routes as well, so the loop reaches
    the whole cmd2 surface through the same Guard and scope path.
    """
    parts = (token or "").strip().split(maxsplit=1)
    if not parts:
        return False
    if _verb_row(parts[0]) is not None:
        return True
    try:
        from modules.lazy_cli_bridge import full_cli_enabled, is_cli_verb

        if full_cli_enabled() and is_cli_verb(parts[0]):
            return True
    except Exception:
        pass
    return False


def build_command(verb: str, target: str = "") -> str:
    """Build the shell command line for ``verb`` bound to ``target``."""
    entry = _verb_row((verb or "").strip())
    if entry is None:
        raise KeyError(f"unknown automation verb: {verb!r}")
    tail = entry.extra_args.strip()
    if entry.needs_target and (target or "").strip():
        tail = f"{(target or '').strip()} {tail}".strip()
    return f"{entry.verb} {tail}".strip() if tail else entry.verb


def verbs_for(text: str) -> list:
    """Return enabled verbs whose keywords appear in the text."""
    lowered = (text or "").lower()
    return [row for row in _verb_rows() if row.enabled and any(keyword in lowered for keyword in row.keywords)]


def propose_intents(goal: str, target: str = "", finding_texts: tuple[str, ...] = ()) -> list[str]:
    """Propose ``auto <verb>`` intent summaries for planner candidates.

    Verbs whose required binaries are not installed are skipped so the
    planner never dispatches work this host cannot execute.
    """
    seen: list[str] = []
    blob = " ".join([goal or "", target or "", *finding_texts])
    for entry in verbs_for(blob):
        if verb_gap(entry.verb):
            continue
        line = f"auto {entry.verb} {target}".strip() if entry.needs_target else f"auto {entry.verb}"
        if line not in seen:
            seen.append(line)
    return seen


_ATOMIC_VERBS = frozenset({"atomic_tests", "atomic_gen"})
_TECHNIQUE_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b", re.IGNORECASE)
_PLATFORM_RE = re.compile(r"\b(windows|linux|macos)\b", re.IGNORECASE)
_PLAYBOOK_RE = re.compile(r"\b([a-z][a-z0-9_-]{1,40})\s+playbook\b", re.IGNORECASE)


def _atomic_steps(verb: str, text: str) -> list[str] | None:
    """Build a non-interactive atomic staging line from intent text.

    Extracts the first MITRE technique ID (``T1059.001``) and an
    optional platform; always appends ``--non-interactive`` so loop
    workers never block on ``input()``. Returns None when the intent
    names no technique (caller keeps its default probes).
    """
    match = _TECHNIQUE_RE.search(text or "")
    if not match:
        return None
    technique = match.group(0).upper()
    platform = _PLATFORM_RE.search(text or "")
    tail = technique
    if platform:
        tail += f" --platform {platform.group(1).lower()}"
    return [f"{verb} {tail} --non-interactive"]


def _playbook_steps(text: str) -> list[str] | None:
    """Build an apt_playbook staging line from intent text.
    Extracts ``<name> playbook`` (e.g. "emulate the rocke playbook").
    Read-only: generates the attack plan, never executes it.
    Returns None when no playbook name is present.
    """
    match = _PLAYBOOK_RE.search(text or "")
    if not match:
        return None
    name = match.group(1).lower()
    if name in ("apt", "the", "an", "a"):
        return None
    return [f"apt_playbook run {name}"]


def _apt_chain_steps(embedded: str, target: str, strict: bool = False) -> list[str]:
    """Build the one-line apt_chain invocation from intent fragments.

    The heavy lifting lives in the ``apt_chain`` shell command itself
    (assign, scan, sweep, validate, plan, stage); here we only bind the
    playbook name and the target. Defaults: playbook ``rocke``.

    In ``strict`` mode (explicit ``auto apt_chain ...`` form) a lone
    word binds the playbook. In free-text mode only the ``<name>
    playbook`` form binds it, so sentence filler never becomes a
    playbook name; explicit IPs always win over the ambient target.
    """
    playbook = "rocke"
    chained = (target or "").strip()
    tokens = [t for t in (embedded or "").split() if not t.startswith("-")]
    for token in tokens:
        if re.match(r"^[\d.:]+$", token) or ("." in token and _looks_like_target(token)):
            chained = token
        elif strict and playbook == "rocke":
            playbook = token.lower()
    if not strict:
        planned = _playbook_steps(embedded or "")
        if planned:
            playbook = planned[0].split()[-1]
    line = f"apt_chain {playbook}" + (f" {chained}" if chained else "")
    return [line]


def steps_for(text: str, target: str = "") -> list[str] | None:
    """Translate an intent summary into shell command lines, or None.

    Handles the explicit ``auto <verb>`` form, the ``lazy addon <name>``
    form from service-trigger matching, plus the implicit keyword
    signals for exploit/pivot/privesc/msf/populate work. Returns None
    when the intent carries no automation signal (caller keeps its
    default bash probes) or when the verb's tooling is unavailable.
    """
    lowered = (text or "").strip().lower()
    if lowered.startswith("auto "):
        parts = lowered.split()
        verb = parts[1] if len(parts) > 1 else ""
        if _verb_row(verb) is not None:
            if verb_gap(verb) or not verb_enabled(verb):
                return None
            if verb == "automsf":
                import re as _re

                match = _re.search(r"\b(?:exploit|auxiliary|post|payload)/[\w./-]+", text)
                if not match:
                    return None
                return [f"automsf {match.group(0)}"]
            if verb in _ATOMIC_VERBS:
                return _atomic_steps(verb, text)
            if verb == "apt_chain":
                return _apt_chain_steps(" ".join(parts[2:]), target, strict=True)
            if verb == "apt_playbook":
                planned = _playbook_steps(text)
                if planned is not None:
                    return planned
                embedded_pb = " ".join(parts[2:]).strip()
                if embedded_pb:
                    return [f"apt_playbook {embedded_pb}"]
                return None
            embedded = " ".join(parts[2:]).strip()
            return [build_command(verb, target or embedded)]
        return None
    if lowered.startswith("lazy addon "):
        parts = (text or "").strip().split()
        name = parts[2] if len(parts) > 2 else ""
        if not name:
            return None
        embedded = " ".join(parts[3:]).strip()
        tail = (target or embedded or "").strip()
        suffix = f" --target {tail}" if tail else ""
        return [f"lazy_addon run {name}{suffix}".strip()]
    if lowered.startswith("install capability "):
        try:
            from modules.lazy_installer import steps_for_install as _install_steps

            return _install_steps(text)
        except Exception:
            return None
    matched = [entry for entry in verbs_for(lowered) if not verb_gap(entry.verb)]
    planned_kw = _playbook_steps(text)
    if planned_kw is not None and not any(e.verb == "apt_chain" for e in verbs_for(lowered)):
        return planned_kw
    if matched:
        if matched[0].verb == "apt_chain":
            return _apt_chain_steps(text, target)
        if matched[0].verb in _ATOMIC_VERBS:
            return _atomic_steps(matched[0].verb, text)
        if matched[0].verb == "apt_playbook":
            planned = _playbook_steps(text)
            if planned is not None:
                return planned
            return None
        try:
            from modules.lazy_orchestrator_feedback import rank_verbs

            order = rank_verbs(matched[0].phases[0] if matched[0].phases else "", [e.verb for e in matched])
            matched.sort(key=lambda e: order.index(e.verb) if e.verb in order else len(order))
        except Exception:
            pass
        return [build_command(matched[0].verb, target)]
    if verbs_for(lowered):
        return None
    try:
        from modules.lazy_cli_bridge import (
            build_cli_command,
            full_cli_enabled,
            is_cli_verb,
            phase_for,
        )
        from modules.orchestrator_config import verb_config as _verb_cfg

        if full_cli_enabled():
            raw_parts = (text or "").strip().split()
            head = raw_parts[0].lower() if raw_parts else ""
            if head and is_cli_verb(head):
                cfg = _verb_cfg(head)
                if cfg is None or cfg.get("enabled", True):
                    tail = " ".join(raw_parts[1:]).strip() or (target or "").strip()
                    return [build_cli_command(head, tail)]
            for token in lowered.split():
                if is_cli_verb(token):
                    cfg = _verb_cfg(token)
                    if cfg is not None and not cfg.get("enabled", True):
                        continue
                    _ = phase_for(token)
                    return [build_cli_command(token, target)]
    except Exception:
        pass
    return None


@dataclass
class ShellResult:
    """Captured outcome of one shell-verb execution."""

    output: str = ""
    timed_out: bool = False


class _TeeCapture(io.StringIO):
    """StringIO that forwards every write chunk to an observer.

    The observer frequently prints (progress panels, streamers) and it
    runs while ``stdout`` is redirected to *this* buffer, so an observer
    printing to stdout would recurse into ``write`` forever. A per-thread
    reentrancy flag stops the cycle: nested writes still land in the
    buffer, but the observer is only invoked on the outermost write.
    """

    def __init__(self, observer=None) -> None:
        super().__init__()
        self._observer = observer
        self._local = threading.local()

    def write(self, data: str) -> int:
        """Capture text and stream the chunk to the observer once."""
        if self._observer is not None and not getattr(self._local, "in_observer", False):
            self._local.in_observer = True
            try:
                self._observer(str(data))
            except Exception:
                pass
            finally:
                self._local.in_observer = False
        return super().write(data)


def execute_shell_verb(
    shell: object, command: str, timeout_sec: float = DEFAULT_SHELL_TIMEOUT_SEC, on_output=None
) -> str:
    """Run a LazyOwn shell verb capturing stdout, with a hard timeout.

    Uses the same redirect+thread pattern as the agent runner: the verb
    runs off-thread so a hanging automation (listener, prompt) cannot
    wedge the loop. Never raises; timeouts report as text the loop can
    record as a fact like any other transcript.

    Args:
        shell: Live LazyOwn shell.
        command: Routable shell verb line.
        timeout_sec: Hard timeout for the background verb.
        on_output: Optional callback receiving output chunks live so the
            operator watches colored tool output while it runs.
    """
    if shell is None:
        return "execution failed: no shell context for automation verb"
    if not is_routable_command(command):
        return f"execution failed: not an automation verb: {command[:80]}"
    results: queue.Queue = queue.Queue()

    def _invoke() -> None:
        with contextlib.redirect_stdout(capture):
            if hasattr(shell, "onecmd_plus_hooks"):
                shell.onecmd_plus_hooks(command)
            elif hasattr(shell, "onecmd"):
                shell.onecmd(command)
            else:
                print("Error: shell has no onecmd method")

    capture = _TeeCapture(on_output)

    def _target() -> None:
        verb_target = auto_verb_target(command)
        try:
            import modules.command_executor as _command_executor
        except Exception:
            _command_executor = None
        if _command_executor is not None:
            try:
                _command_executor.set_thread_timeout(timeout_sec)
                _command_executor.set_thread_stdin_devnull(True)
            except Exception:
                pass
        try:
            if verb_target and hasattr(shell, "params"):
                with AUTO_VERB_PARAMS_LOCK:
                    params = shell.params
                    previous = params.get("rhost")
                    if str(previous or "") != verb_target:
                        print(f"[*] auto verb target override: rhost={verb_target} (payload had {previous!r})")
                        params["rhost"] = verb_target
                        try:
                            _invoke()
                        finally:
                            params["rhost"] = previous
                    else:
                        _invoke()
            else:
                _invoke()
            results.put(ShellResult(output=capture.getvalue()))
        except Exception as exc:  # noqa: BLE001 - surfaced as transcript text
            results.put(ShellResult(output=f"Error executing automation verb: {exc}"))
        finally:
            if _command_executor is not None:
                try:
                    _command_executor.clear_thread_timeout()
                    _command_executor.clear_thread_stdin_devnull()
                except Exception:
                    pass

    worker = threading.Thread(target=_target, daemon=True)
    worker.start()
    worker.join(timeout=max(1.0, float(timeout_sec or DEFAULT_SHELL_TIMEOUT_SEC)))
    if worker.is_alive():
        try:
            partial = capture.getvalue() or ""
        except Exception:
            partial = ""
        tail = f"\n[partial output, {len(partial)} chars]\n{partial[-1500:]}" if partial.strip() else ""
        return (
            f"{SHELL_TIMEOUT_MESSAGE}: automation verb exceeded "
            f"{timeout_sec}s and is still running in the background: "
            f"{command[:120]}{tail}"
        )
    try:
        result = results.get_nowait()
    except queue.Empty:
        return f"execution failed: automation verb produced no output: {command[:120]}"
    return str(result.output or "")


_ACTIVE_PROCS: set = set()
_ACTIVE_LOCK = threading.Lock()


def _register_process(process) -> None:
    """Track a live streaming process for cancellation."""
    with _ACTIVE_LOCK:
        _ACTIVE_PROCS.add(process)


def _unregister_process(process) -> None:
    """Drop a finished streaming process from the tracker."""
    with _ACTIVE_LOCK:
        _ACTIVE_PROCS.discard(process)


def track_process(process) -> None:
    """Register a live child process for global cancellation."""
    _register_process(process)


def untrack_process(process) -> None:
    """Drop a finished child process from the cancellation registry."""
    _unregister_process(process)


def cancel_running_commands() -> int:
    """Kill every live streaming process group (operator Ctrl+C).

    Returns:
        Number of process groups signalled.
    """
    with _ACTIVE_LOCK:
        processes = list(_ACTIVE_PROCS)
        _ACTIVE_PROCS.clear()
    killed = 0
    for process in processes:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            killed += 1
        except Exception:
            try:
                process.kill()
                killed += 1
            except Exception:
                continue
    return killed


def execute_streaming(command: str, on_output=None, timeout_sec: float = DEFAULT_SHELL_TIMEOUT_SEC) -> str:
    """Run a bash command streaming lines while capturing the output.

    Args:
        command: Shell command line (pipes/redirects allowed, gated by
            the guard, scope and constraint layers before it gets here).
        on_output: Optional callback receiving each output line live.
        timeout_sec: Hard timeout; the process is killed on expiry.

    Returns:
        Full captured output, or a TIMEOUT/error transcript line.
    """
    if not (command or "").strip():
        return ""
    try:
        process = subprocess.Popen(  # noqa: S602 - loop commands are guard-gated
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            errors="replace",
            start_new_session=True,
        )
    except OSError as exc:
        return f"execution failed: {exc}"
    _register_process(process)
    chunks: list[str] = []
    timed_out = {"flag": False}

    def _kill() -> None:
        timed_out["flag"] = True
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass

    watchdog = threading.Timer(max(1.0, float(timeout_sec or DEFAULT_SHELL_TIMEOUT_SEC)), _kill)
    watchdog.daemon = True
    watchdog.start()
    try:
        if process.stdout is not None:
            for line in iter(process.stdout.readline, ""):
                chunks.append(line)
                if on_output is not None:
                    try:
                        on_output(line.rstrip("\n"))
                    except Exception:
                        pass
        process.wait(timeout=max(1.0, float(timeout_sec or DEFAULT_SHELL_TIMEOUT_SEC)))
    except subprocess.TimeoutExpired:
        _kill()
    except Exception as exc:
        _kill()
        return f"execution failed: {exc}"
    finally:
        watchdog.cancel()
        _unregister_process(process)
        try:
            if process.stdout is not None:
                process.stdout.close()
        except Exception:
            pass
    if timed_out["flag"]:
        return f"{SHELL_TIMEOUT_MESSAGE}: command exceeded {int(timeout_sec)}s: {command[:120]}"
    return "".join(chunks)


__all__ = [
    "verb_enabled",
    "ALTERNATIVE_BINARIES",
    "AUTO_VERBS",
    "ADDON_TRIGGER_CAP",
    "DEFAULT_SHELL_TIMEOUT_SEC",
    "REQUIRED_BINARIES",
    "ROUTABLE_PREFIXES",
    "ROUTABLE_VERBS",
    "AutoVerb",
    "ShellResult",
    "addon_hits_for",
    "binary_available",
    "build_command",
    "cancel_running_commands",
    "execute_shell_verb",
    "execute_streaming",
    "is_routable_command",
    "is_shell_verb",
    "iter_addon_triggers",
    "iter_tool_triggers",
    "missing_binary",
    "propose_addon_intents",
    "propose_intents",
    "service_tokens",
    "steps_for",
    "track_process",
    "untrack_process",
    "verb_available",
    "verb_gap",
    "verbs",
    "verbs_for",
]
