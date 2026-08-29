"""TDD tests for the AES key resolution contract.

Contract: ``core.config.resolve_aes_key`` returns a 32-byte key derived
from a configuration value, an existing on-disk key, or a freshly
generated one. The resolved key is exposed on :class:`Config` as
``self.aes_key`` (bytes) and through the legacy ``self.params['aes_key']``
access path (hex string).

Invariants:

1. When ``aes_key`` in the payload is a 64-char hex string, it is decoded
   into 32 bytes and used as-is.
2. When ``aes_key`` is empty/missing, an on-disk key under
   ``sessions/key.aes`` is loaded if present.
3. When neither exists, ``os.urandom(32)`` is generated and persisted
   with mode ``0o600``.
4. An invalid hex string of the wrong length raises ``ValueError``.
5. After ``Config(...)`` is built, ``self.aes_key`` is always 32 bytes.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from core.config import Config, resolve_aes_key


class TestHexSource:
    """A 64-char hex in the payload becomes 32 bytes."""

    def test_valid_hex_decodes_to_32_bytes(self) -> None:
        hex_value = "82e672ae054aa4de6f042c888111686a82e672ae054aa4de6f042c888111686a"
        key = resolve_aes_key({"aes_key": hex_value}, sessions_dir=Path("/tmp/never-used"))
        assert isinstance(key, bytes)
        assert len(key) == 32
        assert key.hex() == hex_value

    def test_wrong_length_raises(self) -> None:
        with pytest.raises(ValueError):
            resolve_aes_key(
                {"aes_key": "abcd"},
                sessions_dir=Path("/tmp/never-used"),
            )

    def test_non_hex_raises(self) -> None:
        with pytest.raises(ValueError):
            resolve_aes_key(
                {"aes_key": "z" * 64},
                sessions_dir=Path("/tmp/never-used"),
            )


class TestDiskSource:
    """An on-disk key is loaded when the payload is empty."""

    def test_existing_disk_key_is_loaded(self, tmp_path: Path) -> None:
        existing = os.urandom(32)
        (tmp_path / "key.aes").write_bytes(existing)
        key = resolve_aes_key({}, sessions_dir=tmp_path)
        assert key == existing


class TestGeneratedSource:
    """A fresh key is generated when nothing else is available."""

    def test_generated_key_is_32_bytes(self, tmp_path: Path) -> None:
        key = resolve_aes_key({}, sessions_dir=tmp_path)
        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_generated_key_is_persisted(self, tmp_path: Path) -> None:
        resolve_aes_key({}, sessions_dir=tmp_path)
        on_disk = (tmp_path / "key.aes").read_bytes()
        assert len(on_disk) == 32
        mode = stat.S_IMODE((tmp_path / "key.aes").stat().st_mode)
        assert mode == 0o600


class TestConfigExposesKey:
    """The resolved key is reachable from :class:`Config`."""

    def test_config_has_aes_key_attribute(self) -> None:
        config = Config({"aes_key": "82e672ae054aa4de6f042c888111686a82e672ae054aa4de6f042c888111686a"})
        assert isinstance(config.aes_key, bytes)
        assert len(config.aes_key) == 32

    def test_config_exposes_params_dict(self) -> None:
        config = Config({"aes_key": "82e672ae054aa4de6f042c888111686a82e672ae054aa4de6f042c888111686a"})
        params = config.as_params()
        assert params["aes_key"] == "82e672ae054aa4de6f042c888111686a82e672ae054aa4de6f042c888111686a"
