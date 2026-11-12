"""Seeded guard rules that arm the planner filter before any attribution data.

Failure attribution only demotes a verb after the target has already refused it
several times, so the first rounds of a loop re-propose known-unsafe commands
until the evidence accrues. This store seeds the planner's filter from round
zero with a persisted baseline of rules an unattended loop must never emit
regardless of attribution: destructive-to-self commands that would wreck the
operator host or the engagement.

The baseline is a built-in safety floor merged with an operator override from
``payload.json:loop_guard_rules`` and persisted once to
``sessions/guard_rules_<task>.json`` so it is visible and auditable. Matching
is argv-based, not substring: a command is tokenised, shell and privilege
wrappers (``sudo``, ``env``, ``bash -c`` and friends) are peeled to reach the
real verb, and destructive forms are recognised by structure (recursive-force
``rm`` on a system path, ``dd`` onto a block device) so that ``rm -fr /`` and
``rm --recursive --force /`` are caught as surely as ``rm -rf /``. Every read
fails open to the built-in floor, never an empty set, so a malformed override
can only ever add safety, not remove it. Nothing here imports the loop runtime,
keeping the module cycle-free.
"""

from __future__ import annotations

import json
import os
import shlex
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent

_WRAPPERS: frozenset[str] = frozenset({"sudo", "doas", "env", "nice", "ionice", "timeout", "stdbuf", "nohup", "setsid"})
_SHELL_WRAPPERS: frozenset[str] = frozenset({"bash", "sh", "zsh", "dash", "ash", "ksh"})
_SYSTEM_PATHS: tuple[str, ...] = ("/", "/*", "/bin", "/boot", "/dev", "/etc", "/lib", "/lib64", "/sbin", "/usr", "/var", "/root", "/home")

_DEFAULT_VERBS: tuple[str, ...] = (
    "shutdown",
    "reboot",
    "halt",
    "poweroff",
    "mkfs",
    "wipefs",
    "shred",
)

_DEFAULT_PATTERNS: tuple[str, ...] = (
    ":(){",
    "> /dev/sda",
)

_cache: dict[str, dict[str, set[str]]] = {}


def _default_rules() -> dict[str, list[str]]:
    """Return a fresh copy of the built-in safety floor."""
    return {"verbs": list(_DEFAULT_VERBS), "patterns": list(_DEFAULT_PATTERNS)}


def _parse_override(raw: object) -> dict[str, list[str]]:
    """Parse an operator override into verb and pattern lists.

    The override may be a mapping with ``verbs``/``patterns`` keys, a list
    (treated as patterns), or a comma-separated string (treated as patterns).
    Anything unparseable yields empty lists so it can only add to the floor.

    Args:
        raw: The raw ``loop_guard_rules`` value from config.

    Returns:
        A dict with ``verbs`` and ``patterns`` lists, each possibly empty.
    """
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return {"verbs": [], "patterns": []}
        try:
            raw = json.loads(text)
        except ValueError:
            return {"verbs": [], "patterns": [p.strip().lower() for p in text.split(",") if p.strip()]}
    if isinstance(raw, dict):
        verbs = [str(v).strip().lower() for v in (raw.get("verbs") or []) if str(v).strip()]
        patterns = [str(p).strip().lower() for p in (raw.get("patterns") or []) if str(p).strip()]
        return {"verbs": verbs, "patterns": patterns}
    if isinstance(raw, list):
        return {"verbs": [], "patterns": [str(p).strip().lower() for p in raw if str(p).strip()]}
    return {"verbs": [], "patterns": []}


def _tokenize(command: str) -> list[str]:
    """Split a command into argv, falling back to whitespace on a parse error."""
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def _unwrap(tokens: list[str]) -> list[str]:
    """Peel privilege and shell wrappers to reach the real command argv.

    Leading wrappers (``sudo``, ``env``, ``timeout`` and friends) and their
    option/assignment/numeric arguments are dropped; a shell wrapper with a
    ``-c`` argument is replaced by the argv of that inlined command, recursively.

    Args:
        tokens: The tokenised command line.

    Returns:
        The argv of the effective command, wrappers removed.
    """
    for _ in range(8):
        if not tokens:
            return tokens
        head = os.path.basename(tokens[0])
        if head in _WRAPPERS:
            rest = tokens[1:]
            while rest and (rest[0].startswith("-") or "=" in rest[0] or rest[0].isdigit()):
                rest = rest[1:]
            tokens = rest
            continue
        if head in _SHELL_WRAPPERS and "-c" in tokens[1:]:
            idx = tokens.index("-c", 1)
            if idx + 1 < len(tokens):
                tokens = _tokenize(tokens[idx + 1])
                continue
        return tokens
    return tokens


def _rm_is_destructive(tokens: list[str]) -> bool:
    """Return True for a recursive-force ``rm`` targeting a system path.

    Recursion and force are detected across every flag form (``-rf``, ``-fr``,
    ``-r -f``, ``--recursive --force``), and the command is destructive only
    when an operand is a system path, so a normal ``rm -rf ./build`` is allowed.

    Args:
        tokens: The unwrapped command argv, ``tokens[0]`` being ``rm``.

    Returns:
        True when the command would recursively force-delete a system path.
    """
    recursive = False
    force = False
    operands: list[str] = []
    for token in tokens[1:]:
        if token == "--":
            continue
        if token.startswith("--"):
            if token in ("--recursive",):
                recursive = True
            elif token in ("--force",):
                force = True
            continue
        if token.startswith("-") and len(token) > 1:
            letters = set(token[1:])
            recursive = recursive or bool(letters & {"r", "R"})
            force = force or ("f" in letters)
            continue
        operands.append(token)
    if not recursive:
        return False
    for operand in operands:
        normalized = operand.rstrip("/") or "/"
        if operand in _SYSTEM_PATHS or normalized in _SYSTEM_PATHS:
            return True
    return force and not operands


def _dd_is_destructive(tokens: list[str]) -> bool:
    """Return True for a ``dd`` writing to a block device."""
    return any(token.startswith("of=/dev/") for token in tokens[1:])


class GuardRules:
    """Load, persist and query the seeded planner guard rules for a task.

    The ruleset is the built-in floor unioned with the operator override; it is
    written once to ``sessions/guard_rules_<task>.json`` (and only when its
    content changes) so the active rules are inspectable without rewriting the
    file on every construction.
    """

    def __init__(self, task_id: str = "", base_dir: Path | None = None, override: object | None = None) -> None:
        """Assemble the ruleset and persist it once, failing open to the floor.

        Args:
            task_id: Campaign/task identifier; blank uses a shared file.
            base_dir: Optional directory override for tests.
            override: Explicit override for tests; when None the value is read
                from ``payload.json:loop_guard_rules``.
        """
        root = Path(base_dir) if base_dir is not None else _BASE_DIR / "sessions"
        name = f"guard_rules_{task_id}.json" if task_id else "guard_rules.json"
        self._path = root / name
        self._rules = self._assemble(override)
        self._persist_once()

    def _assemble(self, override: object | None) -> dict[str, set[str]]:
        """Union the built-in floor with the operator override into rule sets."""
        floor = _default_rules()
        if override is None:
            override = self._read_config_override()
        extra = _parse_override(override)
        verbs = {v.lower() for v in floor["verbs"]} | set(extra["verbs"])
        patterns = {p.lower() for p in floor["patterns"]} | set(extra["patterns"])
        return {"verbs": verbs, "patterns": patterns}

    @staticmethod
    def _read_config_override() -> object:
        """Return the raw ``loop_guard_rules`` value, or empty on failure."""
        try:
            from core.config import load_payload

            return (load_payload() or {}).get("loop_guard_rules", "")
        except Exception:
            return ""

    def _serialised(self) -> str:
        """Return the canonical on-disk form of the active ruleset."""
        payload = {"verbs": sorted(self._rules["verbs"]), "patterns": sorted(self._rules["patterns"])}
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)

    def _persist_once(self) -> None:
        """Write the ruleset only when the stored copy differs, under a lock."""
        serialised = self._serialised()
        try:
            if self._path.exists() and self._path.read_text(encoding="utf-8") == serialised:
                return
        except OSError:
            pass
        try:
            from core.atomic_store import write_text_atomic

            write_text_atomic(self._path, serialised)
        except OSError:
            return

    def blocked_verbs(self) -> set[str]:
        """Return the verbs the planner must never propose for this task."""
        return set(self._rules["verbs"])

    def blocks_command(self, command: str) -> bool:
        """Return True when a command is seeded-unsafe for an unattended loop.

        The command is tokenised and unwrapped to its real verb before any
        decision, so privilege and shell wrappers cannot hide a blocked verb.
        A blocked verb, a structurally destructive ``rm`` or ``dd``, or a seeded
        substring pattern each block the command.

        Args:
            command: The candidate command line.

        Returns:
            True when the command matches a seeded verb, a destructive form, or
            a seeded substring pattern.
        """
        text = str(command or "").strip()
        if not text:
            return False
        lowered = " ".join(text.lower().split())
        if any(pattern in lowered for pattern in self._rules["patterns"]):
            return True
        tokens = _unwrap(_tokenize(text))
        if not tokens:
            return False
        verb = os.path.basename(tokens[0]).lower()
        if verb in self._rules["verbs"]:
            return True
        if verb == "rm" and _rm_is_destructive(tokens):
            return True
        return verb == "dd" and _dd_is_destructive(tokens)


def guard_rules(task_id: str = "") -> GuardRules:
    """Return a cached :class:`GuardRules` for a task, built at most once.

    Caching keeps repeated planner rounds from re-reading config and rewriting
    the ruleset file; the first call for a task assembles and persists it, later
    calls reuse the instance.

    Args:
        task_id: Campaign/task identifier.

    Returns:
        The shared guard ruleset for the task.
    """
    key = str(task_id or "")
    cached = _cache.get(key)
    if cached is None:
        instance = GuardRules(task_id)
        _cache[key] = instance._rules
        return instance
    instance = GuardRules.__new__(GuardRules)
    instance._rules = cached
    root = _BASE_DIR / "sessions"
    instance._path = root / (f"guard_rules_{key}.json" if key else "guard_rules.json")
    return instance


__all__ = ["GuardRules", "guard_rules"]
