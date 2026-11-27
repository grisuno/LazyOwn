"""Secret storage, sealing and credential environment handling.

Owner-only file modes, Fernet sealing backed by the shared AES key
resolver, encryption-key requirements and the sshpass ``-e`` environment
contract live here so credential flows have one auditable home.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from core.errors import SecurityViolation

log = logging.getLogger("core.secrets")

SECRET_FILE_MODE = 0o600
SECRET_DIR_MODE = 0o700
MAX_SSH_COMMAND_LENGTH = 4096

SEALED_SECRET_PREFIX = "enc:v2:"


def require_encryption_key(
    env_key: str = "LAZYOWN_SECRET_KEY",
    secret_file: Path | None = None,
) -> str:
    """Require a proper encryption key; never fall back to a static default.

    Args:
        env_key: Environment variable name for the secret key.
        secret_file: Optional path to a file containing the key.

    Returns:
        The encryption key string.

    Raises:
        SecurityViolation: If no key is configured.
    """
    secret = os.environ.get(env_key, "")
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def build_sshpass_command(
    password: str,
    ssh_args: list[str],
    *,
    max_password_length: int = 256,
) -> list[str]:
    """Build an sshpass command using SSHPASS env var (sshpass -e).

    Never uses sshpass -p which exposes passwords in process listings.

    Args:
        password: The SSH password to use.
        ssh_args: Arguments to pass to ssh/scp after sshpass.
        max_password_length: Maximum allowed password length.

    Returns:
        List of command arguments suitable for subprocess.run.

    Raises:
        SecurityViolation: If password exceeds max_password_length or
            contains characters that could break the env var.
    """
    if len(password) > max_password_length:
        raise SecurityViolation("Password exceeds maximum allowed length")
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def set_sshpass_env(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def store_secret_owner_only(path: str | Path, text: str) -> str:
    """Atomically store a secret owner-only (0600, dir 0700).

    Args:
        path: Destination file path.
        text: Secret text to persist.

    Returns:
        Resolved absolute path as string.
    """
    target = Path(path)
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(parent, SECRET_DIR_MODE)
    except OSError:
        pass
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW
    fd = os.open(str(target), flags, SECRET_FILE_MODE)
    try:
        payload = str(text or "").encode("utf-8")
        view = memoryview(payload)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        os.chmod(target, SECRET_FILE_MODE)
    except OSError:
        pass
    return str(target)


def _seal_key(sessions_dir: str | Path = "sessions") -> bytes:
    """Resolve the 32-byte sealing key via the shared AES resolver.

    Args:
        sessions_dir: Directory holding the ``key.aes`` key file.

    Returns:
        Raw 32-byte key material.
    """
    from core.config import resolve_aes_key

    return resolve_aes_key({}, sessions_dir=sessions_dir)


def seal_secret(plaintext: str, *, sessions_dir: str | Path = "sessions") -> str:
    """Seal a secret with Fernet (AES-128-CBC + HMAC) for storage.

    The key comes from the shared ``key.aes`` resolver so sealed values
    round-trip across restarts without new configuration. Sealing never
    degrades to plaintext: a missing key or backend raises, so a caller
    that cannot protect a secret knows instead of writing it bare.

    Args:
        plaintext: Secret to protect.
        sessions_dir: Key directory override (tests).

    Returns:
        ``enc:v2:`` sealed value.

    Raises:
        SecurityViolation: If the key or the cryptography backend is
            unavailable — plaintext is never stored as a fallback.
    """
    text = str(plaintext or "")
    if not text or text.startswith(SEALED_SECRET_PREFIX):
        return text
    try:
        import base64 as _b64

        from cryptography.fernet import Fernet

        raw = _seal_key(sessions_dir)
        token = Fernet(_b64.urlsafe_b64encode(raw)).encrypt(text.encode("utf-8"))
        return SEALED_SECRET_PREFIX + token.decode("ascii")
    except Exception as exc:
        log.error("secret sealing failed; refusing to store plaintext: %s", type(exc).__name__)
        raise SecurityViolation(f"secret sealing unavailable: {type(exc).__name__}") from exc


def unseal_secret(stored: str, *, sessions_dir: str | Path = "sessions") -> str:
    """Reveal a secret stored by :func:`seal_secret` (legacy-compatible).

    Legacy ``enc:v1:`` vault values and plaintext fall back to the
    credential vault / passthrough so existing stores keep working.

    Args:
        stored: Sealed or plaintext value.
        sessions_dir: Key directory override (tests).

    Returns:
        Plaintext secret, or empty string when undecryptable.
    """
    text = str(stored or "")
    if not text:
        return ""
    if text.startswith(SEALED_SECRET_PREFIX):
        try:
            import base64 as _b64

            from cryptography.fernet import Fernet

            raw = _seal_key(sessions_dir)
            return (
                Fernet(_b64.urlsafe_b64encode(raw))
                .decrypt(text[len(SEALED_SECRET_PREFIX) :].encode("ascii"))
                .decode("utf-8")
            )
        except Exception:
            return ""
    try:
        from core.credential_vault import unseal_value as _vault_unseal

        revealed = _vault_unseal(text)
        if revealed:
            return str(revealed)
    except Exception as exc:
        log.debug("credential-vault unseal unavailable: %s", exc)
    return text


__all__ = [
    "MAX_SSH_COMMAND_LENGTH",
    "SECRET_DIR_MODE",
    "SECRET_FILE_MODE",
    "SEALED_SECRET_PREFIX",
    "build_sshpass_command",
    "require_encryption_key",
    "seal_secret",
    "set_sshpass_env",
    "store_secret_owner_only",
    "unseal_secret",
]
