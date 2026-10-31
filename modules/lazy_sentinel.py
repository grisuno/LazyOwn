"""Internal-network sentinel for LazyOwn.

Turns the C2 beacon fleet into scan probes. One self-contained, copy-paste
``sh`` blob does the discovery and version sweep from inside the private
network, spools a grepable nmap artefact plus a done marker, and everything
an operator or a beacon session has to do is paste the one-liner. The
``ingest`` side parses the spool back into :class:`Sighting` rows so the
feed matcher, the exposure report and autofire all see inside-out evidence
without leaving this contract.

Guards: only private, bounded CIDR ranges (no loopback, link-local,
multicast or cloud-metadata addresses, no range wider than
:data:`MAX_RANGE_HOSTS` hosts), and every blob is read-only.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import secrets
import shlex
import time
from pathlib import Path

from modules.lazy_feedmatch import Sighting

BASE_DIR = Path(__file__).resolve().parent.parent
SPOOL_DIR = BASE_DIR / "sessions" / "sentinel"
DONE_MARK = b"SENTINEL_DONE"
MAX_RANGE_HOSTS = 256
MAX_RANGES = 8
_MIN_PORT = 1
_MAX_PORT = 65535

_SWEEP_COMMAND = (
    "nmap -Pn -sV --version-intensity 5 --open -oG {spool} {targets}"
)
_TSVPART = re.compile(
    r"Host:\s*(?P<ip>\S+)\s.*Ports:\s*(?P<ports>.+)$"
)


def ingest_spool(path: str | Path) -> dict:
    """Parse a sentinel spool artefact back into queryable sightings.

    Accepts the nmap grepable format (``-oG``) and a plain
    ``ip<TAB>port<TAB>product<TAB>version`` fallback.

    Args:
        path: Local path of the copied spool artefact.

    Returns:
        ``{"hosts": [{"ip", "services": [{"port", "product", "version"}]}],
        "sightings": [Sighting]}``; errors never raise, a bad file simply
        yields an empty result.
    """
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"hosts": [], "sightings": []}
    hosts: dict[str, dict] = {}
    for line in text.splitlines():
        for service in _parse_line(line):
            entry = hosts.setdefault(service["ip"], {"ip": service["ip"], "services": []})
            if all(svc["port"] != service["service"]["port"] for svc in entry["services"]):
                entry["services"].append(service["service"])
    shaped = list(hosts.values())
    return {"hosts": shaped, "sightings": _sightings(shaped)}


def _parse_line(line: str) -> list[dict]:
    """Parse one spool row into ``[{"ip", "service"}]`` entries."""
    tsv = _parse_tsv(line)
    if tsv:
        return [tsv]
    return _parse_grepable(line)


def _parse_grepable(line: str) -> list[dict]:
    """Project one ``Host: ... Ports: ...`` grepable row onto the service shape.

    nmap packs the product and version into the slot after the service
    name; when only one token is present it names the product.
    """
    match = _TSVPART.search(line)
    if not match:
        return []
    ip = match.group("ip")
    rows: list[dict] = []
    for spec in match.group("ports").split(", "):
        tokens = spec.strip().split("/")
        if len(tokens) < 5:
            continue
        try:
            port = int(tokens[0])
        except ValueError:
            continue
        if not _MIN_PORT <= port <= _MAX_PORT:
            continue
        block = tokens[6] if len(tokens) > 6 and tokens[6].strip() else (tokens[5] if len(tokens) > 5 else "")
        product, version = _split_product_version(block.strip())
        rows.append({"ip": ip, "service": {"port": port, "product": product or tokens[4], "version": version}})
    return rows


def _parse_tsv(line: str) -> dict | None:
    """Parse one ``ip port product version`` tab-separated fallback row."""
    parts = re.split(r"\t", line.strip())
    if len(parts) < 3:
        return None
    ip = parts[0].strip()
    try:
        port = int(parts[1])
    except ValueError:
        return None
    if not _MIN_PORT <= port <= _MAX_PORT:
        return None
    return {"ip": ip, "service": {"port": port, "product": parts[2].strip(), "version": (parts[3].strip() if len(parts) > 3 else "")}}


def validate_ranges(ranges: list[str]) -> list[str]:
    """Reject unbounded or non-private targets for the sentinel blob.

    Args:
        ranges: CIDR strings proposed for an internal sweep.

    Returns:
        One error message per rejected range, empty when all pass.
    """
    errors: list[str] = []
    for cidr in ranges[: MAX_RANGES + 1]:
        try:
            network = ipaddress.ip_network(cidr.strip(), strict=False)
        except ValueError:
            errors.append(f"invalid CIDR: {cidr}")
            continue
        if network.num_addresses > MAX_RANGE_HOSTS:
            errors.append(f"range {cidr} wider than {MAX_RANGE_HOSTS} hosts")
            continue
        if network.is_loopback or network.is_multicast or network.is_reserved or network.is_link_local:
            errors.append(f"range {cidr} is loopback/link-local/multicast/reserved")
            continue
        if not (network.is_private or network.is_loopback):
            errors.append(f"range {cidr} is not a private range")
    if len(ranges) > MAX_RANGES:
        errors.append(f"more than {MAX_RANGES} ranges")
    return errors


def provision_blob(
    ranges: list[str],
    spool_path: str | Path | None = None,
    spool_dir: str | Path | None = None,
) -> dict:
    """Build the copy-paste sentinel sweep blob.

    Args:
        ranges: Private CIDR strings, validated first.
        spool_path: Optional spool file override inside the target.
        spool_dir: Optional local directory override for the id records.

    Returns:
        ``{"id", "ranges", "spool_path", "script", "oneliner", "errors"}``
        where ``errors`` is empty only on success. Never executes anything.
    """
    errors = validate_ranges(ranges)
    if errors:
        return {"id": "", "ranges": [], "spool_path": "", "script": "", "oneliner": "", "errors": errors}
    token = secrets.token_hex(4)
    spool = str(spool_path or f"/tmp/lazy_sentinel_{token}.gmap")
    targets = " ".join(shlex.quote(cidr.strip()) for cidr in ranges)
    sweep = _SWEEP_COMMAND.format(spool=shlex.quote(spool), targets=targets)
    script = (
        "set -u\n"
        f"sweep() {{ {sweep} ; }}\n"
        "if command -v nmap >/dev/null 2>&1; then sweep; else echo 'sentinel: nmap not available' >&2; exit 3; fi\n"
        f"echo {DONE_MARK.decode()} {token}\n"
    )
    oneliner = f"sh -c {shlex.quote(script)}"
    local_dir = Path(spool_dir or SPOOL_DIR)
    try:
        local_dir.mkdir(parents=True, exist_ok=True)
        _atomic_json(local_dir / f"provision_{token}.json", {
            "id": token,
            "ranges": ranges,
            "spool_path": spool,
            "created_at": time.time(),
        })
    except OSError:
        pass
    return {
        "id": token,
        "ranges": ranges,
        "spool_path": spool,
        "script": script,
        "oneliner": oneliner,
        "errors": [],
    }


def dispatch_line(client_id: str, blob: dict) -> str:
    """Render the ``c2_exec`` line that runs the blob through one beacon.

    Args:
        client_id: Validated beacon client identifier.
        blob: Provision result from :func:`provision_blob`.

    Returns:
        A ``c2_exec ... sh -c '<blob>'`` command line.

    Raises:
        ValueError: On an empty client id or a failed blob.
    """
    cid = (client_id or "").strip()
    script = (blob or {}).get("script", "")
    if not cid or not script:
        raise ValueError("dispatch needs a client_id and a provisioned blob")
    return f"c2_exec {cid} sh -c {shlex.quote(script)}"


def _split_product_version(block: str) -> tuple[str, str]:
    """Split ``Product Version`` text with multi-word products allowed.

    nmap packs the block into one slot; the version is the last
    space-separated token when it starts with a digit.
    """
    pieces = [piece for piece in block.split(" ") if piece]
    if not pieces:
        return "", ""
    if len(pieces) > 1 and pieces[-1][:1].isdigit():
        return " ".join(pieces[:-1]), pieces[-1]
    return " ".join(pieces), ""


def _sightings(hosts: list[dict]) -> list[Sighting]:
    """Flatten host/service rows into :class:`Sighting` values."""
    rows: list[Sighting] = []
    for host in hosts:
        for svc in host.get("services", []):
            rows.append(Sighting(
                host=str(host.get("ip", "")),
                port=int(svc.get("port") or 0),
                protocol="tcp",
                product=str(svc.get("product") or "").strip(),
                version=str(svc.get("version") or "").strip(),
            ))
    return rows


def save_sightings(sightings: list[Sighting], path: str | Path | None = None) -> Path | None:
    """Persist parsed sightings for the report/check surfaces.

    Args:
        sightings: Flattened sightings from :func:`ingest_spool`.
        path: Optional output override.

    Returns:
        The written path or None on failure. Never raises.
    """
    out = Path(path) if path else SPOOL_DIR / f"sightings_{int(time.time())}.json"
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        _atomic_json(out, {
            "saved_at": time.time(),
            "sightings": [
                {
                    "ip": item.host,
                    "port": item.port,
                    "product": item.product,
                    "version": item.version,
                }
                for item in sightings
            ],
        })
        return out
    except OSError:
        return None


def load_sightings(path: str | Path) -> list[Sighting]:
    """Reload a previous ``save_sightings`` artefact.

    Args:
        path: Artefact written earlier.

    Returns:
        Sighting rows; empty list on unreadable or malformed input.
    """
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    rows = data.get("sightings") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        return []
    out: list[Sighting] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        out.append(Sighting(
            host=str(row.get("ip") or row.get("host") or ""),
            port=int(row.get("port") or 0),
            product=str(row.get("product") or "").strip(),
            version=str(row.get("version") or "").strip(),
            source=str(row.get("source") or "scanner"),
        ))
    return out


def _atomic_json(path: Path, data: dict) -> None:
    """Write JSON atomically via a tmp file plus ``os.replace``."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    os.replace(tmp, path)


__all__ = [
    "DONE_MARK",
    "MAX_RANGES",
    "MAX_RANGE_HOSTS",
    "SPOOL_DIR",
    "dispatch_line",
    "ingest_spool",
    "load_sightings",
    "provision_blob",
    "save_sightings",
    "validate_ranges",
]
