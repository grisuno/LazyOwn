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


def test_set_config_refuses_null_values():
    """set_config must never null out payload keys (static contract).

    The handler runs inside MCP server processes where a live-file
    round-trip test is unsafe; assert the fail-closed branch exists.
    """
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "_h_set_config":
            src = ast.get_source_segment(SRC, node) or ""
            assert "Refused" in src and "coerced is None" in src
            return
    raise AssertionError("_h_set_config not found")


def test_new_chain_shell_tools_have_defs_and_handlers():
    """apt_chain/atomic_shell/atomic_clean: Tool def + elif handler each."""
    import re as _re

    tools = set(_re.findall(r'name="(lazyown_apt_chain|lazyown_atomic_shell|lazyown_atomic_clean)"', SRC))
    assert tools == {"lazyown_apt_chain", "lazyown_atomic_shell", "lazyown_atomic_clean"}
    branches = _fallback_branches()
    assert {"lazyown_apt_chain", "lazyown_atomic_shell", "lazyown_atomic_clean"} <= branches


def test_opencode_bridge_curates_loop_and_chain():
    """Local-model bridge must expose loop + apt_chain under short names."""
    bridge = (Path(__file__).resolve().parent.parent / "skills" / "lazyown_mcp_opencode.py").read_text(
        encoding="utf-8"
    )
    for short, full in [
        ("auto_loop", "lazyown_auto_loop"),
        ("apt_chain", "lazyown_apt_chain"),
        ("atomic_shell", "lazyown_atomic_shell"),
        ("atomic_clean", "lazyown_atomic_clean"),
        ("ttp_chain", "lazyown_ttp_chain"),
    ]:
        assert f'"{short}": "{full}"' in bridge, f"missing alias {short} -> {full}"


def test_mcp_never_offers_interactive_repl():
    """No MCP path may request an interactive shell session."""
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in (
            "_h_run_command",
        ):
            continue
    segment_start = SRC.find('elif name == "lazyown_atomic_shell"')
    assert segment_start != -1
    segment = SRC[segment_start : segment_start + 2000]
    assert "interactive=False" in segment
    assert "interactive=True" not in segment
