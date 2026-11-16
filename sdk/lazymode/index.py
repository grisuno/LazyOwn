"""Discoverable index of the lazymode SDK surface.

``lazymode_search`` must let the model learn what it can call without
loading every MCP tool schema into context. Instead of a hand-maintained
catalogue, the index is introspected live from :class:`sdk.facade.Lazy`,
so a new namespace or method appears in search the moment it is added.
Each entry carries a dotted call path, its signature and its one-line
summary; search ranks entries by keyword overlap against path and summary.
"""

from __future__ import annotations

import inspect
from typing import Any

from sdk.facade import Lazy

_NAMESPACE_ATTRS = ("config", "sessions", "recon")


def _entry(path: str, member: Any) -> dict[str, str]:
    """Build one index entry for a callable *member* at *path*.

    Args:
        path: Dotted call path, e.g. ``lazy.config.set``.
        member: The bound method or function to describe.

    Returns:
        A mapping of path, signature and one-line summary.
    """
    try:
        signature = str(inspect.signature(member))
    except (TypeError, ValueError):
        signature = "()"
    doc = inspect.getdoc(member) or ""
    summary = doc.splitlines()[0] if doc else ""
    return {"path": path, "signature": signature, "summary": summary}


def build_index() -> list[dict[str, str]]:
    """Introspect the SDK facade into a list of callable entries.

    Returns:
        One entry per public method of the facade and its namespaces,
        ordered by call path.
    """
    facade = Lazy(payload_path="/dev/null", sessions_dir="/dev/null")
    entries: list[dict[str, str]] = []
    for name in dir(facade):
        if name.startswith("_") or name in _NAMESPACE_ATTRS:
            continue
        member = getattr(facade, name)
        if callable(member):
            entries.append(_entry(f"lazy.{name}", member))
    for namespace in _NAMESPACE_ATTRS:
        obj = getattr(facade, namespace)
        for name in dir(obj):
            if name.startswith("_"):
                continue
            member = getattr(obj, name)
            if callable(member):
                entries.append(_entry(f"lazy.{namespace}.{name}", member))
    return sorted(entries, key=lambda item: item["path"])


def search(query: str, limit: int = 10) -> list[dict[str, str]]:
    """Return index entries most relevant to *query*.

    Args:
        query: Free-text keywords describing the wanted capability.
        limit: Maximum number of entries to return.

    Returns:
        Matching entries ranked by keyword overlap; the full index when
        *query* is empty.
    """
    index = build_index()
    terms = [token for token in str(query).lower().split() if token]
    if not terms:
        return index[:limit]

    def score(entry: dict[str, str]) -> int:
        haystack = f"{entry['path']} {entry['summary']}".lower()
        return sum(haystack.count(term) for term in terms)

    ranked = [(score(entry), entry) for entry in index]
    hits = [entry for value, entry in sorted(ranked, key=lambda pair: pair[0], reverse=True) if value > 0]
    return hits[:limit]
