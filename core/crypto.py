"""Symmetric primitives used by the framework.

Currently only XOR — used by the Go beacon stub and a few payload-obfuscation
sites. Behavior is preserved bit-for-bit from the legacy
``utils.xor_encrypt_decrypt`` so existing artefacts remain decodable.
"""

from __future__ import annotations

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


__all__ = ["xor_encrypt_decrypt"]
