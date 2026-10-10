"""Stateless multi-channel notifier for finding events.

Ports the LAZY notify contract. Channels stay stateless so one
instance serves many configurations concurrently. Severity filters
drop noise and secret patterns are masked before dispatch.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class NotifyConfig:
    """Centralized constants for notification behavior (LAZY parity)."""

    kinds: frozenset = frozenset(
        {"dingtalk", "feishu", "wecom", "webhook", "telegram", "email"})
    events: frozenset = frozenset({"finding_created", "finding_status_changed"})
    severity_rank: tuple = ("low", "medium", "high", "critical")
    secret_patterns: tuple = ("sk-", "AKIA", "xoxb-", "ghp_",
                              "xoxp-", "xoxa-", "gho_", "glpat-",
                              "-----BEGIN", "password=", "passwd=")
    digest_sec: float = 1800.0


CONFIG = NotifyConfig()


def severity_rank(severity: str, config: NotifyConfig = CONFIG) -> int:
    """Return the comparable order for a severity label."""
    try:
        return config.severity_rank.index(str(severity or "").lower()) + 1
    except ValueError:
        return 0


def mask_secrets(text: str, config: NotifyConfig = CONFIG) -> str:
    """Replace known secret prefixes with a redaction marker."""
    redacted = str(text or "")
    for marker in config.secret_patterns:
        if marker.endswith("="):
            redacted = re.sub(re.escape(marker) + r"[^\s&;]{1,64}",
                              marker + "[REDACTED]", redacted,
                              flags=re.IGNORECASE)
        elif marker.startswith("-----"):
            redacted = redacted.replace(marker, "[REDACTED-KEY]")
        else:
            redacted = re.sub(re.escape(marker) + r"[A-Za-z0-9_-]{4,}",
                              "[REDACTED]", redacted)
    redacted = re.sub(r"https?://[^/\s]*:[^@/\s]+@[^\s]+",
                      "https://[REDACTED]@[hidden]", redacted)
    return redacted


def url_allowed(url: str) -> tuple[bool, str]:
    """SSRF dial-guard for webhook delivery (LAZY parity).

    Blocks loopback/link-local unless LAZY_NOTIFY_ALLOW_LOCAL=1 and
    never allows cross-host redirects (checked by the caller).
    Returns (allowed, reason).
    """
    import ipaddress as _ip
    import os as _os
    import urllib.parse as _url
    try:
        parts = _url.urlparse(str(url or ""))
    except Exception:
        return False, "unparseable url"
    if parts.scheme not in ("http", "https"):
        return False, f"unsupported scheme: {parts.scheme}"
    host = (parts.hostname or "").strip().lower()
    if not host:
        return False, "empty host"
    if host in ("localhost",):
        if _os.environ.get("LAZY_NOTIFY_ALLOW_LOCAL", "") != "1":
            return False, "loopback blocked (set LAZY_NOTIFY_ALLOW_LOCAL=1)"
        return True, "ok-local"
    try:
        addr = _ip.ip_address(host)
        if addr.is_loopback or addr.is_link_local:
            if _os.environ.get("LAZY_NOTIFY_ALLOW_LOCAL", "") != "1":
                return False, "loopback/link-local blocked"
            return True, "ok-local"
        return True, "ok"
    except ValueError:
        return True, "ok-hostname"


@dataclass
class NotifyMessage:
    """Event payload awaiting channel fan-out."""

    event: str
    severity: str
    title: str
    body: str = ""
    finding_id: str = ""
    task: str = ""
    asset: str = ""


@dataclass
class Channel:
    """Single destination with its own filter and credentials."""

    kind: str
    name: str
    min_severity: str = "low"
    settings: dict = field(default_factory=dict)
    include_keywords: tuple = ()
    exclude_keywords: tuple = ()
    scope: tuple = ()
    realtime: bool = True

    def __post_init__(self) -> None:
        """Validate channel kind and event compatibility."""
        if self.kind not in CONFIG.kinds:
            raise ValueError(f"Unsupported channel kind: {self.kind}")


class Notifier:
    """Filter, render, and dispatch messages across channels."""

    def __init__(self, config: NotifyConfig = CONFIG) -> None:
        """Initialize with shared notification constants."""
        self._config = config
        self.sent: list[dict] = []
        self._digest: list[tuple] = []
        import time as _time
        self._digest_since: float = _time.time()

    def should_send(self, message: NotifyMessage, channel: Channel) -> bool:
        """Apply event, severity, keyword and scope gates (LAZY parity)."""
        if message.event not in self._config.events:
            return False
        if severity_rank(message.severity, self._config) < \
                severity_rank(channel.min_severity, self._config):
            return False
        hay = f"{message.title}\n{message.body}".lower()
        for kw in (channel.exclude_keywords or ()):
            if kw and str(kw).lower() in hay:
                return False
        if channel.include_keywords:
            if not any(kw and str(kw).lower() in hay
                       for kw in channel.include_keywords):
                return False
        if channel.scope:
            wanted = {str(s).strip().lower() for s in channel.scope if str(s).strip()}
            got = {str(message.task or '').strip().lower(),
                   str(message.asset or '').strip().lower()} - {""}
            if wanted and not (wanted & got):
                return False
        return True

    def render(self, message: NotifyMessage) -> str:
        """Render masked Markdown text for a message."""
        title = mask_secrets(message.title, self._config)
        body = mask_secrets(message.body, self._config)
        return f"[{message.severity}] {title}\n{body}".strip()

    def dispatch(self, message: NotifyMessage,
                 channels: list[Channel]) -> list[dict]:
        """Fan out to eligible channels and journal deliveries."""
        import time as _time
        deliveries: list[dict] = []
        for channel in channels:
            if not self.should_send(message, channel):
                continue
            if not channel.realtime:
                self._digest.append((message, channel))
                continue
            deliveries.append({"channel": channel.name, "kind": channel.kind,
                               "text": self.render(message)})
        self.sent.extend(deliveries)
        return deliveries

    def flush_digest(self, max_age_sec: float = 0.0) -> list[dict]:
        """Emit one digest per channel when due (default 30m, LAZY parity)."""
        import time as _time
        window = max_age_sec or self._config.digest_sec
        if _time.time() - self._digest_since < window or not self._digest:
            return []
        by_channel: dict = {}
        for message, channel in self._digest:
            by_channel.setdefault(channel.name, (channel, []))[1].append(message)
        out: list[dict] = []
        for name, (channel, messages) in by_channel.items():
            lines = [f"digest: {len(messages)} finding(s)"]
            for msg in messages[:20]:
                lines.append(f"- [{msg.severity}] {mask_secrets(msg.title, self._config)}")
            out.append({"channel": name, "kind": channel.kind,
                        "text": "\n".join(lines)})
        self._digest.clear()
        self._digest_since = _time.time()
        self.sent.extend(out)
        return out
