"""Task status finite state machine for the autonomous loop.

Single source of truth for which task-status transitions are legal.
The vocabulary lives in ``modules.lazy_loop.TASK_STATUSES``; this module
classifies it into active and terminal states and enforces the observed
transition table of the loop engine:

- active → active: pause/resume/enqueue/dequeue (queued↔running↔paused).
- active → terminal: done/failed/timeout/exhausted/handoff verdicts.
- terminal → running/queued: operator revive via add_intent or requeue.
- terminal → terminal: only the same state (idempotent writes).

Every transition that violates the table raises
:class:`InvalidTaskTransition` (a ``ValueError`` subclass, so existing
call-site handlers keep working).
"""

from __future__ import annotations

from modules.lazy_loop import TASK_STATUSES

ACTIVE_STATUSES = ("queued", "running", "paused")
TERMINAL_STATUSES = ("done", "failed", "timeout", "exhausted", "handoff")

_ACTIVE_SET = frozenset(ACTIVE_STATUSES)
_TERMINAL_SET = frozenset(TERMINAL_STATUSES)
_ACTIVE_TARGETS = frozenset(ACTIVE_STATUSES) | _TERMINAL_SET
_TERMINAL_TARGETS = frozenset({"running", "queued"})

_TRANSITIONS: dict[str, frozenset[str]] = {}
for _status in TASK_STATUSES:
    if _status in _ACTIVE_SET:
        _TRANSITIONS[_status] = _ACTIVE_TARGETS
    else:
        _TRANSITIONS[_status] = _TERMINAL_TARGETS | {_status}
del _status, _ACTIVE_TARGETS, _TERMINAL_TARGETS


class InvalidTaskTransition(ValueError):
    """Raised when a task status transition violates the FSM table."""


def is_valid_status(status: object) -> bool:
    """Return True when ``status`` belongs to the task-status vocabulary."""
    return status in _TRANSITIONS


def is_active(status: object) -> bool:
    """Return True when ``status`` is an active (non-terminal) state."""
    return status in _ACTIVE_SET


def is_terminal(status: object) -> bool:
    """Return True when ``status`` is a terminal verdict state."""
    return status in _TERMINAL_SET


def allowed_transitions(status: str) -> frozenset[str]:
    """Return the set of target statuses legal from ``status``.

    Args:
        status: Current task status.

    Returns:
        The frozenset of allowed target statuses; empty for unknown
        statuses.

    Raises:
        ValueError: When ``status`` is not in the vocabulary.
    """
    if status not in _TRANSITIONS:
        raise ValueError(f"unknown status: {status}")
    return _TRANSITIONS[status]


def can_transition(current: str, target: str) -> bool:
    """Return True when ``current → target`` is a legal transition.

    Args:
        current: Current task status.
        target: Requested task status.

    Returns:
        True when the transition is allowed (same-state writes are
        always allowed for known statuses).
    """
    if current == target:
        return current in _TRANSITIONS
    return target in _TRANSITIONS.get(current, frozenset())


def require_transition(current: str, target: str) -> None:
    """Validate one task status transition.

    Args:
        current: Current task status.
        target: Requested task status.

    Raises:
        ValueError: When either status is unknown.
        InvalidTaskTransition: When the transition violates the table.
    """
    if current not in _TRANSITIONS:
        raise ValueError(f"unknown status: {current}")
    if target not in _TRANSITIONS:
        raise ValueError(f"unknown status: {target}")
    if current == target:
        return
    if target not in _TRANSITIONS[current]:
        raise InvalidTaskTransition(
            f"illegal task transition {current!r} -> {target!r}; allowed: {sorted(_TRANSITIONS[current])}"
        )
