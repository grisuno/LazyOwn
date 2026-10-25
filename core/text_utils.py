"""Shared text helpers for terminal surfaces.

Single source of truth for truncating display strings. Replaces eight
near-identical ``_truncate`` copies across ``cli/``.
"""

from __future__ import annotations


def truncate_text(value: str | None, max_len: int, marker: str = "…") -> str:
    """Truncate value to max_len using marker.

    Args:
        value: Text to truncate. None becomes empty string.
        max_len: Maximum output length including marker.
        marker: Suffix appended when truncation occurs.

    Returns:
        Truncated string of at most max_len characters.
    """
    text = value or ""
    if max_len <= 0:
        return ""
    if len(text) <= max_len:
        return text
    if len(marker) >= max_len:
        return marker[:max_len]
    return text[: max_len - len(marker)] + marker


__all__ = ["truncate_text"]
