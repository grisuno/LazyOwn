"""Immutable domain types consumed by the UI.

These dataclasses are deliberately framework-agnostic. They never carry Qt
references so they can be created from threads or background workers without
touching the GUI loop. Widgets adapt them at the edge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping


class BackendKind(str, Enum):
    """Stable identifiers for the backend implementations."""

    LOCAL = "local"
    TEAMSERVER = "teamserver"


class EventLevel(str, Enum):
    """Severity levels for :class:`EventRecord`. Order matters for filtering."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    @property
    def numeric(self) -> int:
        """Numeric rank used to compare severity."""
        return _LEVEL_ORDER[self]


_LEVEL_ORDER: dict[EventLevel, int] = {
    EventLevel.DEBUG: 0,
    EventLevel.INFO: 1,
    EventLevel.WARNING: 2,
    EventLevel.ERROR: 3,
    EventLevel.CRITICAL: 4,
}


@dataclass(frozen=True, slots=True)
class Session:
    """A connected implant/session as reported by the backend."""

    identifier: str
    hostname: str
    operating_system: str
    process_id: str
    user: str
    ip_addresses: str
    discovered_ips: str
    last_command: str
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Listener:
    """A C2 listener (HTTP/HTTPS/DNS/TCP) advertised by the backend."""

    identifier: str
    kind: str
    address: str
    port: int
    is_secure: bool
    description: str = ""


@dataclass(frozen=True, slots=True)
class Operator:
    """An operator account known to the teamserver."""

    name: str
    role: str
    is_authenticated: bool
    karma_name: str = ""
    elo: int = 0


@dataclass(frozen=True, slots=True)
class EventRecord:
    """A single line in the event log."""

    timestamp: datetime
    level: EventLevel
    source: str
    message: str

    @classmethod
    def now(cls, level: EventLevel, source: str, message: str) -> "EventRecord":
        """Construct a record stamped with the current UTC time."""
        return cls(timestamp=datetime.now(tz=timezone.utc), level=level, source=source, message=message)
