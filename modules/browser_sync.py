"""Browser identity sync between the operator browser and the recorder proxy.

A Chrome/Brave extension (``browser_sync_extension/``) pushes the real
cookie store plus fingerprint headers (user agent, languages, client
hints) to a local, token-authenticated receiver exposed by this module.
The recorder proxy (:mod:`modules.lazy_proxy`) then calls
:func:`apply_identity_headers` on every forwarded exchange so the
autonomous loop, ``apt_chain`` and ``auto_pwn`` reuse the genuine browser
session instead of fingerprint-breaking anonymous requests.

Burp-style "Match and Replace" rules live in ``sessions/browser_sync/rules.json``
and are applied after the identity headers, letting the operator rewrite
any header or body region of the proxied traffic.

Security contract: the receiver binds loopback only, requires a runtime
generated token, caps request size, sanitises every stored header value
and never raises on I/O; a broken sync degrades to anonymous traffic.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DEFAULT_SYNC_HOST = "127.0.0.1"
DEFAULT_SYNC_PORT = 8898
SYNC_DIR_NAME = "browser_sync"
ENDPOINT_PATH = "/__lazyown/sync"
HEALTH_PATH = "/__lazyown/health"
TOKEN_HEADER = "X-LazyOwn-Token"
TOKEN_BYTES = 24
MAX_SYNC_BODY = 8_000_000
MAX_SYNC_DRAIN = 32_000_000
MAX_COOKIES = 8000
MAX_COOKIE_VALUE = 8192
MAX_HEADER_VALUE = 8192
MAX_RULES = 200
PROFILE_TTL_SEC = 0.0
DEFAULT_INJECT = True
INJECTABLE_HEADER_PREFIXES = ("sec-ch-ua", "accept-language", "user-agent", "cookie")

_SESSIONS_DIR = Path(os.environ.get("LAZYOWN_SESSIONS_DIR", "")) if os.environ.get("LAZYOWN_SESSIONS_DIR") else None
_PAYLOAD_PATH = Path(os.environ.get("LAZYOWN_PAYLOAD_PATH", "payload.json"))

_FORBIDDEN_HEADER_CHARS = ("\r", "\n", "\x00")
_COOKIE_KEYS = (
    "domain",
    "name",
    "value",
    "path",
    "secure",
    "httpOnly",
    "hostOnly",
    "session",
    "sameSite",
    "expirationDate",
)

log = __import__("logging").getLogger("modules.browser_sync")


def _sessions_dir() -> Path:
    """Return the browser sync directory under sessions."""
    base = _SESSIONS_DIR or Path("sessions")
    return base / SYNC_DIR_NAME


def _profile_path() -> Path:
    """Return the profile JSON path."""
    return _sessions_dir() / "profile.json"


def _jar_path() -> Path:
    """Return the Netscape cookie jar path."""
    return _sessions_dir() / "cookies.jar"


def _rules_path() -> Path:
    """Return the Match and Replace rules path."""
    return _sessions_dir() / "rules.json"


def _token_path() -> Path:
    """Return the receiver token path."""
    return _sessions_dir() / "token"


def _sanitize_header_value(value: Any) -> str:
    """Strip CR, LF and NUL from a header value.

    Args:
        value: Raw header value of any type.

    Returns:
        Safe printable string, at most ``MAX_HEADER_VALUE`` chars.
    """
    text = str(value or "")
    for forbidden in _FORBIDDEN_HEADER_CHARS:
        text = text.replace(forbidden, "")
    return text[:MAX_HEADER_VALUE]


def token(create: bool = True) -> str:
    """Return the receiver auth token, generating it on first use.

    Args:
        create: When False, return an empty string instead of creating.

    Returns:
        The hex token, or an empty string when absent and ``create`` is False.
    """
    path = _token_path()
    try:
        if path.is_file():
            text = path.read_text(encoding="utf-8").strip()
            if text:
                return text
        if not create:
            return ""
        path.parent.mkdir(parents=True, exist_ok=True)
        value = secrets.token_hex(TOKEN_BYTES)
        path.write_text(value + "\n", encoding="utf-8")
        os.chmod(path, 0o600)
        return value
    except OSError:
        return ""


def reset_token() -> str:
    """Regenerate the receiver token.

    Returns:
        The new hex token.
    """
    try:
        _token_path().unlink(missing_ok=True)
    except OSError:
        pass
    return token()


def load_profile() -> dict[str, Any]:
    """Load the last synced browser identity profile.

    Returns:
        The profile dict, or an empty dict when absent or corrupt.
    """
    path = _profile_path()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def profile_stats() -> dict[str, Any]:
    """Summarise the synced profile.

    Returns:
        Dict with cookie count, distinct domains, age seconds and sync time.
    """
    profile = load_profile()
    cookies = profile.get("cookies") or []
    domains = sorted({str(c.get("domain") or "").lstrip(".") for c in cookies if c.get("domain")})
    synced_at = float(profile.get("synced_at") or 0.0)
    return {
        "cookies": len(cookies),
        "domains": domains,
        "age_sec": max(0.0, time.time() - synced_at) if synced_at else 0.0,
        "synced_at": synced_at,
        "user_agent": _sanitize_header_value(profile.get("user_agent") or ""),
    }


def cookie_matches_host(cookie: dict[str, Any], host: str) -> bool:
    """Return True when a synced cookie applies to a request host.

    Args:
        cookie: Synced cookie dict with ``domain`` and optional ``hostOnly``.
        host: Request host (no port, no brackets).

    Returns:
        True on exact host match (hostOnly) or domain suffix match.
    """
    domain = str(cookie.get("domain") or "").strip().lstrip(".").lower()
    target = str(host or "").strip().strip("[]").lower()
    if not domain or not target:
        return False
    if cookie.get("hostOnly"):
        return domain == target
    return target == domain or target.endswith("." + domain)


def cookie_matches_path(cookie: dict[str, Any], request_path: str) -> bool:
    """Return True when a synced cookie applies to one request path.

    RFC 6265 path-match: equal path, or the cookie path is a prefix of the
    request path and either ends with a slash or is followed by a slash.

    Args:
        cookie: Synced cookie dict with ``path`` (default ``/``).
        request_path: Request path including the query-stripped location.

    Returns:
        True when the browser would send this cookie for the path.
    """
    cookie_path = str(cookie.get("path") or "/") or "/"
    target = str(request_path or "/").split("?")[0] or "/"
    if not target.startswith("/"):
        target = "/" + target
    if target == cookie_path:
        return True
    return target.startswith(cookie_path) and (
        cookie_path.endswith("/") or target[len(cookie_path)] == "/"
    )


def cookie_expired(cookie: dict[str, Any], now: float | None = None) -> bool:
    """Return True when a persistent cookie is already expired.

    Session cookies (no ``expirationDate``) never expire here; the next
    sync replaces the whole store anyway.

    Args:
        cookie: Synced cookie dict.
        now: Reference timestamp, defaults to current time.

    Returns:
        True when the cookie must not be sent.
    """
    expiry = cookie.get("expirationDate")
    if expiry is None:
        return False
    try:
        return float(expiry) <= (time.time() if now is None else now)
    except (TypeError, ValueError):
        return False


def cookies_for_host(
    profile: dict[str, Any],
    host: str,
    path: str = "/",
    scheme: str = "https",
) -> list[dict[str, Any]]:
    """Return synced cookies a browser would send for one request.

    Filters by host match, RFC path match, ``Secure`` only over https and
    expiry, exactly like a browser would.

    Args:
        profile: Synced profile dict.
        host: Request host.
        path: Request path (query included or not).
        scheme: Request scheme; ``Secure`` cookies only apply to https.

    Returns:
        List of cookie dicts, longest domain match first.
    """
    secure_ok = str(scheme or "https").lower() == "https"
    matched = [
        cookie
        for cookie in (profile.get("cookies") or [])
        if cookie_matches_host(cookie, host)
        and cookie_matches_path(cookie, path)
        and not cookie_expired(cookie)
        and (secure_ok or not cookie.get("secure"))
    ]
    matched.sort(key=lambda c: len(str(c.get("domain") or "")), reverse=True)
    return matched


def build_cookie_header(existing: str, cookies: list[dict[str, Any]]) -> str:
    """Merge synced cookies into an existing Cookie header.

    Synced names win over names already present; unrelated existing
    cookies are preserved.

    Args:
        existing: Current Cookie header value (may be empty).
        cookies: Synced cookies for this host.

    Returns:
        The merged Cookie header value.
    """
    existing_pairs: dict[str, str] = {}
    for pair in str(existing or "").split(";"):
        name, _, value = pair.partition("=")
        name = name.strip()
        if name:
            existing_pairs[name] = value.strip()
    merged: dict[str, str] = {}
    for cookie in cookies:
        name = str(cookie.get("name") or "").strip()
        value = str(cookie.get("value") or "")
        if not name or not value:
            continue
        merged[name] = value[:MAX_COOKIE_VALUE]
    for name, value in existing_pairs.items():
        if name not in merged:
            merged[name] = value
    return "; ".join(f"{name}={value}" for name, value in merged.items())


def _netscape_line(cookie: dict[str, Any]) -> str:
    """Render one Netscape cookie jar line.

    Args:
        cookie: Synced cookie dict.

    Returns:
        Seven tab separated fields, expiry 0 for session cookies.
    """
    domain = str(cookie.get("domain") or "").lstrip(".")
    include_sub = "FALSE" if cookie.get("hostOnly") else ("TRUE" if domain else "FALSE")
    path = str(cookie.get("path") or "/")
    secure = "TRUE" if cookie.get("secure") else "FALSE"
    expiry = cookie.get("expirationDate")
    try:
        expires = str(int(float(expiry))) if expiry else "0"
    except (TypeError, ValueError):
        expires = "0"
    name = str(cookie.get("name") or "")
    value = str(cookie.get("value") or "").replace("\t", " ").replace("\n", " ").replace("\r", " ")
    return f"{domain}\t{include_sub}\t{path}\t{secure}\t{expires}\t{name}\t{value}"


def write_netscape_jar(profile: dict[str, Any], path: str | Path | None = None) -> int:
    """Write the synced cookie store as a Netscape cookie jar.

    Args:
        profile: Synced profile dict.
        path: Destination override; defaults to ``sessions/browser_sync/cookies.jar``.

    Returns:
        Number of jar lines written, or 0 on I/O failure.
    """
    destination = Path(path) if path else _jar_path()
    lines = [_netscape_line(c) for c in (profile.get("cookies") or []) if c.get("name")]
    header = "# Netscape HTTP Cookie File\n# Generated by LazyOwn browser_sync\n"
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(header + "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        os.chmod(destination, 0o600)
        return len(lines)
    except OSError:
        return 0


def jar_path() -> str:
    """Return the cookie jar path as a string."""
    return str(_jar_path())


def _load_rules_cached() -> list[dict[str, Any]]:
    """Load Burp-style rules with an mtime keyed cache."""
    path = _rules_path()
    try:
        stat = path.stat()
    except OSError:
        _RULES_CACHE.clear()
        return []
    key = (str(path), stat.st_mtime_ns, stat.st_size)
    cached = _RULES_CACHE.get("key")
    if cached == key:
        return _RULES_CACHE.get("rules") or []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        rules = data if isinstance(data, list) else (data.get("rules") or [])
        rules = rules[:MAX_RULES] if isinstance(rules, list) else []
    except (OSError, ValueError):
        rules = []
    _RULES_CACHE["key"] = key
    _RULES_CACHE["rules"] = rules
    return rules


_RULES_CACHE: dict[str, Any] = {}


def _read_payload_cached() -> dict[str, Any]:
    """Read payload.json flags with a small TTL cache."""
    now = time.time()
    cached = _PAYLOAD_CACHE.get("ts") or 0.0
    if now - cached < 2.0:
        return _PAYLOAD_CACHE.get("params") or {}
    try:
        params = json.loads(_PAYLOAD_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        params = {}
    _PAYLOAD_CACHE["ts"] = now
    _PAYLOAD_CACHE["params"] = params
    return params


_PAYLOAD_CACHE: dict[str, Any] = {}

WIRING_ENABLED = True


def _payload_inject_enabled() -> bool:
    """Read the ``browser_sync_inject`` payload flag with a small TTL cache."""
    return bool(_read_payload_cached().get("browser_sync_inject", DEFAULT_INJECT))


def apply_rules(headers: dict[str, str], body: bytes) -> tuple[dict[str, str], bytes, int]:
    """Apply Burp-style Match and Replace rules to request headers and body.

    Rule types: ``header_replace`` (regex over the header value of a
    matching header name), ``header_add`` (only when the name is absent),
    ``header_set`` (add or overwrite), ``header_remove`` and
    ``body_replace`` (regex over bytes). The ``Host`` header is never
    rewritten; values are sanitised and capped.

    Args:
        headers: Mutable request header dict.
        body: Raw request body bytes.

    Returns:
        Tuple of (headers, body, applied rule count).
    """
    applied = 0
    for rule in _load_rules_cached():
        if not isinstance(rule, dict) or rule.get("enabled") is False:
            continue
        kind = str(rule.get("type") or "header_replace")
        match = str(rule.get("match") or "")
        replace = _sanitize_header_value(rule.get("replace"))
        try:
            if kind == "header_replace" and match:
                pattern = re.compile(match, re.IGNORECASE)
                for name, value in list(headers.items()):
                    if name.lower() == "host":
                        continue
                    new_value = pattern.sub(replace, value)
                    if new_value != value:
                        headers[name] = new_value
                        applied += 1
            elif kind == "header_add" and match:
                if not any(name.lower() == match.lower() for name in headers):
                    headers[match] = replace
                    applied += 1
            elif kind == "header_set" and match:
                headers[match] = replace
                applied += 1
            elif kind == "header_remove" and match:
                lowered = match.lower()
                for name in list(headers):
                    if name.lower() == lowered:
                        del headers[name]
                        applied += 1
            elif kind == "body_replace" and match and body:
                pattern = re.compile(match.encode("utf-8"))
                new_body, count = pattern.subn(replace.encode("utf-8"), body)
                if count:
                    body = new_body
                    applied += count
        except (re.error, ValueError):
            continue
    return headers, body, applied


def apply_identity_headers(
    host: str,
    headers: dict[str, str],
    body: bytes = b"",
    path: str = "/",
    scheme: str = "https",
) -> tuple[dict[str, str], bytes]:
    """Inject the synced browser identity into one proxied request.

    Order: synced cookies and fingerprint headers for ``host``, then
    Burp-style rules. Cookie selection honours the RFC path match, the
    ``Secure`` flag against ``scheme`` and expiry, like a browser would.
    Disabled (``browser_sync_inject`` false) or empty profiles leave the
    request untouched; the function never raises.

    Args:
        host: Upstream request host.
        headers: Mutable request header dict.
        body: Raw request body bytes.
        path: Request path.
        scheme: Request scheme.

    Returns:
        Tuple of (headers, body) after identity and rule application.
    """
    try:
        if not _payload_inject_enabled():
            return headers, body
        profile = _profile_cache_get()
        if not profile:
            return headers, body
        lowered = {name.lower(): name for name in headers}
        if lowered.get("cookie") and not str(headers.get(lowered["cookie"]) or "").strip():
            del headers[lowered["cookie"]]
            lowered.pop("cookie", None)
        matched = cookies_for_host(profile, host, path, scheme)
        if matched:
            existing = headers.get(lowered.get("cookie", "Cookie"), "")
            merged = build_cookie_header(existing, matched)
            if merged:
                headers["Cookie"] = merged
        user_agent = _sanitize_header_value(profile.get("user_agent"))
        if user_agent:
            headers["User-Agent"] = user_agent
        languages = profile.get("languages")
        if isinstance(languages, list) and languages:
            headers["Accept-Language"] = ",".join(str(v) for v in languages[:8])
        hints = profile.get("client_hints")
        if isinstance(hints, dict):
            for name, value in hints.items():
                safe_name = _sanitize_header_value(name)
                safe_value = _sanitize_header_value(value)
                if safe_name and safe_value and safe_name.lower().startswith(INJECTABLE_HEADER_PREFIXES):
                    headers[safe_name] = safe_value
        headers, body, applied = apply_rules(headers, body)
        if applied:
            length = len(body)
            for name in list(headers):
                if name.lower() == "content-length":
                    headers[name] = str(length)
        return headers, body
    except Exception:
        return headers, body


_PROFILE_CACHE: dict[str, Any] = {"mtime_ns": 0, "profile": {}}


def _profile_cache_get() -> dict[str, Any]:
    """Return the profile with an mtime keyed cache."""
    path = _profile_path()
    try:
        stat = path.stat()
    except OSError:
        _PROFILE_CACHE["mtime_ns"] = 0
        _PROFILE_CACHE["profile"] = {}
        return {}
    if stat.st_mtime_ns != _PROFILE_CACHE["mtime_ns"]:
        try:
            profile = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            profile = {}
        _PROFILE_CACHE["mtime_ns"] = stat.st_mtime_ns
        _PROFILE_CACHE["profile"] = profile if isinstance(profile, dict) else {}
    return _PROFILE_CACHE["profile"]


def _clean_cookie(raw: Any) -> dict[str, Any] | None:
    """Whitelist and cap one extension cookie object.

    Args:
        raw: Arbitrary parsed JSON cookie value.

    Returns:
        Clean cookie dict, or None when the shape is invalid.
    """
    if not isinstance(raw, dict):
        return None
    name = str(raw.get("name") or "").strip()
    value = str(raw.get("value") or "")[:MAX_COOKIE_VALUE]
    if not name or not value:
        return None
    clean: dict[str, Any] = {"name": name, "value": value}
    for key in ("domain", "path", "sameSite"):
        if raw.get(key) is not None:
            clean[key] = str(raw[key])[:255]
    for key in ("secure", "httpOnly", "hostOnly", "session"):
        if key in raw:
            clean[key] = bool(raw[key])
    if raw.get("expirationDate") is not None:
        try:
            clean["expirationDate"] = float(raw["expirationDate"])
        except (TypeError, ValueError):
            pass
    return clean


class SyncReceiver:
    """Token-authenticated loopback receiver for the browser extension."""

    def __init__(self, host: str = DEFAULT_SYNC_HOST, port: int = DEFAULT_SYNC_PORT) -> None:
        """Prepare state; nothing binds until :meth:`start`.

        Args:
            host: Bind address.
            port: Bind port (0 picks a free one).
        """
        self._host = host
        self._port = int(port)
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._last_sync = 0.0
        self._sync_count = 0

    def start(self, host: str | None = None, port: int | None = None) -> dict[str, Any]:
        """Bind the receiver; idempotent while already running.

        Args:
            host: Bind address override (None keeps the current one).
            port: Bind port override (None or 0 keeps the current one
                when already running, otherwise picks a free one).

        Returns:
            Status dict with running state, address and profile stats.
        """
        with self._lock:
            if host is not None:
                self._host = host
            if port is not None:
                if self._server is None or int(port) > 0:
                    self._port = int(port)
            if self._server is not None:
                return self.status()
            token()
            receiver = self

            class _Handler(BaseHTTPRequestHandler):
                """Serve the sync endpoint for the extension service worker."""

                protocol_version = "HTTP/1.1"
                server_version = "LazyOwnBrowserSync/1.0"

                def log_message(self, fmt, *args):
                    """Silence per-request logging; the profile is the audit trail."""
                    return None

                def do_GET(self):
                    """Answer the health probe."""
                    if (self.path or "").split("?")[0] == HEALTH_PATH:
                        body = json.dumps({"ok": True}).encode()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)
                        return
                    self.send_error(404)

                def do_POST(self):
                    """Accept one identity sync push."""
                    if (self.path or "").split("?")[0] != ENDPOINT_PATH:
                        self.send_error(404)
                        return
                    supplied = str(self.headers.get(TOKEN_HEADER) or "")
                    expected = token()
                    if not expected or not hmac.compare_digest(supplied, expected):
                        self._reply(401, {"error": "unauthorized"})
                        return
                    try:
                        length = int(self.headers.get("Content-Length") or 0)
                    except ValueError:
                        length = 0
                    if length <= 0 or length > MAX_SYNC_BODY:
                        self._drain(length)
                        self._reply(413, {"error": "body size rejected"})
                        return
                    raw = self.rfile.read(length)
                    try:
                        data = json.loads(raw)
                    except ValueError:
                        self._reply(400, {"error": "invalid json"})
                        return
                    stored = receiver._store(data)
                    if stored is None:
                        self._reply(400, {"error": "invalid profile"})
                        return
                    receiver._last_sync = time.time()
                    receiver._sync_count += 1
                    self._reply(200, {"ok": True, "cookies": stored})

                def _drain(self, length: int) -> None:
                    """Discard an oversized body so the client can read the reply."""
                    remaining = min(length, MAX_SYNC_DRAIN)
                    try:
                        while remaining > 0:
                            chunk = self.rfile.read(min(65536, remaining))
                            if not chunk:
                                break
                            remaining -= len(chunk)
                    except OSError:
                        self.close_connection = True

                def _reply(self, code: int, payload: dict[str, Any]) -> None:
                    """Send one JSON reply; a gone client is never an exception."""
                    body = json.dumps(payload).encode()
                    try:
                        self.send_response(code)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        self.close_connection = True

            self._server = ThreadingHTTPServer((self._host, self._port), _Handler)
            self._port = int(self._server.server_address[1])
            self._thread = threading.Thread(target=self._server.serve_forever, name="lazy-browser-sync", daemon=True)
            self._thread.start()
            return self.status()

    def _store(self, data: Any) -> int | None:
        """Persist one sync payload as profile plus Netscape jar.

        Args:
            data: Parsed extension payload.

        Returns:
            Stored cookie count, or None when the shape is invalid.
        """
        if not isinstance(data, dict):
            return None
        cookies_raw = data.get("cookies")
        if not isinstance(cookies_raw, list):
            return None
        cookies = [clean for raw in cookies_raw[:MAX_COOKIES] if (clean := _clean_cookie(raw))]
        profile = {
            "synced_at": time.time(),
            "user_agent": _sanitize_header_value(data.get("user_agent")),
            "languages": [str(v)[:64] for v in data.get("languages") or []][:8] if isinstance(data.get("languages"), list) else [],
            "client_hints": {
                _sanitize_header_value(k): _sanitize_header_value(v)
                for k, v in (data.get("client_hints") or {}).items()
                if isinstance(data.get("client_hints"), dict)
                and _sanitize_header_value(k).lower().startswith(INJECTABLE_HEADER_PREFIXES)
            },
            "cookies": cookies,
        }
        path = _profile_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(profile, indent=2), encoding="utf-8")
            os.chmod(tmp, 0o600)
            os.replace(tmp, path)
        except OSError:
            return None
        write_netscape_jar(profile)
        return len(cookies)

    def stop(self) -> dict[str, Any]:
        """Shut the receiver down; safe when it was never started."""
        with self._lock:
            server, thread = self._server, self._thread
            self._server = None
            self._thread = None
        if server is not None:
            try:
                server.shutdown()
                server.server_close()
            except Exception:
                pass
        if thread is not None:
            thread.join(timeout=5.0)
        return self.status()

    def status(self) -> dict[str, Any]:
        """Report running state, address, token and profile stats."""
        stats = profile_stats()
        running = self._server is not None
        return {
            "running": running,
            "host": self._host,
            "port": self._port if running else 0,
            "endpoint": f"http://{self._host}:{self._port}{ENDPOINT_PATH}" if running else "",
            "token": token() if running else "",
            "syncs": self._sync_count,
            "last_sync": self._last_sync,
            **stats,
        }


_RECEIVER: SyncReceiver | None = None
_RECEIVER_LOCK = threading.Lock()


def get_receiver() -> SyncReceiver:
    """Return the process-wide shared receiver instance."""
    global _RECEIVER
    with _RECEIVER_LOCK:
        if _RECEIVER is None:
            _RECEIVER = SyncReceiver()
        return _RECEIVER


def start_receiver(port: int = DEFAULT_SYNC_PORT, host: str = DEFAULT_SYNC_HOST) -> dict[str, Any]:
    """Start the shared receiver.

    Args:
        port: Bind port (None/0 keeps the running port or picks a free one).
        host: Bind address.

    Returns:
        Receiver status dict.
    """
    return get_receiver().start(host=host, port=port)


def stop_receiver() -> dict[str, Any]:
    """Stop the shared receiver.

    Returns:
        Receiver status dict.
    """
    return get_receiver().stop()


def clear_profile() -> dict[str, Any]:
    """Delete the synced profile and cookie jar.

    Returns:
        Dict with the removed artefact names.
    """
    removed: list[str] = []
    for path in (_profile_path(), _jar_path()):
        try:
            path.unlink(missing_ok=True)
            removed.append(path.name)
        except OSError:
            continue
    _PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
    return {"removed": removed}


def apply_identity_to_url(url: str, headers: dict[str, str], body: bytes | None = None) -> tuple[dict[str, str], bytes]:
    """Apply the synced browser identity to one URL-scoped request.

    URL variant of :func:`apply_identity_headers` for modules that speak
    HTTP with a full URL (requests-based tools such as the lazy burp
    fuzzer). Same merge rules, same fail-soft contract; rules may rewrite
    the body.

    Args:
        url: Absolute target URL.
        headers: Mutable request header dict.
        body: Raw request body bytes (None means empty).

    Returns:
        Tuple of (headers, body) after identity and rule application.
    """
    from urllib.parse import urlsplit

    parts = urlsplit(url)
    host = parts.hostname or ""
    scheme = parts.scheme or "http"
    target = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
    return apply_identity_headers(host, headers, body if body is not None else b"", path=target, scheme=scheme)


def ensure_wiring() -> dict[str, Any]:
    """Start the receiver and route framework traffic through the recorder proxy.

    Payload-driven (``proxy_autostart``, ``proxy_port``, ``proxy_upstream``,
    ``browser_sync_enabled``, ``browser_sync_port``), idempotent and
    fail-soft. Once the proxy env is applied, every ``run_command``
    subprocess (curl in the loop, apt_chain steps, the burp fuzzer) and
    every in-process ``requests`` call inherit the routing and receive the
    synced browser identity.

    Returns:
        Dict with ``receiver`` and ``proxy`` status sub-dicts.
    """
    if not WIRING_ENABLED:
        return {"receiver": {}, "proxy": {}, "disabled": True}
    params = _read_payload_cached()
    result: dict[str, Any] = {"receiver": {}, "proxy": {}}
    if bool(params.get("browser_sync_enabled", True)):
        try:
            port = int(params.get("browser_sync_port", DEFAULT_SYNC_PORT) or DEFAULT_SYNC_PORT)
        except (TypeError, ValueError):
            port = DEFAULT_SYNC_PORT
        try:
            result["receiver"] = start_receiver(port=port)
        except Exception as exc:
            result["receiver"] = {"running": False, "error": str(exc)[:200]}
    if bool(params.get("proxy_autostart", True)):
        try:
            from modules import lazy_proxy

            try:
                port = int(params.get("proxy_port") or 0)
            except (TypeError, ValueError):
                port = 0
            status = lazy_proxy.get_proxy().start(port=port, upstream=str(params.get("proxy_upstream") or ""))
            lazy_proxy.apply_env(status.get("ca_path", ""), status.get("host", ""), status.get("port", 0))
            result["proxy"] = status
        except Exception as exc:
            result["proxy"] = {"running": False, "error": str(exc)[:200]}
    return result


def masked_rows(profile: dict[str, Any], domain_filter: str = "", full: bool = False) -> list[str]:
    """Render synced cookies as display rows with masked values.

    Args:
        profile: Synced profile dict.
        domain_filter: Optional substring filter on the cookie domain.
        full: When True, show raw values (operator explicitly requested).

    Returns:
        One ``domain name value`` row per matching cookie.
    """
    rows: list[str] = []
    for cookie in profile.get("cookies") or []:
        domain = str(cookie.get("domain") or "")
        name = str(cookie.get("name") or "")
        value = str(cookie.get("value") or "")
        if domain_filter and domain_filter.lower() not in domain.lower():
            continue
        shown = value if full else (value[:4] + "..." + hashlib.sha256(value.encode()).hexdigest()[:6]) if value else ""
        rows.append(f"{domain}  {name}  {shown}")
    return rows
