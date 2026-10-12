"""Incremental JSONL reader shared by the monitor TUI and the loop runner.

The activity log only ever appends, so a byte offset is a stable cursor:
each reader keeps its own offset and returns only complete records,
tolerating a partially written final line.
"""

from __future__ import annotations

import json
from pathlib import Path


class JsonlTail:
    """Incremental JSONL reader that tolerates partially-written lines."""

    def __init__(self, path: str | Path) -> None:
        """Bind the tail to one file path."""
        self.path = Path(path)
        self.offset = 0

    def read_new(self, limit: int = 500) -> list[dict]:
        """Return new complete records since the last call."""
        if not self.path.exists():
            return []
        out: list[dict] = []
        try:
            with self.path.open("r", encoding="utf-8", errors="replace") as handle:
                handle.seek(self.offset)
                while len(out) < max(1, limit):
                    position = handle.tell()
                    line = handle.readline()
                    if not line:
                        break
                    if not line.endswith("\n"):
                        handle.seek(position)
                        break
                    try:
                        record = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(record, dict):
                        out.append(record)
                self.offset = handle.tell()
        except OSError:
            return []
        return out


__all__ = ["JsonlTail"]
