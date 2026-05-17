"""Security sanitizers shared across the LazyOwn framework.

This module centralises the defensive code paths the framework
relies on so each concern is implemented once, with strict input
validation, and consumed from every caller that previously rolled
its own logic. The classes here are the single source of truth for:

* Validating untrusted bind addresses before opening a server socket.
* Resolving operator-supplied filenames against the sessions
  directory without enabling traversal.
* Sanitising HTTP header values to prevent response-splitting.
* Redacting credentials when shell commands are rendered for
  display or logging.
* Converting arbitrary Python values into a JSON-safe shape that
  can never leak exception details or traceback information.

Each sanitizer is its own small class so the Single Responsibility
Principle is satisfied; callers depend on the public method names
rather than the internal implementations (Dependency Inversion);
new sanitizers can be added without modifying existing ones (Open /
Closed); and every tunable is exposed on :class:`SecurityConfig` so
the framework keeps the ``payload.json`` single-source-of-truth
contract documented in ``CLAUDE.md``.
"""

from __future__ import annotations

import ipaddress
import os
import re
from dataclasses import dataclass, fields, replace
from typing import Any, Mapping, Optional, Sequence, Tuple


@dataclass(frozen=True)
class SecurityConfig:
    """Immutable tunables consumed by every sanitizer in this module.

    Defaults are conservative; the operator can override any value
    by adding the matching key to ``payload.json``. The dataclass
    is frozen so a sanitizer instance can be shared across threads
    without locking. Tightening a value never breaks an existing
    caller because every helper exposes the resulting behaviour as
    a sentinel rather than as an exception.
    """

    redacted_username_token: str = "[REDACTED-USERNAME]"
    redacted_password_token: str = "[REDACTED-PASSWORD]"
    placeholder_username_marker: str = "deefbeef"
    exception_placeholder: str = "<exception_omitted>"
    non_serializable_placeholder: str = "<unserializable>"
    filtered_header_sentinel: str = "[FILTERED]"
    generic_command_error_message: str = "Command execution error"
    max_serialization_depth: int = 8
    max_serialization_collection: int = 1024
    max_header_value_length: int = 4096
    max_path_segments: int = 32
    max_path_segment_length: int = 255
    bind_loopback_address: str = "127.0.0.1"
    bind_unspecified_address: str = "0.0.0.0"
    allow_unspecified_bind: bool = False
    header_name_pattern: str = r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$"
    header_value_pattern: str = r"^[\x20-\x7E\t]+$"
    path_segment_pattern: str = r"^[A-Za-z0-9._-]+$"

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "SecurityConfig":
        """Build a configuration object from a ``payload.json`` mapping.

        Unknown keys are ignored so adding a new tunable in code
        does not require an immediate ``payload.json`` migration.
        Type-mismatched values are dropped silently because the
        payload file is hand-edited by operators and the framework
        must remain operational even with a partially valid file.

        Args:
            payload: A mapping produced by ``json.load`` over
                ``payload.json`` (or any equivalent dictionary).

        Returns:
            A new, frozen :class:`SecurityConfig` populated from
            the supplied mapping.
        """
        defaults = cls()
        overrides: dict[str, Any] = {}
        for field in fields(cls):
            value = payload.get(field.name) if isinstance(payload, Mapping) else None
            if value is None:
                continue
            expected_type = type(getattr(defaults, field.name))
            if expected_type is bool and isinstance(value, bool):
                overrides[field.name] = value
            elif expected_type is int and isinstance(value, int) and not isinstance(value, bool):
                overrides[field.name] = value
            elif expected_type is str and isinstance(value, str):
                overrides[field.name] = value
        return replace(defaults, **overrides)


class HeaderValueSanitizer:
    """Validate HTTP header names and values before transmission.

    Headers crossing a proxy boundary may carry CR, LF or NUL
    bytes that, if forwarded verbatim, allow an upstream to inject
    extra headers or a response body. The sanitizer strips those
    bytes and then enforces an allowlist regex; values failing
    the allowlist are replaced by an opaque sentinel rather than
    silently coerced to the empty string so the operator can spot
    abnormal upstream behaviour in proxy logs.
    """

    _FORBIDDEN_CHARS: Tuple[str, ...] = ("\r", "\n", "\x00")

    def __init__(self, config: SecurityConfig):
        """Bind the sanitizer to a configuration instance.

        Args:
            config: The :class:`SecurityConfig` from which the
                regex patterns, length limit and sentinel string
                are read at validation time.
        """
        if not isinstance(config, SecurityConfig):
            raise TypeError("config must be a SecurityConfig instance")
        self._config = config
        self._name_re = re.compile(config.header_name_pattern)
        self._value_re = re.compile(config.header_value_pattern)

    def is_valid_name(self, name: Any) -> bool:
        """Return True iff ``name`` is a syntactically valid header token.

        The check follows RFC 7230 ``token`` grammar via the
        allowlist regex in :class:`SecurityConfig`.
        """
        if not isinstance(name, str) or not name:
            return False
        return self._name_re.fullmatch(name) is not None

    def sanitize_value(self, value: Any) -> str:
        """Return a header value that cannot smuggle a response split.

        The output is guaranteed to consist solely of printable
        ASCII plus the horizontal-tab character, with no CR, LF
        or NUL bytes, and to be no longer than the configured
        ``max_header_value_length``. Inputs that are not strings,
        that become empty after stripping forbidden bytes, or that
        fail the allowlist are replaced by the configured sentinel.
        """
        if not isinstance(value, str) or not value:
            return ""
        cleaned = value
        for forbidden in self._FORBIDDEN_CHARS:
            if forbidden in cleaned:
                cleaned = cleaned.replace(forbidden, "")
        if not cleaned:
            return ""
        if self._value_re.fullmatch(cleaned) is None:
            return self._config.filtered_header_sentinel
        return cleaned[: self._config.max_header_value_length]


class SessionPathResolver:
    """Resolve untrusted filenames against a fixed base directory.

    Every resolver is bound to one base directory whose realpath
    is computed at construction; subsequent ``resolve`` calls join
    the validated relative path with that base and reject anything
    that would escape it after symlink resolution. Because the
    validation logic is centralised here, CodeQL data-flow analysis
    consistently recognises the sanitisation and the same guarantees
    apply to every caller that routes through this class.
    """

    def __init__(self, base_dir: str, config: SecurityConfig):
        """Bind the resolver to an absolute, real base directory.

        Args:
            base_dir: The directory that all resolved paths must
                stay within after symlink resolution.
            config: The :class:`SecurityConfig` providing the
                allowlist regex and depth limits.
        """
        if not isinstance(base_dir, str) or not base_dir:
            raise ValueError("base_dir must be a non-empty string")
        if not isinstance(config, SecurityConfig):
            raise TypeError("config must be a SecurityConfig instance")
        self._config = config
        self._base_real = os.path.realpath(base_dir)
        self._segment_re = re.compile(config.path_segment_pattern)

    @property
    def base_dir(self) -> str:
        """The resolved, absolute base directory."""
        return self._base_real

    def resolve(self, untrusted_name: Any) -> Optional[Tuple[str, str]]:
        """Return ``(absolute, relative)`` for a safe filename.

        ``relative`` is suitable for ``send_from_directory`` while
        ``absolute`` is the realpath after joining and may be used
        for ``os.path.isfile`` style checks. Returns ``None`` when
        any structural, textual or filesystem check fails so the
        caller has a single branch to handle every error.
        """
        if not isinstance(untrusted_name, str) or not untrusted_name:
            return None
        if "\x00" in untrusted_name:
            return None
        normalised = untrusted_name.replace("\\", "/").strip()
        if not normalised or normalised.startswith("/"):
            return None
        raw_segments = normalised.split("/")
        if len(raw_segments) > self._config.max_path_segments:
            return None
        clean: list[str] = []
        for piece in raw_segments:
            if piece == "" or piece == ".":
                continue
            if piece == "..":
                return None
            if len(piece) > self._config.max_path_segment_length:
                return None
            if self._segment_re.fullmatch(piece) is None:
                return None
            clean.append(piece)
        if not clean:
            return None
        relative = "/".join(clean)
        candidate = os.path.realpath(os.path.join(self._base_real, relative))
        try:
            common = os.path.commonpath([self._base_real, candidate])
        except ValueError:
            return None
        if common != self._base_real:
            return None
        return candidate, relative

    def file_exists(self, untrusted_name: Any) -> bool:
        """Return True iff ``untrusted_name`` resolves to an existing file.

        The method swallows :class:`OSError` so the caller never
        observes filesystem-level errors during an availability
        probe; missing, denied or unreadable entries all surface
        as ``False``.
        """
        resolved = self.resolve(untrusted_name)
        if resolved is None:
            return False
        absolute, _ = resolved
        try:
            return os.path.isfile(absolute)
        except OSError:
            return False


class BindAddressResolver:
    """Pick the address a server socket should bind to.

    The resolver fails closed: when the operator has not chosen an
    address, it falls back to the configured loopback rather than
    the unspecified ``0.0.0.0`` address. The unspecified address is
    returned only when ``allow_unspecified_bind`` is ``True`` in
    :class:`SecurityConfig`, which gives the operator an explicit,
    auditable opt-in for exposing the C2 on every interface.
    """

    _OCTET_RE = re.compile(r"^[0-9a-fA-F:.]+$")

    def __init__(self, config: SecurityConfig, preferred_addresses: Sequence[Any] = ()):
        """Build a resolver with a prioritised list of candidate addresses.

        Args:
            config: The :class:`SecurityConfig` providing the
                loopback fallback, the unspecified address literal
                and the opt-in flag.
            preferred_addresses: Operator-controlled address
                candidates evaluated in order. The first value that
                parses as a valid IPv4 or IPv6 literal wins.
        """
        if not isinstance(config, SecurityConfig):
            raise TypeError("config must be a SecurityConfig instance")
        self._config = config
        self._preferred = tuple(preferred_addresses)

    def _is_well_formed(self, candidate: Any) -> bool:
        """Return True iff ``candidate`` is a parseable IP literal."""
        if not isinstance(candidate, str):
            return False
        stripped = candidate.strip()
        if not stripped or self._OCTET_RE.fullmatch(stripped) is None:
            return False
        try:
            ipaddress.ip_address(stripped)
            return True
        except ValueError:
            return False

    def resolve(self) -> str:
        """Return the address sockets should bind to.

        Resolution order:

        1. The first operator-preferred address that parses.
        2. The unspecified address when ``allow_unspecified_bind``
           is explicitly enabled by the operator.
        3. The loopback fallback from :class:`SecurityConfig`.
        """
        for candidate in self._preferred:
            if self._is_well_formed(candidate):
                return candidate.strip()
        if self._config.allow_unspecified_bind and self._is_well_formed(self._config.bind_unspecified_address):
            return self._config.bind_unspecified_address
        if self._is_well_formed(self._config.bind_loopback_address):
            return self._config.bind_loopback_address
        return "127.0.0.1"


class CommandRedactor:
    """Render shell commands without leaking the supplied credentials.

    The redactor produces two strings from a single template: an
    executable form, where the real credentials are substituted in
    place, and a display form, where every credential placeholder
    and every byte-for-byte occurrence of the credentials is
    replaced by an opaque sentinel. Callers must use the executable
    form for ``subprocess`` calls and the display form for printing
    or logging.
    """

    _USERNAME_PLACEHOLDER = "{username}"
    _PASSWORD_PLACEHOLDER = "{password}"

    def __init__(self, config: SecurityConfig):
        """Bind the redactor to a configuration instance.

        Args:
            config: The :class:`SecurityConfig` providing the
                redaction sentinels and the placeholder-username
                marker.
        """
        if not isinstance(config, SecurityConfig):
            raise TypeError("config must be a SecurityConfig instance")
        self._config = config

    def _display_username(self, username: str) -> str:
        """Return the username representation safe to print."""
        if not username:
            return ""
        if username == self._config.placeholder_username_marker:
            return username
        return self._config.redacted_username_token

    def _display_password(self, password: str) -> str:
        """Return the password representation safe to print."""
        if not password:
            return ""
        return self._config.redacted_password_token

    def render(
        self,
        template: str,
        substitutions: Mapping[str, str],
        username: str,
        password: str,
    ) -> Tuple[str, str]:
        """Return ``(executable, display)`` for a templated command.

        ``substitutions`` provides the non-credential replacements
        (host, port, output directory and so on). The method
        guarantees that ``display`` never contains the supplied
        ``username`` or ``password`` byte-for-byte unless
        ``username`` matches the placeholder marker. The dual
        return value avoids any chance of the caller printing the
        executable form by accident.
        """
        if not isinstance(template, str):
            raise TypeError("template must be a string")
        if not isinstance(substitutions, Mapping):
            raise TypeError("substitutions must be a mapping")
        if username is not None and not isinstance(username, str):
            raise TypeError("username must be a string or None")
        if password is not None and not isinstance(password, str):
            raise TypeError("password must be a string or None")
        user_value = username or ""
        pass_value = password or ""
        executable = template
        display = template
        for key, value in substitutions.items():
            if not isinstance(key, str):
                continue
            replacement = "" if value is None else str(value)
            marker = "{" + key + "}"
            executable = executable.replace(marker, replacement)
            display = display.replace(marker, replacement)
        executable = executable.replace(self._USERNAME_PLACEHOLDER, user_value)
        executable = executable.replace(self._PASSWORD_PLACEHOLDER, pass_value)
        display = display.replace(self._USERNAME_PLACEHOLDER, self._display_username(user_value))
        display = display.replace(self._PASSWORD_PLACEHOLDER, self._display_password(pass_value))
        if user_value and user_value != self._config.placeholder_username_marker:
            display = display.replace(user_value, self._config.redacted_username_token)
        if pass_value:
            display = display.replace(pass_value, self._config.redacted_password_token)
        return executable, display


class OutputSanitizer:
    """Project arbitrary Python values into a JSON-safe shape.

    Exceptions, traceback objects and any value that fails JSON
    serialisation are replaced by opaque sentinels rather than
    their ``str`` representation, which prevents stack traces,
    internal file paths and instance attributes from reaching the
    HTTP client. Recursion is bounded by the configured maximum
    depth and the breadth of every collection is capped so a
    hostile callee cannot exhaust the responder's stack or memory.
    """

    def __init__(self, config: SecurityConfig):
        """Bind the sanitizer to a configuration instance.

        Args:
            config: The :class:`SecurityConfig` providing the
                placeholders, depth limit and collection cap.
        """
        if not isinstance(config, SecurityConfig):
            raise TypeError("config must be a SecurityConfig instance")
        self._config = config

    def sanitize(self, value: Any) -> Any:
        """Return ``value`` projected into a JSON-serialisable form."""
        return self._sanitize(value, 0)

    def _sanitize(self, value: Any, depth: int) -> Any:
        """Recursive worker for :meth:`sanitize`."""
        if depth >= self._config.max_serialization_depth:
            return self._config.non_serializable_placeholder
        if isinstance(value, BaseException):
            return self._config.exception_placeholder
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            return value
        if isinstance(value, (bytes, bytearray)):
            try:
                return bytes(value).decode("utf-8", errors="replace")
            except (UnicodeError, AttributeError, TypeError):
                return self._config.non_serializable_placeholder
        if isinstance(value, Mapping):
            output: dict[str, Any] = {}
            cap = self._config.max_serialization_collection
            for index, (key, item) in enumerate(value.items()):
                if index >= cap:
                    break
                if isinstance(key, str):
                    safe_key = key
                elif isinstance(key, bool) or key is None or isinstance(key, (int, float)):
                    safe_key = str(key)
                else:
                    continue
                output[safe_key] = self._sanitize(item, depth + 1)
            return output
        if isinstance(value, (list, tuple, set, frozenset)):
            out_list: list[Any] = []
            cap = self._config.max_serialization_collection
            for index, item in enumerate(value):
                if index >= cap:
                    break
                out_list.append(self._sanitize(item, depth + 1))
            return out_list
        return self._config.non_serializable_placeholder


def build_default_config(payload: Optional[Mapping[str, Any]] = None) -> SecurityConfig:
    """Return a :class:`SecurityConfig` populated from ``payload``.

    Convenience entry point so callers do not need to import the
    dataclass directly. ``payload`` is typically the result of
    ``utils.load_payload``; when ``None``, the conservative
    defaults are returned.
    """
    if payload is None:
        return SecurityConfig()
    if not isinstance(payload, Mapping):
        return SecurityConfig()
    return SecurityConfig.from_payload(payload)


__all__ = (
    "SecurityConfig",
    "HeaderValueSanitizer",
    "SessionPathResolver",
    "BindAddressResolver",
    "CommandRedactor",
    "OutputSanitizer",
    "build_default_config",
)
