"""Non-blocking advisories and feature degradation.

Advisories notify supervisors without interrupting the running logic.
The feature gate drops optional work first when capacity degrades and
restores it only after an explicit re-arm or a clean restart.
"""

from __future__ import annotations

import threading
from typing import Any

ADVISORY_LIMIT: int = 128
SUSPENDABLE_FEATURES: frozenset[str] = frozenset({"render", "enrich", "llm_stream", "swan"})


class AdvisoryLedger:
    """Bounded non-blocking notice stream (newest first)."""

    def __init__(self, limit: int = ADVISORY_LIMIT) -> None:
        """Create an empty ledger.

        Args:
            limit: Maximum retained notices (oldest dropped).
        """
        self._lock = threading.Lock()
        self._limit = max(1, int(limit))
        self._items: list[dict[str, Any]] = []
        self._dropped = 0

    def notice(self, code: str, message: str = "") -> dict[str, Any]:
        """Record one advisory without blocking the caller.

        Args:
            code: Short machine tag (for example ``tier_saturated``).
            message: Optional human detail.

        Returns:
            The stored advisory entry.
        """
        entry: dict[str, Any] = {"code": str(code or "notice")[:64], "message": str(message or "")[:200]}
        with self._lock:
            self._items.insert(0, entry)
            del self._items[self._limit :]
            self._dropped += 1
            entry["seq"] = self._dropped
            return dict(entry)

    def tail(self, limit: int = 10) -> list[dict[str, Any]]:
        """Return the newest notices up to the limit."""
        with self._lock:
            return [dict(item) for item in self._items[: max(1, int(limit))]]

    def clear(self) -> int:
        """Drop every notice, returning the discarded count."""
        with self._lock:
            count = len(self._items)
            self._items.clear()
            return count

    def describe(self) -> dict[str, Any]:
        """Return the ledger summary for the admin console."""
        with self._lock:
            return {"count": len(self._items), "dropped_total": self._dropped, "items": self.tail_locked(10)}

    def tail_locked(self, limit: int) -> list[dict[str, Any]]:
        """Tail helper used by describe; caller holds the lock."""
        return [dict(item) for item in self._items[: max(1, int(limit))]]


class FeatureGate:
    """Optional-feature suspension registry for graceful degradation."""

    def __init__(self, features: frozenset[str] = SUSPENDABLE_FEATURES) -> None:
        """Create a gate limited to the known optional features.

        Args:
            features: Suspendable feature names.
        """
        self._lock = threading.Lock()
        self._features = set(features)
        self._suspended: dict[str, str] = {}

    def suspend(self, feature: str, reason: str = "") -> bool:
        """Suspend one optional feature.

        Args:
            feature: Feature name from :data:`SUSPENDABLE_FEATURES`.
            reason: Optional operator-facing detail.

        Returns:
            True when the feature is now suspended; False for unknown
            features (core features can never degrade).
        """
        name = str(feature).strip().lower()
        with self._lock:
            if name not in self._features:
                return False
            self._suspended.setdefault(name, str(reason or "degraded")[:120])
            return True

    def resume(self, feature: str) -> bool:
        """Resume one suspended feature, returning True when it changed."""
        name = str(feature).strip().lower()
        with self._lock:
            return self._suspended.pop(name, None) is not None

    def resume_all(self) -> int:
        """Resume every suspended feature, returning the resumed count."""
        with self._lock:
            count = len(self._suspended)
            self._suspended.clear()
            return count

    def is_suspended(self, feature: str) -> bool:
        """Return True when the feature is currently suspended."""
        with self._lock:
            return str(feature).strip().lower() in self._suspended

    def suspended(self) -> dict[str, str]:
        """Return the suspended feature map (feature -> reason)."""
        with self._lock:
            return dict(self._suspended)

    def describe(self) -> dict[str, Any]:
        """Return the gate state for the admin console."""
        with self._lock:
            return {"known": sorted(self._features), "suspended": dict(self._suspended)}


__all__ = ["ADVISORY_LIMIT", "SUSPENDABLE_FEATURES", "AdvisoryLedger", "FeatureGate"]
