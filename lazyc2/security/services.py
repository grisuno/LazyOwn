"""Security services for the LazyOwn C2 web layer.

Services encapsulate stateful security operations such as safe file
handling, secret generation, and content sanitization.
"""

import os
import secrets
from pathlib import Path

from lazyc2.security.constants import (
    AES_KEY_SIZE_BYTES,
    FILE_PERMISSION_OWNER_RW,
    DIR_PERMISSION_OWNER_RWX,
    SESSIONS_DIR_NAME,
    MAX_UPLOAD_SIZE_BYTES,
)
from lazyc2.security.validators import validate_file_path_within_base, validate_aes_key


class SecretKeyManager:
    """Manages the Flask secret key lifecycle.

    Generates a cryptographically secure secret key on first boot and
    persists it to disk with restrictive permissions. Subsequent boots
    load the persisted key. No fallback secrets are permitted.
    """

    KEY_FILENAME = '.secret_key'
    KEY_SIZE_BYTES = 64

    def __init__(self, sessions_dir: Path):
        self._key_file = sessions_dir / self.KEY_FILENAME

    def get_or_create(self) -> str:
        """Return an existing secret key or generate and persist a new one.

        Returns:
            A hex-encoded secret key string.

        Raises:
            RuntimeError: If the key file exists but cannot be read.
        """
        if self._key_file.exists():
            try:
                key = self._key_file.read_text(encoding='utf-8').strip()
                if len(key) >= self.KEY_SIZE_BYTES * 2:
                    return key
            except OSError as exc:
                raise RuntimeError(f"Cannot read secret key file: {exc}") from exc

        key = secrets.token_hex(self.KEY_SIZE_BYTES)
        self._key_file.write_text(key, encoding='utf-8')
        os.chmod(self._key_file, FILE_PERMISSION_OWNER_RW)
        return key


class SafeFileService:
    """Provides safe file read/write operations with path traversal protection.

    All paths are resolved canonically and verified to be within the
    configured base directory before any I/O occurs.
    """

    def __init__(self, base_dir: Path):
        self._base_dir = base_dir.resolve()
        if not self._base_dir.is_dir():
            raise ValueError(f"Base directory does not exist: {base_dir}")

    def _resolve_safe(self, relative_path: str) -> Path:
        """Resolve a relative path safely within the base directory.

        Args:
            relative_path: A relative path string.

        Returns:
            The resolved Path object.

        Raises:
            PermissionError: If the resolved path escapes the base directory.
        """
        candidate = self._base_dir / relative_path
        is_valid, error = validate_file_path_within_base(candidate, self._base_dir)
        if not is_valid:
            raise PermissionError(error)
        return candidate

    def read_bytes(self, relative_path: str) -> bytes:
        """Read a file as bytes after path validation.

        Args:
            relative_path: Relative path within the base directory.

        Returns:
            File contents as bytes.

        Raises:
            PermissionError: If path traversal is detected.
            FileNotFoundError: If the file does not exist.
        """
        safe_path = self._resolve_safe(relative_path)
        return safe_path.read_bytes()

    def read_text(self, relative_path: str, encoding: str = 'utf-8') -> str:
        """Read a file as text after path validation.

        Args:
            relative_path: Relative path within the base directory.
            encoding: Text encoding to use.

        Returns:
            File contents as string.

        Raises:
            PermissionError: If path traversal is detected.
            FileNotFoundError: If the file does not exist.
        """
        safe_path = self._resolve_safe(relative_path)
        return safe_path.read_text(encoding=encoding)

    def write_bytes(self, relative_path: str, data: bytes) -> None:
        """Write bytes to a file after path validation.

        Creates parent directories if needed.

        Args:
            relative_path: Relative path within the base directory.
            data: Bytes to write.

        Raises:
            PermissionError: If path traversal is detected.
        """
        safe_path = self._resolve_safe(relative_path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_bytes(data)
        os.chmod(safe_path, FILE_PERMISSION_OWNER_RW)

    def exists(self, relative_path: str) -> bool:
        """Check if a path exists after validation.

        Args:
            relative_path: Relative path within the base directory.

        Returns:
            True if the path exists, False otherwise.

        Raises:
            PermissionError: If path traversal is detected.
        """
        safe_path = self._resolve_safe(relative_path)
        return safe_path.exists()


class AESKeyManager:
    """Manages AES key generation and validation.

    Ensures keys are exactly the required size for AES-256-CFB.
    """

    def __init__(self, key_file: Path):
        self._key_file = key_file

    def get_or_generate(self) -> bytes:
        """Return an existing AES key or generate a new one.

        Returns:
            A 32-byte AES key.

        Raises:
            ValueError: If an existing key has an invalid length.
        """
        if self._key_file.exists():
            key = self._key_file.read_bytes()
            is_valid, error = validate_aes_key(key)
            if not is_valid:
                raise ValueError(error)
            return key

        key = os.urandom(AES_KEY_SIZE_BYTES)
        self._key_file.write_bytes(key)
        os.chmod(self._key_file, FILE_PERMISSION_OWNER_RW)
        return key


class UploadSizeValidator:
    """Validates upload size constraints.

    Stateless service that checks content length against configured limits.
    """

    def __init__(self, max_size_bytes: int = MAX_UPLOAD_SIZE_BYTES):
        self._max_size = max_size_bytes

    def validate(self, content_length: int | None) -> None:
        """Validate upload size.

        Args:
            content_length: The content length header value.

        Raises:
            ValueError: If the content length exceeds the maximum.
        """
        if content_length is not None and content_length > self._max_size:
            raise ValueError(
                f"Upload size {content_length} exceeds maximum {self._max_size}"
            )
