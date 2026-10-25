"""Single host-validation policy shared by CLI gates and hardening.

SDD contract: ``core.host_policy`` owns host shape validation.
``core.validators.check_*`` (UX gates with coloured errors) and
``core.hardening.validate_host`` (pure security predicate) both
delegate to it, so the accept/reject sets cannot drift apart.
"""

from __future__ import annotations

from core.hardening import validate_host
from core.host_policy import is_valid_host, rejects_shell_meta
from core.validators import check_lhost, check_lport, check_rhost

VALID = [
    "10.10.11.5",
    "192.168.1.1",
    "8.8.8.8",
    "2001:db8::1",
    "example.com",
    "corp.local",
    "localhost",
    "host-01.example-domain.com",
    "192.168.1.0/24",
    "10.0.0.0/8",
    "  10.0.0.1  ",
]

INVALID = [
    "",
    "   ",
    None,
    12345,
    ["10.0.0.1"],
    "10.0.0.1; rm -rf /",
    "10.0.0.1|cat /etc/passwd",
    "$(whoami)",
    "`id`",
    "host\ninjected",
    "a" * 254,
    "http://example.com",
]

PINNED_QUIRKS = [
    # Pinned historic behavior, preserved verbatim from core.validators:
    # all-numeric dotted strings fall through to the hostname pattern.
    "999.999.999.999",
]


class TestSharedPolicy:
    def test_valid_hosts_accepted(self) -> None:
        for value in VALID:
            assert is_valid_host(value) is True, value
            assert validate_host(value) is True, value

    def test_invalid_hosts_rejected(self) -> None:
        for value in INVALID:
            assert is_valid_host(value) is False, value
            assert validate_host(value if isinstance(value, str) else "") is False, value

    def test_shell_meta_rejected(self) -> None:
        for ch in (";", "&", "|", "`", "$", "(", ")", "{", "}", "\n"):
            assert rejects_shell_meta(f"10.0.0.1{ch}") is True
        assert rejects_shell_meta("10.0.0.1") is False

    def test_pinned_quirks_unchanged(self) -> None:
        for value in PINNED_QUIRKS:
            assert is_valid_host(value) is True, value
            assert validate_host(value) is True, value


class TestCliGatesDelegate:
    def test_check_rhost_matches_policy(self, capsys) -> None:
        for value in VALID:
            assert check_rhost(value) is True, value
        for value in INVALID:
            capsys.readouterr()
            assert check_rhost(value) is False, value

    def test_check_lhost_matches_policy(self, capsys) -> None:
        for value in VALID:
            assert check_lhost(value) is True, value
        for value in INVALID:
            capsys.readouterr()
            assert check_lhost(value) is False, value

    def test_check_lport_unchanged(self, capsys) -> None:
        assert check_lport(8080) is True
        assert check_lport("5555") is True
        capsys.readouterr()
        assert check_lport(0) is False
        assert check_lport(70000) is False
        assert check_lport("abc") is False
