"""Durable, content-addressed evidence store independent of disposable traffic.

A finding binds its proof by traffic digest, but the traffic ledger is a
rotating, tail-bounded stream: once enough exchanges accrue, the row a finding
points at scrolls out of the readable window and the proof is gone while the
finding still claims it. This store snapshots the exchange behind a finding
into its own space the moment it is bound, so the proof outlives any traffic
rotation.

Each snapshot is keyed by its traffic digest, which is itself derived from the
command and output, so the store is content-addressed: the same exchange maps
to the same file and a re-bind is idempotent. Garbage collection reaps only
snapshots that are both unreferenced by any live finding and older than a grace
period, keeping a full day's grace so a failed or racing write is never swept
mid-flight. Nothing here imports the loop runtime, keeping the module cycle-free
and testable in isolation.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

_BASE_DIR = Path(__file__).resolve().parent.parent
_DEFAULT_GRACE_SECONDS = 86400.0
_SAFE_DIGEST = set("0123456789abcdefABCDEF")


def _sanitize_digest(digest: str) -> str:
    """Return a filesystem-safe digest, or empty when it is not hex.

    The traffic digest is a hex string by construction; rejecting anything
    else keeps a hostile or malformed digest from ever reaching a path join,
    honouring the project rule that input touching the filesystem is filtered
    to a whitelist first.

    Args:
        digest: The traffic digest to validate.

    Returns:
        The digest unchanged when it is non-empty hex, otherwise an empty
        string.
    """
    text = str(digest or "").strip().lower()
    if not text or any(char not in _SAFE_DIGEST for char in text):
        return ""
    return text[:64]


class EvidenceStore:
    """Persist and retrieve finding evidence beyond the traffic window.

    The store lives under ``sessions/evidence/<task>/`` and holds one JSON
    snapshot per bound traffic digest. It is append-mostly: snapshots are
    written once and read many times, with an explicit grace-aware GC the only
    way a file is removed.
    """

    def __init__(self, task_id: str = "", base_dir: Path | None = None) -> None:
        """Bind the store to a task, creating its directory lazily on write.

        Args:
            task_id: Campaign/task identifier; blank uses a shared stream.
            base_dir: Optional root override for tests.
        """
        root = Path(base_dir) if base_dir is not None else _BASE_DIR / "sessions" / "evidence"
        self._dir = root / (str(task_id) if task_id else "_shared")

    @property
    def directory(self) -> Path:
        """Return the directory this store writes snapshots into."""
        return self._dir

    def _path_for(self, digest: str) -> Path | None:
        """Return the snapshot path for a digest, or None when it is unsafe."""
        safe = _sanitize_digest(digest)
        if not safe:
            return None
        candidate = (self._dir / f"{safe}.json").resolve()
        allowed = self._dir.resolve()
        if not str(candidate).startswith(str(allowed) + os.sep):
            return None
        return candidate

    def has(self, digest: str) -> bool:
        """Return True when a snapshot for the digest already exists."""
        path = self._path_for(digest)
        return bool(path and path.exists())

    def preserve(self, record: dict[str, Any]) -> str:
        """Snapshot one traffic exchange durably and return its digest.

        The write is idempotent: a digest already preserved is left untouched
        so re-binding the same evidence never rewrites it. A missing or unsafe
        digest, or any I/O failure, returns an empty string rather than raising,
        because losing a snapshot must never abort the bind that triggered it.

        Args:
            record: A traffic record carrying at least ``digest``; ``command``,
                ``output``, ``preview``, ``bytes`` and ``meta`` are preserved
                when present.

        Returns:
            The preserved digest, or an empty string on rejection or failure.
        """
        digest = _sanitize_digest(str((record or {}).get("digest", "")))
        if not digest:
            return ""
        path = self._path_for(digest)
        if path is None:
            return ""
        if path.exists():
            return digest
        snapshot = {
            "digest": digest,
            "command": str(record.get("command", ""))[:2000],
            "output": str(record.get("output", "")),
            "preview": str(record.get("preview", ""))[:1000],
            "bytes": int(record.get("bytes", 0) or 0),
            "template": str(record.get("template", ""))[:200],
            "meta": dict(record.get("meta", {}) or {}),
            "preserved_at": time.time(),
        }
        try:
            from core.atomic_store import write_text_atomic

            write_text_atomic(path, json.dumps(snapshot, ensure_ascii=False, sort_keys=True))
            return digest
        except OSError:
            return ""

    def fetch(self, digest: str) -> dict[str, Any] | None:
        """Return the durable snapshot for a digest, or None when absent.

        Args:
            digest: The traffic digest to retrieve.

        Returns:
            The snapshot document, or None when no snapshot exists or the file
            is unreadable.
        """
        path = self._path_for(digest)
        if path is None or not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    def gc(self, referenced: set[str], grace_seconds: float = _DEFAULT_GRACE_SECONDS) -> int:
        """Reap snapshots neither referenced nor within the grace period.

        A snapshot is removed only when its digest is absent from
        ``referenced`` and its file is older than ``grace_seconds``, so a
        just-written snapshot that a finding has not yet bound is never swept.

        Args:
            referenced: Digests still claimed by a live finding.
            grace_seconds: Minimum snapshot age before it is eligible to reap.

        Returns:
            The number of snapshots removed.
        """
        if not self._dir.exists():
            return 0
        keep = {_sanitize_digest(d) for d in (referenced or set())}
        cutoff = time.time() - max(0.0, float(grace_seconds))
        removed = 0
        for path in self._dir.glob("*.json"):
            digest = path.stem
            if digest in keep:
                continue
            try:
                if path.stat().st_mtime >= cutoff:
                    continue
                path.unlink()
                removed += 1
            except OSError:
                continue
        return removed


__all__ = ["EvidenceStore"]
