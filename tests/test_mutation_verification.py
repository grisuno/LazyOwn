"""Mutation testing verification - manually verifies that mutations would be caught."""

import ast
import sys
import tempfile
from pathlib import Path

from modules.db import LazyOwnDB


def test_sql_injection_blocked():
    """If VALID_TABLES check is removed, SQL injection becomes possible."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = LazyOwnDB(Path(tmpdir) / "test.db")
        try:
            db.export_csv("hosts; DROP TABLE hosts--")
            print("FAIL: No exception raised - SQL injection possible!")
            return False
        except ValueError:
            print("PASS: SQL injection blocked by table name allowlist")
            return True


def test_hmac_compare_digest_used():
    """If hmac.compare_digest is replaced with ==, timing attack is possible."""
    source = Path("lazyc2.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "check_auth":
            func_source = ast.get_source_segment(source, node)
            if "hmac.compare_digest" not in func_source:
                print("FAIL: hmac.compare_digest NOT used")
                return False
            if "username == USERNAME" in func_source:
                print("FAIL: Plaintext comparison still present")
                return False
            print("PASS: hmac.compare_digest used, no plaintext comparison")
            return True
    print("FAIL: check_auth function not found")
    return False


def test_shell_false_in_safe_runner():
    """If shell=True is restored in SafeRunner, shell injection is possible."""
    source = Path("core/safe_subprocess.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == "run":
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant):
                        if kw.value.value is False:
                            print("PASS: shell=False confirmed in SafeRunner")
                            return True
                        else:
                            print(f"FAIL: shell={kw.value.value}")
                            return False
    print("PASS: No shell=True found")
    return True


def test_pickle_removed():
    """If pickle is re-imported, RCE via deserialization becomes possible."""
    source = Path("utils.py").read_text(encoding="utf-8")
    for line in source.split("\n"):
        stripped = line.strip()
        if stripped.startswith("import pickle") or stripped.startswith("from pickle"):
            print(f"FAIL: pickle still imported: {stripped}")
            return False
    print("PASS: pickle not imported in utils.py")
    return True


def test_no_hardcoded_secrets():
    """If hardcoded secrets are restored, they leak to git history."""
    source = Path("utils.py").read_text(encoding="utf-8")
    for secret in ["LAZYOWNBLUEADMIN123", "LAZYOWNREDADMIN123", "LAZYOWNADMIN123"]:
        if secret in source:
            print(f"FAIL: Hardcoded secret {secret} still present")
            return False
    print("PASS: No hardcoded secrets in utils.py")
    return True


if __name__ == "__main__":
    results = [
        test_sql_injection_blocked(),
        test_hmac_compare_digest_used(),
        test_shell_false_in_safe_runner(),
        test_pickle_removed(),
        test_no_hardcoded_secrets(),
    ]
    print()
    if all(results):
        print("ALL MUTATION TESTS PASSED - mutations would be caught!")
        sys.exit(0)
    else:
        print("SOME MUTATION TESTS FAILED")
        sys.exit(1)
