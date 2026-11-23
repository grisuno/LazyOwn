"""C2 channel plugins: operator chat platforms as C2 transports.

Contracts:
    - :mod:`modules.c2_channels.base` owns the HTTP transport base.
    - ``telegram``/``discord``/``slack`` adapters are request builders.
    - :mod:`modules.c2_channels.registry` is the single factory home
      with payload-driven gating (``enable_<name>_c2``).

Channels are transport-only (``send``/``poll``); command execution is
owned by an injected executor strategy, never by the channel. A channel
without credentials reports ``configured=False`` and fails soft.
"""

from modules.c2_channels.base import HttpC2Channel
from modules.c2_channels.registry import (
    available_channels,
    create_channel,
    create_enabled,
    enabled_channels,
    register_channel,
)

__all__ = [
    "HttpC2Channel",
    "available_channels",
    "create_channel",
    "create_enabled",
    "enabled_channels",
    "register_channel",
]
