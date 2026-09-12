"""Contract tests for live prompt refresh after a payload change.

The migrated CommandSets write ``self.custom_prompt`` and ``self.prompt``
expecting the shell to own them. The base class forwards unknown reads to the
shell, but it did not forward writes, so ``assign rhost`` changed
``payload.json`` and left the Neon Box prompt stale. These tests pin the write
forwarding and the ``refresh_prompt`` wiring.
"""

from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

from cli.banner_config import render_prompt
from cli.commands._base import LazyOwnCommandSet

REPO_ROOT = Path(__file__).resolve().parent.parent


def _command_set_with_fake_shell() -> tuple[LazyOwnCommandSet, SimpleNamespace]:
    command_set = LazyOwnCommandSet()
    fake_shell = SimpleNamespace(custom_prompt="old-prompt", prompt="old-prompt")
    command_set._resolve_shell = lambda: fake_shell
    return command_set, fake_shell


def test_prompt_write_forwards_to_shell() -> None:
    """Assigning custom_prompt on a CommandSet updates the bound shell."""
    command_set, fake_shell = _command_set_with_fake_shell()
    command_set.custom_prompt = "new-prompt"
    assert fake_shell.custom_prompt == "new-prompt"
    assert "custom_prompt" not in command_set.__dict__


def test_prompt_read_after_forward() -> None:
    """Reading custom_prompt after forwarding returns the shell value."""
    command_set, _ = _command_set_with_fake_shell()
    command_set.custom_prompt = "fresh"
    assert command_set.custom_prompt == "fresh"


def test_unrelated_write_stays_local() -> None:
    """A non-prompt attribute is never forwarded to the shell."""
    command_set, fake_shell = _command_set_with_fake_shell()
    command_set.some_local_state = 42
    assert command_set.__dict__["some_local_state"] == 42
    assert not hasattr(fake_shell, "some_local_state")


def test_do_assign_calls_refresh_prompt() -> None:
    """do_assign must refresh the prompt after a successful payload write."""
    source = (REPO_ROOT / "cli" / "commands" / "misc_migrated.py").read_text(encoding="utf-8")
    block = source.split("def do_assign", 1)[1].split("def do_tenant", 1)[0]
    assert "self.refresh_prompt()" in block


def test_shell_defines_refresh_prompt() -> None:
    """LazyOwnShell must own the refresh_prompt helper."""
    source = (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")
    assert re.search(r"def refresh_prompt\(self\)", source)


def test_render_prompt_includes_rhost() -> None:
    """The rendered prompt reflects the rhost passed in the payload."""
    prompt = render_prompt({"rhost": "203.0.113.9", "lhost": "10.0.0.1"})
    assert "203.0.113.9" in prompt
