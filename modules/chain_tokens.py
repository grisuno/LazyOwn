"""Engagement-state tokens for YAML chains.

Chains reference live engagement state through tokens such as
``{ports}``, ``{services}`` and ``{password}``. This module resolves
those tokens from the fact store (``skills.lazyown_facts``) and from
sessions credential files, so operators never paste discovered data
into YAML by hand. Every produced value is untrusted: the runner keeps
these keys in its quoting set, so raw shell steps re-render them
single-quoted.
"""

from __future__ import annotations

from pathlib import Path

_TOKEN_KEYS = ("ports", "services", "username", "password", "hash", "os", "access", "creds_file", "svc_port")
_MAX_TOKEN_LENGTH = 2000
_MAX_TOKEN_ITEMS = 24
_MAX_FILES_SCAN = 48
_BASE_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"


def token_keys() -> tuple[str, ...]:
    """Return every engagement token name this module can produce."""
    return _TOKEN_KEYS


def build_tokens(target: str, params: dict | None = None) -> dict[str, str]:
    """Resolve engagement tokens for one target.

    Args:
        target: E.g. ``172.17.0.2``; empty disables resolution.
        params: Unused today; reserved so callers can extend sources.

    Returns:
        Mapping with discovered tokens only (unknown facts are absent).
        Failures never raise: an unresponsive fact store yields fewer
        tokens instead of breaking the chain run.
    """
    del params
    tokens: dict[str, str] = {}
    host = str(target or "").strip()
    if not host:
        return tokens
    facts = _load_host_facts(host)
    if facts is not None:
        ports = sorted({int(service.port) for service in facts.services if service.port})
        if ports:
            tokens["ports"] = ",".join(str(port) for port in ports[:_MAX_TOKEN_ITEMS])
            tokens["svc_port"] = str(ports[0])
        slugs = sorted({(service.service or "").split("/")[0] for service in facts.services if service.service})
        if slugs:
            tokens["services"] = " ".join(slug[:24] for slug in slugs[:_MAX_TOKEN_ITEMS])
        password_creds = [cred for cred in facts.credentials if getattr(cred, "password", "")]
        hash_creds = [cred for cred in facts.credentials if getattr(cred, "hash_value", "")]
        name_creds = [cred for cred in facts.credentials if getattr(cred, "username", "")]
        if password_creds:
            tokens["username"] = str(getattr(password_creds[0], "username", "") or "")
            tokens["password"] = str(getattr(password_creds[0], "password", "") or "")
        elif hash_creds:
            tokens["username"] = str(getattr(hash_creds[0], "username", "") or "")
            tokens["hash"] = str(getattr(hash_creds[0], "hash_value", "") or "")
        elif name_creds:
            tokens["username"] = str(getattr(name_creds[0], "username", "") or "")
        if facts.os_hint:
            tokens["os"] = str(facts.os_hint)[:120]
        access = facts.highest_access()
        if access and access != "none":
            tokens["access"] = access
    creds_file = _newest_creds_file(host)
    if creds_file:
        tokens["creds_file"] = str(creds_file)
    return {key: value[:_MAX_TOKEN_LENGTH] for key, value in tokens.items() if value}


def _load_host_facts(host: str):
    """Return one HostFacts snapshot, or None when facts are unavailable."""
    try:
        from skills.lazyown_facts import Config as FactConfig
        from skills.lazyown_facts import FactStore

        store = FactStore(cfg=FactConfig.default())
        try:
            store.parse_all(target=host)
        except Exception:
            pass
        return store.get_host(host)
    except Exception:
        return None


def _newest_creds_file(host: str) -> Path | None:
    """Return the best credential file for the host, or None.

    Preference order: file whose name AND content mention the host, then
    content-only matches, then the newest file with cred in its name.
    Encrypted files (``*.encrypted``) are skipped: their content is not
    readable without the session key.
    """
    if not _SESSIONS_DIR.is_dir() or not host:
        return None
    lowered = host.lower()
    candidates = _candidate_files()
    for path in candidates:
        if "cred" in path.name.lower() and lowered in path.name.lower() and _mentions(path, lowered):
            return path.resolve()
    for path in candidates:
        if "cred" in path.name.lower() and _mentions(path, lowered):
            return path.resolve()
    for path in candidates:
        if _mentions(path, lowered):
            return path.resolve()
    for path in candidates:
        if "cred" in path.name.lower():
            return path.resolve()
    return None


def _candidate_files() -> list[Path]:
    """Return newest-first session text files worth scanning."""
    try:
        paths = [path for path in _SESSIONS_DIR.glob("*.txt*") if path.is_file() and not path.name.endswith(".encrypted")]
    except OSError:
        return []
    paths.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return paths[:_MAX_FILES_SCAN]


def _mentions(path: Path, needle: str) -> bool:
    """Return True when a file's head contains one needle."""
    try:
        return needle in path.read_text(encoding="utf-8", errors="replace")[:65536].lower()
    except OSError:
        return False


__all__ = ["build_tokens", "token_keys"]
