"""Tests for LazyOwnShell._rotate_existing_credentials.

The helper backs up ``sessions/credentials.txt`` before ``createcredentials``
overwrites it. It must tolerate the file vanishing between the existence check
and the rename (a concurrent CLI + daemon writer), an empty or colon-less first
line, and rename failures, instead of raising ``FileNotFoundError`` and
aborting the command as it did before.

The method does not use ``self``, so it is exercised as an unbound function with
``None`` as the instance to avoid the cost of constructing the full shell.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import lazyown  # noqa: E402

_rotate = lazyown.LazyOwnShell._rotate_existing_credentials


@pytest.fixture
def in_tmp_sessions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "sessions").mkdir()
    return tmp_path


def test_missing_file_returns_none(in_tmp_sessions):
    assert _rotate(None, "sessions/credentials.txt") is None


def test_existing_file_is_backed_up_by_username(in_tmp_sessions):
    src = in_tmp_sessions / "sessions" / "credentials.txt"
    src.write_text("alice:secret\n", encoding="utf-8")
    result = _rotate(None, "sessions/credentials.txt")
    assert result == "sessions/credentials_alice.txt"
    assert not src.exists()
    assert (in_tmp_sessions / "sessions" / "credentials_alice.txt").exists()


def test_empty_file_uses_fallback_username(in_tmp_sessions):
    src = in_tmp_sessions / "sessions" / "credentials.txt"
    src.write_text("", encoding="utf-8")
    result = _rotate(None, "sessions/credentials.txt")
    assert result == "sessions/credentials_previous.txt"


def test_line_without_colon_uses_whole_token(in_tmp_sessions):
    src = in_tmp_sessions / "sessions" / "credentials.txt"
    src.write_text("justauser\n", encoding="utf-8")
    result = _rotate(None, "sessions/credentials.txt")
    assert result == "sessions/credentials_justauser.txt"


def test_race_on_rename_is_swallowed(in_tmp_sessions, monkeypatch):
    src = in_tmp_sessions / "sessions" / "credentials.txt"
    src.write_text("bob:pw\n", encoding="utf-8")

    def _boom(*_args, **_kwargs):
        raise FileNotFoundError(2, "No such file or directory")

    monkeypatch.setattr(os, "rename", _boom)
    assert _rotate(None, "sessions/credentials.txt") is None


def test_oserror_on_rename_is_swallowed(in_tmp_sessions, monkeypatch):
    src = in_tmp_sessions / "sessions" / "credentials.txt"
    src.write_text("bob:pw\n", encoding="utf-8")

    def _boom(*_args, **_kwargs):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(os, "rename", _boom)
    assert _rotate(None, "sessions/credentials.txt") is None
