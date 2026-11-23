"""Short URL management shim for the C2 phishing module.

Delegates the ``short_urls.json`` load/save contract to
:mod:`lazyc2.phishing.short_urls_store` so the monolith routes and the
factory-path blueprint share one registry implementation and one file.
Intended for internal use by :mod:`lazyc2.blueprints.phishing`.
"""

from __future__ import annotations

import logging
import os
from urllib.parse import urlparse

import validators

from lazyc2.phishing.paths import SHORT_URLS_FILE
from lazyc2.phishing.short_urls_store import load_short_urls, save_short_urls

ALLOWED_BASE_DIR = os.path.abspath("./sessions")

__all__ = [
    "ALLOWED_BASE_DIR",
    "SHORT_URLS_FILE",
    "configure",
    "is_valid_url",
    "load_short_urls",
    "save_short_urls",
]


def configure(sessions_phishing_dir: str) -> None:
    """Record the phishing directory where short_urls.json lives.

    Kept for backwards compatibility with :mod:`lazyc2.app_factory`; the
    registry path itself is owned by
    :data:`lazyc2.phishing.paths.SHORT_URLS_FILE` and never changes.

    Args:
        sessions_phishing_dir: Absolute or relative path to the phishing
            session directory.
    """
    _ = sessions_phishing_dir


def _get_safe_file_path(user_path: str) -> str | None:
    """Resolve a user-supplied path safely under ALLOWED_BASE_DIR.

    Args:
        user_path: Raw path supplied by the caller (possibly ``file://``
            prefixed).

    Returns:
        Absolute safe path if the resolved location is contained under
        ``ALLOWED_BASE_DIR``, otherwise ``None``.
    """
    if user_path.startswith("file://"):
        user_path = user_path[7:]
    normalized = os.path.normpath(user_path)
    abs_user = os.path.abspath(normalized)
    abs_allowed = os.path.abspath(ALLOWED_BASE_DIR)
    try:
        common = os.path.commonpath([abs_allowed, abs_user])
        if common != abs_allowed:
            logging.warning("Path outside allowed directory: %s", abs_user)
            return None
    except ValueError:
        logging.warning("Invalid path structure: %s", abs_user)
        return None
    if not abs_user.startswith(abs_allowed + os.sep):
        logging.warning("Path not within allowed directory: %s", abs_user)
        return None
    return abs_user


def is_valid_url(url: str) -> bool:
    """Validate if the input is a valid URL or existing local file path.

    Args:
        url: URL string or local file path to validate.

    Returns:
        ``True`` when the value is a valid web URL or an existing local
        file under the allowed base directory.
    """
    if validators.url(url):
        return True
    parsed = urlparse(url)
    if parsed.scheme in ("file", "") or not parsed.scheme:
        file_path = parsed.path if parsed.scheme == "file" else url
        safe = _get_safe_file_path(file_path)
        if not safe:
            return False
        return os.path.exists(safe) and os.path.isfile(safe)
    return False
