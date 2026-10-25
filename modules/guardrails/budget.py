"""Bounded capacity accounting with strict priority reservation.

Every execution tier owns a fixed capacity. A tier may only consume
capacity while every higher tier keeps a reserve below the saturation
threshold, so a class N task can never starve class N-1. When a tier
saturates the reclaim step drops SUPPORT work and resumes only when the
operator re-arms or usage drains.
"""

from __future__ import annotations

import threading
from typing import Any

from modules.guardrails.contracts import TaskClass

DEFAULT_SATURATION_THRESHOLD: float = 0.85
DEFAULT_CAPACITY_CORE: int = 10000
DEFAULT_CAPACITY_MISSION: int = 2000
DEFAULT_CAPACITY_SUPPORT: int = 512
_MIN_CAPACITY: int = 1
_MAX_THRESHOLD: float = 0.99


class CapacityEnvelope:
    """Fixed-capacity ledger per task class with priority reservation."""

    def __init__(self, capacities: dict[TaskClass, int] | None = None, threshold: float | None = None) -> None:
        """Seed capacities and the saturation threshold.

        Args:
            capacities: Optional per-class capacity override.
            threshold: Optional saturation threshold (0 < t <= 0.99).
        """
        self._lock = threading.Lock()
        self._usage: dict[TaskClass, int] = {tier: 0 for tier in TaskClass}
        self._capacities: dict[TaskClass, int] = dict(self._default_capacities())
        self._threshold = DEFAULT_SATURATION_THRESHOLD
        self.configure(capacities=capacities, threshold=threshold)

    @staticmethod
    def _default_capacities() -> dict[TaskClass, int]:
        """Return the built-in per-class capacity table."""
        return {
            TaskClass.CORE: DEFAULT_CAPACITY_CORE,
            TaskClass.MISSION: DEFAULT_CAPACITY_MISSION,
            TaskClass.SUPPORT: DEFAULT_CAPACITY_SUPPORT,
        }

    def configure(
        self,
        capacities: dict[TaskClass, int] | dict[str, int] | None = None,
        threshold: float | None = None,
    ) -> dict[str, Any]:
        """Apply capacity and threshold settings, clamping invalid values.

        Args:
            capacities: Per-class capacity overrides keyed by TaskClass
                or by the enum name string.
            threshold: Saturation threshold in (0, 0.99].

        Returns:
            The effective settings snapshot.
        """
        with self._lock:
            if capacities:
                for tier, value in capacities.items():
                    key = tier if isinstance(tier, TaskClass) else TaskClass[str(tier).upper()]
                    self._capacities[key] = max(_MIN_CAPACITY, int(value))
            if threshold is not None:
                try:
                    candidate = float(threshold)
                except (TypeError, ValueError):
                    candidate = DEFAULT_SATURATION_THRESHOLD
                self._threshold = min(_MAX_THRESHOLD, max(0.01, candidate))
            return self._snapshot_locked()

    def admit(self, task_class: TaskClass, units: int = 1) -> bool:
        """Reserve units for one tier honouring the priority contract.

        Core is survival: only hard capacity can refuse it. Mission is
        refused while core saturates; support is refused while core or
        mission saturates; any tier over its own capacity is refused.

        Args:
            task_class: Tier requesting admission.
            units: Capacity units the execution will account.

        Returns:
            False when refused by the priority contract or capacity;
            True when admitted.
        """
        if not TaskClass.is_known(task_class):
            return False
        tier = TaskClass(int(task_class))
        with self._lock:
            capacity = self._capacities.get(tier, _MIN_CAPACITY)
            if self._usage[tier] + max(0, int(units)) > capacity:
                return False
            if tier is not TaskClass.CORE and self._usage_ratio(tier) >= self._threshold:
                return False
            for upper in TaskClass:
                if upper >= tier:
                    break
                if self._usage_ratio(upper) >= self._threshold:
                    return False
            return True

    def account(self, task_class: TaskClass, units: int = 1) -> None:
        """Record consumed units for one tier (idempotent on refusal)."""
        if not TaskClass.is_known(task_class):
            return
        tier = TaskClass(int(task_class))
        with self._lock:
            capacity = self._capacities.get(tier, _MIN_CAPACITY)
            self._usage[tier] = min(capacity, self._usage[tier] + max(0, int(units)))

    def release(self, task_class: TaskClass, units: int = 1) -> None:
        """Return units to a tier ledger once an execution finishes."""
        if not TaskClass.is_known(task_class):
            return
        tier = TaskClass(int(task_class))
        with self._lock:
            self._usage[tier] = max(0, self._usage[tier] - max(0, int(units)))

    def purge(self, task_class: TaskClass) -> int:
        """Zero one tier ledger, returning the freed unit count."""
        if not TaskClass.is_known(task_class):
            return 0
        tier = TaskClass(int(task_class))
        with self._lock:
            freed = self._usage[tier]
            self._usage[tier] = 0
            return freed

    def reclaim(self) -> int:
        """Purge SUPPORT allocations, returning the freed unit count."""
        return self.purge(TaskClass.SUPPORT)

    def usage(self, task_class: TaskClass) -> int:
        """Return current consumed units for one tier."""
        if not TaskClass.is_known(task_class):
            return 0
        with self._lock:
            return self._usage[TaskClass(int(task_class))]

    def capacity(self, task_class: TaskClass) -> int:
        """Return configured capacity for one tier."""
        if not TaskClass.is_known(task_class):
            return 0
        with self._lock:
            return self._capacities.get(TaskClass(int(task_class)), _MIN_CAPACITY)

    def saturated(self, task_class: TaskClass) -> bool:
        """Return True when the tier usage ratio reaches the threshold."""
        if not TaskClass.is_known(task_class):
            return False
        with self._lock:
            return self._usage_ratio(TaskClass(int(task_class))) >= self._threshold

    def threshold(self) -> float:
        """Return the configured saturation threshold."""
        with self._lock:
            return self._threshold

    def describe(self) -> dict[str, Any]:
        """Return a per-tier usage snapshot for the admin console."""
        with self._lock:
            return self._snapshot_locked()

    def _usage_ratio(self, tier: TaskClass) -> float:
        """Compute the usage ratio for one tier; caller holds the lock."""
        capacity = max(_MIN_CAPACITY, self._capacities.get(tier, _MIN_CAPACITY))
        return self._usage[tier] / capacity

    def _snapshot_locked(self) -> dict[str, Any]:
        """Serialise tiers, threshold and usage; caller holds the lock."""
        tiers = {}
        for tier in TaskClass:
            tiers[tier.name.lower()] = {
                "usage": self._usage[tier],
                "capacity": self._capacities.get(tier, _MIN_CAPACITY),
                "ratio": round(self._usage_ratio(tier), 4),
                "saturated": self._usage_ratio(tier) >= self._threshold,
            }
        return {"threshold": self._threshold, "tiers": tiers}


__all__ = [
    "DEFAULT_CAPACITY_CORE",
    "DEFAULT_CAPACITY_MISSION",
    "DEFAULT_CAPACITY_SUPPORT",
    "DEFAULT_SATURATION_THRESHOLD",
    "CapacityEnvelope",
]
