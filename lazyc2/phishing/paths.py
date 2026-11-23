"""Canonical storage layout for the phishing domain.

Single source of truth for where campaigns, email templates, the tracking
database and the short-URL registry live. :func:`ensure_storage` creates
the directories and the tracking tables and is idempotent, so the C2 boot
path and tests can call it freely.
"""

from __future__ import annotations

import logging
import os
import sqlite3

_log = logging.getLogger(__name__)

CAMPAIGNS_DIR = os.path.join(os.getcwd(), "sessions", "phishing", "campaigns")
TEMPLATES_DIR = os.path.join(os.getcwd(), "templates", "phishing", "emails")
DB_PATH = os.path.join(os.getcwd(), "sessions", "phishing", "tracking.db")
SHORT_URLS_FILE = os.path.join(CAMPAIGNS_DIR, "short_urls.json")


def ensure_storage() -> None:
    """Create the phishing directories and tracking tables when missing.

    Never raises: a storage failure is logged and left to the per-request
    error paths, matching the fail-soft behaviour of the original boot
    block.
    """
    try:
        os.makedirs(CAMPAIGNS_DIR, exist_ok=True)
        os.makedirs(TEMPLATES_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS tracking "
                "(campaign_id TEXT, email TEXT, event TEXT, ip TEXT, timestamp TEXT)"
            )
            conn.commit()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS behavioral_tracking ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "campaign_id TEXT, short_url TEXT, email TEXT, event_type TEXT, "
                "ip TEXT, user_agent TEXT, timestamp TEXT, behavior_data TEXT)"
            )
            conn.commit()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS multivector_tracking ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "campaign_id TEXT, email TEXT, event_type TEXT, ip TEXT, timestamp TEXT)"
            )
            conn.commit()
        finally:
            conn.close()
    except OSError as exc:
        _log.warning("[phishing] storage bootstrap failed: %s", exc)
    except sqlite3.Error as exc:
        _log.warning("[phishing] tracking schema bootstrap failed: %s", exc)
