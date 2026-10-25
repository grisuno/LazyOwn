"""Marketplace placeholder substitution must be shell-safe.

SDD contract: ``poc_tui.plugin_loader._replace_placeholders`` injects
payload values into commands executed with ``shell=True``. Values
arrive from scan data and operator config, so every substituted value
is wrapped in ``shlex.quote`` (the same remediation already applied
in ``modules/conditional_hooks.py``). Multi-word values become a
single quoted shell word; per-run flags travel as free args, which
are appended verbatim and never substituted.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

SRC = (Path(__file__).resolve().parent.parent / "poc_tui" / "plugin_loader.py").read_text(
    encoding="utf-8"
)


def _load_fn():
    tree = ast.parse(SRC)
    node = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "_replace_placeholders"
    )
    namespace: dict = {"re": re, "shlex": __import__("shlex")}
    exec(
        compile(ast.Module(body=[node], type_ignores=[]), "<subst>", "exec"),
        namespace,
    )
    return namespace["_replace_placeholders"]


class TestPlaceholderQuoting:
    def test_plain_values_pass_through(self) -> None:
        subst = _load_fn()
        assert subst("./tool scan {target}", {"target": "10.0.0.1"}) == "./tool scan 10.0.0.1"

    def test_injection_neutralized(self) -> None:
        subst = _load_fn()
        out = subst("./tool scan {target}", {"target": "10.0.0.1; rm -rf /"})
        assert out == "./tool scan '10.0.0.1; rm -rf /'"

    def test_command_substitution_neutralized(self) -> None:
        subst = _load_fn()
        out = subst("echo {name}", {"name": "$(id)"})
        assert out == "echo '$(id)'"

    def test_missing_key_left_verbatim(self) -> None:
        subst = _load_fn()
        assert subst("./tool {missing}", {}) == "./tool {missing}"

    def test_uses_shlex_quote(self) -> None:
        tree = ast.parse(SRC)
        node = next(
            n
            for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name == "_replace_placeholders"
        )
        calls = {
            n.func.attr
            for n in ast.walk(node)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        }
        assert "quote" in calls, "_replace_placeholders must wrap values in shlex.quote"
