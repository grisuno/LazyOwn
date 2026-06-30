"""Command allowlist policy for the LazyOwn C2 ``/api/run`` endpoint.

Contract: this module gates arbitrary command execution so only commands
whose first whitespace-delimited token is on a configurable allowlist can
reach the LazyOwn shell. Shell metacharacters are always rejected as a
defence-in-depth check independent of the allowlist.

Invariants:

1. The first non-whitespace token of the command is matched against the
   allowlist in a case-insensitive way.
2. Any of the characters ``;``, ``|``, ``&``, ``$``, ``>``, ``<``,
   backtick, newline, carriage return, or backslash causes a rejection
   with reason :class:`CommandRejectionReason.SHELL_METACHAR`.
3. Empty / whitespace / non-string commands reject with reason
   :class:`CommandRejectionReason.EMPTY`.
4. When ``audit_log_path`` is set, every decision is appended as a single
   JSON line so the operator can review what was attempted.

Config keys owned:

- ``c2_api_command_allowlist`` (CSV string, default
  ``"ping,set,show,help,status,sessions,sitrep,gets,get,downloader,getosession,osession,setar,getar,session,clean"``)
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Iterable


class CommandRejectionReason(str, Enum):
    """Why a command was rejected by :class:`CommandAllowlist`."""

    EMPTY = "empty"
    NOT_ALLOWED = "not_allowed"
    SHELL_METACHAR = "shell_metachar"


_SHELL_METACHARS = set(";|&$><`\\\n\r")


@dataclass(frozen=True)
class CommandDecision:
    """The outcome of a single command allowlist check.

    Attributes:
        allowed: ``True`` if the command may be executed.
        reason: The rejection reason, or ``None`` when allowed.
        first_token: The normalized first token, useful for audit logs.
    """

    allowed: bool
    reason: CommandRejectionReason | None
    first_token: str

    def to_dict(self) -> dict[str, str | bool | None]:
        """Return a JSON-serializable dict for the audit log."""
        return {
            "allowed": self.allowed,
            "reason": self.reason.value if self.reason is not None else None,
            "first_token": self.first_token,
        }


class CommandAllowlist:
    """Allowlist gate for the ``/api/run`` endpoint.

    Args:
        allowed: Iterable of allowed first tokens. Order is irrelevant;
            matching is case-insensitive.
        audit_log_path: Optional filesystem path. When provided, every
            decision is appended as one JSON object per line.
    """

    __slots__ = ("_allowed", "_audit_log_path")

    def __init__(
        self,
        allowed: Iterable[str],
        audit_log_path: str | Path | None = None,
    ) -> None:
        normalized = {token.strip().lower() for token in allowed if token and token.strip()}
        if not normalized:
            raise ValueError("CommandAllowlist requires at least one allowed command")
        self._allowed = frozenset(normalized)
        self._audit_log_path = Path(audit_log_path) if audit_log_path is not None else None

    @property
    def allowed(self) -> frozenset[str]:
        """Return the immutable set of allowed first tokens (lowercased)."""
        return self._allowed

    def check(self, command: object) -> CommandDecision:
        """Return the :class:`CommandDecision` for ``command``.

        Args:
            command: The raw command string from the request.

        Returns:
            A :class:`CommandDecision` describing the outcome. The
            decision is also written to the audit log if configured.
        """
        if not isinstance(command, str) or not command.strip():
            decision = CommandDecision(False, CommandRejectionReason.EMPTY, "")
            self._audit(decision, command)
            return decision
        if any(ch in _SHELL_METACHARS for ch in command):
            first = command.strip().split(maxsplit=1)[0].lower()
            decision = CommandDecision(False, CommandRejectionReason.SHELL_METACHAR, first)
            self._audit(decision, command)
            return decision
        first_token = command.strip().split(maxsplit=1)[0]
        normalized = first_token.lower()
        if normalized in self._allowed:
            decision = CommandDecision(True, None, normalized)
        else:
            decision = CommandDecision(False, CommandRejectionReason.NOT_ALLOWED, normalized)
        self._audit(decision, command)
        return decision

    def _audit(self, decision: CommandDecision, command: object) -> None:
        if self._audit_log_path is None:
            return
        record = decision.to_dict()
        record["command"] = command if isinstance(command, str) else str(command)
        record["timestamp"] = datetime.now(timezone.utc).isoformat()
        self._audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._audit_log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


__all__ = [
    "CommandAllowlist",
    "CommandDecision",
    "CommandRejectionReason",
]
