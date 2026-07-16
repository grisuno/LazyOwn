"""Symmetric primitives used by the framework.

XOR (legacy), AES-256-GCM, key generation, and file-dropping utilities
extracted from ``utils.py``.
"""

from __future__ import annotations

import os
import random
from typing import Union

ByteLike = Union[bytes, bytearray]

_AES_GCM_NONCE_LENGTH = 12
_AES_GCM_TAG_LENGTH = 16


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

    from Crypto.Cipher import AES as _AES

    k = hashlib.sha256(key).digest()
    nonce = os.urandom(_AES_GCM_NONCE_LENGTH)
    cipher = _AES.new(k, _AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + ct + tag, key


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

    from Crypto.Cipher import AES as _AES

    if len(data) < _AES_GCM_NONCE_LENGTH + _AES_GCM_TAG_LENGTH:
        raise ValueError("ciphertext too short to contain nonce and tag")
    nonce = data[:_AES_GCM_NONCE_LENGTH]
    tag = data[-_AES_GCM_TAG_LENGTH:]
    ct = data[_AES_GCM_NONCE_LENGTH:-_AES_GCM_TAG_LENGTH]
    k = hashlib.sha256(key).digest()
    cipher = _AES.new(k, _AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ct, tag)
    return plaintext


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
