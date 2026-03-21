#!/usr/bin/env python3
"""
modules/collab_bp.py
====================
Multi-operator collaboration layer for LazyOwn.

Provides:
- Server-Sent Events (SSE) stream at /collab/stream  -- real-time broadcast to all operators
- Target locking  at /collab/lock / /collab/unlock   -- prevents two operators executing same target
- Operator registry at /collab/operators             -- who is currently connected
- Event bus at /collab/publish                       -- any module can push structured events

Design (SOLID)
--------------
- SRP : EventBus, LockManager, OperatorRegistry are independent classes
- OCP : new event types added by publishing with a new "type" field
- LSP : OperatorRegistry and LockManager share a common Resettable interface
- ISP : consumers only import the blueprint; internal classes are not exposed
- DIP : Blueprint depends on injected EventBus / LockManager instances (testable)

Usage
-----
In lazyc2.py:

    try:
        from collab_bp import collab_bp
        app.register_blueprint(collab_bp, url_prefix="/collab")
    except Exception as err:
        print(f"[collab] Blueprint not loaded: {err}")

JavaScript (operator dashboard):

    const es = new EventSource("/collab/stream?operator=alice");
    es.onmessage = e => console.log(JSON.parse(e.data));
"""
from __future__ import annotations

import json
import logging
import queue
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from flask import Blueprint, Response, jsonify, request, stream_with_context

log = logging.getLogger("collab_bp")

# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclass
class ColabEvent:
    type:      str               # "command", "finding", "lock", "chat", "phase_change"
    payload:   dict
    operator:  str  = "system"
    ts:        float = field(default_factory=time.time)
    id:        str   = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_sse(self) -> str:
        data = json.dumps(asdict(self))
        return f"id: {self.id}\ndata: {data}\n\n"


@dataclass
class OperatorInfo:
    name:       str
    joined_at:  float = field(default_factory=time.time)
    last_seen:  float = field(default_factory=time.time)
    active:     bool  = True


# ---------------------------------------------------------------------------
# EventBus
# ---------------------------------------------------------------------------

class EventBus:
    """
    In-process pub/sub bus.
    Each subscriber gets its own Queue; publish() fans out to all queues.
    Thread-safe.
    """
    _MAX_QUEUE = 200
    _STALE_SECS = 120

    def __init__(self) -> None:
        self._lock:   threading.RLock                = threading.RLock()
        self._queues: Dict[str, queue.Queue]          = {}
        self._history: List[ColabEvent]              = []

    def subscribe(self, subscriber_id: str) -> queue.Queue:
        q: queue.Queue = queue.Queue(maxsize=self._MAX_QUEUE)
        with self._lock:
            self._queues[subscriber_id] = q
            # replay last 20 events so new operators catch up
            for ev in self._history[-20:]:
                try:
                    q.put_nowait(ev)
                except queue.Full:
                    pass
        return q

    def unsubscribe(self, subscriber_id: str) -> None:
        with self._lock:
            self._queues.pop(subscriber_id, None)

    def publish(self, event: ColabEvent) -> None:
        with self._lock:
            self._history.append(event)
            if len(self._history) > 500:
                self._history = self._history[-500:]
            dead = []
            for sid, q in self._queues.items():
                try:
                    q.put_nowait(event)
                except queue.Full:
                    dead.append(sid)
            for sid in dead:
                log.debug("Dropping stale subscriber %s", sid)
                self._queues.pop(sid, None)

    def recent(self, n: int = 50) -> List[ColabEvent]:
        with self._lock:
            return list(self._history[-n:])

    def reset(self) -> None:
        with self._lock:
            self._queues.clear()
            self._history.clear()


# ---------------------------------------------------------------------------
# LockManager
# ---------------------------------------------------------------------------

@dataclass
class TargetLock:
    target:   str
    operator: str
    acquired: float = field(default_factory=time.time)
    ttl_secs: int   = 300


class LockManager:
    """
    Per-target advisory locks. Prevents two operators running tools
    against the same host simultaneously.
    """

    def __init__(self) -> None:
        self._lock:  threading.RLock           = threading.RLock()
        self._locks: Dict[str, TargetLock]     = {}

    def acquire(self, target: str, operator: str, ttl_secs: int = 300) -> bool:
        with self._lock:
            self._expire()
            if target in self._locks:
                existing = self._locks[target]
                if existing.operator == operator:
                    existing.acquired = time.time()
                    return True
                return False
            self._locks[target] = TargetLock(target, operator, ttl_secs=ttl_secs)
            return True

    def release(self, target: str, operator: str) -> bool:
        with self._lock:
            lock = self._locks.get(target)
            if lock and lock.operator == operator:
                del self._locks[target]
                return True
            return False

    def status(self, target: str) -> Optional[TargetLock]:
        with self._lock:
            self._expire()
            return self._locks.get(target)

    def all_locks(self) -> List[TargetLock]:
        with self._lock:
            self._expire()
            return list(self._locks.values())

    def _expire(self) -> None:
        now = time.time()
        expired = [t for t, l in self._locks.items() if now - l.acquired > l.ttl_secs]
        for t in expired:
            log.debug("Lock on %s expired", t)
            del self._locks[t]

    def reset(self) -> None:
        with self._lock:
            self._locks.clear()


# ---------------------------------------------------------------------------
# OperatorRegistry
# ---------------------------------------------------------------------------

class OperatorRegistry:
    """Tracks which operators are currently connected."""

    _STALE_SECS = 90

    def __init__(self) -> None:
        self._lock:      threading.RLock              = threading.RLock()
        self._operators: Dict[str, OperatorInfo]      = {}

    def join(self, name: str) -> OperatorInfo:
        with self._lock:
            if name in self._operators:
                op = self._operators[name]
                op.active    = True
                op.last_seen = time.time()
            else:
                op = OperatorInfo(name=name)
                self._operators[name] = op
            return op

    def heartbeat(self, name: str) -> None:
        with self._lock:
            if name in self._operators:
                self._operators[name].last_seen = time.time()
                self._operators[name].active    = True

    def leave(self, name: str) -> None:
        with self._lock:
            if name in self._operators:
                self._operators[name].active = False

    def active_operators(self) -> List[OperatorInfo]:
        with self._lock:
            self._expire()
            return [o for o in self._operators.values() if o.active]

    def _expire(self) -> None:
        now = time.time()
        for op in self._operators.values():
            if now - op.last_seen > self._STALE_SECS:
                op.active = False

    def reset(self) -> None:
        with self._lock:
            self._operators.clear()


# ---------------------------------------------------------------------------
# Module-level singletons (injected into Blueprint via closure)
# ---------------------------------------------------------------------------

_bus      = EventBus()
_locks    = LockManager()
_registry = OperatorRegistry()


def get_event_bus()       -> EventBus:        return _bus
def get_lock_manager()    -> LockManager:     return _locks
def get_operator_registry() -> OperatorRegistry: return _registry


def publish_event(type: str, payload: dict, operator: str = "system") -> None:
    """Module-level convenience for other modules to broadcast events."""
    _bus.publish(ColabEvent(type=type, payload=payload, operator=operator))


# ---------------------------------------------------------------------------
# Blueprint
# ---------------------------------------------------------------------------

collab_bp = Blueprint("collab", __name__)


@collab_bp.route("/stream")
def stream():
    """SSE endpoint. Each connected operator subscribes here."""
    operator = request.args.get("operator", "anonymous")
    _registry.join(operator)
    _bus.publish(ColabEvent(
        type="operator_joined",
        payload={"operator": operator, "active_count": len(_registry.active_operators())},
        operator="system",
    ))
    sub_id = f"{operator}_{uuid.uuid4().hex[:6]}"
    q = _bus.subscribe(sub_id)

    def generate():
        # Send a keepalive comment every 15 s so proxies don't kill the connection
        try:
            yield ": keepalive\n\n"
            while True:
                try:
                    event: ColabEvent = q.get(timeout=15)
                    yield event.to_sse()
                except queue.Empty:
                    yield ": keepalive\n\n"
                    _registry.heartbeat(operator)
        finally:
            _bus.unsubscribe(sub_id)
            _registry.leave(operator)
            _bus.publish(ColabEvent(
                type="operator_left",
                payload={"operator": operator},
                operator="system",
            ))

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control":   "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@collab_bp.route("/operators")
def operators():
    active = _registry.active_operators()
    return jsonify({
        "count":     len(active),
        "operators": [{"name": o.name, "joined_at": o.joined_at, "last_seen": o.last_seen}
                      for o in active],
    })


@collab_bp.route("/publish", methods=["POST"])
def publish():
    """Any operator or module can push a structured event."""
    data     = request.get_json(force=True, silent=True) or {}
    etype    = str(data.get("type", "generic"))[:64]
    payload  = data.get("payload", {})
    operator = str(data.get("operator", "anonymous"))[:64]
    if not isinstance(payload, dict):
        return jsonify({"error": "payload must be a JSON object"}), 400
    _bus.publish(ColabEvent(type=etype, payload=payload, operator=operator))
    return jsonify({"status": "published"})


@collab_bp.route("/lock", methods=["POST"])
def lock():
    data     = request.get_json(force=True, silent=True) or {}
    target   = str(data.get("target", "")).strip()
    operator = str(data.get("operator", "anonymous")).strip()
    ttl      = int(data.get("ttl_secs", 300))
    if not target:
        return jsonify({"error": "target is required"}), 400
    acquired = _locks.acquire(target, operator, ttl_secs=ttl)
    if acquired:
        _bus.publish(ColabEvent(
            type="lock_acquired",
            payload={"target": target, "operator": operator},
            operator=operator,
        ))
    return jsonify({"acquired": acquired, "target": target, "operator": operator})


@collab_bp.route("/unlock", methods=["POST"])
def unlock():
    data     = request.get_json(force=True, silent=True) or {}
    target   = str(data.get("target", "")).strip()
    operator = str(data.get("operator", "anonymous")).strip()
    released = _locks.release(target, operator)
    if released:
        _bus.publish(ColabEvent(
            type="lock_released",
            payload={"target": target, "operator": operator},
            operator=operator,
        ))
    return jsonify({"released": released, "target": target})


@collab_bp.route("/locks")
def locks():
    all_locks = _locks.all_locks()
    return jsonify({
        "count": len(all_locks),
        "locks": [{"target": l.target, "operator": l.operator,
                   "acquired": l.acquired, "ttl_secs": l.ttl_secs}
                  for l in all_locks],
    })


@collab_bp.route("/history")
def history():
    n      = min(int(request.args.get("n", 100)), 500)
    events = _bus.recent(n)
    return jsonify({
        "count":  len(events),
        "events": [asdict(e) for e in events],
    })


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(collab_bp, url_prefix="/collab")

    print("collab_bp routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule}")

    bus = get_event_bus()
    bus.publish(ColabEvent(type="test", payload={"msg": "hello"}, operator="cli"))
    print(f"history: {[e.type for e in bus.recent(10)]}")
    print("collab_bp OK")
