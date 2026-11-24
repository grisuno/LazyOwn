"""Interactive chain-prompt engine wiring for ``LazyOwnShell``.

Owns the shell side of chain mode: building the
:class:`cli.chain_mode.ChainPromptEngine`, resolving world-model-driven
next steps through :class:`cli.command_chain.CommandChain`, offering the
first step at boot, mirroring the chain-active flag into the tips engine,
and running the interactive accept/override loop after a command executes.

The pure chain-mode policy (step state machine, persistence, guard
limits) lives in :mod:`cli.chain_mode`; this mixin is only the glue that
binds that engine to shell state. It reads shell attributes exposed
through ``self`` (``_chain_prompt``, ``_command_chain``, ``params``,
``sessions_dir``, ``onecmd_plus_hooks``) and never touches module globals
of ``lazyown.py``, so it mixes in without any call-site rewrite.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from cli.chain_mode import LOOP_GUARD_MARGIN as _CHAIN_GUARD_MARGIN
from cli.chain_mode import MAX_STEPS_DEFAULT as _CHAIN_MAX_STEPS
from cli.chain_mode import ChainModeConfig as _ChainModeConfig
from cli.chain_mode import ChainPromptEngine as _ChainPromptEngine
from cli.tips_engine import TipsEngine as _TipsEngine
from utils import parse_bool, print_msg, print_warn

if TYPE_CHECKING:
    from cli.command_chain import CommandChain


class ChainPromptMixin:
    """Wire the interactive chain-mode engine into :class:`LazyOwnShell`.

    Mixed into the shell; invoked from ``__init__`` (build + boot) and
    from the unified post-command hook (sync + step loop).
    """

    params: dict[str, Any]
    onecmd_plus_hooks: Callable[..., Any]
    _command_chain: CommandChain | None

    def _sync_chain_active(self, tips_engine: _TipsEngine) -> None:
        """Mirror the chain-mode toggle into the tips engine suppression flag.

        Args:
            tips_engine: The unified tips engine whose ``chain_active``
                config flag controls the competing suggestion surfaces.
        """
        try:
            chain_engine = getattr(self, "_chain_prompt", None)
            active = bool(chain_engine is not None and chain_engine.enabled)
            tips_engine.config.chain_active = active
        except Exception:
            pass

    def _chain_boot_prompt(self) -> None:
        """Offer the first chain step right after the banner.

        Runs exactly once per shell session (from ``__init__``) so the
        operator sees the world-model-driven chain immediately, before
        typing any command. Skipped silently for non-interactive shells.
        """
        engine = getattr(self, "_chain_prompt", None)
        if engine is None or not engine.enabled or not engine.interactive:
            return
        try:
            self._maybe_chain_prompt("", self.params.get("phase") or "")
        except Exception as exc:
            print_warn(f"chain prompt failed at boot: {exc}")

    def _build_chain_prompt_engine(self) -> _ChainPromptEngine:
        """Construct the interactive chain-mode engine wired to the shell.

        The resolver delegates to :class:`cli.command_chain.CommandChain`
        so suggestions are governed by the world model: static kill-chain
        adjacency first, then nmap-discovered services (port triggers),
        then addon/tool triggers, then phase priority. The engine is
        non-interactive unless stdin is a TTY so headless/daemon shells
        can never block on the prompt.

        Returns:
            A ready-to-use :class:`cli.chain_mode.ChainPromptEngine`.
        """
        sessions_dir = getattr(self, "sessions_dir", "sessions") or "sessions"
        payload_default = parse_bool(self.params.get("enable_chainmode", False))
        interactive = bool(sys.stdin.isatty())
        return _ChainPromptEngine(
            config=_ChainModeConfig(
                sessions_dir=sessions_dir,
                enabled_default=payload_default,
            ),
            resolver=self._chain_resolver,
            interactive=interactive,
        )

    def _chain_resolver(self, cmd: str, phase: str) -> list:
        """Resolve world-model-driven next steps for the chain prompt.

        Args:
            cmd: The command that just executed (first token).
            phase: Current engagement phase identifier.

        Returns:
            Ordered :class:`cli.command_chain.NextStep` list, empty when no
            signal exists.
        """
        from cli.command_chain import CommandChain

        if self._command_chain is None:
            self._command_chain = CommandChain()
        target = self.params.get("rhost") or None
        return self._command_chain.next(cmd=cmd, params=self.params, target=target, phase=phase, limit=5)

    def _maybe_chain_prompt(self, cmd: str, phase: str) -> None:
        """Run the interactive chain loop after a command executes.

        Keeps prompting while the operator accepts, overrides or picks
        numbered alternatives. The loop is guarded by a busy flag so the
        nested hooks of chained executions never re-enter it, and by the
        engine's own step limit.

        Args:
            cmd: The command that just executed (first token).
            phase: Current engagement phase identifier.
        """
        engine = getattr(self, "_chain_prompt", None)
        if engine is None or not engine.enabled:
            return
        if getattr(self, "_chain_prompt_busy", False):
            return
        self._chain_prompt_busy = True
        try:
            last_cmd = cmd
            guard_limit = int(getattr(engine.config, "max_steps", _CHAIN_MAX_STEPS)) + _CHAIN_GUARD_MARGIN
            guard = 0
            while engine.enabled and guard < guard_limit:
                outcome = engine.step(last_cmd, phase)
                if outcome.state != "run":
                    if outcome.state == "off" and outcome.reason:
                        print_msg(outcome.reason)
                    break
                print_msg(f"chain: running '{outcome.command}'")
                try:
                    self.onecmd_plus_hooks(outcome.command)
                except Exception as exc:
                    print_warn(f"chain: '{outcome.command}' failed: {exc}")
                tokens = outcome.command.split()
                last_cmd = tokens[0] if tokens else ""
                phase = self.params.get("phase") or phase
                guard += 1
        except KeyboardInterrupt:
            try:
                engine.set_enabled(False, persist=True)
            except Exception:
                pass
            print_warn("chainmode interrupted — chainmode off")
        finally:
            self._chain_prompt_busy = False
