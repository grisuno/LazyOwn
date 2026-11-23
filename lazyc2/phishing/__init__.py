"""Phishing domain contracts for the C2 server.

Owns the campaign storage layout (campaigns, email templates, tracking
database, short-URL registry) and the campaign REST blueprint. Import the
public surface from here so route modules and the monolith share one path
contract.
"""

from lazyc2.phishing.paths import (
    CAMPAIGNS_DIR,
    DB_PATH,
    SHORT_URLS_FILE,
    TEMPLATES_DIR,
    ensure_storage,
)
from lazyc2.phishing.short_urls_store import load_short_urls, save_short_urls

__all__ = [
    "CAMPAIGNS_DIR",
    "DB_PATH",
    "SHORT_URLS_FILE",
    "TEMPLATES_DIR",
    "ensure_storage",
    "load_short_urls",
    "save_short_urls",
]
