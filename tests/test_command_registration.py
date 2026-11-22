"""Tests for the extracted command-registration mixin."""

from __future__ import annotations

import json

from cli.command_registration import SHELL_BUILTIN_TOKENS, CommandRegistrationMixin


class _StubShell(CommandRegistrationMixin):
    """Minimal host exposing only what the mixin reads through ``self``."""

    def __init__(self, tmp_path):
        self.params = {"rhost": "10.0.0.5", "rport": "80"}
        self.plugins_dir = str(tmp_path / "plugins")
        self.lazyaddons_dir = str(tmp_path / "lazyaddons")
        self.ran: list[str] = []
        self.toasts: list[tuple[str, str]] = []

    def cmd(self, line):
        self.ran.append(line)

    def onecmd(self, line):
        self.ran.append(line)

    def display_toastr(self, message, type="info"):
        self.toasts.append((message, type))

    def do_adversary_yaml(self, line):
        self.ran.append(f"adversary_yaml {line}")


def test_mixin_has_no_shell_dependency_at_import():
    """Given the mixin, When imported, Then its builtin-token set is intact."""
    assert "cd" in SHELL_BUILTIN_TOKENS
    assert "sleep" in SHELL_BUILTIN_TOKENS
    assert len(SHELL_BUILTIN_TOKENS) == 26


def test_register_tool_command_builds_runnable_wrapper(tmp_path, monkeypatch):
    """Given an active tool file, When registered, Then a do_<name> runs the template."""
    monkeypatch.chdir(tmp_path)
    tool_dir = tmp_path / "tools"
    tool_dir.mkdir()
    (tool_dir / "demo.tool").write_text(
        json.dumps(
            {
                "toolname": "demotool",
                "command": "echo {ip}:{port}",
                "active": True,
                "trigger": [],
                "category": "01. Recon",
                "description": "demo",
            }
        )
    )
    shell = _StubShell(tmp_path)
    shell.register_tool_commands()
    assert hasattr(shell, "do_demotool")
    shell.do_demotool("")
    assert shell.ran == ["echo 10.0.0.5:80"]


def test_register_yaml_plugin_registers_command(tmp_path):
    """Given an addon mapping, When registered, Then a do_<name> runs the execute command."""
    shell = _StubShell(tmp_path)
    shell.register_yaml_plugin(
        {
            "name": "myaddon",
            "description": "addon",
            "enabled": True,
            "tool": {"execute_command": "echo hi"},
        }
    )
    assert hasattr(shell, "do_myaddon")
    shell.do_myaddon("")
    assert shell.ran == ["echo hi"]


def test_register_adversary_command_dispatches_to_yaml(tmp_path):
    """Given a valid adversary entry, When registered, Then it dispatches to adversary_yaml."""
    from utils import REQUIRED_KEYS

    shell = _StubShell(tmp_path)
    adv = {key: "x" for key in REQUIRED_KEYS}
    adv.update({"name": "apt.demo", "description": "d", "id": 42})
    shell._register_adversary_command(adv)
    assert hasattr(shell, "do_apt_demo")
    shell.do_apt_demo("")
    assert shell.ran == ["adversary_yaml 42 l"]
