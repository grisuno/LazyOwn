"""Execution harness facade: guarded runs, warm restart, degradation.

``run_guarded`` classifies one execution into a task class, reserves
capacity, and applies the failure policy: core executions warm-restart
from the latest checkpoint and retry once; mission and support
executions degrade with a non-blocking advisory. The process keeps its
control cycle alive instead of crashing.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import Any

from modules.guardrails.advisories import AdvisoryLedger, FeatureGate
from modules.guardrails.budget import CapacityEnvelope
from modules.guardrails.checkpoints import CheckpointLedger
from modules.guardrails.contracts import RunTicket, TaskClass

_KILL_SIGNALS: tuple[type[BaseException], ...] = (KeyboardInterrupt, SystemExit)


class GuardHarness:
    """Facade binding capacity, checkpoints and degradation policies."""

    def __init__(
        self,
        threshold: float | None = None,
        capacities: dict[str, int] | None = None,
    ) -> None:
        """Create a harness with payload-driven or default settings.

        Args:
            threshold: Optional saturation threshold override.
            capacities: Optional per-tier capacity overrides keyed by
                tier name.
        """
        self._envelope = CapacityEnvelope(threshold=threshold)
        self._ledger = CheckpointLedger()
        self._advisories = AdvisoryLedger()
        self._features = FeatureGate()
        self._lock = threading.Lock()
        if capacities:
            self._envelope.configure(capacities=capacities)

    def configure(self, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        """Apply settings from the payload guardrails section.

        Args:
            settings: Mapping with optional ``saturation_threshold`` and
                ``capacity`` (per-tier name to integer).

        Returns:
            The effective harness description after configuration.
        """
        settings = settings or {}
        capacities = settings.get("capacity") if isinstance(settings.get("capacity"), dict) else None
        self._envelope.configure(capacities=capacities, threshold=settings.get("saturation_threshold"))
        return self.describe()

    def run_guarded(
        self,
        task_class: TaskClass,
        fn: Callable[..., Any],
        *args: Any,
        key: str = "",
        state: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Execute fn under the tier policy, degrading instead of crashing.

        Core executions capture a checkpoint first and warm-restart with
        one retry on failure. Mission and support executions record a
        non-blocking advisory and return None; suspended support
        features are refused outright.

        Args:
            task_class: Execution tier.
            fn: Callable to execute.
            key: Optional checkpoint key (core retries restore it).
            state: Optional checkpoint snapshot captured before execution.
            args: Positional arguments for fn.
            kwargs: Keyword arguments for fn.

        Returns:
            The callable result, the warm-restart retry result, or None
            when refused or degraded. KeyboardInterrupt and SystemExit
            always propagate.

        Raises:
            KeyboardInterrupt: When the operator interrupts execution.
            SystemExit: When the interpreter is shutting down.
        """
        tier = TaskClass(int(task_class))
        if tier is TaskClass.SUPPORT and self._features.is_suspended("render"):
            self._advisories.notice(
                "feature_dropped", f"support task refused while degraded: {getattr(fn, '__qualname__', fn)}"
            )
            return None
        units = 1
        if not self._envelope.admit(tier, units):
            self._advisories.notice(
                "tier_refused",
                f"{tier.name.lower()} execution refused at saturation: {getattr(fn, '__qualname__', fn)}",
            )
            return None
        if state is not None and key:
            self._ledger.capture(key, state)
        ticket = RunTicket(
            ticket_id=f"{tier.name.lower()}-{time.time_ns()}", task_class=tier, granted_at=time.time(), units=units
        )
        try:
            result = fn(*args, **kwargs)
        except _KILL_SIGNALS:
            self._envelope.account(tier, ticket.units)
            raise
        except Exception as exc:
            return self._on_failure(tier, ticket, key, fn, args, kwargs, exc)
        self._envelope.account(tier, ticket.units)
        return result

    def warm_restart(self, core_key: str = "") -> dict[str, Any]:
        """Purge non-critical contexts and restore the core checkpoint.

        Args:
            core_key: Optional checkpoint key to restore.

        Returns:
            The warm-restart summary from the checkpoint ledger.
        """
        freed = self._envelope.reclaim()
        summary = self._ledger.warm_restart(core_key)
        self._advisories.notice("warm_restart", f"purged support units={freed} restored={summary.get('restored')}")
        return summary

    def suspend(self, feature: str, reason: str = "") -> bool:
        """Suspend one optional feature until re-arm.

        Args:
            feature: Feature name from :data:`SUSPENDABLE_FEATURES`.
            reason: Optional operator-facing detail.

        Returns:
            True when the feature is now suspended.
        """
        ok = self._features.suspend(feature, reason)
        if ok:
            self._advisories.notice("feature_suspended", f"{feature}: {reason or 'degraded'}")
        return ok

    def rearm(self) -> dict[str, Any]:
        """Resume suspended features, clear advisories and refresh budgets.

        Returns:
            Summary with resumed feature count and cleared notices.
        """
        resumed = self._features.resume_all()
        cleared = self._advisories.clear()
        self._envelope.purge(TaskClass.MISSION)
        self._envelope.purge(TaskClass.SUPPORT)
        return {"resumed": resumed, "cleared": cleared}

    def describe(self) -> dict[str, Any]:
        """Return the full harness snapshot for the admin console."""
        return {
            "envelope": self._envelope.describe(),
            "checkpoints": self._ledger.describe(),
            "advisories": self._advisories.describe(),
            "features": self._features.describe(),
        }

    def _on_failure(
        self,
        tier: TaskClass,
        ticket: RunTicket,
        key: str,
        fn: Callable[..., Any],
        args: tuple,
        kwargs: dict,
        exc: Exception,
    ) -> Any:
        """Apply the tier failure policy for one failed execution.

        Args:
            tier: Execution tier of the failed callable.
            ticket: Reservation ticket of the failed attempt.
            key: Checkpoint key captured before execution.
            fn: The failed callable.
            args: Original positional arguments.
            kwargs: Original keyword arguments.
            exc: The captured failure.

        Returns:
            The retry result for core executions, None otherwise.
        """
        self._envelope.account(tier, ticket.units)
        self._advisories.notice(f"{tier.name.lower()}_failed", f"{type(exc).__name__}: {exc}")
        if tier is not TaskClass.CORE:
            return None
        summary = self.warm_restart(key)
        if not summary.get("restored"):
            self._advisories.notice("core_no_checkpoint", f"no checkpoint to restore for {key or 'anonymous'}")
            return None
        if not self._envelope.admit(tier, ticket.units):
            self._advisories.notice("tier_refused", "core retry refused at saturation")
            return None
        retry_ticket = RunTicket(
            ticket_id=f"{tier.name.lower()}-retry-{time.time_ns()}",
            task_class=tier,
            granted_at=time.time(),
            units=ticket.units,
        )
        try:
            retried = fn(*args, **kwargs)
        except _KILL_SIGNALS:
            self._envelope.account(tier, retry_ticket.units)
            raise
        except Exception as retry_exc:
            self._envelope.account(tier, retry_ticket.units)
            self._advisories.notice("core_retry_failed", f"{type(retry_exc).__name__}: {retry_exc}")
            return None
        self._envelope.account(tier, retry_ticket.units)
        return retried


_HARNESS: GuardHarness | None = None
_HARNESS_LOCK = threading.Lock()


def global_harness() -> GuardHarness:
    """Return the process-wide harness, creating it on first use."""
    global _HARNESS
    with _HARNESS_LOCK:
        if _HARNESS is None:
            _HARNESS = GuardHarness()
        return _HARNESS


def reset_global_harness() -> GuardHarness:
    """Replace the process-wide harness (tests and warm reloads only).

    Returns:
        The fresh harness instance.
    """
    global _HARNESS
    with _HARNESS_LOCK:
        _HARNESS = GuardHarness()
        return _HARNESS


__all__ = ["GuardHarness", "global_harness", "reset_global_harness"]
