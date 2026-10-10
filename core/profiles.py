"""Runtime profiles: ``light`` vs ``full`` installations.

The profile selects how much of the framework is expected to be present:

- ``full`` (default): every current behavior. Shell, C2, recon, analytics,
  and optional AI/LLM features that degrade gracefully when their packages
  are missing.
- ``light``: shell + C2 + recon core without the analytics and AI stack.
  The installer skips the heavy data/AI distributions and ``doctor`` does
  not require them.

Selection is explicit and never guessed: the ``LAZYOWN_PROFILE`` environment
variable wins, otherwise ``full`` applies. Anything else is a
:exc:`ValueError` so typos fail loudly instead of silently changing behavior.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import TypeVar

_SpecT = TypeVar("_SpecT")

PROFILE_LIGHT = "light"
PROFILE_FULL = "full"
PROFILE_ENV_VAR = "LAZYOWN_PROFILE"

_KNOWN_PROFILES = frozenset({PROFILE_LIGHT, PROFILE_FULL})

LIGHT_SKIPPED_IMPORTS = frozenset({"pandas", "pyarrow", "networkx", "groq"})
"""Import names ``doctor`` does not check under the light profile.

``pandas``/``pyarrow``/``networkx`` back reports, parquet bases, and graphs;
``groq`` backs the optional LLM provider. None of them is needed to run the
shell, the C2, or recon, so a light install is healthy without them.
"""


def active_profile() -> str:
    """Return the selected runtime profile.

    Returns:
        ``"light"`` when ``LAZYOWN_PROFILE=light`` (case-insensitive,
        surrounding whitespace ignored), otherwise ``"full"``.

    Raises:
        ValueError: When ``LAZYOWN_PROFILE`` is set to anything else.
    """
    raw = os.environ.get(PROFILE_ENV_VAR, "")
    normalized = raw.strip().lower()
    if not normalized:
        return PROFILE_FULL
    if normalized not in _KNOWN_PROFILES:
        raise ValueError(f"Unknown {PROFILE_ENV_VAR}={raw!r}; expected 'light' or 'full'.")
    return normalized


def is_light() -> bool:
    """Return ``True`` when the light profile is selected."""
    return active_profile() == PROFILE_LIGHT


def specs_for_profile(specs: Sequence[_SpecT]) -> list[_SpecT]:
    """Filter dependency specs down to the ones the active profile needs.

    Args:
        specs: :class:`cli.doctor.PackageSpec` entries (or any objects with
            an ``import_name`` attribute).

    Returns:
        Full list under the full profile; the list minus
        :data:`LIGHT_SKIPPED_IMPORTS` under the light profile.
    """
    if not is_light():
        return list(specs)
    return [s for s in specs if getattr(s, "import_name", None) not in LIGHT_SKIPPED_IMPORTS]
