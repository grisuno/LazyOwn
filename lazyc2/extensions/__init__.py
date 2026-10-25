"""Shared C2 extension modules.

Each module is a self-contained set of helpers that the monolithic
``lazyc2.py`` and/or individual Flask blueprints import. Call the
module-level ``configure()`` function during app initialisation to
set paths.
"""

from lazyc2.extensions import decoy, short_urls, storage

__all__ = ["decoy", "short_urls", "storage"]
