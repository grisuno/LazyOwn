"""Tests for cli.auto_crypto — automatic session data encryption.

Covers:
    - AutoCryptoConfig defaults and overrides
    - AutoCryptoEngine construction
    - Salt generation and key derivation
    - Encrypt/decrypt round-trip
    - is_encrypted detection
    - Graceful no-op when password provider returns None
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def crypto_module():
    from cli.auto_crypto import AutoCryptoConfig, AutoCryptoEngine
    return AutoCryptoConfig, AutoCryptoEngine


@pytest.fixture
def tmp_sessions():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


class TestAutoCryptoConfig:
    def test_default_config(self, crypto_module):
        AutoCryptoConfig = crypto_module[0]
        cfg = AutoCryptoConfig()
        assert cfg.sessions_dir == "sessions"
        assert cfg.auto_enabled is True
        assert len(cfg.protect_globs) > 0
        assert "credentials_*.txt" in cfg.protect_globs

    def test_custom_config(self, crypto_module):
        AutoCryptoConfig = crypto_module[0]
        cfg = AutoCryptoConfig(
            sessions_dir="/tmp/test",
            auto_enabled=False,
            protect_globs=["secrets.txt"],
        )
        assert cfg.sessions_dir == "/tmp/test"
        assert cfg.auto_enabled is False
        assert cfg.protect_globs == ["secrets.txt"]


class TestAutoCryptoEngine:
    def test_disabled_engine_is_noop(self, crypto_module, tmp_sessions):
        AutoCryptoConfig, AutoCryptoEngine = crypto_module
        cfg = AutoCryptoConfig(
            sessions_dir=str(tmp_sessions),
            auto_enabled=False,
        )
        engine = AutoCryptoEngine(cfg)
        assert engine.enabled is False
        assert engine.encrypt_session() is False
        assert engine.decrypt_session() is False

    def test_no_password_provider_returns_false(self, crypto_module, tmp_sessions):
        AutoCryptoConfig, AutoCryptoEngine = crypto_module
        cfg = AutoCryptoConfig(
            sessions_dir=str(tmp_sessions),
            auto_enabled=True,
            password_provider=None,
        )
        engine = AutoCryptoEngine(cfg)
        result = engine.encrypt_session()
        assert result is False

    def test_empty_directory_is_not_encrypted(self, crypto_module, tmp_sessions):
        AutoCryptoConfig, AutoCryptoEngine = crypto_module
        cfg = AutoCryptoConfig(
            sessions_dir=str(tmp_sessions),
            auto_enabled=True,
        )
        engine = AutoCryptoEngine(cfg)
        assert engine.is_encrypted is False

    def test_encrypt_decrypt_roundtrip(self, crypto_module, tmp_sessions):
        AutoCryptoConfig, AutoCryptoEngine = crypto_module
        password = "test-password-123"
        cfg = AutoCryptoConfig(
            sessions_dir=str(tmp_sessions),
            auto_enabled=True,
            password_provider=lambda: password,
        )
        engine = AutoCryptoEngine(cfg)

        secret_file = tmp_sessions / "credentials_test.txt"
        secret_file.write_text("secret_credentials_data")

        key_file = tmp_sessions / "key.aes"
        key_file.write_bytes(b"\x00" * 32)

        encrypted = engine.encrypt_session()
        assert encrypted is True

        assert not secret_file.exists()
        encrypted_secret = tmp_sessions / "credentials_test.txt.encrypted"
        assert encrypted_secret.exists()

        assert not key_file.exists()
        encrypted_key = tmp_sessions / "key.aes.encrypted"
        assert encrypted_key.exists()

        decrypted = engine.decrypt_session()
        assert decrypted is True

        assert secret_file.exists()
        assert secret_file.read_text() == "secret_credentials_data"

        assert key_file.exists()
        assert key_file.read_bytes()[:4] == b"\x00\x00\x00\x00"

    def test_salt_is_persisted(self, crypto_module, tmp_sessions):
        AutoCryptoConfig, AutoCryptoEngine = crypto_module
        from cli.auto_crypto import SALT_FILE

        cfg = AutoCryptoConfig(
            sessions_dir=str(tmp_sessions),
            auto_enabled=True,
            password_provider=lambda: "password",
        )
        engine = AutoCryptoEngine(cfg)

        secret = tmp_sessions / "creds.txt"
        secret.write_text("data")

        engine.encrypt_session()

        salt_path = tmp_sessions / SALT_FILE
        assert salt_path.exists()
        assert salt_path.read_bytes()
        assert len(salt_path.read_bytes()) >= 16


class TestPasswordProvider:
    def test_build_provider_returns_callable(self):
        from cli.auto_crypto import build_password_provider_from_cli_login
        provider = build_password_provider_from_cli_login()
        assert callable(provider)
