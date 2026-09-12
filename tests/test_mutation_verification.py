"""Mutation verification contracts.

Each test encodes a mutation that the suite must catch. If the guard under
test is removed, the matching test fails. The tests assert, so pytest records
a real pass or fail instead of warning about a returned value.
"""

from __future__ import annotations

import ast
import tempfile
from pathlib import Path

import pytest

from modules.db import LazyOwnDB


def test_sql_injection_blocked() -> None:
    """A table name with SQL metacharacters is rejected by the allowlist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = LazyOwnDB(Path(tmpdir) / "test.db")
        with pytest.raises(ValueError):
            db.export_csv("hosts; DROP TABLE hosts--")


def test_hmac_compare_digest_used() -> None:
    """check_auth uses hmac.compare_digest and no plaintext comparison."""
    source = Path("lazyc2.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    check_auth = next(
        (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "check_auth"),
        None,
    )
    assert check_auth is not None, "check_auth function not found"
    func_source = ast.get_source_segment(source, check_auth) or ""
    assert "hmac.compare_digest" in func_source
    assert "username == USERNAME" not in func_source


def test_shell_false_in_safe_runner() -> None:
    """core/safe_subprocess.py runs every command with shell=False."""
    source = Path("core/safe_subprocess.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    shell_values = [
        keyword.value.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "run"
        for keyword in node.keywords
        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant)
    ]
    assert shell_values, "no shell keyword found in safe_subprocess"
    assert all(value is False for value in shell_values)


def test_pickle_removed() -> None:
    """utils.py does not import pickle."""
    source = Path("utils.py").read_text(encoding="utf-8")
    assert "import pickle" not in source
    assert "from pickle" not in source


def test_no_hardcoded_secrets() -> None:
    """utils.py does not embed the legacy bootstrap passwords."""
    source = Path("utils.py").read_text(encoding="utf-8")
    for secret in ("LAZYOWNBLUEADMIN123", "LAZYOWNREDADMIN123", "LAZYOWNADMIN123"):
        assert secret not in source, f"hardcoded secret present: {secret}"
