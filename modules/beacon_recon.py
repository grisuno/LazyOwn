"""Beacon recon ingest — post-foothold discovery feeds the world model.

The Go implant reports two recon payloads on every beacon result:

- ``discovered_ips`` — output of the ``discover:`` command (live hosts
  found from the compromised host).
- ``result_portscan`` — output of the ``portscan:`` command. The implant
  sends either the legacy flat string (``"22,80"``) or a JSON map of
  ``{"<ip>": [22, 80]}``.

Both transit through :mod:`lazyc2` ``receive_result``. This module
turns them into world-model hosts/services (feeding the intel and
attack graphs through the outcome bus) instead of leaving them
display-only.
"""

from __future__ import annotations

import ipaddress
import json
import logging
from pathlib import Path
from typing import Any

from modules.outcome_bus import record_event

log = logging.getLogger("beacon_recon")

DISCOVERY_LEDGER = "hostsdiscovery.txt"
DISCOVERY_SINKS = (
    "intel_graph",
    "attack_graph",
    "event_bus",
    "objectives",
    "c2_surfaces",
    "report",
)
_MAX_ITEMS_PER_BEACON = 64
_MAX_PORT = 65535


def _looks_like_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value.strip())
    except ValueError:
        return False
    return True


def parse_discovered_ips(raw: Any) -> list[str]:
    """Extract clean IP strings from a beacon discovery payload.

    Args:
        raw: Beacon ``discovered_ips`` payload. Accepts a flat string
            (``"10.0.0.2 10.0.0.5, subnet"``), a list, or a dict whose
            values may be lists of IPs.

    Returns:
        Deduplicated valid IP addresses in first-seen order, capped at
        ``_MAX_ITEMS_PER_BEACON`` entries per beacon.
    """
    parts: list[str]
    if isinstance(raw, dict):
        parts = []
        for key, value in raw.items():
            parts.append(str(key))
            if isinstance(value, (list, tuple)):
                parts.extend(str(item) for item in value)
            elif isinstance(value, dict):
                parts.extend(str(item) for item in value.keys())
            elif isinstance(value, str):
                parts.extend(value.replace(",", " ").replace(";", " ").split())
    else:
        text = raw if isinstance(raw, str) else json.dumps(raw, default=str)
        parts = str(text).replace(",", " ").replace(";", " ").split()

    seen: list[str] = []
    skipped = 0
    for candidate in parts:
        candidate = candidate.strip()
        if not candidate or candidate in seen:
            continue
        if len(candidate) > 64 or not _looks_like_ip(candidate):
            skipped += 1
            continue
        seen.append(candidate)
        if len(seen) >= _MAX_ITEMS_PER_BEACON:
            break
    if skipped:
        log.debug("beacon_recon: skipped %d non-IP discovery tokens", skipped)
    return seen


def parse_beacon_portscan(raw: Any, default_host: str = "") -> list[tuple[str, int]]:
    """Normalise any known port-scan payload into ``(host, port)`` pairs.

    Args:
        raw: The beacon ``result_portscan`` value. Supported shapes: the
            Go implant JSON map string (``'{"10.0.0.2":[22,80]}'``), a
            dict of ``{ip: [ports]}``, a flat string (``"22,80"``), and
            a ``host:port``-ish string list.
        default_host: Host credited for entries carrying no IP (e.g. the
            ``"22,80"`` flat string) — usually the beacon primary IP.

    Returns:
        Deduplicated ``(host, port)`` tuples in first-seen order, capped
        at ``_MAX_ITEMS_PER_BEACON`` entries per beacon.
    """
    port_map: dict[str, list[int]] = {}

    def _ports_from(value: Any) -> list[int]:
        if isinstance(value, bool):
            return []
        if isinstance(value, int):
            return [value] if 0 < value <= _MAX_PORT else []
        if isinstance(value, (list, tuple)):
            return [port for item in value for port in _ports_from(item)]
        if isinstance(value, str):
            return [
                int(token)
                for token in str(value).replace(",", " ").replace(";", " ").split()
                if token.isdigit() and 0 < int(token) <= _MAX_PORT
            ]
        return []

    if isinstance(raw, dict):
        for key, value in raw.items():
            port_map[str(key)] = _ports_from(value)
    else:
        text = raw if isinstance(raw, str) else json.dumps(raw, default=str)
        text = str(text).strip()
        if text.startswith("{"):
            try:
                decoded = json.loads(text)
                if isinstance(decoded, dict):
                    for key, value in decoded.items():
                        port_map[str(key)] = _ports_from(value)
            except json.JSONDecodeError:
                pass
        if not port_map:
            host = default_host
            tokens = [token for token in text.replace(",", " ").split() if token]
            if tokens and ":" in tokens[0]:
                head, _, rest = tokens[0].partition(":")
                if _looks_like_ip(head):
                    host, tokens = head, rest.split(",") + tokens[1:]
            if host and not port_map:
                port_map[host] = _ports_from(" ".join(tokens))

    pairs: list[tuple[str, int]] = []
    seen: set[tuple[str, int]] = set()
    for host, ports in port_map.items():
        credited_host = host if _looks_like_ip(host) else default_host
        if not credited_host:
            continue
        for port in ports:
            if not isinstance(port, int) or port <= 0 or port > _MAX_PORT:
                continue
            marker = (credited_host, port)
            if marker in seen:
                continue
            seen.add(marker)
            pairs.append(marker)
            if len(pairs) >= _MAX_ITEMS_PER_BEACON:
                return pairs
    return pairs


def ingest_beacon_recon(
    primary_ip: str,
    discovered_ips: Any = None,
    portscan: Any = None,
    hostname: str = "",
    user: str = "",
    client_id: str = "",
    sessions_dir: Path | None = None,
) -> dict[str, int]:
    """Fold beacon discovery and port-scan payloads into the state layer.

    Adds discovered hosts and scanned services to the world model, appends
    the beacon-reported live hosts to ``sessions/hostsdiscovery.txt`` (the
    existing discovery consumer), and publishes one ``discovery`` outcome
    so intel/attack graph summaries refresh automatically.

    Args:
        primary_ip: IP of the beacon (foothold) that produced the data.
        discovered_ips: Payload from the ``discover:`` command.
        portscan: Payload from the ``portscan:`` command.
        hostname: Beacon hostname label.
        user: Beacon user label.
        client_id: Sanitised beacon identifier.
        sessions_dir: Sessions directory override (tests).

    Returns:
        ``{"hosts": <new hosts added>, "services": <new service pairs>,
        "outcomes": <1 when the discovery outcome published>}``.
    """
    primary_ip = str(primary_ip or "").strip()
    if not primary_ip:
        return {"hosts": 0, "services": 0, "outcomes": 0}

    from modules.world_model import get_world_model

    discovered = [ip for ip in parse_discovered_ips(discovered_ips) if ip != primary_ip]
    scan_pairs = parse_beacon_portscan(portscan, default_host=primary_ip)

    wm = get_world_model()
    known_hosts = set(wm.get_hosts_summary())
    new_hosts = 0
    for ip in discovered:
        if ip not in known_hosts:
            new_hosts += 1
        wm.add_host(ip)
        wm.add_note(ip, f"Discovered from beacon {primary_ip}: {hostname or client_id or user}")
        wm.add_relation(
            primary_ip,
            ip,
            "discovered_by",
            attributes={"source": "beacon", "hostname": hostname, "user": user},
        )
    if new_hosts:
        log.info("beacon_recon: %d new host(s) from beacon %s", new_hosts, primary_ip)

    _append_discovery_ledger(primary_ip, discovered, sessions_dir)

    scanned: dict[str, list[int]] = {}
    for host, port in scan_pairs:
        wm.add_service(host, port)
        scanned.setdefault(host, []).append(port)

    published = 0
    if discovered or scan_pairs:
        try:
            record_event(
                kind="discovery",
                target=primary_ip,
                host=primary_ip,
                title=f"beacon recon {primary_ip}",
                description=f"{hostname or 'beacon'}: hosts {discovered or 'none'}; ports {scanned or 'none'}",
                severity="info",
                success=True,
                source="c2_beacon",
                sinks=list(DISCOVERY_SINKS),
                metadata={
                    "discovered_ips": discovered,
                    "portscan": scanned,
                    "client_id": client_id,
                    "sessions_dir": str(sessions_dir) if sessions_dir else "",
                },
            )
            published = 1
        except Exception as exc:
            log.warning("beacon_recon outcome publish failed: %s", exc)

    return {
        "hosts": new_hosts,
        "services": len(scan_pairs),
        "outcomes": published,
        "scanned": scanned,
        "discovered": discovered,
    }


def _append_discovery_ledger(
    primary_ip: str,
    discovered: list[str],
    sessions_dir: Path | None,
) -> None:
    base = sessions_dir or (Path(__file__).resolve().parent.parent / "sessions")
    try:
        ledger = Path(base) / DISCOVERY_LEDGER
        existing: set[str] = set()
        if ledger.exists():
            for line in ledger.read_text(errors="replace").splitlines():
                existing.add(line.strip().split(":", 1)[0].strip())
        fresh = [ip for ip in discovered if ip not in existing]
        if not fresh:
            return
        lines = "".join(
            f"{ip}: discovered by beacon {primary_ip}\n" for ip in fresh
        )
        with open(ledger, "a", encoding="utf-8") as handle:
            handle.write(lines)
    except Exception as exc:
        log.debug("beacon_recon ledger append failed: %s", exc)
