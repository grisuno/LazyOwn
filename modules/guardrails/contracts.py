"""Contracts for the execution guardrail harness.

The harness protects the operator and the machine from degradation:
every execution is classified into an immutable task class, bounded
capacity is accounted per class, failures warm-restart from the last
checkpoint instead of crashing, and secondary features degrade first.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Protocol

CONFIG_SECTION: str = "orchestrator.guardrails"


class TaskClass(IntEnum):
    """Immutable execution tier.

    A class N task never blocks or consumes capacity reserved for class
    N-1; when capacity saturates the lowest classes are refused first.
    """

    CORE = 0
    MISSION = 1
    SUPPORT = 2

    @classmethod
    def is_known(cls, value: object) -> bool:
        """Return True when the value names a registered class."""
        try:
            return int(value) in tuple(item.value for item in cls)  # type: ignore[call-overload]
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class RunTicket:
    """One admitted execution reservation."""

    ticket_id: str
    task_class: TaskClass
    granted_at: float
    units: int


class GuardrailContract(Protocol):
    """Public surface every harness implementation must expose."""

    def describe(self) -> dict[str, Any]:
        """Return tier usage, advisories, suspended features and checkpoints."""
        ...

    def run_guarded(
        self,
        task_class: TaskClass,
        fn: Callable[..., Any],
        *args: Any,
        key: str = "",
        state: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Execute fn under capacity accounting and warm-restart policy."""
        ...

    def warm_restart(self) -> dict[str, Any]:
        """Purge non-critical contexts and restore the last checkpoint."""
        ...


class HarnessAdminPort(Protocol):
    """Administration surface consumed by the orchestrator console."""

    def configure(self, settings: dict[str, Any]) -> dict[str, Any]:
        """Apply capacity and threshold settings from the payload."""
        ...

    def rearm(self) -> dict[str, Any]:
        """Clear advisories and resume suspended features after an operator review."""
        ...


__all__ = [
    "CONFIG_SECTION",
    "GuardrailContract",
    "HarnessAdminPort",
    "RunTicket",
    "TaskClass",
]
