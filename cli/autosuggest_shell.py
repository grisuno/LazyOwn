"""Autosuggest wiring for ``LazyOwnShell``.

Owns the shell side of the ghost-text autosuggestion surface: reading the
recent command transcript and recomputing the active suggestion from the
engine's provider chain. The suggestion provider logic itself lives in
:mod:`cli.autosuggest`; this mixin is only the glue that feeds shell state
(last command, phase, target, OS hint, recent commands) into the engine.

Both methods read shell attributes through ``self`` (``_autosuggest``,
``sessions_dir``, ``params``) and are invoked from the forwarding
CommandSets (``cli/commands/session_ops.py``) via the bound shell, so the
mixin keeps the exact ``self`` semantics with no call-site rewrite.
"""

from __future__ import annotations

import csv
import os

from cli.autosuggest import SuggestionContext as _SuggestionContext


class AutosuggestMixin:
    """Feed shell state into the autosuggestion engine.

    Mixed into :class:`LazyOwnShell`; invoked after a command executes to
    refresh the ghost-text suggestion.
    """

    def _read_recent_commands_for_autosuggest(self, limit: int = 5) -> list:
        """Return the last ``limit`` first-tokens from the session transcript.

        Args:
            limit: Maximum number of distinct command names to return.

        Returns:
            A list of command first-tokens. Empty when the file is absent.
        """
        try:
            sessions_dir = getattr(self, "sessions_dir", "sessions") or "sessions"
            path = os.path.join(sessions_dir, "LazyOwn_session_report.csv")
            if not os.path.isfile(path):
                return []
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                reader = csv.DictReader(fh)
                commands: list = []
                for row in reader:
                    for column in ("command", "tool", "name"):
                        value = (row.get(column) or "").strip().split()
                        if value:
                            commands.append(value[0])
                            break
                return commands[-limit:]
        except Exception:
            return []

    def _refresh_autosuggest(self, executed_command: str) -> None:
        """Recompute the active suggestion from the engine's provider chain.

        Args:
            executed_command: Raw string of the command that just ran.
        """
        engine = getattr(self, "_autosuggest", None)
        if engine is None:
            return
        enabled = str(self.params.get("enable_autosuggest", True)).lower() not in (
            "false",
            "0",
            "no",
        )
        engine.set_enabled(enabled)
        if not enabled:
            return
        context = _SuggestionContext(
            last_command=executed_command,
            phase=self.params.get("phase") or "",
            recent_commands=self._read_recent_commands_for_autosuggest(),
            target=self.params.get("rhost") or "",
            os_hint=str(self.params.get("os_id") or "unknown"),
        )
        engine.refresh(context)
