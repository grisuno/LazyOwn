#!/usr/bin/env python3
"""Thread-safe singleton facade over core.config for payload.json.

Contract: preserves the get_config/set_config/reload_config API while
delegating all file parsing and atomic persistence to core.config. This
removes the duplicated JSON load and dump logic without changing behavior.
"""

from __future__ import annotations

import copy
import logging
import threading
from pathlib import Path
from typing import Any

from core.config import load_payload, save_payload

log = logging.getLogger("config_store")

_DEFAULT_PATH = Path(__file__).parent.parent / "payload.json"

# ── Singleton state ────────────────────────────────────────────────────────────

_lock: threading.RLock = threading.RLock()
_data: dict[str, Any] = {}
_payload_path: Path = _DEFAULT_PATH
_last_mtime: float = 0.0
_watcher_thread: threading.Thread | None = None
_watcher_stop: threading.Event = threading.Event()


# ── Public API ─────────────────────────────────────────────────────────────────

def init(path: str | Path = _DEFAULT_PATH, watch: bool = False) -> None:
    """
    Initialise the config store (idempotent).

    Parameters
    ----------
    path  : path to payload.json (default: <project_root>/payload.json)
    watch : if True, start a background thread that reloads on file change
    """
    global _payload_path
    with _lock:
        _payload_path = Path(path)
        _load()
    if watch:
        _start_watcher()


def get_config(key: str = "", default: Any = None) -> Any:
    """
    Return a config value (or the full dict when *key* is empty).

    Always returns a deep copy so callers cannot mutate the cache.
    """
    _ensure_loaded()
    with _lock:
        if not key:
            return copy.deepcopy(_data)
        return copy.deepcopy(_data.get(key, default))


def set_config(**kwargs: Any) -> None:
    """
    Update one or more keys and persist to disk atomically.

    Example
    -------
        set_config(rhost="10.10.10.10", lport=4444)
    """
    _ensure_loaded()
    with _lock:
        _data.update(kwargs)
        _persist()


def set_config_dict(updates: dict[str, Any]) -> None:
    """
    Bulk-update from a dict and persist to disk.
    """
    _ensure_loaded()
    with _lock:
        _data.update(updates)
        _persist()


def reload_config() -> None:
    """Force reload from disk (discards in-memory changes)."""
    with _lock:
        _load()


def stop_watcher() -> None:
    """Stop the file-watcher background thread (if running)."""
    _watcher_stop.set()
    if _watcher_thread and _watcher_thread.is_alive():
        _watcher_thread.join(timeout=3)


# ── Internal ───────────────────────────────────────────────────────────────────

def _ensure_loaded() -> None:
    """Lazy-load on first access."""
    with _lock:
        if not _data:
            _load()


def _load() -> None:
    """Load payload.json into _data via core.config. Caller must hold _lock."""
    global _last_mtime
    p = _payload_path
    if not p.exists():
        log.warning("payload.json not found at %s — using empty config", p)
        _data.clear()
        return
    try:
        loaded = load_payload(str(p))
        _data.clear()
        _data.update(loaded)
        _last_mtime = p.stat().st_mtime
        log.debug("Config loaded from %s (%d keys)", p, len(_data))
    except (OSError, ValueError) as exc:
        log.error("Failed to load config from %s: %s", p, exc)


def _persist() -> None:
    """Write _data back to disk via core.config. Caller must hold _lock."""
    global _last_mtime
    p = _payload_path
    try:
        save_payload(dict(_data), str(p))
        _last_mtime = p.stat().st_mtime
        log.debug("Config persisted to %s", p)
    except (OSError, ValueError) as exc:
        log.error("Failed to persist config to %s: %s", p, exc)


def _start_watcher(interval: float = 2.0) -> None:
    """Start background thread that reloads config when the file changes."""
    global _watcher_thread
    _watcher_stop.clear()

    def _watch_loop() -> None:
        while not _watcher_stop.wait(interval):
            try:
                mtime = _payload_path.stat().st_mtime
            except FileNotFoundError:
                continue
            with _lock:
                if mtime != _last_mtime:
                    log.info("payload.json changed on disk — reloading")
                    _load()

    _watcher_thread = threading.Thread(
        target=_watch_loop,
        name="config_store_watcher",
        daemon=True,
    )
    _watcher_thread.start()
    log.debug("Config file-watcher started (interval=%.1fs)", interval)


# ── Module-level singleton init (lazy) ────────────────────────────────────────
# No auto-init here; callers use init() or just call get_config() directly
# (which triggers _ensure_loaded on first access).
