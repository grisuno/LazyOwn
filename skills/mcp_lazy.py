"""Single helper behind every lazy optional import of the MCP server.

Each ``_ensure_*`` wrapper in ``lazyown_mcp`` used to repeat the same
skeleton: return the cached flag when set, otherwise try the import,
bind names on success, store False on failure. Centralising the
skeleton here keeps one fail-closed policy (any import error disables
the feature instead of crashing the server) while every wrapper only
declares what to load.
"""

from __future__ import annotations

from typing import Any, Callable, MutableMapping

Loader = Callable[[MutableMapping[str, Any]], bool]


def ensure_optional(namespace: MutableMapping[str, Any], flag: str, loader: Loader) -> bool:
    """Return the cached flag or run ``loader`` once to compute it.

    Args:
        namespace: Module globals holding the flag and bound names.
        flag: Name of the availability flag inside ``namespace``.
        loader: Receives ``namespace``; binds imported names into it
            and returns True on success, False when it installed a
            fallback stub instead.

    Returns:
        True when the optional dependency is usable, False otherwise.
        Any exception from ``loader`` fails closed to False.
    """
    current = namespace.get(flag)
    if current is not None:
        return current
    try:
        namespace[flag] = bool(loader(namespace))
    except Exception:
        namespace[flag] = False
    return namespace[flag]
