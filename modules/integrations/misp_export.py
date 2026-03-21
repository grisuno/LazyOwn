#!/usr/bin/env python3
"""
modules/integrations/misp_export.py
=====================================
Exports LazyOwn session findings as MISP-compatible events (JSON format).

Design (SOLID)
--------------
- Single Responsibility : each FindingMapper handles exactly one FindingType
- Open/Closed           : new types via new FindingMapper subclass, no edits needed
- Liskov                : all mappers honour Optional[MISPAttribute] return contract
- Interface Segregation : consumers see only FindingMapper; exporter is separate
- Dependency Inversion  : MISPExporter depends on FindingMapper abstraction

Usage
-----
    from modules.integrations.misp_export import get_exporter

    exporter = get_exporter()
    event = exporter.export_session("sessions/")
    path  = exporter.save(event, "sessions/misp_event.json")

    # CLI:
    python3 modules/integrations/misp_export.py --output sessions/misp_event.json
    python3 modules/integrations/misp_export.py --output sessions/misp_event.json \\
        --misp-url https://misp.example.com --misp-key <API_KEY>
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

log = logging.getLogger("misp_export")

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

_BASE_DIR = Path(__file__).parent.parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclass
class MISPAttribute:
    """A single MISP attribute inside an event."""
    type: str
    value: str
    category: str = "External analysis"
    to_ids: bool = False
    comment: str = ""


@dataclass
class MISPEvent:
    """A complete MISP event ready for JSON serialisation or API push."""
    info: str
    threat_level_id: int = 2          # 1=High, 2=Medium, 3=Low, 4=Undefined
    analysis: int = 0                  # 0=Initial, 1=Ongoing, 2=Completed
    distribution: int = 0             # 0=Organisation only
    attributes: List[MISPAttribute] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Abstract mapper
# ---------------------------------------------------------------------------

class FindingMapper(ABC):
    """Maps a single Finding to a MISPAttribute (or None when not applicable)."""

    @abstractmethod
    def map(self, finding: Any) -> Optional[MISPAttribute]:
        """
        Convert *finding* to a MISPAttribute.

        Returns None if the finding is not relevant to this mapper.
        """


# ---------------------------------------------------------------------------
# Concrete mappers (one per FindingType, Open/Closed)
# ---------------------------------------------------------------------------

class IPMapper(FindingMapper):
    """Maps IP findings to MISP ip-dst attributes."""

    def map(self, finding: Any) -> Optional[MISPAttribute]:
        if not self._is_ip(finding):
            return None
        return MISPAttribute(
            type="ip-dst",
            value=str(finding.value),
            category="Network activity",
            to_ids=True,
            comment=f"Discovered by LazyOwn on host {getattr(finding, 'host', '')}",
        )

    @staticmethod
    def _is_ip(finding: Any) -> bool:
        ftype = str(getattr(finding, "type", "")).lower()
        return "ip" in ftype


class CredentialMapper(FindingMapper):
    """Maps credential findings to MISP text attributes."""

    def map(self, finding: Any) -> Optional[MISPAttribute]:
        if not self._is_credential(finding):
            return None
        return MISPAttribute(
            type="text",
            value=str(finding.value),
            category="Payload delivery",
            to_ids=False,
            comment="Credential found during engagement",
        )

    @staticmethod
    def _is_credential(finding: Any) -> bool:
        ftype = str(getattr(finding, "type", "")).lower()
        return "credential" in ftype


class CVEMapper(FindingMapper):
    """Maps CVE findings to MISP vulnerability attributes."""

    def map(self, finding: Any) -> Optional[MISPAttribute]:
        if not self._is_cve(finding):
            return None
        return MISPAttribute(
            type="vulnerability",
            value=str(finding.value).upper(),
            category="External analysis",
            to_ids=True,
            comment="CVE identified during LazyOwn scan",
        )

    @staticmethod
    def _is_cve(finding: Any) -> bool:
        ftype = str(getattr(finding, "type", "")).lower()
        return "cve" in ftype


class DomainMapper(FindingMapper):
    """Maps domain findings to MISP domain attributes."""

    def map(self, finding: Any) -> Optional[MISPAttribute]:
        if not self._is_domain(finding):
            return None
        return MISPAttribute(
            type="domain",
            value=str(finding.value),
            category="Network activity",
            to_ids=True,
            comment="Domain discovered during enumeration",
        )

    @staticmethod
    def _is_domain(finding: Any) -> bool:
        ftype = str(getattr(finding, "type", "")).lower()
        return "domain" in ftype


class HashMapper(FindingMapper):
    """
    Maps hash findings to MISP md5 or sha256 attributes.

    Auto-detects hash type by length:
      32 chars -> md5
      64 chars -> sha256
    """

    def map(self, finding: Any) -> Optional[MISPAttribute]:
        if not self._is_hash(finding):
            return None
        value = str(finding.value).strip()
        hash_type = self._detect_type(value)
        return MISPAttribute(
            type=hash_type,
            value=value,
            category="Artifacts dropped",
            to_ids=True,
            comment="Hash extracted by LazyOwn",
        )

    @staticmethod
    def _is_hash(finding: Any) -> bool:
        ftype = str(getattr(finding, "type", "")).lower()
        return "hash" in ftype

    @staticmethod
    def _detect_type(value: str) -> str:
        clean = re.sub(r"[^0-9a-fA-F]", "", value)
        if len(clean) == 64:
            return "sha256"
        return "md5"


class ServiceMapper(FindingMapper):
    """Maps service_version findings to MISP text attributes."""

    def map(self, finding: Any) -> Optional[MISPAttribute]:
        if not self._is_service(finding):
            return None
        return MISPAttribute(
            type="text",
            value=str(finding.value),
            category="Network activity",
            to_ids=False,
            comment=f"Service identified on {getattr(finding, 'host', '')}",
        )

    @staticmethod
    def _is_service(finding: Any) -> bool:
        ftype = str(getattr(finding, "type", "")).lower()
        return "service" in ftype


# Registry of all concrete mappers (order matters: first match wins)
_DEFAULT_MAPPERS: List[FindingMapper] = [
    IPMapper(),
    CredentialMapper(),
    CVEMapper(),
    DomainMapper(),
    HashMapper(),
    ServiceMapper(),
]


# ---------------------------------------------------------------------------
# Exporter
# ---------------------------------------------------------------------------

class MISPExporter:
    """
    Reads LazyOwn session artefacts and produces a MISPEvent.

    Parameters
    ----------
    mappers : list of FindingMapper instances (injected for testability)
    """

    def __init__(self, mappers: Optional[List[FindingMapper]] = None) -> None:
        self._mappers: List[FindingMapper] = mappers if mappers is not None else _DEFAULT_MAPPERS

    # -- Public API ------------------------------------------------------------

    def export_session(
        self,
        sessions_dir: str | Path = _SESSIONS_DIR,
        target: Optional[str] = None,
    ) -> MISPEvent:
        """
        Read policy_facts.json and events.jsonl from *sessions_dir*,
        map all findings, and return a populated MISPEvent.
        """
        sdir = Path(sessions_dir)
        findings = self._load_findings(sdir)

        info = f"LazyOwn engagement"
        if target:
            info += f" — {target}"

        event = MISPEvent(
            info=info,
            threat_level_id=2,
            analysis=1,
            distribution=0,
            tags=["lazyown", "pentest", "automated"],
        )

        for finding in findings:
            attr = self._map_finding(finding)
            if attr is not None:
                event.attributes.append(attr)

        return event

    def to_json(self, event: MISPEvent) -> str:
        """Serialise *event* to a MISP-compatible JSON string."""
        payload = {
            "Event": {
                "info": event.info,
                "threat_level_id": str(event.threat_level_id),
                "analysis": str(event.analysis),
                "distribution": str(event.distribution),
                "Tag": [{"name": t} for t in event.tags],
                "Attribute": [
                    {
                        "type": a.type,
                        "value": a.value,
                        "category": a.category,
                        "to_ids": a.to_ids,
                        "comment": a.comment,
                    }
                    for a in event.attributes
                ],
            }
        }
        return json.dumps(payload, indent=2)

    def save(self, event: MISPEvent, path: str | Path) -> Path:
        """Write the MISP event JSON to *path* and return the resolved path."""
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_json(event), encoding="utf-8")
        log.info("MISP event saved to %s (%d attributes)", out, len(event.attributes))
        return out

    def push_to_misp(
        self, event: MISPEvent, url: str, api_key: str
    ) -> bool:
        """
        HTTP-push the event to a live MISP instance.

        Returns False gracefully if requests is not available or the push fails.
        """
        if not _REQUESTS_AVAILABLE:
            log.warning("requests not available; cannot push to MISP")
            return False

        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        endpoint = url.rstrip("/") + "/events"
        try:
            resp = _requests.post(
                endpoint,
                data=self.to_json(event),
                headers=headers,
                timeout=30,
                verify=True,
            )
            if resp.status_code in (200, 201):
                log.info("MISP push succeeded: %s", resp.status_code)
                return True
            log.warning("MISP push returned %s: %s", resp.status_code, resp.text[:200])
            return False
        except Exception as exc:
            log.warning("MISP push failed: %s", exc)
            return False

    # -- Internal helpers ------------------------------------------------------

    def _load_findings(self, sdir: Path) -> list:
        """Load findings from policy_facts.json and events.jsonl."""
        findings: list = []
        findings.extend(self._load_policy_facts(sdir))
        findings.extend(self._load_events(sdir))
        return findings

    def _load_policy_facts(self, sdir: Path) -> list:
        path = sdir / "policy_facts.json"
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not read policy_facts.json: %s", exc)
            return []
        return self._dict_to_findings(data)

    def _load_events(self, sdir: Path) -> list:
        path = sdir / "events.jsonl"
        if not path.exists():
            return []
        findings: list = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    findings.extend(self._dict_to_findings(record))
                except json.JSONDecodeError:
                    continue
        except OSError as exc:
            log.warning("Could not read events.jsonl: %s", exc)
        return findings

    @staticmethod
    def _dict_to_findings(data: Any) -> list:
        """Convert raw dict/list data into lightweight finding-like objects."""
        findings: list = []

        if isinstance(data, list):
            for item in data:
                findings.extend(MISPExporter._dict_to_findings(item))
            return findings

        if not isinstance(data, dict):
            return findings

        # If the dict looks like a Finding already, wrap it
        if "type" in data and "value" in data:
            findings.append(_DictFinding(data))
            return findings

        # Direct CVE extraction from vulnerability record: {"id": "CVE-...", "cvss": 9.8}
        if "id" in data and isinstance(data["id"], str) and data["id"].upper().startswith("CVE-"):
            findings.append(_DictFinding({"type": "cve", "value": data["id"], "host": ""}))
            return findings

        # Recurse into well-known structural keys first
        _KNOWN = ("findings", "hosts", "services", "vulns", "vulnerabilities", "credentials")
        matched_any = False
        for key in _KNOWN:
            val = data.get(key)
            if val is not None and isinstance(val, (list, dict)):
                findings.extend(MISPExporter._dict_to_findings(val))
                matched_any = True

        # If no known keys matched, this may be a host-map {"<ip>": {...}} or similar.
        # Recurse into all dict values so we do not silently drop nested records.
        if not matched_any:
            for val in data.values():
                if isinstance(val, (list, dict)):
                    findings.extend(MISPExporter._dict_to_findings(val))

        return findings

    def _map_finding(self, finding: Any) -> Optional[MISPAttribute]:
        for mapper in self._mappers:
            result = mapper.map(finding)
            if result is not None:
                return result
        return None


class _DictFinding:
    """Lightweight wrapper to give dict-based findings the .type / .value interface."""

    def __init__(self, data: dict) -> None:
        self.type = data.get("type", "")
        self.value = data.get("value", "")
        self.host = data.get("host", "")
        self.confidence = data.get("confidence", 1.0)
        self.raw = data.get("raw", "")


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_exporter: Optional[MISPExporter] = None


def get_exporter() -> MISPExporter:
    """Return the module-level MISPExporter singleton."""
    global _exporter
    if _exporter is None:
        _exporter = MISPExporter()
    return _exporter


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(
        description="Export LazyOwn session findings as a MISP event"
    )
    parser.add_argument(
        "--sessions",
        metavar="DIR",
        default=str(_SESSIONS_DIR),
        help="Path to the sessions directory (default: sessions/)",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default=str(_SESSIONS_DIR / "misp_event.json"),
        help="Output JSON file path",
    )
    parser.add_argument("--target", metavar="HOST", help="Target host label for event info")
    parser.add_argument("--misp-url", metavar="URL", help="MISP instance URL for push")
    parser.add_argument("--misp-key", metavar="KEY", help="MISP API key for push")
    args = parser.parse_args()

    exporter = get_exporter()
    event = exporter.export_session(args.sessions, target=args.target)
    out = exporter.save(event, args.output)
    print(f"Saved: {out}  ({len(event.attributes)} attributes)")

    if args.misp_url and args.misp_key:
        ok = exporter.push_to_misp(event, args.misp_url, args.misp_key)
        print("MISP push:", "OK" if ok else "FAILED")


if __name__ == "__main__":
    _main()
