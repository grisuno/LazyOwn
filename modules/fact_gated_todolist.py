"""Fact-gated todolist: dispatch an intent only when its prerequisite facts exist.

ARTEX keeps a persistent todolist whose next item is dispatched only once the
facts it depends on are present, so a campaign walks injection -> creds ->
lateral -> privesc without getting ahead of its own evidence. LazyOwn already
has the dual graph (the global :class:`AssetGraph` and the per-task
exploration graph joined by exploration anchors) and an event bus; the missing
contract is this dependency gate.

This module is the pure contract: given todolist items that each declare the
fact predicates they require and the set of facts already observed, it
partitions them into the items ready to dispatch now and the items still
blocked, naming each blocked item's missing predicates. It has no framework
imports so the planner, the dashboard and tests all share one definition.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def unmet_requirements(requires: Iterable[str], facts: Iterable[str]) -> list[str]:
    """Return the required predicates not satisfied by any known fact.

    A predicate is satisfied when its text appears, case-insensitively, inside
    any observed fact; empty predicates are ignored. Substring matching keeps
    the contract dependency-free while tolerating the free-form fact text the
    exploration graph stores.

    Args:
        requires: Fact predicates the item depends on.
        facts: Fact texts already observed in the engagement.

    Returns:
        The subset of ``requires`` that no fact satisfies, order preserved.
    """
    fact_blob = " \n ".join(str(fact) for fact in facts).lower()
    missing: list[str] = []
    for predicate in requires:
        token = str(predicate or "").strip().lower()
        if token and token not in fact_blob:
            missing.append(str(predicate))
    return missing


def gate(items: Iterable[dict[str, Any]], facts: Iterable[str]) -> dict[str, list]:
    """Partition todolist items into those ready to dispatch and those blocked.

    Args:
        items: Todolist items, each a mapping that may carry a ``requires``
            list of fact predicates. An item with no requirements is always
            ready.
        facts: Fact texts already observed.

    Returns:
        ``{"ready": [item, ...], "blocked": [{"item": item, "missing": [...]}]}``
        where ``ready`` preserves input order and each blocked entry names the
        predicates that are still missing.
    """
    fact_list = list(facts)
    ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    for item in items:
        missing = unmet_requirements(item.get("requires", []) or [], fact_list)
        if missing:
            blocked.append({"item": item, "missing": missing})
        else:
            ready.append(item)
    return {"ready": ready, "blocked": blocked}
