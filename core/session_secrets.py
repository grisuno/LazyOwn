"""Session-scoped secret rotation.

Engagement secrets live only for the lifetime of a session:

- ``aes_key`` — beacon channel AES-256 key (``sessions/key.aes``).
- ``rat_key`` — beacon HMAC signing key (``payload.json``).
- ``session_magic`` — activation string baked into lab implants.

``rotate_session_secrets`` generates all three with ``secrets``/``os.urandom``,
persists them and mirrors the values onto the live config object so the C2,
the shell and the implant builders read the same secrets in one deployment.
``clean`` rotates them again after artifact removal, and the C2 rotates on
boot when ``rotate_keys_on_boot`` is enabled, so nothing durable ships with
a secret that is public knowledge.
"""

from __future__ import annotations

import logging
import os
import secrets
from pathlib import Path
from typing import Any

from core.config import load_payload, save_payload

logger = logging.getLogger(__name__)

_AES_KEY_BYTES = 32
_RAT_KEY_BYTES = 32
_SESSION_MAGIC_BYTES = 16
_KEY_FILE_MODE = 0o600
_SESSIONS_DIRNAME = "sessions"
_KEY_FILENAME = "key.aes"
_SECRETS_KEYS = ("rat_key", "session_magic")


def rotate_session_secrets(
    config_obj: Any = None, sessions_dir: str | os.PathLike[str] = _SESSIONS_DIRNAME
) -> dict[str, str]:
    """Generate and persist a fresh set of session secrets.

    Args:
        config_obj: Optional live config wrapper (``core.config.Config``)
            whose attributes are refreshed in memory.
        sessions_dir: Directory that holds the on-disk AES key file.

    Returns:
        Mapping with the generated ``aes_hex``, ``rat_key`` and
        ``session_magic`` values as strings.

    Raises:
        OSError: if the AES key file or ``payload.json`` cannot be written.
    """
    aes_bytes = os.urandom(_AES_KEY_BYTES)
    aes_hex = aes_bytes.hex()
    rat_key = secrets.token_hex(_RAT_KEY_BYTES).lower()
    session_magic = secrets.token_hex(_SESSION_MAGIC_BYTES).lower()
    key_path = Path(sessions_dir) / _KEY_FILENAME
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_bytes(aes_bytes)
    os.chmod(key_path, _KEY_FILE_MODE)
    payload = load_payload()
    payload["rat_key"] = rat_key
    payload["session_magic"] = session_magic
    save_payload(payload)
    _mirror(config_obj, aes_hex=aes_hex, rat_key=rat_key, session_magic=session_magic)
    logger.info("Rotated session secrets (aes_key, rat_key, session_magic)")
    return {"aes_hex": aes_hex, "rat_key": rat_key, "session_magic": session_magic}


def ensure_session_secrets(
    config_obj: Any = None,
    rotate: bool = False,
    sessions_dir: str | os.PathLike[str] = _SESSIONS_DIRNAME,
) -> dict[str, str]:
    """Return valid session secrets, rotating them when required.

    Args:
        config_obj: Optional live config wrapper refreshed in memory.
        rotate: Force a full rotation regardless of current validity.
        sessions_dir: Directory that holds the on-disk AES key file.

    Returns:
        Mapping with ``aes_hex``, ``rat_key`` and ``session_magic``.
    """
    if rotate:
        return rotate_session_secrets(config_obj, sessions_dir=sessions_dir)
    payload = load_payload()
    rat_key = str(payload.get("rat_key", "") or "")
    session_magic = str(payload.get("session_magic", "") or "")
    key_path = Path(sessions_dir) / _KEY_FILENAME
    aes_ok = key_path.exists() and key_path.stat().st_size == _AES_KEY_BYTES
    if (
        aes_ok
        and _valid_session_token(rat_key, _RAT_KEY_BYTES * 2)
        and _valid_session_token(session_magic, _SESSION_MAGIC_BYTES * 2)
    ):
        aes_hex = key_path.read_bytes().hex()
        if config_obj is not None:
            _mirror(config_obj, aes_hex=aes_hex, rat_key=rat_key, session_magic=session_magic)
        return {"aes_hex": aes_hex, "rat_key": rat_key, "session_magic": session_magic}
    return rotate_session_secrets(config_obj, sessions_dir=sessions_dir)


def _valid_session_token(value: str, hex_len: int) -> bool:
    """Return True when ``value`` is a fresh deployment token of ``hex_len``."""
    if not value or len(value) != hex_len:
        return False
    if any(marker in value.upper() for marker in ("CHANGE_ME", "REPLACE_ME", "YOUR_", "{", "}")):
        return False
    return all(c in "0123456789abcdef" for c in value)


def _mirror(config_obj: Any, aes_hex: str, rat_key: str, session_magic: str) -> None:
    """Refresh ``config_obj`` attributes for the rotated secrets."""
    if config_obj is None:
        return
    try:
        config_obj.rat_key = rat_key
        config_obj.session_magic = session_magic
        config_obj.aes_key = aes_hex
        if hasattr(config_obj, "config") and isinstance(config_obj.config, dict):
            config_obj.config["rat_key"] = rat_key
            config_obj.config["session_magic"] = session_magic
            config_obj.config["aes_key"] = aes_hex
    except Exception as exc:
        logger.debug("Could not mirror session secrets onto the live config: %s", exc)


__all__ = ["ensure_session_secrets", "rotate_session_secrets"]
