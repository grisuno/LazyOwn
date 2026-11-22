"""Tests for the auto-crypto at-rest key resolution hardening.

The predictable ``lazyown:<operator>`` key derivation was removed from the
write path. These tests pin the replacement contract:

    - the primary resolver never returns a key derived from a public value;
    - resolution is env -> OS keyring -> device-bound random secret -> None;
    - the device secret is random, mode 0o600, and rejected if world-writable;
    - old files encrypted with the legacy scheme still decrypt (read compat);
    - encrypt/decrypt round-trips both with and without a master password.
"""

from __future__ import annotations

import os
import secrets
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def tmp_sessions():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture(autouse=True)
def _no_keyring_no_env(monkeypatch):
    """Isolate tests from the host env var and any installed keyring backend."""
    monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
    monkeypatch.setattr("core.crypto._keyring_secret", lambda create=True: None)


class TestMachineSecret:
    def test_creates_random_secret_mode_600(self, tmp_sessions):
        from core.crypto import STATE_SECRET_FILE, machine_secret

        value = machine_secret(tmp_sessions)
        assert value and len(value) >= 32
        path = tmp_sessions / STATE_SECRET_FILE
        assert oct(path.stat().st_mode & 0o777) == "0o600"

    def test_is_persistent_and_stable(self, tmp_sessions):
        from core.crypto import machine_secret

        first = machine_secret(tmp_sessions)
        assert machine_secret(tmp_sessions) == first

    def test_rejects_world_writable_secret(self, tmp_sessions):
        from core.crypto import STATE_SECRET_FILE, machine_secret

        machine_secret(tmp_sessions)
        os.chmod(tmp_sessions / STATE_SECRET_FILE, 0o666)
        assert machine_secret(tmp_sessions) is None

    def test_no_create_returns_none_when_absent(self, tmp_sessions):
        from core.crypto import machine_secret

        assert machine_secret(tmp_sessions, create=False) is None


class TestResolveMasterPassword:
    def test_env_wins(self, tmp_sessions, monkeypatch):
        from core.crypto import resolve_master_password

        monkeypatch.setenv("LAZYOWN_MASTER_PASSWORD", "topsecret")
        assert resolve_master_password(tmp_sessions) == "topsecret"

    def test_device_fallback(self, tmp_sessions):
        from core.crypto import resolve_master_password

        value = resolve_master_password(tmp_sessions)
        assert value and not value.startswith("lazyown:")

    def test_none_when_everything_disabled(self, tmp_sessions):
        from core.crypto import resolve_master_password

        assert resolve_master_password(tmp_sessions, allow_keyring=False, allow_device=False) is None


class TestLegacyKeyHelper:
    def test_legacy_master_password(self):
        from core.crypto import legacy_master_password

        assert legacy_master_password("bob") == "lazyown:bob"
        assert legacy_master_password(None) is None
        assert legacy_master_password("") is None


class TestProvidersNeverPredictable:
    def test_primary_provider_ignores_operator(self, tmp_sessions, monkeypatch):
        import modules.cli_auth as cli_auth
        from cli.auto_crypto import build_password_provider_from_cli_login

        monkeypatch.setattr(cli_auth, "get_current_operator", lambda: "alice", raising=False)
        password = build_password_provider_from_cli_login(sessions_dir=str(tmp_sessions))()
        assert password is not None
        assert password != "lazyown:alice"
        assert not password.startswith("lazyown:")

    def test_legacy_provider_is_read_only_predictable(self, monkeypatch):
        import modules.cli_auth as cli_auth
        from cli.auto_crypto import build_legacy_password_provider

        monkeypatch.setattr(cli_auth, "get_current_operator", lambda: "alice", raising=False)
        assert build_legacy_password_provider()() == "lazyown:alice"


class TestRoundTrips:
    def _engine(self, tmp_sessions, provider, legacy=None):
        from cli.auto_crypto import AutoCryptoConfig, AutoCryptoEngine

        return AutoCryptoEngine(
            AutoCryptoConfig(
                sessions_dir=str(tmp_sessions),
                password_provider=provider,
                legacy_password_provider=legacy,
            )
        )

    def test_roundtrip_with_master_password(self, tmp_sessions, monkeypatch):
        monkeypatch.setenv("LAZYOWN_MASTER_PASSWORD", "env-master")
        from cli.auto_crypto import build_password_provider_from_cli_login

        (tmp_sessions / "credentials_a.txt").write_text("admin:hunter2")
        engine = self._engine(tmp_sessions, build_password_provider_from_cli_login(str(tmp_sessions)))
        assert engine.encrypt_session() is True
        assert not (tmp_sessions / "credentials_a.txt").exists()
        assert engine.decrypt_session() is True
        assert (tmp_sessions / "credentials_a.txt").read_text() == "admin:hunter2"

    def test_roundtrip_without_master_password_uses_device(self, tmp_sessions):
        from cli.auto_crypto import build_password_provider_from_cli_login

        provider = build_password_provider_from_cli_login(str(tmp_sessions))
        assert not provider().startswith("lazyown:")
        (tmp_sessions / "hash1.txt").write_text("deadbeef")
        engine = self._engine(tmp_sessions, provider)
        assert engine.encrypt_session() is True
        assert engine.decrypt_session() is True
        assert (tmp_sessions / "hash1.txt").read_text() == "deadbeef"

    def test_legacy_encrypted_file_still_decrypts(self, tmp_sessions):
        from cryptography.fernet import Fernet

        from cli.auto_crypto import ENCRYPTED_SUFFIX, SALT_FILE
        from core.crypto import derive_key

        salt = secrets.token_bytes(16)
        (tmp_sessions / SALT_FILE).write_bytes(salt)
        legacy_cipher = Fernet(derive_key("lazyown:alice", salt))
        token = legacy_cipher.encrypt(b"admin:legacy-pass")
        (tmp_sessions / f"credentials_old.txt{ENCRYPTED_SUFFIX}").write_bytes(token)

        engine = self._engine(
            tmp_sessions,
            provider=lambda: "a-different-current-key",
            legacy=lambda: "lazyown:alice",
        )
        assert engine.decrypt_session() is True
        assert (tmp_sessions / "credentials_old.txt").read_bytes() == b"admin:legacy-pass"
