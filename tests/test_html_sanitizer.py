"""TDD tests for the bleach-based HTML sanitizer contract.

Contract: ``lazyc2.security.html_sanitizer.sanitize_html`` strips all
dangerous tags and attributes from a snippet of HTML while keeping the
benign formatting tags operators rely on for notes and reports.

Invariants:

1. ``<script>...</script>`` is removed entirely.
2. ``<iframe>``, ``<object>``, ``<embed>``, and ``<style>`` are removed.
3. ``on*=`` event handlers (e.g. ``onerror``, ``onclick``) are stripped.
4. ``javascript:`` URIs in ``href`` and ``src`` are stripped.
5. Benign tags (``p``, ``strong``, ``em``, ``ul``, ``ol``, ``li``, ``a``,
   ``code``, ``pre``, ``h1``..``h6``, ``blockquote``) survive untouched.
6. The ``allowed_tags`` and ``allowed_attributes`` can be overridden by
   the caller; the defaults are derived from
   :mod:`lazyc2.security.constants`.
"""

from __future__ import annotations

import pytest

from lazyc2.security.html_sanitizer import sanitize_html


class TestScriptStripping:
    """Dangerous script blocks must be removed."""

    def test_script_block_removed(self) -> None:
        out = sanitize_html("<p>hi</p><script>alert(1)</script>")
        assert "<script" not in out
        assert "alert(1)" not in out

    def test_iframe_removed(self) -> None:
        out = sanitize_html('<iframe src="http://evil"></iframe>hi')
        assert "<iframe" not in out
        assert "evil" not in out

    def test_object_and_embed_removed(self) -> None:
        out = sanitize_html('<object data="x"></object><embed src="y">')
        assert "<object" not in out
        assert "<embed" not in out

    def test_style_removed(self) -> None:
        out = sanitize_html("<style>body{display:none}</style><p>x</p>")
        assert "<style" not in out
        assert "display:none" not in out


class TestEventHandlerStripping:
    """Inline event handlers must be removed."""

    def test_onclick_removed(self) -> None:
        out = sanitize_html('<a href="x" onclick="bad()">link</a>')
        assert "onclick" not in out
        assert "bad()" not in out

    def test_onerror_removed(self) -> None:
        out = sanitize_html('<img src="x" onerror="bad()">')
        assert "onerror" not in out
        assert "bad()" not in out


class TestJavascriptUriStripping:
    """``javascript:`` URIs must be neutralised."""

    def test_javascript_href_stripped(self) -> None:
        out = sanitize_html('<a href="javascript:alert(1)">x</a>')
        assert "javascript:" not in out


class TestBenignTagsPreserved:
    """Benign formatting tags must survive untouched."""

    def test_basic_formatting_preserved(self) -> None:
        out = sanitize_html("<p>hello <strong>world</strong></p>")
        assert "<p>" in out
        assert "<strong>" in out
        assert "hello" in out
        assert "world" in out

    def test_lists_preserved(self) -> None:
        out = sanitize_html("<ul><li>one</li><li>two</li></ul>")
        assert "<ul>" in out
        assert "<li>one</li>" in out or "<li>one</li>" in out

    def test_headings_preserved(self) -> None:
        for level in range(1, 7):
            out = sanitize_html(f"<h{level}>title</h{level}>")
            assert f"<h{level}>" in out
            assert "title" in out


class TestCustomAllowlist:
    """Allowlist overrides must be honoured."""

    def test_strict_allowlist_strips_more(self) -> None:
        out = sanitize_html(
            "<p>kept</p><strong>stripped</strong>",
            allowed_tags={"p"},
        )
        assert "<p>" in out
        assert "<strong>" not in out
