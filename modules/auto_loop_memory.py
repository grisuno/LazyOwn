"""Persistent memory for the auto loop.

Two stores backed by atomic JSON files under ``sessions/auto_loop``:

- ``FailureMemory``: how many times each (target, category, command)
  combination failed, plus the set of base commands considered blocked
  either because they failed past ``BLOCK_THRESHOLD`` or because the
  stuck-loop detector vetoed them. Survives loop restarts so a command
  that already burned two attempts is not burned again next session.
- ``DecisionPersistence``: reactive-engine decisions that could not be
  consumed in the step that produced them. Written as a backlog and
  drained at the top of the next cascade so expensive findings (e.g. a
  privesc hint) are never dropped when the loop exits mid-step.

Keys are pipe-separated segments (``target|category|command``) because
command strings may contain colons. The command segment stores the exact
string the selector attempted; base-command blocking derives the first
whitespace token from recorded entries.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

_BLOCK_THRESHOLD = 2
_FAILURE_MAX_ENTRIES = 200
_DECISION_MAX_ENTRIES = 64
_ENTRY_KEY = "key"
_ENTRY_COUNT = "count"
_ENTRY_TS = "last_ts"
_ITEMS = "items"
_DECISIONS = "decisions"
_COMMAND = "command"
_REASON = "reason"
_TS = "ts"
_BASE_INDEX = "bases"


@dataclass
class PendingDecision:
    """A reactive-engine decision parked for the next selection cycle."""

    command: str
    reason: str = ""
    ts: int = 0


class FailureMemory:
    """Durable per-target failure counters and blocked base commands."""

    def __init__(self, filepath: str | Path) -> None:
        self._path = Path(filepath)
        self._counts: dict[str, dict[str, object]] = {}
        self._vetoed: dict[str, set[str]] = {}
        self._load()

    @property
    def path(self) -> Path:
        """Backing file path for administrative inspection."""
        return self._path

    @staticmethod
    def make_key(target: str, category: str, command: str) -> str:
        """Build the storage key; raises on empty target or command."""
        if not target or not command:
            raise ValueError("target and command are required")
        return f"{target}|{category}|{command}"

    @staticmethod
    def base_of(command: str) -> str:
        """Extract the base command from a full command string."""
        return command.strip().split()[0] if command.strip() else ""

    def record_failure(self, target: str, category: str, command: str) -> int:
        """Increment and persist the failure count; returns the new count."""
        key = self.make_key(target, category, command)
        entry = self._counts.get(key, {})
        count = int(entry.get(_ENTRY_COUNT, 0)) + 1
        self._counts[key] = {_ENTRY_COUNT: count, _ENTRY_TS: int(time.time())}
        self._trim()
        self.save()
        return count

    def failure_count(self, target: str, category: str, command: str) -> int:
        """Current persisted failure count for the combination."""
        entry = self._counts.get(self.make_key(target, category, command), {})
        return int(entry.get(_ENTRY_COUNT, 0))

    def count_for_base(self, target: str, base_command: str) -> int:
        """Failure hits aggregated across exact keys whose base matches."""
        total = 0
        for key, entry in self._counts.items():
            if not key.startswith(f"{target}|"):
                continue
            base = self.base_of(str(key.split("|", 2)[-1]))
            if base == base_command:
                total += int(entry.get(_ENTRY_COUNT, 0))
        return total

    def veto_base(self, target: str, base_command: str) -> None:
        """Mark a base command as blocked by the stuck-loop detector."""
        if not target or not base_command:
            return
        bases = self._vetoed.setdefault(target, set())
        if base_command in bases:
            return
        bases.add(base_command)
        self.save()

    def is_blocked(self, target: str, base_command: str, bonus_key: str = "") -> bool:
        """True when the base is vetoed or its failure count hit the threshold."""
        if base_command in self._vetoed.get(target, set()):
            return True
        if bonus_key and self.failure_count_strict(target, bonus_key) >= _BLOCK_THRESHOLD:
            return True
        return self.count_for_base(target, base_command) >= _BLOCK_THRESHOLD

    def failure_count_strict(self, target: str, key: str) -> int:
        """Failure count for a raw storage key already containing separators."""
        entry = self._counts.get(key, {})
        return int(entry.get(_ENTRY_COUNT, 0))

    def blocked_bases(self, target: str) -> set[str]:
        """All blocked base commands for the target (vetoed plus past threshold)."""
        bases = set(self._vetoed.get(target, set()))
        totals: dict[str, int] = {}
        for key, entry in self._counts.items():
            if not key.startswith(f"{target}|"):
                continue
            base = self.base_of(str(key.split("|", 2)[-1]))
            totals[base] = totals.get(base, 0) + int(entry.get(_ENTRY_COUNT, 0))
        bases.update(base for base, total in totals.items() if total >= _BLOCK_THRESHOLD)
        return bases

    def clear_target(self, target: str) -> None:
        """Forget every record for a target (manual reset path)."""
        self._counts = {k: v for k, v in self._counts.items() if not k.startswith(f"{target}|")}
        self._vetoed.pop(target, None)
        self.save()

    def sanctioned_bases(self, target: str) -> list[dict[str, object]]:
        """Administrative view: counts above threshold with their last timestamp."""
        rows: list[dict[str, object]] = []
        for key, entry in self._counts.items():
            if not key.startswith(f"{target}|"):
                continue
            count = int(entry.get(_ENTRY_COUNT, 0))
            if count < _BLOCK_THRESHOLD:
                continue
            rows.append({"base": self.base_of(str(key.split("|", 2)[-1])), "count": count, "ts": entry.get(_ENTRY_TS, 0)})
        rows.sort(key=lambda r: int(r["ts"]))
        return rows

    def _trim(self) -> None:
        if len(self._counts) <= _FAILURE_MAX_ENTRIES:
            return
        ordered = sorted(self._counts.items(), key=lambda item: int(item[1].get(_ENTRY_TS, 0)))
        for key, _entry in ordered[: len(self._counts) - _FAILURE_MAX_ENTRIES]:
            self._counts.pop(key, None)

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            _ITEMS: [
                {**{k: v for k, v in entry.items()}, _ENTRY_KEY: key}
                for key, entry in sorted(self._counts.items())
            ],
            _BASE_INDEX: {t: sorted(b) for t, b in sorted(self._vetoed.items())},
        }
        fd, tmp_name = tempfile.mkstemp(dir=str(self._path.parent), prefix=".failure_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False)
            os.replace(tmp_name, self._path)
        except OSError:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        raw_items = payload.get(_ITEMS, [])
        if isinstance(raw_items, list):
            for item in raw_items:
                if not isinstance(item, dict):
                    continue
                key = str(item.get(_ENTRY_KEY, ""))
                if not key:
                    continue
                self._counts[key] = {
                    _ENTRY_COUNT: int(item.get(_ENTRY_COUNT, 0)),
                    _ENTRY_TS: int(item.get(_ENTRY_TS, 0)) or int(time.time()),
                }
        raw_bases = payload.get(_BASE_INDEX, {})
        if isinstance(raw_bases, dict):
            for target, bases in raw_bases.items():
                if isinstance(bases, list):
                    self._vetoed[str(target)] = {str(b) for b in bases}


class DecisionPersistence:
    """Backlog of reactive decisions that outlives a single loop process."""

    def __init__(self, filepath: str | Path) -> None:
        self._path = Path(filepath)
        self._decisions: list[PendingDecision] = []
        self._load()

    def push(self, command: str, reason: str = "") -> None:
        """Park one decision for later consumption (newest first)."""
        command = command.strip()
        if not command:
            return
        self._decisions.insert(0, PendingDecision(command=command, reason=reason, ts=int(time.time())))
        self._decisions = self._decisions[:_DECISION_MAX_ENTRIES]
        self.save()

    def pop(self) -> PendingDecision | None:
        """Consume and persist-removal of the newest parked decision."""
        if not self._decisions:
            return None
        decision = self._decisions.pop(0)
        self.save()
        return decision

    def peek(self) -> PendingDecision | None:
        """Newest parked decision without consuming it."""
        return self._decisions[0] if self._decisions else None

    def __len__(self) -> int:
        return len(self._decisions)

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            _DECISIONS: [
                {_COMMAND: d.command, _REASON: d.reason, _TS: d.ts} for d in self._decisions
            ]
        }
        fd, tmp_name = tempfile.mkstemp(dir=str(self._path.parent), prefix=".decisions_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False)
            os.replace(tmp_name, self._path)
        except OSError:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for item in payload.get(_DECISIONS, []) or []:
            if isinstance(item, dict) and str(item.get(_COMMAND, "")).strip():
                self._decisions.append(
                    PendingDecision(
                        command=str(item.get(_COMMAND, "")).strip(),
                        reason=str(item.get(_REASON, "")),
                        ts=int(item.get(_TS, 0)),
                    )
                )
