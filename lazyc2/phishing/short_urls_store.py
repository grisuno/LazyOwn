"""Short-URL registry persistence for the phishing domain.

Single implementation of the ``short_urls.json`` load/save contract shared
by the C2 routes and the campaign blueprint. The registry file lives under
the campaigns directory as declared in :mod:`lazyc2.phishing.paths`.
"""

from __future__ import annotations

import json
import logging
import os

from lazyc2.phishing.paths import SHORT_URLS_FILE

_log = logging.getLogger(__name__)


def load_short_urls() -> dict:
    """Load the short-URL registry, creating the file when missing.

    Returns:
        Dict mapping short codes to their metadata (original_url, active,
        created_at); an empty dict when the file cannot be parsed.
    """
    if not os.path.exists(SHORT_URLS_FILE):
        try:
            with open(SHORT_URLS_FILE, "w") as f:
                json.dump({}, f)
        except Exception:
            _log.error("Failed to create short_urls.json: %s", "")
            raise
    try:
        with open(SHORT_URLS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        _log.error("Failed to parse short_urls.json: %s", "")
        return {}
    except Exception:
        _log.error("Error reading short_urls.json: %s", "")
        raise


def save_short_urls(data: dict) -> None:
    """Persist the short-URL registry.

    Args:
        data: Registry mapping short codes to their metadata.
    """
    try:
        with open(SHORT_URLS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        _log.error("Failed to save short_urls.json: %s", "")
        raise
