"""Credential vault — AES-256-GCM encryption for sensitive config values.

Wraps ``core.crypto.AESencrypt``/``AESdecrypt`` to protect secrets stored
in ``payload.json`` (``c2_pass``, ``email_password``, ``api_key``, etc.)
and provides transparent load/save with encryption.

Design (SOLID):
- Single Responsibility: CredentialVault only handles encryption of secrets.
- Open/Closed: new sensitive keys added via SENSITIVE_KEYS without code change.
- Liskov: any AES-compatible encryptor can replace the default.
- Interface Segregation: seal(), unseal(), and seal_payload() are the surface.
- Dependency Inversion: depends on bytes-based encrypt/decrypt callables.

Usage:
    from core.credential_vault import seal_payload, unseal_payload

    payload = load_payload()
    secure = seal_payload(payload)
    save_payload(secure)

    loaded = load_payload()
    plain = unseal_payload(loaded)
"""

from __future__ import annotations

import logging
import os
from base64 import b64decode, b64encode
from pathlib import Path
from typing import Any

from core.crypto import AESdecrypt, AESencrypt

log = logging.getLogger("credential_vault")

SENSITIVE_KEYS: tuple[str, ...] = (
    "c2_pass",
    "email_password",
    "smtp_password",
    "api_key",
    "rat_key",
    "backdoor_password",
    "backdoor_username",
    "start_pass",
    "start_user_pass",
)

_DEFAULT_CREDS = {"CHANGE_ME", "", "deefbeef", "password", "admin", "changeme"}
_VAULT_MARKER = b"LAZYOWN_VAULT_V1:"

DANGEROUS_DEFAULTS: dict[str, str] = {
    "c2_pass": "CHANGE_ME — C2 password is still the default",
    "backdoor_password": "CHANGE_ME — backdoor password is still the default",
    "backdoor_username": "CHANGE_ME — backdoor username is still the default",
    "api_key": "CHANGE_ME — Groq API key is still the default",
    "start_user": "CHANGE_ME — starting username is still the default",
    "start_pass": "CHANGE_ME — starting password is still the default",
    "email_password": "CHANGE_ME — email/SMTP password is still the default",
}


def check_dangerous_defaults(payload: dict[str, Any]) -> list[str]:
    """Scan payload for unchanged default credential values.

    Returns a list of human-readable warning messages. An empty list means
    all sensitive keys have been changed from their factory defaults.
    """
    warnings: list[str] = []
    for key, message in DANGEROUS_DEFAULTS.items():
        value = str(payload.get(key, "")).strip()
        if not value:
            warnings.append(f"{key} is empty — configure it in payload.json")
        elif value.lower() in _DEFAULT_CREDS or "CHANGE_ME" in value:
            warnings.append(message)
    return warnings


def _get_aes_key(payload: dict[str, Any] | None = None) -> bytes:
    """Resolve the AES key from payload, disk, or generate fresh.

    Args:
        payload: Optional payload dict. Uses ``payload.json`` on disk if None.

    Returns:
        32-byte AES key.
    """
    from core.config import resolve_aes_key

    return resolve_aes_key(payload or {}, sessions_dir=Path("sessions"))


def seal_value(plaintext: str, key: bytes | None = None) -> str:
    """Encrypt a single credential value.

    Args:
        plaintext: Sensitive value to encrypt.
        key: AES key (auto-resolved if None).

    Returns:
        Base64-encoded sealed value with vault marker prefix.
    """
    if not plaintext:
        return ""
    k = key or _get_aes_key()
    ct, _ = AESencrypt(plaintext.encode("utf-8"), k)
    encoded = b64encode(ct).decode("ascii")
    marker = b64encode(_VAULT_MARKER).decode("ascii")
    return marker + encoded


def unseal_value(sealed: str, key: bytes | None = None) -> str:
    """Decrypt a sealed credential value.

    Returns the value unchanged if it is not a sealed vault value (plaintext
    backward compat). Returns empty string for empty input.

    Args:
        sealed: Possibly encrypted credential string.
        key: AES key (auto-resolved if None).

    Returns:
        Decrypted plaintext string.
    """
    if not sealed:
        return ""
    marker = b64encode(_VAULT_MARKER).decode("ascii")
    if not sealed.startswith(marker):
        return sealed
    k = key or _get_aes_key()
    encoded = sealed[len(marker) :]
    try:
        ct = b64decode(encoded)
        plaintext = AESdecrypt(ct, k)
        return plaintext.decode("utf-8")
    except Exception as exc:
        log.warning("Failed to unseal credential: %s", exc)
        return sealed


def seal_payload(payload: dict[str, Any], key: bytes | None = None) -> dict[str, Any]:
    """Return a copy of ``payload`` with all sensitive values encrypted.

    Non-sensitive keys and the key ``aes_key`` itself are left untouched.
    The returned dict is safe to write to ``payload.json``.

    Args:
        payload: Configuration dict to seal.
        key: AES key (auto-resolved if None).

    Returns:
        Shallow copy with sensitive fields encrypted.
    """
    k = key or _get_aes_key(payload)
    result = dict(payload)
    for sensitive in SENSITIVE_KEYS:
        if sensitive in result:
            val = str(result[sensitive])
            if val:
                result[sensitive] = seal_value(val, k)
    return result


def unseal_payload(payload: dict[str, Any], key: bytes | None = None) -> dict[str, Any]:
    """Return a copy of ``payload`` with all sealed values decrypted.

    Values that are not sealed are passed through unchanged.

    Args:
        payload: Configuration dict possibly containing sealed values.
        key: AES key (auto-resolved if None).

    Returns:
        Shallow copy with sensitive fields decrypted in-place.
    """
    k = key or _get_aes_key(payload)
    result = dict(payload)
    for sensitive in SENSITIVE_KEYS:
        if sensitive in result:
            val = str(result[sensitive])
            if val:
                result[sensitive] = unseal_value(val, k)
    return result


def rotate_aes_key(
    payload: dict[str, Any],
    current_key: bytes | None = None,
) -> tuple[dict[str, Any], bytes]:
    """Generate a new AES key, re-encrypt all sealed values under it.

    First decrypts with ``current_key``, then encrypts with a fresh key.
    The fresh key is written to ``sessions/key.aes`` with mode 0o600.

    Args:
        payload: Configuration dict (can be sealed or plain).
        current_key: Current AES key (auto-resolved if None).

    Returns:
        ``(new_payload, new_key_bytes)`` tuple. ``new_payload``
        is sealed with the fresh key and ready to save.
    """
    cur_key = current_key or _get_aes_key(payload)
    plain = unseal_payload(payload, cur_key)
    fresh_key = os.urandom(32)
    sessions_dir = Path("sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    key_path = sessions_dir / "key.aes"
    key_path.write_bytes(fresh_key)
    os.chmod(key_path, 0o600)
    new_payload = seal_payload(plain, fresh_key)
    return new_payload, fresh_key


def generate_secure_defaults() -> dict[str, str]:
    """Generate cryptographically random default values for sensitive keys.

    Returns a dict mapping each sensitive key to a 32-char hex random value.
    Use this to bootstrap a new ``payload.json`` with secure defaults.
    """
    import secrets

    defaults: dict[str, str] = {}
    for key in ("c2_pass", "backdoor_password", "backdoor_username", "rat_key"):
        defaults[key] = secrets.token_hex(16)
    for key in ("api_key", "email_password", "start_pass"):
        defaults[key] = secrets.token_hex(32)
    return defaults


__all__ = [
    "SENSITIVE_KEYS",
    "DANGEROUS_DEFAULTS",
    "check_dangerous_defaults",
    "seal_value",
    "unseal_value",
    "seal_payload",
    "unseal_payload",
    "rotate_aes_key",
    "generate_secure_defaults",
]
