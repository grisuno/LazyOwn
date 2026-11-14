"""Backward-compat kill-chain progress types for the dashboard TUI.

The canonical phase definitions and progress computation live in
``modules.killchain.KillChain``, which already wraps ``WorldModel`` and
raw ``world_model.json``. Consumers should migrate there. What remains
here is only the :class:`PhaseProgress` dataclass the TUI imports.
"""

from __future__ import annotations

from dataclasses import dataclass

STATE_DONE: str = "done"
STATE_ACTIVE: str = "active"
STATE_PENDING: str = "pending"


@dataclass(frozen=True)
class PhaseProgress:
    """Computed progress for a single kill-chain phase.

    Attributes:
        key: Canonical phase identifier (e.g. ``recon``).
        label: Human-readable phase label (e.g. ``Recon``).
        state: One of :data:`STATE_DONE`, :data:`STATE_ACTIVE`,
            :data:`STATE_PENDING`.
        activity: Number of daemon step events observed in this phase.
        reward: Sum of step rewards recorded in this phase.
    """

    key: str
    label: str
    state: str
    activity: int
    reward: float


__all__ = ["PhaseProgress", "STATE_ACTIVE", "STATE_DONE", "STATE_PENDING"]
