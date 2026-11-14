"""Canonical operating limits for the autonomous loop.

Single source of truth for the CLI parse defaults and hard caps shared
by ``modules.lazy_runner`` (CLI runner), ``modules.loop_manager`` (C2
dashboard subprocess manager) and the ``auto_loop`` MCP tool. Engine
direct-call defaults are a separate concern and stay in
``modules.lazy_loop`` (``ENGINE_DEFAULT_*``).
"""

from __future__ import annotations

DEFAULT_ROUNDS = 6
DEFAULT_WORKERS = 2
MAX_ROUNDS = 50
MAX_WORKERS = 5

__all__ = [
    "DEFAULT_ROUNDS",
    "DEFAULT_WORKERS",
    "MAX_ROUNDS",
    "MAX_WORKERS",
]
