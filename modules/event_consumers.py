"""
Event Consumers — reactive layer that makes EventBus events drive real actions.

These subscribers turn the EventBus from a passive log into an active nervous
system. Each consumer listens for specific event patterns and triggers
concrete framework actions without any component needing to know about others.

Consumers:
- PhaseTracker      : advances host states, updates world_model.json on scan/enum events
- AutoRecommender   : injects "recommend next" objectives after scans complete
- CredentialReactor : auto-triggers credential spraying when creds are found
- SoulSync          : keeps sessions/soul.md in sync with campaign phase/state
- DashboardPusher   : pushes events to collab_bus SSE + session_state.json

All consumers are self-registering — call ``wire_all_consumers()`` once at boot.
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

log = logging.getLogger("event_consumers")

_LAZYOWN_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
_SOUL_FILE = _SESSIONS_DIR / "soul.md"
_OBJECTIVES_FILE = _SESSIONS_DIR / "objectives.jsonl"
_WORLD_MODEL_FILE = _SESSIONS_DIR / "world_model.json"
_SESSION_STATE_FILE = _SESSIONS_DIR / "session_state.json"

_wired = False
_wire_lock = threading.Lock()


def _load_payload() -> dict[str, Any]:
    payload_path = _LAZYOWN_DIR / "payload.json"
    if payload_path.exists():
        try:
            with open(payload_path, encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _inject_objective(text: str, priority: str = "medium", source: str = "event_consumer") -> None:
    """Append an objective to objectives.jsonl."""
    obj = {
        "id": f"evt_{int(time.time())}",
        "text": text,
        "priority": priority,
        "status": "pending",
        "source": source,
        "context": {},
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "notes": "",
    }
    _OBJECTIVES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_OBJECTIVES_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _update_world_model_host(address: str, state: str, services: list[dict] | None = None) -> None:
    """Update or create a host entry in world_model.json."""
    wm: dict[str, Any] = {}
    if _WORLD_MODEL_FILE.exists():
        try:
            with open(_WORLD_MODEL_FILE, encoding="utf-8") as fh:
                wm = json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass
    if "hosts" not in wm:
        wm["hosts"] = {}
    if address not in wm["hosts"]:
        wm["hosts"][address] = {"ip": address, "hostname": "", "os": "", "state": "unknown", "services": {}}
    host = wm["hosts"][address]
    host["state"] = state
    host["ip"] = address
    if services:
        for svc in services:
            port = str(svc.get("port", ""))
            if port:
                host["services"][port] = {
                    "port": svc.get("port"),
                    "protocol": svc.get("protocol", "tcp"),
                    "name": svc.get("name", svc.get("service", "")),
                    "version": svc.get("version", ""),
                    "product": svc.get("product", ""),
                    "state": svc.get("state", "open"),
                }
    wm["saved_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    tmp = _WORLD_MODEL_FILE.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(wm, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, _WORLD_MODEL_FILE)
    except OSError:
        pass


def _update_soul(phase: str = "", credentials: list[str] | None = None, access: str = "") -> None:
    """Update sections of sessions/soul.md."""
    if not _SOUL_FILE.exists():
        return
    try:
        content = _SOUL_FILE.read_text(encoding="utf-8")
    except OSError:
        return
    if phase:
        content = re.sub(
            r"^(\*\*Phase:\*\*).*$",
            f"**Phase:** {phase}",
            content,
            flags=re.MULTILINE,
        )
    if credentials:
        creds_text = "\n".join(f"- {c}" for c in credentials[-10:])
        content = re.sub(
            r"(## Known Credentials\n).*?(\n##|\Z)",
            rf"\1{creds_text}\n\2",
            content,
            flags=re.DOTALL,
        )
    if access:
        content = re.sub(
            r"(## Achieved Access\n).*?(\n##|\Z)",
            rf"\1- {access}\n\2",
            content,
            flags=re.DOTALL,
        )
    try:
        _SOUL_FILE.write_text(content, encoding="utf-8")
    except OSError:
        pass


class PhaseTracker:
    """Advances host states and updates world_model.json based on scan/enum events.

    State machine:
        command like lazynmap   → host state "scanned"
        service_added            → host state "enumerated" (if services present)
        vulnerability_added      → host state "exploited" (if vulns present)
        credential_added         → host state "owned"
    """

    def __init__(self) -> None:
        self._seen_services: dict[str, list[dict]] = {}

    def __call__(self, event: Any) -> None:
        cat = getattr(event, "category", None)
        etype = getattr(event, "event_type", "")
        payload = getattr(event, "payload", {})
        target = getattr(event, "target", "")

        if not target:
            return

        try:
            cat_val = cat.value if hasattr(cat, "value") else str(cat)
            if cat_val in ("scan", "recon") and etype in ("lazynmap", "nmap", "lazymasscan"):
                _update_world_model_host(target, "scanned")
                log.info("[PhaseTracker] %s → scanned", target)

            elif cat_val == "scan" and etype == "service_added":
                port_info = {
                    "port": payload.get("port"), "protocol": payload.get("protocol", "tcp"),
                    "name": payload.get("name", ""), "version": payload.get("version", ""),
                    "product": payload.get("product", ""), "state": "open",
                }
                if target not in self._seen_services:
                    self._seen_services[target] = []
                self._seen_services[target].append(port_info)
                _update_world_model_host(target, "enumerated", self._seen_services[target])
                log.info("[PhaseTracker] %s → enumerated (%d services)", target, len(self._seen_services[target]))

            elif cat_val == "vuln" and etype == "vulnerability_added":
                _update_world_model_host(target, "exploited")
                log.info("[PhaseTracker] %s → exploited (vuln: %s)", target, payload.get("name", ""))

            elif cat_val == "credential" and etype == "credential_added":
                _update_world_model_host(target, "owned")
                log.info("[PhaseTracker] %s → owned (creds found)", target)

        except Exception:
            log.debug("[PhaseTracker] failed for %s", target, exc_info=True)


class AutoRecommender:
    """Injects objectives when significant events happen (scan done, vuln found, etc.)."""

    def __init__(self) -> None:
        self._recooldown: dict[str, float] = {}

    def __call__(self, event: Any) -> None:
        cat = getattr(event, "category", None)
        etype = getattr(event, "event_type", "")
        payload = getattr(event, "payload", {})
        target = getattr(event, "target", "")

        try:
            cat_val = cat.value if hasattr(cat, "value") else str(cat)
        except Exception:
            return

        now = time.time()

        if cat_val == "scan" and etype == "nmap_imported":
            hosts = payload.get("hosts", 0)
            services = payload.get("services", 0)
            if hosts > 0 and services > 0:
                key = f"nmap:{target}"
                if now - self._recooldown.get(key, 0) > 60:
                    self._recooldown[key] = now
                    _inject_objective(
                        f"Run lazyown_recommend_next for target {target} ({services} services found)",
                        priority="high",
                        source="auto_recommender",
                    )
                    log.info("[AutoRecommender] Injected objective for %s", target)

        elif cat_val == "scan" and etype == "service_added":
            port = payload.get("port")
            name = payload.get("name", "")
            key = f"svc:{target}:{port}"
            if now - self._recooldown.get(key, 0) > 120:
                self._recooldown[key] = now
                _inject_objective(
                    f"Enumerate {name} service on {target}:{port}",
                    priority="high",
                    source="auto_recommender",
                )
                log.info("[AutoRecommender] Injected enum objective for %s:%s", target, port)

        elif cat_val == "credential" and etype == "credential_added":
            username = payload.get("username", "")
            key = f"cred:{target}:{username}"
            if now - self._recooldown.get(key, 0) > 120:
                self._recooldown[key] = now
                _inject_objective(
                    f"Validate and use credentials {username} against {target} (spray, lateral, or privesc)",
                    priority="critical",
                    source="auto_recommender",
                )
                log.info("[AutoRecommender] Injected credential validation for %s@%s", username, target)

        elif cat_val == "vuln" and etype == "vulnerability_added":
            vuln_name = payload.get("name", "")
            key = f"vuln:{target}:{vuln_name}"
            if now - self._recooldown.get(key, 0) > 120:
                self._recooldown[key] = now
                _inject_objective(
                    f"Research and exploit {vuln_name} on {target}",
                    priority="high",
                    source="auto_recommender",
                )
                log.info("[AutoRecommender] Injected exploit objective for %s: %s", target, vuln_name)


class CredentialReactor:
    """Detects credential patterns in command output and auto-captures them."""

    _CRED_PATTERNS = [
        (re.compile(r"([\w.-]+):([^\\s]{3,})", re.I), "user:pass in output"),
        (re.compile(r"([a-fA-F0-9]{32}:[a-fA-F0-9]{32})"), "NTLM hash"),
        (re.compile(r"\\[\\w.-]+\\\\([\\w.-]+):([^\\s]{3,})", re.I), "domain\\user:pass"),
        (re.compile(r"([\\w.-]+):::", re.I), "kerberos ticket"),
    ]

    def __call__(self, event: Any) -> None:
        cat = getattr(event, "category", None)
        etype = getattr(event, "event_type", "")
        payload = getattr(event, "payload", {})
        target = getattr(event, "target", "")

        try:
            cat_val = cat.value if hasattr(cat, "value") else str(cat)
        except Exception:
            return

        if cat_val != "command":
            return

        output = payload.get("output_snippet", "")
        if not output:
            return

        for pattern, desc in self._CRED_PATTERNS:
            matches = pattern.findall(output)
            for match in matches[:3]:
                cred_str = match if isinstance(match, str) else ":".join(m for m in match if m)
                if len(cred_str) < 6:
                    continue
                try:
                    from modules.state_manager import get_state_manager
                    sm = get_state_manager()
                    parts = cred_str.split(":", 1)
                    if len(parts) == 2:
                        host = target or sm._payload.get("rhost", "")
                        if host:
                            sm.add_credential(host, parts[0], parts[1], origin=f"auto_capture:{desc}")
                            log.info("[CredentialReactor] Captured %s from %s output", cred_str[:30], etype)
                except Exception:
                    pass


class SoulSync:
    """Keeps sessions/soul.md in sync with campaign state from events."""

    def __call__(self, event: Any) -> None:
        cat = getattr(event, "category", None)
        etype = getattr(event, "event_type", "")
        payload = getattr(event, "payload", {})

        try:
            cat_val = cat.value if hasattr(cat, "value") else str(cat)
        except Exception:
            return

        if cat_val in ("discovery", "scan") and etype == "host_added":
            _update_soul(phase="scanning")

        elif cat_val == "scan" and etype in ("service_added", "nmap_imported"):
            _update_soul(phase="enumeration")

        elif cat_val == "vuln" and etype == "vulnerability_added":
            _update_soul(phase="exploitation")

        elif cat_val == "credential" and etype == "credential_added":
            username = payload.get("username", "")
            _update_soul(
                phase="post_exploitation",
                credentials=[f"{username}@{payload.get('host','')} ({payload.get('origin','')})"],
            )

        elif cat_val == "beacon" and etype == "beacon_registered":
            user = payload.get("user", "")
            ip = payload.get("ip", "")
            _update_soul(
                phase="post_exploitation",
                access=f"Shell on {ip} as {user}",
            )


class DashboardPusher:
    """Refreshes session_state.json and pushes to collab_bus on every event."""

    def __call__(self, event: Any) -> None:
        try:
            from modules.state_manager import get_state_manager
            sm = get_state_manager()
            sm.session_snapshot()
        except Exception:
            pass


_CONSUMERS: list[Callable] = [
    PhaseTracker(),
    AutoRecommender(),
    CredentialReactor(),
    SoulSync(),
    DashboardPusher(),
]


def wire_all_consumers(bus=None) -> int:
    """Register all event consumers on the UnifiedEventBus.

    Args:
        bus: Optional UnifiedEventBus instance. Uses singleton if None.

    Returns:
        Number of consumers registered.
    """
    global _wired

    with _wire_lock:
        if _wired:
            return len(_CONSUMERS)
        _wired = True

    if bus is None:
        from modules.event_bus import get_event_bus
        bus = get_event_bus()

    for i, consumer in enumerate(_CONSUMERS):
        name = type(consumer).__name__
        bus.subscribe(f"consumer_{name}", consumer)
        log.info("[consumers] Wired %s", name)

    return len(_CONSUMERS)


def unwire_all_consumers(bus=None) -> None:
    """Remove all event consumers from the bus."""
    global _wired

    if bus is None:
        from modules.event_bus import get_event_bus
        bus = get_event_bus()

    for consumer in _CONSUMERS:
        name = type(consumer).__name__
        bus.unsubscribe(f"consumer_{name}")

    _wired = False
    log.info("[consumers] All consumers unwired")
