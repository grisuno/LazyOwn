"""lazymode: programmatic (code-mode) execution over the LazyOwn SDK.

Exposes the two script runners and the surface index that back the two
MCP tools (search and execute). One script replaces many tool round-trips
and keeps intermediate output out of the model context.
"""

from __future__ import annotations

from sdk.lazymode.index import build_index, search
from sdk.lazymode.runner import LazymodeResult, run, run_lua, run_python

__all__ = [
    "LazymodeResult",
    "run",
    "run_python",
    "run_lua",
    "build_index",
    "search",
]
