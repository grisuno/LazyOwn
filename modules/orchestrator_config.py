"""Operator configuration for the loop core: profiles, stages and auto verbs.

YAML is the default source of truth. ``config/orchestrator.yaml`` declares
profiles, pipeline stages, numeric limits, budgets, default chain/playbook
and outcome sink toggles. ``payload.json`` keeps runtime overrides under
``orchestrator``; an override always wins over YAML.

The module exposes one merged view so the TUI, the runner and the engine
read the same values. A missing or invalid YAML never stops the loop: the
built-in fallback table keeps it running.
"""

from __future__ import annotations

import copy
import logging
import threading
import time
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

log = logging.getLogger("orchestrator_config")

BASE_DIR = Path(__file__).resolve().parent.parent
ORCHESTRATOR_YAML_PATH = BASE_DIR / "config" / "orchestrator.yaml"
_MAX_YAML_BYTES = 200_000

STAGE_DEFS = (
    ("enrich", "Asset enrichment (DNS/HTTP)", "every round: first untested scoped assets, 300s cooldown per asset"),
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
    ("ai_bus", "Publish loop events to the unified event bus and Hive Mind", "every activity line except raw stream kinds"),
    ("detection_oracle", "Annotate commands with detection probability", "before every executed command"),
    ("defense_validate", "Detection rule replay over attack and control logs", "on terminal status when rule_path and log files are configured"),
    ("closedloop_tune", "Baseline vs candidate detection rule comparison with tuning suggestions", "on terminal status after defense_validate when both rules are configured"),
    ("hunt_verify", "Evidence verdicts per chain stage (observed, inferred, not_observed, insufficient)", "on terminal status when a hunt design and evidence file exist"),
    ("llm_pool", "LLM provider pool with circuit breaker and backoff ladder", "every pool and agent LLM call while providers trip"),
    ("rl_feedback", "MoE router and RL trainer outcome learning", "after each LLM reply, command and at terminal"),
    ("swan_ensemble", "SWAN ensemble planning (disabled by default)", "planner LLM step when enabled"),
    ("llm_stream", "Stream model deltas into the activity log", "every pool and agent LLM call while supported"),
)

FALLBACK_STAGES: dict[str, dict[str, Any]] = {
    name: {
        "enabled": name != "swan_ensemble",
        "label": label,
        "fires_when": fires,
        "params": {},
    }
    for name, label, fires in STAGE_DEFS
}

FALLBACK_LIMITS: dict[str, int | float] = {
    "rounds": 10,
    "workers": 3,
    "worker_parallel_cap": 5,
    "heartbeat_sec": 600,
    "wake_debounce_sec": 0.8,
    "intel_sync_sec": 15,
    "enrich_limit": 2,
    "enrich_cooldown_sec": 300,
    "retest_limit": 3,
    "max_intents_per_round": 4,
    "max_worker_steps": 6,
    "verb_timeout_sec": 300,
    "step_delay_sec": 0.5,
}

FALLBACK_BUDGET: dict[str, int] = {"max_rounds": 10, "max_toolcalls": 200, "max_findings": 50}

FALLBACK_SINKS: dict[str, bool] = {
    "world_model": True,
    "killchain": True,
    "intel_graph": True,
    "attack_graph": True,
    "c2_surfaces": True,
    "campaign_db": True,
    "objectives": True,
    "event_bus": True,
    "report": True,
}

DEFAULT_STAGES: dict[str, bool] = {name: bool(data["enabled"]) for name, data in FALLBACK_STAGES.items()}

_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, Any] = {"at": 0.0, "stages": None, "verbs": None}
CACHE_TTL_SEC = 1.0


def _invalidate() -> None:
    """Drop the merged-view cache after a write."""
    with _CACHE_LOCK:
        _CACHE["stages"] = None
        _CACHE["verbs"] = None
        _CACHE["at"] = 0.0


def reload() -> None:
    """Invalidate every merged view after an external configuration change."""
    _invalidate()


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


def _read_yaml(path: Path | str | None = None) -> dict:
    """Read the orchestration YAML, returning an empty mapping on failure."""
    target = Path(path or ORCHESTRATOR_YAML_PATH)
    if yaml is None:
        log.warning("PyYAML is unavailable; orchestrator YAML disabled")
        return {}
    try:
        if not target.is_file() or target.stat().st_size > _MAX_YAML_BYTES:
            return {}
        with target.open("r", encoding="utf-8", errors="replace") as handle:
            data = yaml.safe_load(handle)
    except Exception as exc:
        log.warning("orchestrator YAML unreadable at %s: %s", target, exc)
        return {}
    if not isinstance(data, dict):
        log.warning("orchestrator YAML at %s is not a mapping", target)
        return {}
    errors = validate_config(data)
    if errors:
        log.warning("orchestrator YAML invalid at %s: %s", target, "; ".join(errors))
        return {}
    return data


def _fallback_profile() -> dict[str, Any]:
    """Return the synthetic profile used when YAML is absent."""
    return {
        "description": "Built-in fallback profile.",
        "extends": "",
        "stages": copy.deepcopy(FALLBACK_STAGES),
        "limits": dict(FALLBACK_LIMITS),
        "budget": dict(FALLBACK_BUDGET),
        "chain": "apt_chain",
        "playbook": "rocke",
        "sinks": dict(FALLBACK_SINKS),
    }


def _merge_stage(base: dict, override: dict) -> dict:
    """Merge one stage override, keeping parent values for absent keys."""
    merged = copy.deepcopy(base)
    for key in ("enabled", "label", "fires_when"):
        if key in override:
            merged[key] = override[key]
    if isinstance(override.get("params"), dict):
        merged.setdefault("params", {})
        merged["params"].update(override["params"])
    merged.setdefault("enabled", True)
    merged.setdefault("label", "")
    merged.setdefault("fires_when", "")
    merged.setdefault("params", {})
    return merged


def _merge_profile(parent: dict, child: dict) -> dict:
    """Merge a child profile over its parent."""
    merged = copy.deepcopy(parent)
    merged["extends"] = str(child.get("extends", "") or "")
    if child.get("description") is not None:
        merged["description"] = str(child.get("description") or "")
    stages = dict(merged.get("stages") or {})
    for name, override in (child.get("stages") or {}).items():
        stages[name] = _merge_stage(stages.get(name, {}), override)
    merged["stages"] = stages
    for key in ("limits", "budget", "sinks"):
        value = dict(merged.get(key) or {})
        value.update(child.get(key) or {})
        merged[key] = value
    for key in ("chain", "playbook"):
        if child.get(key) is not None:
            merged[key] = str(child.get(key) or "")
    if child.get("harness") is not None:
        merged["harness"] = bool(child.get("harness"))
    return merged


def _resolve_profile(name: str, raw_profiles: dict, stack: tuple[str, ...] = ()) -> dict:
    """Resolve one profile, following ``extends`` with cycle protection."""
    if name in stack:
        raise ValueError(f"profile extends cycle: {' -> '.join((*stack, name))}")
    raw = raw_profiles[name]
    parent_name = str(raw.get("extends", "") or "")
    if parent_name:
        if parent_name not in raw_profiles:
            raise ValueError(f"unknown parent profile: {parent_name!r}")
        parent = _resolve_profile(parent_name, raw_profiles, (*stack, name))
    else:
        parent = _fallback_profile()
    return _merge_profile(parent, raw)


def profiles() -> dict[str, dict]:
    """Return every resolved profile, including inherited values."""
    data = _read_yaml()
    raw_profiles = data.get("profiles") or {}
    if not isinstance(raw_profiles, dict) or not raw_profiles:
        return {"default": _fallback_profile()}
    resolved: dict[str, dict] = {}
    for name in raw_profiles:
        try:
            resolved[str(name)] = _resolve_profile(str(name), raw_profiles)
        except ValueError as exc:
            log.warning("Skipping profile %s: %s", name, exc)
    return resolved or {"default": _fallback_profile()}


def _default_profile_name(data: dict | None = None) -> str:
    """Return the configured default profile name."""
    document = data if data is not None else _read_yaml()
    name = str(document.get("default_profile", "") or "")
    available = profiles()
    if name in available:
        return name
    return "default" if "default" in available else next(iter(available))


def active_profile() -> str:
    """Return the profile selected by the payload, falling back safely."""
    available = profiles()
    selected = str(_section().get("profile", "") or "")
    if selected in available:
        return selected
    fallback = _default_profile_name()
    if selected and selected not in available:
        log.warning("Unknown orchestrator profile %r; using %r", selected, fallback)
    return fallback


def profile_config(name: str = "") -> dict:
    """Return one resolved profile by name, or the active profile."""
    available = profiles()
    wanted = str(name or active_profile())
    return copy.deepcopy(available.get(wanted, available[_default_profile_name()]))


def set_profile(name: str) -> dict:
    """Persist the active profile name.

    Args:
        name: Profile declared in the YAML or the fallback table.

    Returns:
        The resolved profile after persisting.

    Raises:
        KeyError: Unknown profile name.
    """
    available = profiles()
    wanted = str(name or "").strip()
    if wanted not in available:
        raise KeyError(f"unknown profile: {wanted}")
    payload = _payload()
    section = dict(payload.get("orchestrator") or {})
    section["profile"] = wanted
    payload["orchestrator"] = section
    _save(payload)
    return profile_config(wanted)


def set_harness(enabled: bool) -> dict:
    """Persist the deterministic-harness toggle in the payload.

    When enabled, the harness profile is also selected so the loop and
    the factory agree on a local-only, deterministic regime.

    Args:
        enabled: True engages the harness; False disables the flag and
            restores the previous profile selection.

    Returns:
        A ``{"harness": bool, "profile": str}`` summary after persisting.
    """
    payload = _payload()
    section = dict(payload.get("orchestrator") or {})
    section["harness"] = bool(enabled)
    if enabled and section.get("profile") != "default":
        section.setdefault("profile", active_profile())
        section["profile"] = "harness"
    payload["orchestrator"] = section
    _save(payload)
    try:
        current = profile_config() if not bool(enabled) else profile_config("harness")
    except Exception:
        current = {}
    return {
        "harness": bool(enabled),
        "profile": str(section.get("profile", "") or ""),
        "chain": str(current.get("chain", "") or ""),
    }


def limits() -> dict:
    """Return resolved numeric limits for the active profile."""
    merged = dict(FALLBACK_LIMITS)
    merged.update(profile_config().get("limits") or {})
    return merged


def budget() -> dict:
    """Return resolved budgets for the active profile."""
    merged = dict(FALLBACK_BUDGET)
    merged.update(profile_config().get("budget") or {})
    return merged


def chain_defaults() -> dict:
    """Return the default chain and playbook for the active profile."""
    profile = profile_config()
    return {
        "chain": str(profile.get("chain", "apt_chain") or "apt_chain"),
        "playbook": str(profile.get("playbook", "rocke") or "rocke"),
    }


def sinks() -> dict:
    """Return outcome sink toggles for the active profile plus payload overrides."""
    merged = dict(FALLBACK_SINKS)
    merged.update({key: bool(value) for key, value in (profile_config().get("sinks") or {}).items()})
    overrides = dict(_section().get("sinks") or {})
    if "attack_graph" not in overrides and "asset_graph" in overrides:
        overrides["attack_graph"] = overrides["asset_graph"]
    merged.update({key: bool(value) for key, value in overrides.items() if key in merged})
    return merged


def stages() -> dict[str, dict]:
    """Merged stage view: enabled flag, label, firing condition and params."""
    with _CACHE_LOCK:
        cached = _CACHE["stages"]
        fresh = cached is not None and (time.monotonic() - float(_CACHE["at"])) < CACHE_TTL_SEC
    if fresh:
        return cached
    profile = profile_config()
    overrides = dict(_section().get("stages") or {})
    merged: dict[str, dict] = {}
    for name, base in (profile.get("stages") or FALLBACK_STAGES).items():
        entry = _merge_stage(FALLBACK_STAGES.get(name, {}), base)
        raw_override = overrides.get(name) or {}
        if isinstance(raw_override, dict) and raw_override.get("enabled") is not None:
            entry["enabled"] = bool(raw_override["enabled"])
        entry["name"] = name
        entry["default"] = bool((profile.get("stages") or {}).get(name, {}).get("enabled", entry["enabled"]))
        merged[name] = entry
    for name, base in FALLBACK_STAGES.items():
        if name not in merged:
            entry = copy.deepcopy(base)
            entry["name"] = name
            entry["default"] = bool(entry["enabled"])
            merged[name] = entry
    with _CACHE_LOCK:
        _CACHE["stages"] = merged
        _CACHE["at"] = time.monotonic()
    return merged


def stage_enabled(name: str) -> bool:
    """Return whether one pipeline stage is enabled (unknown = enabled)."""
    stage = stages().get(str(name))
    return bool(stage["enabled"]) if stage else True


def stage_params(name: str) -> dict:
    """Return the resolved parameter mapping of one stage."""
    return dict((stages().get(str(name)) or {}).get("params") or {})


def set_stage(name: str, enabled: bool) -> dict:
    """Persist the enabled flag of one stage.

    Args:
        name: Stage identifier from the active profile.
        enabled: New flag.

    Returns:
        The updated merged stage view for that stage.

    Raises:
        KeyError: Unknown stage name.
    """
    if name not in stages():
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
    """Merged auto-verb view: built-ins plus operator overrides, additions and catalog."""
    with _CACHE_LOCK:
        cached = _CACHE["verbs"]
        fresh = cached is not None and (time.monotonic() - float(_CACHE["at"])) < CACHE_TTL_SEC
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
        seen.add(verb)
    merged.extend(_catalog_verbs(seen, overrides))
    with _CACHE_LOCK:
        _CACHE["verbs"] = merged
        _CACHE["at"] = time.monotonic()
    return [dict(entry) for entry in merged]


def _catalog_verbs(seen: set[str], overrides: dict) -> list[dict]:
    """Append catalog CLI verbs not already covered by built-ins or overrides.

    Args:
        seen: Verb names already present in the merged view.
        overrides: Payload overrides that win over catalog state.

    Returns:
        Catalog entries shaped like the merged verb view.
    """
    try:
        from modules.verb_catalog import entries as catalog_entries

        table = catalog_entries()
    except Exception:
        return []
    out: list[dict] = []
    for name, stored in sorted(table.items()):
        if name in seen:
            continue
        raw = dict(overrides.get(name) or {})
        out.append(
            {
                "name": name,
                "enabled": bool(raw.get("enabled", stored.get("enabled", False))),
                "phases": list(raw.get("phases", [stored.get("phase", "")] if stored.get("phase") else [])),
                "keywords": list(raw.get("keywords") or []),
                "needs_target": bool(raw.get("needs_target", True)),
                "extra_args": str(raw.get("extra_args") or ""),
                "description": str(raw.get("description") or stored.get("description") or ""),
                "source": "catalog",
            }
        )
        seen.add(name)
    return out


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
    """Remove a custom verb, or disable a built-in one."""
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
    """Drop every orchestrator override (back to YAML defaults)."""
    payload = _payload()
    payload.pop("orchestrator", None)
    _save(payload)


def validate_config(data: Any) -> list[str]:
    """Validate one raw orchestration mapping.

    Args:
        data: Parsed YAML document.

    Returns:
        Human-readable errors; an empty list means the document is valid.
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["document must be a mapping"]
    version = data.get("version")
    if isinstance(version, bool) or version != 1:
        errors.append(f"unsupported version: {version!r}")
    stages = data.get("stages", {})
    if stages is not None and not isinstance(stages, dict):
        errors.append("stages must be a mapping")
        stages = {}
    for name, stage in (stages or {}).items():
        if not isinstance(stage, dict):
            errors.append(f"stage {name} must be a mapping")
            continue
        if "enabled" in stage and not isinstance(stage["enabled"], bool):
            errors.append(f"stage {name} enabled must be a boolean")
        if "label" in stage and not isinstance(stage["label"], str):
            errors.append(f"stage {name} label must be a string")
        if "fires_when" in stage and not isinstance(stage["fires_when"], str):
            errors.append(f"stage {name} fires_when must be a string")
        if "params" in stage and not isinstance(stage["params"], dict):
            errors.append(f"stage {name} params must be a mapping")
    profiles = data.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        errors.append("profiles must be a non-empty mapping")
        return errors
    default = str(data.get("default_profile", "") or "")
    if default and default not in profiles:
        errors.append(f"default_profile {default!r} is not declared")
    known_stages = set(stages or {})
    for name, profile in profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"profile {name} must be a mapping")
            continue
        parent = str(profile.get("extends", "") or "")
        if parent and parent not in profiles:
            errors.append(f"profile {name} extends unknown profile {parent!r}")
        for key in ("limits", "budget", "sinks"):
            if key in profile and not isinstance(profile[key], dict):
                errors.append(f"profile {name} {key} must be a mapping")
        for key, value in (profile.get("limits") or {}).items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors.append(f"profile {name} limit {key} must be numeric")
            elif value < 0:
                errors.append(f"profile {name} limit {key} must be non-negative")
        for key, value in (profile.get("sinks") or {}).items():
            if not isinstance(value, bool):
                errors.append(f"profile {name} sink {key} must be a boolean")
        for stage_name in (profile.get("stages") or {}):
            if stage_name not in known_stages:
                errors.append(f"profile {name} references unknown stage {stage_name!r}")
    try:
        from modules.trigger_policy import validate_triggers

        errors.extend(f"triggers: {error}" for error in validate_triggers(data.get("triggers")))
    except Exception:
        pass
    return errors


__all__ = [
    "DEFAULT_STAGES",
    "FALLBACK_BUDGET",
    "FALLBACK_LIMITS",
    "FALLBACK_SINKS",
    "FALLBACK_STAGES",
    "ORCHESTRATOR_YAML_PATH",
    "STAGE_DEFS",
    "active_profile",
    "budget",
    "chain_defaults",
    "effective_verbs",
    "limits",
    "profiles",
    "profile_config",
    "reload",
    "remove_verb",
    "reset",
    "set_profile",
    "set_stage",
    "sinks",
    "stage_enabled",
    "stage_params",
    "stages",
    "upsert_verb",
    "validate_config",
    "verb_config",
    "verb_enabled",
]
