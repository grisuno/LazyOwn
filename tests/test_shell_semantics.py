"""Contract tests for shell-semantics detection and colored child output.

The 2026 security pass replaced ``shell=True`` with ``shlex.split`` in the
generic command runners, which silently broke shell syntax (``;``, ``&&``,
globs, tilde, command substitution). These tests pin the detection helper and
the color-preserving environment so a future refactor cannot repeat the
regression.
"""

from __future__ import annotations

from core.hardening import terminal_env
from core.process import run_command
from core.safe_exec import needs_shell


def test_needs_shell_detects_control_and_expansion() -> None:
    """Chaining, pipes, substitutions, globs, tilde and redirection need a shell."""
    for command in (
        "a; b",
        "a && b",
        "a | b",
        "echo $(pwd)",
        "ls *.txt",
        "ls ~/work",
        "cat f > out",
        "echo `id`",
    ):
        assert needs_shell(command), command


def test_needs_shell_accepts_plain_argv() -> None:
    """A program with plain arguments runs without a shell."""
    for command in ("nmap -sV 10.0.0.1", "python3 script.py --flag value", "/bin/ls -la /tmp"):
        assert not needs_shell(command), command


def test_run_command_interprets_semicolon() -> None:
    """run_command executes two chained commands, not a single argv token."""
    output = run_command("printf alpha; printf beta")
    assert "alpha" in output
    assert "beta" in output


def test_run_command_expands_tilde_and_glob(tmp_path, monkeypatch) -> None:
    """run_command lets the shell expand tilde and glob patterns."""
    (tmp_path / "one.txt").write_text("x", encoding="utf-8")
    monkeypatch.setenv("HOME", str(tmp_path))
    output = run_command("ls ~/*.txt")
    assert "one.txt" in output


def test_terminal_env_forces_color(monkeypatch) -> None:
    """CLICOLOR_FORCE and FORCE_COLOR are set so piped tools keep color."""
    monkeypatch.delenv("NO_COLOR", raising=False)
    env = terminal_env()
    assert env["CLICOLOR_FORCE"] == "1"
    assert env["FORCE_COLOR"] == "1"


def test_terminal_env_respects_no_color(monkeypatch) -> None:
    """An explicit NO_COLOR wins over the forced color variables."""
    monkeypatch.setenv("NO_COLOR", "1")
    env = terminal_env()
    assert "CLICOLOR_FORCE" not in env
    assert "FORCE_COLOR" not in env


def test_linpeas_http_server_is_detached(monkeypatch) -> None:
    """The linpeas HTTP server must start detached, not with a trailing ampersand."""
    import cli.commands.privilege_escalation as privilege_escalation

    captured: dict = {}

    class _FakePopen:
        def __init__(self, argv, **kwargs):
            captured["argv"] = argv
            captured["kwargs"] = kwargs

    monkeypatch.setattr(privilege_escalation.subprocess, "Popen", _FakePopen)
    privilege_escalation._serve_via_http(None, "linpeas.sh", "/tmp/sessions", 1337)
    assert captured["argv"][:4] == ["python3", "-m", "http.server", "1337"]
    assert captured["kwargs"].get("start_new_session") is True
    assert "&" not in " ".join(captured["argv"])


def test_safe_runner_interprets_shell_syntax() -> None:
    """SafeRunner.run_shell must let the shell interpret chaining."""
    from core.safe_subprocess import SafeRunner

    result = SafeRunner().run_shell("printf alpha; printf beta", allow=True, reason="test")
    assert "alpha" in result.stdout
    assert "beta" in result.stdout
