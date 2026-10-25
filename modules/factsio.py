"""Canonical reader for the FactStore ``policy_facts.json`` document.

The on-disk truth is host-keyed and written by ``skills.lazyown_facts``
``FactStore.save``::

    {
        "<ip>": {
            "services": [{"host": ..., "port": ..., "protocol": ...,
                          "service": ..., "product": ..., "version": ...,
                          "state": ...}],
            "credentials": [{"host": ..., "username": ..., "password": ...,
                             "source_file": ..., "hash_value": ...,
                             "hash_type": ...}],
            "vulnerabilities": [{"host": ..., "vuln_id": ..., "severity": ...,
                                 "title": ..., "url": ...}],
            "shares": [...], "access": [...], "paths": [...],
            "raw_files": [...], "os_hint": "..."
        },
        ...
    }

Historically some consumers assumed a wrapped legacy shape
(``{"hosts": {...}, "credentials": [...]}``). Every reader now goes
through :func:`load_policy_facts` so both shapes resolve to one
host-keyed canonical form; writers remain FactStore only.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

log = logging.getLogger("factsio")


def load_policy_facts(path: str | Path) -> dict[str, dict[str, Any]]:
    """Load ``policy_facts.json`` into canonical host-keyed form.

    Args:
        path: Path to the facts document.

    Returns:
        ``{ip: host_record}`` with only dict-typed records. Legacy
        wrapped documents (``{"hosts": {...}}``) are unwrapped. Returns
        an empty dict for missing, unreadable, or non-object documents.
    """
    facts_file = Path(path)
    if not facts_file.exists():
        return {}
    try:
        data = json.loads(facts_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log.warning("factsio: failed to read %s: %s", facts_file, exc)
        return {}
    return canonical_policy_facts(data)


def canonical_policy_facts(data: Any) -> dict[str, dict[str, Any]]:
    """Project any legacy or canonical facts document to host-keyed form.

    Args:
        data: Raw parsed JSON value.

    Returns:
        Host-keyed mapping containing only dict-valued host records.
        Wrapped documents resolve via their ``hosts`` object first.
    """
    if not isinstance(data, dict):
        return {}
    hosts = data.get("hosts")
    if isinstance(hosts, dict):
        source: dict[str, Any] = hosts
    else:
        source = data
    return {str(key): value for key, value in source.items() if isinstance(value, dict)}


def iter_host_records(host_keyed: dict[str, dict[str, Any]]) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield ``(ip, record)`` pairs from canonical host-keyed facts.

    Args:
        host_keyed: Mapping produced by :func:`load_policy_facts`.

    Yields:
        Tuples of host IP and its record.
    """
    yield from host_keyed.items()


def iter_flat_facts(host_keyed: dict[str, dict[str, Any]]) -> Iterator[dict[str, Any]]:
    """Yield one flat record per fact kind found in the host map.

    Each record carries ``type`` (``service`` | ``credential`` |
    ``vulnerability`` | ``share`` | ``access`` | ``path``) and merges
    the underlying fact fields. ``observable`` is derived per kind:
    service name, ``user:password`` / hash, or ``vuln_id``.

    Args:
        host_keyed: Mapping produced by :func:`load_policy_facts`.

    Yields:
        Flat fact records suitable for finding-style consumers.
    """
    for ip, record in host_keyed.items():
        yield from _iter_kind(record, "services", "service", ip)
        yield from _iter_kind(record, "credentials", "credential", ip)
        yield from _iter_kind(record, "vulnerabilities", "vulnerability", ip)
        yield from _iter_kind(record, "shares", "share", ip)
        yield from _iter_kind(record, "access", "access", ip)
        yield from _iter_kind(record, "paths", "path", ip)


def _iter_kind(
    record: dict[str, Any],
    key: str,
    fact_type: str,
    host: str,
) -> None:
    for value in _as_list(record.get(key)):
        yield_kind = dict(value) if isinstance(value, dict) else {}
        yield_kind.setdefault("type", fact_type)
        yield_kind.setdefault("host", yield_kind.get("host") or host)
        yield_kind.setdefault("observable", _observable(yield_kind, fact_type))
        yield_kind.setdefault("value", yield_kind.get("observable", ""))
        yield yield_kind


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return [v for v in value if isinstance(v, dict)]
    return []


def _observable(record: dict[str, Any], fact_type: str) -> str:
    if fact_type == "credential":
        username = str(record.get("username", "") or "")
        password = str(record.get("password", "") or "")
        hash_value = str(record.get("hash_value", "") or "")
        if password:
            return f"{username}:{password}"
        if hash_value:
            return hash_value
        return username
    if fact_type == "vulnerability":
        return str(record.get("vuln_id", "") or record.get("cve", "") or "")
    if fact_type == "service":
        return str(record.get("service", "") or record.get("name", "") or "")
    if fact_type == "share":
        return str(record.get("share_name", "") or record.get("name", "") or "")
    if fact_type == "path":
        return str(record.get("path", "") or "")
    return str(record.get("level", "") or "")
