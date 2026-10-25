"""Single execution kernel shared by every command runner.

SDD contract: ``CommandExecutor.run_tee`` / ``run_passthrough`` own
process spawning for the framework. ``LazyOwnShell.cmd`` delegates
its spawn loop to them with CLI policies (terminal env, resilient
writer, sessions log path, NOLOGS passthrough) while keeping its
telemetry (toastr, logcsv, metrics, event bus) untouched.

Colors: bytes flow untouched from child stdout to the writer and the
log file, and the child runs under ``core.hardening.terminal_env``
so piped tools keep emitting ANSI. Shell selection follows the
shared ``core.safe_exec.needs_shell`` policy.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from core.safe_exec import needs_shell
from modules.command_executor import CommandExecutor

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_SRC = (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")

ANSI_RED = "\x1b[31mred\x1b[0m\n"


def _executor() -> CommandExecutor:
    return CommandExecutor()


class TestColorsPreserved:
    def test_writer_receives_raw_ansi_bytes(self) -> None:
        seen: list[str] = []
        result = _executor().run_tee(
            f"printf '{ANSI_RED}'", writer=seen.append, log_file=None
        )
        assert result.exit_code == 0
        assert "".join(seen) == ANSI_RED

    def test_log_file_is_byte_identical_to_writer(self, tmp_path: Path) -> None:
        seen: list[str] = []
        log = tmp_path / "out.log"
        result = _executor().run_tee(
            f"printf '{ANSI_RED}'", writer=seen.append, log_file=str(log)
        )
        assert result.exit_code == 0
        assert log.read_text() == "".join(seen) == ANSI_RED
        assert result.output == ANSI_RED

    def test_stderr_merged_into_stream(self) -> None:
        seen: list[str] = []
        result = _executor().run_tee(
            "echo out; echo err >&2", writer=seen.append, log_file=None
        )
        assert result.exit_code == 0
        assert "out\n" in seen
        assert "err\n" in seen


class TestExitCodes:
    def test_shell_path_exit_code(self) -> None:
        result = _executor().run_tee(
            "bash -c 'exit 3'", writer=lambda _l: None
        )
        assert result.exit_code == 3
        assert result.success is False

    def test_argv_path_exit_code(self) -> None:
        result = _executor().run_tee(
            "python3 -c 'import sys; sys.exit(7)'", writer=lambda _l: None
        )
        assert result.exit_code == 7

    def test_passthrough_returns_exit_code(self) -> None:
        assert (
            _executor().run_passthrough(
                "python3 -c 'import sys; sys.exit(5)'"
            )
            == 5
        )
        assert _executor().run_passthrough("true") == 0
        assert _executor().run_passthrough("false") == 1


class TestShellPolicy:
    CASES = [
        "nmap -sV 10.0.0.1",
        "echo a | grep b",
        "ls *.txt",
        "echo ~",
        "echo a; echo b",
        "cat < f",
        "echo $HOME",
        "echo $(id)",
        "ping -c1 host",
        "true",
    ]

    def test_matches_shared_policy(self) -> None:
        executor = _executor()
        for command in self.CASES:
            assert executor._needs_shell(command) is needs_shell(command), command

    def test_timeout_kills_and_raises(self) -> None:
        with __import__("pytest").raises(subprocess.TimeoutExpired):
            _executor().run_tee(
                "sleep 5", writer=lambda _l: None, log_file=None, timeout=0.2
            )


class TestSingleSpawnPath:
    def test_cmd_delegates_spawning_to_kernel(self) -> None:
        import ast as _ast

        tree = _ast.parse(LAZYOWN_SRC)
        cmd = next(
            node
            for node in _ast.walk(tree)
            if isinstance(node, _ast.FunctionDef) and node.name == "cmd"
        )
        constructed = {
            (n.func.attr if isinstance(n.func, _ast.Attribute) else n.func.id)
            for n in _ast.walk(cmd)
            if isinstance(n, _ast.Call)
            and isinstance(n.func, (_ast.Attribute, _ast.Name))
            and (
                (isinstance(n.func, _ast.Attribute) and n.func.attr in ("Popen", "call", "run"))
                or (isinstance(n.func, _ast.Name) and n.func.id in ("Popen",))
            )
        }
        assert not constructed, f"cmd must not spawn processes directly: {constructed}"
        names = {
            n.attr if isinstance(n, _ast.Attribute) else n.id
            for n in _ast.walk(cmd)
            if isinstance(n, (_ast.Attribute, _ast.Name))
        }
        assert "run_tee" in names
        assert "run_passthrough" in names

    def test_cmd_keeps_telemetry(self) -> None:
        src = LAZYOWN_SRC[
            LAZYOWN_SRC.index("    def cmd(self, line):") : LAZYOWN_SRC.index(
                "    def onecmd_plus_hooks("
            )
        ]
        for marker in (
            "display_toastr",
            "logcsv",
            "get_recorder",
            "get_event_bus",
            "write_stdout",
            "_terminal_env",
        ):
            assert marker in src, f"cmd lost telemetry: {marker}"
