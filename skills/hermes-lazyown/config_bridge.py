"""
Configuration bridge: unifies LazyOwn payload.json, environment variables,
and fallback defaults into a single read-only configuration source.

Follows the Adapter pattern: downstream code depends on this abstraction,
not on payload.json directly.
"""

import json
import os
from pathlib import Path
from typing import Any

from constants import ConfigKeys, Defaults, EnvKeys, Paths


class ConfigBridgeError(Exception):
    """Raised when the configuration bridge cannot resolve a required value."""

    pass


class ConfigBridge:
    """
    Unified configuration accessor for the Hermes-LazyOwn integration.

    Reads from (highest priority first):
      1. Environment variables (HERMES_*, LAZYOWN_*)
      2. payload.json
      3. Module-level Defaults

    All values are cached on first read. Call refresh() to invalidate cache.
    """

    def __init__(self, payload_path: Path | None = None) -> None:
        self._payload_path = payload_path or Paths.payload_file()
        self._payload_cache: dict[str, Any] | None = None
        self._payload_mtime: float | None = None

    # ── Public API ──────────────────────────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for *key*, or *default* if not found anywhere."""
        return self._resolve(key, default)

    def get_required(self, key: str) -> Any:
        """Return the value for *key*, raising ConfigBridgeError if missing."""
        value = self._resolve(key, None)
        if value is None:
            raise ConfigBridgeError(f"Required configuration key '{key}' is not set.")
        return value

    def get_str(self, key: str, default: str = "") -> str:
        """Return the string value for *key*."""
        value = self._resolve(key, default)
        return str(value) if value is not None else default

    def get_int(self, key: str, default: int = 0) -> int:
        """Return the integer value for *key*."""
        value = self._resolve(key, default)
        try:
            return int(value) if value is not None else default
        except (TypeError, ValueError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Return the boolean value for *key*."""
        value = self._resolve(key, default)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "yes", "on")

    def refresh(self) -> None:
        """Invalidate all caches so the next read reloads from disk."""
        self._payload_cache = None
        self._payload_mtime = None

    def active_target(self) -> dict[str, Any]:
        """Return a dict with the minimal target context (rhost, domain, os_id)."""
        return {
            ConfigKeys.RHOST: self.get_str(ConfigKeys.RHOST),
            ConfigKeys.DOMAIN: self.get_str(ConfigKeys.DOMAIN),
            ConfigKeys.OS_ID: self.get_str(ConfigKeys.OS_ID),
            ConfigKeys.START_USER: self.get_str(ConfigKeys.START_USER),
            ConfigKeys.START_PASS: self.get_str(ConfigKeys.START_PASS),
        }

    def attacker_context(self) -> dict[str, Any]:
        """Return a dict with the attacker context (lhost, lport, etc.)."""
        return {
            ConfigKeys.LHOST: self.get_str(ConfigKeys.LHOST),
            ConfigKeys.LPORT: self.get_int(ConfigKeys.LPORT, Defaults.TIMEOUT_SECONDS),
            ConfigKeys.C2_PORT: self.get_int(ConfigKeys.C2_PORT, 4444),
            ConfigKeys.API_KEY: self.get_str(ConfigKeys.API_KEY),
        }

    def is_hermes_session(self) -> bool:
        """Return True if running inside a Hermes agent session."""
        return bool(os.environ.get(EnvKeys.HERMES_SESSION_ID))

    # ── Internal helpers ────────────────────────────────────────────────────────

    def _resolve(self, key: str, default: Any) -> Any:
        """Resolve a key across env -> payload -> built-in default."""
        env_value = self._from_env(key)
        if env_value is not None:
            return env_value

        payload_value = self._from_payload(key)
        if payload_value is not None:
            return payload_value

        return default

    def _from_env(self, key: str) -> Any:
        """Map payload keys to env var names and return the value, if set."""
        env_map = {
            ConfigKeys.RHOST: EnvKeys.LAZYOWN_DIR,
            ConfigKeys.C2_PORT: EnvKeys.LAZYOWN_C2_PORT,
        }
        env_key = env_map.get(key)
        if env_key:
            value = os.environ.get(env_key)
            if value is not None:
                return value
        # Direct mapping: LAZYOWN_RHOST, LAZYOWN_LHOST, etc.
        direct = os.environ.get(f"LAZYOWN_{key.upper()}")
        if direct is not None:
            return direct
        return None

    def _from_payload(self, key: str) -> Any:
        """Return the value from payload.json, loading the file if needed."""
        cache = self._load_payload()
        return cache.get(key)

    def _load_payload(self) -> dict[str, Any]:
        """Lazy-load payload.json with mtime check."""
        path = self._payload_path
        try:
            mtime = path.stat().st_mtime
        except OSError:
            mtime = None

        if self._payload_cache is not None and self._payload_mtime == mtime:
            return self._payload_cache

        if not path.exists():
            self._payload_cache = {}
            self._payload_mtime = mtime
            return self._payload_cache

        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            raise ConfigBridgeError(
                f"Failed to parse payload.json at {path}: {exc}"
            ) from exc

        self._payload_cache = data if isinstance(data, dict) else {}
        self._payload_mtime = mtime
        return self._payload_cache
