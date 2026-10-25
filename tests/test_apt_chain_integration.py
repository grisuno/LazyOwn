"""BDD integration: apt_chain runs real cmd2 verbs, raw commands and shell.

Given a registered command set, When a chain mixes a verb, a raw command
and an interactive shell, Then all three execute on the operator thread,
raw output is printed, no boolean leaks and the shell still opens.
"""

from __future__ import annotations

import threading

import cmd2
import yaml

from cli.commands.command_and_control_migrated import CommandAndControlMigratedCommandSet
import modules.chain_registry as chain_registry


class _Set(CommandAndControlMigratedCommandSet):
    """Command set that records the interactive shell request."""

    def do_atomic_shell(self, line: str) -> None:
        """Record the shell request without blocking."""
        shell = self._resolve_shell()
        shell.calls.append(("atomic_shell", line, threading.current_thread()))


class _Shell(cmd2.Cmd):
    """Minimal registered shell with the verbs a chain needs."""

    def __init__(self) -> None:
        super().__init__(allow_cli_args=False)
        self.params = {"rhost": "10.0.0.5", "lhost": "127.0.0.1", "lport": "4444"}
        self.calls: list[tuple[str, str, threading.Thread]] = []
        self.register_command_set(_Set())

    def do_assign(self, line: str) -> None:
        """Record the assign verb."""
        self.calls.append(("assign", line, threading.current_thread()))


def test_apt_chain_prints_raw_output_and_opens_shell_on_main_thread(tmp_path, monkeypatch, capsys):
    """The exact regression: no False leak, raw output visible, shell on main thread."""
    document = {
        "name": "test_chain",
        "version": 2,
        "steps": [
            {"id": "scope", "run": "assign target {target}"},
            {"id": "raw", "run": 'python3 -c "print(6*7)"'},
            {"id": "shell", "run": "atomic_shell --interactive {target}"},
        ],
    }
    (tmp_path / "test_chain.yaml").write_text(yaml.safe_dump(document), encoding="utf-8")
    chain = chain_registry.load_all(tmp_path)["test_chain"]
    monkeypatch.setattr(chain_registry, "CHAINS_DIR", tmp_path)
    monkeypatch.setattr(
        chain_registry,
        "get",
        lambda name, chains_dir=None: chain if name == "test_chain" else None,
    )
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    shell = _Shell()
    shell.do_apt_chain("test_chain 10.0.0.5")
    output = capsys.readouterr().out
    assert "False" not in output
    assert "42" in output
    assert "chain finished: 3/3" in output
    assert [name for name, _line, _thread in shell.calls] == ["assign", "atomic_shell"]
    assert all(thread is threading.main_thread() for _name, _line, thread in shell.calls)
    assert shell.calls[-1][1] == "--interactive 10.0.0.5"
