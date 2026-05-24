"""``assign`` business logic.

Extracted from :class:`LazyOwnShell.do_assign` so the persistence and validation
behaviour can be unit-tested without booting the cmd2 shell.

Tier 2.5 promises:

- ``assign <key> <value>`` only succeeds when ``key`` is already part of the
  payload (no silent introduction of new keys).
- On success the live ``params`` dict is mutated in place AND a save callback
  is invoked so the change survives a shell restart.
- On failure (unknown key) nothing is mutated and no save callback fires.

Schema integration (additive, backwards compatible):

- When the key is registered in :data:`core.payload_schema.SCHEMA`, the value
  is coerced to the canonical type (``"5555"`` → ``5555`` for ports) before
  being stored, so downstream consumers no longer have to defensively cast.
- A schema validation failure for an existing key is reported through the
  optional ``on_issue`` callback. The assignment still goes through — the
  legacy contract was lenient, and the wizard is the right place to be
  strict.
"""

from __future__ import annotations

from typing import Any, Callable

from core.payload_schema import ValidationIssue, coerce_value, validate_value

SaveFn = Callable[[dict[str, Any]], None]
IssueFn = Callable[[ValidationIssue], None]


def apply_assign(
    params: dict[str, Any],
    key: str,
    value: Any,
    *,
    save: SaveFn | None = None,
    on_issue: IssueFn | None = None,
) -> bool:
    """Validate, mutate and persist a single payload assignment.

    Args:
        params: Live parameter dict. Mutated in place when ``key`` exists.
        key: Parameter name.
        value: New value to store.
        save: Optional callable invoked with ``params`` after a successful
            mutation. Pass :func:`core.config.save_payload` to persist to
            ``payload.json``. ``None`` skips persistence (useful for tests).
        on_issue: Optional callback invoked with the validation issue when
            the value fails the schema for ``key``. The assignment still
            proceeds — the callback exists only so the caller (typically
            the CLI) can surface a hint to the operator.

    Returns:
        ``True`` if ``key`` existed in ``params`` and was updated;
        ``False`` otherwise. Callers can use the return value to decide
        whether to refresh dependent state (e.g. aliases).
    """
    if key not in params:
        return False
    coerced = coerce_value(key, value)
    if on_issue is not None:
        issue = validate_value(key, coerced)
        if issue is not None:
            on_issue(issue)
    params[key] = coerced
    if save is not None:
        save(params)
    return True


__all__ = ["SaveFn", "IssueFn", "apply_assign"]
