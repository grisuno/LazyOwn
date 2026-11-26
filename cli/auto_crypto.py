"""Automatic encryption of sensitive session data on app open/close.

Before this module the operator had to manually run ``lazyenc.py encrypt``
and ``lazyenc.py decrypt`` to protect session data at rest. This module
provides automatic encryption when the application closes and automatic
decryption when an authenticated user opens it.

Scope of protection:
    - ``sessions/credentials_*.txt`` — captured credentials
    - ``sessions/*.pem`` — TLS certificates
    - ``sessions/world_model.json`` — operational state
    - ``sessions/hash*.txt`` — captured hashes

Key material (``key.aes``, ``*.key``, ``.secret_key``) is deliberately
NOT encrypted at rest: sealing a boot-time key with another boot-time
key created a rotation loop that invalidated live beacons and lost
vault credentials. Key files stay owner-only (0600) instead.

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

import logging
import os
import secrets
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

_log = logging.getLogger(__name__)
_UNREADABLE_WARNED: set[str] = set()

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
            "*.pem",
        ]
    )
    password_provider: Callable[[], str | None] | None = None
    legacy_password_provider: Callable[[], str | None] | None = None
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
                try:
                    with open(path, "rb") as fh:
                        header = fh.read(32)
                except OSError:
                    continue
                if header and (header.startswith(b"gAAAAA") or header[:4] == b"\x80\x00\x00\x00"):
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
                    tmp_path = encrypted_path.with_name(f"{encrypted_path.name}.{os.getpid()}.tmp")
                    with open(tmp_path, "wb") as fh:
                        fh.write(encrypted_data)
                    tmp_path.replace(encrypted_path)
                    os.remove(path)
                    encrypted_count += 1
                except OSError as exc:
                    _log.warning("auto_crypto: skipping %s: %s", path, exc)
                    try:
                        tmp_path.unlink(missing_ok=True)  # type: ignore[possibly-undefined]
                    except OSError:
                        pass
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
        legacy_cipher = self._build_legacy_cipher(salt)

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
                            header = fh.read(8)
                        if header.startswith(b"gAAAAA") or header[:4] == b"\x80\x00\x00\x00":
                            encrypted_files.append(path)
                    except OSError:
                        continue

        for path in encrypted_files:
            if path.name == SALT_FILE or path.name == SALT_FILE + ENCRYPTED_SUFFIX:
                continue
            try:
                with open(path, "rb") as fh:
                    encrypted_data = fh.read()
                try:
                    decrypted_data = cipher.decrypt(encrypted_data)
                except InvalidToken:
                    decrypted_data = self._decrypt_legacy(legacy_cipher, encrypted_data, path)
                    if decrypted_data is None:
                        if str(path) not in _UNREADABLE_WARNED:
                            _UNREADABLE_WARNED.add(str(path))
                            _log.warning("auto_crypto: wrong password or corrupt file %s", path)
                        continue
                if path.name.endswith(ENCRYPTED_SUFFIX):
                    original_name = path.name[: -len(ENCRYPTED_SUFFIX)]
                    original_path = sessions / original_name
                else:
                    original_path = path
                tmp_path = Path(f"{original_path}.{os.getpid()}.tmp")
                with open(tmp_path, "wb") as fh:
                    fh.write(decrypted_data)
                tmp_path.replace(original_path)
                if path.name.endswith(ENCRYPTED_SUFFIX):
                    os.remove(path)
                decrypted_count += 1
            except OSError as exc:
                _log.warning("auto_crypto: skipping %s: %s", path, exc)
                continue

        return decrypted_count > 0

    def _build_legacy_cipher(self, salt: bytes):
        """Build a Fernet cipher for the deprecated ``lazyown:<operator>`` key.

        Args:
            salt: The persisted PBKDF2 salt, shared with the primary cipher.

        Returns:
            A ``Fernet`` instance for the legacy key, or ``None`` when no
            legacy provider is configured or it yields no password.
        """
        provider = self._config.legacy_password_provider
        if provider is None:
            return None
        try:
            legacy_password = provider()
        except Exception:
            return None
        if not legacy_password:
            return None
        from cryptography.fernet import Fernet

        return Fernet(self._derive_key(legacy_password, salt))

    def _decrypt_legacy(self, legacy_cipher, encrypted_data: bytes, path: Path) -> bytes | None:
        """Decrypt one file with the legacy cipher, warning once on success.

        Args:
            legacy_cipher: The legacy ``Fernet`` cipher, or ``None``.
            encrypted_data: The ciphertext bytes.
            path: The file being decrypted (for the warning).

        Returns:
            The plaintext bytes when the legacy key matches, else ``None``.
            A successful legacy decryption re-encrypts under the current key on
            the next encryption pass, migrating the file off the old scheme.
        """
        if legacy_cipher is None:
            return None
        from cryptography.fernet import InvalidToken

        try:
            plaintext = legacy_cipher.decrypt(encrypted_data)
        except InvalidToken:
            return None
        _log.warning(
            "auto_crypto: %s was encrypted with the deprecated lazyown:<operator> "
            "scheme; decrypting and migrating to the current key on next save.",
            path,
        )
        return plaintext

    def has_password(self) -> bool:
        """Return True when the configured provider yields a password now.

        Exit paths use this to distinguish "nothing to protect" from
        "no credential available", so a skipped encryption is never
        silent.

        Returns:
            True when a non-empty password is available.
        """
        return bool(self._get_password())

    def _get_password(self) -> str | None:
        provider = self._config.password_provider
        if provider is None:
            return None
        try:
            return provider()
        except Exception:
            return None

    def _load_or_create_salt(self) -> bytes:
        try:
            raw = self._salt_path.read_bytes()
            if len(raw) >= 16:
                return raw[:16]
        except FileNotFoundError:
            pass
        except OSError as exc:
            _log.warning("auto_crypto: cannot read salt: %s", exc)
        salt = secrets.token_bytes(16)
        self._salt_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self._salt_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            try:
                os.write(fd, salt)
            finally:
                os.close(fd)
            return salt
        except FileExistsError:
            try:
                raw = self._salt_path.read_bytes()
                if len(raw) >= 16:
                    return raw[:16]
            except OSError:
                pass
            return salt
        except OSError as exc:
            _log.warning("auto_crypto: cannot write salt: %s", exc)
            return salt

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        from core.crypto import derive_key

        return derive_key(password, salt)


def build_password_provider_from_cli_login(
    sessions_dir: str = DEFAULT_SESSIONS_DIR,
) -> Callable[[], str | None]:
    """Return the at-rest password provider for session encryption.

    Resolution is delegated to :func:`core.crypto.resolve_master_password`:
    ``LAZYOWN_MASTER_PASSWORD`` env, then the OS keyring, then a device-bound
    random secret, then ``None`` (encryption skipped, with an explicit
    warning). The key is never derived from the public operator username; the
    removed ``lazyown:<operator>`` scheme survives only as a read-only legacy
    fallback (see :func:`build_legacy_password_provider`).

    Args:
        sessions_dir: Directory for the device-bound secret.

    Returns:
        A zero-argument callable returning the resolved password or ``None``.
    """

    def _provider() -> str | None:
        from core.crypto import resolve_master_password

        return resolve_master_password(sessions_dir)

    return _provider


def build_legacy_password_provider() -> Callable[[], str | None]:
    """Return a READ-ONLY provider yielding the deprecated ``lazyown:<operator>``.

    Used solely to decrypt files written by the pre-removal predictable scheme;
    such files re-encrypt under the current key on the next encryption pass. It
    must never be configured as the primary provider.

    Returns:
        A zero-argument callable returning ``lazyown:<operator>`` or ``None``.
    """

    def _provider() -> str | None:
        from core.crypto import legacy_master_password

        try:
            from modules.cli_auth import get_current_operator

            return legacy_master_password(get_current_operator())
        except Exception:
            return None

    return _provider


__all__ = [
    "AutoCryptoEngine",
    "AutoCryptoConfig",
    "SALT_FILE",
    "ENCRYPTED_SUFFIX",
    "build_password_provider_from_cli_login",
    "build_legacy_password_provider",
]
