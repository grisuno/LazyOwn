"""Configuration loader and Config wrapper.

``payload.json`` is the single source of runtime configuration for the entire
LazyOwn framework. This module exposes:

- ``PAYLOAD_PATH`` constant pointing at ``payload.json`` in the current working
  directory.
- ``load_payload`` / ``save_payload`` for reading and writing it atomically.
- ``Config`` — a thin attribute-style wrapper around the payload dictionary.
- ``resolve_aes_key`` — the AES key resolver used by ``Config`` so the
  key is reachable from the shell, the C2, the MCP, and the lazyaddons
  templating.

Atomic writes go through ``*.tmp`` and ``os.replace`` so a crashed write never
leaves the operator with a corrupt payload file.
"""

from __future__ import annotations

import json
import logging
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

PAYLOAD_FILENAME = "payload.json"
PAYLOAD_PATH = Path(PAYLOAD_FILENAME)

_AES_KEY_FILENAME = "key.aes"
_AES_KEY_BYTES = 32
_AES_KEY_HEX_LEN = 64
_AES_KEY_FILE_MODE = 0o600

LAZYOWN_ENV_PREFIX = "LAZYOWN_"

_CONFIG_AUDIT_LOG = Path("sessions/config_changes.jsonl")

_UNRESOLVED_PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}|<\w+>|YOUR_|CHANGE_ME|REPLACE_ME|INSERT_|__\w+__")

_DEFAULT_VALUE_MARKERS = {
    "CHANGE_ME",
    "YOUR_API_KEY_HERE",
    "YOUR_",
    "CHANGE_ME —",
    "deefbeef",
    "admin",
    "password",
}

_SENSITIVE_PATTERNS = ("pass", "secret", "key", "token")

_overridden_keys: set[str] = set()

logger = logging.getLogger(__name__)

_KEY_MIGRATIONS = {
    "c2_maleable_route": "c2_malleable_route",
    "url_trafic_1": "url_traffic_1",
    "url_trafic_2": "url_traffic_2",
    "url_trafic_3": "url_traffic_3",
}


def _apply_env_overrides(payload: dict[str, Any]) -> dict[str, Any]:
    """Override payload values with matching ``LAZYOWN_*`` environment variables.

    Keys are mapped to lowercase. Integer and boolean coercion is applied
    based on the type of the existing payload value.

    Args:
        payload: The payload dictionary to overlay env vars onto.

    Returns:
        A new dict with env-var overrides applied. The input payload is
        not mutated.
    """
    result = dict(payload)
    for env_key, env_val in os.environ.items():
        if not env_key.startswith(LAZYOWN_ENV_PREFIX):
            continue
        cfg_key = env_key[len(LAZYOWN_ENV_PREFIX) :].lower()
        existing = result.get(cfg_key)
        coerced = _coerce_env_value(env_val, existing)
        if cfg_key in result and result[cfg_key] == coerced:
            continue
        result[cfg_key] = coerced
        _overridden_keys.add(cfg_key)
        logger.info(
            "Env override: %s=%s (from %s)",
            cfg_key,
            _mask_if_sensitive(cfg_key, coerced),
            env_key,
        )
    return result


def _coerce_env_value(raw: str, existing: Any) -> Any:
    """Convert a string env-var value to match the type of *existing*.

    Args:
        raw: The raw string value from the environment variable.
        existing: The current value in the payload dict (used to infer type).

    Returns:
        The coerced value. Defaults to the raw string when the target
        type cannot be determined.
    """
    if isinstance(existing, bool):
        lowered = raw.strip().lower()
        return lowered in {"true", "1", "yes", "on"}
    if isinstance(existing, int):
        try:
            return int(raw, 10)
        except (ValueError, TypeError):
            try:
                return int(raw, 0)
            except (ValueError, TypeError):
                return raw
    return raw


def _mask_if_sensitive(key: str, value: Any) -> str:
    """Return a masked representation when *key* matches a sensitive pattern.

    Args:
        key: Configuration key name.
        value: The raw value associated with the key.

    Returns:
        ``"***"`` for sensitive keys, otherwise a truncated string
        representation (max 80 chars).
    """
    key_lower = key.lower()
    for pattern in _SENSITIVE_PATTERNS:
        if pattern in key_lower:
            return "***"
    return str(value)[:80]


def _log_config_change(key: str, old_value: Any, new_value: Any) -> None:
    """Append a JSONL audit entry recording a configuration change.

    Sensitive values are masked before logging.

    Args:
        key: The configuration key that changed.
        old_value: The previous value (``None`` for newly added keys).
        new_value: The new value.
    """
    try:
        _CONFIG_AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "key": key,
            "old_value": _mask_if_sensitive(key, old_value),
            "new_value": _mask_if_sensitive(key, new_value),
        }
        with open(_CONFIG_AUDIT_LOG, "a", encoding="utf-8") as fh:
            json.dump(entry, fh)
            fh.write("\n")
    except OSError as exc:
        logger.warning("Failed to write config audit log: %s", exc)


def _collect_validation_warnings(payload: dict[str, Any]) -> list[str]:
    """Inspect the payload for non-schema warnings.

    Checks for unresolved placeholders and values that look like
    unchanged factory defaults.

    Args:
        payload: The configuration dictionary.

    Returns:
        List of human-readable warning strings.
    """
    warnings: list[str] = []
    for key, val in payload.items():
        str_val = str(val) if val is not None else ""
        if _UNRESOLVED_PLACEHOLDER_RE.search(str_val):
            warnings.append(f"{key}: value contains unresolved placeholder — {str_val[:60]}")
        for marker in _DEFAULT_VALUE_MARKERS:
            if isinstance(val, str) and marker in val and val.strip() not in {"", "null"}:
                warnings.append(f"{key}: value looks like an unchanged default — {val[:60]}")
                break
    return warnings


class Config:
    """Attribute-style wrapper around a configuration dictionary.

    Behavior is intentionally preserved from the legacy ``utils.Config``:
    every key in the underlying dictionary becomes both an instance attribute
    and is accessible via ``config[key]``. Missing keys via ``__getitem__``
    return ``None`` rather than raising.

    The instance also exposes ``aes_key`` (resolved bytes) and ``as_params``
    (a snapshot of the underlying dictionary) so the LazyOwn shell can
    substitute ``{{aes_key}}`` and other tokens in lazyaddons.
    """

    def __init__(self, config_dict: dict[str, Any], sessions_dir: str | os.PathLike[str] | None = None) -> None:
        _migrate_keys(config_dict)
        self.config: dict[str, Any] = config_dict
        resolved_aes = resolve_aes_key(config_dict, sessions_dir=sessions_dir or Path("sessions"))
        self.config["aes_key"] = resolved_aes.hex()
        for key, value in self.config.items():
            setattr(self, key, value)
        self.aes_key: bytes = resolved_aes

    def __getattr__(self, name: str) -> Any:
        return None

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def as_params(self) -> dict[str, Any]:
        """Return a shallow copy of the underlying parameter dictionary.

        Returns:
            A dict suitable for ``self.params`` on the cmd2 shell. The
            ``aes_key`` value is the hex string, matching the format
            consumed by lazyaddon template substitution.
        """
        return dict(self.config)

    def overridden_keys(self) -> list[str]:
        """Return sorted list of keys that were overridden via ``LAZYOWN_*`` env vars."""
        return sorted(_overridden_keys)


def _migrate_keys(config_dict: dict[str, Any]) -> None:
    """Migrate legacy misspelled config keys to corrected names.

    Copies values from old keys to new, canonical keys without
    removing the old ones so existing payload files continue to work.
    """
    for old_key, new_key in _KEY_MIGRATIONS.items():
        if new_key not in config_dict and old_key in config_dict:
            config_dict[new_key] = config_dict[old_key]
            logger.debug("Migrated config key %s -> %s", old_key, new_key)


def resolve_aes_key(
    config_dict: dict[str, Any],
    *,
    sessions_dir: str | os.PathLike[str],
) -> bytes:
    """Return a 32-byte AES key derived from config, disk, or randomness.

    Args:
        config_dict: The payload dictionary. Looks for an ``aes_key``
            entry holding a 64-character hex string.
        sessions_dir: Directory holding ``key.aes``. Created if missing.

    Returns:
        Exactly 32 bytes suitable for AES-256.

    Raises:
        ValueError: when ``aes_key`` is present but not a 64-char hex.
    """
    raw = (config_dict or {}).get("aes_key")
    if isinstance(raw, str) and raw:
        if len(raw) != _AES_KEY_HEX_LEN:
            raise ValueError(f"aes_key must be {_AES_KEY_HEX_LEN} hex characters when set, got {len(raw)}")
        try:
            return bytes.fromhex(raw)
        except ValueError as exc:
            raise ValueError(f"aes_key is not valid hex: {exc}") from exc
    sessions_path = Path(sessions_dir)
    sessions_path.mkdir(parents=True, exist_ok=True)
    key_file = sessions_path / _AES_KEY_FILENAME
    if key_file.exists():
        existing = key_file.read_bytes()
        if len(existing) != _AES_KEY_BYTES:
            raise ValueError(f"On-disk AES key at {key_file} has length {len(existing)}, expected {_AES_KEY_BYTES}")
        return existing
    fresh = os.urandom(_AES_KEY_BYTES)
    key_file.write_bytes(fresh)
    os.chmod(key_file, _AES_KEY_FILE_MODE)
    return fresh


_EXAMPLE_FILENAME = "payload.example.json"


def _load_raw_payload(path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> dict[str, Any]:
    """Load JSON from *path* and return dict.

    Does **not** apply environment variable overrides. Used internally
    by :func:`load_payload` and for audit comparison in
    :func:`save_payload`.

    Raises:
        FileNotFoundError: if neither the payload nor the example exists.
        json.JSONDecodeError: if the payload is not valid JSON.
    """
    target = Path(path)
    if not target.exists():
        example = target.parent / _EXAMPLE_FILENAME
        if example.exists():
            import shutil

            shutil.copy(str(example), str(target))
    with open(target, encoding="utf-8") as fh:
        raw = json.load(fh)
    return raw


def load_payload(path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> dict[str, Any]:
    """Load and return the JSON payload at ``path``.

    If the payload does not exist but ``payload.example.json`` does, the
    example file is copied to ``path`` automatically so a fresh clone never
    leaves the operator without a starting configuration.

    Environment variable overrides
    (``LAZYOWN_<KEY>``) are applied on top of the file contents.

    Raises:
        FileNotFoundError: if neither the payload nor the example exists.
        json.JSONDecodeError: if the payload is not valid JSON.
    """
    payload = _load_raw_payload(path)
    return _apply_env_overrides(payload)


def load_and_validate(
    path: str | os.PathLike[str] = PAYLOAD_FILENAME,
) -> dict[str, Any]:
    """Load ``payload.json``, validate against the schema, and return a result dict.

    Validation never raises: problems are collected in the ``warnings`` and
    ``errors`` lists of the result dict. The payload is returned in the
    ``payload`` key as loaded.

    Args:
        path: Filesystem location of the payload (defaults to
            ``payload.json`` in the current working directory).

    Returns:
        A dict with keys:
        - ``payload`` (``dict``): the loaded configuration dictionary.
        - ``valid`` (``bool``): ``True`` when no errors were found.
        - ``warnings`` (``list[str]``): advisory issues (schema warnings,
          unresolved placeholders, default-looking values).
        - ``errors`` (``list[str]``): blocking issues from schema
          validation.
        - ``issues`` (``list[ValidationIssue]``): structured schema issues
          for programmatic consumers (preserves backward compat).
    """
    from core.payload_schema import Severity, validate_payload

    payload = load_payload(path)
    schema_issues = validate_payload(payload)

    schema_warnings: list[str] = []
    schema_errors: list[str] = []
    for issue in schema_issues:
        msg = f"{issue.key}: {issue.message}"
        if issue.severity == Severity.ERROR:
            schema_errors.append(msg)
        else:
            schema_warnings.append(msg)

    extra_warnings = _collect_validation_warnings(payload)

    all_warnings = schema_warnings + extra_warnings

    return {
        "payload": payload,
        "valid": len(schema_errors) == 0,
        "warnings": all_warnings,
        "errors": schema_errors,
        "issues": schema_issues,
    }


def save_payload(payload: dict[str, Any], path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> None:
    """Atomically write ``payload`` as pretty-printed JSON to ``path``.

    Uses a sibling ``*.tmp`` file plus ``os.replace`` so a crash mid-write
    cannot leave the operator with a half-written payload.

    Configuration changes are audited to ``sessions/config_changes.jsonl``.
    """
    target = Path(path)

    previous: dict[str, Any] | None = None
    if target.exists():
        try:
            previous = _load_raw_payload(target)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not load existing payload for audit: %s", exc)
    if previous is not None:
        for key, new_val in payload.items():
            old_val = previous.get(key)
            if key not in previous or old_val != new_val:
                _log_config_change(key, old_val, new_val)

    disk_payload = payload

    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent or "."),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(disk_payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp_name, target)
        os.chmod(target, 0o644)
    except Exception:
        if os.path.exists(tmp_name):
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        raise


__all__ = [
    "Config",
    "LAZYOWN_ENV_PREFIX",
    "load_payload",
    "load_and_validate",
    "save_payload",
    "resolve_aes_key",
    "PAYLOAD_PATH",
    "PAYLOAD_FILENAME",
]
