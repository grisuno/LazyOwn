"""Registry of loop-ready automation verbs (the ``auto_*`` family).

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
import queue
import threading
from dataclasses import dataclass

DEFAULT_SHELL_TIMEOUT_SEC = 600.0


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
        keywords=("exploit", "pwn", "gain access", "initial access", "own the",
                  "compromise", "get shell", "foothold"),
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
        extra_args="",
        description="automated Metasploit exploitation and listener setup",
    ),
    AutoVerb(
        verb="autoblody",
        phases=("privesc", "cred"),
        keywords=("privesc", "privilege escalation", "active directory",
                  "domain", "bloody", "dacl", "kerberos"),
        description="automated AD privilege-escalation path finder",
    ),
    AutoVerb(
        verb="auto_populate",
        phases=("recon",),
        keywords=("populate", "world model", "context", "facts about"),
        needs_target=False,
        description="parse latest nmap XML into payload context",
    ),
    AutoVerb(
        verb="pyautomate",
        phases=("exploit",),
        keywords=("web exploit", "pwntomate", "auto exploit", "mass exploit",
                  "nmap xml"),
        description="pwntomate automated exploitation workflow over nmap XML",
    ),
)

_VERB_BY_NAME = {entry.verb: entry for entry in AUTO_VERBS}

SHELL_TIMEOUT_MESSAGE = "TIMEOUT"


def verbs() -> tuple[str, ...]:
    """Return every canonical automation verb name."""
    return tuple(entry.verb for entry in AUTO_VERBS)


def is_shell_verb(token: str) -> bool:
    """Return True when ``token`` names a loop-routable shell verb."""
    parts = (token or "").strip().split(maxsplit=1)
    return bool(parts) and parts[0] in _VERB_BY_NAME


def build_command(verb: str, target: str = "") -> str:
    """Build the shell command line for ``verb`` bound to ``target``."""
    entry = _VERB_BY_NAME.get((verb or "").strip())
    if entry is None:
        raise KeyError(f"unknown automation verb: {verb!r}")
    tail = entry.extra_args.strip()
    if entry.needs_target and (target or "").strip():
        tail = f"{(target or '').strip()} {tail}".strip()
    return f"{entry.verb} {tail}".strip() if tail else entry.verb


def verbs_for(text: str) -> list[AutoVerb]:
    """Return verbs whose keywords appear in ``text`` (goal/intent/finding)."""
    lowered = (text or "").lower()
    return [entry for entry in AUTO_VERBS
            if any(keyword in lowered for keyword in entry.keywords)]


def propose_intents(goal: str, target: str = "",
                    finding_texts: tuple[str, ...] = ()) -> list[str]:
    """Propose ``auto <verb>`` intent summaries for planner candidates."""
    seen: list[str] = []
    blob = " ".join([goal or "", target or "", *finding_texts])
    for entry in verbs_for(blob):
        line = f"auto {entry.verb} {target}".strip() if entry.needs_target else f"auto {entry.verb}"
        if line not in seen:
            seen.append(line)
    return seen


def steps_for(text: str, target: str = "") -> list[str] | None:
    """Translate an intent summary into shell command lines, or None.

    Handles the explicit ``auto <verb>`` form plus the implicit keyword
    signals for exploit/pivot/privesc/msf/populate work. Returns None
    when the intent carries no automation signal (caller keeps its
    default bash probes).
    """
    lowered = (text or "").strip().lower()
    if lowered.startswith("auto "):
        parts = lowered.split()
        verb = parts[1] if len(parts) > 1 else ""
        if verb in _VERB_BY_NAME:
            embedded = " ".join(parts[2:]).strip()
            return [build_command(verb, target or embedded)]
        return None
    matched = verbs_for(lowered)
    if not matched:
        return None
    return [build_command(matched[0].verb, target)]


@dataclass
class ShellResult:
    """Captured outcome of one shell-verb execution."""

    output: str = ""
    timed_out: bool = False


def execute_shell_verb(shell: object, command: str,
                       timeout_sec: float = DEFAULT_SHELL_TIMEOUT_SEC) -> str:
    """Run a LazyOwn shell verb capturing stdout, with a hard timeout.

    Uses the same redirect+thread pattern as the agent runner: the verb
    runs off-thread so a hanging automation (listener, prompt) cannot
    wedge the loop. Never raises; timeouts report as text the loop can
    record as a fact like any other transcript.
    """
    if shell is None:
        return "execution failed: no shell context for automation verb"
    if not is_shell_verb(command):
        return f"execution failed: not an automation verb: {command[:80]}"
    results: queue.Queue = queue.Queue()

    def _target() -> None:
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                if hasattr(shell, "onecmd_plus_hooks"):
                    shell.onecmd_plus_hooks(command)
                elif hasattr(shell, "onecmd"):
                    shell.onecmd(command)
                else:
                    print("Error: shell has no onecmd method")
            results.put(ShellResult(output=capture.getvalue()))
        except Exception as exc:  # noqa: BLE001 - surfaced as transcript text
            results.put(ShellResult(output=f"Error executing automation verb: {exc}"))

    worker = threading.Thread(target=_target, daemon=True)
    worker.start()
    worker.join(timeout=max(1.0, float(timeout_sec or DEFAULT_SHELL_TIMEOUT_SEC)))
    if worker.is_alive():
        return (f"{SHELL_TIMEOUT_MESSAGE}: automation verb exceeded "
                f"{timeout_sec}s and is still running in the background: "
                f"{command[:120]}")
    try:
        result = results.get_nowait()
    except queue.Empty:
        return f"execution failed: automation verb produced no output: {command[:120]}"
    return str(result.output or "")


__all__ = [
    "AUTO_VERBS",
    "DEFAULT_SHELL_TIMEOUT_SEC",
    "AutoVerb",
    "ShellResult",
    "build_command",
    "execute_shell_verb",
    "is_shell_verb",
    "propose_intents",
    "steps_for",
    "verbs",
    "verbs_for",
]
