"""Multi-target loop entry: scope-file parsing, validation and caps."""

from __future__ import annotations

import pytest

from modules.lazy_runner import load_targets_file, parse_loop_line


def test_parse_loop_line_accepts_targets_file(tmp_path):
    """Given a scope file flag, When parsed, Then the config carries it."""
    scope = tmp_path / "scope.txt"
    scope.write_text("10.10.10.5\n10.10.10.7\n", encoding="utf-8")
    config = parse_loop_line(f'--targets-from-file {scope} --max-concurrent 2 "gain access"')
    assert config.targets_file == str(scope)
    assert config.max_concurrent == 2
    assert config.goal == "gain access"


def test_parse_loop_line_defaults_without_file():
    """Given a plain goal, When parsed, Then multi-target knobs stay unset."""
    config = parse_loop_line("plain goal")
    assert config.targets_file == ""
    assert config.max_concurrent == 0


def test_load_targets_file_skips_comments_and_invalid(tmp_path):
    """Given a mixed scope file, When loaded, Then comments, blanks and
    invalid dotted quads are dropped and dedupe applies."""
    scope = tmp_path / "scope.txt"
    scope.write_text(
        "# authorized only\n10.10.10.5\n\n999.999.1.1\n10.10.10.5\nexample.lab\n",
        encoding="utf-8",
    )
    assert load_targets_file(str(scope)) == ["10.10.10.5", "example.lab"]


def test_load_targets_file_caps_batch(tmp_path):
    """Given more targets than the cap, When loaded, Then the count is
    capped and the excess warned."""
    scope = tmp_path / "scope.txt"
    scope.write_text("\n".join(f"10.0.{block}.1" for block in range(30)), encoding="utf-8")
    assert len(load_targets_file(str(scope))) == 16


def test_load_targets_file_missing_raises(tmp_path):
    """Given a missing file, When loaded, Then ValueError carries the path."""
    with pytest.raises(ValueError, match="targets file not found"):
        load_targets_file(str(tmp_path / "nope.txt"))


def test_load_targets_file_empty_raises(tmp_path):
    """Given a file with comments only, When loaded, Then ValueError."""
    scope = tmp_path / "scope.txt"
    scope.write_text("# nothing here\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no valid targets"):
        load_targets_file(str(scope))
