"""Typed errors for the LazyOwn programmatic SDK.

The SDK is the single programmatic surface consumed by the lazymode code
runners, the MCP tool layer and, over time, the CLI. Every failure it
raises is one of these types so a caller (including a sandboxed lazymode
script) can distinguish an operator-scope rejection from an invalid
configuration write or a generic SDK fault without string matching.
"""

from __future__ import annotations


class SdkError(Exception):
    """Base class for every error raised by the LazyOwn SDK facade."""


class ScopeBlocked(PermissionError, SdkError):
    """Raised when an offensive operation targets an out-of-scope host.

    Raised only when the injected scope check is in the enforcing posture
    and the target is not inside the authorized engagement scope. The SDK
    is fail-open: when no scope check is injected the guard is dormant and
    this error is never raised.
    """


class ConfigValidationError(ValueError, SdkError):
    """Raised when a configuration write fails payload-schema validation."""


class SessionPathError(PermissionError, SdkError):
    """Raised when a session artefact name escapes the sessions directory."""
