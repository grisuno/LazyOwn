"""Beacon queue, history and recon-state storage for the C2 server.

Single source of truth for the on-disk beacon state shared by the C2 routes,
the CLI and the autonomous loop. Every resolved path is confined under the
configured base directory so a hostile client id can never escape the C2 root.

Contracts:
    - ``BeaconStore.queue_path`` resolves ``cmd_<safe_id>.json`` under the base.
    - ``BeaconStore.enqueue`` / ``pop_next`` implement the FIFO command queue.
    - ``BeaconStore.append_record`` / ``read_records`` delegate to
      :mod:`modules.beacon_history`, the canonical result-history store.
    - ``BeaconStore.load_recon_state`` / ``save_recon_state`` own the
      per-beacon malleable recon markers.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from modules.beacon_history import BeaconHistoryConfig
from modules.beacon_history import append_record as _append_history_record
from modules.beacon_history import read_records as _read_history_records
from modules.security_sanitizers import sanitize_client_id

_log = logging.getLogger(__name__)

QUEUE_FILENAME_PREFIX = "cmd_"
QUEUE_FILENAME_SUFFIX = ".json"
RECON_STATE_FILENAME = "recon_state.json"
RECON_STATE_PARENT = "sessions"
RECON_STATE_DIRNAME = "c2"
ATOMIC_TEMP_SUFFIX = ".tmp"


class BeaconPathError(ValueError):
    """Raised when a beacon path would escape the configured base directory."""


@dataclass(frozen=True, slots=True)
class BeaconStore:
    """Path-safe storage contract for one C2 base directory.

    Attributes:
        base_dir: Directory that holds ``cmd_<id>.json`` queue files and the
            per-beacon recon-state directories.
        history_config: Configuration for the result history store. Defaults
            to the repository sessions layout used by ``modules.beacon_history``.
    """

    base_dir: Path
    history_config: BeaconHistoryConfig = field(default_factory=BeaconHistoryConfig)

    def __post_init__(self) -> None:
        object.__setattr__(self, "base_dir", Path(self.base_dir))

    @property
    def _root(self) -> Path:
        return self.base_dir.resolve()

    def _safe_id(self, client_id: object) -> str:
        safe_id = sanitize_client_id(client_id)
        if not safe_id:
            raise BeaconPathError(f"Invalid client_id after sanitization: {client_id}")
        return safe_id

    def _confined(self, candidate: Path) -> Path:
        resolved = candidate.resolve()
        root = self._root
        if resolved != root and root not in resolved.parents:
            raise BeaconPathError(f"Beacon path escapes the base directory: {resolved}")
        return resolved

    def queue_path(self, client_id: object) -> Path:
        """Resolve the command queue file for one beacon.

        Args:
            client_id: Raw beacon id; sanitized before path resolution.

        Returns:
            The confined ``cmd_<safe_id>.json`` path.

        Raises:
            BeaconPathError: When the sanitized id is empty or the resolved
                path escapes the base directory.
        """
        safe_id = self._safe_id(client_id)
        candidate = self.base_dir / f"{QUEUE_FILENAME_PREFIX}{safe_id}{QUEUE_FILENAME_SUFFIX}"
        return self._confined(candidate)

    def load_queue(self, client_id: object) -> list[str]:
        """Read the pending command queue for one beacon.

        Args:
            client_id: Raw beacon id.

        Returns:
            The queued commands in FIFO order; an empty list when the queue
            is missing, unreadable or not a JSON array.
        """
        try:
            path = self.queue_path(client_id)
        except BeaconPathError as exc:
            _log.debug("queue path rejected: %s", exc)
            return []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return []
        except (OSError, json.JSONDecodeError) as exc:
            _log.debug("queue read failed for %s: %s", path, exc)
            return []
        if not isinstance(raw, list):
            _log.debug("queue file %s is not a JSON array", path)
            return []
        return [str(item) for item in raw]

    def save_queue(self, client_id: object, commands: Iterable[object]) -> bool:
        """Persist the command queue atomically.

        Args:
            client_id: Raw beacon id.
            commands: Commands to write, in delivery order.

        Returns:
            True when the queue file was replaced, False on I/O or path errors.
        """
        try:
            path = self.queue_path(client_id)
            self._write_json_atomic(path, [str(command) for command in commands])
            return True
        except (OSError, BeaconPathError, TypeError, ValueError) as exc:
            _log.warning("queue save failed: %s", exc)
            return False

    def enqueue(self, client_id: object, command: object) -> bool:
        """Append one command to the beacon queue.

        Args:
            client_id: Raw beacon id.
            command: Command payload the implant will poll.

        Returns:
            True when the queue was written, False otherwise.
        """
        queue = self.load_queue(client_id)
        queue.append(str(command))
        return self.save_queue(client_id, queue)

    def pop_next(self, client_id: object) -> str | None:
        """Pop the oldest queued command for one beacon.

        Args:
            client_id: Raw beacon id.

        Returns:
            The next command, or None when the queue is empty or the trimmed
            queue could not be persisted.
        """
        queue = self.load_queue(client_id)
        if not queue:
            return None
        command = queue.pop(0)
        if not self.save_queue(client_id, queue):
            return None
        return command

    def recon_state_dir(self, client_id: object) -> Path:
        """Resolve the per-beacon malleable recon-state directory.

        Args:
            client_id: Raw beacon id.

        Returns:
            The confined ``<base>/sessions/<safe_id>/c2`` directory.

        Raises:
            BeaconPathError: When the sanitized id is empty or the resolved
                path escapes the base directory.
        """
        safe_id = self._safe_id(client_id)
        candidate = self.base_dir / RECON_STATE_PARENT / safe_id / RECON_STATE_DIRNAME
        return self._confined(candidate)

    def recon_state_path(self, client_id: object) -> Path:
        """Resolve the recon marker file for one beacon.

        Args:
            client_id: Raw beacon id.

        Returns:
            The confined ``recon_state.json`` path.

        Raises:
            BeaconPathError: When the sanitized id is empty or the resolved
                path escapes the base directory.
        """
        return self._confined(self.recon_state_dir(client_id) / RECON_STATE_FILENAME)

    def load_recon_state(self, client_id: object) -> dict[str, Any]:
        """Read the malleable recon markers for one beacon.

        Args:
            client_id: Raw beacon id.

        Returns:
            The stored marker dict, or an empty dict when unavailable.
        """
        try:
            path = self.recon_state_path(client_id)
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {}
        except (OSError, json.JSONDecodeError, BeaconPathError) as exc:
            _log.debug("recon state load failed: %s", exc)
            return {}
        return raw if isinstance(raw, dict) else {}

    def save_recon_state(self, client_id: object, state: dict[str, Any]) -> bool:
        """Persist the malleable recon markers for one beacon.

        Args:
            client_id: Raw beacon id.
            state: Marker dict such as ``{"discover_queued": True}``.

        Returns:
            True when the marker file was replaced, False on errors.
        """
        try:
            path = self.recon_state_path(client_id)
            self._write_json_atomic(path, state)
            return True
        except (OSError, BeaconPathError, TypeError, ValueError) as exc:
            _log.debug("recon state save failed: %s", exc)
            return False

    def history_path(self, client_id: object) -> Path:
        """Resolve the result-history file for one beacon.

        Args:
            client_id: Raw beacon id.

        Returns:
            The history path owned by :class:`modules.beacon_history`.
        """
        safe_id = self._safe_id(client_id)
        return self.history_config.records_path(safe_id)

    def append_record(self, record: dict[str, Any]) -> bool:
        """Append one result record to the beacon history.

        Args:
            record: Normalized beacon record; ``client_id`` is required.

        Returns:
            True when the append succeeded.
        """
        try:
            return _append_history_record(record, self.history_config)
        except Exception as exc:
            _log.warning("history append failed: %s", exc)
            return False

    def read_records(self, client_id: object) -> list[dict[str, Any]]:
        """Read the ordered result history for one beacon.

        Args:
            client_id: Raw beacon id.

        Returns:
            Records oldest first; an empty list when unavailable.
        """
        try:
            safe_id = self._safe_id(client_id)
            return _read_history_records(safe_id, self.history_config)
        except Exception as exc:
            _log.debug("history read failed: %s", exc)
            return []

    @staticmethod
    def _write_json_atomic(path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=ATOMIC_TEMP_SUFFIX,
            delete=False,
        )
        temp_path = Path(handle.name)
        try:
            with handle:
                json.dump(payload, handle)
            os.replace(temp_path, path)
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise
