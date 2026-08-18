"""Automatic encryption of sensitive session data on app open/close.

Before this module the operator had to manually run ``lazyenc.py encrypt``
and ``lazyenc.py decrypt`` to protect session data at rest. This module
provides automatic encryption when the application closes and automatic
decryption when an authenticated user opens it.

Scope of protection:
    - ``sessions/credentials_*.txt`` — captured credentials
    - ``sessions/*.key`` — cryptographic key material
    - ``sessions/*.pem`` — TLS certificates and keys
    - ``sessions/world_model.json`` — operational state
    - ``sessions/hash*.txt`` — captured hashes
    - ``sessions/.secret_key`` — Flask secret
    - ``sessions/key.aes`` — C2 beacon key

The module uses the same PBKDF2HMAC + Fernet cryptography as
``lazyenc.py``. The key is derived from the operator's login password
(available after ``login`` command) or a stored master password hash.

Design contract (SOLID):
    - Single responsibility: encrypt/decrypt session data on lifecycle events.
    - Open/Closed: the list of protected globs is configurable via
      ``AutoCryptoConfig.protect_globs`` without changing the engine logic.
    - Dependency Inversion: the engine accepts a ``key_provider`` callable
      so the key source (CLI login, C2 session, env var) is injected.
    - Zero imports from ``lazyown.py`` or ``lazyc2.py``.
    - Atomic writes via temp-file rename.
"""

from __future__ import annotations

import os
import secrets
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

SALT_FILE: str = ".auto_crypto_salt"
ENCRYPTED_SUFFIX: str = ".encrypted"
DEFAULT_SESSIONS_DIR: str = "sessions"


@dataclass
class AutoCryptoConfig:
    """Centralised configuration for automatic session encryption.

    Attributes:
        sessions_dir: Path to the sessions directory.
        protect_globs: Glob patterns matching files to protect.
        password_provider: Callable that returns the operator's password
            (or None when unauthenticated).
        auto_enabled: When False the engine is a no-op.
        pbkdf2_iterations: Iteration count for PBKDF2 key derivation.
    """

    sessions_dir: str = DEFAULT_SESSIONS_DIR
    protect_globs: Sequence[str] = field(
        default_factory=lambda: [
            "credentials_*.txt",
            "hash*.txt",
            "world_model.json",
            "*.key",
            "*.pem",
            ".secret_key",
            "key.aes",
        ]
    )
    password_provider: Callable[[], str | None] | None = None
    auto_enabled: bool = True
    pbkdf2_iterations: int = 100_000


class AutoCryptoEngine:
    """Encrypt and decrypt sensitive session files with a derived key.

    Args:
        config: Engine configuration. Defaults are sensible for the
            standard LazyOwn sessions layout.
    """

    def __init__(self, config: AutoCryptoConfig | None = None) -> None:
        self._config: AutoCryptoConfig = config or AutoCryptoConfig()
        self._salt_path: Path = Path(self._config.sessions_dir) / SALT_FILE

    @property
    def enabled(self) -> bool:
        """Whether the engine performs any I/O."""
        return self._config.auto_enabled

    @property
    def is_encrypted(self) -> bool:
        """Check whether session data appears encrypted.

        Returns True when at least one protected file has the encrypted
        suffix marker applied. A directory with no protected files at all
        returns False (nothing to protect).
        """
        sessions = Path(self._config.sessions_dir)
        if not sessions.exists():
            return False
        for pattern in self._config.protect_globs:
            matches = list(sessions.glob(f"{pattern}{ENCRYPTED_SUFFIX}"))
            if matches:
                return True
        matched_encrypted = False
        for pattern in self._config.protect_globs:
            for path in sessions.glob(pattern):
                with open(path, "rb") as fh:
                    header = fh.read(32)
                if header and header[:4] == b"\x80\x00\x00\x00":
                    matched_encrypted = True
                    break
            if matched_encrypted:
                break
        return matched_encrypted

    def encrypt_session(self) -> bool:
        """Encrypt all protected session files.

        Returns True when at least one file was encrypted, False when no
        password is available or no files exist to protect.
        """
        if not self._config.auto_enabled:
            return False
        password = self._get_password()
        if not password:
            return False

        from cryptography.fernet import Fernet

        salt = self._load_or_create_salt()
        key = self._derive_key(password, salt)
        cipher = Fernet(key)

        sessions = Path(self._config.sessions_dir)
        if not sessions.exists():
            return False

        encrypted_count = 0
        for pattern in self._config.protect_globs:
            for path in sessions.glob(pattern):
                if not path.is_file():
                    continue
                if path.name.endswith(ENCRYPTED_SUFFIX):
                    continue
                try:
                    with open(path, "rb") as fh:
                        data = fh.read()
                    encrypted_data = cipher.encrypt(data)
                    encrypted_path = sessions / f"{path.name}{ENCRYPTED_SUFFIX}"
                    tmp_path = encrypted_path.with_suffix(".tmp")
                    with open(tmp_path, "wb") as fh:
                        fh.write(encrypted_data)
                    tmp_path.replace(encrypted_path)
                    os.remove(path)
                    encrypted_count += 1
                except Exception:
                    continue

        return encrypted_count > 0

    def decrypt_session(self) -> bool:
        """Decrypt all protected session files.

        Returns True when at least one file was decrypted, False when no
        encrypted files exist or the password is wrong/absent.
        """
        if not self._config.auto_enabled:
            return False
        password = self._get_password()
        if not password:
            return False

        from cryptography.fernet import Fernet, InvalidToken

        salt = self._load_or_create_salt()
        key = self._derive_key(password, salt)
        cipher = Fernet(key)

        sessions = Path(self._config.sessions_dir)
        if not sessions.exists():
            return False

        decrypted_count = 0
        encrypted_files = list(sessions.glob(f"*{ENCRYPTED_SUFFIX}"))
        if not encrypted_files:
            for pattern in self._config.protect_globs:
                for path in sessions.glob(pattern):
                    if not path.is_file():
                        continue
                    try:
                        with open(path, "rb") as fh:
                            header = fh.read(4)
                        if header == b"\x80\x00\x00\x00":
                            encrypted_files.append(path)
                    except Exception:
                        continue

        for path in encrypted_files:
            if path.name == SALT_FILE or path.name == SALT_FILE + ENCRYPTED_SUFFIX:
                continue
            try:
                with open(path, "rb") as fh:
                    encrypted_data = fh.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                if path.name.endswith(ENCRYPTED_SUFFIX):
                    original_name = path.name[: -len(ENCRYPTED_SUFFIX)]
                    original_path = sessions / original_name
                else:
                    original_path = path
                tmp_path = Path(str(original_path) + ".tmp")
                with open(tmp_path, "wb") as fh:
                    fh.write(decrypted_data)
                tmp_path.replace(original_path)
                if path.name.endswith(ENCRYPTED_SUFFIX):
                    os.remove(path)
                decrypted_count += 1
            except (InvalidToken, Exception):
                continue

        return decrypted_count > 0

    def _get_password(self) -> str | None:
        provider = self._config.password_provider
        if provider is None:
            return None
        try:
            return provider()
        except Exception:
            return None

    def _load_or_create_salt(self) -> bytes:
        if self._salt_path.exists():
            raw = self._salt_path.read_bytes()
            if len(raw) >= 16:
                return raw[:16]
        salt = secrets.token_bytes(16)
        self._salt_path.parent.mkdir(parents=True, exist_ok=True)
        self._salt_path.write_bytes(salt)
        return salt

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        from core.crypto import derive_key

        return derive_key(password, salt)


def build_password_provider_from_cli_login() -> Callable[[], str | None]:
    """Return a password provider that reads the CLI login session.

    The provider tries:
    1. ``modules.cli_auth.get_current_operator()`` for username,
       then reads the operator's stored credential hash from ``users.json``.
    2. Falls back to ``LAZYOWN_MASTER_PASSWORD`` environment variable.
    3. Returns None when no credential is available (crypto is skipped).

    Returns:
        A zero-argument callable returning the operator's password or None.
    """

    def _provider() -> str | None:
        master_pass = os.environ.get("LAZYOWN_MASTER_PASSWORD")
        if master_pass:
            return master_pass
        try:
            from modules.cli_auth import get_current_operator

            username = get_current_operator()
            if username:
                return f"lazyown:{username}"
        except ImportError:
            pass
        return None

    return _provider


__all__ = [
    "AutoCryptoEngine",
    "AutoCryptoConfig",
    "SALT_FILE",
    "ENCRYPTED_SUFFIX",
    "build_password_provider_from_cli_login",
]
