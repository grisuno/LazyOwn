"""C2 auto-generated credentials discovery.

``lazyc2.py`` writes ``.c2_credentials.txt`` at startup containing the
auto-generated strong credentials. This module provides the parser that
reads that file and returns a ``(username, password)`` tuple so the GUI
can auto-connect without manual credential entry.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

_logger = logging.getLogger(__name__)

_CREDENTIALS_FILE_NAME: str = ".c2_credentials.txt"
_USERNAME_PATTERN = re.compile(r"^USERNAME=(\S+)", re.MULTILINE)
_PASSWORD_PATTERN = re.compile(r"^PASSWORD=(\S+)", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class C2Credentials:
    """Parsed credentials from the auto-generated file."""

    username: str
    password: str
    source_path: Path
    loaded: bool = True

    @classmethod
    def empty(cls) -> C2Credentials:
        """Return a sentinel representing no credentials available."""
        return cls(username="", password="", source_path=Path("."), loaded=False)


def load_c2_credentials_from_file(file_path: Path) -> C2Credentials:
    """Parse ``.c2_credentials.txt`` and return username + password.

    Args:
        file_path: Absolute path to the credentials file.

    Returns:
        A populated :class:`C2Credentials` if the file exists and contains
        valid entries, or :meth:`C2Credentials.empty` otherwise.
    """
    if not file_path.is_file():
        return C2Credentials.empty()
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        _logger.warning("Failed to read credentials file %s: %s", file_path, exc)
        return C2Credentials.empty()

    user_match = _USERNAME_PATTERN.search(content)
    pass_match = _PASSWORD_PATTERN.search(content)

    if not user_match or not pass_match:
        _logger.warning("Credentials file %s missing USERNAME or PASSWORD line", file_path)
        return C2Credentials.empty()

    return C2Credentials(
        username=user_match.group(1),
        password=pass_match.group(1),
        source_path=file_path,
        loaded=True,
    )


def load_c2_credentials(project_root: Path) -> C2Credentials:
    """Resolve and parse the credentials file relative to ``project_root``.

    Args:
        project_root: The LazyOwn repository root directory.

    Returns:
        A :class:`C2Credentials` instance, found or empty.
    """
    file_path = project_root / _CREDENTIALS_FILE_NAME
    return load_c2_credentials_from_file(file_path)
