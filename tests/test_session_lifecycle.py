"""Tests for the extracted session crypto + lifecycle mixin."""

from __future__ import annotations

import cli.session_lifecycle as lifecycle
from cli.session_lifecycle import SessionLifecycleMixin


class _StubCrypto:
    """Scriptable AutoCryptoEngine stand-in."""

    def __init__(self, enabled=True, has_password=True, decrypted=True, encrypted=True):
        self.enabled = enabled
        self._has_password = has_password
        self._decrypted = decrypted
        self._encrypted = encrypted
        self.calls: list = []

    def has_password(self):
        return self._has_password

    def decrypt_session(self):
        self.calls.append("decrypt")
        return self._decrypted

    def encrypt_session(self):
        self.calls.append("encrypt")
        return self._encrypted


class _StubShell(SessionLifecycleMixin):
    """Minimal host exposing only the crypto handle the mixin reads."""

    def __init__(self, crypto=None):
        self._auto_crypto = crypto


def test_decrypt_runs_when_enabled():
    """Given an enabled engine, When decrypting, Then the session decrypts."""
    crypto = _StubCrypto()
    _StubShell(crypto)._run_auto_decrypt()
    assert crypto.calls == ["decrypt"]


def test_decrypt_noop_when_disabled():
    """Given a disabled engine, When decrypting, Then nothing runs."""
    crypto = _StubCrypto(enabled=False)
    _StubShell(crypto)._run_auto_decrypt()
    assert crypto.calls == []


def test_decrypt_without_engine_is_noop():
    """Given no engine, When decrypting, Then nothing raises."""
    _StubShell(None)._run_auto_decrypt()


def test_encrypt_runs_when_password_present():
    """Given a password, When encrypting, Then the session encrypts."""
    crypto = _StubCrypto()
    _StubShell(crypto)._run_auto_encrypt()
    assert crypto.calls == ["encrypt"]


def test_encrypt_skipped_without_password():
    """Given no password, When encrypting, Then encryption is skipped."""
    crypto = _StubCrypto(has_password=False)
    _StubShell(crypto)._run_auto_encrypt()
    assert crypto.calls == []


def test_gym_cleanup_skipped_when_autonomous(monkeypatch):
    """Given LAZYOWN_AUTONOMOUS=1, When cleaning up, Then no teardown runs."""
    monkeypatch.setenv("LAZYOWN_AUTONOMOUS", "1")
    called: list = []
    monkeypatch.setattr(
        "modules.gym_cleanup.cleanup_gym_machines",
        lambda **kwargs: called.append(kwargs),
    )
    _StubShell()._run_gym_cleanup()
    assert called == []


def test_gym_cleanup_skipped_for_command_and_chain_runs(monkeypatch):
    """Given a -c / --run-chain startup, When cleaning up, Then no teardown runs."""
    monkeypatch.delenv("LAZYOWN_AUTONOMOUS", raising=False)
    monkeypatch.setattr(lifecycle.startup_ns, "command", "ping", raising=False)
    monkeypatch.setattr(lifecycle.startup_ns, "run_chain", "", raising=False)
    called: list = []
    monkeypatch.setattr(
        "modules.gym_cleanup.cleanup_gym_machines",
        lambda **kwargs: called.append(kwargs),
    )
    _StubShell()._run_gym_cleanup()
    assert called == []


def test_gym_cleanup_runs_for_interactive_shell(monkeypatch):
    """Given an interactive shell, When cleaning up, Then teardown runs once."""
    monkeypatch.delenv("LAZYOWN_AUTONOMOUS", raising=False)
    monkeypatch.setattr(lifecycle.startup_ns, "command", "", raising=False)
    monkeypatch.setattr(lifecycle.startup_ns, "run_chain", "", raising=False)
    called: list = []
    monkeypatch.setattr(
        "modules.gym_cleanup.cleanup_gym_machines",
        lambda **kwargs: called.append(kwargs),
    )
    _StubShell()._run_gym_cleanup()
    assert called == [{"verbose": True}]
