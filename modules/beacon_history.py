"""Persistent beacon command/result history storage.

Owns the on-disk JSONL history for beacon results so the C2, the Flask GUI
and GUI2 all replay the same ordered timeline. Kept module-scoped (no Flask
dependency) so it is unit-testable without booting the C2 application.

Contract:
    - ``BeaconHistoryConfig`` holds the storage root and the history suffix.
    - ``append_record`` appends one record (atomic, safe for concurrent implant polls).
    - ``read_records`` returns the ordered records for a beacon.
    - ``records_path`` resolves the history file for a sanitised beacon id.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

DEFAULT_HISTORY_SUFFIX: str = ".records.jsonl"


@dataclass(frozen=True, slots=True)
class BeaconHistoryConfig:
    """Centralised configuration for beacon history storage.

    Attributes:
        base_dir: Root directory that contains the ``sessions`` folder.
        history_suffix: File suffix appended to a beacon id for its history.
    """

    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    history_suffix: str = DEFAULT_HISTORY_SUFFIX

    def sessions_dir(self) -> Path:
        """Return the resolved sessions directory under the base dir."""
        return self.base_dir / "sessions"

    def records_path(self, client_id: str) -> Path:
        """Resolve the history file path for a sanitised beacon client id.

        The resolved path is verified to stay inside the sessions directory
        so a bypassed or weakened sanitisation can never write outside the
        storage root.

        Args:
            client_id: Raw beacon id; it is sanitised against path traversal.

        Returns:
            A :class:`pathlib.Path` inside the sessions directory.

        Raises:
            ValueError: When the resulting path would escape the sessions dir.
        """
        safe_id = "".join(c for c in str(client_id) if c.isalnum() or c in "-_")
        candidate = self.sessions_dir() / f"{safe_id}{self.history_suffix}"
        sessions_root = self.sessions_dir().resolve()
        if sessions_root not in candidate.resolve().parents:
            raise ValueError("beacon history path escapes the sessions directory")
        return candidate


_DEFAULT_CONFIG = BeaconHistoryConfig()


def sanitize_client_id(client_id: str) -> str:
    """Sanitise a beacon id to only URL/file-safe characters.

    Args:
        client_id: Raw beacon id.

    Returns:
        The sanitised id containing only alphanumerics, dashes and underscores.
    """
    return "".join(c for c in str(client_id) if c.isalnum() or c in "-_")


def append_record(record: dict[str, Any], config: BeaconHistoryConfig = _DEFAULT_CONFIG) -> bool:
    """Append one beacon result record to the persistent JSONL history.

    The write is atomic (append to a temp file then replace) so concurrent
    beacon polls never interleave partial lines.

    Args:
        record: The normalised beacon record dict.
        config: Storage configuration (defaults to the standard sessions layout).

    Returns:
        True when the append succeeded, False otherwise.
    """
    client_id = str(record.get("client_id", ""))
    if not client_id:
        return False
    path = config.records_path(client_id)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=False)
        tmp = Path(str(path) + ".tmp")
        if path.exists():
            tmp.write_bytes(path.read_bytes())
        with tmp.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        tmp.replace(path)
        return True
    except Exception as exc:
        _log.warning("beacon history append failed: %s", exc)
        if path.exists():
            path.with_suffix(".tmp").unlink(missing_ok=True)
        return False


def read_records(client_id: str, config: BeaconHistoryConfig = _DEFAULT_CONFIG) -> list[dict[str, Any]]:
    """Read the ordered JSONL history for a beacon client id (oldest first).

    Args:
        client_id: The beacon id whose history is requested.
        config: Storage configuration.

    Returns:
        A list of record dicts in chronological order.
    """
    path = config.records_path(client_id)
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                _log.warning("skipping malformed beacon history line")
                continue
    except Exception as exc:
        _log.warning("beacon history read failed: %s", exc)
    return records


def records_path(client_id: str, config: BeaconHistoryConfig = _DEFAULT_CONFIG) -> Path:
    """Resolve the history file path for a beacon client id.

    Args:
        client_id: The beacon id whose history path is requested.
        config: Storage configuration.

    Returns:
        The resolved history file path.
    """
    return config.records_path(client_id)


__all__ = [
    "BeaconHistoryConfig",
    "append_record",
    "read_records",
    "records_path",
    "sanitize_client_id",
]
