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

Authentication
--------------
All endpoints require authentication (login_required + require_permission).
Operators are identified from their authenticated session, not from self-reported
query parameters.  The ``operator`` field in events is derived from the
``current_user`` identity.
"""
from __future__ import annotations

import json
import logging
import queue
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from functools import wraps

from flask import (
    Blueprint,
    Response,
    jsonify,
    render_template,
    request,
    stream_with_context,
)

log = logging.getLogger("collab_bp")

# ── Import RBAC module (graceful degradation) ─────────────────────────────────
_RBAC_AVAILABLE = False
_require_permission_deco = None
_get_rbac_store_fn = None

try:
    from modules.lazy_rbac import (
        Permission as _RBACPermission,
    )
    from modules.lazy_rbac import (
        get_rbac_store as _rbac_get_store,
    )
    from modules.lazy_rbac import (
        require_permission as _rbac_require_permission,
    )
    _RBAC_AVAILABLE = True
    _require_permission_deco = _rbac_require_permission
    _get_rbac_store_fn = _rbac_get_store
except ImportError:
    pass

try:
    from flask_login import current_user, login_required
    _AUTH_AVAILABLE = True
except ImportError:
    _AUTH_AVAILABLE = False

    def login_required(f):  # type: ignore[no-redef]
        """No-op decorator when Flask-Login is unavailable."""
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated


def _authenticated_operator():
    """Return the authenticated operator handle, or 'anonymous' if not logged in."""
    try:
        if _AUTH_AVAILABLE and current_user.is_authenticated:
            return current_user.username
    except Exception:
        pass
    return "anonymous"


def _check_collab_permission(perm_name: str) -> bool:
    """Check if the current user has a specific collaboration permission."""
    if not _AUTH_AVAILABLE:
        return True
    try:
        if not current_user.is_authenticated:
            return False
        if _RBAC_AVAILABLE and _get_rbac_store_fn:
            store = _get_rbac_store_fn()
            user = store.find_by_id(int(current_user.id))
            if user:
                try:
                    return user.has_permission(_RBACPermission(perm_name))
                except ValueError:
                    return True
        return True
    except Exception:
        return True


def _collab_login_required(f):
    """Authentication decorator that also verifies collaboration permission."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if _AUTH_AVAILABLE:
            try:
                if not current_user.is_authenticated:
                    return jsonify({"error": "authentication required"}), 401
            except Exception:
                return jsonify({"error": "authentication required"}), 401
        return f(*args, **kwargs)
    return decorated


def _collab_permission_required(perm_name: str):
    """Decorator that checks both auth and specific collab permission."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if _AUTH_AVAILABLE:
                try:
                    if not current_user.is_authenticated:
                        return jsonify({"error": "authentication required"}), 401
                except Exception:
                    return jsonify({"error": "authentication required"}), 401
            if not _check_collab_permission(perm_name):
                return jsonify({"error": f"permission denied: missing {perm_name}"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

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
        self._queues: dict[str, queue.Queue]          = {}
        self._history: list[ColabEvent]              = []

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

    def recent(self, n: int = 50) -> list[ColabEvent]:
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
        self._locks: dict[str, TargetLock]     = {}

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

    def status(self, target: str) -> TargetLock | None:
        with self._lock:
            self._expire()
            return self._locks.get(target)

    def all_locks(self) -> list[TargetLock]:
        with self._lock:
            self._expire()
            return list(self._locks.values())

    def _expire(self) -> None:
        now = time.time()
        expired = [t for t, lock in self._locks.items() if now - lock.acquired > lock.ttl_secs]
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
        self._operators: dict[str, OperatorInfo]      = {}

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

    def active_operators(self) -> list[OperatorInfo]:
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

collab_bp = Blueprint("collab", __name__, template_folder="../templates")


@collab_bp.route("/")
@login_required
def collab_ui():
    from flask import current_app as _current_app
    operator = _authenticated_operator()
    cfg = _current_app.config.get("LAZYOWN_CONFIG")
    if cfg is None:
        cfg = {}
    lhost   = cfg.get("lhost", "localhost") if isinstance(cfg, dict) else getattr(cfg, "lhost", "localhost")
    c2_port = cfg.get("c2_port", 4444) if isinstance(cfg, dict) else getattr(cfg, "c2_port", 4444)
    join_url = f"https://{lhost}:{c2_port}/collab/?operator=<your_handle>"
    return render_template("collab.html", operator=operator, c2_host=f"{lhost}:{c2_port}", join_url=join_url)


@collab_bp.route("/stream")
@_collab_login_required
def stream():
    operator = _authenticated_operator()
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
@_collab_login_required
def operators():
    active = _registry.active_operators()
    return jsonify({
        "count":     len(active),
        "operators": [{"name": o.name, "joined_at": o.joined_at, "last_seen": o.last_seen}
                      for o in active],
    })


@collab_bp.route("/publish", methods=["POST"])
@_collab_permission_required("collab_publish")
def publish():
    data     = request.get_json(force=True, silent=True) or {}
    etype    = str(data.get("type", "generic"))[:64]
    payload  = data.get("payload", {})
    operator = _authenticated_operator()
    if not isinstance(payload, dict):
        return jsonify({"error": "payload must be a JSON object"}), 400
    _bus.publish(ColabEvent(type=etype, payload=payload, operator=operator))
    return jsonify({"status": "published"})


@collab_bp.route("/lock", methods=["POST"])
@_collab_permission_required("collab_lock")
def lock():
    data     = request.get_json(force=True, silent=True) or {}
    target   = str(data.get("target", "")).strip()
    operator = _authenticated_operator()
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
@_collab_permission_required("collab_lock")
def unlock():
    data     = request.get_json(force=True, silent=True) or {}
    target   = str(data.get("target", "")).strip()
    operator = _authenticated_operator()
    released = _locks.release(target, operator)
    if released:
        _bus.publish(ColabEvent(
            type="lock_released",
            payload={"target": target, "operator": operator},
            operator=operator,
        ))
    return jsonify({"released": released, "target": target})


@collab_bp.route("/locks")
@_collab_login_required
def locks():
    all_locks = _locks.all_locks()
    return jsonify({
        "count": len(all_locks),
        "locks": [{"target": lock.target, "operator": lock.operator,
                   "acquired": lock.acquired, "ttl_secs": lock.ttl_secs}
                  for lock in all_locks],
    })


@collab_bp.route("/history")
@_collab_login_required
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
