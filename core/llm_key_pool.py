"""Per-backend LLM API key pool with round-robin rotation and quota cooldown.

sapper-v2 keeps a pool of API keys (``SAPPER_KEY_POOL``) and rotates to the
next one when a provider returns an explicit quota/credit error, so a long
autonomous run survives the exhaustion of any single key. LazyOwn already
rotates *models/members* on quota (``modules.lazy_loop.task_llm_chain``); this
module adds the orthogonal *key* axis.

The pool is pure and process-wide. It reads nothing itself: a builder parses
``payload.json`` once via :func:`build_from_config`, seeding each backend's
pool with its primary key first so a single-key deployment behaves exactly as
before. Keys that hit an explicit quota error are parked for a cooldown window
and skipped until it elapses; when every key is cooling down the least-recently
parked one is returned so the caller still makes progress.

Config shape (``payload.json``):
    ``llm_key_pool``: either a flat list of extra keys for the default cloud
    backend (groq), or a mapping ``{backend: [keys, ...]}``. The backend's
    primary key (``api_key``/``openai_api_key``/...) is always tried first.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Iterable, Mapping
from typing import Any

_DEFAULT_COOLDOWN_SEC = 900.0
_POOL_BACKENDS = ("groq", "openai", "anthropic", "deepseek")
_PRIMARY_KEY_FIELDS = {
    "groq": "api_key",
    "openai": "openai_api_key",
    "anthropic": "anthropic_api_key",
    "deepseek": "deepseek_api_key",
}


def _is_real_key(value: object) -> bool:
    """Return True when a value is a non-placeholder API key string.

    Args:
        value: Candidate key.

    Returns:
        True when the trimmed value is set and is not a shipped placeholder.
    """
    text = str(value or "").strip()
    if not text:
        return False
    lowered = text.lower()
    return lowered not in ("api_key",) and "your_api_key" not in lowered


def _dedupe(keys: Iterable[str]) -> list[str]:
    """Return keys in first-seen order without duplicates or placeholders."""
    seen: set[str] = set()
    ordered: list[str] = []
    for key in keys:
        if not _is_real_key(key) or key in seen:
            continue
        seen.add(key)
        ordered.append(key)
    return ordered


class KeyPool:
    """Thread-safe round-robin key selector with per-key quota cooldown.

    One pool instance serves every backend. Each backend has an ordered key
    list (primary first) plus a cursor and a cooldown map. The pool never
    performs I/O; callers mark a key exhausted when the provider reports an
    explicit quota error.
    """

    def __init__(self, cooldown_sec: float = _DEFAULT_COOLDOWN_SEC) -> None:
        """Initialize an empty pool.

        Args:
            cooldown_sec: Seconds a quota-exhausted key is skipped.
        """
        self._lock = threading.RLock()
        self._keys: dict[str, list[str]] = {}
        self._cursor: dict[str, int] = {}
        self._cooldown: dict[str, dict[str, float]] = {}
        self._cooldown_sec = max(1.0, float(cooldown_sec))

    def set_keys(self, backend: str, keys: Iterable[str]) -> None:
        """Replace the key list for one backend.

        Args:
            backend: Backend identifier.
            keys: Ordered candidate keys (primary first); placeholders and
                duplicates are dropped.
        """
        with self._lock:
            ordered = _dedupe(keys)
            self._keys[backend] = ordered
            self._cursor.setdefault(backend, 0)
            if self._cursor[backend] >= len(ordered):
                self._cursor[backend] = 0
            live = set(ordered)
            self._cooldown[backend] = {
                key: until for key, until in self._cooldown.get(backend, {}).items() if key in live
            }

    def has_pool(self, backend: str) -> bool:
        """Return True when more than one key is configured for the backend."""
        with self._lock:
            return len(self._keys.get(backend, [])) > 1

    def size(self, backend: str) -> int:
        """Return the number of keys configured for the backend."""
        with self._lock:
            return len(self._keys.get(backend, []))

    def next_key(self, backend: str, now: float | None = None) -> str | None:
        """Return the next usable key for a backend, advancing the cursor.

        Keys in cooldown are skipped. When every key is cooling down the one
        whose cooldown expires soonest is returned so progress continues.

        Args:
            backend: Backend identifier.
            now: Optional monotonic-equivalent timestamp (for tests).

        Returns:
            A key string, or None when no keys are configured.
        """
        stamp = time.time() if now is None else now
        with self._lock:
            keys = self._keys.get(backend, [])
            if not keys:
                return None
            cooldown = self._cooldown.get(backend, {})
            count = len(keys)
            start = self._cursor.get(backend, 0) % count
            for offset in range(count):
                index = (start + offset) % count
                key = keys[index]
                until = cooldown.get(key, 0.0)
                if until <= stamp:
                    self._cursor[backend] = (index + 1) % count
                    return key
            soonest = min(keys, key=lambda candidate: cooldown.get(candidate, 0.0))
            self._cursor[backend] = (keys.index(soonest) + 1) % count
            return soonest

    def mark_exhausted(self, backend: str, key: str, now: float | None = None) -> None:
        """Park a key for the cooldown window after an explicit quota error.

        Args:
            backend: Backend identifier.
            key: The key that reported quota exhaustion.
            now: Optional timestamp (for tests).
        """
        if not _is_real_key(key):
            return
        stamp = time.time() if now is None else now
        with self._lock:
            self._cooldown.setdefault(backend, {})[key] = stamp + self._cooldown_sec

    def available(self, backend: str, now: float | None = None) -> int:
        """Return how many keys are not currently cooling down."""
        stamp = time.time() if now is None else now
        with self._lock:
            keys = self._keys.get(backend, [])
            cooldown = self._cooldown.get(backend, {})
            return sum(1 for key in keys if cooldown.get(key, 0.0) <= stamp)

    def reset(self) -> None:
        """Clear every backend's keys, cursors and cooldowns."""
        with self._lock:
            self._keys.clear()
            self._cursor.clear()
            self._cooldown.clear()


def _pool_entries(raw: Any) -> dict[str, list[str]]:
    """Normalize the ``llm_key_pool`` config value into per-backend lists.

    Args:
        raw: The raw ``llm_key_pool`` value (list, mapping or None).

    Returns:
        A mapping of backend to extra key list.
    """
    entries: dict[str, list[str]] = {}
    if isinstance(raw, Mapping):
        for backend, keys in raw.items():
            name = str(backend).strip().lower()
            if name not in _POOL_BACKENDS:
                continue
            if isinstance(keys, str):
                values = [keys]
            elif isinstance(keys, Iterable):
                values = [str(item) for item in keys]
            else:
                values = []
            entries[name] = values
    elif isinstance(raw, str):
        entries["groq"] = [raw]
    elif isinstance(raw, Iterable):
        entries["groq"] = [str(item) for item in raw]
    return entries


def build_from_config(config: Mapping[str, Any], pool: KeyPool | None = None) -> KeyPool:
    """Build or refresh a :class:`KeyPool` from a payload-derived mapping.

    Each backend's pool is seeded with its primary configured key first, then
    the extra keys from ``llm_key_pool``, so a deployment without a pool keeps
    its single primary key and unchanged behaviour.

    Args:
        config: A mapping derived from ``payload.json``.
        pool: An existing pool to refresh, or None to build a fresh one.

    Returns:
        The populated pool.
    """
    target = pool if pool is not None else KeyPool()
    extras = _pool_entries(config.get("llm_key_pool"))
    for backend in _POOL_BACKENDS:
        primary = config.get(_PRIMARY_KEY_FIELDS[backend])
        ordered: list[str] = []
        if _is_real_key(primary):
            ordered.append(str(primary))
        ordered.extend(extras.get(backend, []))
        target.set_keys(backend, ordered)
    return target


_GLOBAL_POOL = KeyPool()
_GLOBAL_LOCK = threading.Lock()


def get_key_pool() -> KeyPool:
    """Return the process-wide key pool singleton."""
    return _GLOBAL_POOL


def refresh_from_config(config: Mapping[str, Any]) -> KeyPool:
    """Refresh and return the global pool from a payload-derived mapping."""
    with _GLOBAL_LOCK:
        return build_from_config(config, _GLOBAL_POOL)


def resolve_pooled_key(backend: str, config: Mapping[str, Any], fallback: str | None) -> str | None:
    """Return the next pooled key for a backend, or ``fallback`` when no pool.

    A single-key backend returns ``fallback`` unchanged so nothing about the
    default deployment changes. Only when two or more real keys exist does the
    round-robin take over.

    Args:
        backend: Backend identifier.
        config: Payload-derived mapping (used to refresh the pool lazily).
        fallback: The key the caller resolved by its normal path.

    Returns:
        A usable key, or ``fallback`` when no multi-key pool is configured.
    """
    name = str(backend or "").strip().lower()
    if name not in _POOL_BACKENDS:
        return fallback
    refresh_from_config(config)
    pool = get_key_pool()
    if not pool.has_pool(name):
        return fallback
    return pool.next_key(name) or fallback


def note_quota_error(backend: str, key: str | None) -> None:
    """Park a key on the global pool after an explicit provider quota error.

    A no-op when the key is unknown or empty, so quota-detection call sites can
    invoke it unconditionally.

    Args:
        backend: Backend identifier.
        key: The key that reported quota exhaustion.
    """
    name = str(backend or "").strip().lower()
    if name not in _POOL_BACKENDS or not _is_real_key(key):
        return
    get_key_pool().mark_exhausted(name, str(key))


__all__ = [
    "KeyPool",
    "build_from_config",
    "get_key_pool",
    "note_quota_error",
    "refresh_from_config",
    "resolve_pooled_key",
]
