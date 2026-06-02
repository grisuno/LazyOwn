"""Self-populating kill-chain progress derived from the daemon event stream.

The dashboard kill-chain used to depend on ``world_model.json`` carrying a
``completed_phases`` / ``phase`` pair, but the autonomous daemon never writes
those keys, so the panel stayed empty during a live run. This module computes
kill-chain progress from the authoritative source instead: the structured
events the daemon appends to ``sessions/autonomous_events.jsonl``.

Each step the daemon takes carries a ``phase`` field, and phase transitions are
emitted as ``PHASE_ADVANCE`` / ``PHASE_CHANGE`` events. From that signal we can
mark every phase the engagement has passed through as *done*, the current phase
as *active*, and the rest as *pending*, while also surfacing per-phase activity
counts and accumulated reward. The result is a kill chain that fills itself as
the daemon works.

The module imports nothing from ``lazyown.py`` / ``lazyc2.py`` and performs no
rendering, so it stays unit-testable and reusable across the Textual dashboard
and the web dashboard.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_PHASES: tuple[tuple[str, str], ...] = (
    ("recon", "Recon"),
    ("scan", "Scan"),
    ("enum", "Enum"),
    ("exploit", "Exploit"),
    ("privesc", "PrivEsc"),
    ("lateral", "Lateral"),
    ("exfil", "Exfil"),
    ("report", "Report"),
)

STATE_DONE: str = "done"
STATE_ACTIVE: str = "active"
STATE_PENDING: str = "pending"

_PHASE_STEP_TYPES: frozenset[str] = frozenset({"STEP_START", "STEP_DONE", "STEP_SKIPPED"})
_PHASE_TRANSITION_TYPES: frozenset[str] = frozenset({"PHASE_ADVANCE", "PHASE_CHANGE"})


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


def _phase_from_event(event: dict[str, Any]) -> str:
    """Return the phase an event belongs to, empty string if absent."""
    payload = event.get("payload")
    if not isinstance(payload, dict):
        return ""
    if event.get("type") in _PHASE_TRANSITION_TYPES:
        return str(payload.get("to") or payload.get("phase") or "").lower()
    return str(payload.get("phase") or "").lower()


def _detect_current_phase(
    events: list[dict[str, Any]],
    world: dict[str, Any],
    phase_keys: list[str],
) -> str:
    """Resolve the active phase from events, falling back to the world model.

    Args:
        events: Daemon events ordered oldest first.
        world: Parsed ``world_model.json`` snapshot.
        phase_keys: Ordered list of canonical phase identifiers.

    Returns:
        The active phase identifier, or an empty string when unknown.
    """
    for event in reversed(events):
        phase = _phase_from_event(event)
        if phase in phase_keys:
            return phase
    world_phase = str(world.get("phase") or world.get("current_phase") or "").lower()
    if world_phase in phase_keys:
        return world_phase
    return ""


def compute_killchain(
    events: list[dict[str, Any]],
    world: dict[str, Any] | None = None,
    phases: tuple[tuple[str, str], ...] = DEFAULT_PHASES,
) -> list[PhaseProgress]:
    """Compute kill-chain progress from daemon events and the world model.

    A phase is marked *done* when the engagement has advanced past it (its index
    is below the active phase) or the world model explicitly lists it as
    completed. The active phase is *active*; everything after it is *pending*.
    Per-phase activity counts and accumulated reward are derived from the step
    events regardless of state.

    Args:
        events: Daemon events ordered oldest first (see
            :func:`cli.reasoning_stream.read_raw_events`).
        world: Optional ``world_model.json`` snapshot used as a fallback for the
            current phase and for an explicit ``completed_phases`` list.
        phases: Ordered ``(key, label)`` pairs describing the kill chain.

    Returns:
        One :class:`PhaseProgress` per phase, in kill-chain order.
    """
    world = world or {}
    phase_keys = [key for key, _ in phases]

    activity: dict[str, int] = {key: 0 for key in phase_keys}
    reward: dict[str, float] = {key: 0.0 for key in phase_keys}
    for event in events:
        if event.get("type") not in _PHASE_STEP_TYPES:
            continue
        phase = _phase_from_event(event)
        if phase not in activity:
            continue
        activity[phase] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            value = payload.get("reward")
            if isinstance(value, (int, float)):
                reward[phase] += float(value)

    current = _detect_current_phase(events, world, phase_keys)
    current_idx = phase_keys.index(current) if current in phase_keys else -1
    explicit_done = {str(p).lower() for p in (world.get("completed_phases") or world.get("phases_done") or [])}

    progress: list[PhaseProgress] = []
    for idx, (key, label) in enumerate(phases):
        if key == current:
            state = STATE_ACTIVE
        elif key in explicit_done or (current_idx >= 0 and idx < current_idx):
            state = STATE_DONE
        else:
            state = STATE_PENDING
        progress.append(
            PhaseProgress(
                key=key,
                label=label,
                state=state,
                activity=activity[key],
                reward=round(reward[key], 3),
            )
        )
    return progress
