"""Operator-owned YAML catalog of every routable shell verb.

The autonomous loop historically routed only the built-in ``auto_*``
verbs; every other cmd2 command was reachable only when the text of an
intent literally named it. This module flips the model: the shell
catalogue is discovered once (``cli/command_index.json`` plus the same
``do_*`` scan the CLI bridge uses), materialised as ``config/verbs.yaml``
and every entry starts disabled unless it is enabled today.

Ownership split (SOLID):

- this module owns discovery, YAML persistence and catalog queries;
- ``modules/orchestrator_config`` keeps owning the merged view the loop
  reads, so the TUI, the API and the planner see one truth;
- operator toggles live in ``config/verbs.yaml`` (versioned, diffable),
  payload overrides keep working for advanced verb fields.

A missing, invalid or oversized YAML never raises into the loop: the
catalog degrades to "no catalog entries" and routing falls back to the
built-in verb set only.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

import logging

log = logging.getLogger("verb_catalog")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG_PATH = REPO_ROOT / "config" / "verbs.yaml"
DEFAULT_INDEX_PATH = REPO_ROOT / "cli" / "command_index.json"

BUILTIN_ENABLED_VERBS: frozenset[str] = frozenset({"lazynmap"})

_CACHE_TTL_SEC = 2.0
_CACHE_LOCK = threading.Lock()
_WRITE_LOCK = threading.Lock()
_CACHE: dict[str, Any] = {"at": 0.0, "path": None, "entries": None}


@dataclass(frozen=True)
class VerbCatalogConfig:
    """Centralised paths and limits for the catalog subsystem.

    Args:
        catalog_path: YAML file holding the operator catalog.
        index_path: Pre-built command index JSON.
        version: Schema version this module reads and writes.
        default_enabled: Enabled flag for newly discovered commands.
        max_yaml_bytes: Safety cap so a corrupt file cannot stall reads.
        search_limit: Default row cap for :func:`search`.
    """

    catalog_path: Path = field(default=DEFAULT_CATALOG_PATH)
    index_path: Path = field(default=DEFAULT_INDEX_PATH)
    version: int = 1
    default_enabled: bool = False
    max_yaml_bytes: int = 1_000_000
    search_limit: int = 60


def _default_config() -> VerbCatalogConfig:
    """Return the process-wide configuration (override point for tests)."""
    return VerbCatalogConfig()


def _builtin_names() -> set[str]:
    """Return the verbs that are enabled today and must stay enabled."""
    names = set(BUILTIN_ENABLED_VERBS)
    try:
        from modules.auto_registry import AUTO_VERBS

        names.update(spec.verb for spec in AUTO_VERBS)
    except Exception:
        pass
    return names


def _phase_fallback(verb: str) -> str:
    """Return the kill-chain phase for a verb absent from the index."""
    try:
        from modules.lazy_cli_bridge import phase_for

        return phase_for(verb)
    except Exception:
        return "other"


def _risk_fallback(verb: str) -> str:
    """Return the risk class for a verb absent from the index."""
    try:
        from modules.lazy_cli_bridge import risk_for

        return risk_for(verb)
    except Exception:
        return "safe"


def index_commands(config: VerbCatalogConfig | None = None) -> dict[str, dict[str, str]]:
    """Return discovered shell commands as ``{name: {summary, phase}}``.

    The configured index file is authoritative. When it is missing or
    unreadable the CLI bridge discovery covers the gap so the catalog
    never loses a command that exists in the shell.

    Args:
        config: Active configuration; defaults to the process config.

    Returns:
        Mapping of command name to ``{summary, phase}`` metadata.
    """
    cfg = config or _default_config()
    discovered: dict[str, dict[str, str]] = {}
    try:
        if cfg.index_path.is_file():
            doc = json.loads(cfg.index_path.read_text(encoding="utf-8"))
            for row in doc.get("commands", []) if isinstance(doc, dict) else []:
                if row.get("duplicate_of") is not None:
                    continue
                name = str(row.get("name", ""))[3:]
                if name:
                    discovered[name] = {
                        "summary": str(row.get("summary") or ""),
                        "phase": str(row.get("phase") or ""),
                    }
    except (OSError, ValueError) as exc:
        log.warning("command index unreadable at %s: %s", cfg.index_path, exc)
        discovered = {}
    if not discovered:
        try:
            from modules.lazy_cli_bridge import cli_verbs

            discovered = {verb: {"summary": "", "phase": ""} for verb in cli_verbs()}
        except Exception:
            discovered = {}
    return discovered


def validate_catalog(data: Any) -> list[str]:
    """Validate one raw catalog document.

    Args:
        data: Parsed YAML document.

    Returns:
        Human-readable errors; an empty list means the document is valid.
    """
    if not isinstance(data, dict):
        return ["document must be a mapping"]
    errors: list[str] = []
    version = data.get("version")
    if isinstance(version, bool) or version != 1:
        errors.append(f"unsupported version: {version!r}")
    verbs = data.get("verbs")
    if verbs is None:
        return errors
    if not isinstance(verbs, dict):
        errors.append("verbs must be a mapping")
        return errors
    for name, entry in verbs.items():
        if not isinstance(entry, dict):
            errors.append(f"verb {name} must be a mapping")
            continue
        if not isinstance(entry.get("enabled", False), bool):
            errors.append(f"verb {name} enabled must be a boolean")
        for key in ("phase", "risk", "description", "source"):
            if key in entry and not isinstance(entry[key], str):
                errors.append(f"verb {name} {key} must be a string")
    return errors


def load(config: VerbCatalogConfig | None = None) -> dict[str, dict[str, Any]]:
    """Return the raw catalog mapping ``{name: entry}``.

    Args:
        config: Active configuration; defaults to the process config.

    Returns:
        The parsed ``verbs`` mapping, or an empty mapping when the file
        is missing, oversized, or invalid.
    """
    cfg = config or _default_config()
    if yaml is None:
        log.warning("PyYAML is unavailable; verb catalog disabled")
        return {}
    try:
        if not cfg.catalog_path.is_file() or cfg.catalog_path.stat().st_size > cfg.max_yaml_bytes:
            return {}
        with cfg.catalog_path.open("r", encoding="utf-8", errors="replace") as handle:
            data = yaml.safe_load(handle)
    except Exception as exc:
        log.warning("verb catalog unreadable at %s: %s", cfg.catalog_path, exc)
        return {}
    if not isinstance(data, dict):
        log.warning("verb catalog at %s is not a mapping", cfg.catalog_path)
        return {}
    errors = validate_catalog(data)
    if errors:
        log.warning("verb catalog invalid at %s: %s", cfg.catalog_path, "; ".join(errors))
        return {}
    verbs = data.get("verbs") or {}
    return {str(name): dict(entry) for name, entry in verbs.items() if isinstance(entry, dict)}


def entries(config: VerbCatalogConfig | None = None) -> dict[str, dict[str, Any]]:
    """Return the catalog with defaults filled in, cached briefly.

    Args:
        config: Active configuration; defaults to the process config.

    Returns:
        Mapping of command name to entry with keys ``enabled``,
        ``phase``, ``risk``, ``description`` and ``source``.
    """
    cfg = config or _default_config()
    key = str(cfg.catalog_path)
    with _CACHE_LOCK:
        cached_path = _CACHE["path"]
        fresh = (
            cached_path == key
            and _CACHE["entries"] is not None
            and (time.monotonic() - float(_CACHE["at"])) < _CACHE_TTL_SEC
        )
        if fresh:
            return dict(_CACHE["entries"])
    discovered = index_commands(cfg)
    raw = load(cfg)
    merged: dict[str, dict[str, Any]] = {}
    for name, meta in discovered.items():
        stored = dict(raw.get(name) or {})
        phase = str(stored.get("phase") or meta.get("phase") or "")
        if phase in ("", "uncategorized"):
            phase = _phase_fallback(name)
        merged[name] = {
            "enabled": bool(stored.get("enabled", cfg.default_enabled)),
            "phase": phase,
            "risk": str(stored.get("risk") or _risk_fallback(name)),
            "description": str(stored.get("description") or meta.get("summary") or ""),
            "source": str(stored.get("source") or "cli"),
        }
    for name, stored in raw.items():
        if name in merged:
            continue
        merged[name] = {
            "enabled": bool(stored.get("enabled", cfg.default_enabled)),
            "phase": str(stored.get("phase") or "") or _phase_fallback(name),
            "risk": str(stored.get("risk") or _risk_fallback(name)),
            "description": str(stored.get("description") or ""),
            "source": str(stored.get("source") or "cli"),
        }
    with _CACHE_LOCK:
        _CACHE["path"] = key
        _CACHE["entries"] = dict(merged)
        _CACHE["at"] = time.monotonic()
    return dict(merged)


def catalog_enabled(name: str, config: VerbCatalogConfig | None = None) -> bool | None:
    """Return the catalog state of one verb.

    Args:
        name: Command name without the ``do_`` prefix.
        config: Active configuration; defaults to the process config.

    Returns:
        ``True``/``False`` when catalogued, ``None`` when unknown so the
        caller can apply its own fallback.
    """
    entry = entries(config).get(str(name or "").strip())
    return None if entry is None else bool(entry["enabled"])


def catalog_source(name: str, config: VerbCatalogConfig | None = None) -> str | None:
    """Return the catalog source of one verb, ``None`` when unknown.

    Args:
        name: Command name without the ``do_`` prefix.
        config: Active configuration; defaults to the process config.

    Returns:
        The source tag (``cli``, or another registered layer).
    """
    entry = entries(config).get(str(name or "").strip())
    return None if entry is None else str(entry["source"])


def set_enabled(name: str, enabled: bool, config: VerbCatalogConfig | None = None) -> dict[str, Any]:
    """Flip one verb in the YAML catalog atomically.

    Args:
        name: Command name without the ``do_`` prefix.
        enabled: New flag.
        config: Active configuration; defaults to the process config.

    Returns:
        The updated entry.

    Raises:
        KeyError: The command is not exposed by the shell.
        ValueError: The verb name is empty or the YAML cannot be written.
    """
    clean = str(name or "").strip()
    if not clean:
        raise ValueError("verb name is required")
    cfg = config or _default_config()
    discovered = index_commands(cfg)
    with _WRITE_LOCK:
        if clean not in discovered and clean not in load(cfg):
            raise KeyError(f"unknown shell verb: {clean!r}")
        raw = load(cfg)
        entry = dict(raw.get(clean) or {})
        entry["enabled"] = bool(enabled)
        entry.setdefault("phase", discovered.get(clean, {}).get("phase") or _phase_fallback(clean))
        entry.setdefault("risk", _risk_fallback(clean))
        entry.setdefault("description", discovered.get(clean, {}).get("summary") or "")
        entry.setdefault("source", "cli")
        raw[clean] = entry
        _write(cfg, raw)
    _drop_cache(str(cfg.catalog_path))
    return dict(entry)


def sync(config: VerbCatalogConfig | None = None) -> dict[str, int]:
    """Materialise the discovered shell catalogue into the YAML file.

    Operator choices are preserved: entries keep their stored ``enabled``
    flag, today's built-ins default to enabled and every newly discovered
    command lands disabled. Commands that no longer exist are pruned.

    Args:
        config: Active configuration; defaults to the process config.

    Returns:
        Statistics ``{added, kept, removed, total, on, off}``.
    """
    cfg = config or _default_config()
    discovered = index_commands(cfg)
    builtins = _builtin_names()
    with _WRITE_LOCK:
        raw = load(cfg)
        merged: dict[str, dict[str, Any]] = {}
        added = 0
        kept = 0
        for name, meta in discovered.items():
            stored = raw.get(name)
            if stored is None:
                merged[name] = {
                    "enabled": name in builtins,
                    "phase": meta.get("phase") or "",
                    "risk": _risk_fallback(name),
                    "description": meta.get("summary") or "",
                    "source": "builtin" if name in builtins else "cli",
                }
                added += 1
            else:
                entry = dict(stored)
                entry.setdefault("phase", meta.get("phase") or "")
                entry.setdefault("risk", _risk_fallback(name))
                entry.setdefault("description", meta.get("summary") or "")
                entry.setdefault("source", "builtin" if name in builtins else "cli")
                merged[name] = entry
                kept += 1
        removed = len(raw) - len([name for name in raw if name in discovered])
        _write(cfg, merged)
    _drop_cache(str(cfg.catalog_path))
    on = sum(1 for entry in merged.values() if entry["enabled"])
    return {"added": added, "kept": kept, "removed": max(0, removed), "total": len(merged), "on": on, "off": len(merged) - on}


def _write(cfg: VerbCatalogConfig, verbs: dict[str, dict[str, Any]]) -> bool:
    """Persist the verb mapping atomically (tmp + rename).

    Args:
        cfg: Active configuration.
        verbs: Full verb mapping to store.

    Returns:
        ``True`` on success, ``False`` when the filesystem rejects it.
    """
    if yaml is None:
        return False
    try:
        cfg.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = cfg.catalog_path.with_suffix(cfg.catalog_path.suffix + ".tmp")
        payload = {"version": cfg.version, "verbs": dict(sorted(verbs.items()))}
        tmp.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
        tmp.replace(cfg.catalog_path)
        return True
    except OSError as exc:
        log.warning("verb catalog write failed at %s: %s", cfg.catalog_path, exc)
        return False


def _drop_cache(path_key: str) -> None:
    """Invalidate the entries cache after a write."""
    with _CACHE_LOCK:
        if _CACHE["path"] in (None, path_key):
            _CACHE["entries"] = None
            _CACHE["at"] = 0.0


def stats(config: VerbCatalogConfig | None = None) -> dict[str, int]:
    """Summarise the catalog for the brief and the HTTP API.

    Args:
        config: Active configuration; defaults to the process config.

    Returns:
        ``{total, on, off}``.
    """
    table = entries(config)
    on = sum(1 for entry in table.values() if entry["enabled"])
    return {"total": len(table), "on": on, "off": len(table) - on}


def search(
    query: str = "",
    config: VerbCatalogConfig | None = None,
    phase: str = "",
    enabled: bool | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Search catalog entries by substring, phase and state.

    Args:
        query: Case-insensitive substring over name and description.
        config: Active configuration; defaults to the process config.
        phase: Optional exact kill-chain phase filter.
        enabled: Optional state filter.
        limit: Row cap; defaults to ``VerbCatalogConfig.search_limit``.

    Returns:
        Matching entries with the name injected, sorted by name.
    """
    cfg = config or _default_config()
    needle = (query or "").strip().lower()
    wanted_phase = (phase or "").strip().lower()
    cap = max(1, int(limit or cfg.search_limit))
    table = entries(cfg)
    out: list[dict[str, Any]] = []
    for name in sorted(table):
        entry = table[name]
        if enabled is not None and entry["enabled"] != enabled:
            continue
        if wanted_phase and entry["phase"] != wanted_phase:
            continue
        if needle and needle not in name.lower() and needle not in entry["description"].lower():
            continue
        out.append({"name": name, **entry})
        if len(out) >= cap:
            break
    return out


__all__ = [
    "BUILTIN_ENABLED_VERBS",
    "DEFAULT_CATALOG_PATH",
    "DEFAULT_INDEX_PATH",
    "VerbCatalogConfig",
    "catalog_enabled",
    "entries",
    "index_commands",
    "load",
    "search",
    "set_enabled",
    "stats",
    "sync",
    "validate_catalog",
]
