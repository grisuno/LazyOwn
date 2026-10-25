"""BDD behavior scenarios for the command allowlist contract."""

from __future__ import annotations

import json
from pathlib import Path

from lazyc2.security.command_allowlist import CommandAllowlist, CommandRejectionReason


def test_given_allowlisted_ping_when_checked_then_allowed() -> None:
    """Given a whitelisted first token, the gate allows the command."""
    allowlist = CommandAllowlist(["ping", "set", "show"])
    decision = allowlist.check("ping 10.0.0.1")
    assert decision.allowed is True


def test_given_rm_when_checked_then_denied() -> None:
    """Given a non-allowlisted verb, the gate denies."""
    allowlist = CommandAllowlist(["ping", "set"])
    decision = allowlist.check("rm -rf /")
    assert decision.allowed is False
    assert decision.reason is CommandRejectionReason.NOT_ALLOWED


def test_given_injection_when_checked_then_denied(tmp_path: Path) -> None:
    """Given a metachar injection, the gate denies and the attempt is audited."""
    log = tmp_path / "audit.jsonl"
    allowlist = CommandAllowlist(["ping"], audit_log_path=log)
    decision = allowlist.check("ping; cat /etc/passwd")
    assert decision.allowed is False
    assert decision.reason is CommandRejectionReason.SHELL_METACHAR
    record = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert record["allowed"] is False
    assert record["reason"] == "shell_metachar"
