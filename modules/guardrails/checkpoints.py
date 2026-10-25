"""Checkpoint ledger with warm-restart recovery.

Checkpoints capture the caller's meaningful state snapshot before risky
executions. A warm restart purges non-critical runtime contexts, keeps
core state intact and restores the latest core checkpoint; it never
raises and never resets the whole application.
"""

from __future__ import annotations

import copy
import threading
from typing import Any

CHECKPOINT_HISTORY_PER_KEY: int = 3


class CheckpointLedger:
    """Bounded per-key checkpoint history with warm-restart restore."""

    def __init__(self, history: int = CHECKPOINT_HISTORY_PER_KEY) -> None:
        """Create an empty ledger.

        Args:
            history: Snapshot history retained per key (>= 1).
        """
        self._lock = threading.Lock()
        self._history = max(1, int(history))
        self._slots: dict[str, list[Any]] = {}
        self._restarts = 0
        self._last_restart: dict[str, Any] | None = None

    def capture(self, key: str, state: Any) -> bool:
        """Store one immutable snapshot for a key.

        Args:
            key: Checkpoint identity (for example ``loop.core_round``).
            state: JSON-serializable snapshot; deep-copied on capture.

        Returns:
            True when the snapshot was stored.
        """
        if not str(key).strip():
            return False
        with self._lock:
            slots = self._slots.setdefault(str(key), [])
            slots.append(copy.deepcopy(state))
            del slots[: -self._history]
            return True

    def restore(self, key: str) -> Any:
        """Return the latest snapshot for a key, or None when missing."""
        with self._lock:
            slots = self._slots.get(str(key)) or []
            if not slots:
                return None
            return copy.deepcopy(slots[-1])

    def keys(self) -> list[str]:
        """Return the tracked checkpoint keys."""
        with self._lock:
            return sorted(self._slots)

    def warm_restart(self, core_key: str = "") -> dict[str, Any]:
        """Purge non-core runtime contexts and restore the core snapshot.

        Args:
            core_key: Optional checkpoint key to restore from.

        Returns:
            A summary with restored flag, payload and restart counter.
        """
        try:
            with self._lock:
                payload = None
                restored = False
                if core_key:
                    slots = self._slots.get(str(core_key)) or []
                    if slots:
                        payload = copy.deepcopy(slots[-1])
                        restored = True
                self._restarts += 1
                self._last_restart = {
                    "restored": restored,
                    "core_key": str(core_key or ""),
                    "restarts": self._restarts,
                }
                return dict(self._last_restart) | {"payload": copy.deepcopy(payload)}
        except Exception:
            return {"restored": False, "core_key": str(core_key or ""), "restarts": self._restarts, "payload": None}

    def describe(self) -> dict[str, Any]:
        """Return the ledger state for the admin console."""
        with self._lock:
            return {
                "keys": sorted(self._slots),
                "history_per_key": self._history,
                "restarts": self._restarts,
                "last_restart": dict(self._last_restart) if self._last_restart else None,
            }


__all__ = ["CHECKPOINT_HISTORY_PER_KEY", "CheckpointLedger"]
