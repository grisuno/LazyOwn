"""Prompt builder for LazyOwn CLI and C2 dashboard banner.

Exposes :func:`getprompt` which returns the coloured status line shown
in both the CLI header and the C2 web dashboard. Extracted from
``utils.py`` to break the 3358-line monolith.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from core.config import load_payload


def _load_prompt_payload() -> dict:
    """Load ``payload.json`` and return a dict with default values.

    Returns:
        Dict with ``lhost``, ``rhost``, ``domain``, ``api_key`` keys.
    """
    try:
        data = load_payload()
    except Exception:
        data = {}
    return {
        "lhost": data.get("lhost", "127.0.0.1"),
        "rhost": data.get("rhost", ""),
        "domain": data.get("domain", ""),
        "api_key": data.get("api_key", ""),
    }


def get_git_info() -> str:
    """Return current git branch and dirty-status for the prompt.

    Returns an empty string if git is not available or the working
    tree is not a git repo.
    """
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=3,
        ).stdout.strip()
        dirty = "*" if status else ""
        return f"{branch}{dirty}"
    except Exception:
        return ""


def get_venv_info() -> str:
    """Return the active virtualenv name, or empty string if none."""
    venv = os.environ.get("VIRTUAL_ENV", "")
    if venv:
        return str(Path(venv).name)
    return ""


def get_kernel() -> str:
    """Return the running kernel version (short form)."""
    try:
        import platform
        return platform.release()
    except Exception:
        return "unknown"


def get_terminal_size() -> tuple[int, int]:
    """Return ``(width, height)`` of the terminal, defaulting to 80x24."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except (OSError, ValueError):
        return 80, 24


def get_local_ips() -> str:
    """Return a comma-separated string of non-loopback IPv4 addresses."""
    import socket
    try:
        import netifaces
        ips = []
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            for addr in addrs.get(socket.AF_INET, []):
                ip = addr.get("addr", "")
                if ip and not ip.startswith("127."):
                    ips.append(ip)
        return ", ".join(ips)
    except ImportError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return ""


def copy2clip(text: str) -> bool:
    """Copy ``text`` to the system clipboard via xclip.

    Returns True on success, False if xclip is unavailable.
    """
    try:
        proc = subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text, text=True, capture_output=True, timeout=3,
        )
        return proc.returncode == 0
    except Exception:
        return False


def getprompt() -> str:
    """Build the coloured status line for the CLI header and C2 dashboard.

    Returns a Rich-formatted string containing the current session
    context: operator@host, network interfaces, target, domain, git
    branch, virtualenv, and timestamp.

    Returns:
        A Rich-console compatible string.
    """
    payload = _load_prompt_payload()

    import socket as _socket
    import time as _time

    hostname = _socket.gethostname()
    user = os.environ.get("USER", os.environ.get("USERNAME", "operator"))

    lhost = payload.get("lhost", "127.0.0.1")
    rhost = payload.get("rhost", "")
    domain = payload.get("domain", "")

    git_info = get_git_info()
    venv_info = get_venv_info()
    ts = _time.strftime("%H:%M:%S")

    parts = [
        f"[bold bright_green]{user}@{hostname}[/]",
        f"[bright_cyan]{lhost}[/]",
    ]

    if rhost:
        parts.append(f"[bold bright_red]target={rhost}[/]")
    if domain:
        parts.append(f"[bright_yellow]domain={domain}[/]")
    if git_info:
        parts.append(f"[bright_yellow]git:{git_info}[/]")
    if venv_info:
        parts.append(f"[bright_blue]venv:{venv_info}[/]")
    parts.append(f"[bright_cyan]{ts}[/]")

    return " | ".join(parts)
