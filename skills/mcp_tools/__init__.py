"""Auto-discovered one-file-per-tool registry for the LazyOwn MCP server.

Historically every MCP tool's JSON schema lived inside one multi-thousand
line ``list_tools`` literal and its handler inside a giant ``call_tool``
if/elif chain in ``skills/lazyown_mcp.py``. This package replaces that
with one module per tool: each ``mcp_tools/<name>.py`` exposes a ``TOOL``
schema and a ``handle(arguments, tool_name, ctx)`` function. The runtime
discovers them declaratively, exactly like :mod:`cli.registry` does for
``cmd2`` command sets, so adding or moving a tool is a single new file and
no edit to the god-file.

Modules whose leaf name starts with an underscore (``_context``) hold
shared scaffolding and are skipped by discovery.
"""

from __future__ import annotations

import asyncio
import importlib
import logging
import pkgutil
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType

from mcp_tools._context import MCPContext

PACKAGE_NAME = "mcp_tools"
_UNDERSCORE_PREFIX = "_"
_REPO_ROOT = Path(__file__).resolve().parents[2]
_logger = logging.getLogger("mcp_tools")

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def iter_tool_modules() -> Iterator[ModuleType]:
    """Yield every discovered tool module exposing ``TOOL`` and ``handle``.

    Each non-underscore module under :mod:`mcp_tools` is imported and kept
    only when it declares both the ``TOOL`` schema and a ``handle``
    callable, so partial or helper modules are ignored rather than crashing
    discovery. A module that fails to import (for example an environment
    without an optional dependency) is logged and skipped so one broken
    tool never takes down the whole registry and, with it, the server.

    Yields:
        Each tool module that satisfies the one-file-per-tool contract.
    """
    pkg = importlib.import_module(PACKAGE_NAME)
    for info in pkgutil.iter_modules(pkg.__path__, prefix=f"{PACKAGE_NAME}."):
        leaf = info.name.rsplit(".", 1)[-1]
        if leaf.startswith(_UNDERSCORE_PREFIX):
            continue
        try:
            module = importlib.import_module(info.name)
        except Exception as exc:  # noqa: BLE001
            _logger.warning("skipping tool module %s: %s", info.name, exc)
            continue
        if hasattr(module, "TOOL") and hasattr(module, "handle"):
            yield module


def iter_schemas() -> Iterator[object]:
    """Yield the ``types.Tool`` schema of every discovered tool module."""
    for module in iter_tool_modules():
        yield module.TOOL


def register_handlers(handlers: dict, ctx: MCPContext) -> list[str]:
    """Bind each discovered tool's handler into the shared dispatch table.

    The runtime passes its ``_TOOL_HANDLERS`` dict and a built
    :class:`MCPContext`. Every tool handler is wrapped so the dispatch
    contract ``handler(arguments, tool_name)`` is honoured while the tool
    file keeps its clean ``handle(arguments, tool_name, ctx)`` signature.
    Both synchronous and coroutine handlers are supported.

    Args:
        handlers: The live dispatch table to populate in place.
        ctx: The dependency-injection context passed to each handler.

    Returns:
        The list of tool names registered, for logging and tests.
    """
    registered: list[str] = []
    for module in iter_tool_modules():
        name = module.TOOL.name
        handle = module.handle
        if asyncio.iscoroutinefunction(handle):

            async def _async_wrap(arguments, tool_name, _handle=handle):
                return await _handle(arguments, tool_name, ctx)

            handlers[name] = _async_wrap
        else:

            def _sync_wrap(arguments, tool_name, _handle=handle):
                return _handle(arguments, tool_name, ctx)

            handlers[name] = _sync_wrap
        registered.append(name)
    return registered
