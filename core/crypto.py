"""Symmetric primitives used by the framework.

XOR (legacy), AES-256-GCM, key generation, and file-dropping utilities
extracted from ``utils.py``.
"""

from __future__ import annotations

import base64
import logging
import os
import random
import secrets
import stat
from pathlib import Path
from typing import Union

ByteLike = Union[bytes, bytearray]

_log = logging.getLogger(__name__)

_AES_GCM_NONCE_LENGTH = 12
_AES_GCM_TAG_LENGTH = 16

_FERNET_KEY_LENGTH = 32
_PBKDF2_ITERATIONS = 100_000

MASTER_PASSWORD_ENV = "LAZYOWN_MASTER_PASSWORD"
STATE_SECRET_FILE = ".state_secret"
_STATE_SECRET_BYTES = 32
_RESTRICTED_FILE_MODE = 0o600
_KEYRING_SERVICE = "lazyown-state"
_KEYRING_ACCOUNT = "master"
_WARNED: set[str] = set()


def _warn_once(tag: str, message: str) -> None:
    """Emit ``message`` at WARNING level only the first time for ``tag``."""
    if tag in _WARNED:
        return
    _WARNED.add(tag)
    _log.warning(message)


def machine_secret(sessions_dir: str | os.PathLike[str], create: bool = True) -> str | None:
    """Return a device-bound random at-rest secret.

    The secret is a random hex string persisted in
    ``<sessions_dir>/.state_secret`` with mode ``0o600``. It is NOT derived
    from any predictable value, so disk access alone no longer yields the key
    from public data such as the operator username. A file with group- or
    world-writable permissions is rejected.

    Args:
        sessions_dir: Directory holding the per-engagement secret.
        create: Create the secret on first use when ``True``.

    Returns:
        The hex secret, or ``None`` when it cannot be created or read safely.
    """
    secret_path = Path(sessions_dir) / STATE_SECRET_FILE
    try:
        if secret_path.exists():
            mode = stat.S_IMODE(secret_path.stat().st_mode)
            if mode & 0o022:
                _log.warning("crypto: %s has unsafe mode; refusing device key", secret_path)
                return None
            value = secret_path.read_text(encoding="utf-8").strip()
            return value if len(value) >= _STATE_SECRET_BYTES else None
        if not create:
            return None
        Path(sessions_dir).mkdir(parents=True, exist_ok=True)
        fd = os.open(secret_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, _RESTRICTED_FILE_MODE)
        try:
            os.write(fd, secrets.token_hex(_STATE_SECRET_BYTES).encode())
        finally:
            os.close(fd)
        os.chmod(secret_path, _RESTRICTED_FILE_MODE)
        return secret_path.read_text(encoding="utf-8").strip()
    except Exception as exc:  # noqa: BLE001 - any failure means no device key
        _log.warning("crypto: device key unavailable: %s", exc)
        return None


def _keyring_secret(create: bool = True) -> str | None:
    """Fetch (or create) a random master secret from the OS keyring.

    Returns ``None`` when the ``keyring`` package is not installed or the
    platform backend is unavailable, so the caller degrades to the device
    secret. A single fixed account is used so every component resolves the
    same secret.

    Args:
        create: Store a freshly generated secret when none exists.

    Returns:
        The keyring-held secret, or ``None`` when unavailable.
    """
    try:
        import keyring
    except Exception:
        return None
    try:
        existing = keyring.get_password(_KEYRING_SERVICE, _KEYRING_ACCOUNT)
        if existing:
            return existing
        if not create:
            return None
        new_secret = secrets.token_hex(_STATE_SECRET_BYTES)
        keyring.set_password(_KEYRING_SERVICE, _KEYRING_ACCOUNT, new_secret)
        return new_secret
    except Exception as exc:  # noqa: BLE001 - any backend error means no keyring key
        _log.warning("crypto: keyring unavailable: %s", exc)
        return None


def resolve_master_password(
    sessions_dir: str | os.PathLike[str],
    *,
    allow_keyring: bool = True,
    allow_device: bool = True,
    create: bool = True,
) -> str | None:
    """Resolve the at-rest master password with NO predictable derivation.

    Resolution order:
        1. ``LAZYOWN_MASTER_PASSWORD`` environment variable (portable, strongest).
        2. OS keyring random secret (when ``keyring`` is installed).
        3. Device-bound random secret in ``<sessions_dir>/.state_secret``.
        4. ``None`` - encryption is skipped and the caller is warned.

    A key is NEVER derived from a public value such as the operator username.
    The device-secret and no-key paths emit a one-time explicit warning so a
    weaker-than-env posture is never silent.

    Args:
        sessions_dir: Directory for the device-bound secret.
        allow_keyring: Consult the OS keyring when ``True``.
        allow_device: Fall back to the device-bound secret when ``True``.
        create: Allow creating a keyring/device secret when none exists.

    Returns:
        The resolved password, or ``None`` when encryption must be skipped.
    """
    env = os.environ.get(MASTER_PASSWORD_ENV)
    if env:
        return env
    if allow_keyring:
        secret = _keyring_secret(create=create)
        if secret:
            return secret
    if allow_device:
        secret = machine_secret(sessions_dir, create=create)
        if secret:
            _warn_once(
                "device",
                f"crypto: {MASTER_PASSWORD_ENV} unset and no OS keyring; using the "
                f"device-bound secret {sessions_dir}/{STATE_SECRET_FILE} (local-disk "
                f"security only). Set {MASTER_PASSWORD_ENV} for portable at-rest encryption.",
            )
            return secret
    _warn_once(
        "none",
        f"crypto: no {MASTER_PASSWORD_ENV}, OS keyring, or device secret available; "
        f"sensitive session data will NOT be encrypted at rest. Set {MASTER_PASSWORD_ENV} "
        "to enable encryption.",
    )
    return None


def legacy_master_password(operator: str | None) -> str | None:
    """Return the DEPRECATED ``lazyown:<operator>`` key material.

    This predictable scheme (a key derived from the public operator username)
    is retained for READ-ONLY backward compatibility: it decrypts files written
    before the scheme was removed, after which they re-encrypt under the current
    key. It must never be used to encrypt new data.

    Args:
        operator: The authenticated operator username, if any.

    Returns:
        ``"lazyown:<operator>"`` when an operator is known, else ``None``.
    """
    if operator:
        return f"lazyown:{operator}"
    return None


def generate_salt(length: int = 16) -> bytes:
    """Generate a cryptographically random salt.

    Args:
        length: Salt length in bytes.

    Returns:
        Random bytes suitable for PBKDF2 key derivation.
    """
    return secrets.token_bytes(length)


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password using PBKDF2HMAC.

    Uses SHA-256 with 100000 iterations over ``password`` + ``salt`` and
    returns a URL-safe Base64 key accepted by ``cryptography.Fernet``.

    Args:
        password: The user-provided password.
        salt: Salt bytes (see ``generate_salt``). Callers persisting
            encrypted data must store the salt alongside it.

    Returns:
        Base64-encoded Fernet key bytes.

    Raises:
        ValueError: if ``password`` is empty.
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    if not password:
        raise ValueError("derive_key requires a non-empty password")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_FERNET_KEY_LENGTH,
        salt=salt,
        iterations=_PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def xor_encrypt_decrypt(data: ByteLike, key: str) -> bytearray:
    """Return ``bytearray`` produced by XOR-ing each byte of ``data`` with ``key``.

    XOR is symmetric, so the same call encrypts and decrypts. The key is
    cycled byte-by-byte over the data. ``key`` must be a non-empty string.

    Raises:
        ValueError: if ``key`` is empty.
    """
    if not key:
        raise ValueError("xor_encrypt_decrypt requires a non-empty key")
    key_bytes = key.encode("utf-8")
    key_length = len(key_bytes)
    return bytearray(data[i] ^ key_bytes[i % key_length] for i in range(len(data)))


def generate_xor_key(length: int) -> str:
    """Generate a random XOR key of the given length as a hex string.

    Args:
        length: Length of the XOR key in bytes.

    Returns:
        Hex-encoded key string.
    """
    if length <= 0:
        raise ValueError("The length must be longer than 0")
    key_bytes = [random.randint(0, 255) for _ in range(length)]
    return "".join(f"{byte:02X}" for byte in key_bytes)


def AESencrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Encrypt ``plaintext`` with AES-256-GCM using a random nonce.

    Output format is ``nonce (12 bytes) || ciphertext || tag (16 bytes)``
    so that ``AESdecrypt`` can extract all three components.

    Args:
        plaintext: Data to encrypt.
        key: Raw key material (SHA-256 hashed before use).

    Returns:
        ``(ciphertext, key)`` tuple where ``ciphertext`` includes the
        nonce and authentication tag prepended/appended.
    """
    import hashlib

    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    k = hashlib.sha256(key).digest()
    nonce = os.urandom(_AES_GCM_NONCE_LENGTH)
    ct_and_tag = AESGCM(k).encrypt(nonce, plaintext, None)
    return nonce + ct_and_tag, key


def AESdecrypt(data: bytes, key: bytes) -> bytes:
    """Decrypt data produced by ``AESencrypt``.

    Expects ``nonce (12 bytes) || ciphertext || tag (16 bytes)``.

    Args:
        data: Encrypted payload with embedded nonce and tag.
        key: The same key used during encryption.

    Returns:
        Decrypted plaintext.

    Raises:
        ValueError: If the authentication tag does not verify (data
            tampered or wrong key).
    """
    import hashlib

    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    if len(data) < _AES_GCM_NONCE_LENGTH + _AES_GCM_TAG_LENGTH:
        raise ValueError("ciphertext too short to contain nonce and tag")
    nonce = data[:_AES_GCM_NONCE_LENGTH]
    ct_and_tag = data[_AES_GCM_NONCE_LENGTH:]
    k = hashlib.sha256(key).digest()
    try:
        return AESGCM(k).decrypt(nonce, ct_and_tag, None)
    except InvalidTag as exc:
        raise ValueError("authentication failed: data tampered or wrong key") from exc


def dropFile(key: bytes, ciphertext: bytes) -> None:
    """Write AES key and ciphertext to ``sessions/cipher.bin`` and ``sessions/key.bin``.

    Args:
        key: AES key bytes.
        ciphertext: Encrypted payload bytes (includes nonce + tag).
    """
    os.makedirs("sessions", exist_ok=True)
    with open("sessions/cipher.bin", "wb") as fc:
        fc.write(ciphertext)
    with open("sessions/key.bin", "wb") as fk:
        fk.write(key)


__all__ = [
    "xor_encrypt_decrypt",
    "generate_xor_key",
    "AESencrypt",
    "AESdecrypt",
    "dropFile",
]
