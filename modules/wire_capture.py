"""Durable byte-for-byte capture of a traffic exchange's raw output.

The traffic ledger keeps only a truncated head of each exchange inline, enough
to preview but not to reproduce: once an output runs past the inline cutoff the
tail is gone, so a finding bound to that digest can never be replayed exactly.
This store snapshots the full, unmodified output beside the evidence store the
moment it is produced, keyed by the same traffic digest, so the proof can be
reconstructed to the byte regardless of how far the ledger has rotated.

Capture is content-addressed and idempotent: the digest already derives from
command and output, so the same exchange maps to the same file and a re-capture
is a no-op. Writes are bounded and atomic, and any failure degrades to the
truncated inline copy rather than raising, because losing the raw wire must
never abort the execution that produced it. Nothing here imports the loop
runtime, keeping the module cycle-free.
"""

from __future__ import annotations

import os
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent
_DIRECTORY_MODE = 0o700
_SAFE_DIGEST = set("0123456789abcdefABCDEF")
_MAX_WIRE_BYTES = 4 * 1024 * 1024


def _sanitize_digest(digest: str) -> str:
    """Return a filesystem-safe hex digest, or empty when it is not hex.

    Rejecting anything but hex keeps a hostile or malformed digest from ever
    reaching a path join, honouring the project rule that filesystem input is
    whitelist-filtered first.

    Args:
        digest: The traffic digest to validate.

    Returns:
        The digest unchanged when it is non-empty hex, otherwise empty.
    """
    text = str(digest or "").strip()
    if not text or any(char not in _SAFE_DIGEST for char in text):
        return ""
    return text[:64]


class WireStore:
    """Persist and retrieve the full raw output of a traffic exchange.

    The store lives under ``sessions/wire/<task>/`` and holds one blob per
    captured traffic digest. It is append-mostly: a blob is written once and
    read many times, and is only ever removed by the evidence garbage collector
    that owns the same digests.
    """

    def __init__(self, task_id: str = "", base_dir: Path | None = None) -> None:
        """Bind the store to a task, creating its directory lazily on write.

        Args:
            task_id: Campaign/task identifier; blank uses a shared stream.
            base_dir: Optional root override for tests.
        """
        root = Path(base_dir) if base_dir is not None else _BASE_DIR / "sessions" / "wire"
        self._dir = root / (str(task_id) if task_id else "_shared")

    @property
    def directory(self) -> Path:
        """Return the directory this store writes blobs into."""
        return self._dir

    def _path_for(self, digest: str) -> Path | None:
        """Return the blob path for a digest, or None when it is unsafe."""
        safe = _sanitize_digest(digest)
        if not safe:
            return None
        candidate = (self._dir / f"{safe}.wire").resolve()
        allowed = self._dir.resolve()
        if not str(candidate).startswith(str(allowed) + os.sep):
            return None
        return candidate

    def has(self, digest: str) -> bool:
        """Return True when a raw blob for the digest already exists."""
        path = self._path_for(digest)
        return bool(path and path.exists())

    def capture(self, digest: str, raw: str, max_bytes: int = _MAX_WIRE_BYTES) -> str:
        """Snapshot the full raw output for a digest, idempotently.

        A digest already captured is left untouched so re-executing the same
        exchange never rewrites it. A missing or unsafe digest, or any I/O
        failure, returns an empty string rather than raising.

        Args:
            digest: The traffic digest keying this exchange.
            raw: The full, unmodified output to preserve.
            max_bytes: Upper bound on bytes written, guarding against an
                unbounded capture flooding the store.

        Returns:
            The captured digest, or an empty string on rejection or failure.
        """
        safe = _sanitize_digest(digest)
        if not safe:
            return ""
        path = self._path_for(safe)
        if path is None:
            return ""
        if path.exists():
            return safe
        body = str(raw or "")
        encoded = body.encode("utf-8", errors="replace")[: max(0, int(max_bytes))]
        try:
            self._dir.mkdir(parents=True, exist_ok=True)
            try:
                os.chmod(self._dir, _DIRECTORY_MODE)
            except OSError:
                pass
            tmp = path.with_suffix(".wire.tmp")
            tmp.write_bytes(encoded)
            os.replace(tmp, path)
            return safe
        except OSError:
            return ""

    def fetch(self, digest: str) -> str | None:
        """Return the full raw output for a digest, or None when absent.

        Args:
            digest: The traffic digest to retrieve.

        Returns:
            The decoded raw output, or None when no blob exists or it is
            unreadable.
        """
        path = self._path_for(digest)
        if path is None or not path.exists():
            return None
        try:
            return path.read_bytes().decode("utf-8", errors="replace")
        except OSError:
            return None


__all__ = ["WireStore"]
