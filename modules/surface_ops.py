"""Pure attack-surface helpers (no cmd2): discovery targets, confirm parsing.

Used by the ``surface`` CommandSet and unit-tested without the shell.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

_IPV4_RE = re.compile(r"^(\d{1,3})(\.\d{1,3}){3}$")


def is_ipv4(value: str) -> bool:
    """Return True for dotted-quad IPv4 literals with 0-255 octets."""
    match = _IPV4_RE.match((value or "").strip())
    if not match:
        return False
    return all(0 <= int(octet) <= 255 for octet in match.group(0).split("."))


def parse_confirm(answer: str) -> bool:
    """Return True for an affirmative scan confirmation answer."""
    return (answer or "").strip().lower() in ("y", "yes")


def discovery_targets(sessions_dir: str | Path = SESSIONS_DIR) -> list[str]:
    """List every discovery IP across the sessions discovery files."""
    root = Path(str(sessions_dir))
    paths = [root / "hostsdiscovery.txt"] + sorted(root.glob("hosts_*_discovery.txt"))
    out: list[str] = []
    for path in paths:
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line in lines:
            ip = line.strip()
            if ip and is_ipv4(ip) and ip not in out:
                out.append(ip)
    return sorted(out)


def write_world_model_hosts(document: dict, sessions: str | Path) -> int:
    """Append unknown estorides host IPs to world_model.json hosts."""
    path = Path(str(sessions)) / "world_model.json"
    try:
        world = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        world = {}
    if not isinstance(world, dict):
        world = {}
    hosts = world.get("hosts", {}) or {}
    as_list = isinstance(hosts, list)
    known: set[str] = set()
    if as_list:
        for entry in hosts:
            if isinstance(entry, dict) and entry.get("ip"):
                known.add(str(entry["ip"]))
    else:
        known = set(map(str, hosts))
    added = 0
    for node in document.get("nodes", []) or []:
        if not isinstance(node, dict) or node.get("kind") != "host":
            continue
        ip = str(node.get("value", ""))
        if not is_ipv4(ip) or ip in known:
            continue
        record = {"ip": ip, "state": "estorides", "os_hint": "",
                  "services": {}, "source": "estorides"}
        if as_list:
            hosts.append(record)
        else:
            hosts[ip] = record
        known.add(ip)
        added += 1
    if added:
        world["hosts"] = hosts
        path.write_text(json.dumps(world, indent=2))
    return added


__all__ = [
    "discovery_targets",
    "is_ipv4",
    "parse_confirm",
    "write_world_model_hosts",
]
