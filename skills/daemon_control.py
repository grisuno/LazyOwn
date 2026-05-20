"""Operator steering layer for the LazyOwn autonomous daemon.

The daemon (``skills/autonomous_daemon.py``) reads the control state
written here before every command execution. The CLI (``do_daemon_*``)
and MCP (``lazyown_daemon_*``) write the same state. This module owns:

* The data model (:class:`ControlState`, :class:`PendingAction`).
* Atomic persistence to ``sessions/daemon_control.json``.
* The approval-gate state machine and a blocking wait helper.

All public methods are safe for concurrent use across processes
because every write goes through ``tempfile`` + ``os.replace`` so
readers either see the previous file or the new one but never a
truncated file.
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional


CONTROL_FILE_NAME: str = "daemon_control.json"
PENDING_TTL_DEFAULT_S: float = 30.0
APPROVAL_POLL_INTERVAL_S: float = 0.5
PAUSE_POLL_INTERVAL_S: float = 1.0
CONTROL_FILE_MODE: int = 0o600

MODE_AUTO: str = "auto"
MODE_APPROVAL: str = "approval"
MODE_PAUSED: str = "paused"
VALID_MODES: frozenset[str] = frozenset({MODE_AUTO, MODE_APPROVAL, MODE_PAUSED})

DECISION_PENDING: str = "pending"
DECISION_APPROVED: str = "approved"
DECISION_VETOED: str = "vetoed"
DECISION_EXPIRED: str = "expired"
VALID_DECISIONS: frozenset[str] = frozenset(
    {DECISION_PENDING, DECISION_APPROVED, DECISION_VETOED, DECISION_EXPIRED}
)


@dataclass
class PendingAction:
    """A single command awaiting operator approval.

    Args:
        action_id: Unique identifier matched by the operator when
            approving or vetoing.
        command: Shell command proposed by the daemon.
        reason: Selector-supplied rationale forwarded to the operator.
        target: Active target host the command will run against.
        proposed_at: Epoch seconds when the action was registered.
        ttl_seconds: How long the action waits before expiring.
        decision: One of :data:`DECISION_PENDING`,
            :data:`DECISION_APPROVED`, :data:`DECISION_VETOED`,
            :data:`DECISION_EXPIRED`.
        decided_at: Epoch seconds when the decision was recorded
            (``0.0`` while pending).
        operator: Identifier of the operator who decided (empty when
            expired).
    """

    action_id: str = ""
    command: str = ""
    reason: str = ""
    target: str = ""
    proposed_at: float = 0.0
    ttl_seconds: float = PENDING_TTL_DEFAULT_S
    decision: str = DECISION_PENDING
    decided_at: float = 0.0
    operator: str = ""

    def is_expired(self, now: Optional[float] = None) -> bool:
        """Return ``True`` when a still-pending action has exceeded its TTL."""
        if self.decision != DECISION_PENDING:
            return False
        moment = now if now is not None else time.time()
        return moment - self.proposed_at >= self.ttl_seconds


@dataclass
class ControlState:
    """Steering state shared between operator surfaces and the daemon.

    Args:
        mode: One of :data:`MODE_AUTO`, :data:`MODE_APPROVAL`,
            :data:`MODE_PAUSED`. Default is auto, which preserves the
            historical daemon behaviour.
        vetoed_commands: First-token names the daemon must avoid.
        focus_targets: When non-empty, the daemon only executes
            objectives whose target appears in this list.
        pending: Active approval request, when ``mode == approval`` and
            the daemon has proposed a command.
        updated_at: Epoch seconds of the last write — populated by
            :meth:`DaemonControl.save`.
    """

    mode: str = MODE_AUTO
    vetoed_commands: list[str] = field(default_factory=list)
    focus_targets: list[str] = field(default_factory=list)
    pending: Optional[PendingAction] = None
    updated_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialise the state to a plain JSON-ready dict."""
        return {
            "mode": self.mode,
            "vetoed_commands": list(self.vetoed_commands),
            "focus_targets": list(self.focus_targets),
            "pending": asdict(self.pending) if self.pending is not None else None,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ControlState":
        """Build a state from JSON data, sanitising malformed input."""
        mode = str(data.get("mode") or MODE_AUTO)
        if mode not in VALID_MODES:
            mode = MODE_AUTO
        pending_raw = data.get("pending")
        pending: Optional[PendingAction] = None
        if isinstance(pending_raw, dict):
            decision = str(pending_raw.get("decision") or DECISION_PENDING)
            if decision not in VALID_DECISIONS:
                decision = DECISION_PENDING
            ttl_raw = pending_raw.get("ttl_seconds")
            ttl_seconds = (
                float(ttl_raw)
                if ttl_raw is not None
                else PENDING_TTL_DEFAULT_S
            )
            pending = PendingAction(
                action_id=str(pending_raw.get("action_id") or ""),
                command=str(pending_raw.get("command") or ""),
                reason=str(pending_raw.get("reason") or ""),
                target=str(pending_raw.get("target") or ""),
                proposed_at=float(pending_raw.get("proposed_at") or 0.0),
                ttl_seconds=ttl_seconds,
                decision=decision,
                decided_at=float(pending_raw.get("decided_at") or 0.0),
                operator=str(pending_raw.get("operator") or ""),
            )
        return cls(
            mode=mode,
            vetoed_commands=[str(c) for c in (data.get("vetoed_commands") or []) if c],
            focus_targets=[str(t) for t in (data.get("focus_targets") or []) if t],
            pending=pending,
            updated_at=float(data.get("updated_at") or 0.0),
        )


def _first_token(command: str) -> str:
    """Return the first whitespace-separated token of ``command``."""
    stripped = command.strip()
    if not stripped:
        return ""
    return stripped.split()[0]


class DaemonControl:
    """Atomic read/write facade for ``sessions/daemon_control.json``.

    All mutations write to a temp file then ``os.replace`` for
    atomicity so concurrent readers (daemon + CLI + MCP) never observe
    partial JSON. The instance is also safe to share inside one
    process: every write is serialised by an internal lock.
    """

    def __init__(self, sessions_dir: Path | str) -> None:
        """Pin the control file to ``<sessions_dir>/daemon_control.json``.

        Args:
            sessions_dir: Absolute or relative path to the LazyOwn
                ``sessions/`` directory. The directory is created on
                the first write if it does not yet exist.
        """
        self._sessions_dir: Path = Path(sessions_dir)
        self._path: Path = self._sessions_dir / CONTROL_FILE_NAME
        self._lock: threading.Lock = threading.Lock()

    @property
    def path(self) -> Path:
        """Absolute path of the control file on disk."""
        return self._path

    def load(self) -> ControlState:
        """Return the current state or defaults when the file is missing."""
        if not self._path.exists():
            return ControlState()
        try:
            raw = self._path.read_text(encoding="utf-8")
            data = json.loads(raw)
            if not isinstance(data, dict):
                return ControlState()
            return ControlState.from_dict(data)
        except (OSError, json.JSONDecodeError):
            return ControlState()

    def save(self, state: ControlState) -> None:
        """Persist ``state`` atomically.

        The ``updated_at`` field is overwritten with the current epoch
        so callers do not need to maintain it.
        """
        with self._lock:
            self._sessions_dir.mkdir(parents=True, exist_ok=True)
            state.updated_at = time.time()
            payload = json.dumps(state.to_dict(), indent=2, ensure_ascii=False)
            fd, tmp_path = tempfile.mkstemp(
                prefix=".daemon_control.",
                suffix=".tmp",
                dir=str(self._sessions_dir),
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as fh:
                    fh.write(payload)
                os.replace(tmp_path, self._path)
                try:
                    os.chmod(self._path, CONTROL_FILE_MODE)
                except OSError:
                    pass
            except Exception:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise

    def set_mode(self, mode: str) -> ControlState:
        """Switch between :data:`MODE_AUTO`, :data:`MODE_APPROVAL`, :data:`MODE_PAUSED`."""
        if mode not in VALID_MODES:
            raise ValueError(
                f"invalid mode '{mode}', expected one of {sorted(VALID_MODES)}"
            )
        state = self.load()
        state.mode = mode
        self.save(state)
        return state

    def pause(self) -> ControlState:
        """Convenience wrapper for ``set_mode(MODE_PAUSED)``."""
        return self.set_mode(MODE_PAUSED)

    def resume(self) -> ControlState:
        """Convenience wrapper for ``set_mode(MODE_AUTO)``."""
        return self.set_mode(MODE_AUTO)

    def require_approval(self) -> ControlState:
        """Convenience wrapper for ``set_mode(MODE_APPROVAL)``."""
        return self.set_mode(MODE_APPROVAL)

    def add_veto(self, command_token: str) -> ControlState:
        """Append a first-token name to the veto list.

        Raises:
            ValueError: When ``command_token`` is empty.
        """
        token = _first_token(command_token)
        if not token:
            raise ValueError("empty veto token")
        state = self.load()
        if token not in state.vetoed_commands:
            state.vetoed_commands.append(token)
        self.save(state)
        return state

    def remove_veto(self, command_token: str) -> ControlState:
        """Remove a previously vetoed command from the list."""
        token = _first_token(command_token)
        state = self.load()
        state.vetoed_commands = [c for c in state.vetoed_commands if c != token]
        self.save(state)
        return state

    def clear_vetoes(self) -> ControlState:
        """Remove every entry from the veto list."""
        state = self.load()
        state.vetoed_commands = []
        self.save(state)
        return state

    def set_focus(self, targets: list[str]) -> ControlState:
        """Replace the focus-target list. An empty list disables focus."""
        cleaned = [t.strip() for t in targets if isinstance(t, str) and t.strip()]
        state = self.load()
        state.focus_targets = cleaned
        self.save(state)
        return state

    def propose(
        self,
        command: str,
        *,
        reason: str = "",
        target: str = "",
        ttl_seconds: Optional[float] = None,
    ) -> PendingAction:
        """Daemon-side: register a pending action awaiting approval.

        Returns the freshly created :class:`PendingAction` whose
        ``action_id`` the daemon will use when calling
        :func:`wait_for_decision` and :meth:`consume`.
        """
        action = PendingAction(
            action_id=uuid.uuid4().hex[:12],
            command=command,
            reason=reason,
            target=target,
            proposed_at=time.time(),
            ttl_seconds=(
                ttl_seconds if ttl_seconds is not None else PENDING_TTL_DEFAULT_S
            ),
        )
        state = self.load()
        state.pending = action
        self.save(state)
        return action

    def decide(
        self,
        action_id: str,
        decision: str,
        *,
        operator: str = "",
    ) -> Optional[PendingAction]:
        """Operator-side: approve or veto the pending action.

        Returns the updated :class:`PendingAction` or ``None`` when
        there is no pending action with the supplied id.

        Raises:
            ValueError: When ``decision`` is not approved or vetoed.
        """
        if decision not in (DECISION_APPROVED, DECISION_VETOED):
            raise ValueError(
                f"invalid decision '{decision}', expected approved or vetoed"
            )
        state = self.load()
        if state.pending is None or state.pending.action_id != action_id:
            return None
        state.pending.decision = decision
        state.pending.decided_at = time.time()
        state.pending.operator = operator
        self.save(state)
        return state.pending

    def consume(
        self,
        action_id: str,
        *,
        now: Optional[float] = None,
    ) -> Optional[PendingAction]:
        """Daemon-side: read the final decision and clear the slot.

        When the action is still pending but has exceeded its TTL the
        returned :class:`PendingAction` carries ``decision =
        DECISION_EXPIRED``. The pending slot is always cleared so the
        daemon can propose a new action on the next step.

        Args:
            action_id: Identifier returned by :meth:`propose`.
            now: Replaceable wall-clock value, in epoch seconds. When
                ``None`` (production default) ``time.time()`` is used.
                Tests pass an explicit value so expiry can be exercised
                deterministically.
        """
        state = self.load()
        if state.pending is None or state.pending.action_id != action_id:
            return None
        pending = state.pending
        moment = now if now is not None else time.time()
        if pending.decision == DECISION_PENDING and pending.is_expired(now=moment):
            pending.decision = DECISION_EXPIRED
            pending.decided_at = moment
        state.pending = None
        self.save(state)
        return pending

    def is_paused(self) -> bool:
        """Return ``True`` when the daemon must stop before executing."""
        return self.load().mode == MODE_PAUSED

    def is_vetoed(self, command: str) -> bool:
        """Return ``True`` when the command's first token is in the veto list."""
        token = _first_token(command)
        if not token:
            return False
        return token in self.load().vetoed_commands

    def target_in_focus(self, target: str) -> bool:
        """Return ``True`` when no focus is configured or ``target`` is in focus."""
        state = self.load()
        if not state.focus_targets:
            return True
        return target in state.focus_targets


def wait_for_decision(
    control: DaemonControl,
    action: PendingAction,
    *,
    poll_interval: float = APPROVAL_POLL_INTERVAL_S,
    sleep_fn: Callable[[float], None] = time.sleep,
    now_fn: Callable[[], float] = time.time,
) -> PendingAction:
    """Block until the operator decides or the TTL expires.

    The poll interval and clock are injectable so unit tests can drive
    the state machine deterministically without sleeping.

    Args:
        control: :class:`DaemonControl` instance bound to the same
            ``sessions/`` directory the operator surfaces use.
        action: The :class:`PendingAction` previously returned by
            :meth:`DaemonControl.propose`.
        poll_interval: Seconds between state polls.
        sleep_fn: Replaceable ``time.sleep`` for tests.
        now_fn: Replaceable ``time.time`` for tests.

    Returns:
        The final :class:`PendingAction` with ``decision`` set to one
        of :data:`DECISION_APPROVED`, :data:`DECISION_VETOED`, or
        :data:`DECISION_EXPIRED`.
    """
    deadline = action.proposed_at + action.ttl_seconds
    while True:
        state = control.load()
        current = state.pending
        if (
            current is not None
            and current.action_id == action.action_id
            and current.decision != DECISION_PENDING
        ):
            return current
        current_time = now_fn()
        if current_time >= deadline:
            final = control.consume(action.action_id, now=current_time)
            if final is not None:
                return final
            return PendingAction(
                action_id=action.action_id,
                command=action.command,
                reason=action.reason,
                target=action.target,
                proposed_at=action.proposed_at,
                ttl_seconds=action.ttl_seconds,
                decision=DECISION_EXPIRED,
                decided_at=now_fn(),
            )
        sleep_fn(poll_interval)


def wait_until_unpaused(
    control: DaemonControl,
    *,
    poll_interval: float = PAUSE_POLL_INTERVAL_S,
    sleep_fn: Callable[[float], None] = time.sleep,
    max_wait_seconds: Optional[float] = None,
    now_fn: Callable[[], float] = time.time,
) -> bool:
    """Block while the daemon is paused, returning when it resumes.

    Args:
        control: :class:`DaemonControl` instance.
        poll_interval: Seconds between mode checks.
        sleep_fn: Replaceable ``time.sleep`` for tests.
        max_wait_seconds: Optional upper bound. ``None`` waits forever.
        now_fn: Replaceable ``time.time`` for tests.

    Returns:
        ``True`` when the daemon resumed; ``False`` when
        ``max_wait_seconds`` elapsed without a resume signal.
    """
    started = now_fn()
    while control.is_paused():
        if max_wait_seconds is not None and (now_fn() - started) >= max_wait_seconds:
            return False
        sleep_fn(poll_interval)
    return True


__all__ = [
    "APPROVAL_POLL_INTERVAL_S",
    "CONTROL_FILE_NAME",
    "ControlState",
    "DECISION_APPROVED",
    "DECISION_EXPIRED",
    "DECISION_PENDING",
    "DECISION_VETOED",
    "DaemonControl",
    "MODE_APPROVAL",
    "MODE_AUTO",
    "MODE_PAUSED",
    "PAUSE_POLL_INTERVAL_S",
    "PENDING_TTL_DEFAULT_S",
    "PendingAction",
    "VALID_DECISIONS",
    "VALID_MODES",
    "wait_for_decision",
    "wait_until_unpaused",
]
