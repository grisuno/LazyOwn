"""Tests for cli/fuzzy_picker.py and lint-regression for lazyown.py.

Two concerns are covered here:

1. The fuzzy picker primitives (MatchScorer, PickerConfig, FuzzyPicker,
   ReadlineBridge) — exercised through small fakes so the suite does not
   require an interactive terminal.
2. A regression check that confirms the SyntaxWarning fixes in
   ``lazyown.py`` did not alter the runtime bytes of the affected shell
   command strings. We assert literal substrings rather than scanning the
   source so the test is robust against further escape-related cleanups.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.fuzzy_picker import (  # noqa: E402
    FuzzyPicker,
    MatchScorer,
    PickerConfig,
    PickerItem,
    PickerView,
    ReadlineBridge,
)


class _FakeView(PickerView):
    """Deterministic view used to drive FuzzyPicker without curses."""

    def __init__(self, selection_index: int | None) -> None:
        self.selection_index = selection_index
        self.received_items: Sequence[PickerItem] | None = None
        self.received_query: str | None = None

    def run(self, items: Sequence[PickerItem], initial_query: str) -> str | None:
        self.received_items = list(items)
        self.received_query = initial_query
        if self.selection_index is None:
            return None
        if not items:
            return None
        return items[self.selection_index].text


@pytest.fixture
def scorer() -> MatchScorer:
    return MatchScorer(PickerConfig())


@pytest.fixture
def sample_items() -> list[PickerItem]:
    return [
        PickerItem("lazynmap", "TCP/UDP nmap"),
        PickerItem("lazypass", "password helpers"),
        PickerItem("lazyc2", "C2 controller"),
        PickerItem("evil", "evil-winrm"),
        PickerItem("gobuster", "directory brute"),
    ]


# --- MatchScorer ----------------------------------------------------------


def test_empty_query_returns_all_items_in_order(scorer, sample_items):
    ranked = scorer.rank(sample_items, "")
    assert [r.item.text for r in ranked] == [it.text for it in sample_items]
    assert all(r.score == PickerConfig().score_exact for r in ranked)


def test_exact_match_scores_highest(scorer, sample_items):
    ranked = scorer.rank(sample_items, "evil")
    assert ranked[0].item.text == "evil"
    assert ranked[0].score == PickerConfig().score_exact


def test_prefix_match_outranks_substring(scorer):
    items = [PickerItem("nmap_helper"), PickerItem("xnmapx")]
    ranked = MatchScorer(PickerConfig()).rank(items, "nmap")
    assert ranked[0].item.text == "nmap_helper"


def test_subsequence_match_emits_positions(scorer, sample_items):
    ranked = scorer.rank(sample_items, "lzc")
    assert ranked, "expected at least one subsequence match"
    top = ranked[0]
    assert top.item.text == "lazyc2"
    assert top.positions == (0, 2, 4)


def test_similarity_floor_excludes_unrelated_text(scorer):
    items = [PickerItem("nmap"), PickerItem("aardvark")]
    ranked = MatchScorer(PickerConfig()).rank(items, "xyz")
    assert ranked == []


def test_subsequence_positions_helper_returns_empty_when_no_match():
    positions = MatchScorer._subsequence_positions("abcdef", "zz")
    assert positions == ()


# --- PickerConfig ---------------------------------------------------------


def test_config_from_payload_respects_known_overrides():
    payload = {"fuzzy_picker": {"max_visible_rows": 4, "footer_help": "custom"}}
    cfg = PickerConfig.from_payload(payload)
    assert cfg.max_visible_rows == 4
    assert cfg.footer_help == "custom"


def test_config_from_payload_ignores_unknown_keys():
    cfg = PickerConfig.from_payload({"fuzzy_picker": {"nonsense_field": 99}})
    assert cfg.max_visible_rows == PickerConfig().max_visible_rows


def test_config_from_payload_returns_defaults_when_no_block():
    assert PickerConfig.from_payload({}) == PickerConfig()
    assert PickerConfig.from_payload(None) == PickerConfig()


# --- FuzzyPicker ----------------------------------------------------------


def test_picker_short_circuits_single_item():
    picker = FuzzyPicker(view_factory=lambda cfg, scorer: _FakeView(selection_index=None))
    chosen = picker.pick([PickerItem("solo")])
    assert chosen == "solo"


def test_picker_routes_through_view_for_multiple_items(sample_items):
    fake = _FakeView(selection_index=2)
    picker = FuzzyPicker(view_factory=lambda cfg, scorer: fake)
    chosen = picker.pick(sample_items, initial_query="laz")
    assert chosen == sample_items[2].text
    assert fake.received_query == "laz"


def test_picker_cancel_returns_none(sample_items):
    fake = _FakeView(selection_index=None)
    picker = FuzzyPicker(view_factory=lambda cfg, scorer: fake)
    assert picker.pick(sample_items) is None


def test_picker_empty_input_returns_none():
    picker = FuzzyPicker(view_factory=lambda cfg, scorer: _FakeView(selection_index=0))
    assert picker.pick([]) is None


# --- ReadlineBridge -------------------------------------------------------


def test_strip_ansi_removes_csi_sequences():
    stripped = ReadlineBridge._strip_ansi("\x1b[31mred\x1b[0m_text")
    assert stripped == "red_text"


def test_strip_ansi_passes_through_plain_text():
    assert ReadlineBridge._strip_ansi("plain") == "plain"


# --- Lint-regression: lazyown.py shell strings ---------------------------

import ast  # noqa: E402


def _collect_string_constants(source: str) -> list[str]:
    """Return every string literal value present in ``source`` after parse.

    Walking the AST captures the post-escape byte content of every literal,
    which is exactly what reaches subprocess / shell calls at runtime. The
    helper deliberately ignores f-string format expressions because their
    interpolated values are runtime-dependent; only the static template
    fragments inside ``ast.JoinedStr`` are captured.
    """
    tree = ast.parse(source)
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            found.append(node.value)
        elif isinstance(node, ast.JoinedStr):
            for piece in node.values:
                if isinstance(piece, ast.Constant) and isinstance(piece.value, str):
                    found.append(piece.value)
    return found


_LAZYOWN_SRC = (_ROOT / "lazyown.py").read_text(encoding="utf-8")


def _collect_runtime_strings() -> list[str]:
    """Aggregate string literals from every CLI source the shell may dispatch.

    Returns:
        All string constants found in ``lazyown.py`` plus the migrated
        ``do_*`` modules under ``cli/commands/`` and the C2 builder
        module that hosts the cloudflare tunnel templates. Files that
        cannot be parsed are skipped silently so the test runs on
        partially valid checkouts.
    """

    sources: list[Path] = [_ROOT / "lazyown.py"]
    sources.extend(sorted((_ROOT / "cli" / "commands").glob("*.py")))
    sources.append(_ROOT / "modules" / "c2_builder.py")

    collected: list[str] = []
    for path in sources:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        try:
            collected.extend(_collect_string_constants(text))
        except SyntaxError:
            continue
    return collected


_LAZYOWN_STRINGS = _collect_runtime_strings()


@pytest.mark.parametrize(
    "expected_substring",
    [
        r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer",
        r"reg.exe save hklm\sam C:\sam.save",
        r"reg.exe save hklm\system C:\system.save",
        r"reg.exe save hklm\security C:\security.save",
        r"HKLM\System\CurrentControlSet\Control\TerminalServer",
        r"HKLM:\SYSTEM\CurrentControlSet\Services\ADSync",
        r"C:\Windows\Tasks",
        r"%Program Files%\Windows Defender\MpCmdRun.exe",
        r"C:\Program Files\Microsoft Azure AD Sync\Bin\miiserver.exe",
        r"procdump.exe -accepteula -ma lsass.exe",
        r"C:\windows\system32\comsvcs.dll",
        r"C:\lsass.dmp",
        r"C:\Windows\Temp\system.save",
        r"C:\Windows*",
        r"C:\folder_to_check\|*",
        "find / -type f \\( -iname '*cred*'",
        "Active\\ Directory",
        r"\bDNS:([^\s,]+)",
        r"^.\{",
        r"Perfil\s*:\s",
        r"trycloudflare.com",
        r".\hellbird.ps1",
        r".\pivot.exe",
        r".\z.ps1",
        r"htb\lazyown",
        r"C:\users\grisun0\documents\OpenSSH-Win64-v9.8.1.0.msi",
    ],
)
def test_lazyown_runtime_strings_preserve_shell_payload(expected_substring):
    matched = any(expected_substring in value for value in _LAZYOWN_STRINGS)
    assert matched, (
        f"expected substring not found in any literal after escape cleanup: "
        f"{expected_substring!r}"
    )


def test_lazyown_source_has_no_invalid_escape_warning():
    import warnings
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        compile(_LAZYOWN_SRC, "lazyown.py", "exec")
    syntax_warnings = [w for w in captured if issubclass(w.category, SyntaxWarning)]
    assert syntax_warnings == [], (
        "lazyown.py still emits SyntaxWarning:\n"
        + "\n".join(str(w.message) for w in syntax_warnings)
    )


# --- getprompt smoke test -------------------------------------------------


def test_getprompt_renders_three_lines_and_includes_payload_segments():
    import re

    from cli.banner_config import GlyphRegistry
    from utils import getprompt
    raw = getprompt()
    plain = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", raw)
    lines = plain.splitlines()
    assert len(lines) == 3, plain
    registry = GlyphRegistry()
    assert any(lines[0].startswith(c) for c in registry.choices("top_left")), plain
    assert any(lines[1].startswith(c) for c in registry.choices("vertical")), plain
    assert any(lines[2].startswith(c) for c in registry.choices("bottom_left")), plain
    assert "@" in lines[0]
