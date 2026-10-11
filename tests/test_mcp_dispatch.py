"""call_tool dispatches through the handler registry.

SDD contract: ``_TOOL_HANDLERS`` (populated by ``@register_handler``)
is checked before the legacy ``if/elif`` fallback inside
``call_tool``. No ``if/elif`` branch may duplicate a registered name
(such branches are unreachable dead code), and migrated handlers
must stay registered under their tool names.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

SRC = (Path(__file__).resolve().parent.parent / "skills" / "lazyown_mcp.py").read_text(
    encoding="utf-8"
)

MIGRATED = ["lazyown_ack_event", "lazyown_c2_status"]


def _registered() -> set[str]:
    tree = ast.parse(SRC)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for deco in node.decorator_list:
                if (
                    isinstance(deco, ast.Call)
                    and isinstance(deco.func, ast.Name)
                    and deco.func.id == "register_handler"
                    and deco.args
                    and isinstance(deco.args[0], ast.Constant)
                ):
                    names.add(deco.args[0].value)
    return names


def _fallback_branches() -> set[str]:
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "call_tool":
            segment = ast.get_source_segment(SRC, node)
            return set(
                re.findall(r"(?:if|elif) name == [\"']([^\"']+)[\"']", segment)
            )
    raise AssertionError("call_tool not found")


class TestRegistryDispatch:
    def test_no_dead_duplicate_branches(self) -> None:
        overlap = _registered() & _fallback_branches()
        assert not overlap, f"unreachable duplicate branches: {sorted(overlap)}"

    def test_migrated_handlers_registered(self) -> None:
        registered = _registered()
        for name in MIGRATED:
            assert name in registered, f"{name} must be registry-dispatched"

    def test_migrated_handlers_absent_from_fallback(self) -> None:
        branches = _fallback_branches()
        for name in MIGRATED:
            assert name not in branches, f"{name} elif must be removed"
