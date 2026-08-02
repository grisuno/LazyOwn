"""Immutable domain types consumed by the UI.

These dataclasses are deliberately framework-agnostic. They never carry Qt
references so they can be created from threads or background workers without
touching the GUI loop. Widgets adapt them at the edge.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class BackendKind(StrEnum):
    """Stable identifiers for the backend implementations."""

    LOCAL = "local"
    TEAMSERVER = "teamserver"


class EventLevel(StrEnum):
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
    def now(cls, level: EventLevel, source: str, message: str) -> EventRecord:
        """Construct a record stamped with the current UTC time."""
        return cls(timestamp=datetime.now(tz=UTC), level=level, source=source, message=message)


@dataclass(frozen=True, slots=True)
class GraphNode:
    """A node in the attack topography graph."""

    identifier: str
    label: str
    node_type: str
    shape: str = "dot"
    color: str = "#58a6ff"
    metadata: Mapping[str, str] = field(default_factory=dict)
    icon: str = ""


@dataclass(frozen=True, slots=True)
class GraphEdge:
    """An edge connecting two graph nodes."""

    source_id: str
    target_id: str
    label: str = ""
    edge_type: str = "default"
    color: str = "#30363d"


@dataclass(frozen=True, slots=True)
class Topology:
    """Complete graph topology from the teamserver."""

    nodes: Sequence[GraphNode] = ()
    edges: Sequence[GraphEdge] = ()

    @classmethod
    def empty(cls) -> Topology:
        """Return an empty topology."""
        return cls()


@dataclass(frozen=True, slots=True)
class DashboardPayload:
    """Aggregated dashboard data from ``/api/dashboard``."""

    connected_clients: Sequence[str] = ()
    beacon_count: int = 0
    events: Sequence[EventRecord] = ()
    campaign_state: Mapping[str, Any] = field(default_factory=dict)
    facts_count: int = 0
    last_update: str = ""


@dataclass(frozen=True, slots=True)
class CampaignSummary:
    """Campaign status from the backend."""

    identifier: str
    name: str
    status: str
    playbook: str
    objectives_total: int = 0
    objectives_completed: int = 0
    target_count: int = 0


@dataclass(frozen=True, slots=True)
class BeaconResult:
    """Command result returned by a beacon."""

    client_id: str
    output: str
    command: str
    operating_system: str = ""
    hostname: str = ""
    user: str = ""
    ips: str = ""
    pid: str = ""
    discovered_ips: str = ""
    result_portscan: str = ""
    result_pwd: str = ""
