"""Durable chain checkpoints for pause, resume and audit.

A checkpoint records everything one chain run needs to continue after
an interruption: chains/ run id, target, tokens, variables, captured
keys, executed steps and the next index. Files live under
``sessions/chains/`` as ``<run_id>.json`` so the ``apt_chain resume``
command can pick them up. Storage is additive only: writing never
mutates an existing run id, and loading never executes anything.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

_SESSIONS_DIRNAME = "sessions"
_CHAINS_SUBDIRNAME = "chains"
_STATE_SUFFIX = ".json"
_MAX_CHECKPOINT_BYTES = 512_000
_MAX_STEPS_RECORD = 200


def checkpoint_dir(base_dir: str | Path | None = None) -> Path:
    """Return the directory that stores chain checkpoints."""
    if base_dir is not None:
        return Path(base_dir)
    return Path.cwd() / _SESSIONS_DIRNAME / _CHAINS_SUBDIRNAME


def new_run_id(chain_name: str) -> str:
    """Return a collision-resistant run id for one chain execution."""
    slug = "".join(char if char.isalnum() else "_" for char in str(chain_name)).strip("_")[:32] or "chain"
    return f"{slug}_{time.strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"


def write_checkpoint(directory: Path | str, state: dict[str, Any]) -> Path:
    """Persist one chain run state as JSON and return the file path.

    Args:
        directory: Target checkpoint directory (created when missing).
        state: JSON-serializable run state; keys are truncated so a
            pathological chain cannot bloat the file.

    Returns:
        Path of the written checkpoint.

    Raises:
        OSError: When the directory cannot be created or written.
    """
    path = checkpoint_dir(directory) / (f"{state.get('run_id', 'unknown')}{_STATE_SUFFIX}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(state)
    payload["steps"] = list(payload.get("steps") or [])[:_MAX_STEPS_RECORD]
    payload["updated_at"] = time.time()
    text = json.dumps(payload, default=str)[:_MAX_CHECKPOINT_BYTES * 4]
    tmp = path.with_suffix(_STATE_SUFFIX + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
    return path


def load_checkpoint(directory: Path | str, run_id: str) -> dict[str, Any] | None:
    """Load one checkpoint by run id, or None when missing/unreadable."""
    wanted = str(run_id).strip()
    if not wanted:
        return None
    path = checkpoint_dir(directory) / f"{wanted}{_STATE_SUFFIX}"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def list_checkpoints(
    directory: Path | str | None = None,
    limit: int = 20,
    chain: str = "",
) -> list[dict[str, Any]]:
    """Return the newest checkpoints (run_id, chain, target, state, times).

    Args:
        directory: Checkpoint directory override.
        limit: Maximum rows to return.
        chain: Optional chain-name filter, case-insensitive.

    Returns:
        Newest-first rows; each row also carries ``ok``/``aborted``/
        ``reason`` so callers can identify the failed runs.
    """
    directory = checkpoint_dir(directory)
    lowered_chain = (chain or "").strip().lower()
    rows: list[dict[str, Any]] = []
    if not directory.is_dir():
        return rows
    for path in sorted(directory.glob(f"*{_STATE_SUFFIX}"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        if lowered_chain and str(data.get("chain", "")).lower() != lowered_chain:
            continue
        rows.append(
            {
                "run_id": str(data.get("run_id", path.stem)),
                "chain": str(data.get("chain", "")),
                "target": str(data.get("target", "")),
                "state": str(data.get("state", "")),
                "ok": bool(data.get("ok", True)),
                "aborted": bool(data.get("aborted", False)),
                "reason": str(data.get("reason", "")),
                "steps": int(len(data.get("steps") or [])),
                "started_at": float(data.get("started_at", 0.0) or 0.0),
                "updated_at": float(data.get("updated_at", 0.0) or 0.0),
                "path": str(path),
            }
        )
        if len(rows) >= max(1, limit):
            break
    return rows


__all__ = [
    "checkpoint_dir",
    "list_checkpoints",
    "load_checkpoint",
    "new_run_id",
    "write_checkpoint",
]
