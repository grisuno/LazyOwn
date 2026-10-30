"""The one shared contract for autonomous action selection.

Both autonomous runtimes (the LazyLoopEngine planner and the autonomous
daemon) used to pick the next action with their own private logic. This
module defines the single vocabulary they now share: a :class:`SelectionContext`
describing the live engagement state, an :class:`ActionDecision` naming the
command to run next, and the :class:`Selector` protocol every strategy
implements. One selector lives per file under ``modules/selectors/`` so each
strategy is a single contract; the runtimes only know this protocol.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class SelectionContext:
    """Immutable snapshot of what the loop knows when it picks the next action.

    Attributes:
        target: Host currently under test.
        phase: Canonical kill-chain phase (``recon``, ``exploit``, ...).
        os_hint: Target platform hint (``linux``/``windows``), blank if unknown.
        services: Discovered service names for the target.
        has_creds: Whether usable credentials are known.
        exclude: Action identifiers already taken, to avoid repeats.
        extra: Open map for strategy-specific inputs without widening the
            shared contract.
    """

    target: str
    phase: str = ""
    os_hint: str = ""
    services: tuple[str, ...] = ()
    has_creds: bool = False
    exclude: frozenset[str] = frozenset()
    extra: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionDecision:
    """One proposed next action, runtime-agnostic.

    Attributes:
        command: The shell/verb command line to execute.
        source: Selector identity that produced it.
        reason: Short human rationale for the trace.
        priority: Lower is more urgent; runtimes may use it to rank.
        mitre: Optional ATT&CK technique id when the action maps to one.
    """

    command: str
    source: str = "selector"
    reason: str = ""
    priority: int = 5
    mitre: str = ""


@runtime_checkable
class Selector(Protocol):
    """Contract for one action-selection strategy.

    Implementations are single-responsibility and side-effect free beyond
    their own bookkeeping; they return ``None`` when they have no suggestion
    so the cascade falls through to the next selector.
    """

    name: str

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return the next action for this strategy, or None to abstain."""
        ...


__all__ = ["ActionDecision", "SelectionContext", "Selector"]
