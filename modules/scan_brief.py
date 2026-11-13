"""Scan brief: sharpen loop probes against services an nmap scan already found.

Every ``lazynmap`` run persists ``sessions/scan_<target>.nmap.xml``; the
brief turns that XML into a small per-target YAML with the discovered
ports, services and versions so the orchestrator TUI, the operator and
the autonomous planner all read the same focused surface instead of
re-deriving it from raw XML. The planner converts each brief service
into a one-shot sharpening intent anchored to the scanned asset, so a
stealth profile can aim existing evidence at the right ports without a
second scan.

The module never raises: unreadable XML, missing dependencies or a bad
brief file all degrade to empty results.
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

from core.hardening import defused_xml_parse

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
BRIEF_VERSION = 1
MAX_BRIEF_SERVICES = 40

_IP_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def safe_target(target: str) -> str:
    """Return the filesystem-safe scan name fragment for a target.

    Args:
        target: Host or IP the scan covered.

    Returns:
        Sanitized fragment safe for glob composition, empty when invalid.
    """
    value = str(target or "").strip()
    if not value or not _IP_RE.match(value) and not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", value):
        return ""
    return value.replace("/", "_")


def freshest_scan_xml(target: str, sessions_dir: Path | None = None) -> Path:
    """Return the newest scan XML for a target, or an empty path.

    Args:
        target: Host the scan covers.
        sessions_dir: Sessions directory override (tests).

    Returns:
        Path of ``scan_<target>*.nmap.xml`` with the newest mtime, or
        an empty ``Path()`` when none exists.
    """
    safe = safe_target(target)
    base = Path(sessions_dir or SESSIONS_DIR)
    if not safe:
        return Path()
    try:
        candidates = sorted(
            base.glob(f"scan_{safe}*.nmap.xml"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return Path()
    return candidates[0] if candidates else Path()


def parse_nmap_services(path: Path | str) -> list[dict[str, Any]]:
    """Extract ``(port, protocol, service, version, product)`` rows from nmap XML.

    Args:
        path: Path of the nmap XML file.

    Returns:
        Up to ``MAX_BRIEF_SERVICES`` service mappings, empty on failure.
    """
    try:
        root = defused_xml_parse(str(path))
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for host in root.iter("host"):
        address = ""
        for addr in host.iter("address"):
            if str(addr.get("addrtype", "")).startswith("ipv") and addr.get("addr"):
                address = str(addr.get("addr"))
                break
        for port in host.iter("port"):
            entry = {
                "host": address,
                "port": int(port.get("portid", 0) or 0),
                "protocol": str(port.get("protocol", "tcp") or "tcp"),
            }
            service = port.find("service")
            if service is not None:
                entry["service"] = str(service.get("name", "") or "")
                entry["product"] = str(service.get("product", "") or "")
                entry["version"] = str(service.get("version", "") or "")
            else:
                entry["service"] = ""
                entry["product"] = ""
                entry["version"] = ""
            if entry["port"]:
                rows.append(entry)
            if len(rows) >= MAX_BRIEF_SERVICES:
                return rows
    return rows


def build_brief(target: str, sessions_dir: Path | None = None) -> dict[str, Any] | None:
    """Build the brief mapping for a target from its freshest scan XML.

    Args:
        target: Host the scan covered.
        sessions_dir: Sessions directory override (tests).

    Returns:
        Brief mapping (version, target, source_scan, services) or None
        when no scan XML exists or it carries no services.
    """
    scan = freshest_scan_xml(target, sessions_dir)
    if not scan:
        return None
    services = parse_nmap_services(scan)
    if not services:
        return None
    host = str(services[0].get("host", "") or "")
    return {
        "version": BRIEF_VERSION,
        "target": str(target or host),
        "source_scan": str(scan),
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "services": services,
    }


def brief_to_yaml(brief: dict[str, Any]) -> str:
    """Render one brief mapping as YAML text.

    Args:
        brief: Mapping from :func:`build_brief`.

    Returns:
        YAML string (empty when PyYAML is unavailable).
    """
    if yaml is None:
        return ""
    try:
        return str(yaml.safe_dump(brief, sort_keys=False, allow_unicode=False))
    except Exception:
        return ""


def write_brief(target: str, sessions_dir: Path | None = None) -> str:
    """Generate and persist ``sessions/loop_brief_<target>.yaml``.

    Args:
        target: Host the scan covered.
        sessions_dir: Sessions directory override (tests).

    Returns:
        Path of the written brief file, empty when there was nothing to
        write (no scan, no services, no PyYAML).
    """
    brief = build_brief(target, sessions_dir)
    if not brief:
        return ""
    base = Path(sessions_dir or SESSIONS_DIR)
    safe = safe_target(target) or "target"
    path = base / f"loop_brief_{safe}.yaml"
    text = brief_to_yaml(brief)
    if not text:
        return ""
    try:
        base.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError:
        return ""
    return str(path)


def load_brief(path: Path | str) -> dict[str, Any] | None:
    """Load one brief YAML from disk.

    Args:
        path: Brief file path.

    Returns:
        The parsed mapping, or None when missing, invalid or not a mapping.
    """
    if yaml is None:
        return None
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return data


def brief_path_for(target: str, sessions_dir: Path | None = None) -> Path:
    """Return the brief file path for a target.

    Args:
        target: Host the brief covers.
        sessions_dir: Sessions directory override (tests).

    Returns:
        Expected brief path (may not exist).
    """
    safe = safe_target(target) or "target"
    return Path(sessions_dir or SESSIONS_DIR) / f"loop_brief_{safe}.yaml"


def focus_summary(brief: dict[str, Any] | None, limit: int = 6) -> str:
    """Return one compact English line describing the focused surface.

    Args:
        brief: Brief mapping or None.
        limit: Maximum services named.

    Returns:
        Like ``"4445/krb524, 5555/agent"``; empty when unusable.
    """
    if not brief:
        return ""
    parts = []
    for row in (brief.get("services") or [])[: max(1, limit)]:
        port = row.get("port")
        service = str(row.get("service", "") or "unknown")
        parts.append(f"{port}/{service}")
    return ", ".join(parts)


def intents_from_brief(brief: dict[str, Any] | None, limit: int = 6) -> list[str]:
    """Return one sharpening intent text per brief service.

    Args:
        brief: Brief mapping or None.
        limit: Maximum intents.

    Returns:
        Intent summaries like ``brief service: http on 10.0.0.5:80 (from scan brief)``
        referencing the target, anchored intent text the planner can route.
    """
    if not brief:
        return []
    target = str(brief.get("target", "") or "")
    out: list[str] = []
    for row in (brief.get("services") or [])[: max(1, limit)]:
        port = int(row.get("port", 0) or 0)
        service = str(row.get("service", "") or "").strip() or "unknown"
        product = str(row.get("product", "") or "").strip()
        detail = f" {product}" if product else ""
        text = f"brief service: {service}{detail} on {target}:{port} (from scan brief)"
        if text not in out:
            out.append(text)
    return out


__all__ = [
    "BRIEF_VERSION",
    "brief_path_for",
    "brief_to_yaml",
    "build_brief",
    "focus_summary",
    "freshest_scan_xml",
    "intents_from_brief",
    "load_brief",
    "parse_nmap_services",
    "safe_target",
    "write_brief",
]
