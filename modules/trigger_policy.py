"""Declarative trigger policy: YAML seeds for the loop TriggerStore.

The scheduler triggers (``TriggerStore``) used to be runtime-only state:
every operator created them by hand after the loop started. This module
makes them configuration: the ``triggers`` section of
``config/orchestrator.yaml`` declares the default trigger set, the loop
seeds it on every round start, and operators add runtime triggers on
top without ever losing the declarative layer.

Ownership split (SOLID):

- ``modules/loop_triggers.TriggerStore`` owns trigger storage and
  firing semantics;
- this module owns parsing, validation and seeding of the declarative
  policy;
- ``modules.orchestrator_config`` owns YAML file resolution and
  validation for the document that carries the section.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from modules.loop_triggers import TRIGGER_KINDS

log = logging.getLogger("trigger_policy")


@dataclass(frozen=True)
class TriggerPolicyConfig:
    """Knobs for declarative trigger seeds and store round-trips."""

    arg_max_chars: int = 300


TRIGGER_POLICY = TriggerPolicyConfig()


def validate_triggers(raw: object) -> list[str]:
    """Validate the raw ``triggers`` section of the orchestrator YAML.

    Args:
        raw: Entry from the YAML document (expected: list of mappings).

    Returns:
        Human-readable errors; an empty list means the section is valid.
    """
    if raw is None:
        return []
    if not isinstance(raw, list):
        return ["triggers must be a list"]
    errors: list[str] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            errors.append(f"trigger #{index} must be a mapping")
            continue
        kind = entry.get("kind")
        if not isinstance(kind, str) or kind not in TRIGGER_KINDS:
            errors.append(f"trigger #{index} has unknown kind {kind!r}")
            continue
        every_sec = entry.get("every_sec", 0.0)
        if isinstance(every_sec, bool) or not isinstance(every_sec, (int, float, str)):
            errors.append(f"trigger #{index} every_sec must be numeric")
        elif isinstance(every_sec, str):
            try:
                float(every_sec)
            except ValueError:
                errors.append(f"trigger #{index} every_sec must be numeric")
        flag = entry.get("enabled", True)
        if not isinstance(flag, bool):
            errors.append(f"trigger #{index} enabled must be a boolean")
        arg = entry.get("arg")
        if arg is not None and not isinstance(arg, str):
            errors.append(f"trigger #{index} arg must be a string")
    return errors


def _coerce_every_sec(value: object) -> float:
    """Return ``every_sec`` coerced to a non-negative float."""
    try:
        return max(0.0, float(value or 0.0))
    except (TypeError, ValueError):
        return 0.0


def seeds(raw: object) -> list[dict]:
    """Coerce validated trigger rows into seed dicts for the store.

    Args:
        raw: The raw ``triggers`` section (list of mappings).

    Returns:
        Normalised seeds ``{kind, arg, every_sec, enabled}``. Unknown or
        invalid kinds are dropped with a warning so one bad row never
        blocks the rest.
    """
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for index, entry in enumerate(raw if isinstance(raw, list) else []):
        if not isinstance(entry, dict):
            continue
        kind = str(entry.get("kind", "")).strip()
        if kind not in TRIGGER_KINDS:
            log.warning("trigger seed #%s dropped: unknown kind %r", index, entry.get("kind"))
            continue
        flag = entry.get("enabled", True)
        out.append(
            {
                "kind": kind,
                "arg": str(entry.get("arg", "") or "")[: TRIGGER_POLICY.arg_max_chars],
                "every_sec": _coerce_every_sec(entry.get("every_sec")),
                "enabled": bool(flag) if isinstance(flag, bool) else True,
            }
        )
    return out


def read_policy(path: str | None = None) -> dict:
    """Read the shipped orchestrator YAML triggers section.

    Args:
        path: Optional explicit YAML path override.

    Returns:
        ``{raw, seeds}`` where ``raw`` is the validated section value;
        empty mappings when the file or section is unavailable.
    """
    try:
        from pathlib import Path as _Path

        from modules.orchestrator_config import _read_yaml

        document = _read_yaml(_Path(path) if path else None)
    except Exception:
        return {}
    raw = document.get("triggers") if isinstance(document, dict) else None
    errors = validate_triggers(raw)
    if errors:
        log.warning("invalid triggers section: %s", "; ".join(errors))
        return {}
    return {"raw": raw or [], "seeds": seeds(raw)}


def seed_store(policy: list[dict] | None = None, store=None, task_id: str = "") -> dict:
    """Merge declarative seeds into a persistent TriggerStore.

    Without ``policy`` the shipped YAML is read; ``store=None`` builds a
    fresh global store for ``task_id`` and seeds it. Runtime triggers
    added later by the operator are never touched.

    Args:
        policy: Seed rows, or ``None`` to read the YAML policy.
        store: Existing TriggerStore to seed, or ``None`` to create one.
        task_id: Task-scoped store name when creating the store.

    Returns:
        ``{added, total}`` statistics for the brief and the API.
    """
    if policy is None:
        policy = (read_policy().get("seeds") or [])
    if store is None:
        from modules.loop_triggers import TriggerStore

        store = TriggerStore(task_id)
    added = store.upsert_defaults(list(policy or []))
    return {"added": len(added), "total": len(store.list())}


def export_store(task_id: str = "") -> list[dict]:
    """Return the current store rows for TUI and API surfaces.

    Args:
        task_id: Task-scoped table, or empty string for the global one.

    Returns:
        The trigger items as stored on disk.
    """
    from modules.loop_triggers import TriggerStore

    return TriggerStore(task_id).list()


def remove_seed(kind: str, arg: str = "", task_id: str = "") -> bool:
    """Drop the first runtime trigger matching a declarative signature.

    Args:
        kind: Trigger kind from ``TRIGGER_KINDS``.
        arg: Matching ``arg`` value (empty for kind-only matches).
        task_id: Task-scoped table, or empty string for the global one.

    Returns:
        ``True`` when a trigger was removed.

    Raises:
        ValueError: Unknown trigger kind.
    """
    if kind not in TRIGGER_KINDS:
        raise ValueError(f"kind must be one of {TRIGGER_KINDS}")
    from modules.loop_triggers import TriggerStore

    store = TriggerStore(task_id)
    for item in store.list():
        if item.get("kind") == kind and str(item.get("arg", "")) == arg:
            return store.remove(int(item.get("id", 0)))
    return False


__all__ = [
    "TRIGGER_KINDS",
    "export_store",
    "read_policy",
    "remove_seed",
    "seed_store",
    "seeds",
    "validate_triggers",
]
