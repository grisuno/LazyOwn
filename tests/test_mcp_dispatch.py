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

import sys  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills"))

import mcp_tools  # noqa: E402

MIGRATED = ["lazyown_run_command", "lazyown_get_config", "lazyown_rea"]


def _package_names() -> set[str]:
    return {module.TOOL.name for module in mcp_tools.iter_tool_modules()}


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
        package = _package_names()
        for name in MIGRATED:
            assert name in package, f"{name} must be served by the mcp_tools package"

    def test_migrated_handlers_absent_from_fallback(self) -> None:
        branches = _fallback_branches()
        registered = _registered()
        for name in MIGRATED:
            assert name not in branches, f"{name} elif must be removed"
            assert name not in registered, f"{name} must not remain a god-file handler"


def test_set_config_refuses_null_values():
    """set_config must never null out payload keys (static contract).

    The handler runs inside MCP server processes where a live-file
    round-trip test is unsafe; assert the fail-closed branch exists. The
    handler now lives in the one-file-per-tool package, so the contract is
    asserted against that module.
    """
    set_config_src = (
        Path(__file__).resolve().parent.parent / "skills" / "mcp_tools" / "set_config.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(set_config_src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "handle":
            src = ast.get_source_segment(set_config_src, node) or ""
            assert "Refused" in src and "coerced is None" in src
            return
    raise AssertionError("set_config handle not found")


def test_new_chain_shell_tools_have_defs_and_handlers():
    """apt_chain/atomic_shell/atomic_clean are served by the package registry."""
    expected = {"lazyown_apt_chain", "lazyown_atomic_shell", "lazyown_atomic_clean"}
    package = _package_names()
    assert expected <= package, f"missing from package: {expected - package}"


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
    """No MCP path may request an interactive shell session.

    The atomic_shell tool now lives in the one-file-per-tool package; the
    security contract (interactive=False, never interactive=True) is
    asserted against that module.
    """
    atomic_shell_src = (
        Path(__file__).resolve().parent.parent / "skills" / "mcp_tools" / "atomic_shell.py"
    ).read_text(encoding="utf-8")
    assert "interactive=False" in atomic_shell_src
    assert "interactive=True" not in atomic_shell_src
