"""Reverse-shell fallback secret — sealed persistence contract.

Single-responsibility home for the C2 ``/lazyos`` fallback password so the
logic is importable without the heavy ``lazyc2`` dependency chain (Flask,
dnslib, yagmail). ``lazyc2.py`` delegates to these helpers; tests target
this module directly.

Secrets are sealed with :func:`core.hardening.seal_secret` (Fernet,
AES-128-CBC + HMAC, key from the shared ``key.aes`` resolver) and files
are written owner-only (0700 dir / 0600 file). Legacy plaintext files
still load so existing operator stores keep working.
"""

from __future__ import annotations

import secrets as _secrets
from pathlib import Path

REVERSE_SHELL_SECRET_FILENAME = ".reverse_shell_password"
REVERSE_SHELL_PASSWORD_MIN_LENGTH = 12
REVERSE_SHELL_TOKEN_HEX_BYTES = 32


def seal_reverse_shell_password(plaintext: str) -> str:
    """Seal a fallback password for storage.

    Args:
        plaintext: Generated fallback password.

    Returns:
        Sealed value when sealing resolves, else plaintext.
    """
    try:
        from core.hardening import seal_secret as _seal_secret

        return _seal_secret(str(plaintext or ""))
    except Exception:
        return str(plaintext or "")


def load_reverse_shell_password(secret_path: str | Path) -> str:
    """Load a persisted fallback password, unsealing vault values.

    Args:
        secret_path: Path of the persisted fallback secret.

    Returns:
        Stored password, or empty string when unreadable.
    """
    try:
        lines = Path(secret_path).read_text(encoding="utf-8").strip().splitlines()
    except OSError:
        return ""
    if not lines or not lines[0].strip():
        return ""
    candidate = lines[0].strip()
    try:
        from core.hardening import unseal_secret as _unseal_secret

        return str(_unseal_secret(candidate) or "")
    except Exception:
        return candidate


def generate_reverse_shell_password() -> str:
    """Generate a fresh cryptographically random fallback password.

    Returns:
        64-character hex token (32 random bytes).
    """
    return _secrets.token_hex(REVERSE_SHELL_TOKEN_HEX_BYTES)


def is_configured_password_valid(candidate: str, minimum_length: int = REVERSE_SHELL_PASSWORD_MIN_LENGTH) -> bool:
    """Return True when an operator-configured password meets the floor.

    Args:
        candidate: Configured ``c2_reverse_shell_password`` value.
        minimum_length: Minimum accepted length.

    Returns:
        True when non-empty and at least ``minimum_length`` chars.
    """
    text = str(candidate or "").strip()
    return bool(text) and len(text) >= int(minimum_length)


__all__ = [
    "REVERSE_SHELL_SECRET_FILENAME",
    "REVERSE_SHELL_PASSWORD_MIN_LENGTH",
    "REVERSE_SHELL_TOKEN_HEX_BYTES",
    "seal_reverse_shell_password",
    "load_reverse_shell_password",
    "generate_reverse_shell_password",
    "is_configured_password_valid",
]
