"""Backward-compatibility shims for deprecated scripts.

Contract: the canonical location of these scripts is now
``contrib/legacy/``. Every module in this package is a symlink to its
counterpart there, so ``python3 modules/legacy/<name>.py``,
``run_script("modules/legacy/<name>.py")`` and
``from modules.legacy.<name> import ...`` keep working without any
caller change. New code must import from ``contrib.legacy`` directly
and must not add new modules here.
"""

from __future__ import annotations

import pathlib

_CONTRIB_LEGACY = pathlib.Path(__file__).resolve().parents[2] / "contrib" / "legacy"

__path__ = [str(_CONTRIB_LEGACY), __path__[0]]  # noqa: PTH201
__all__: list[str] = []
