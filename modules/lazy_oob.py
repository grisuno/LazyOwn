"""Local OOB canary for blind SSRF/RCE detection.

Starts an HTTP listener bound to the operator's ``lhost`` and serves
unique token paths (``/oob/<token>``). Attack payloads reference the
canary URL; any callback proves code execution or server-side request
forgery. Hits are recorded in memory and mirrored to
``sessions/oob_hits.jsonl``. The listener never parses, execs or proxies
anything: it only records that a request arrived.

>>> from modules import lazy_oob
>>> canary = lazy_oob.start()
>>> canary.url()
'http://127.0.0.1:<port>/oob/<token>'
>>> lazy_oob.stop()
"""

from __future__ import annotations

import json
import secrets
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
HITS_PATH = BASE_DIR / "sessions" / "oob_hits.jsonl"
DEFAULT_BIND_HOST = "127.0.0.1"
DEFAULT_PORT = 0
TOKEN_BYTES = 8
MAX_TOKENS = 64
MAX_HITS = 2000

_LOCK = threading.Lock()
_STATE: dict[str, Any] = {"server": None, "thread": None, "tokens": [], "hits": []}


@dataclass
class OobHit:
    """One callback observed by the canary."""

    token: str
    path: str
    source: str
    method: str
    at: float
    headers: dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return the JSON-serialisable row."""
        return {
            "token": self.token,
            "path": self.path,
            "source": self.source,
            "method": self.method,
            "at": self.at,
            "headers": self.headers,
        }


class _CanaryHandler(BaseHTTPRequestHandler):
    """Record-only request handler: no parsing, no proxying, no exec."""

    def _record(self) -> None:
        token = ""
        parts = self.path.split("/")
        if len(parts) >= 3 and parts[1] == "oob":
            token = parts[2]
        headers = {key.lower(): value for key, value in list(self.headers.items())[:8]}
        hit = OobHit(
            token=token,
            path=self.path[:256],
            source=self.client_address[0] if self.client_address else "",
            method=self.command,
            at=time.time(),
            headers=headers,
        )
        record_hit(hit)

    def _respond(self) -> None:
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")
        except Exception:
            pass

    def do_GET(self) -> None:
        """Record a GET callback."""
        self._record()
        self._respond()

    def do_POST(self) -> None:
        """Record a POST callback (body discarded)."""
        self._record()
        self._respond()

    def do_HEAD(self) -> None:
        """Record a HEAD callback."""
        self._record()
        self._respond()

    def log_message(self, fmt: str, *args: Any) -> None:
        """Silence the default stderr access log."""
        return


def record_hit(hit: OobHit) -> None:
    """Store one hit in memory and append it to the JSONL mirror.

    Args:
        hit: The observed callback.
    """
    with _LOCK:
        _STATE["hits"] = (list(_STATE["hits"]) + [hit])[-MAX_HITS:]
    try:
        HITS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with HITS_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(hit.as_dict()) + "\n")
    except Exception:
        pass


def start(host: str = "", port: int = DEFAULT_PORT) -> dict[str, Any]:
    """Start (or reuse) the canary listener.

    Args:
        host: Bind address; empty binds to ``lhost`` from payload.json,
            falling back to loopback.
        port: Bind port; 0 picks a free ephemeral port.

    Returns:
        Mapping with ``ok``, ``token``, ``port``, ``url`` and ``error``.
    """
    bind = str(host or "").strip() or _configured_lhost() or DEFAULT_BIND_HOST
    with _LOCK:
        server = _STATE.get("server")
        if server is not None:
            token = _STATE["tokens"][-1] if _STATE["tokens"] else new_token()
            return {
                "ok": True,
                "already": True,
                "token": token,
                "port": server.server_address[1],
                "url": f"http://{bind}:{server.server_address[1]}/oob/{token}",
                "error": "",
            }
    try:
        httpd = ThreadingHTTPServer((bind, port), _CanaryHandler)
    except Exception as exc:
        return {"ok": False, "token": "", "port": 0, "url": "", "error": str(exc)}
    token = new_token()
    thread = threading.Thread(target=httpd.serve_forever, name="lazyoob-canary", daemon=True)
    thread.start()
    with _LOCK:
        _STATE["server"] = httpd
        _STATE["thread"] = thread
        _STATE["tokens"] = (list(_STATE["tokens"]) + [token])[-MAX_TOKENS:]
        bound_port = int(httpd.server_address[1])
    return {"ok": True, "already": False, "token": token, "port": bound_port, "url": f"http://{bind}:{bound_port}/oob/{token}", "error": ""}


def new_token() -> str:
    """Return one URL-safe callback token."""
    return secrets.token_hex(TOKEN_BYTES)


def _configured_lhost() -> str:
    """Read ``lhost`` from payload.json without importing the shell."""
    try:
        import json as _json

        payload = BASE_DIR / "payload.json"
        data = _json.loads(payload.read_text(encoding="utf-8", errors="replace"))
        return str(data.get("lhost") or "").strip()
    except Exception:
        return ""


def url(token: str = "") -> str:
    """Return the callback URL for a token (latest when omitted).

    Args:
        token: Explicit token; empty reuses the latest active token.

    Returns:
        The URL string, or empty when the canary is not running.
    """
    with _LOCK:
        server = _STATE.get("server")
        if server is None:
            return ""
        chosen = str(token or "").strip() or (_STATE["tokens"][-1] if _STATE["tokens"] else "")
        if not chosen:
            return ""
        bind = server.server_address[0] or DEFAULT_BIND_HOST
        return f"http://{bind}:{server.server_address[1]}/oob/{chosen}"


def hits(token: str = "") -> list[dict[str, Any]]:
    """Return recorded hits, optionally filtered by token.

    Args:
        token: Filter token; empty returns every hit.

    Returns:
        Hit dicts, newest last.
    """
    with _LOCK:
        rows = [hit.as_dict() for hit in _STATE["hits"]]
    if token:
        rows = [row for row in rows if row["token"] == token]
    return rows


def stop() -> dict[str, Any]:
    """Shut the canary down and report how many hits it saw.

    Returns:
        Mapping with ``ok``, ``hits`` and ``error``.
    """
    with _LOCK:
        server = _STATE.get("server")
        count = len(_STATE["hits"])
        _STATE["server"] = None
        _STATE["thread"] = None
    if server is None:
        return {"ok": True, "hits": count, "error": "not running"}
    try:
        server.shutdown()
        server.server_close()
    except Exception as exc:
        return {"ok": False, "hits": count, "error": str(exc)}
    return {"ok": True, "hits": count, "error": ""}


def reset() -> None:
    """Clear recorded hits and stop the listener (operator/test utility)."""
    stop()
    with _LOCK:
        _STATE["hits"] = []
        _STATE["tokens"] = []


def is_running() -> bool:
    """Return whether the canary listener is alive."""
    with _LOCK:
        return _STATE.get("server") is not None


__all__ = [
    "DEFAULT_BIND_HOST",
    "HITS_PATH",
    "OobHit",
    "hits",
    "is_running",
    "new_token",
    "record_hit",
    "start",
    "stop",
    "url",
]
