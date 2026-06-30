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
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.payload_schema import ValidationIssue

PAYLOAD_FILENAME = "payload.json"
PAYLOAD_PATH = Path(PAYLOAD_FILENAME)

_AES_KEY_FILENAME = "key.aes"
_AES_KEY_BYTES = 32
_AES_KEY_HEX_LEN = 64
_AES_KEY_FILE_MODE = 0o600


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
            raise ValueError(
                f"aes_key must be {_AES_KEY_HEX_LEN} hex characters when set, got {len(raw)}"
            )
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
            raise ValueError(
                f"On-disk AES key at {key_file} has length {len(existing)}, expected {_AES_KEY_BYTES}"
            )
        return existing
    fresh = os.urandom(_AES_KEY_BYTES)
    key_file.write_bytes(fresh)
    os.chmod(key_file, _AES_KEY_FILE_MODE)
    return fresh


def load_payload(path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> dict[str, Any]:
    """Load and return the JSON payload at ``path``.

    Raises:
        FileNotFoundError: if the payload does not exist.
        json.JSONDecodeError: if the payload is not valid JSON.
    """
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_and_validate(
    path: str | os.PathLike[str] = PAYLOAD_FILENAME,
) -> tuple[dict[str, Any], list[ValidationIssue]]:
    """Load ``payload.json`` and return it together with schema issues.

    Validation never raises: a malformed value produces a
    :class:`core.payload_schema.ValidationIssue` so callers can decide
    whether to warn the operator, abort, or coerce. The dictionary is
    returned exactly as loaded so the existing free-form behaviour is
    preserved.

    Args:
        path: Filesystem location of the payload (defaults to
            ``payload.json`` in the current working directory).

    Returns:
        ``(payload, issues)`` tuple. ``issues`` is empty when the payload
        matches the schema; otherwise it contains a structured entry per
        problem detected by :func:`core.payload_schema.validate_payload`.
    """
    from core.payload_schema import validate_payload

    payload = load_payload(path)
    issues = validate_payload(payload)
    return payload, issues


def save_payload(payload: dict[str, Any], path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> None:
    """Atomically write ``payload`` as pretty-printed JSON to ``path``.

    Uses a sibling ``*.tmp`` file plus ``os.replace`` so a crash mid-write
    cannot leave the operator with a half-written payload.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent or "."),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp_name, target)
    except Exception:
        if os.path.exists(tmp_name):
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        raise


__all__ = [
    "Config",
    "load_payload",
    "load_and_validate",
    "save_payload",
    "resolve_aes_key",
    "PAYLOAD_PATH",
    "PAYLOAD_FILENAME",
]
