"""Backdoor credentials: random like C2 operators, persisted via assign."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.commands.persist_migrated import PersistMigratedCommandSet  # noqa: E402

_FORBIDDEN = set(";|&$()`{}!><*?~#\\'\"\n\r \t:")


def test_username_shape_and_uniqueness() -> None:
    """Usernames look like C2 operators and never repeat."""
    first = PersistMigratedCommandSet.generate_backdoor_username()
    second = PersistMigratedCommandSet.generate_backdoor_username()
    assert first.startswith("operator_") and len(first) == len("operator_") + 8
    assert first != second


def test_password_assign_and_shell_safe() -> None:
    """Passwords survive apply_assign, chpasswd, and single quotes."""
    for _ in range(25):
        password = PersistMigratedCommandSet.generate_backdoor_password()
        assert len(password) == 20
        assert not (set(password) & _FORBIDDEN), password


def test_resolve_keeps_configured() -> None:
    """Configured credentials pass through untouched."""
    params = {"backdoor_username": "svc_acct", "backdoor_password": "s3cret-long-enough"}
    assert PersistMigratedCommandSet.resolve_backdoor_creds(params) == ("svc_acct", "s3cret-long-enough")


def test_resolve_generates_on_placeholders() -> None:
    """CHANGE_ME, empty, or missing keys all trigger generation."""
    for params in (
        {"backdoor_username": "CHANGE_ME", "backdoor_password": "CHANGE_ME"},
        {"backdoor_username": "", "backdoor_password": ""},
        {},
    ):
        username, password = PersistMigratedCommandSet.resolve_backdoor_creds(params)
        assert username.startswith("operator_") and len(password) == 20


def test_ensure_persists_once_then_reuses(monkeypatch) -> None:
    """First call generates + saves; second call reuses without saving."""
    saved: list = []
    monkeypatch.setattr(
        "cli.commands.persist_migrated.save_payload",
        lambda params: saved.append(dict(params)),
    )
    stub = SimpleNamespace(params={"backdoor_username": "CHANGE_ME", "backdoor_password": "CHANGE_ME"})
    stub.resolve_backdoor_creds = PersistMigratedCommandSet.resolve_backdoor_creds
    stub.generate_backdoor_username = PersistMigratedCommandSet.generate_backdoor_username
    stub.generate_backdoor_password = PersistMigratedCommandSet.generate_backdoor_password
    first = PersistMigratedCommandSet._ensure_backdoor_creds(stub)
    assert first is not None and len(saved) == 2
    assert stub.params["backdoor_username"] == first[0]
    assert stub.params["backdoor_password"] == first[1]
    second = PersistMigratedCommandSet._ensure_backdoor_creds(stub)
    assert second == first and len(saved) == 2
