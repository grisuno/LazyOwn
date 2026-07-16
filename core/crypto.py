"""Symmetric primitives used by the framework.

XOR (legacy), AES-CBC, key generation, and file-dropping utilities
extracted from ``utils.py``.
"""

from __future__ import annotations

import hashlib
import os
import random
from typing import Union

ByteLike = Union[bytes, bytearray]


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


def _get_aes_cipher(key: bytes):
    """Lazy-import AES from pycryptodome and return a CIPHER=key pair."""
    from Crypto.Cipher import AES as _AES
    from Crypto.Util.Padding import pad as _pad
    iv = 16 * b"\x00"
    k = hashlib.sha256(key).digest()
    cipher = _AES.new(k, _AES.MODE_CBC, iv)
    return cipher, _pad


def AESencrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Encrypt ``plaintext`` with AES-256-CBC using a SHA-256 derived key.

    Args:
        plaintext: Data to encrypt.
        key: Raw key material (SHA-256 hashed before use).

    Returns:
        ``(ciphertext, key)`` tuple.
    """
    cipher, pad = _get_aes_cipher(key)
    padded = pad(plaintext, 16)
    return cipher.encrypt(padded), key


def dropFile(key: bytes, ciphertext: bytes) -> None:
    """Write AES key and ciphertext to ``sessions/cipher.bin`` and ``sessions/key.bin``.

    Args:
        key: AES key bytes.
        ciphertext: Encrypted payload bytes.
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
    "dropFile",
]
