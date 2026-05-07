"""Diagnostics CommandSet (Tier 2 pilot).

A small, low-risk phase module that proves the ``CommandSet`` registration
flow works end-to-end against a live ``LazyOwnShell`` instance. It exposes
read-only commands operators can use to inspect the framework's runtime
state without mutating anything.

Subsequent tiers migrate the ~280 legacy ``do_*`` methods from
``lazyown.py`` into similar phase-scoped modules.
"""

from __future__ import annotations

import json
import platform
import sys

from cmd2 import with_category

from cli.commands._base import LazyOwnCommandSet


class DiagnosticsCommandSet(LazyOwnCommandSet):
    """Operator-facing diagnostics commands."""

    phase = "diagnostics"
    category = "Diagnostics"

    @with_category("Diagnostics")
    def do_lazy_runtime(self, _statement) -> None:
        """Print interpreter, platform and core LazyOwn paths."""
        info = {
            "python": sys.version.split()[0],
            "executable": sys.executable,
            "platform": platform.platform(),
            "cwd": str(__import__("pathlib").Path.cwd()),
        }
        print(json.dumps(info, indent=2))

    @with_category("Diagnostics")
    def do_lazy_payload_keys(self, _statement) -> None:
        """List the keys currently present in the parent shell's payload."""
        payload = self.params or {}
        if not payload:
            print("(payload empty or unavailable)")
            return
        for key in sorted(payload):
            print(key)


__all__ = ["DiagnosticsCommandSet"]
