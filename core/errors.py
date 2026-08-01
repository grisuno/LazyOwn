"""Error taxonomy for the LazyOwn framework.

Provides a hierarchy of exception classes with error codes, enabling
structured error reporting and programmatic error handling.
"""

from enum import IntEnum
from typing import Optional


class ErrorCode(IntEnum):
    """Structured error codes for the LazyOwn framework."""

    CONFIG_MISSING = 1001
    CONFIG_INVALID = 1002

    TARGET_UNREACHABLE = 2001
    TARGET_DENIED = 2002

    AUTH_FAILED = 3001
    AUTH_EXPIRED = 3002

    TOOL_NOT_FOUND = 4001
    TOOL_TIMEOUT = 4002
    TOOL_FAILED = 4003

    DB_CONNECTION = 5001
    DB_QUERY = 5002

    NETWORK_TIMEOUT = 6001
    NETWORK_REFUSED = 6002

    VALIDATION_TYPE = 7001
    VALIDATION_RANGE = 7002

    INTERNAL_ERROR = 9001


_ERROR_TYPE_MAP: dict[ErrorCode, str] = {
    ErrorCode.CONFIG_MISSING: "ConfigError",
    ErrorCode.CONFIG_INVALID: "ConfigError",
    ErrorCode.TARGET_UNREACHABLE: "TargetError",
    ErrorCode.TARGET_DENIED: "TargetError",
    ErrorCode.AUTH_FAILED: "AuthError",
    ErrorCode.AUTH_EXPIRED: "AuthError",
    ErrorCode.TOOL_NOT_FOUND: "ToolError",
    ErrorCode.TOOL_TIMEOUT: "ToolError",
    ErrorCode.TOOL_FAILED: "ToolError",
    ErrorCode.DB_CONNECTION: "DatabaseError",
    ErrorCode.DB_QUERY: "DatabaseError",
    ErrorCode.NETWORK_TIMEOUT: "NetworkError",
    ErrorCode.NETWORK_REFUSED: "NetworkError",
    ErrorCode.VALIDATION_TYPE: "ValidationError",
    ErrorCode.VALIDATION_RANGE: "ValidationError",
    ErrorCode.INTERNAL_ERROR: "LazyOwnError",
}


class LazyOwnError(Exception):
    """Base exception for all LazyOwn framework errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code or ErrorCode.INTERNAL_ERROR

    def to_dict(self) -> dict:
        """Return a serialisable dict with code, type, and message."""
        return {
            "code": self.error_code,
            "type": _ERROR_TYPE_MAP.get(
                ErrorCode(self.error_code), self.__class__.__name__
            ),
            "message": self.message,
        }

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class ConfigError(LazyOwnError):
    """Configuration-related errors (missing/invalid payload.json, etc.)."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.CONFIG_INVALID)


class TargetError(LazyOwnError):
    """Target connectivity or access errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.TARGET_UNREACHABLE)


class AuthError(LazyOwnError):
    """Authentication or authorisation failures."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.AUTH_FAILED)


class ToolError(LazyOwnError):
    """External tool execution errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.TOOL_FAILED)


class PayloadError(LazyOwnError):
    """Payload generation or deployment errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.INTERNAL_ERROR)


class DatabaseError(LazyOwnError):
    """Database operation errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.DB_QUERY)


class NetworkError(LazyOwnError):
    """Network-level errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.NETWORK_TIMEOUT)


class PermissionError(LazyOwnError):
    """Insufficient-permission errors (wraps OS-level PermissionError)."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.INTERNAL_ERROR)


class ValidationError(LazyOwnError):
    """Input validation / sanitisation errors."""

    def __init__(self, message: str, error_code: Optional[int] = None) -> None:
        super().__init__(message, error_code or ErrorCode.VALIDATION_TYPE)
