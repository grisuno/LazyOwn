"""Centralized safe command execution for the LazyOwn framework.

Contract: replaces all ``os.system()`` and ``subprocess.run(shell=True)``
call sites with a single, audited, default-deny execution path.

Invariants:

1. ``safe_system`` never passes user-controlled strings to a shell.
2. ``safe_run_argv`` always uses ``shell=False``.
3. ``safe_run_shell`` requires explicit ``allow=True`` plus a reason.
4. ``safe_clear_screen`` uses the terminal capability query, never os.system.
5. ``validate_url`` rejects shell metacharacters in URLs before git clone.
6. ``safe_git_clone`` uses subprocess list-form, never os.system.
7. ``safe_ip_display`` parses ``ip`` output in Python, never via shell pipes.
"""

from __future__ import annotations

import logging
import re
import shlex
import subprocess
import sys
import urllib.parse
from collections.abc import Sequence
from pathlib import Path

log = logging.getLogger("core.safe_exec")

_URL_SAFE_PATTERN = re.compile(
    r"^https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+$"
)

_SHELL_META_PATTERN = re.compile(r"[;&|`$(){}!\n\r]")

_MAX_COMMAND_LENGTH = 8192

_CLEAR_COMMANDS = {
    "linux": ["tput", "reset"],
    "darwin": ["tput", "reset"],
}


class CommandInjectionError(PermissionError):
    """Raised when a command contains shell metacharacters."""


class UrlValidationError(PermissionError):
    """Raised when a URL contains shell metacharacters."""


def safe_system(command: str, *, reason: str = "") -> int:
    """Execute a fixed command string through the shell safely.

    Only allows pre-defined, non-user-controlled command strings.
    Rejects any command containing shell metacharacters that could
    indicate injection.

    Args:
        command: A fixed command string (no user interpolation).
        reason: Audit justification.

    Returns:
        The exit code of the command.

    Raises:
        CommandInjectionError: If the command contains metacharacters.
        ValueError: If command is empty.
    """
    if not command or not command.strip():
        raise ValueError("command must not be empty")
    if _SHELL_META_PATTERN.search(command):
        raise CommandInjectionError(
            f"Shell metacharacters rejected in safe_system: {command[:80]}"
        )
    log.debug("safe_system: %s reason=%s", command[:80], reason)
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode


def safe_run_argv(
    argv: Sequence[str],
    *,
    timeout: float | None = None,
    capture_output: bool = True,
    check: bool = False,
    input_data: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Execute a command via subprocess without shell interpretation.

    Args:
        argv: Program and arguments as a sequence. Must not be empty.
        timeout: Optional wall-clock timeout in seconds.
        capture_output: Whether to capture stdout and stderr.
        check: Whether to raise on non-zero exit.
        input_data: Optional stdin content.

    Returns:
        CompletedProcess result.

    Raises:
        ValueError: If argv is empty.
    """
    if not argv:
        raise ValueError("argv must contain at least the program name")
    for arg in argv:
        if "\0" in arg:
            raise CommandInjectionError("Null byte in argument rejected")
    log.debug("safe_run_argv: %s", argv[0])
    return subprocess.run(
        list(argv),
        shell=False,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=check,
        input=input_data,
    )


def safe_run_shell(
    command: str,
    *,
    allow: bool = False,
    reason: str = "",
    timeout: float | None = None,
) -> subprocess.CompletedProcess[str]:
    """Execute a command through the shell, gated by policy.

    Args:
        command: The shell command to run.
        allow: Must be True to execute.
        reason: Free-text justification.
        timeout: Optional wall-clock timeout.

    Returns:
        CompletedProcess result.

    Raises:
        PermissionError: When allow is not True.
        ValueError: When allow is True but reason is empty.
    """
    if not allow:
        raise PermissionError(
            "safe_run_shell requires allow=True with a reason"
        )
    if not reason or not reason.strip():
        raise ValueError("safe_run_shell requires a non-empty reason")
    if not command or not command.strip():
        raise ValueError("command must not be empty")
    log.debug("safe_run_shell: %s reason=%s", command[:80], reason)
    return subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def safe_clear_screen() -> None:
    """Clear the terminal screen without using os.system.

    Uses tput reset via subprocess list-form, falling back to
    ANSI escape sequences when tput is unavailable.
    """
    platform_key = sys.platform
    cmd = _CLEAR_COMMANDS.get(platform_key, _CLEAR_COMMANDS["linux"])
    try:
        subprocess.run(cmd, capture_output=True, timeout=5, check=False)
    except FileNotFoundError:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def validate_url(url: str) -> str:
    """Validate a URL string, rejecting shell metacharacters.

    Args:
        url: The URL to validate.

    Returns:
        The validated URL string.

    Raises:
        UrlValidationError: If the URL contains shell metacharacters
            or does not match the expected URL pattern.
        ValueError: If the URL is empty.
    """
    if not url or not url.strip():
        raise ValueError("URL must not be empty")
    url = url.strip()
    if _SHELL_META_PATTERN.search(url):
        raise UrlValidationError(
            f"Shell metacharacters rejected in URL: {url[:80]}"
        )
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise UrlValidationError(
            f"URL scheme must be http or https, got: {parsed.scheme}"
        )
    if not parsed.netloc:
        raise UrlValidationError("URL must have a valid hostname")
    return url


def safe_git_clone(
    repo_url: str,
    target_dir: str | Path,
    *,
    timeout: float = 120,
) -> subprocess.CompletedProcess[str]:
    """Clone a git repository safely using subprocess list-form.

    Never uses os.system. Validates the URL before execution.

    Args:
        repo_url: The git repository URL (http/https only).
        target_dir: The target directory path.
        timeout: Clone timeout in seconds.

    Returns:
        CompletedProcess result.

    Raises:
        UrlValidationError: If the URL is invalid.
    """
    validated_url = validate_url(repo_url)
    target = str(target_dir)
    log.info("safe_git_clone: %s -> %s", validated_url, target)
    return subprocess.run(
        ["git", "clone", validated_url, target],
        shell=False,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def safe_ip_show(interface: str = "scope global") -> list[dict[str, str]]:
    """Parse IP addresses from ``ip show`` output in Python.

    Replaces shell pipes like ``ip a show ... | awk | grep | cut``.

    Args:
        interface: The ip show filter argument.

    Returns:
        List of dicts with 'interface' and 'address' keys.
    """
    argv = ["ip", "a", "show"] + shlex.split(interface)
    try:
        result = safe_run_argv(argv, timeout=5)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    entries: list[dict[str, str]] = []
    current_iface = ""
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if stripped and stripped[0].isdigit() and ":" in stripped:
            parts = stripped.split(":", 2)
            if len(parts) >= 2:
                current_iface = parts[1].strip().rstrip("@")
        elif stripped.startswith("inet ") and current_iface:
            addr_part = stripped.split()[1]
            addr = addr_part.split("/")[0]
            entries.append({"interface": current_iface, "address": addr})
    return entries


def safe_find_tool(name: str) -> str | None:
    """Find a tool on PATH using shutil.which.

    Replaces hardcoded paths like ``/usr/local/bin/go``.

    Args:
        name: The executable name to find.

    Returns:
        Absolute path to the tool, or None if not found.
    """
    import shutil
    return shutil.which(name)


def safe_file_read(path: str | Path, *, max_bytes: int = 10 * 1024 * 1024) -> str:
    """Read a file safely with a size limit.

    Args:
        path: File path to read.
        max_bytes: Maximum bytes to read.

    Returns:
        File contents as string.

    Raises:
        ValueError: If the file exceeds max_bytes.
        FileNotFoundError: If the file does not exist.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    size = p.stat().st_size
    if size > max_bytes:
        raise ValueError(
            f"File {path} is {size} bytes, exceeds limit {max_bytes}"
        )
    return p.read_text(encoding="utf-8")


__all__ = [
    "CommandInjectionError",
    "UrlValidationError",
    "safe_system",
    "safe_run_argv",
    "safe_run_shell",
    "safe_clear_screen",
    "validate_url",
    "safe_git_clone",
    "safe_ip_show",
    "safe_find_tool",
    "safe_file_read",
]
