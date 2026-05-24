"""Enforce a hard cap on ``CLAUDE.md`` size.

``CLAUDE.md`` is loaded into every assistant conversation. The Anthropic
prompt cache only pays off when the document fits comfortably in the
warm-cache window; beyond ~40 KB the file becomes a tax on every turn
and the marginal context is rarely worth the cost. Long-form material
belongs in the per-directory README files, with CLAUDE.md keeping only
the durable, cross-cutting context.

This test is intentionally a single assertion so a future drift breaks
exactly one line.
"""

from __future__ import annotations

from pathlib import Path

CLAUDE_MD = Path(__file__).resolve().parent.parent / "CLAUDE.md"
MAX_BYTES = 40 * 1024


def test_claude_md_under_size_budget() -> None:
    """``CLAUDE.md`` must stay under the 40 KB prompt-cache budget."""
    assert CLAUDE_MD.is_file(), "CLAUDE.md missing — repository in unexpected state"
    size = CLAUDE_MD.stat().st_size
    assert size <= MAX_BYTES, (
        f"CLAUDE.md is {size} bytes; budget is {MAX_BYTES} bytes. "
        "Move long-form material into a directory README and link to it."
    )
