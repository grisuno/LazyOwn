"""Operator configuration for the loop core: pipeline stages and auto verbs.

Single source of truth for *what the orchestrator fires* and *which auto
verbs it may propose or execute*. Defaults live here; operator overrides
persist under ``payload.json`` -> ``orchestrator`` so the TUI, the engine
and the registry always read the same merged view.

Layout of the payload section::

    {
      "orchestrator": {
        "stages": {"compact": {"enabled": false}},
        "auto_verbs": {
          "automsf": {"enabled": false},
          "myscan": {"enabled": true, "keywords": ["myscan"],
                     "needs_target": true, "description": "custom verb"}
        }
      }
    }
"""

from __future__ import annotations

import threading
import time

STAGE_DEFS = (
    ("enrich", "Asset enrichment (DNS/HTTP)", "every round: first 2 untested scoped assets, 300s cooldown per asset"),
    ("scheduler", "TriggerStore / scheduler due()", "every round: interval, service, task_create, timeout events"),
    ("planner", "Planner wake (heuristics + LLM)", "every round unless paused, expired or over budget"),
    ("workers", "Frontier claim + worker execution", "every round while open intents exist (up to --workers)"),
    ("traffic_ingest", "Recorder proxy ingest", "every round while proxy autostart is enabled"),
    ("retest", "Auto retest pending findings", "every round, up to 3 findings per round"),
    ("reporter", "Apply background reporter drafts", "every round when a finished draft is ready"),
    ("compact", "Cold-graph compaction round stamps", "every planner round; triggers by thresholds and cooldown"),
    ("intel_sync", "Fuse into world model / objectives", "throttled 15s per round; forced on terminal status"),
    ("wrapup", "Final planner round + settlement summary", "on exhausted or timeout status"),
    ("archive", "Task and traffic archive snapshot", "on terminal status (done, exhausted, timeout)"),
    ("report", "Findings report export", "on terminal status when findings exist"),
    ("notify", "Channel notifications (finding, task_status)", "on finding creation and terminal status"),
    (
        "ai_bus",
        "Publish loop events to the unified event bus and Hive Mind",
        "every activity line except raw stream kinds (tool/result/llm)",
    ),
    (
        "detection_oracle",
        "Annotate commands with detection probability",
        "before every executed command; writes oracle risk into the traffic log",
    ),
    (
        "rl_feedback",
        "MoE router and RL trainer outcome learning",
        "after each LLM reply, each executed command, and at terminal",
    ),
    (
        "swan_ensemble",
        "SWAN ensemble planning (disabled by default)",
        "planner LLM step when enabled and SWAN experts are available",
    ),
    (
        "llm_stream",
        "Stream model deltas into the activity log",
        "every pool and agent LLM call while the backend supports streaming",
    ),
)

DEFAULT_STAGES: dict[str, bool] = {name: name != "swan_ensemble" for name, _label, _fires in STAGE_DEFS}
_CACHE_LOCK = threading.Lock()
_CACHE: dict = {"at": 0.0, "stages": None, "verbs": None}
CACHE_TTL_SEC = 1.0


def _invalidate() -> None:
    """Drop the merged-view cache after a write."""
    with _CACHE_LOCK:
        _CACHE["stages"] = None
        _CACHE["verbs"] = None
        _CACHE["at"] = 0.0


def _payload() -> dict:
    """Load the live payload mapping (empty on failure)."""
    try:
        from core.config import load_payload

        return dict(load_payload() or {})
    except Exception:
        return {}


def _section(payload: dict | None = None) -> dict:
    """Return the ``orchestrator`` payload section."""
    return dict((payload if payload is not None else _payload()).get("orchestrator") or {})


def _save(payload: dict) -> None:
    """Persist the payload through core.config and refresh the cache."""
    from core.config import save_payload

    save_payload(payload)
    _invalidate()


def stages() -> dict[str, dict]:
    """Merged stage view: enabled flag, label and firing condition."""
    with _CACHE_LOCK:
        cached = _CACHE["stages"]
        fresh = cached is not None and (time.monotonic() - _CACHE["at"]) < CACHE_TTL_SEC
    if fresh:
        return cached
    overrides = dict(_section().get("stages") or {})
    merged: dict[str, dict] = {}
    for name, label, fires in STAGE_DEFS:
        raw = overrides.get(name) or {}
        enabled = raw.get("enabled")
        merged[name] = {
            "name": name,
            "label": label,
            "fires_when": fires,
            "enabled": DEFAULT_STAGES[name] if enabled is None else bool(enabled),
            "default": DEFAULT_STAGES[name],
        }
    with _CACHE_LOCK:
        _CACHE["stages"] = merged
        _CACHE["at"] = time.monotonic()
    return merged


def stage_enabled(name: str) -> bool:
    """Return whether one pipeline stage is enabled (unknown = enabled)."""
    stage = stages().get(str(name))
    return bool(stage["enabled"]) if stage else True


def set_stage(name: str, enabled: bool) -> dict:
    """Persist the enabled flag of one stage.

    Args:
        name: Stage identifier from :data:`STAGE_DEFS`.
        enabled: New flag.

    Returns:
        The updated merged stage view for that stage.

    Raises:
        KeyError: Unknown stage name.
    """
    if name not in DEFAULT_STAGES:
        raise KeyError(f"unknown stage: {name}")
    payload = _payload()
    section = dict(payload.get("orchestrator") or {})
    stage_overrides = dict(section.get("stages") or {})
    stage_overrides[name] = {"enabled": bool(enabled)}
    section["stages"] = stage_overrides
    payload["orchestrator"] = section
    _save(payload)
    return stages()[name]


def effective_verbs() -> list[dict]:
    """Merged auto-verb view: built-ins plus operator overrides and additions.

    Each entry carries ``name``, ``enabled``, ``phases``, ``keywords``,
    ``needs_target``, ``extra_args``, ``description`` and ``source``
    (``builtin`` or ``custom``).
    """
    with _CACHE_LOCK:
        cached = _CACHE["verbs"]
        fresh = cached is not None and (time.monotonic() - _CACHE["at"]) < CACHE_TTL_SEC
    if fresh:
        return [dict(entry) for entry in cached]
    try:
        from modules.auto_registry import AUTO_VERBS
    except Exception:
        AUTO_VERBS = ()
    overrides = dict(_section().get("auto_verbs") or {})
    merged: list[dict] = []
    seen: set[str] = set()
    for spec in AUTO_VERBS:
        raw = dict(overrides.get(spec.verb) or {})
        merged.append(
            {
                "name": spec.verb,
                "enabled": bool(raw.get("enabled", True)),
                "phases": list(raw.get("phases", spec.phases) or []),
                "keywords": list(raw.get("keywords", spec.keywords) or []),
                "needs_target": bool(raw.get("needs_target", spec.needs_target)),
                "extra_args": str(raw.get("extra_args", spec.extra_args) or ""),
                "description": str(raw.get("description", spec.description) or ""),
                "source": "builtin",
            }
        )
        seen.add(spec.verb)
    for verb, raw in overrides.items():
        if verb in seen or not isinstance(raw, dict):
            continue
        if not raw.get("custom"):
            continue
        merged.append(
            {
                "name": verb,
                "enabled": bool(raw.get("enabled", True)),
                "phases": list(raw.get("phases") or []),
                "keywords": list(raw.get("keywords") or []),
                "needs_target": bool(raw.get("needs_target", True)),
                "extra_args": str(raw.get("extra_args") or ""),
                "description": str(raw.get("description") or ""),
                "source": "custom",
            }
        )
    with _CACHE_LOCK:
        _CACHE["verbs"] = merged
        _CACHE["at"] = time.monotonic()
    return [dict(entry) for entry in merged]


def verb_config(name: str) -> dict | None:
    """Return the merged configuration of one auto verb, or None."""
    wanted = str(name or "").strip()
    for entry in effective_verbs():
        if entry["name"] == wanted:
            return entry
    return None


def verb_enabled(name: str) -> bool:
    """Return whether one auto verb may be proposed or executed."""
    entry = verb_config(name)
    return bool(entry and entry["enabled"])


def upsert_verb(
    name: str,
    *,
    enabled: bool | None = None,
    keywords: list[str] | None = None,
    phases: list[str] | None = None,
    needs_target: bool | None = None,
    extra_args: str | None = None,
    description: str | None = None,
    custom: bool = False,
) -> dict:
    """Create or update one auto-verb override in the payload.

    Args:
        name: Verb (must match an existing shell command when custom).
        enabled: New enabled flag.
        keywords: Intent/goal signals selecting the verb.
        phases: Kill-chain phases the verb serves.
        needs_target: Whether the built line carries the loop target.
        extra_args: Fixed tail args appended after the target.
        description: Operator-facing note.
        custom: Mark as a new operator-defined verb.

    Returns:
        The merged entry after persisting.

    Raises:
        ValueError: Empty verb name.
    """
    clean = str(name or "").strip()
    if not clean:
        raise ValueError("verb name is required")
    payload = _payload()
    section = dict(payload.get("orchestrator") or {})
    overrides = dict(section.get("auto_verbs") or {})
    entry = dict(overrides.get(clean) or {})
    if custom:
        entry["custom"] = True
    if enabled is not None:
        entry["enabled"] = bool(enabled)
    if keywords is not None:
        entry["keywords"] = [str(word).strip() for word in keywords if str(word).strip()]
    if phases is not None:
        entry["phases"] = [str(phase).strip() for phase in phases if str(phase).strip()]
    if needs_target is not None:
        entry["needs_target"] = bool(needs_target)
    if extra_args is not None:
        entry["extra_args"] = str(extra_args)
    if description is not None:
        entry["description"] = str(description)
    overrides[clean] = entry
    section["auto_verbs"] = overrides
    payload["orchestrator"] = section
    _save(payload)
    return verb_config(clean) or {"name": clean, "enabled": False, "source": "override"}


def remove_verb(name: str) -> bool:
    """Remove a custom verb, or disable a built-in one.

    Returns:
        True when something changed.
    """
    clean = str(name or "").strip()
    payload = _payload()
    section = dict(payload.get("orchestrator") or {})
    overrides = dict(section.get("auto_verbs") or {})
    raw = overrides.get(clean)
    if raw is None:
        entry = verb_config(clean)
        if entry is None or entry["source"] != "builtin":
            return False
        return upsert_verb(clean, enabled=False)["enabled"] is False
    if raw.get("custom"):
        overrides.pop(clean, None)
        section["auto_verbs"] = overrides
        payload["orchestrator"] = section
        _save(payload)
        return True
    return upsert_verb(clean, enabled=False)["enabled"] is False


def reset() -> None:
    """Drop every orchestrator override (back to defaults)."""
    payload = _payload()
    payload.pop("orchestrator", None)
    _save(payload)


__all__ = [
    "DEFAULT_STAGES",
    "STAGE_DEFS",
    "effective_verbs",
    "remove_verb",
    "reset",
    "set_stage",
    "stage_enabled",
    "stages",
    "upsert_verb",
    "verb_config",
    "verb_enabled",
]
