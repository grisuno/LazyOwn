"""
modules/engagement_hooks.py — Engagement narration and notification fabric
==========================================================================

Single bridge layer shared by skills/autonomous_daemon.py (EngageOrchestrator)
and lazyc2.py (beacon registration). Provides:

  - EngagementNarrator   : human-readable journal at sessions/engagement.log
  - INotificationSink    : abstract sink contract (SRP/ISP)
  - CollabNotificationSink     : bridges to modules.collab_bp.publish_event
  - TelegramNotificationSink   : optional, gated by payload.enable_telegram_c2
  - DiscordNotificationSink    : optional, gated by payload.enable_discord_c2
  - StreamEventSink            : appends to sessions/autonomous_events.jsonl
  - NotificationBroadcaster    : fan-out to every registered sink
  - publish_shell_obtained(...): single entry point for lazyc2.py beacon code

SOLID:
  S — every class owns one concern.
  O — new sinks (Slack, syslog, SIEM) plug in via INotificationSink without
      touching the broadcaster or the narrator.
  L — every sink honours the INotificationSink contract; broadcaster never
      type-checks.
  I — small role-specific interfaces; the narrator does not depend on sink
      delivery details.
  D — the broadcaster depends on INotificationSink, not on concrete classes;
      callers inject sinks at construction time.

Security:
  - No dynamic imports of arbitrary modules. No eval/exec.
  - Outbound HTTP uses urllib with explicit URLs from payload.json keys only.
  - Every sink wraps its delivery in try/except; a failing sink never blocks
    the engagement loop or the beacon response path.
  - File writes go through pathlib with explicit parents=True so the daemon
    creates sessions/ on first use without escalating into other directories.
  - All payload keys read with .get() to default safely when payload.json is
    incomplete; missing credentials simply disable the corresponding sink.
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import re
import threading
import urllib.error
import urllib.request
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


_LAZYOWN_DIR = Path(os.environ.get(
    "LAZYOWN_DIR",
    str(Path(__file__).resolve().parent.parent),
))
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
_PAYLOAD_FILE = _LAZYOWN_DIR / "payload.json"

ENGAGEMENT_LOG = _SESSIONS_DIR / "engagement.log"
ENGAGEMENT_AUDIT = _SESSIONS_DIR / "engagement_audit.jsonl"
APPROVALS_FILE = _SESSIONS_DIR / "engagement_approvals.jsonl"
SHELL_SEEN_FILE = _SESSIONS_DIR / "engagement_seen_beacons.json"

_log = logging.getLogger("engagement_hooks")

_IO_LOCK = threading.Lock()


_VALID_IP_RE = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
_VALID_HOSTNAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,253}$")


def _safe_str(value: Any, maxlen: int = 200) -> str:
    """Coerce any value to a length-bounded printable string."""
    if value is None:
        return ""
    text = str(value)
    if len(text) > maxlen:
        return text[:maxlen]
    return "".join(ch for ch in text if ch.isprintable() or ch in "\t\n")


def _load_payload() -> Dict[str, Any]:
    """Return payload.json as a dict, empty on any error.

    The engagement layer never raises on payload errors — it simply falls
    back to no-op behaviour for the sinks that depend on the missing key.
    """
    try:
        return json.loads(_PAYLOAD_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


@dataclass(frozen=True)
class EngagementEvent:
    """Value object describing a single engagement-narrator event.

    Attributes:
        event_id: Short hex identifier unique within a daemon run.
        ts: ISO-8601 UTC timestamp.
        kind: Semantic event type (PHASE, STEP, FINDING, SHELL, APPROVAL,
              SWITCH_TOOL, ERROR, INFO).
        target: Primary target IP or hostname for the event.
        message: Human-readable narrative line for engagement.log.
        payload: Structured machine-readable payload for the audit JSONL.
        severity: One of info, warning, critical.
    """

    event_id: str
    ts: str
    kind: str
    target: str
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)
    severity: str = "info"

    @classmethod
    def now(
        cls,
        kind: str,
        target: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ) -> "EngagementEvent":
        """Construct an event with a fresh id and current UTC timestamp."""
        return cls(
            event_id=uuid.uuid4().hex[:8],
            ts=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            kind=_safe_str(kind, 40) or "INFO",
            target=_safe_str(target, 64),
            message=_safe_str(message, 500),
            payload=payload or {},
            severity=severity if severity in ("info", "warning", "critical") else "info",
        )

    def render_line(self) -> str:
        """Return a single-line operator-facing log entry."""
        sev = self.severity.upper()
        tgt = self.target or "-"
        return f"[{self.ts[:19]}Z] [{sev:<8}] [{self.kind:<14}] {tgt:<16} {self.message}"


class INotificationSink(ABC):
    """Contract for downstream delivery channels (collab, telegram, etc.)."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable channel identifier used for diagnostic logging."""

    @abstractmethod
    def deliver(self, event: EngagementEvent) -> bool:
        """Deliver one event. Return True when accepted.

        Implementations must never raise. A delivery failure is reported by
        returning False and logging the cause at debug level.
        """


class StreamEventSink(INotificationSink):
    """Append every event to sessions/autonomous_events.jsonl for the daemon stream.

    This sink is the canonical record consumed by lazyown_autonomous_events
    so engage events join the existing autonomous stream rather than living
    in a parallel file.
    """

    EVENTS_FILE: Path = _SESSIONS_DIR / "autonomous_events.jsonl"

    @property
    def name(self) -> str:
        return "stream"

    def deliver(self, event: EngagementEvent) -> bool:
        record = {
            "id":       event.event_id,
            "ts":       event.ts,
            "type":     event.kind,
            "severity": event.severity,
            "payload": {
                "target":  event.target,
                "message": event.message,
                **event.payload,
            },
        }
        try:
            with _IO_LOCK:
                self.EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
                with self.EVENTS_FILE.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
            return True
        except Exception as exc:
            _log.debug("StreamEventSink delivery failed: %s", exc)
            return False


class CollabNotificationSink(INotificationSink):
    """Bridges engagement events to modules.collab_bp.publish_event.

    Teammates connected to the C2 dashboard see every narrated event in
    real time without any extra wiring. The import is lazy so unit tests
    that do not bring up Flask still pass.
    """

    @property
    def name(self) -> str:
        return "collab"

    def deliver(self, event: EngagementEvent) -> bool:
        try:
            from collab_bp import publish_event as _publish
        except Exception as exc:
            _log.debug("CollabNotificationSink unavailable: %s", exc)
            return False
        try:
            _publish(
                type="engagement",
                payload={
                    "event_id": event.event_id,
                    "kind":     event.kind,
                    "target":   event.target,
                    "message":  event.message,
                    "severity": event.severity,
                    "data":     event.payload,
                    "ts":       event.ts,
                },
                operator="engage_daemon",
            )
            return True
        except Exception as exc:
            _log.debug("CollabNotificationSink delivery failed: %s", exc)
            return False


class _OutboundHTTPSink(INotificationSink):
    """Base class for HTTPS-based sinks (Telegram/Discord/webhook).

    Subclasses override `_build_request(event)` to return (url, body_bytes,
    headers) or None when delivery should be skipped (missing config).
    """

    HTTP_TIMEOUT_S = 4.0

    @property
    def name(self) -> str:
        raise NotImplementedError

    def _build_request(self, event: EngagementEvent) -> Optional[tuple]:
        raise NotImplementedError

    def deliver(self, event: EngagementEvent) -> bool:
        try:
            built = self._build_request(event)
            if built is None:
                return False
            url, body, headers = built
            if not url.startswith(("http://", "https://")):
                _log.debug("%s: refusing non-http(s) url", self.name)
                return False
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=self.HTTP_TIMEOUT_S) as resp:
                return 200 <= resp.status < 300
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            _log.debug("%s delivery failed: %s", self.name, exc)
            return False
        except Exception as exc:
            _log.debug("%s unexpected delivery error: %s", self.name, exc)
            return False


class TelegramNotificationSink(_OutboundHTTPSink):
    """Send a notification to a Telegram chat via the Bot API.

    Required payload.json keys:
      enable_telegram_c2: truthy flag to enable delivery
      telegram_token   : Bot API token
      telegram_chat_id : numeric chat id (or @channel)
    """

    @property
    def name(self) -> str:
        return "telegram"

    def _build_request(self, event: EngagementEvent) -> Optional[tuple]:
        cfg = _load_payload()
        if not str(cfg.get("enable_telegram_c2", "")).lower() in ("true", "1", "yes"):
            return None
        token = str(cfg.get("telegram_token", "") or "").strip()
        chat_id = str(cfg.get("telegram_chat_id", "") or "").strip()
        if not token or not chat_id:
            return None
        text = f"[{event.kind}] {event.target} — {event.message}"
        body = json.dumps({
            "chat_id": chat_id,
            "text":    text[:3500],
        }).encode("utf-8")
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        headers = {"Content-Type": "application/json"}
        return url, body, headers


class DiscordNotificationSink(_OutboundHTTPSink):
    """Send a notification to a Discord channel via webhook.

    Required payload.json keys:
      enable_discord_c2 : truthy flag to enable delivery
      discord_webhook   : full webhook URL
    """

    @property
    def name(self) -> str:
        return "discord"

    def _build_request(self, event: EngagementEvent) -> Optional[tuple]:
        cfg = _load_payload()
        if not str(cfg.get("enable_discord_c2", "")).lower() in ("true", "1", "yes"):
            return None
        webhook = str(cfg.get("discord_webhook", "") or "").strip()
        if not webhook:
            return None
        text = f"**[{event.kind}]** `{event.target}` {event.message}"
        body = json.dumps({"content": text[:1900]}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        return webhook, body, headers


class NotificationBroadcaster:
    """Fan-out events to every registered sink.

    Construction:
        broadcaster = NotificationBroadcaster.default()

    Custom sinks (or test doubles):
        broadcaster = NotificationBroadcaster([StreamEventSink(), my_sink])

    deliver(event) returns the list of sink names that accepted the event.
    No exception escapes; sink failures are silent at info level.
    """

    def __init__(self, sinks: List[INotificationSink]) -> None:
        self._sinks = list(sinks)
        self._lock = threading.Lock()

    @classmethod
    def default(cls) -> "NotificationBroadcaster":
        """Return a broadcaster with the standard four-sink configuration."""
        return cls([
            StreamEventSink(),
            CollabNotificationSink(),
            TelegramNotificationSink(),
            DiscordNotificationSink(),
        ])

    def add(self, sink: INotificationSink) -> None:
        """Register an additional sink at runtime."""
        with self._lock:
            self._sinks.append(sink)

    def deliver(self, event: EngagementEvent) -> List[str]:
        """Push event to all sinks. Return the names of accepting sinks."""
        accepted: List[str] = []
        for sink in list(self._sinks):
            try:
                if sink.deliver(event):
                    accepted.append(sink.name)
            except Exception as exc:
                _log.debug("sink %s threw (suppressed): %s", sink.name, exc)
        return accepted


class EngagementNarrator:
    """Writes human-readable narration to sessions/engagement.log and an
    audit JSONL trail, then fans the event out through the broadcaster.

    The narrator does not know about delivery details; it owns formatting
    and persistence only.
    """

    LOG_FILE: Path = ENGAGEMENT_LOG
    AUDIT_FILE: Path = ENGAGEMENT_AUDIT

    def __init__(
        self,
        broadcaster: Optional[NotificationBroadcaster] = None,
    ) -> None:
        self._broadcaster = broadcaster or NotificationBroadcaster.default()
        self._lock = threading.Lock()

    def narrate(
        self,
        kind: str,
        target: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ) -> EngagementEvent:
        """Write one line + audit record and dispatch to every sink.

        Returns the constructed EngagementEvent so callers can correlate.
        """
        event = EngagementEvent.now(kind, target, message, payload, severity)
        self._persist(event)
        self._broadcaster.deliver(event)
        return event

    def _persist(self, event: EngagementEvent) -> None:
        line = event.render_line()
        audit = {
            "event_id": event.event_id,
            "ts":       event.ts,
            "kind":     event.kind,
            "target":   event.target,
            "message":  event.message,
            "severity": event.severity,
            "payload":  event.payload,
        }
        try:
            with self._lock:
                self.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
                with self.LOG_FILE.open("a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
                with self.AUDIT_FILE.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(audit, ensure_ascii=False, default=str) + "\n")
        except Exception as exc:
            _log.debug("EngagementNarrator persist failed: %s", exc)


# ─────────────────────────────────────────────────────────────────────────────
# Shell-obtained entry point (called by lazyc2.py beacon registration)
# ─────────────────────────────────────────────────────────────────────────────


def _load_seen_beacons() -> Dict[str, Dict[str, Any]]:
    """Return the persisted set of beacons we have already narrated."""
    if not SHELL_SEEN_FILE.exists():
        return {}
    try:
        data = json.loads(SHELL_SEEN_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_seen_beacons(seen: Dict[str, Dict[str, Any]]) -> None:
    """Persist the seen-beacons map atomically."""
    try:
        SHELL_SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = SHELL_SEEN_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(seen, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, SHELL_SEEN_FILE)
    except Exception as exc:
        _log.debug("seen-beacons persist failed: %s", exc)


def _sanitize_client_id(client_id: str) -> str:
    """Restrict client_id to alphanumerics, dash, underscore (<=64 chars).

    Dots are disallowed so a malicious beacon cannot smuggle `..` into any
    file path derived from the id.
    """
    if not isinstance(client_id, str):
        return ""
    cleaned = "".join(c for c in client_id if c.isalnum() or c in "-_")
    return cleaned[:64]


_default_narrator_singleton: Optional[EngagementNarrator] = None
_default_narrator_lock = threading.Lock()


def get_default_narrator() -> EngagementNarrator:
    """Return the process-wide default narrator (lazy singleton)."""
    global _default_narrator_singleton
    with _default_narrator_lock:
        if _default_narrator_singleton is None:
            _default_narrator_singleton = EngagementNarrator()
        return _default_narrator_singleton


def publish_shell_obtained(
    client_id: str,
    primary_ip: str = "",
    hostname: str = "",
    user: str = "",
    platform: str = "",
    narrator: Optional[EngagementNarrator] = None,
) -> Optional[EngagementEvent]:
    """Single entry point called by lazyc2.py on every beacon check-in.

    Idempotent: only narrates the first time a client_id is seen. Subsequent
    calls for the same beacon return None without emitting any event so the
    operator log stays clean.

    Args:
        client_id: Beacon client identifier from the C2 registration.
        primary_ip: First IP from the beacon's ips field.
        hostname: Hostname reported by the beacon.
        user: Username under which the beacon is running.
        platform: Beacon's reported OS / platform string.
        narrator: Optional injected narrator (for tests).

    Returns:
        EngagementEvent for the first sighting, None for repeats.
    """
    cid = _sanitize_client_id(client_id)
    if not cid:
        return None
    seen = _load_seen_beacons()
    if cid in seen:
        return None

    ip_clean = _safe_str(primary_ip, 45)
    host_clean = _safe_str(hostname, 100)
    user_clean = _safe_str(user, 50)
    plat_clean = _safe_str(platform, 60)

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    seen[cid] = {
        "first_seen": now_iso,
        "ip":         ip_clean,
        "hostname":   host_clean,
        "user":       user_clean,
        "platform":   plat_clean,
    }
    _save_seen_beacons(seen)

    nar = narrator or get_default_narrator()
    target = ip_clean or host_clean or cid
    message = (
        f"shell obtained — client_id={cid} host={host_clean or '?'} "
        f"user={user_clean or '?'} platform={plat_clean or '?'}"
    )
    return nar.narrate(
        kind="SHELL_OBTAINED",
        target=target,
        message=message,
        payload={
            "client_id": cid,
            "ip":        ip_clean,
            "hostname":  host_clean,
            "user":      user_clean,
            "platform":  plat_clean,
        },
        severity="critical",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Approval-pending record helpers (consumed by EngageOrchestrator)
# ─────────────────────────────────────────────────────────────────────────────


def append_approval_record(record: Dict[str, Any]) -> None:
    """Append one approval-pending record to sessions/engagement_approvals.jsonl."""
    try:
        with _IO_LOCK:
            APPROVALS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with APPROVALS_FILE.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except Exception as exc:
        _log.debug("approval append failed: %s", exc)


def list_pending_approvals() -> List[Dict[str, Any]]:
    """Return every approval record whose status is still 'pending'."""
    if not APPROVALS_FILE.exists():
        return []
    pending: List[Dict[str, Any]] = []
    try:
        for line in APPROVALS_FILE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("status") == "pending":
                pending.append(rec)
        # Filter by latest status per approval_id
        latest: Dict[str, Dict[str, Any]] = {}
        for rec in pending:
            aid = rec.get("approval_id", "")
            if aid:
                latest[aid] = rec
        return list(latest.values())
    except Exception:
        return []


def resolve_approval(approval_id: str, decision: str, operator: str = "") -> bool:
    """Append a resolution record for the given approval_id.

    Args:
        approval_id: Identifier returned when the approval was created.
        decision: 'approved' or 'denied'.
        operator: Optional operator handle for audit.

    Returns:
        True when the resolution was persisted; False on malformed input.
    """
    if not isinstance(approval_id, str) or not approval_id:
        return False
    if decision not in ("approved", "denied"):
        return False
    record = {
        "approval_id": _safe_str(approval_id, 64),
        "status":      decision,
        "operator":    _safe_str(operator, 64) or "system",
        "resolved_ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    append_approval_record(record)
    return True


def is_valid_target(value: str) -> bool:
    """Validate that value is a dotted-quad IPv4 or a safe hostname token."""
    if not isinstance(value, str):
        return False
    candidate = value.strip()
    if not candidate or len(candidate) > 253:
        return False
    if _VALID_IP_RE.match(candidate):
        parts = candidate.split(".")
        return all(0 <= int(p) <= 255 for p in parts)
    return bool(_VALID_HOSTNAME_RE.match(candidate))


__all__ = [
    "EngagementEvent",
    "INotificationSink",
    "StreamEventSink",
    "CollabNotificationSink",
    "TelegramNotificationSink",
    "DiscordNotificationSink",
    "NotificationBroadcaster",
    "EngagementNarrator",
    "publish_shell_obtained",
    "get_default_narrator",
    "append_approval_record",
    "list_pending_approvals",
    "resolve_approval",
    "is_valid_target",
    "ENGAGEMENT_LOG",
    "ENGAGEMENT_AUDIT",
    "APPROVALS_FILE",
]
