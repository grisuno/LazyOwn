"""Shared logging helper for swallowed UX-path exceptions.

The interactive shell deliberately swallows exceptions on cosmetic/UX
paths (hints, splash, onboarding, crypto lifecycle) so a non-critical
failure never crashes the operator's session. Those sites still log at
DEBUG so the failure is recoverable from ``lazyown.ux`` logs. This single
helper is the one home for that pattern, shared by ``lazyown.py`` and the
shell mixins under ``cli/`` so the wrapper is not duplicated per module.
"""

from __future__ import annotations

from modules.logging_config import get_logger as _get_logger


def ux_debug(context: str, exc: Exception) -> None:
    """Log a swallowed UX-path exception at DEBUG level.

    Args:
        context: Human-readable description of the failed step.
        exc: The exception that was caught.
    """
    _get_logger("lazyown.ux").debug("%s: %s", context, exc, exc_info=True)
