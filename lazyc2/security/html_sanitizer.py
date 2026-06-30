"""HTML sanitizer backed by ``bleach`` for the LazyOwn C2 web layer.

Contract: this module is the single source of truth for cleaning
operator-supplied HTML before it is rendered. It replaces the previous
regex-based approach in :mod:`lazyc2`, which was vulnerable to nested
tag and ``javascript:`` URI bypasses.

Invariants:

1. ``<script>``, ``<iframe>``, ``<object>``, ``<embed>``, ``<style>`` and
   their contents are removed entirely.
2. ``on*`` event handlers are stripped from every element.
3. ``javascript:`` URIs in ``href`` and ``src`` are neutralised.
4. Benign tags (``p``, ``strong``, ``em``, ``ul``, ``ol``, ``li``, ``a``,
   ``code``, ``pre``, ``h1``..``h6``, ``blockquote``) survive untouched.
5. The allowlist can be overridden by the caller, in which case the
   defaults from :mod:`lazyc2.security.constants` are not used.

Config keys owned: none (the defaults live in
:mod:`lazyc2.security.constants`).
"""

from __future__ import annotations

import re
from typing import Iterable

import bleach

from lazyc2.security.constants import ALLOWED_HTML_ATTRIBUTES, ALLOWED_HTML_TAGS


_DEFAULT_PROTOCOL_ALLOWLIST = frozenset({"http", "https", "mailto"})

_DANGEROUS_BLOCK_TAGS: tuple[str, ...] = (
    "script",
    "iframe",
    "object",
    "embed",
    "style",
    "svg",
    "math",
    "form",
    "input",
    "button",
    "textarea",
    "select",
)

_DANGEROUS_BLOCK_PATTERN = re.compile(
    r"<\s*(?P<tag>" + "|".join(_DANGEROUS_BLOCK_TAGS) + r")\b[^>]*>.*?</\s*(?P=tag)\s*>",
    re.IGNORECASE | re.DOTALL,
)

_DANGEROUS_VOID_PATTERN = re.compile(
    r"<\s*(?P<tag>" + "|".join(_DANGEROUS_BLOCK_TAGS) + r")\b[^>]*/?>",
    re.IGNORECASE,
)

_HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_dangerous_blocks(raw_html: str) -> str:
    """Remove dangerous element blocks and their contents.

    Args:
        raw_html: The HTML string to pre-process.

    Returns:
        The HTML with ``<script>``, ``<style>``, ``<iframe>`` and the
        other dangerous block tags completely removed.
    """
    cleaned = _DANGEROUS_BLOCK_PATTERN.sub("", raw_html)
    cleaned = _DANGEROUS_VOID_PATTERN.sub("", cleaned)
    cleaned = _HTML_COMMENT_PATTERN.sub("", cleaned)
    return cleaned


def sanitize_html(
    raw_html: str | None,
    allowed_tags: Iterable[str] | None = None,
    allowed_attributes: dict[str, Iterable[str]] | None = None,
) -> str:
    """Return a sanitized HTML string safe for ``render_template``.

    Args:
        raw_html: The HTML to clean. ``None`` or empty returns ``""``.
        allowed_tags: Optional override for the tag allowlist.
        allowed_attributes: Optional override for the attribute map.

    Returns:
        The sanitized HTML. Guaranteed to contain no ``<script>``,
        ``<iframe>``, ``<object>``, ``<embed>``, ``<style>``, ``on*``
        attributes, ``javascript:`` URIs, or HTML comments.
    """
    if not raw_html:
        return ""
    pre = _strip_dangerous_blocks(raw_html)
    tags = set(allowed_tags) if allowed_tags is not None else set(ALLOWED_HTML_TAGS)
    attrs = dict(allowed_attributes) if allowed_attributes is not None else dict(ALLOWED_HTML_ATTRIBUTES)
    cleaned = bleach.clean(
        pre,
        tags=tags,
        attributes=attrs,
        protocols=_DEFAULT_PROTOCOL_ALLOWLIST,
        strip=True,
        strip_comments=True,
    )
    return cleaned


__all__ = ["sanitize_html"]
