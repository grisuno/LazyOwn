"""
UnifiedEventBus — central nervous system connecting all LazyOwn components.

Replaces the fragmented event systems (collab_bp.EventBus, engagement_hooks,
event_engine) with a single typed pub/sub bus that CLI, C2, MCP, autonomous
agents, and bridges all share.

Design (SOLID)
--------------
- Single Responsibility : UnifiedEventBus owns only event routing + persistence.
- Open/Closed           : new event types/categories added without modifying bus.
- Liskov                : all subscribers honour Callable[[LazyEvent], None].
- Interface Segregation : subscribe/unsubscribe/publish are the only surface.
- Dependency Inversion  : bus depends on abstract Sink, not concrete backends.

Thread-safe. Async-compatible. Worker-based dispatch with backpressure via
a bounded queue. Persists to sessions/events.jsonl.
"""

from __future__ import annotations

import json
import logging
import queue
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

log = logging.getLogger("event_bus")

_LAZYOWN_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
_EVENTS_FILE = _SESSIONS_DIR / "events.jsonl"

MAX_HISTORY = 1000
MAX_QUEUE_PER_SUB = 500
DISPATCH_QUEUE_SIZE = 500


class EventCategory(str, Enum):
    COMMAND = "command"
    RECON = "recon"
    SCAN = "scan"
    ENUM = "enum"
    EXPLOIT = "exploit"
    POST_EXPLOIT = "post_exploit"
    PERSIST = "persist"
    PRIVESC = "privesc"
    CREDENTIAL = "credential"
    LATERAL = "lateral"
    EXFIL = "exfil"
    C2 = "c2"
    BEACON = "beacon"
    PHASE = "phase"
    SYSTEM = "system"
    ERROR = "error"
    FINDING = "finding"
    LOCK = "lock"
    CHAT = "chat"
    DISCOVERY = "discovery"
    VULN = "vuln"
    LOOT = "loot"
    REPORT = "report"


class EventSeverity(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class LazyEvent:
    """Universal event envelope for all LazyOwn components."""
    category: EventCategory
    event_type: str
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    severity: EventSeverity = EventSeverity.INFO
    ts: float = field(default_factory=time.time)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    session_id: str = ""
    target: str = ""
    operator: str = "system"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ts": self.ts,
            "ts_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(self.ts)),
            "category": self.category.value,
            "event_type": self.event_type,
            "source": self.source,
            "severity": self.severity.value,
            "payload": self.payload,
            "session_id": self.session_id,
            "target": self.target,
            "operator": self.operator,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LazyEvent:
        return cls(
            id=d.get("id", uuid.uuid4().hex[:12]),
            ts=d.get("ts", time.time()),
            category=EventCategory(d.get("category", "system")),
            event_type=d.get("event_type", "unknown"),
            source=d.get("source", "unknown"),
            severity=EventSeverity(d.get("severity", "info")),
            payload=d.get("payload", {}),
            session_id=d.get("session_id", ""),
            target=d.get("target", ""),
            operator=d.get("operator", "system"),
        )


Subscriber = Callable[[LazyEvent], None]


class Sink(ABC):
    """Abstract sink for persisting or forwarding events."""

    @abstractmethod
    def write(self, event: LazyEvent) -> None: ...

    @abstractmethod
    def close(self) -> None: ...


class JsonlSink(Sink):
    """Persists events to sessions/events.jsonl (append-only)."""

    def __init__(self, filepath: Path = _EVENTS_FILE) -> None:
        self._filepath = filepath
        self._lock = threading.Lock()
        self._filepath.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: LazyEvent) -> None:
        with self._lock:
            try:
                with open(self._filepath, "a", encoding="utf-8") as fh:
                    fh.write(event.to_json() + "\n")
            except OSError:
                log.exception("Failed to persist event %s", event.id)

    def close(self) -> None:
        pass


class CollabBusSink(Sink):
    """Forwards LazyEvents to the existing collab_bp.EventBus for SSE streaming."""

    def __init__(self) -> None:
        self._collab_bus = None

    @property
    def _bus(self):
        if self._collab_bus is None:
            try:
                from collab_bp import ColabEvent, get_event_bus
                self._collab_bus = get_event_bus()
                self._ColabEvent = ColabEvent
            except ImportError:
                self._collab_bus = False
        return self._collab_bus if self._collab_bus is not False else None

    def write(self, event: LazyEvent) -> None:
        bus = self._bus
        if bus is None:
            return
        try:
            bus.publish(self._ColabEvent(
                type=f"{event.category.value}:{event.event_type}",
                payload=event.payload,
                operator=event.operator,
                ts=event.ts,
                id=event.id,
            ))
        except Exception:
            log.debug("CollabBusSink forward failed", exc_info=True)

    def close(self) -> None:
        pass


class EngagementSink(Sink):
    """Forwards LazyEvents to the engagement_hooks narrator."""

    def write(self, event: LazyEvent) -> None:
        try:
            from engagement_hooks import EngagementNarrator
            narrator = EngagementNarrator.instance()
            if event.category in (EventCategory.EXPLOIT, EventCategory.BEACON,
                                  EventCategory.PRIVESC, EventCategory.CREDENTIAL):
                narrator.narrate(
                    event_type=event.event_type,
                    source=event.source,
                    target=event.target,
                    details=event.payload,
                    severity=event.severity.value,
                )
        except Exception:
            log.debug("EngagementSink forward failed", exc_info=True)

    def close(self) -> None:
        pass


class UnifiedEventBus:
    """Central event bus for all LazyOwn components.

    Events are queued on a bounded ``queue.Queue`` (backpressure) and
    dispatched by a dedicated worker thread. This decouples publish()
    latency from subscriber execution speed and provides natural
    backpressure when subscribers fall behind.

    Usage::

        bus = get_event_bus()
        bus.subscribe("my_module", lambda ev: print(ev.event_type))
        bus.publish(LazyEvent(
            category=EventCategory.RECON,
            event_type="scan_complete",
            source="lazynmap",
            payload={"host": "10.0.0.1", "ports": [22, 80, 445]},
        ))
    """

    _instance: UnifiedEventBus | None = None
    _instance_lock = threading.Lock()

    _SHUTDOWN_SENTINEL = "__event_bus_shutdown__"

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)
        self._topic_subscribers: dict[str, list[Subscriber]] = defaultdict(list)
        self._async_queues: dict[str, queue.Queue] = {}
        self._history: list[LazyEvent] = []
        self._sinks: list[Sink] = []
        self._running = True
        self._dispatch_queue: queue.Queue = queue.Queue(maxsize=DISPATCH_QUEUE_SIZE)
        self._worker: threading.Thread | None = None
        self._init_sinks()
        self._worker = threading.Thread(
            target=self._dispatch_loop,
            daemon=True,
            name="lazyown-eventbus-worker",
        )
        self._worker.start()

    def _init_sinks(self) -> None:
        self._sinks.append(JsonlSink())

        try:
            self._sinks.append(CollabBusSink())
        except Exception:
            log.debug("CollabBusSink not available")

        try:
            self._sinks.append(EngagementSink())
        except Exception:
            log.debug("EngagementSink not available")

    @classmethod
    def instance(cls) -> UnifiedEventBus:
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def subscriber_count(self) -> int:
        """Return the number of active subscribers across all registration types."""
        with self._lock:
            return (
                len(self._subscribers)
                + len(self._topic_subscribers)
                + len(self._async_queues)
            )

    def subscribe(self, subscriber_id: str, callback: Subscriber) -> None:
        """Register a callback for all events."""
        with self._lock:
            self._subscribers[subscriber_id].append(callback)

    def subscribe_topic(self, subscriber_id: str, topic: str, callback: Subscriber) -> None:
        """Register a callback for events matching a topic.

        Topics are dotted strings like 'recon.nmap' or 'beacon.*'.
        Wildcards: '*' matches any single segment, '**' matches everything.
        """
        with self._lock:
            key = f"{subscriber_id}:{topic}"
            self._topic_subscribers[key].append(callback)

    def subscribe_async(self, subscriber_id: str) -> queue.Queue:
        """Get a Queue for async event consumption (for SSE, WebSocket, etc.)."""
        q: queue.Queue = queue.Queue(maxsize=MAX_QUEUE_PER_SUB)
        with self._lock:
            self._async_queues[subscriber_id] = q
            for ev in self._history[-20:]:
                try:
                    q.put_nowait(ev)
                except queue.Full:
                    break
        return q

    def unsubscribe(self, subscriber_id: str) -> None:
        """Remove all subscriptions for a subscriber."""
        with self._lock:
            self._subscribers.pop(subscriber_id, None)
            keys_to_remove = [k for k in self._topic_subscribers
                              if k.startswith(f"{subscriber_id}:")]
            for k in keys_to_remove:
                self._topic_subscribers.pop(k, None)
            self._async_queues.pop(subscriber_id, None)

    def publish(self, event: LazyEvent) -> None:
        """Publish an event via the bounded dispatch queue.

        Appends to history immediately. The event is then placed on the
        internal dispatch queue for worker-thread delivery to subscribers
        and sinks.  When the queue is full this call blocks, providing
        natural backpressure.

        Args:
            event: The event to publish.
        """
        with self._lock:
            self._history.append(event)
            if len(self._history) > MAX_HISTORY:
                self._history = self._history[-MAX_HISTORY:]

        self._dispatch_queue.put(event)

    def drain(self) -> None:
        """Consume and drop all pending events from the dispatch queue.

        Already-delivered events that were dispatched before the drain
        call are not affected.  History is preserved so post-drain
        queries can still see what was published.
        """
        dropped = 0
        while not self._dispatch_queue.empty():
            try:
                self._dispatch_queue.get_nowait()
                self._dispatch_queue.task_done()
                dropped += 1
            except queue.Empty:
                break
        if dropped:
            log.info("Drained %d pending events from dispatch queue", dropped)

    def shutdown(self) -> None:
        """Shut down the event bus cleanly.

        1. Marks the bus as stopped.
        2. Sends a shutdown sentinel through the dispatch queue so the
           worker thread can notify all subscribers and exit.
        3. Joins the worker thread (with a timeout).
        4. Closes all sinks and clears subscriber registrations.

        Thread-safe. Idempotent.
        """
        if not self._running:
            return
        self._running = False

        shutdown_event = LazyEvent(
            category=EventCategory.SYSTEM,
            event_type=self._SHUTDOWN_SENTINEL,
            source="event_bus",
            payload={"action": "shutdown"},
        )
        try:
            self._dispatch_queue.put(shutdown_event, timeout=2)
        except queue.Full:
            log.warning("Dispatch queue full during shutdown; draining first")
            self.drain()
            try:
                self._dispatch_queue.put(shutdown_event, timeout=2)
            except queue.Full:
                log.error("Could not enqueue shutdown sentinel; forcing stop")

        if self._worker and self._worker.is_alive():
            self._worker.join(timeout=5)

        with self._lock:
            for sink in self._sinks:
                try:
                    sink.close()
                except Exception:
                    pass
            self._subscribers.clear()
            self._topic_subscribers.clear()
            self._async_queues.clear()

    def _dispatch_loop(self) -> None:
        """Worker loop consuming events from ``_dispatch_queue``.

        Processes events one at a time, delivering to all subscribers,
        topic subscribers, async queues, and sinks. Stops when the
        shutdown sentinel is received or ``_running`` becomes ``False``.
        """
        while self._running:
            try:
                event = self._dispatch_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            try:
                if (
                    event.category == EventCategory.SYSTEM
                    and event.event_type == self._SHUTDOWN_SENTINEL
                ):
                    self._notify_shutdown()
                    self._dispatch_queue.task_done()
                    break

                self._dispatch_event(event)
            except Exception:
                log.exception("Unhandled exception in dispatch loop")
            finally:
                self._dispatch_queue.task_done()

    def _dispatch_event(self, event: LazyEvent) -> None:
        """Deliver a single event to every registered consumer."""
        with self._lock:
            subs = list(self._subscribers.items())
            topic_subs = list(self._topic_subscribers.items())
            async_qs = list(self._async_queues.items())

        for sid, callbacks in subs:
            for cb in callbacks:
                try:
                    cb(event)
                except Exception:
                    log.debug("Subscriber %s callback failed", sid, exc_info=True)

        for key, callbacks in topic_subs:
            parts = key.split(":", 1)
            if len(parts) != 2:
                continue
            _, topic = parts
            if self._match_topic(topic, event):
                for cb in callbacks:
                    try:
                        cb(event)
                    except Exception:
                        log.debug("Topic subscriber %s failed", key, exc_info=True)

        for sid, q in async_qs:
            try:
                q.put_nowait(event)
            except queue.Full:
                log.debug("Async queue full for %s", sid)

        for sink in self._sinks:
            try:
                sink.write(event)
            except Exception:
                log.debug("Sink write failed", exc_info=True)

    def _notify_shutdown(self) -> None:
        """Notify all subscribers that the bus is shutting down."""
        shutdown_notice = LazyEvent(
            category=EventCategory.SYSTEM,
            event_type="shutdown",
            source="event_bus",
            payload={"action": "shutdown"},
        )
        with self._lock:
            subs = list(self._subscribers.items())
            topic_subs = list(self._topic_subscribers.items())
            async_qs = list(self._async_queues.items())

        for sid, callbacks in subs:
            for cb in callbacks:
                try:
                    cb(shutdown_notice)
                except Exception:
                    log.debug("Shutdown notify %s failed", sid, exc_info=True)

        for key, callbacks in topic_subs:
            parts = key.split(":", 1)
            if len(parts) != 2:
                continue
            _, topic = parts
            if self._match_topic(topic, shutdown_notice):
                for cb in callbacks:
                    try:
                        cb(shutdown_notice)
                    except Exception:
                        log.debug("Shutdown topic notify %s failed", key, exc_info=True)

        for sid, q in async_qs:
            try:
                q.put_nowait(shutdown_notice)
            except queue.Full:
                log.debug("Async queue full during shutdown notify for %s", sid)

    def _match_topic(self, topic: str, event: LazyEvent) -> bool:
        """Match a dotted topic pattern against an event.

        The event's topic is '{category.value}.{event_type}'.
        Supports '*' (single segment) and '**' (any depth) wildcards.
        """
        if topic == "**":
            return True

        event_topic = f"{event.category.value}.{event.event_type}"
        topic_parts = topic.split(".")
        event_parts = event_topic.split(".")

        ti = 0
        ei = 0
        while ti < len(topic_parts) and ei < len(event_parts):
            tp = topic_parts[ti]
            if tp == "**":
                if ti == len(topic_parts) - 1:
                    return True
                ti += 1
                if ti >= len(topic_parts):
                    return True
                next_tp = topic_parts[ti]
                while ei < len(event_parts) and event_parts[ei] != next_tp:
                    ei += 1
                if ei >= len(event_parts):
                    return False
            elif tp == "*":
                ti += 1
                ei += 1
            elif tp == event_parts[ei]:
                ti += 1
                ei += 1
            else:
                return False

        return ti == len(topic_parts) and ei == len(event_parts)

    def history(self, n: int = 50, category: EventCategory | None = None) -> list[LazyEvent]:
        """Return recent events, optionally filtered by category."""
        with self._lock:
            events = list(self._history[-n:])
        if category:
            events = [e for e in events if e.category == category]
        return events

    def history_since(self, since_ts: float) -> list[LazyEvent]:
        """Return all events since a given timestamp."""
        with self._lock:
            return [e for e in self._history if e.ts >= since_ts]


def get_event_bus() -> UnifiedEventBus:
    """Return the singleton UnifiedEventBus instance."""
    return UnifiedEventBus.instance()


def publish_event(
    category: EventCategory | str,
    event_type: str,
    source: str = "system",
    payload: dict[str, Any] | None = None,
    severity: EventSeverity | str = EventSeverity.INFO,
    target: str = "",
    operator: str = "system",
) -> LazyEvent:
    """Convenience function to build and publish an event in one call."""
    if isinstance(category, str):
        category = EventCategory(category)
    if isinstance(severity, str):
        severity = EventSeverity(severity)
    event = LazyEvent(
        category=category,
        event_type=event_type,
        source=source,
        payload=payload or {},
        severity=severity,
        target=target,
        operator=operator,
    )
    get_event_bus().publish(event)
    return event
