"""Fake transports and channel fixtures for the C2 channel tests."""

from __future__ import annotations

from typing import Any

import requests

from core.protocols import C2Message
from modules.c2_channels.telegram import TelegramC2Channel

API_BASE = "https://api.telegram.org"


class _FakeResponse:
    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def json(self) -> Any:
        return self._payload


class FakeTransport:
    """In-memory requests replacement recording calls and results."""

    def __init__(self) -> None:
        self.calls: dict[str, str] = {}
        self.poll_params: dict[str, Any] = {}
        self.sent: list[str] = []
        self.updates: list[dict[str, Any]] = []

    def inject_message(self, sender: str, text: str, update_id: int | None = None) -> None:
        update_id = update_id if update_id is not None else len(self.updates) + 1
        self.updates.append({"update_id": update_id, "message": {"text": text, "from": {"id": sender}}})

    def post(self, url: str, json: dict | None = None, timeout: float = 10.0) -> _FakeResponse:
        self.calls["send_url"] = url
        self.sent.append(str((json or {}).get("text", "")))
        return _FakeResponse({"ok": True})

    def get(self, url: str, params: dict | None = None, timeout: float = 15.0) -> _FakeResponse:
        self.calls["poll_url"] = url
        self.poll_params = dict(params or {})
        offset = int((params or {}).get("offset", 0))
        visible = [u for u in self.updates if int(u.get("update_id", 0)) >= offset]
        return _FakeResponse({"ok": True, "result": visible})


class ExplodingTransport(FakeTransport):
    def post(self, url: str, json: dict | None = None, timeout: float = 10.0) -> _FakeResponse:
        raise requests.ConnectionError("boom")

    def get(self, url: str, params: dict | None = None, timeout: float = 15.0) -> _FakeResponse:
        raise requests.ConnectionError("boom")


def advance(channel: TelegramC2Channel, force: bool = False) -> None:
    """Move the channel past its poll rate-limit window."""
    if force or channel._last_poll > 0:
        channel._last_poll = 0.0


class FakeOkTransport(TelegramC2Channel):
    """Telegram channel bound to the in-memory fake transport."""

    def __init__(self, config: dict) -> None:
        self.transport = FakeTransport()
        super().__init__(config)

    def _send_request(self, text: str):
        return self.transport.post(self._send_url(), json={"text": text})

    def _poll_request(self, limit: int):
        response = self.transport.get(self._poll_url(), params={"offset": self._update_offset + 1, "limit": limit})
        return self._consume(response)

    def _send_url(self) -> str:
        return f"{API_BASE}/bot{self._token}/sendMessage"

    def _poll_url(self) -> str:
        return f"{API_BASE}/bot{self._token}/getUpdates"

    def _consume(self, response: _FakeResponse) -> list[C2Message]:
        body = response.json()
        updates = body.get("result", []) if isinstance(body, dict) else []
        messages: list[C2Message] = []
        for update in updates:
            update_id = int(update.get("update_id", 0))
            if update_id > self._update_offset:
                self._update_offset = update_id
            message = update.get("message") or {}
            text = str(message.get("text", "") or "")
            sender = str((message.get("from") or {}).get("id", "") or "")
            if text and sender:
                messages.append(C2Message(channel=self.name, sender=sender, text=text))
        return messages


class FakeExplodingTransport(TelegramC2Channel):
    def __init__(self, config: dict) -> None:
        self.transport = ExplodingTransport()
        super().__init__(config)

    def _send_request(self, text: str):
        return self.transport.post("https://unit.test/send", json={"text": text})

    def _poll_request(self, limit: int):
        _ = limit
        response = self.transport.get("https://unit.test/poll", params={})
        _ = response
        return []
