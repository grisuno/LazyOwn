"""Channel secret sealing for loop credential stores.

Extracted from ``modules/lazy_loop``: AES-256-GCM sealing of SMTP/SMS
channel passwords with the ``LAZYOWN_SECRET_KEY`` material, plaintext
fallback (with a one-time warning) when no key is configured. The
``enc:v1:`` prefix and the AES scheme are fixed by existing stores —
do not confuse this with ``core.secrets.seal_secret`` (Fernet, vault).
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CHANNEL_SECRET_PREFIX = "enc:v1:"
_CHANNEL_SECRET_WARNED = False


def _channel_encryption_key() -> bytes | None:
    """Return the AES key for channel secrets, or None when unconfigured."""
    try:
        from core.hardening import require_encryption_key
    except ImportError:
        return None
    try:
        secret = require_encryption_key(
            env_key="LAZYOWN_SECRET_KEY",
            secret_file=BASE_DIR / "sessions" / ".secret_key",
        )
    except Exception:
        return None
    return hashlib.sha256(secret.encode("utf-8")).digest()


def _encrypt_channel_secret(plaintext: str) -> str:
    """Encrypt a channel password for storage; plaintext fallback when no key.

    When ``LAZYOWN_SECRET_KEY`` (or ``sessions/.secret_key``) is set the
    value is AES-256-GCM sealed and prefixed ``enc:v1:``. Otherwise the
    value is stored as-is with 0600 file perms and a one-time warning;
    callers must still restrict the store file.
    """
    global _CHANNEL_SECRET_WARNED
    text = str(plaintext or "")
    if not text:
        return ""
    if text.startswith(CHANNEL_SECRET_PREFIX):
        return text
    key = _channel_encryption_key()
    if key is None:
        if not _CHANNEL_SECRET_WARNED:
            _CHANNEL_SECRET_WARNED = True
            try:
                logging.getLogger("modules.lazy_loop").warning(
                    "channel password stored without encryption; set LAZYOWN_SECRET_KEY"
                )
            except Exception:
                pass
        return text
    try:
        import base64 as _b64

        from core.crypto import AESencrypt

        blob, _ = AESencrypt(text.encode("utf-8"), key)
        return CHANNEL_SECRET_PREFIX + _b64.b64encode(blob).decode("ascii")
    except Exception:
        return text


def _decrypt_channel_secret(stored: str) -> str:
    """Reveal a channel password stored by :func:`_encrypt_channel_secret`."""
    text = str(stored or "")
    if not text.startswith(CHANNEL_SECRET_PREFIX):
        return text
    key = _channel_encryption_key()
    if key is None:
        return ""
    try:
        import base64 as _b64

        from core.crypto import AESdecrypt

        return AESdecrypt(_b64.b64decode(text[len(CHANNEL_SECRET_PREFIX) :]), key).decode("utf-8")
    except Exception:
        return ""


__all__ = [
    "CHANNEL_SECRET_PREFIX",
    "_channel_encryption_key",
    "_encrypt_channel_secret",
    "_decrypt_channel_secret",
]
