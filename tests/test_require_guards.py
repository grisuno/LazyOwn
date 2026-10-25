"""Single-call requirement guards for CommandSet methods.

SDD contract: ``require_rhost`` / ``require_lhost`` /
``require_lport`` / ``require_rport`` replace the ``params[...]`` +
``check_*`` two-liner with one fail-closed call. They return exactly
what the underlying ``check_*`` returns for present values and
``False`` (with the checker's error message) instead of raising
``KeyError`` when the key is missing.
"""

from __future__ import annotations

from core.validators import (
    require_lhost,
    require_lport,
    require_rhost,
    require_rport,
)


class TestRequireGuards:
    def test_present_valid_values_pass(self, capsys) -> None:
        params = {"rhost": "10.10.11.5", "lhost": "192.168.1.1", "lport": 4444, "rport": 80}
        assert require_rhost(params) is True
        assert require_lhost(params) is True
        assert require_lport(params) is True
        assert require_rport(params) is True

    def test_missing_keys_fail_closed_without_keyerror(self, capsys) -> None:
        assert require_rhost({}) is False
        assert require_lhost({}) is False
        assert require_lport({}) is False
        assert require_rport({}) is False

    def test_invalid_values_rejected(self, capsys) -> None:
        assert require_rhost({"rhost": "10.0.0.1; id"}) is False
        assert require_lhost({"lhost": ""}) is False
        assert require_lport({"lport": 70000}) is False
        assert require_rport({"rport": "abc"}) is False

    def test_equivalent_to_checkers_on_present_values(self, capsys) -> None:
        from core.validators import check_lhost, check_lport, check_port, check_rhost

        cases = ["10.0.0.1", "example.com", "", "bad;host", None, 0, 65536]
        for value in cases:
            capsys.readouterr()
            assert require_rhost({"rhost": value}) is check_rhost(value)
            capsys.readouterr()
            assert require_lhost({"lhost": value}) is check_lhost(value)
            capsys.readouterr()
            assert require_lport({"lport": value}) is check_lport(value)
            capsys.readouterr()
            assert require_rport({"rport": value}) is check_port(value, name="rport")
