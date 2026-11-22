"""Tests for the extracted chain-prompt engine wiring mixin."""

from __future__ import annotations

from cli.chain_prompt import ChainPromptMixin


class _StubChainEngine:
    """Scriptable chain engine: yields queued outcomes then stops."""

    def __init__(self, outcomes, enabled=True, interactive=True):
        self.enabled = enabled
        self.interactive = interactive
        self._outcomes = list(outcomes)
        self.config = type("Cfg", (), {"max_steps": 3, "chain_active": False})()
        self.disabled_persist = None

    def step(self, last_cmd, phase):
        if self._outcomes:
            return self._outcomes.pop(0)
        return type("O", (), {"state": "idle", "command": "", "reason": ""})()

    def set_enabled(self, value, persist=False):
        self.enabled = value
        self.disabled_persist = persist


def _outcome(state, command="", reason=""):
    return type("O", (), {"state": state, "command": command, "reason": reason})()


class _StubShell(ChainPromptMixin):
    """Minimal host exposing only what the chain-prompt mixin reads."""

    def __init__(self, engine=None, params=None):
        self._chain_prompt = engine
        self._chain_prompt_busy = False
        self._command_chain = None
        self.params = params or {}
        self.ran: list = []

    def onecmd_plus_hooks(self, command):
        self.ran.append(command)
        return False


def test_sync_chain_active_mirrors_enabled_flag():
    """Given an enabled engine, When synced, Then the tips flag turns on."""
    tips = type("T", (), {"config": type("C", (), {"chain_active": None})()})()
    shell = _StubShell(_StubChainEngine([], enabled=True))
    shell._sync_chain_active(tips)
    assert tips.config.chain_active is True


def test_maybe_chain_prompt_runs_until_non_run_state():
    """Given queued run steps, When looped, Then each command dispatches once."""
    engine = _StubChainEngine(
        [
            _outcome("run", "lazynmap"),
            _outcome("run", "gobuster"),
            _outcome("off", reason="chain exhausted"),
        ]
    )
    shell = _StubShell(engine)
    shell._maybe_chain_prompt("ping", "recon")
    assert shell.ran == ["lazynmap", "gobuster"]
    assert shell._chain_prompt_busy is False


def test_maybe_chain_prompt_reentrancy_guard():
    """Given the busy flag set, When re-entered, Then nothing runs."""
    engine = _StubChainEngine([_outcome("run", "lazynmap")])
    shell = _StubShell(engine)
    shell._chain_prompt_busy = True
    shell._maybe_chain_prompt("ping", "recon")
    assert shell.ran == []


def test_maybe_chain_prompt_disabled_engine_noop():
    """Given a disabled engine, When prompted, Then nothing runs."""
    engine = _StubChainEngine([_outcome("run", "lazynmap")], enabled=False)
    shell = _StubShell(engine)
    shell._maybe_chain_prompt("ping", "recon")
    assert shell.ran == []


def test_boot_prompt_skips_non_interactive():
    """Given a non-interactive engine, When booted, Then no step runs."""
    engine = _StubChainEngine([_outcome("run", "lazynmap")], interactive=False)
    shell = _StubShell(engine)
    shell._chain_boot_prompt()
    assert shell.ran == []
