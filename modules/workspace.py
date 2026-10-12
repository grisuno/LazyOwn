"""Confined workspace file browser for operators and loop agents.

All paths resolve inside ``sessions/workspace``; traversal attempts
(``..``, absolute paths, symlink escapes) raise before any IO. The loop
can route ``lazy_workspace read <path>`` steps through the same
confined API, so agents inspect task artefacts without leaving the
sandbox.
"""

from __future__ import annotations

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = BASE_DIR / "sessions" / "workspace"
MAX_READ_BYTES = 65536
MAX_WRITE_CHARS = 200000


def root() -> Path:
    """Return (and create) the workspace root directory."""
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    return WORKSPACE_ROOT


def resolve(rel: str) -> Path:
    """Resolve a workspace-relative path, refusing escapes.

    Args:
        rel: Relative path inside the workspace.

    Returns:
        Absolute confined path.

    Raises:
        PermissionError: Path escapes the workspace.
    """
    base = root().resolve()
    candidate = (base / (rel or "")).resolve()
    if candidate != base and base not in candidate.parents:
        raise PermissionError("path escapes the workspace")
    return candidate


def list_entries(rel: str = "") -> list[dict]:
    """List one directory with names, kinds and sizes."""
    base = resolve(rel)
    if not base.is_dir():
        raise FileNotFoundError(f"not a directory: {rel}")
    entries = []
    for entry in sorted(base.iterdir(), key=lambda item: item.name):
        try:
            size = entry.stat().st_size
        except OSError:
            size = 0
        entries.append({"name": entry.name,
                        "kind": "dir" if entry.is_dir() else "file",
                        "size": size})
    return entries


def read_text(rel: str, limit: int = MAX_READ_BYTES) -> str:
    """Read one file, truncated to the byte limit."""
    path = resolve(rel)
    if not path.is_file():
        raise FileNotFoundError(f"not a file: {rel}")
    data = path.read_bytes()[: max(1, int(limit))]
    return data.decode("utf-8", "replace")


def write_text(rel: str, content: str) -> int:
    """Write one file, creating parents; returns the character count."""
    text = str(content or "")
    if len(text) > MAX_WRITE_CHARS:
        raise ValueError(f"content too large (>{MAX_WRITE_CHARS} chars)")
    path = resolve(rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text)


def make_dir(rel: str) -> str:
    """Create one directory (parents included)."""
    path = resolve(rel)
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def remove(rel: str) -> bool:
    """Delete a file or directory tree inside the workspace."""
    path = resolve(rel)
    if not path.exists():
        return False
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


__all__ = ["MAX_READ_BYTES", "MAX_WRITE_CHARS", "WORKSPACE_ROOT",
           "list_entries", "make_dir", "read_text", "remove", "resolve",
           "root", "write_text"]
