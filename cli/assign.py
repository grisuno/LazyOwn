"""``assign`` business logic.

Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation
behaviour can be unit-tested without booting the cmd2 shell.

Tier 2.5 promises:

- ``assign <key> <value>`` only succeeds when ``key`` is already part of the
  payload (no silent introduction of new keys).
- On success the live ``params`` dict is mutated in place AND a save callback
  is invoked so the change survives a shell restart.
- On failure (unknown key) nothing is mutated and no save callback fires.
"""

from __future__ import annotations

from typing import Any, Callable

SaveFn = Callable[[dict[str, Any]], None]


def apply_assign(
    params: dict[str, Any],
    key: str,
    value: Any,
    *,
    save: SaveFn | None = None,
) -> bool:
    """Validate, mutate and persist a single payload assignment.

    Args:
        params: Live parameter dict. Mutated in place when ``key`` exists.
        key: Parameter name.
        value: New value to store.
        save: Optional callable invoked with ``params`` after a successful
            mutation. Pass :func:`core.config.save_payload` to persist to
            ``payload.json``. ``None`` skips persistence (useful for tests).

    Returns:
        ``True`` if ``key`` existed in ``params`` and was updated;
        ``False`` otherwise. Callers can use the return value to decide
        whether to refresh dependent state (e.g. aliases).
    """
    if key not in params:
        return False
    params[key] = value
    if save is not None:
        save(params)
    return True


__all__ = ["SaveFn", "apply_assign"]
