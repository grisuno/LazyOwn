"""Short URL management utilities for the C2 phishing module.

Provides load/save/validation helpers for short URL redirection
and phishing campaign tracking. Intended for internal use by
:mod:`lazyc2.blueprints.phishing`.
"""

from __future__ import annotations

import json
import logging
import os
from urllib.parse import urlparse

import validators

SHORT_URLS_FILE: str = ""
ALLOWED_BASE_DIR: str = ""


def configure(sessions_phishing_dir: str) -> None:
    """Set the phishing directory where short_urls.json lives.

    Args:
        sessions_phishing_dir: Absolute or relative path to the phishing
            session directory.
    """
    global SHORT_URLS_FILE, ALLOWED_BASE_DIR  # noqa: PLW0603
    SHORT_URLS_FILE = os.path.join(sessions_phishing_dir, "short_urls.json")
    ALLOWED_BASE_DIR = os.path.abspath("./sessions")


def load_short_urls() -> dict:
    """Load short URLs from JSON file, creating it if it doesn't exist.

    Returns:
        A dict mapping short URL keys to their metadata (original_url,
        active, created_at).
    """
    if not os.path.exists(SHORT_URLS_FILE):
        try:
            os.makedirs(os.path.dirname(SHORT_URLS_FILE), exist_ok=True)
            with open(SHORT_URLS_FILE, "w") as f:
                json.dump({}, f)
        except Exception:
            logging.error("Failed to create short_urls.json")
            raise
    try:
        with open(SHORT_URLS_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error("Failed to parse short_urls.json")
        return {}
    except Exception:
        logging.error("Error reading short_urls.json")
        raise


def save_short_urls(data: dict) -> None:
    """Save short URLs to JSON file.

    Args:
        data: Dict mapping short URL keys to their metadata.
    """
    try:
        os.makedirs(os.path.dirname(SHORT_URLS_FILE), exist_ok=True)
        with open(SHORT_URLS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        logging.error("Failed to save short_urls.json")
        raise


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
