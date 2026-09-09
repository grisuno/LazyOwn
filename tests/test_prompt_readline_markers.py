"""Regression tests for readline marker handling in the Neon Box prompt.

Covers the ``^A``/``^B`` leak reported when the cmd2 prompt wrapped
newlines in readline zero-width markers. Markers must fence ANSI
escapes only, never newlines or printable text.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.banner_config import (  # noqa: E402
    BannerConfig,
    _readline_safe,
    render_prompt,
    strip_ansi,
    strip_readline_markers,
)


def test_ansi_escape_gets_fenced():
    """ANSI escapes are wrapped while printable text stays bare."""
    cfg = BannerConfig()
    fenced = _readline_safe("\033[96mX\033[0m", cfg)
    assert (
        fenced
        == f"{cfg.readline_start_marker}\033[96m{cfg.readline_end_marker}X{cfg.readline_start_marker}\033[0m{cfg.readline_end_marker}"
    )


def test_newline_stays_bare():
    """Newlines are never wrapped in zero-width markers."""
    cfg = BannerConfig()
    fenced = _readline_safe("line_one\nline_two", cfg)
    assert fenced == "line_one\nline_two"
    assert f"{cfg.readline_start_marker}\n{cfg.readline_end_marker}" not in fenced


def test_mixed_prompt_fences_only_ansi():
    """Mixed content fences escapes and preserves line breaks verbatim."""
    cfg = BannerConfig()
    raw = "\033[96mA\033[0m\nplain $\x20"
    fenced = _readline_safe(raw, cfg)
    assert "\n" in fenced
    assert fenced.count("\n") == raw.count("\n")
    assert strip_readline_markers(fenced, cfg) == raw


def test_render_prompt_default_has_no_markers():
    """Default prompt is raw ANSI for prompt_toolkit, free of markers."""
    cfg = BannerConfig()
    prompt = render_prompt(None, cfg)
    assert cfg.readline_start_marker not in prompt
    assert cfg.readline_end_marker not in prompt
    assert prompt.count("\n") == 2


def test_render_prompt_readline_mode_fences_ansi_only():
    """Opt-in readline mode fences escapes and never wraps newlines."""
    cfg = BannerConfig()
    prompt = render_prompt(None, cfg, readline_safe=True)
    assert f"{cfg.readline_start_marker}\n{cfg.readline_end_marker}" not in prompt
    assert prompt.count("\n") == 2


def test_render_prompt_raw_has_no_markers():
    """Display mode returns raw ANSI without any readline markers."""
    cfg = BannerConfig()
    raw = render_prompt(None, cfg, readline_safe=False)
    assert cfg.readline_start_marker not in raw
    assert cfg.readline_end_marker not in raw
    assert raw.count("\n") == 2


def test_strip_readline_markers_restores_raw():
    """Stripping markers from the readline prompt restores display text."""
    cfg = BannerConfig()
    safe = render_prompt(None, cfg, readline_safe=True)
    raw = render_prompt(None, cfg, readline_safe=False)
    assert strip_readline_markers(safe, cfg) == raw


def test_stripped_prompt_matches_box_shape():
    """Fully stripped prompt keeps the three-line Neon Box structure."""
    plain = strip_ansi(render_prompt(None))
    lines = plain.splitlines()
    assert len(lines) == 3
    assert lines[0].startswith("╔")
    assert lines[1].startswith("║")
    assert lines[2].startswith("╚")
