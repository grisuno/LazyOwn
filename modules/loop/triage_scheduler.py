"""Difficulty-triage scheduling for the autonomous multi-target loop.

Ports the sapper-v2 scheduling doctrine into LazyOwn terms: a short triage
estimates each target's difficulty, the queue is drained easy-first so quick
wins land before hard assaults, a stop-loss abandons targets that burn attempts
without progress, and near a deadline partially-solved targets are salvaged
first. The scheduler is pure: it operates on plain task records (dicts) and
performs no I/O, so the engine can order its own queue and the policy stays
unit-testable in isolation.

Task records may carry these optional triage fields; all default to neutral so
an unannotated queue degrades to easy-first-by-arrival ordering:
    ``difficulty`` (0.0 easy .. 1.0 hard), ``attempts`` (int),
    ``progress`` (0.0 .. 1.0), ``partial`` (bool, has salvageable partial).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

_DEFAULT_STOP_LOSS_ATTEMPTS = 6
_DEFAULT_SALVAGE_PROGRESS = 0.2
_DEFAULT_HARD_THRESHOLD = 0.6
_PROGRESS_EPSILON = 1e-6
_DIFFICULTY_PORT_FULL = 12.0
_DIFFICULTY_SERVICE_FULL = 8.0


def _clamp01(value: float) -> float:
    """Return value clamped to the inclusive ``[0.0, 1.0]`` range."""
    return max(0.0, min(1.0, float(value)))


def estimate_difficulty(facts: Mapping[str, Any]) -> float:
    """Estimate a target's difficulty in ``[0.0, 1.0]`` from known facts.

    More open ports and more distinct services mean more attack surface to
    work through, so a larger, more varied host scores harder. The estimate is
    deliberately coarse; it only has to rank targets relative to one another.

    Args:
        facts: A mapping that may carry ``open_ports`` (a sized collection or
            int) and ``services`` (a sized collection of service names).

    Returns:
        A difficulty score between 0.0 (trivial) and 1.0 (hard).
    """
    ports = facts.get("open_ports", 0)
    port_count = float(ports) if isinstance(ports, (int, float)) else float(len(ports or []))
    services = facts.get("services", [])
    try:
        service_count = float(len(set(services)))
    except TypeError:
        service_count = 0.0
    port_term = _clamp01(port_count / _DIFFICULTY_PORT_FULL)
    service_term = _clamp01(service_count / _DIFFICULTY_SERVICE_FULL)
    return _clamp01(0.6 * port_term + 0.4 * service_term)


def _item(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return a normalized triage view of a task record."""
    return {
        "task_id": str(record.get("task_id", "")),
        "difficulty": _clamp01(record.get("difficulty", 0.0) or 0.0),
        "attempts": int(record.get("attempts", 0) or 0),
        "progress": _clamp01(record.get("progress", 0.0) or 0.0),
        "partial": bool(record.get("partial", False)),
        "queued_at": float(record.get("queued_at", 0.0) or 0.0),
    }


class TriageScheduler:
    """Order a target queue easy-first with stop-loss and deadline salvage.

    The scheduler holds only policy thresholds; it keeps no per-target state,
    so one instance safely serves the whole engine.
    """

    def __init__(
        self,
        stop_loss_attempts: int = _DEFAULT_STOP_LOSS_ATTEMPTS,
        salvage_progress: float = _DEFAULT_SALVAGE_PROGRESS,
        hard_threshold: float = _DEFAULT_HARD_THRESHOLD,
    ) -> None:
        """Initialize the scheduler with its policy thresholds.

        Args:
            stop_loss_attempts: Attempts without progress before abandoning.
            salvage_progress: Minimum progress for a partial to be salvaged.
            hard_threshold: Difficulty at or above which a target is routed to
                a general (hard assault) rather than a soldier (mass run).
        """
        self.stop_loss_attempts = max(1, int(stop_loss_attempts))
        self.salvage_progress = _clamp01(salvage_progress)
        self.hard_threshold = _clamp01(hard_threshold)

    def should_stop(self, record: Mapping[str, Any]) -> bool:
        """Return True when a target has burned its attempt budget unproductively.

        Args:
            record: A task record with ``attempts`` and ``progress``.

        Returns:
            True when attempts reached the stop-loss limit with no progress.
        """
        item = _item(record)
        return item["attempts"] >= self.stop_loss_attempts and item["progress"] <= _PROGRESS_EPSILON

    def route(self, record: Mapping[str, Any]) -> str:
        """Return the worker tier for a target: ``general`` (hard) or ``soldier``.

        Args:
            record: A task record with a ``difficulty`` field.

        Returns:
            ``"general"`` for hard targets, otherwise ``"soldier"``.
        """
        return "general" if _item(record)["difficulty"] >= self.hard_threshold else "soldier"

    def order(
        self,
        records: Iterable[Mapping[str, Any]],
        *,
        deadline_near: bool = False,
    ) -> list[Mapping[str, Any]]:
        """Return records ordered for draining.

        Normal order is easy-first (lowest difficulty), breaking ties toward
        more progress and earlier arrival. Near a deadline, salvageable
        partials are floated to the front so almost-won targets finish before
        time runs out.

        Args:
            records: The queued task records.
            deadline_near: When True, prioritise salvageable partials.

        Returns:
            A new list of the same records in drain order.
        """
        materialized = list(records)
        views = {id(record): _item(record) for record in materialized}

        def normal_key(record: Mapping[str, Any]) -> tuple[float, float, float, str]:
            view = views[id(record)]
            return (view["difficulty"], -view["progress"], view["queued_at"], view["task_id"])

        if not deadline_near:
            return sorted(materialized, key=normal_key)

        def salvage_key(record: Mapping[str, Any]) -> tuple[int, float]:
            view = views[id(record)]
            salvageable = view["partial"] and view["progress"] >= self.salvage_progress
            if not salvageable:
                return (1, 0.0)
            return (0, -view["progress"])

        return sorted(materialized, key=lambda record: (salvage_key(record), normal_key(record)))

    def pick_next(
        self,
        records: Sequence[Mapping[str, Any]],
        *,
        deadline_near: bool = False,
    ) -> Mapping[str, Any] | None:
        """Return the single record to drain next, or None when empty.

        Args:
            records: The queued task records.
            deadline_near: When True, prioritise salvageable partials.

        Returns:
            The highest-priority record, or None.
        """
        ordered = self.order(records, deadline_near=deadline_near)
        return ordered[0] if ordered else None


__all__ = ["TriageScheduler", "estimate_difficulty"]
