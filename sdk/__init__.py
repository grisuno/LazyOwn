"""The LazyOwn programmatic SDK.

A single stable facade (:class:`sdk.facade.Lazy`) over the framework so a
lazymode code runner, the MCP tool layer and the CLI can all drive the
same operations through one typed surface instead of duplicating logic.
"""

from __future__ import annotations

from sdk.errors import (
    ConfigValidationError,
    ScopeBlocked,
    SdkError,
    SessionPathError,
)
from sdk.facade import Lazy

__all__ = [
    "Lazy",
    "SdkError",
    "ScopeBlocked",
    "ConfigValidationError",
    "SessionPathError",
]
