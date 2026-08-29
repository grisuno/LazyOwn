"""Centralized security hardening utilities for the LazyOwn framework.

Contract: provides safe alternatives to dangerous patterns found across
the codebase. Every function is a single-responsibility security control
that replaces ad-hoc, vulnerable patterns with a tested, auditable path.

Invariants:

1. ``safe_subprocess_run`` never invokes a shell unless explicitly allowed
   and audited.
2. ``safe_clipboard_copy`` uses subprocess list-form, never os.system.
3. ``validate_sshpass_env`` sets SSHPASS env var and uses sshpass -e,
   never sshpass -p.
4. ``escape_html`` sanitizes all user-controlled data before HTML insertion.
5. ``safe_path_join`` prevents path traversal via os.path.realpath prefix
   check.
6. ``require_encryption_key`` refuses to operate with a static fallback key.
7. ``defused_xml_parse`` wraps defusedxml for safe XML parsing.
"""

from __future__ import annotations

import html
import logging
import os
import re
import shlex
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any

log = logging.getLogger("core.hardening")

MAX_SSH_COMMAND_LENGTH = 4096
MAX_CLIPBOARD_CONTENT_LENGTH = 65536
_SAFE_PATH_PATTERN = re.compile(r"^[a-zA-Z0-9._/\-]+$")
_NETWORK_CIDR_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    r"(?:/(?:3[0-2]|[12]?\d))?$"
)
_PORT_PATTERN = re.compile(r"^(?:\d{1,5}(?:,\d{1,5})*(?:-\d{1,5})?)$")


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class SecurityViolation(PermissionError):
    """Raised when a security invariant is violated."""
mutants_x_safe_subprocess_run__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_safe_subprocess_run__mutmut)
def safe_subprocess_run(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_orig(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_1(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = False,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_2(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "XXXX",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_3(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_4(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError(None)
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_5(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("XXargv must contain at least the program nameXX")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_6(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("ARGV MUST CONTAIN AT LEAST THE PROGRAM NAME")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_7(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "XX\0XX" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_8(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" not in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_9(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation(None)
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_10(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("XXNull byte in argument rejectedXX")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_11(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_12(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("NULL BYTE IN ARGUMENT REJECTED")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_13(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug(None, argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_14(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", None, reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_15(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], None)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_16(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug(argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_17(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_18(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], )
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_19(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("XXsafe_subprocess_run: %s reason=%sXX", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_20(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("SAFE_SUBPROCESS_RUN: %S REASON=%S", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_21(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[1], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_22(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        None,
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_23(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=None,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_24(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=None,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_25(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=None,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_26(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=None,
        check=False,
    )


def x_safe_subprocess_run__mutmut_27(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=None,
    )


def x_safe_subprocess_run__mutmut_28(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_29(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_30(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_31(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_32(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        check=False,
    )


def x_safe_subprocess_run__mutmut_33(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        )


def x_safe_subprocess_run__mutmut_34(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(None),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_35(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=True,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_36(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=False,
        timeout=timeout,
        check=False,
    )


def x_safe_subprocess_run__mutmut_37(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    reason: str = "",
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        reason: Free-text justification for audit logging.

    Returns:
        CompletedProcess result.

    Raises:
        SecurityViolation: If argv is empty or contains shell metacharacters.
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise SecurityViolation("Null byte in argument rejected")
    log.debug("safe_subprocess_run: %s reason=%s", argv[0], reason)
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=True,
    )

mutants_x_safe_subprocess_run__mutmut['_mutmut_orig'] = x_safe_subprocess_run__mutmut_orig # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_1'] = x_safe_subprocess_run__mutmut_1 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_2'] = x_safe_subprocess_run__mutmut_2 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_3'] = x_safe_subprocess_run__mutmut_3 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_4'] = x_safe_subprocess_run__mutmut_4 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_5'] = x_safe_subprocess_run__mutmut_5 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_6'] = x_safe_subprocess_run__mutmut_6 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_7'] = x_safe_subprocess_run__mutmut_7 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_8'] = x_safe_subprocess_run__mutmut_8 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_9'] = x_safe_subprocess_run__mutmut_9 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_10'] = x_safe_subprocess_run__mutmut_10 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_11'] = x_safe_subprocess_run__mutmut_11 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_12'] = x_safe_subprocess_run__mutmut_12 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_13'] = x_safe_subprocess_run__mutmut_13 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_14'] = x_safe_subprocess_run__mutmut_14 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_15'] = x_safe_subprocess_run__mutmut_15 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_16'] = x_safe_subprocess_run__mutmut_16 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_17'] = x_safe_subprocess_run__mutmut_17 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_18'] = x_safe_subprocess_run__mutmut_18 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_19'] = x_safe_subprocess_run__mutmut_19 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_20'] = x_safe_subprocess_run__mutmut_20 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_21'] = x_safe_subprocess_run__mutmut_21 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_22'] = x_safe_subprocess_run__mutmut_22 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_23'] = x_safe_subprocess_run__mutmut_23 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_24'] = x_safe_subprocess_run__mutmut_24 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_25'] = x_safe_subprocess_run__mutmut_25 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_26'] = x_safe_subprocess_run__mutmut_26 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_27'] = x_safe_subprocess_run__mutmut_27 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_28'] = x_safe_subprocess_run__mutmut_28 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_29'] = x_safe_subprocess_run__mutmut_29 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_30'] = x_safe_subprocess_run__mutmut_30 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_31'] = x_safe_subprocess_run__mutmut_31 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_32'] = x_safe_subprocess_run__mutmut_32 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_33'] = x_safe_subprocess_run__mutmut_33 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_34'] = x_safe_subprocess_run__mutmut_34 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_35'] = x_safe_subprocess_run__mutmut_35 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_36'] = x_safe_subprocess_run__mutmut_36 # type: ignore # mutmut generated
mutants_x_safe_subprocess_run__mutmut['x_safe_subprocess_run__mutmut_37'] = x_safe_subprocess_run__mutmut_37 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_safe_clipboard_copy__mutmut)
def safe_clipboard_copy(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_orig(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_1(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) >= MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_2(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            None
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_3(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("XXxclipXX", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_4(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("XCLIP", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_5(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["XX-selXX", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_6(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-SEL", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_7(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "XXclipXX"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_8(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "CLIP"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_9(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("XXxselXX", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_10(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("XSEL", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_11(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["XX--clipboardXX", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_12(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--CLIPBOARD", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_13(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "XX--inputXX"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_14(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--INPUT"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_15(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = None
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_16(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                None,
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_17(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=None,
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_18(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=None,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_19(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=None,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_20(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=None,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_21(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_22(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_23(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_24(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_25(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_26(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] - args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_27(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode(None),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_28(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("XXutf-8XX"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_29(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("UTF-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_30(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=True,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_31(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=False,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_32(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=6,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_33(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode != 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_34(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 1:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_35(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return False
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_36(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            break
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_37(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning(None, tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_38(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", None)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_39(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning(tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_40(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", )
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_41(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("XXClipboard tool %s timed outXX", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_42(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_43(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("CLIPBOARD TOOL %S TIMED OUT", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_44(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            break
    log.error("No clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_45(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error(None)
    return False


def x_safe_clipboard_copy__mutmut_46(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("XXNo clipboard tool available (xclip/xsel)XX")
    return False


def x_safe_clipboard_copy__mutmut_47(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("no clipboard tool available (xclip/xsel)")
    return False


def x_safe_clipboard_copy__mutmut_48(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("NO CLIPBOARD TOOL AVAILABLE (XCLIP/XSEL)")
    return False


def x_safe_clipboard_copy__mutmut_49(content: str) -> bool:
    """Copy content to system clipboard without shell interpretation.

    Uses subprocess list-form with xclip or xsel. Never uses os.system.

    Args:
        content: Text to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.

    Raises:
        SecurityViolation: If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.
    """
    if len(content) > MAX_CLIPBOARD_CONTENT_LENGTH:
        raise SecurityViolation(
            f"Clipboard content exceeds {MAX_CLIPBOARD_CONTENT_LENGTH} bytes"
        )
    for tool, args in [
        ("xclip", ["-sel", "clip"]),
        ("xsel", ["--clipboard", "--input"]),
    ]:
        try:
            proc = subprocess.run(
                [tool] + args if isinstance(args, list) else [tool, *args],
                input=content.encode("utf-8"),
                shell=False,
                capture_output=True,
                timeout=5,
            )
            if proc.returncode == 0:
                return True
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            log.warning("Clipboard tool %s timed out", tool)
            continue
    log.error("No clipboard tool available (xclip/xsel)")
    return True

mutants_x_safe_clipboard_copy__mutmut['_mutmut_orig'] = x_safe_clipboard_copy__mutmut_orig # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_1'] = x_safe_clipboard_copy__mutmut_1 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_2'] = x_safe_clipboard_copy__mutmut_2 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_3'] = x_safe_clipboard_copy__mutmut_3 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_4'] = x_safe_clipboard_copy__mutmut_4 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_5'] = x_safe_clipboard_copy__mutmut_5 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_6'] = x_safe_clipboard_copy__mutmut_6 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_7'] = x_safe_clipboard_copy__mutmut_7 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_8'] = x_safe_clipboard_copy__mutmut_8 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_9'] = x_safe_clipboard_copy__mutmut_9 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_10'] = x_safe_clipboard_copy__mutmut_10 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_11'] = x_safe_clipboard_copy__mutmut_11 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_12'] = x_safe_clipboard_copy__mutmut_12 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_13'] = x_safe_clipboard_copy__mutmut_13 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_14'] = x_safe_clipboard_copy__mutmut_14 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_15'] = x_safe_clipboard_copy__mutmut_15 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_16'] = x_safe_clipboard_copy__mutmut_16 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_17'] = x_safe_clipboard_copy__mutmut_17 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_18'] = x_safe_clipboard_copy__mutmut_18 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_19'] = x_safe_clipboard_copy__mutmut_19 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_20'] = x_safe_clipboard_copy__mutmut_20 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_21'] = x_safe_clipboard_copy__mutmut_21 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_22'] = x_safe_clipboard_copy__mutmut_22 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_23'] = x_safe_clipboard_copy__mutmut_23 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_24'] = x_safe_clipboard_copy__mutmut_24 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_25'] = x_safe_clipboard_copy__mutmut_25 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_26'] = x_safe_clipboard_copy__mutmut_26 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_27'] = x_safe_clipboard_copy__mutmut_27 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_28'] = x_safe_clipboard_copy__mutmut_28 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_29'] = x_safe_clipboard_copy__mutmut_29 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_30'] = x_safe_clipboard_copy__mutmut_30 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_31'] = x_safe_clipboard_copy__mutmut_31 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_32'] = x_safe_clipboard_copy__mutmut_32 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_33'] = x_safe_clipboard_copy__mutmut_33 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_34'] = x_safe_clipboard_copy__mutmut_34 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_35'] = x_safe_clipboard_copy__mutmut_35 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_36'] = x_safe_clipboard_copy__mutmut_36 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_37'] = x_safe_clipboard_copy__mutmut_37 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_38'] = x_safe_clipboard_copy__mutmut_38 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_39'] = x_safe_clipboard_copy__mutmut_39 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_40'] = x_safe_clipboard_copy__mutmut_40 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_41'] = x_safe_clipboard_copy__mutmut_41 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_42'] = x_safe_clipboard_copy__mutmut_42 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_43'] = x_safe_clipboard_copy__mutmut_43 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_44'] = x_safe_clipboard_copy__mutmut_44 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_45'] = x_safe_clipboard_copy__mutmut_45 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_46'] = x_safe_clipboard_copy__mutmut_46 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_47'] = x_safe_clipboard_copy__mutmut_47 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_48'] = x_safe_clipboard_copy__mutmut_48 # type: ignore # mutmut generated
mutants_x_safe_clipboard_copy__mutmut['x_safe_clipboard_copy__mutmut_49'] = x_safe_clipboard_copy__mutmut_49 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build_sshpass_command__mutmut)
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


def x_build_sshpass_command__mutmut_orig(
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


def x_build_sshpass_command__mutmut_1(
    password: str,
    ssh_args: list[str],
    *,
    max_password_length: int = 257,
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


def x_build_sshpass_command__mutmut_2(
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
    if len(password) >= max_password_length:
        raise SecurityViolation("Password exceeds maximum allowed length")
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_3(
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
        raise SecurityViolation(None)
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_4(
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
        raise SecurityViolation("XXPassword exceeds maximum allowed lengthXX")
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_5(
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
        raise SecurityViolation("password exceeds maximum allowed length")
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_6(
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
        raise SecurityViolation("PASSWORD EXCEEDS MAXIMUM ALLOWED LENGTH")
    if "\0" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_7(
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
    if "XX\0XX" in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_8(
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
    if "\0" not in password:
        raise SecurityViolation("Null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_9(
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
        raise SecurityViolation(None)
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_10(
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
        raise SecurityViolation("XXNull byte in password rejectedXX")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_11(
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
        raise SecurityViolation("null byte in password rejected")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_12(
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
        raise SecurityViolation("NULL BYTE IN PASSWORD REJECTED")
    return ["sshpass", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_13(
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
    return ["XXsshpassXX", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_14(
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
    return ["SSHPASS", "-e", *ssh_args]


def x_build_sshpass_command__mutmut_15(
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
    return ["sshpass", "XX-eXX", *ssh_args]


def x_build_sshpass_command__mutmut_16(
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
    return ["sshpass", "-E", *ssh_args]

mutants_x_build_sshpass_command__mutmut['_mutmut_orig'] = x_build_sshpass_command__mutmut_orig # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_1'] = x_build_sshpass_command__mutmut_1 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_2'] = x_build_sshpass_command__mutmut_2 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_3'] = x_build_sshpass_command__mutmut_3 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_4'] = x_build_sshpass_command__mutmut_4 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_5'] = x_build_sshpass_command__mutmut_5 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_6'] = x_build_sshpass_command__mutmut_6 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_7'] = x_build_sshpass_command__mutmut_7 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_8'] = x_build_sshpass_command__mutmut_8 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_9'] = x_build_sshpass_command__mutmut_9 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_10'] = x_build_sshpass_command__mutmut_10 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_11'] = x_build_sshpass_command__mutmut_11 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_12'] = x_build_sshpass_command__mutmut_12 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_13'] = x_build_sshpass_command__mutmut_13 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_14'] = x_build_sshpass_command__mutmut_14 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_15'] = x_build_sshpass_command__mutmut_15 # type: ignore # mutmut generated
mutants_x_build_sshpass_command__mutmut['x_build_sshpass_command__mutmut_16'] = x_build_sshpass_command__mutmut_16 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_set_sshpass_env__mutmut)
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


def x_set_sshpass_env__mutmut_orig(password: str) -> dict[str, str]:
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


def x_set_sshpass_env__mutmut_1(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "XX\0XX" in password:
        raise SecurityViolation("Null byte in password rejected")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_2(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" not in password:
        raise SecurityViolation("Null byte in password rejected")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_3(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" in password:
        raise SecurityViolation(None)
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_4(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" in password:
        raise SecurityViolation("XXNull byte in password rejectedXX")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_5(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" in password:
        raise SecurityViolation("null byte in password rejected")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_6(password: str) -> dict[str, str]:
    """Create an environment dict with SSHPASS set for sshpass -e.

    Args:
        password: The SSH password.

    Returns:
        Copy of os.environ with SSHPASS set.

    Raises:
        SecurityViolation: If password contains null bytes.
    """
    if "\0" in password:
        raise SecurityViolation("NULL BYTE IN PASSWORD REJECTED")
    env = os.environ.copy()
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_7(password: str) -> dict[str, str]:
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
    env = None
    env["SSHPASS"] = password
    return env


def x_set_sshpass_env__mutmut_8(password: str) -> dict[str, str]:
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
    env["SSHPASS"] = None
    return env


def x_set_sshpass_env__mutmut_9(password: str) -> dict[str, str]:
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
    env["XXSSHPASSXX"] = password
    return env


def x_set_sshpass_env__mutmut_10(password: str) -> dict[str, str]:
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
    env["sshpass"] = password
    return env

mutants_x_set_sshpass_env__mutmut['_mutmut_orig'] = x_set_sshpass_env__mutmut_orig # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_1'] = x_set_sshpass_env__mutmut_1 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_2'] = x_set_sshpass_env__mutmut_2 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_3'] = x_set_sshpass_env__mutmut_3 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_4'] = x_set_sshpass_env__mutmut_4 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_5'] = x_set_sshpass_env__mutmut_5 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_6'] = x_set_sshpass_env__mutmut_6 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_7'] = x_set_sshpass_env__mutmut_7 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_8'] = x_set_sshpass_env__mutmut_8 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_9'] = x_set_sshpass_env__mutmut_9 # type: ignore # mutmut generated
mutants_x_set_sshpass_env__mutmut['x_set_sshpass_env__mutmut_10'] = x_set_sshpass_env__mutmut_10 # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_escape_html_content__mutmut)
def escape_html_content(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), quote=True)


def x_escape_html_content__mutmut_orig(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), quote=True)


def x_escape_html_content__mutmut_1(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(None, quote=True)


def x_escape_html_content__mutmut_2(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), quote=None)


def x_escape_html_content__mutmut_3(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(quote=True)


def x_escape_html_content__mutmut_4(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), )


def x_escape_html_content__mutmut_5(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(None), quote=True)


def x_escape_html_content__mutmut_6(value: str) -> str:
    """Escape HTML special characters to prevent XSS.

    Args:
        value: Raw string that may contain HTML.

    Returns:
        HTML-escaped string safe for insertion into HTML context.
    """
    return html.escape(str(value), quote=False)

mutants_x_escape_html_content__mutmut['_mutmut_orig'] = x_escape_html_content__mutmut_orig # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut['x_escape_html_content__mutmut_1'] = x_escape_html_content__mutmut_1 # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut['x_escape_html_content__mutmut_2'] = x_escape_html_content__mutmut_2 # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut['x_escape_html_content__mutmut_3'] = x_escape_html_content__mutmut_3 # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut['x_escape_html_content__mutmut_4'] = x_escape_html_content__mutmut_4 # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut['x_escape_html_content__mutmut_5'] = x_escape_html_content__mutmut_5 # type: ignore # mutmut generated
mutants_x_escape_html_content__mutmut['x_escape_html_content__mutmut_6'] = x_escape_html_content__mutmut_6 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_safe_path_join__mutmut)
def safe_path_join(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_orig(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_1(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path and not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_2(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_3(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_4(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError(None)
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_5(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("XXuser_path must not be emptyXX")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_6(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("USER_PATH MUST NOT BE EMPTY")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_7(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = None
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_8(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(None)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_9(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = None
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_10(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(None)
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_11(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(None, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_12(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, None))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_13(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_14(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, ))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_15(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) or candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_16(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_17(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(None) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_18(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed - os.sep) and candidate != allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_19(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate == allowed:
        raise SecurityViolation(
            f"Path traversal blocked: {user_path} resolves outside {base_dir}"
        )
    return candidate


def x_safe_path_join__mutmut_20(base_dir: str, user_path: str) -> str:
    """Join base_dir and user_path safely, preventing path traversal.

    Uses os.path.realpath to resolve symlinks and .. components, then
    verifies the result starts with the allowed base directory.

    Args:
        base_dir: The allowed root directory.
        user_path: User-controlled path component.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        SecurityViolation: If the resolved path escapes base_dir.
        ValueError: If user_path is empty or contains only separators.
    """
    if not user_path or not user_path.strip():
        raise ValueError("user_path must not be empty")
    allowed = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(allowed, user_path))
    if not candidate.startswith(allowed + os.sep) and candidate != allowed:
        raise SecurityViolation(
            None
        )
    return candidate

mutants_x_safe_path_join__mutmut['_mutmut_orig'] = x_safe_path_join__mutmut_orig # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_1'] = x_safe_path_join__mutmut_1 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_2'] = x_safe_path_join__mutmut_2 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_3'] = x_safe_path_join__mutmut_3 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_4'] = x_safe_path_join__mutmut_4 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_5'] = x_safe_path_join__mutmut_5 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_6'] = x_safe_path_join__mutmut_6 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_7'] = x_safe_path_join__mutmut_7 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_8'] = x_safe_path_join__mutmut_8 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_9'] = x_safe_path_join__mutmut_9 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_10'] = x_safe_path_join__mutmut_10 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_11'] = x_safe_path_join__mutmut_11 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_12'] = x_safe_path_join__mutmut_12 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_13'] = x_safe_path_join__mutmut_13 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_14'] = x_safe_path_join__mutmut_14 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_15'] = x_safe_path_join__mutmut_15 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_16'] = x_safe_path_join__mutmut_16 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_17'] = x_safe_path_join__mutmut_17 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_18'] = x_safe_path_join__mutmut_18 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_19'] = x_safe_path_join__mutmut_19 # type: ignore # mutmut generated
mutants_x_safe_path_join__mutmut['x_safe_path_join__mutmut_20'] = x_safe_path_join__mutmut_20 # type: ignore # mutmut generated
mutants_x_validate_network_cidr__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_network_cidr__mutmut)
def validate_network_cidr(cidr: str) -> bool:
    """Validate a network CIDR notation string.

    Args:
        cidr: Network address in CIDR notation (e.g. "192.168.1.0/24").

    Returns:
        True if valid CIDR, False otherwise.
    """
    return bool(_NETWORK_CIDR_PATTERN.match(cidr.strip()))


def x_validate_network_cidr__mutmut_orig(cidr: str) -> bool:
    """Validate a network CIDR notation string.

    Args:
        cidr: Network address in CIDR notation (e.g. "192.168.1.0/24").

    Returns:
        True if valid CIDR, False otherwise.
    """
    return bool(_NETWORK_CIDR_PATTERN.match(cidr.strip()))


def x_validate_network_cidr__mutmut_1(cidr: str) -> bool:
    """Validate a network CIDR notation string.

    Args:
        cidr: Network address in CIDR notation (e.g. "192.168.1.0/24").

    Returns:
        True if valid CIDR, False otherwise.
    """
    return bool(None)


def x_validate_network_cidr__mutmut_2(cidr: str) -> bool:
    """Validate a network CIDR notation string.

    Args:
        cidr: Network address in CIDR notation (e.g. "192.168.1.0/24").

    Returns:
        True if valid CIDR, False otherwise.
    """
    return bool(_NETWORK_CIDR_PATTERN.match(None))

mutants_x_validate_network_cidr__mutmut['_mutmut_orig'] = x_validate_network_cidr__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_network_cidr__mutmut['x_validate_network_cidr__mutmut_1'] = x_validate_network_cidr__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_network_cidr__mutmut['x_validate_network_cidr__mutmut_2'] = x_validate_network_cidr__mutmut_2 # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_port_spec__mutmut)
def validate_port_spec(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or not ports.strip():
        return False
    return bool(_PORT_PATTERN.match(ports.strip()))


def x_validate_port_spec__mutmut_orig(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or not ports.strip():
        return False
    return bool(_PORT_PATTERN.match(ports.strip()))


def x_validate_port_spec__mutmut_1(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports and not ports.strip():
        return False
    return bool(_PORT_PATTERN.match(ports.strip()))


def x_validate_port_spec__mutmut_2(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if ports or not ports.strip():
        return False
    return bool(_PORT_PATTERN.match(ports.strip()))


def x_validate_port_spec__mutmut_3(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or ports.strip():
        return False
    return bool(_PORT_PATTERN.match(ports.strip()))


def x_validate_port_spec__mutmut_4(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or not ports.strip():
        return True
    return bool(_PORT_PATTERN.match(ports.strip()))


def x_validate_port_spec__mutmut_5(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or not ports.strip():
        return False
    return bool(None)


def x_validate_port_spec__mutmut_6(ports: str) -> bool:
    """Validate a port specification string.

    Supports comma-separated ports and ranges (e.g. "22,80,443-445").

    Args:
        ports: Port specification string.

    Returns:
        True if valid, False otherwise.
    """
    if not ports or not ports.strip():
        return False
    return bool(_PORT_PATTERN.match(None))

mutants_x_validate_port_spec__mutmut['_mutmut_orig'] = x_validate_port_spec__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut['x_validate_port_spec__mutmut_1'] = x_validate_port_spec__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut['x_validate_port_spec__mutmut_2'] = x_validate_port_spec__mutmut_2 # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut['x_validate_port_spec__mutmut_3'] = x_validate_port_spec__mutmut_3 # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut['x_validate_port_spec__mutmut_4'] = x_validate_port_spec__mutmut_4 # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut['x_validate_port_spec__mutmut_5'] = x_validate_port_spec__mutmut_5 # type: ignore # mutmut generated
mutants_x_validate_port_spec__mutmut['x_validate_port_spec__mutmut_6'] = x_validate_port_spec__mutmut_6 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_host__mutmut)
def validate_host(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_orig(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_1(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host and len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_2(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_3(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) >= 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_4(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 254:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_5(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return True
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_6(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(None):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_7(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return False
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_8(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = None
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_9(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        None
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_10(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"XX^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*XX"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_11(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-za-z0-9](?:[a-za-z0-9\-]{0,61}[a-za-z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_12(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[A-ZA-Z0-9](?:[A-ZA-Z0-9\-]{0,61}[A-ZA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_13(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"XX[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|XX"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_14(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-za-z0-9](?:[a-za-z0-9\-]{0,61}[a-za-z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_15(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[A-ZA-Z0-9](?:[A-ZA-Z0-9\-]{0,61}[A-ZA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_16(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"XX(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}XX"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_17(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"XX(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$XX"
    )
    return bool(host_pattern.match(host))


def x_validate_host__mutmut_18(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(None)


def x_validate_host__mutmut_19(host: str) -> bool:
    """Validate a hostname or IP address.

    Args:
        host: Hostname or IP to validate.

    Returns:
        True if valid, False otherwise.
    """
    if not host or len(host) > 253:
        return False
    if _NETWORK_CIDR_PATTERN.match(host):
        return True
    host_pattern = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?|"
        r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)?)$"
    )
    return bool(host_pattern.match(None))

mutants_x_validate_host__mutmut['_mutmut_orig'] = x_validate_host__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_1'] = x_validate_host__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_2'] = x_validate_host__mutmut_2 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_3'] = x_validate_host__mutmut_3 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_4'] = x_validate_host__mutmut_4 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_5'] = x_validate_host__mutmut_5 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_6'] = x_validate_host__mutmut_6 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_7'] = x_validate_host__mutmut_7 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_8'] = x_validate_host__mutmut_8 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_9'] = x_validate_host__mutmut_9 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_10'] = x_validate_host__mutmut_10 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_11'] = x_validate_host__mutmut_11 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_12'] = x_validate_host__mutmut_12 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_13'] = x_validate_host__mutmut_13 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_14'] = x_validate_host__mutmut_14 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_15'] = x_validate_host__mutmut_15 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_16'] = x_validate_host__mutmut_16 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_17'] = x_validate_host__mutmut_17 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_18'] = x_validate_host__mutmut_18 # type: ignore # mutmut generated
mutants_x_validate_host__mutmut['x_validate_host__mutmut_19'] = x_validate_host__mutmut_19 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_require_encryption_key__mutmut)
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


def x_require_encryption_key__mutmut_orig(
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


def x_require_encryption_key__mutmut_1(
    env_key: str = "XXLAZYOWN_SECRET_KEYXX",
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


def x_require_encryption_key__mutmut_2(
    env_key: str = "lazyown_secret_key",
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


def x_require_encryption_key__mutmut_3(
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
    secret = None
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_4(
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
    secret = os.environ.get(None, "")
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_5(
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
    secret = os.environ.get(env_key, None)
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_6(
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
    secret = os.environ.get("")
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_7(
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
    secret = os.environ.get(env_key, )
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_8(
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
    secret = os.environ.get(env_key, "XXXX")
    if not secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_9(
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
    if not secret and secret_file or secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_10(
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
    if not secret or secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_11(
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
    if secret and secret_file and secret_file.exists():
        secret = secret_file.read_text().strip()
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_12(
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
        secret = None
    if not secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_13(
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
    if secret:
        raise SecurityViolation(
            f"Encryption key required. Set {env_key} env var or create "
            f"{secret_file or '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_14(
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
            None
        )
    return secret


def x_require_encryption_key__mutmut_15(
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
            f"{secret_file and '.secret_key'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_16(
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
            f"{secret_file or 'XX.secret_keyXX'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_17(
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
            f"{secret_file or '.SECRET_KEY'} file. "
            "Static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_18(
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
            "XXStatic fallback keys are not allowed in production.XX"
        )
    return secret


def x_require_encryption_key__mutmut_19(
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
            "static fallback keys are not allowed in production."
        )
    return secret


def x_require_encryption_key__mutmut_20(
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
            "STATIC FALLBACK KEYS ARE NOT ALLOWED IN PRODUCTION."
        )
    return secret

mutants_x_require_encryption_key__mutmut['_mutmut_orig'] = x_require_encryption_key__mutmut_orig # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_1'] = x_require_encryption_key__mutmut_1 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_2'] = x_require_encryption_key__mutmut_2 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_3'] = x_require_encryption_key__mutmut_3 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_4'] = x_require_encryption_key__mutmut_4 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_5'] = x_require_encryption_key__mutmut_5 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_6'] = x_require_encryption_key__mutmut_6 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_7'] = x_require_encryption_key__mutmut_7 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_8'] = x_require_encryption_key__mutmut_8 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_9'] = x_require_encryption_key__mutmut_9 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_10'] = x_require_encryption_key__mutmut_10 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_11'] = x_require_encryption_key__mutmut_11 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_12'] = x_require_encryption_key__mutmut_12 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_13'] = x_require_encryption_key__mutmut_13 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_14'] = x_require_encryption_key__mutmut_14 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_15'] = x_require_encryption_key__mutmut_15 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_16'] = x_require_encryption_key__mutmut_16 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_17'] = x_require_encryption_key__mutmut_17 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_18'] = x_require_encryption_key__mutmut_18 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_19'] = x_require_encryption_key__mutmut_19 # type: ignore # mutmut generated
mutants_x_require_encryption_key__mutmut['x_require_encryption_key__mutmut_20'] = x_require_encryption_key__mutmut_20 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_defused_xml_parse__mutmut)
def defused_xml_parse(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_orig(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_1(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            None
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_2(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "XXdefusedxml is required for safe XML parsing. XX"
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_3(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe xml parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_4(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "DEFUSEDXML IS REQUIRED FOR SAFE XML PARSING. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_5(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "XXInstall with: pip install defusedxmlXX"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_6(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_7(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "INSTALL WITH: PIP INSTALL DEFUSEDXML"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_8(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) or os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_9(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(None):
        return ET.parse(source)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_10(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(None)
    return ET.fromstring(str(source))


def x_defused_xml_parse__mutmut_11(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(None)


def x_defused_xml_parse__mutmut_12(source: str | Path) -> Any:
    """Parse XML safely using defusedxml.

    Args:
        source: File path or string containing XML data.

    Returns:
        Parsed XML ElementTree root element.

    Raises:
        ImportError: If defusedxml is not installed.
        ValueError: If XML parsing fails.
    """
    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        raise ImportError(
            "defusedxml is required for safe XML parsing. "
            "Install with: pip install defusedxml"
        )
    if isinstance(source, (str, Path)) and os.path.isfile(source):
        return ET.parse(source)
    return ET.fromstring(str(None))

mutants_x_defused_xml_parse__mutmut['_mutmut_orig'] = x_defused_xml_parse__mutmut_orig # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_1'] = x_defused_xml_parse__mutmut_1 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_2'] = x_defused_xml_parse__mutmut_2 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_3'] = x_defused_xml_parse__mutmut_3 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_4'] = x_defused_xml_parse__mutmut_4 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_5'] = x_defused_xml_parse__mutmut_5 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_6'] = x_defused_xml_parse__mutmut_6 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_7'] = x_defused_xml_parse__mutmut_7 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_8'] = x_defused_xml_parse__mutmut_8 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_9'] = x_defused_xml_parse__mutmut_9 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_10'] = x_defused_xml_parse__mutmut_10 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_11'] = x_defused_xml_parse__mutmut_11 # type: ignore # mutmut generated
mutants_x_defused_xml_parse__mutmut['x_defused_xml_parse__mutmut_12'] = x_defused_xml_parse__mutmut_12 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_sanitize_filename__mutmut)
def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_orig(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_1(filename: str, max_length: int = 256) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_2(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = None
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_3(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(None, "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_4(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", None, filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_5(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", None)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_6(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub("_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_7(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_8(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", )
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_9(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"XX[^\w.\-]XX", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_10(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "XX_XX", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_11(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = None
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_12(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip(None)
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_13(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(None, "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_14(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", None, safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_15(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", None).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_16(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub("_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_17(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_18(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", ).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_19(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"XX_+XX", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_20(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "XX_XX", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_21(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("XX_.XX")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_22(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_23(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = None
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_24(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "XXunnamedXX"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_25(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "UNNAMED"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_26(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) >= max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_27(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = None
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_28(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(None)
        safe = name[: max_length - len(ext)] + ext
    return safe


def x_sanitize_filename__mutmut_29(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = None
    return safe


def x_sanitize_filename__mutmut_30(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length - len(ext)] - ext
    return safe


def x_sanitize_filename__mutmut_31(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing dangerous characters.

    Args:
        filename: Raw filename from user input.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename with only safe characters.
    """
    safe = re.sub(r"[^\w.\-]", "_", filename)
    safe = re.sub(r"_+", "_", safe).strip("_.")
    if not safe:
        safe = "unnamed"
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[: max_length + len(ext)] + ext
    return safe

mutants_x_sanitize_filename__mutmut['_mutmut_orig'] = x_sanitize_filename__mutmut_orig # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_1'] = x_sanitize_filename__mutmut_1 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_2'] = x_sanitize_filename__mutmut_2 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_3'] = x_sanitize_filename__mutmut_3 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_4'] = x_sanitize_filename__mutmut_4 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_5'] = x_sanitize_filename__mutmut_5 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_6'] = x_sanitize_filename__mutmut_6 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_7'] = x_sanitize_filename__mutmut_7 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_8'] = x_sanitize_filename__mutmut_8 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_9'] = x_sanitize_filename__mutmut_9 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_10'] = x_sanitize_filename__mutmut_10 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_11'] = x_sanitize_filename__mutmut_11 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_12'] = x_sanitize_filename__mutmut_12 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_13'] = x_sanitize_filename__mutmut_13 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_14'] = x_sanitize_filename__mutmut_14 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_15'] = x_sanitize_filename__mutmut_15 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_16'] = x_sanitize_filename__mutmut_16 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_17'] = x_sanitize_filename__mutmut_17 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_18'] = x_sanitize_filename__mutmut_18 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_19'] = x_sanitize_filename__mutmut_19 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_20'] = x_sanitize_filename__mutmut_20 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_21'] = x_sanitize_filename__mutmut_21 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_22'] = x_sanitize_filename__mutmut_22 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_23'] = x_sanitize_filename__mutmut_23 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_24'] = x_sanitize_filename__mutmut_24 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_25'] = x_sanitize_filename__mutmut_25 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_26'] = x_sanitize_filename__mutmut_26 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_27'] = x_sanitize_filename__mutmut_27 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_28'] = x_sanitize_filename__mutmut_28 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_29'] = x_sanitize_filename__mutmut_29 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_30'] = x_sanitize_filename__mutmut_30 # type: ignore # mutmut generated
mutants_x_sanitize_filename__mutmut['x_sanitize_filename__mutmut_31'] = x_sanitize_filename__mutmut_31 # type: ignore # mutmut generated


__all__ = [
    "SecurityViolation",
    "safe_subprocess_run",
    "safe_clipboard_copy",
    "build_sshpass_command",
    "set_sshpass_env",
    "escape_html_content",
    "safe_path_join",
    "validate_network_cidr",
    "validate_port_spec",
    "validate_host",
    "require_encryption_key",
    "defused_xml_parse",
    "sanitize_filename",
    "MAX_SSH_COMMAND_LENGTH",
    "MAX_CLIPBOARD_CONTENT_LENGTH",
]
