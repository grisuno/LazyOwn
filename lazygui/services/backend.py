"""Backend abstraction.

Implements the Dependency-Inversion principle for the GUI: panels and windows
only depend on :class:`Backend`, never on a concrete client. Concrete
backends (``LocalPtyBackend``, ``TeamserverBackend``) translate between the
abstract contract and their respective transport.

Backends inherit from :class:`QObject` so they can emit Qt signals that
panels subscribe to. The signals always carry framework-agnostic dataclasses
from :mod:`lazygui.services.models`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from PySide6.QtCore import QObject, Signal

from lazygui.services.models import EventRecord, Listener, Operator, Session


class BackendStatus(str, Enum):
    """Lifecycle state of a backend connection."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DEGRADED = "degraded"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class BackendDescriptor:
    """Read-only description shown in connection dialogs."""

    identifier: str
    display_name: str
    summary: str


class Backend(QObject):
    """Abstract interface every backend implementation must satisfy.

    Subclasses must:

    * implement :meth:`start`, :meth:`stop`, :meth:`send_command`,
      :meth:`refresh`, :meth:`resize_terminal`, :meth:`feed_terminal_input`;
    * emit ``status_changed`` whenever their connection lifecycle moves;
    * emit ``terminal_output`` whenever new bytes are available for the
      terminal widget;
    * emit ``sessions_changed`` / ``listeners_changed`` / ``operator_changed``
      when their snapshot of those collections changes;
    * emit ``event_logged`` to surface log lines in the GUI.

    Signals only carry plain Python dataclasses so the receiving widgets can
    be tested without booting the backend.
    """

    status_changed = Signal(BackendStatus)
    terminal_output = Signal(str)
    sessions_changed = Signal(list)
    listeners_changed = Signal(list)
    operator_changed = Signal(Operator)
    event_logged = Signal(EventRecord)

    def __init__(self, descriptor: BackendDescriptor, parent: QObject | None = None) -> None:
        """Store the descriptor that uniquely identifies this backend."""
        super().__init__(parent)
        self._descriptor = descriptor
        self._status = BackendStatus.DISCONNECTED

    @property
    def descriptor(self) -> BackendDescriptor:
        """Read-only identification for connection dialogs."""
        return self._descriptor

    @property
    def status(self) -> BackendStatus:
        """Current connection lifecycle state."""
        return self._status

    def _set_status(self, new_status: BackendStatus) -> None:
        """Set ``status`` and emit ``status_changed`` only on transition."""
        if new_status == self._status:
            return
        self._status = new_status
        self.status_changed.emit(new_status)

    def start(self) -> None:
        """Establish whatever underlying transport this backend uses."""
        raise NotImplementedError

    def stop(self) -> None:
        """Tear the underlying transport down cleanly."""
        raise NotImplementedError

    def send_command(self, command: str, target_session: str | None = None) -> None:
        """Submit ``command``, optionally scoped to ``target_session``."""
        raise NotImplementedError

    def refresh(self) -> None:
        """Force a re-fetch of sessions, listeners and operator info."""
        raise NotImplementedError

    def resize_terminal(self, columns: int, rows: int) -> None:
        """Inform the backend the terminal area was resized."""
        raise NotImplementedError

    def feed_terminal_input(self, data: str) -> None:
        """Feed raw keystrokes typed by the operator into the terminal."""
        raise NotImplementedError

    def known_sessions(self) -> Sequence[Session]:
        """Return the most recent snapshot of sessions, never ``None``."""
        return ()

    def known_listeners(self) -> Sequence[Listener]:
        """Return the most recent snapshot of listeners, never ``None``."""
        return ()
