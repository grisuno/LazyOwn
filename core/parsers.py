"""Shared text kernel for the LazyOwn framework.

Single-implementation rule: the live helpers live in ``utils`` (used
by the CLI and C2). This module keeps only ``strip_ansi``, the one
extraction the framework actually imports. The rest of the historic
``utils.py`` fork was removed because every copy had diverged and
zero callers (see ``tests/test_single_implementation.py``).
"""

from __future__ import annotations

import re


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences and readline markers from a string.

    Handles standard escape codes (``\x1b[...m``), extended unicode
    escape initiators (``\u001b``, ``\u009b``), CSI sequences, and the
    ``\x01``/``\x02`` (SOH/STX) delimiters that ``render_prompt`` emits
    so readline can measure prompt width.

    Args:
        text: Raw terminal output.

    Returns:
        Clean text without ANSI codes or readline control markers.
    """
    ansi_regex = re.compile(r"[\u001b\u009b][\[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]")
    cleaned = ansi_regex.sub("", text)
    return cleaned.replace("\x01", "").replace("\x02", "")


__all__ = ["strip_ansi"]
