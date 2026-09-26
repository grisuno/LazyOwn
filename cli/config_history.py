"""In-memory configuration history with undo and diff.

Assign and set commands mutate payload.json without a safety net. This
value object keeps a bounded stack of snapshots so undo restores the
previous state and diff explains what changed since session start.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConfigHistoryConfig:
    """Centralized knobs for history depth."""

    max_depth: int = 50


@dataclass
class ConfigHistory:
    """Bounded stack of configuration snapshots."""

    config: ConfigHistoryConfig = field(default_factory=ConfigHistoryConfig)
    _stack: list[dict[str, Any]] = field(default_factory=list, repr=False)
    _baseline: dict[str, Any] = field(default_factory=dict, repr=False)

    def capture_baseline(self, state: dict[str, Any]) -> None:
        """Store session-start snapshot used by diff.

        Args:
            state: Current configuration mapping.
        """
        self._baseline = deepcopy(dict(state))

    def push(self, state: dict[str, Any]) -> None:
        """Push a snapshot before mutation.

        Args:
            state: Configuration mapping before the change.
        """
        self._stack.append(deepcopy(dict(state)))
        if len(self._stack) > self.config.max_depth:
            del self._stack[0 : len(self._stack) - self.config.max_depth]

    def undo(self) -> dict[str, Any] | None:
        """Pop the newest snapshot.

        Returns:
            Previous state or None when the stack is empty.
        """
        if not self._stack:
            return None
        return self._stack.pop()

    def diff(self, current: dict[str, Any]) -> dict[str, tuple[Any, Any]]:
        """Compare current state against the baseline.

        Args:
            current: Live configuration mapping.

        Returns:
            Mapping of key to (old, new) for changed keys only.
        """
        changes: dict[str, tuple[Any, Any]] = {}
        keys = set(self._baseline) | set(current)
        for key in sorted(keys):
            old = self._baseline.get(key)
            new = current.get(key)
            if old != new:
                changes[key] = (old, new)
        return changes

    def depth(self) -> int:
        """Return number of stored undo steps."""
        return len(self._stack)


def get_shell_history(shell: Any) -> ConfigHistory:
    """Return the ConfigHistory bound to a shell, creating it on demand.

    Args:
        shell: Parent shell object used as attribute host.

    Returns:
        The shared ConfigHistory instance.
    """
    existing = getattr(shell, "_config_history", None)
    if isinstance(existing, ConfigHistory):
        return existing
    created = ConfigHistory()
    try:
        object.__setattr__(shell, "_config_history", created)
    except Exception:
        try:
            shell._config_history = created
        except Exception:
            return created
    return created


def track_before(history: ConfigHistory, state: dict[str, Any]) -> None:
    """Capture baseline on first use then push a pre-mutation snapshot.

    Args:
        history: Shared history instance.
        state: Configuration mapping before mutation.
    """
    if not history._baseline:
        history.capture_baseline(state)
    history.push(state)


__all__ = ["ConfigHistory", "ConfigHistoryConfig", "get_shell_history", "track_before"]
