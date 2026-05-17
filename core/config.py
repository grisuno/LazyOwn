"""Configuration loader and Config wrapper.

``payload.json`` is the single source of runtime configuration for the entire
LazyOwn framework. This module exposes:

- ``PAYLOAD_PATH`` constant pointing at ``payload.json`` in the current working
  directory.
- ``load_payload`` / ``save_payload`` for reading and writing it atomically.
- ``Config`` — a thin attribute-style wrapper around the payload dictionary.

Atomic writes go through ``*.tmp`` and ``os.replace`` so a crashed write never
leaves the operator with a corrupt payload file.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

PAYLOAD_FILENAME = "payload.json"
PAYLOAD_PATH = Path(PAYLOAD_FILENAME)


class Config:
    """Attribute-style wrapper around a configuration dictionary.

    Behavior is intentionally preserved from the legacy ``utils.Config``:
    every key in the underlying dictionary becomes both an instance attribute
    and is accessible via ``config[key]``. Missing keys via ``__getitem__``
    return ``None`` rather than raising.
    """

    def __init__(self, config_dict: dict[str, Any]) -> None:
        self.config: dict[str, Any] = config_dict
        for key, value in self.config.items():
            setattr(self, key, value)

    def __getattr__(self, name: str) -> Any:
        return None

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)


def load_payload(path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> dict[str, Any]:
    """Load and return the JSON payload at ``path``.

    Raises:
        FileNotFoundError: if the payload does not exist.
        json.JSONDecodeError: if the payload is not valid JSON.
    """
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_payload(payload: dict[str, Any], path: str | os.PathLike[str] = PAYLOAD_FILENAME) -> None:
    """Atomically write ``payload`` as pretty-printed JSON to ``path``.

    Uses a sibling ``*.tmp`` file plus ``os.replace`` so a crash mid-write
    cannot leave the operator with a half-written payload.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent or "."),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp_name, target)
    except Exception:
        if os.path.exists(tmp_name):
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        raise


__all__ = ["Config", "load_payload", "save_payload", "PAYLOAD_PATH", "PAYLOAD_FILENAME"]
