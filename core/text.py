"""Text hardening: HTML escaping, emoji detection and secret redaction.

Pure string operations with no I/O: HTML contexts get escaped values,
emoji codepoints are detectable and enumerable, and credential-like
patterns are masked before persistence or display.
"""

from __future__ import annotations

import html
import re

_EMOJI_RANGES: tuple[tuple[int, int], ...] = (
    (0x1F600, 0x1F64F),
    (0x1F300, 0x1F5FF),
    (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F),
    (0x1F780, 0x1F7FF),
    (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF),
    (0x1FA70, 0x1FAFF),
    (0x2600, 0x26FF),
    (0x2700, 0x27BF),
    (0x2B00, 0x2BFF),
    (0xFE00, 0xFE0F),
    (0x200D, 0x200D),
)

_REDACT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(smbpass\s+)([^\s;]{1,128})"),
    re.compile(r"(?i)(password\s*[=:]\s*['\"]?)([^'\"\s;]{1,128})"),
    re.compile(r"(?i)(passwd\s*[=:]\s*['\"]?)([^'\"\s;]{1,128})"),
    re.compile(r"(?i)(pwd\s*[=:]\s*['\"]?)([^'\"\s;]{1,128})"),
    re.compile(r"(?i)(api[_-]?key\s*[=:]\s*['\"]?)([\w\-.]{8,})(['\"]?)"),
    re.compile(r"(?i)((?:GROQ|OPENAI|DEEPSEEK|ANTHROPIC)[_A-Z]*KEY\s*=\s*['\"]?)([^'\"\s]{8,})"),
    re.compile(r"glpat-[A-Za-z0-9\-_]{8,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[bpa]-[A-Za-z0-9\-]{8,}"),
    re.compile(r"gsk_[A-Za-z0-9]+"),
    re.compile(r"sk-[A-Za-z0-9\-_]{8,}"),
    re.compile(r"ghp_[A-Za-z0-9]{8,}"),
    re.compile(r"gho_[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)(bearer\s+)([A-Za-z0-9\-._~+/]{8,})"),
    re.compile(r"https?://[^/\s]*:[^@/\s]+@[^\s]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def escape_html_content(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), quote=True)


def escape_powershell_single_quoted(value: str) -> str:
    """Escape a value for embedding in a PowerShell single-quoted string.

    Args:
        value: Raw value that may contain quotes or metacharacters.

    Returns:
        Value safe to embed between single quotes in PowerShell.
    """
    return str(value).replace("'", "''")


def _is_emoji_codepoint(code: int) -> bool:
    """Return True when ``code`` falls in a known emoji interval."""
    for start, end in _EMOJI_RANGES:
        if start <= code <= end:
            return True
    return False


def contains_emoji(text: str) -> bool:
    """Return True when ``text`` carries any emoji codepoint.

    Args:
        text: Text to inspect.

    Returns:
        True on first emoji hit; linear scan, no regex.
    """
    for char in text or "":
        if _is_emoji_codepoint(ord(char)):
            return True
    return False


def iter_emoji_spans(text: str) -> list[tuple[int, str]]:
    """Return ``(offset, char)`` for every emoji char in ``text``.

    Args:
        text: Text to inspect.

    Returns:
        List of offset/character pairs in encounter order.
    """
    spans: list[tuple[int, str]] = []
    for offset, char in enumerate(text or ""):
        if _is_emoji_codepoint(ord(char)):
            spans.append((offset, char))
    return spans


def redact_text(text: str) -> str:
    """Mask credential-like patterns before persistence or display.

    Args:
        text: Raw text that may embed secrets.

    Returns:
        Text with secrets replaced by ``***`` markers.
    """
    cleaned = str(text or "")

    def _mask(match: re.Match) -> str:
        groups = match.groups()
        if len(groups) >= 2 and groups[0] and groups[-1] is not None:
            return f"{groups[0]}***{groups[-1] if len(groups) > 2 else ''}"
        return "***"

    for pattern in _REDACT_PATTERNS:
        cleaned = pattern.sub("***" if pattern.groups == 0 else _mask, cleaned)
    return cleaned


__all__ = [
    "contains_emoji",
    "escape_html_content",
    "escape_powershell_single_quoted",
    "iter_emoji_spans",
    "redact_text",
]
