"""The C2 must not build the CLI shell at module load.

SDD contract: ``lazyc2.py`` runs as ``__main__`` and previously did
``from lazyown import LazyOwnShell`` at the top level plus an eager
``shell = LazyOwnShell()``. Module load must not touch the CLI tree:
the shell is created on first use by ``_init_shell`` (same boot
sequence: StringIO stdout, ``onecmd("p")``,
``onecmd("create_session_json")``) and every existing ``shell.*``
call site keeps working through the ``_LazyShellProxy`` stand-in.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYC2_SRC = (REPO_ROOT / "lazyc2.py").read_text(encoding="utf-8")


def _module_tree() -> ast.Module:
    return ast.parse(LAZYC2_SRC)


def _load_proxy_class():
    """Exec the ``_LazyShellProxy`` class definition in isolation.

    Returns:
        The class object plus the namespace it was exec'd with.
    """
    tree = _module_tree()
    node = next(
        n
        for n in tree.body
        if isinstance(n, ast.ClassDef) and n.name == "_LazyShellProxy"
    )
    namespace: dict = {}
    created = {"count": 0}

    class _FakeShell:
        def __init__(self) -> None:
            created["count"] += 1
            self.log: list = []

        def one_cmd(self, command: str) -> str:
            self.log.append(command)
            return f"out:{command}"

    fake = _FakeShell()

    def _init_shell():
        return fake

    namespace["_init_shell"] = _init_shell
    exec(
        compile(ast.Module(body=[node], type_ignores=[]), "<proxy>", "exec"),
        namespace,
    )
    return namespace["_LazyShellProxy"], created


class TestNoEagerCliBuild:
    def test_no_lazyown_import_at_top_level(self) -> None:
        tree = _module_tree()
        offenders = []
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "lazyown":
                offenders.append(ast.dump(node))
            if isinstance(node, ast.Import) and any(
                a.name == "lazyown" or a.name.startswith("lazyown.")
                for a in node.names
            ):
                offenders.append(ast.dump(node))
        assert not offenders, f"top-level CLI imports: {offenders}"

    def test_no_eager_shell_build(self) -> None:
        tree = _module_tree()
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "shell" for t in node.targets
            ):
                assert not (
                    isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == "LazyOwnShell"
                ), "shell must not be built at module top level"

    def test_lazy_accessor_with_boot_sequence(self) -> None:
        tree = _module_tree()
        names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
        assert "_init_shell" in names
        init = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "_init_shell"
        )
        body_src = ast.dump(init)
        assert "LazyOwnShell" in body_src
        assert "StringIO" in body_src
        assert "create_session_json" in LAZYC2_SRC


class TestLazyShellProxy:
    def test_reads_forward_and_share_target(self) -> None:
        proxy_cls, _ = _load_proxy_class()
        proxy = proxy_cls()
        assert proxy.one_cmd("ping") == "out:ping"
        assert proxy.one_cmd("ping") == "out:ping"
        assert proxy._target() is proxy._target()

    def test_writes_forward(self) -> None:
        proxy_cls, _ = _load_proxy_class()
        proxy = proxy_cls()
        proxy.custom_flag = "yes"
        assert proxy.custom_flag == "yes"
        assert proxy._target().custom_flag == "yes"

    def test_shell_output_attribute(self) -> None:
        proxy_cls, _ = _load_proxy_class()
        proxy = proxy_cls()
        proxy.output = "captured"
        assert proxy.output == "captured"
