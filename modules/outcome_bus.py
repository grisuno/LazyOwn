"""Single fan-out contract for engagement outcomes.

Every exploit, emulation step, chain result and loop finding publishes one
:class:`OutcomeEvent` here. The bus calls the configured sink adapters in
``modules/sinks/`` so the world model, kill-chain, routing priors, C2
surfaces, objectives, event bus, intel graph, attack graph and reports
stay consistent without each caller reimplementing the fan-out.

Sinks are best-effort: one failing surface never blocks the others. The
bus deduplicates identical events inside one process and appends every
decision to ``sessions/outcomes.jsonl`` for audit.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import logging
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("outcome_bus")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
LEDGER_FILENAME = "outcomes.jsonl"
MAX_SEEN = 5000

SINK_LOADERS: dict[str, tuple[str, str]] = {
    "world_model": ("modules.sinks.world_model", "apply"),
    "killchain": ("modules.sinks.killchain", "apply"),
    "findings": ("modules.sinks.findings", "apply"),
    "routing": ("modules.sinks.routing", "apply"),
    "c2_surfaces": ("modules.sinks.c2_surfaces", "apply"),
    "objectives": ("modules.sinks.objectives", "apply"),
    "event_bus": ("modules.sinks.event_bus", "apply"),
    "intel_graph": ("modules.sinks.intel_graph", "apply"),
    "attack_graph": ("modules.sinks.attack_graph", "apply"),
    "world_diff": ("modules.sinks.world_diff", "apply"),
    "beacon_dispatch": ("modules.sinks.beacon_dispatch", "apply"),
    "report": ("modules.sinks.report", "apply"),
    "campaign_db": ("modules.sinks.campaign_db", "apply"),
    "chain_feed": ("modules.sinks.chain_feed", "apply"),
}

DEFAULT_SINKS = tuple(name for name in SINK_LOADERS if name != "campaign_db")

_SEVERITY = {
    "critical": "critical",
    "high": "high",
    "medium": "warning",
    "low": "info",
    "info": "info",
    "informational": "info",
}

_CATEGORY = {
    "shell": "exploit",
    "exploit": "exploit",
    "emulation": "exploit",
    "chain": "exploit",
    "finding": "finding",
    "report": "report",
    "loot": "loot",
    "credential": "credential",
    "discovery": "recon",
    "ctf_capture": "exploit",
}


@dataclass
class OutcomeEvent:
    """One engagement outcome ready for sink fan-out."""

    kind: str = "finding"
    target: str = ""
    host: str = ""
    task_id: str = ""
    intent_id: int = 0
    title: str = ""
    description: str = ""
    severity: str = "medium"
    cve: str = ""
    mitre_id: str = ""
    confidence: float = 1.0
    success: bool = False
    shell: bool = False
    source: str = "outcome_bus"
    command: str = ""
    output: str = ""
    port: str = ""
    protocol: str = "tcp"
    service: str = ""
    banner: str = ""
    artifacts: list[str] = field(default_factory=list)
    sinks: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def host_value(self) -> str:
        """Return the best host identifier available."""
        return self.host or self.target

    def key(self) -> str:
        """Return the idempotency key for this event."""
        body = {
            "kind": self.kind,
            "host": self.host_value,
            "title": self.title,
            "cve": self.cve,
            "mitre": self.mitre_id,
            "source": self.source,
            "shell": self.shell,
            "success": self.success,
            "port": self.port,
            "service": self.service,
            "command": self.command[:500],
        }
        blob = json.dumps(body, sort_keys=True, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:24]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "kind": self.kind,
            "target": self.target,
            "host": self.host_value,
            "task_id": self.task_id,
            "intent_id": self.intent_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "cve": self.cve,
            "mitre_id": self.mitre_id,
            "confidence": self.confidence,
            "success": self.success,
            "shell": self.shell,
            "source": self.source,
            "command": self.command,
            "output": self.output,
            "port": self.port,
            "protocol": self.protocol,
            "service": self.service,
            "banner": self.banner,
            "artifacts": list(self.artifacts),
            "sinks": list(self.sinks),
            "metadata": dict(self.metadata),
        }


class OutcomeBus:
    """Fan out outcome events to every configured sink."""

    def __init__(
        self,
        ledger_path: Path | str | None = None,
        sink_map: dict[str, Any] | None = None,
    ) -> None:
        """Bind the audit ledger and an optional sink map for tests."""
        self.ledger_path = Path(ledger_path) if ledger_path else SESSIONS_DIR / LEDGER_FILENAME
        self._sink_map = dict(sink_map or {})
        self._seen: OrderedDict[str, dict[str, bool]] = OrderedDict()
        self._inflight: set[str] = set()
        self._lock = threading.Lock()
        self._ledger_lock = threading.Lock()

    def reset(self) -> None:
        """Clear the in-process dedupe cache."""
        with self._lock:
            self._seen.clear()
            self._inflight.clear()

    def _sink(self, name: str):
        """Resolve one sink callable from the injection map or module loader."""
        if name in self._sink_map:
            return self._sink_map[name]
        loader = SINK_LOADERS.get(name)
        if loader is None:
            return None
        module_name, attribute = loader
        try:
            module = importlib.import_module(module_name)
            return getattr(module, attribute, None)
        except Exception as exc:
            log.debug("sink %s unavailable: %s", name, exc)
            return None

    def _enabled_sinks(self, requested: list[str] | None = None) -> list[str]:
        """Return the ordered sink names after payload toggles and overrides."""
        names = list(requested or DEFAULT_SINKS)
        try:
            from modules import orchestrator_config

            toggles = orchestrator_config.sinks()
        except Exception:
            toggles = {}
        return [name for name in names if bool(toggles.get(name, True))]

    def record(self, event: OutcomeEvent, sinks: list[str] | None = None) -> dict[str, bool]:
        """Publish one event to every enabled sink.

        Args:
            event: Outcome payload.
            sinks: Optional explicit sink list; defaults to the event tags
                merged with the global sink list.

        Returns:
            Mapping of sink name to success. ``_deduplicated`` is true when
            the same event was already processed in this process.
        """
        requested = list(sinks or [])
        if not requested:
            requested = list(dict.fromkeys([*DEFAULT_SINKS, *event.sinks]))
        names = self._enabled_sinks(requested)
        key = f"{event.key()}|{','.join(sorted(names))}"
        with self._lock:
            cached = self._seen.get(key)
            if cached is not None:
                return {**cached, "_deduplicated": True}
            if key in self._inflight:
                return {"_deduplicated": True}
            self._inflight.add(key)
        statuses: dict[str, bool] = {}
        try:
            for name in names:
                sink = self._sink(name)
                if sink is None:
                    statuses[name] = False
                    continue
                try:
                    statuses[name] = bool(sink(event))
                except Exception as exc:
                    log.debug("sink %s failed: %s", name, exc)
                    statuses[name] = False
            self._append_ledger(event, statuses)
            with self._lock:
                if statuses and all(statuses.values()):
                    self._seen[key] = dict(statuses)
                    while len(self._seen) > MAX_SEEN:
                        self._seen.popitem(last=False)
            return statuses
        finally:
            with self._lock:
                self._inflight.discard(key)

    def _append_ledger(self, event: OutcomeEvent, statuses: dict[str, bool]) -> None:
        """Append one auditable row without raising."""
        try:
            with self._ledger_lock:
                self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
                row = {
                    "ts": time.time(),
                    "ts_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                    "event": event.to_dict(),
                    "sinks": dict(statuses),
                }
                with self.ledger_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
        except Exception as exc:
            log.debug("outcome ledger write failed: %s", exc)


_BUS: OutcomeBus | None = None
_BUS_LOCK = threading.Lock()


def get_bus() -> OutcomeBus:
    """Return the process-wide outcome bus."""
    global _BUS
    with _BUS_LOCK:
        if _BUS is None:
            _BUS = OutcomeBus()
        return _BUS


def reset_bus() -> None:
    """Reset the process-wide bus cache (tests and long-lived operators)."""
    get_bus().reset()


def record(event: OutcomeEvent, sinks: list[str] | None = None) -> dict[str, bool]:
    """Publish one event through the process-wide bus."""
    return get_bus().record(event, sinks=sinks)


def record_event(**kwargs: Any) -> dict[str, bool]:
    """Build and publish one event from keyword fields."""
    return record(OutcomeEvent(**kwargs))


def severity_for_event(severity: str) -> str:
    """Map an outcome severity to the event-bus severity vocabulary."""
    return _SEVERITY.get(str(severity or "").lower(), "info")


def category_for_event(kind: str) -> str:
    """Map an outcome kind to the event-bus category vocabulary."""
    return _CATEGORY.get(str(kind or "").lower(), "system")


__all__ = [
    "DEFAULT_SINKS",
    "OutcomeBus",
    "OutcomeEvent",
    "SESSIONS_DIR",
    "SINK_LOADERS",
    "category_for_event",
    "get_bus",
    "record",
    "record_event",
    "reset_bus",
    "severity_for_event",
]
