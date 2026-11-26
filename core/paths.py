"""Filesystem path hardening for untrusted inputs.

Every helper here enforces the same containment shape static analysers
recognise: canonicalise with ``os.path.realpath`` and require the result
to stay inside the realpath of the allowed base directory. Symlink
escapes, ``..`` segments, control characters and overlong values are
rejected in linear time.
"""

from __future__ import annotations

import os
import re
from typing import Any

from core.errors import SecurityViolation
from core.secrets import SECRET_FILE_MODE

UPSTREAM_PATH_MAX_LENGTH = 8192
DIR_PATH_MAX_LENGTH = 256
PATH_SEGMENT_MAX_LENGTH = 64
YAML_NAME_MAX_LENGTH = 128
YAML_SUFFIX = ".yaml"

_SAFE_SEGMENT_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")

_SAFE_PATH_PATTERN = re.compile(r"^[a-zA-Z0-9._/\-]+$")


def realpath_within_base(base_dir: str, user_path: str) -> str:
    """Resolve ``user_path`` against ``base_dir`` and enforce containment.

    Both sides go through ``os.path.realpath`` (normalisation) and the
    result must pass a ``startswith`` guard against the base plus a
    separator, which is the containment shape static analysers
    recognise as a safe access check. Symlink escapes are rejected
    because the final realpath of the candidate must still live under
    the realpath of the base.

    Args:
        base_dir: The allowed root directory.
        user_path: Untrusted relative path joined under ``base_dir``.

    Returns:
        Resolved absolute path strictly inside ``base_dir``.

    Raises:
        SecurityViolation: If the resolved path escapes ``base_dir``.
    """
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep):
        raise SecurityViolation(f"Path traversal blocked: {user_path!r} resolves outside {base_dir}")
    return candidate


def realpath_contained(user_path: str, base_dir: str) -> str:
    """Return ``user_path`` realpath-verified to stay inside ``base_dir``.

    Unlike :func:`realpath_within_base` the untrusted value may already
    be an absolute path (or CWD-relative); it is canonicalised on its
    own and then containment-checked against the base.

    Args:
        user_path: Untrusted path (absolute or relative to the CWD).
        base_dir: The allowed root directory.

    Returns:
        Resolved absolute path strictly inside ``base_dir``.

    Raises:
        SecurityViolation: If the resolved path escapes ``base_dir``.
    """
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(user_path)
    if not candidate.startswith(allowed + os.sep):
        raise SecurityViolation(f"Path traversal blocked: {user_path!r} resolves outside {base_dir}")
    return candidate


def safe_path_join(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Delegates to :func:`realpath_within_base`.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    return realpath_within_base(base_dir, user_path)


def validate_upstream_path(path: str) -> bool:
    """Validate an origin-form upstream path without regular expressions.

    Only ``/absolute-path[?query]`` is accepted: absolute URLs, control
    characters, NUL/CR/LF and overlong values are rejected in linear time.

    Args:
        path: Upstream path or target string.

    Returns:
        True when the path is safe to send upstream.
    """
    text = path or ""
    if not text or len(text) > UPSTREAM_PATH_MAX_LENGTH:
        return False
    if not text.startswith("/"):
        return False
    lowered = text.lower()
    if "://" in lowered:
        return False
    for char in text:
        code = ord(char)
        if code < 32 or code == 127:
            return False
    if "\x00" in text:
        return False
    return True


def is_safe_path_segment(segment: str) -> bool:
    """Validate one path segment with a linear charset scan (no regex).

    Args:
        segment: Single directory or filename stem segment.

    Returns:
        True when the segment uses only safe characters.
    """
    if not segment or len(segment) > PATH_SEGMENT_MAX_LENGTH:
        return False
    if segment in (".", ".."):
        return False
    if segment.startswith("."):
        return False
    for char in segment:
        if char not in _SAFE_SEGMENT_CHARS:
            return False
    return True


def is_safe_dir_path(raw: str) -> bool:
    """Validate a relative directory path with linear scans (no regex).

    Args:
        raw: Untrusted relative directory path.

    Returns:
        True when every segment is safe and no traversal is present.
    """
    if not raw or len(raw) > DIR_PATH_MAX_LENGTH:
        return False
    if "\x00" in raw or "\\" in raw:
        return False
    if raw.startswith("/") or raw.endswith("/"):
        return False
    parts = raw.split("/")
    if len(parts) > 8:
        return False
    if not parts:
        return False
    for part in parts:
        if not is_safe_path_segment(part):
            return False
    return True


def is_safe_yaml_name(name: str) -> bool:
    """Validate a YAML filename with linear scans (no regex).

    Args:
        name: Untrusted filename.

    Returns:
        True when the name is a safe ``*.yaml`` file.
    """
    if not name or len(name) > YAML_NAME_MAX_LENGTH:
        return False
    if "\x00" in name or "/" in name or "\\" in name:
        return False
    if not name.endswith(YAML_SUFFIX):
        return False
    stem = name[: -len(YAML_SUFFIX)]
    return is_safe_path_segment(stem)


def safe_join_under(base_dir: str, user_path: str) -> str:
    """Join and resolve ``user_path`` under ``base_dir`` (symlink-safe).

    Delegates to :func:`realpath_within_base` so ``..`` segments and
    symlink escapes are rejected with the recognised containment guard.

    Args:
        base_dir: Allowed root directory.
        user_path: Untrusted relative path.

    Returns:
        Resolved absolute path within ``base_dir``.

    Raises:
        SecurityViolation: If the resolved path escapes ``base_dir``.
        ValueError: If ``user_path`` is empty.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    return realpath_within_base(base_dir, user_path)


def safe_open_under(base_dir: str, user_path: str, mode: str = "r", **kwargs: Any) -> Any:
    """Open a file under ``base_dir`` after traversal validation.

    Args:
        base_dir: Allowed root directory.
        user_path: Untrusted relative path.
        mode: Open mode (binary-safe modes rejected for writes of text secrets).

    Returns:
        Open file handle. Caller must close it.
    """
    resolved = safe_join_under(base_dir, user_path)
    flags = os.O_RDONLY | os.O_NOFOLLOW
    if "w" in mode or "a" in mode or "+" in mode:
        flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW
        if "a" in mode:
            flags |= os.O_APPEND
        else:
            flags |= os.O_TRUNC
    fd = os.open(resolved, flags, SECRET_FILE_MODE)
    try:
        os.chmod(resolved, SECRET_FILE_MODE)
    except OSError:
        pass
    return os.fdopen(fd, mode, **kwargs)


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


__all__ = [
    "DIR_PATH_MAX_LENGTH",
    "PATH_SEGMENT_MAX_LENGTH",
    "UPSTREAM_PATH_MAX_LENGTH",
    "YAML_NAME_MAX_LENGTH",
    "YAML_SUFFIX",
    "is_safe_dir_path",
    "is_safe_path_segment",
    "is_safe_yaml_name",
    "realpath_contained",
    "realpath_within_base",
    "safe_join_under",
    "safe_open_under",
    "safe_path_join",
    "sanitize_filename",
    "validate_upstream_path",
]
