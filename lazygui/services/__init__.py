"""Service layer.

Defines the domain types the GUI consumes and the backend abstraction that
hides whether commands are issued to a local cmd2 console (PTY) or a remote
LazyOwn teamserver (HTTP/WebSocket).

The :class:`Backend` Protocol is the only contract the UI knows about. New
backend implementations only need to satisfy that contract to be plugged in.
"""

from lazygui.services.backend import Backend, BackendStatus
from lazygui.services.event_log import EventLog
from lazygui.services.factory import BackendFactory
from lazygui.services.local_backend import LocalPtyBackend
from lazygui.services.models import (
    BackendKind,
    EventLevel,
    EventRecord,
    Listener,
    Operator,
    Session,
)
from lazygui.services.teamserver_backend import TeamserverBackend

__all__ = [
    "Backend",
    "BackendStatus",
    "BackendKind",
    "BackendFactory",
    "EventLevel",
    "EventLog",
    "EventRecord",
    "Listener",
    "LocalPtyBackend",
    "Operator",
    "Session",
    "TeamserverBackend",
]
