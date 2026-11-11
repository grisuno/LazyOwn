"""Seeded guard rules that arm the planner filter before any attribution data.

Failure attribution only demotes a verb after the target has already refused it
several times, so the first rounds of a loop re-propose known-unsafe commands
until the evidence accrues. This store seeds the planner's filter from round
zero with a persisted baseline of rules an unattended loop must never emit
regardless of attribution: destructive-to-self commands that would wreck the
operator host or the engagement.

The baseline is a built-in safety floor merged with an operator override from
``payload.json:loop_guard_rules`` and persisted once to
``sessions/guard_rules_<task>.json`` so it is visible and auditable. Rules come
in two shapes: verbs demoted outright, and case-insensitive substrings that
block a whole command line. Every read fails open to the built-in floor, never
an empty set, so a malformed override can only ever add safety, not remove it.
Nothing here imports the loop runtime, keeping the module cycle-free.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent
_DIRECTORY_MODE = 0o700

_DEFAULT_VERBS: tuple[str, ...] = (
    "shutdown",
    "reboot",
    "halt",
    "poweroff",
    "mkfs",
)

_DEFAULT_PATTERNS: tuple[str, ...] = (
    "rm -rf /",
    "rm -rf /*",
    ":(){",
    "dd of=/dev/sd",
    "dd of=/dev/nvme",
    "mkfs.",
    "> /dev/sda",
    "wipefs",
)


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
            return {"verbs": [], "patterns": [p.strip() for p in text.split(",") if p.strip()]}
    if isinstance(raw, dict):
        verbs = [str(v).strip().lower() for v in (raw.get("verbs") or []) if str(v).strip()]
        patterns = [str(p).strip().lower() for p in (raw.get("patterns") or []) if str(p).strip()]
        return {"verbs": verbs, "patterns": patterns}
    if isinstance(raw, list):
        return {"verbs": [], "patterns": [str(p).strip().lower() for p in raw if str(p).strip()]}
    return {"verbs": [], "patterns": []}


class GuardRules:
    """Load, persist and query the seeded planner guard rules for a task.

    The ruleset is the built-in floor unioned with the operator override; it is
    written to ``sessions/guard_rules_<task>.json`` on first construction so the
    active rules are inspectable, and is read back from there on later runs.
    """

    def __init__(self, task_id: str = "", base_dir: Path | None = None, override: object | None = None) -> None:
        """Assemble the ruleset and persist it, failing open to the floor.

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
        self._persist()

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

    def _persist(self) -> None:
        """Write the active ruleset to its file, swallowing I/O failure."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.chmod(self._path.parent, _DIRECTORY_MODE)
            except OSError:
                pass
            payload = {
                "verbs": sorted(self._rules["verbs"]),
                "patterns": sorted(self._rules["patterns"]),
            }
            tmp = self._path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            os.replace(tmp, self._path)
        except OSError:
            return

    def blocked_verbs(self) -> set[str]:
        """Return the verbs the planner must never propose for this task."""
        return set(self._rules["verbs"])

    def blocks_command(self, command: str) -> bool:
        """Return True when a command matches a seeded verb or pattern rule.

        Args:
            command: The candidate command line.

        Returns:
            True when the command's leading verb is seeded-blocked or any seeded
            substring pattern appears in it.
        """
        text = str(command or "").strip().lower()
        if not text:
            return False
        verb = os.path.basename(text.split()[0])
        if verb in self._rules["verbs"]:
            return True
        return any(pattern in text for pattern in self._rules["patterns"])


__all__ = ["GuardRules"]
