"""Build-time default constants loaded from ``config/defaults.toml``.

Single source of truth for fallback ports, wordlists and well-known
paths. Commands read live engagement values from ``payload.json``
first and call these helpers only when the key is unset, so the TOML
file is never rewritten at runtime and per-engagement ``assign``
values always win.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

_DEFAULTS_PATH = Path(__file__).resolve().parent.parent / "config" / "defaults.toml"

_cache: dict[str, dict[str, Any]] = {}


def load_defaults(path: str | Path | None = None) -> dict[str, Any]:
    """Load and cache the defaults document.

    Args:
        path: TOML file to load. Defaults to ``config/defaults.toml``.

    Returns:
        Parsed TOML mapping with ``ports``, ``wordlists`` and
        ``paths`` sections.

    Raises:
        FileNotFoundError: When the TOML file does not exist.
    """
    key = str(path or _DEFAULTS_PATH)
    if key not in _cache:
        with open(key, "rb") as fh:
            data = tomllib.load(fh)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid defaults document: {key}")
        _cache[key] = data
    return _cache[key]


def clear_cache() -> None:
    """Drop cached documents (tests only)."""
    _cache.clear()


def get(section: str, key: str, default: Any = None) -> Any:
    """Return ``defaults[section][key]`` or ``default`` when absent.

    Args:
        section: TOML section (``ports``, ``wordlists``, ``paths``).
        key: Key inside the section.
        default: Fallback when section or key is missing.

    Returns:
        The configured value or ``default``.
    """
    return load_defaults().get(section, {}).get(key, default)


def default_lport() -> int:
    """Return the fallback listener port as an int.

    Returns:
        ``ports.default_lport`` (1337 unless the TOML changes it).
    """
    return int(get("ports", "default_lport", 1337))


def default_rport() -> int:
    """Return the fallback remote port as an int.

    Returns:
        ``ports.default_rport`` (443 unless the TOML changes it).
    """
    return int(get("ports", "default_rport", 443))


def rockyou_wordlist() -> str:
    """Return the default wordlist path.

    Returns:
        ``wordlists.rockyou`` unless the TOML changes it.
    """
    return str(get("wordlists", "rockyou", "/usr/share/wordlists/rockyou.txt"))


def common_wordlists() -> list[str]:
    """Return the ordered wordlist fallback candidates.

    Returns:
        ``wordlists.fallbacks`` as a list of paths.
    """
    value = get("wordlists", "fallbacks", [])
    return [str(item) for item in value]


def sessions_dir() -> str:
    """Return the sessions directory path.

    Returns:
        ``paths.sessions_dir`` (``sessions`` unless changed).
    """
    return str(get("paths", "sessions_dir", "sessions"))
