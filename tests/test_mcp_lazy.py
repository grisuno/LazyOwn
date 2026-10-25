"""Contract for the unified MCP lazy-import helper.

SDD contract: ``skills/mcp_lazy.ensure_optional`` owns the
cache-check / import / fail-closed skeleton. Every ``_ensure_*``
wrapper in ``skills/lazyown_mcp.py`` must delegate to it instead of
repeating the skeleton, and the helper must preserve the observable
semantics: cached value returned untouched, successful loader binds
names and yields True, failing loader yields False without raising.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "skills"))

from mcp_lazy import ensure_optional  # noqa: E402

MCP = (_ROOT / "skills" / "lazyown_mcp.py").read_text(encoding="utf-8")

WRAPPERS = [
    "_ensure_engine",
    "_ensure_bridge",
    "_ensure_state",
    "_ensure_recommender",
    "_ensure_narrator",
    "_ensure_policy",
    "_ensure_facts",
    "_ensure_objectives",
    "_ensure_llm",
    "_ensure_automapper",
    "_ensure_pdb",
    "_ensure_hive",
    "_ensure_auto",
    "_ensure_aci",
]


class TestEnsureOptional:
    def test_success_binds_and_caches(self) -> None:
        namespace: dict = {}
        calls = []

        def loader(ns: dict) -> bool:
            calls.append(1)
            ns["thing"] = object()
            return True

        assert ensure_optional(namespace, "_X_AVAILABLE", loader) is True
        assert namespace["_X_AVAILABLE"] is True
        assert "thing" in namespace
        assert ensure_optional(namespace, "_X_AVAILABLE", loader) is True
        assert len(calls) == 1

    def test_cached_value_returned_untouched(self) -> None:
        namespace = {"_X_AVAILABLE": False}

        def loader(ns: dict) -> bool:
            raise AssertionError("loader must not run when cached")

        assert ensure_optional(namespace, "_X_AVAILABLE", loader) is False

    def test_exception_fails_closed(self) -> None:
        namespace: dict = {}

        def loader(ns: dict) -> bool:
            raise RuntimeError("broken import")

        assert ensure_optional(namespace, "_X_AVAILABLE", loader) is False
        assert namespace["_X_AVAILABLE"] is False

    def test_false_loader_with_fallback(self) -> None:
        namespace: dict = {}

        def loader(ns: dict) -> bool:
            ns["tool"] = lambda: None
            return False

        assert ensure_optional(namespace, "_X_AVAILABLE", loader) is False
        assert callable(namespace["tool"])


class TestWrappersDelegate:
    def test_all_wrappers_delegate_to_helper(self) -> None:
        tree = ast.parse(MCP)
        found = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in WRAPPERS:
                found[node.name] = node
        missing = [name for name in WRAPPERS if name not in found]
        assert not missing, f"wrappers missing: {missing}"
        for name, node in found.items():
            calls = [
                n
                for n in ast.walk(node)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == "_ensure_optional"
            ]
            assert calls, f"{name} must delegate to _ensure_optional"
            loaders = [
                n
                for n in node.body
                if isinstance(n, ast.FunctionDef) and n.name == "_load"
            ]
            assert loaders, f"{name} must declare its imports in a _load step"
            load_ids = {id(n) for n in ast.walk(loaders[0])}
            direct = [
                n
                for n in ast.walk(node)
                if isinstance(n, ast.ExceptHandler) and id(n) not in load_ids
            ]
            assert not direct, f"{name} must not repeat try/except skeleton"
