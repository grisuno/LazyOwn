"""Content-addressed evidence vault independent of disposable traffic.

Ports the LAZY ``evidence`` subsystem: finding evidence is hashed
with SHA-256, written atomically via a staging directory, verified on
read, and garbage-collected when unreferenced past a grace period.
"""

from __future__ import annotations

import binascii
import hashlib
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class EvidenceConfig:
    """Centralized constants for vault behavior."""

    blob_prefix_len: int = 2
    staging_dirname: str = ".staging"
    blobs_dirname: str = "blobs"
    gc_grace_sec: float = 86400.0


CONFIG = EvidenceConfig()

BLOB_PREFIX_LEN = CONFIG.blob_prefix_len
STAGING_DIRNAME = CONFIG.staging_dirname
BLOBS_DIRNAME = CONFIG.blobs_dirname
GC_GRACE_SEC = CONFIG.gc_grace_sec


def hash_bytes(data: bytes) -> str:
    """Return the lowercase hex SHA-256 of data."""
    return hashlib.sha256(bytes(data or b"")).hexdigest()


def _validate_hash(value: str) -> str:
    """Validate a SHA-256 hex digest and return it normalized."""
    normalized = str(value or "").lower()
    if len(normalized) != 64:
        raise ValueError("Invalid evidence hash.")
    try:
        binascii.unhexlify(normalized)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("Invalid evidence hash.") from exc
    return normalized


class EvidenceStore:
    """Durable content-addressed blob store for finding evidence."""

    def __init__(self, base_dir: str | Path) -> None:
        """Create vault directories."""
        self.base_dir = Path(base_dir)
        self.blobs_dir = self.base_dir / BLOBS_DIRNAME
        self.staging_dir = self.base_dir / STAGING_DIRNAME
        self.blobs_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

    def blob_path(self, content_hash: str) -> Path:
        """Resolve the canonical path for a validated hash."""
        digest = _validate_hash(content_hash)
        return self.blobs_dir / digest[:BLOB_PREFIX_LEN] / f"{digest}.bin"

    def put(self, data: bytes) -> str:
        """Atomically store bytes and return their SHA-256 hash."""
        raw = bytes(data or b"")
        digest = hash_bytes(raw)
        target = self.blob_path(digest)
        if target.exists() and target.stat().st_size == len(raw):
            return digest
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(self.staging_dir), prefix="body-")
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(raw)
            os.replace(tmp_name, target)
        finally:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        return digest

    def get(self, content_hash: str) -> bytes:
        """Read and verify blob bytes for a hash."""
        target = self.blob_path(content_hash)
        data = target.read_bytes()
        if hash_bytes(data) != target.stem:
            raise ValueError("Evidence integrity check failed.")
        return data

    def exists(self, content_hash: str) -> bool:
        """Return True when the blob exists on disk."""
        try:
            return self.blob_path(content_hash).exists()
        except ValueError:
            return False

    def garbage_collect(self, referenced: set[str]) -> int:
        """Remove unreferenced blobs older than the grace period."""
        valid = {_validate_hash(h) for h in (referenced or set())}
        now = time.time()
        removed = 0
        for shard in self.blobs_dir.iterdir():
            if not shard.is_dir():
                continue
            for blob in shard.glob("*.bin"):
                if blob.stem in valid:
                    continue
                try:
                    if now - blob.stat().st_mtime < GC_GRACE_SEC:
                        continue
                    blob.unlink()
                    removed += 1
                except OSError:
                    continue
        return removed
