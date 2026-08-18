"""
UnifiedStateManager — single source of truth for all LazyOwn campaign state.

Replaces the fragmented state systems (LazyOwnDB SQLite, WorldModel JSON,
FactStore JSON, SessionState JSON, ObjectiveStore JSONL) with one API that:
- Uses SQLite (LazyOwnDB) as the persistent backend
- Maintains JSON caches for backward compatibility and fast reads
- Publishes events via UnifiedEventBus on every state mutation
- Syncs WorldModel in-memory graph from DB on demand

Design (SOLID)
--------------
- Single Responsibility : owns all campaign state CRUD as one coherent API.
- Open/Closed           : new entity types added via the same add/get/list pattern.
- Liskov                : all state operations return typed dicts or dataclasses.
- Interface Segregation : each domain (hosts, services, creds, etc.) is a logical
                          group, not a separate interface.
- Dependency Inversion  : consumers depend on StateManager, not on DB or files.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("state_manager")

_LAZYOWN_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"

WORLD_MODEL_FILE = _SESSIONS_DIR / "world_model.json"
FACTS_FILE = _SESSIONS_DIR / "policy_facts.json"
SESSION_STATE_FILE = _SESSIONS_DIR / "session_state.json"
OBJECTIVES_FILE = _SESSIONS_DIR / "objectives.jsonl"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    except OSError:
        log.exception("Failed to write %s", path)


@dataclass
class HostSummary:
    address: str
    hostname: str = ""
    os: str = ""
    state: str = "unknown"
    services_count: int = 0
    creds_count: int = 0
    vulns_count: int = 0


@dataclass
class SessionSnapshot:
    generated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))
    phase: str = "recon"
    active_target: str = ""
    lhost: str = ""
    domain: str = ""
    hosts: list[HostSummary] = field(default_factory=list)
    credentials: list[dict[str, Any]] = field(default_factory=list)
    vulnerabilities: list[dict[str, Any]] = field(default_factory=list)
    pending_objectives: int = 0
    total_hosts: int = 0
    total_services: int = 0
    total_vulns: int = 0
    total_creds: int = 0


class StateManager:
    """Unified campaign state API backed by SQLite with JSON caches.

    Usage::

        sm = StateManager()
        sm.add_host("10.0.0.1", hostname="dc01", os="Windows Server 2019")
        sm.add_service("10.0.0.1", 445, "tcp", "microsoft-ds", "SMB")
        sm.add_credential("10.0.0.1", "admin", "P@ssw0rd", origin="crackmapexec")
        snapshot = sm.session_snapshot()
    """

    _instance: StateManager | None = None
    _instance_lock = threading.Lock()

    def __init__(
        self,
        db_path: Path | None = None,
        sessions_dir: Path | None = None,
        world_model_path: Path | None = None,
        facts_path: Path | None = None,
    ) -> None:
        self._lock = threading.RLock()
        self._sessions_dir = sessions_dir or _SESSIONS_DIR
        self._sessions_dir.mkdir(parents=True, exist_ok=True)

        self._world_model_path = world_model_path or WORLD_MODEL_FILE
        self._facts_path = facts_path or FACTS_FILE
        self._session_state_path = SESSION_STATE_FILE

        self._db: Any = None
        self._db_path = db_path or (self._sessions_dir / "db" / "lazyown.db")

        self._payload: dict[str, Any] = {}
        self._workspace_id: int | None = None

    @classmethod
    def instance(cls) -> StateManager:
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def db(self) -> Any:
        if self._db is None:
            from modules.db import LazyOwnDB
            self._db = LazyOwnDB(str(self._db_path))
            self._ensure_workspace()
        return self._db

    @property
    def workspace_id(self) -> int:
        if self._workspace_id is None:
            self._ensure_workspace()
        return self._workspace_id or 1

    def _ensure_workspace(self) -> None:
        if self._payload:
            name = self._payload.get("rhost", "default")
        else:
            name = "default"
        try:
            ws = self.db.workspace_get(name)
            if not ws:
                self._workspace_id = self.db.workspace_create(name)
            else:
                self._workspace_id = ws["id"]
        except Exception:
            self._workspace_id = 1

    def set_payload(self, payload: dict[str, Any]) -> None:
        self._payload = payload
        self._ensure_workspace()

    def _publish(self, category: str, event_type: str, payload: dict[str, Any]) -> None:
        try:
            from modules.event_bus import EventCategory, LazyEvent, get_event_bus
            get_event_bus().publish(LazyEvent(
                category=EventCategory(category),
                event_type=event_type,
                source="state_manager",
                payload=payload,
            ))
        except Exception:
            pass

    def _find_host(self, address: str) -> dict[str, Any] | None:
        """Find a host by exact address match."""
        results = self.db.host_find(self.workspace_id, address)
        for r in results:
            if r["address"] == address:
                return r
        return None

    def _cred_list_for_host(self, host_id: int) -> list[dict[str, Any]]:
        """Get credentials for a specific host_id."""
        all_creds = self.db.cred_list(self.workspace_id)
        return [c for c in all_creds if c.get("host_id") == host_id]

    def _vuln_list_for_host(self, host_id: int) -> list[dict[str, Any]]:
        """Get vulnerabilities for a specific host_id."""
        all_vulns = self.db.vuln_list(self.workspace_id)
        return [v for v in all_vulns if v.get("host_id") == host_id]

    def close(self) -> None:
        with self._lock:
            if self._db:
                try:
                    self._db.close()
                except Exception:
                    pass
                self._db = None

    # ── Hosts ──────────────────────────────────────────────────────────────────

    def add_host(
        self,
        address: str,
        mac: str = "",
        hostname: str = "",
        os: str = "",
        state: str = "unknown",
    ) -> int:
        with self._lock:
            host_id = self.db.host_add(self.workspace_id, address, mac, hostname, os, state)
            self._publish("discovery", "host_added", {
                "address": address, "hostname": hostname, "os": os, "state": state,
            })
            self._sync_world_model_cache()
            return host_id

    def get_host(self, address: str) -> dict[str, Any] | None:
        with self._lock:
            host = self._find_host(address)
            if host:
                host["services"] = self.db.service_list(host["id"])
                host["creds"] = self._cred_list_for_host(host["id"])
                host["vulns"] = self._vuln_list_for_host(host["id"])
            return host

    def list_hosts(self) -> list[dict[str, Any]]:
        with self._lock:
            return self.db.host_list(self.workspace_id)

    def advance_host(self, address: str, new_state: str) -> bool:
        with self._lock:
            host = self._find_host(address)
            if not host:
                return False
            old_state = host.get("state", "unknown")
            self.db.host_add(
                self.workspace_id, address, host.get("mac", ""),
                host.get("hostname", ""), host.get("os", ""), new_state,
            )
            self._publish("phase", "host_advanced", {
                "address": address, "old_state": old_state, "new_state": new_state,
            })
            self._sync_world_model_cache()
            return True

    def delete_host(self, address: str) -> bool:
        with self._lock:
            host = self._find_host(address)
            if not host:
                return False
            self.db.host_delete(host["id"])
            self._publish("discovery", "host_deleted", {"address": address})
            self._sync_world_model_cache()
            return True

    # ── Services ───────────────────────────────────────────────────────────────

    def add_service(
        self,
        host_address: str,
        port: int,
        protocol: str = "tcp",
        name: str = "",
        product: str = "",
        version: str = "",
        state: str = "open",
    ) -> int | None:
        with self._lock:
            host = self._find_host(host_address)
            if not host:
                host_id = self.db.host_add(self.workspace_id, host_address)
            else:
                host_id = host["id"]
            svc_id = self.db.service_add(host_id, port, protocol, state, name, product, version)
            self._publish("scan", "service_added", {
                "host": host_address, "port": port, "protocol": protocol,
                "name": name, "product": product, "version": version,
            })
            self._sync_world_model_cache()
            return svc_id

    def list_services(self, host_address: str) -> list[dict[str, Any]]:
        with self._lock:
            host = self._find_host(host_address)
            if not host:
                return []
            return self.db.service_list(host["id"])

    # ── Credentials ────────────────────────────────────────────────────────────

    def add_credential(
        self,
        host_address: str,
        username: str,
        password: str = "",
        realm: str = "",
        cred_type: str = "password",
        origin: str = "",
    ) -> int | None:
        with self._lock:
            host = self._find_host(host_address)
            if not host:
                return None
            cred_id = self.db.cred_add(
                host["id"], username, password, realm, cred_type, origin,
            )
            self._publish("credential", "credential_added", {
                "host": host_address, "username": username,
                "type": cred_type, "origin": origin,
            })
            self._sync_world_model_cache()
            return cred_id

    def list_credentials(self, host_address: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            if host_address:
                host = self._find_host(host_address)
                if not host:
                    return []
                return self._cred_list_for_host(host["id"])
            return self.db.cred_list(self.workspace_id)

    # ── Vulnerabilities ────────────────────────────────────────────────────────

    def add_vulnerability(
        self,
        host_address: str,
        name: str,
        severity: str = "unknown",
        description: str = "",
        refs: str = "",
    ) -> int | None:
        with self._lock:
            host = self._find_host(host_address)
            if not host:
                return None
            vuln_id = self.db.vuln_add(host["id"], name, severity, description, refs)
            self._publish("vuln", "vulnerability_added", {
                "host": host_address, "name": name, "severity": severity,
            })
            self._sync_world_model_cache()
            return vuln_id

    def list_vulnerabilities(
        self, host_address: str | None = None, severity: str | None = None,
    ) -> list[dict[str, Any]]:
        with self._lock:
            all_vulns = self.db.vuln_list(self.workspace_id, severity)
            if host_address:
                return [v for v in all_vulns if v.get("address") == host_address]
            return all_vulns

    # ── Loot ───────────────────────────────────────────────────────────────────

    def add_loot(
        self,
        name: str,
        loot_type: str = "file",
        path: str = "",
        notes: str = "",
        host_address: str = "",
    ) -> int | None:
        with self._lock:
            host_id = None
            if host_address:
                host = self._find_host(host_address)
                if host:
                    host_id = host["id"]
            loot_id = self.db.loot_add(
                self.workspace_id, name, loot_type, path, notes, host_id,
            )
            self._publish("loot", "loot_added", {
                "name": name, "type": loot_type, "host": host_address,
            })
            return loot_id

    def list_loot(self) -> list[dict[str, Any]]:
        with self._lock:
            return self.db.loot_list(self.workspace_id)

    # ── Notes ──────────────────────────────────────────────────────────────────

    def add_note(
        self, data: str, note_type: str = "general", host_address: str = "",
    ) -> int | None:
        with self._lock:
            host_id = None
            if host_address:
                host = self._find_host(host_address)
                if host:
                    host_id = host["id"]
            note_id = self.db.note_add(self.workspace_id, data, note_type, host_id)
            self._publish("system", "note_added", {
                "type": note_type, "host": host_address,
            })
            return note_id

    def list_notes(self) -> list[dict[str, Any]]:
        with self._lock:
            return self.db.note_list(self.workspace_id)

    # ── NMAP Import ────────────────────────────────────────────────────────────

    def import_nmap_xml(self, xml_path: str) -> dict[str, int]:
        with self._lock:
            result = self.db.import_nmap_xml(self.workspace_id, xml_path)
            self._publish("scan", "nmap_imported", {
                "xml_path": xml_path,
                "hosts": result.get("hosts", 0),
                "services": result.get("services", 0),
                "os": result.get("os", 0),
            })
            self._sync_world_model_cache()
            return result

    def import_nmap_from_facts(self, facts: dict[str, Any]) -> dict[str, int]:
        """Import hosts and services from a FactStore-style facts dict into DB."""
        host_count = 0
        svc_count = 0
        with self._lock:
            for host_ip, host_facts in facts.items():
                if not isinstance(host_facts, dict):
                    continue
                host = self._find_host(host_ip)
                if not host:
                    host_id = self.db.host_add(self.workspace_id, host_ip)
                    host_count += 1
                else:
                    host_id = host["id"]
                os_hint = host_facts.get("os_hint", "")
                if os_hint:
                    self.db.host_add(
                        self.workspace_id, host_ip, "", "", os_hint,
                        host.get("state", "scanned") if host else "scanned",
                    )
                for svc in host_facts.get("services", []):
                    self.db.service_add(
                        host_id,
                        svc.get("port", 0),
                        svc.get("protocol", "tcp"),
                        svc.get("state", "open"),
                        svc.get("service", svc.get("name", "")),
                        svc.get("product", ""),
                        svc.get("version", ""),
                    )
                    svc_count += 1
                for cred in host_facts.get("credentials", []):
                    self.db.cred_add(
                        host_id,
                        cred.get("username", ""),
                        cred.get("password", ""),
                        "",
                        "password",
                        cred.get("source_file", ""),
                    )
                for vuln in host_facts.get("vulnerabilities", []):
                    self.db.vuln_add(
                        host_id,
                        vuln.get("vuln_id", vuln.get("title", "")),
                        vuln.get("severity", "unknown"),
                        vuln.get("title", ""),
                        vuln.get("url", ""),
                    )
        self._sync_world_model_cache()
        return {"hosts": host_count, "services": svc_count}

    def status(self) -> dict[str, int]:
        with self._lock:
            return self.db.status(self.workspace_id)

    # ── World Model Cache ──────────────────────────────────────────────────────

    def _sync_world_model_cache(self) -> dict[str, Any]:
        with self._lock:
            hosts_data: dict[str, Any] = {}
            db_hosts = self.db.host_list(self.workspace_id)
            for h in db_hosts:
                address = h["address"]
                services = self.db.service_list(h["id"])
                hosts_data[address] = {
                    "ip": address,
                    "hostname": h.get("hostname", ""),
                    "os": h.get("os", ""),
                    "state": h.get("state", "unknown"),
                    "services": {
                        str(s["port"]): {
                            "port": s["port"],
                            "protocol": s.get("protocol", "tcp"),
                            "name": s.get("name", ""),
                            "version": s.get("version", ""),
                            "product": s.get("product", ""),
                            "state": s.get("state", "open"),
                        }
                        for s in services
                    },
                }
            all_creds = self.db.cred_list(self.workspace_id)
            all_vulns = self.db.vuln_list(self.workspace_id)
            cache = {
                "hosts": hosts_data,
                "credentials": [
                    {"value": f"{c.get('username','')}:{c.get('password','')}",
                     "host": c.get("address", ""), "confirmed": bool(c.get("cracked"))}
                    for c in all_creds
                ],
                "vulnerabilities": [
                    {"description": v.get("name", ""), "cve": v.get("refs", ""),
                     "severity": v.get("severity", "unknown"), "host": v.get("address", "")}
                    for v in all_vulns
                ],
                "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            _save_json(self._world_model_path, cache)
            return cache

    def get_world_model_cache(self) -> dict[str, Any]:
        with self._lock:
            if self._world_model_path.exists():
                return _load_json(self._world_model_path)
            return self._sync_world_model_cache()

    def load_world_model(self) -> Any:
        """Return a WorldModel instance populated from DB state."""
        try:
            from world_model import WorldModel
            wm = WorldModel(self._sessions_dir)
            db_hosts = self.db.host_list(self.workspace_id)
            for h in db_hosts:
                wm.add_host(h["address"])
                if h.get("os"):
                    wm.add_note(h["address"], f"OS: {h['os']}")
                services = self.db.service_list(h["id"])
                for s in services:
                    wm.add_service(
                        h["address"], s["port"],
                        s.get("name", ""), s.get("version", ""), s.get("protocol", "tcp"),
                    )
                creds = self._cred_list_for_host(h["id"])
                for c in creds:
                    wm.add_credential(
                        f"{c.get('username','')}:{c.get('password','')}",
                        host=h["address"],
                        service=c.get("realm", ""),
                    )
                vulns = self._vuln_list_for_host(h["id"])
                for v in vulns:
                    wm.add_vulnerability(
                        v.get("name", ""), host=h["address"],
                        cve=v.get("refs", ""), severity=v.get("severity", "unknown"),
                    )
            return wm
        except ImportError:
            return None

    # ── Session Snapshot ───────────────────────────────────────────────────────

    def session_snapshot(self) -> SessionSnapshot:
        with self._lock:
            st = self.status()
            db_hosts = self.db.host_list(self.workspace_id)
            hosts = []
            for h in db_hosts:
                svc_count = len(self.db.service_list(h["id"]))
                cred_count = len(self._cred_list_for_host(h["id"]))
                vuln_count = len(self._vuln_list_for_host(h["id"]))
                hosts.append(HostSummary(
                    address=h["address"],
                    hostname=h.get("hostname", ""),
                    os=h.get("os", ""),
                    state=h.get("state", "unknown"),
                    services_count=svc_count,
                    creds_count=cred_count,
                    vulns_count=vuln_count,
                ))
            phase = "recon"
            if st.get("creds", 0) > 0:
                phase = "post_exploit"
            elif st.get("vulns", 0) > 0:
                phase = "exploit"
            elif st.get("services", 0) > 0:
                phase = "enumeration"
            elif st.get("hosts", 0) > 0:
                phase = "scanning"

            all_creds = self.db.cred_list(self.workspace_id)
            all_vulns = self.db.vuln_list(self.workspace_id)

            pending_obj = 0
            if OBJECTIVES_FILE.exists():
                try:
                    with open(OBJECTIVES_FILE, encoding="utf-8") as fh:
                        for line in fh:
                            obj = json.loads(line)
                            if obj.get("status") == "pending":
                                pending_obj += 1
                except Exception:
                    pass

            snapshot = SessionSnapshot(
                phase=phase,
                active_target=self._payload.get("rhost", ""),
                lhost=self._payload.get("lhost", ""),
                domain=self._payload.get("domain", ""),
                hosts=hosts,
                credentials=[{
                    "host": c.get("address", ""), "username": c.get("username", ""),
                    "type": c.get("cred_type", ""), "origin": c.get("origin", ""),
                } for c in all_creds],
                vulnerabilities=[{
                    "host": v.get("address", ""), "name": v.get("name", ""),
                    "severity": v.get("severity", ""),
                } for v in all_vulns],
                pending_objectives=pending_obj,
                total_hosts=st.get("hosts", 0),
                total_services=st.get("services", 0),
                total_vulns=st.get("vulns", 0),
                total_creds=st.get("creds", 0),
            )
            _save_json(self._session_state_path, {
                "generated_at": snapshot.generated_at,
                "phase": snapshot.phase,
                "active_target": snapshot.active_target,
                "lhost": snapshot.lhost,
                "domain": snapshot.domain,
                "hosts": [{
                    "address": h.address, "hostname": h.hostname, "os": h.os,
                    "state": h.state, "services_count": h.services_count,
                    "creds_count": h.creds_count, "vulns_count": h.vulns_count,
                } for h in hosts],
                "credentials": snapshot.credentials,
                "vulnerabilities": snapshot.vulnerabilities,
                "pending_objectives": snapshot.pending_objectives,
                "total_hosts": snapshot.total_hosts,
                "total_services": snapshot.total_services,
                "total_vulns": snapshot.total_vulns,
                "total_creds": snapshot.total_creds,
            })
            return snapshot

    def export_csv(self, table: str) -> str:
        with self._lock:
            return self.db.export_csv(table, self.workspace_id)

    def export_summary(self) -> dict[str, Any]:
        with self._lock:
            st = self.status()
            wm = self.get_world_model_cache()
            return {
                "status": st,
                "world_model_summary": {
                    "hosts_count": len(wm.get("hosts", {})),
                    "credentials_count": len(wm.get("credentials", [])),
                    "vulnerabilities_count": len(wm.get("vulnerabilities", [])),
                    "saved_at": wm.get("saved_at", ""),
                },
            }


def get_state_manager() -> StateManager:
    return StateManager.instance()
