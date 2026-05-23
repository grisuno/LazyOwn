"""Orchestration CommandSet: operator-facing surface for the new modules.

This module exposes two verbs to the cmd2 shell:

* ``status_bar`` — inspect, toggle and refresh the persistent prompt
  status bar provided by :mod:`cli.status_bar`.
* ``orchestrate`` — drive :class:`skills.unified_orchestrator.UnifiedOrchestrator`
  with a single goal string, routing transparently to the daemon, hive
  or SWAN backend.

The set is active (subclass of :class:`cli.commands._base.LazyOwnCommandSet`)
because both verbs are new — there is no legacy ``do_*`` in
``lazyown.py`` that they collide with. Activation therefore happens via
:func:`cli.registry.register_command_sets` on shell startup.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any

from cmd2 import with_argparser, with_category

from cli.commands._base import LazyOwnCommandSet

_CATEGORY = "Orchestration"
_STATUS_BAR_ACTIONS = ("show", "on", "off", "refresh")
_STATUS_BAR_DEFAULT_ACTION = "show"
_ORCHESTRATE_DEFAULT_MODE = "auto"
_ORCHESTRATE_MODES = ("auto", "daemon", "hive", "swan")
_OUTPUT_FORMATS = ("text", "json")


@dataclass(frozen=True)
class OrchestrationConfig:
    """Immutable defaults for the orchestration verbs."""

    enable_status_bar_key: str = "enable_status_bar"
    status_bar_actions: tuple[str, ...] = _STATUS_BAR_ACTIONS
    status_bar_default_action: str = _STATUS_BAR_DEFAULT_ACTION
    orchestrate_modes: tuple[str, ...] = _ORCHESTRATE_MODES
    orchestrate_default_mode: str = _ORCHESTRATE_DEFAULT_MODE
    output_formats: tuple[str, ...] = _OUTPUT_FORMATS
    default_output_format: str = "text"
    payload_attribute: str = "params"
    status_manager_attribute: str = "_status_bar_manager"
    orchestrator_attribute: str = "_unified_orchestrator"
    truthy_strings: tuple[str, ...] = ("1", "true", "yes", "on")
    falsy_strings: tuple[str, ...] = ("0", "false", "no", "off")


_CONFIG = OrchestrationConfig()


def _build_status_bar_parser() -> argparse.ArgumentParser:
    """Return the argparse parser used by ``status_bar``."""
    parser = argparse.ArgumentParser(prog="status_bar")
    parser.add_argument(
        "action",
        nargs="?",
        choices=_CONFIG.status_bar_actions,
        default=_CONFIG.status_bar_default_action,
        help="show prints the rendered line, on/off toggles the flag, refresh recomputes it",
    )
    return parser


def _build_orchestrate_parser() -> argparse.ArgumentParser:
    """Return the argparse parser used by ``orchestrate``."""
    parser = argparse.ArgumentParser(prog="orchestrate")
    parser.add_argument("goal", help="objective string passed to the chosen backend")
    parser.add_argument(
        "--mode",
        choices=_CONFIG.orchestrate_modes,
        default=_CONFIG.orchestrate_default_mode,
        help="routing mode: auto picks the best backend, otherwise force one",
    )
    parser.add_argument(
        "--phase",
        default="",
        help="kill-chain phase identifier (recon, enum, exploitation, ...)",
    )
    parser.add_argument(
        "--task-type",
        dest="task_type",
        default="",
        help="SWAN task type identifier",
    )
    parser.add_argument(
        "--target",
        default="",
        help="single-target identifier consumed by the daemon backend",
    )
    parser.add_argument(
        "--drones",
        type=int,
        default=0,
        help="hive drone count (0 keeps the config default)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="SWAN timeout in seconds (0 keeps the config default)",
    )
    parser.add_argument(
        "--format",
        choices=_CONFIG.output_formats,
        default=_CONFIG.default_output_format,
        help="output rendering: text prints a summary, json prints the full result",
    )
    return parser


class OrchestrationCommandSet(LazyOwnCommandSet):
    """Operator commands exposing the status bar and unified orchestrator."""

    phase = "orchestration"
    category = _CATEGORY

    @with_category(_CATEGORY)
    @with_argparser(_build_status_bar_parser())
    def do_status_bar(self, args: argparse.Namespace) -> None:
        """Inspect, toggle and refresh the prompt status bar.

        Subcommands:
            show     Print the currently rendered status line.
            on / off Persist the flag into payload via the shell.
            refresh  Recompute the status bar context against ``sessions/``.
        """
        action = (getattr(args, "action", None) or _CONFIG.status_bar_default_action).lower()
        manager = self._status_manager()
        if manager is None:
            print("status_bar: manager not installed on this shell")
            return
        if action == "show":
            self._status_bar_show(manager)
            return
        if action == "refresh":
            self._status_bar_refresh(manager)
            return
        if action in ("on", "off"):
            self._status_bar_toggle(manager, enabled=(action == "on"))
            return
        print(f"status_bar: unknown action: {action}")

    @with_category(_CATEGORY)
    @with_argparser(_build_orchestrate_parser())
    def do_orchestrate(self, args: argparse.Namespace) -> None:
        """Route a goal through the unified orchestrator and print the result.

        The orchestrator picks one of ``daemon``, ``hive`` or ``swan`` and
        normalises the response into a single dataclass. Use ``--mode`` to
        force a specific backend; the default ``auto`` routes by
        signature heuristics.
        """
        orchestrator = self._orchestrator()
        if orchestrator is None:
            print("orchestrate: unified orchestrator not installed on this shell")
            return
        result = orchestrator.execute(
            goal=args.goal,
            mode=args.mode,
            phase=args.phase,
            task_type=args.task_type,
            target=args.target,
            drones=args.drones,
            timeout=args.timeout,
        )
        if args.format == "json":
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
            return
        print(self._format_text(result))

    def _resolve_shell(self) -> Any:
        """Return the bound cmd2 shell or ``None`` if not yet registered.

        cmd2 stores the shell in the name-mangled
        ``_CommandSet__cmd_internal`` slot and exposes it through the
        ``_cmd`` property. Reading ``self._cmd`` triggers the property
        and is the only stable way to retrieve the shell — going through
        ``self.__dict__`` returns ``None`` because there is no instance
        attribute by that name.
        """
        try:
            return self._cmd
        except Exception:
            return None

    def _status_manager(self) -> Any:
        shell = self._resolve_shell()
        if shell is None:
            return None
        return getattr(shell, _CONFIG.status_manager_attribute, None)

    def _orchestrator(self) -> Any:
        shell = self._resolve_shell()
        if shell is None:
            return None
        return getattr(shell, _CONFIG.orchestrator_attribute, None)

    def _status_bar_show(self, manager: Any) -> None:
        ctx = manager.collect_context()
        line = manager.render_plain_line(ctx)
        print(line)

    def _status_bar_refresh(self, manager: Any) -> None:
        shell = self._resolve_shell()
        if shell is None:
            return
        base = getattr(shell, "custom_prompt", None) or getattr(shell, "prompt", "")
        if not isinstance(base, str):
            base = ""
        shell.prompt = manager.render_prompt(base)
        print(manager.render_plain_line(manager.collect_context()))

    def _status_bar_toggle(self, manager: Any, enabled: bool) -> None:
        shell = self._resolve_shell()
        params = getattr(shell, _CONFIG.payload_attribute, None) if shell is not None else None
        if isinstance(params, dict):
            params[_CONFIG.enable_status_bar_key] = enabled
        manager.set_enabled(enabled)
        print(f"status_bar: {'on' if enabled else 'off'}")

    @staticmethod
    def _format_text(result: Any) -> str:
        backend = getattr(result, "backend", "") or "-"
        status = getattr(result, "status", "") or "-"
        summary = getattr(result, "summary", "") or "(no summary)"
        request_id = getattr(result, "request_id", "") or "-"
        duration = getattr(result, "duration", 0.0)
        return f"[{backend}] {status} request={request_id} duration={duration:.3f}s\n  {summary}"


__all__ = ["OrchestrationCommandSet", "OrchestrationConfig"]
