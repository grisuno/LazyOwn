"""Contract for the one-file-per-tool MCP registry (``skills/mcp_tools``).

SDD contract: every tool migrated into ``mcp_tools`` is discovered by the
registry, is import-pure (never imports the ``lazyown_mcp`` runtime), and
is served by exactly one path. A name may not appear both in the registry
and in the legacy ``list_tools`` literal or ``@register_handler`` set of
``lazyown_mcp.py``.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "skills"))

import mcp_tools  # noqa: E402
from mcp_tools._context import MCPContext  # noqa: E402

_MCP_SRC = (_ROOT / "skills" / "lazyown_mcp.py").read_text(encoding="utf-8")
_TOOLS_DIR = _ROOT / "skills" / "mcp_tools"


def _registry_names() -> set[str]:
    return {module.TOOL.name for module in mcp_tools.iter_tool_modules()}


def _legacy_schema_names() -> set[str]:
    tree = ast.parse(_MCP_SRC)
    names: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "Tool"
        ):
            for kw in node.keywords:
                if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                    names.add(kw.value.value)
    return names


def _legacy_handler_names() -> set[str]:
    tree = ast.parse(_MCP_SRC)
    names: set[str] = set()
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


class TestRegistryDiscovery:
    def test_reference_tool_discovered(self) -> None:
        assert "lazyown_get_config" in _registry_names()

    def test_register_handlers_populates_table(self) -> None:
        table: dict = {}
        ctx = MCPContext(
            text=lambda name, content: [content],
            load_payload=dict,
            save_payload=lambda data: "",
            lazyown_dir=Path("."),
            sessions_dir=Path("sessions"),
            modules_dir=Path("modules"),
            skills_dir=Path("skills"),
            run_command=lambda command, timeout: "",
            c2_request=lambda path, method="GET", body=None: {},
            get_policy=lambda: None,
            get_transcript=lambda: None,
            get_perm_system=lambda: None,
            get_hooks=lambda: None,
            get_claudemd=lambda: None,
            job_store=None,
            list_tools=lambda: [],
            sitrep_recommendations=lambda *a, **k: [],
        )
        registered = mcp_tools.register_handlers(table, ctx)
        assert set(registered) == _registry_names()
        for name in registered:
            assert name in table


class TestSingleOwnership:
    def test_no_duplicate_schema(self) -> None:
        overlap = _registry_names() & _legacy_schema_names()
        assert not overlap, f"tool schema served by both paths: {sorted(overlap)}"

    def test_no_duplicate_handler(self) -> None:
        overlap = _registry_names() & _legacy_handler_names()
        assert not overlap, f"handler served by both paths: {sorted(overlap)}"


class TestImportPurity:
    def test_tool_modules_do_not_import_runtime(self) -> None:
        offenders: list[str] = []
        for path in _TOOLS_DIR.glob("*.py"):
            if path.name.startswith("_") or path.name == "__init__.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    if any(alias.name == "lazyown_mcp" for alias in node.names):
                        offenders.append(path.name)
                elif isinstance(node, ast.ImportFrom):
                    if (node.module or "").split(".")[0] == "lazyown_mcp":
                        offenders.append(path.name)
        assert not offenders, f"tool files importing the runtime: {sorted(set(offenders))}"
