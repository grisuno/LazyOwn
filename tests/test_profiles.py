"""Tests for runtime install profiles (``core.profiles``).

Covers profile resolution from ``LAZYOWN_PROFILE``, dependency-spec
filtering per profile, the invalid-value contract, and lock-file
consistency between ``requirements-light.txt`` and ``requirements.txt``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.profiles import (
    LIGHT_SKIPPED_IMPORTS,
    PROFILE_FULL,
    PROFILE_LIGHT,
    active_profile,
    is_light,
    specs_for_profile,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class _Spec:
    def __init__(self, import_name: str) -> None:
        self.import_name = import_name


def test_default_profile_is_full(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LAZYOWN_PROFILE", raising=False)
    assert active_profile() == PROFILE_FULL
    assert not is_light()


def test_light_profile_selected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LAZYOWN_PROFILE", "light")
    assert active_profile() == PROFILE_LIGHT
    assert is_light()


def test_profile_value_is_case_insensitive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LAZYOWN_PROFILE", "  LIGHT ")
    assert active_profile() == PROFILE_LIGHT


def test_unknown_profile_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LAZYOWN_PROFILE", "medium")
    with pytest.raises(ValueError, match="LAZYOWN_PROFILE"):
        active_profile()


def test_full_profile_keeps_every_spec(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LAZYOWN_PROFILE", raising=False)
    specs = [_Spec("cmd2"), _Spec("pandas"), _Spec("groq")]
    assert [s.import_name for s in specs_for_profile(specs)] == ["cmd2", "pandas", "groq"]


def test_light_profile_skips_analytics_and_ai(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LAZYOWN_PROFILE", "light")
    specs = [_Spec("cmd2"), _Spec("pandas"), _Spec("pyarrow"), _Spec("networkx"), _Spec("groq")]
    kept = [s.import_name for s in specs_for_profile(specs)]
    assert kept == ["cmd2"]
    assert LIGHT_SKIPPED_IMPORTS == {"pandas", "pyarrow", "networkx", "groq"}


def _pinned_names(path: Path) -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "==" in line and not line.startswith("#"):
            name, _, version = line.partition("==")
            pins[name.strip().lower()] = version.strip()
    return pins


def test_light_lock_is_a_subset_of_full_lock() -> None:
    full = _pinned_names(REPO_ROOT / "requirements.txt")
    light = _pinned_names(REPO_ROOT / "requirements-light.txt")
    assert light, "light lock must pin at least one distribution"
    for name, version in light.items():
        assert name in full, f"{name} pinned in light lock but missing from full lock"
        assert full[name] == version, f"{name} version drift between locks"


def test_light_lock_drops_analytics_and_ai() -> None:
    light = _pinned_names(REPO_ROOT / "requirements-light.txt")
    for name in ("pandas", "pyarrow", "networkx", "groq", "seaborn"):
        assert name not in light, f"{name} must not be pinned in the light lock"
