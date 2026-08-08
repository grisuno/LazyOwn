"""Mutation testing runner for core.api_authz and core.logging.

Introduces targeted mutations into the production code and verifies
that the test suite detects every one. A surviving mutant means the
test is too weak and must be hardened.
"""

from __future__ import annotations

import importlib
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

_MUTATIONS: dict[str, dict] = {
    "api_authz_invert_expiration": {
        "file": "core/api_authz.py",
        "line": "return time.time() > self.expires_at",
        "mutation": "return time.time() < self.expires_at",
        "test": "tests/test_api_authz.py::TestApiKey::test_detects_expiration_correctly",
    },
    "api_authz_skip_validate_expiration": {
        "file": "core/api_authz.py",
        "line": "        if api_key.is_expired():\n            return None",
        "mutation": "        if False:\n            return None",
        "test": "tests/test_api_authz.py::TestApiKeyStore::test_rejects_expired_key",
    },
    "api_authz_skip_permission_enforcement": {
        "file": "core/api_authz.py",
        "line": "            if permissions and not api_key.has_all_permissions(permissions):",
        "mutation": "            if False:",
        "test": "tests/test_api_authz.py::TestRequireApiAuth::test_rejects_key_with_insufficient_permissions_with_403",
    },
    "api_authz_skip_invalid_key_check": {
        "file": "core/api_authz.py",
        "line": "            if api_key is None:\n                abort(401, description=\"Invalid or expired API key\")",
        "mutation": "            if False:\n                abort(401, description=\"Invalid or expired API key\")",
        "test": "tests/test_api_authz.py::TestRequireApiAuth::test_rejects_invalid_key_with_401",
    },
    "logging_skip_redaction": {
        "file": "core/logging.py",
        "line": "                if clean_key in self._redact:",
        "mutation": "                if False:",
        "test": "tests/test_structured_logging.py::TestJsonLineFormatter::test_redacts_sensitive_extra_fields",
    },
}


def _apply_mutation(source: str, data: dict) -> str | None:
    """Apply the mutation to *source*. Returns mutated string or None."""
    if data["line"] not in source:
        return None
    return source.replace(data["line"], data["mutation"], 1)


def _run_mutation_subprocess(test: str) -> bool:
    """Run pytest for *test*. Returns True if test PASSED (mutant survived)."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test, "-x", "-q", "--tb=no"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(REPO_ROOT),
    )
    return result.returncode == 0


def run() -> dict:
    """Run all mutations. Returns dict with killed/survived counts."""
    print("\n=== LazyOwn Mutation Tests: api_authz + logging ===\n")
    results = {"killed": 0, "survived": 0, "skipped": 0, "total": len(_MUTATIONS)}

    for i, (name, data) in enumerate(_MUTATIONS.items(), 1):
        source_path = REPO_ROOT / data["file"]
        original = source_path.read_text(encoding="utf-8")
        mutated = _apply_mutation(original, data)

        status = "???"
        if mutated is None:
            status = "SKIP (no match)"
            results["skipped"] += 1
        elif mutated == original:
            status = "SKIP (no change)"
            results["skipped"] += 1
        else:
            try:
                source_path.write_text(mutated, encoding="utf-8")
                importlib.invalidate_caches()
                survived = _run_mutation_subprocess(data["test"])
                if survived:
                    status = "SURVIVED"
                    results["survived"] += 1
                else:
                    status = "KILLED"
                    results["killed"] += 1
            finally:
                source_path.write_text(original, encoding="utf-8")
                importlib.invalidate_caches()
        print(f"[{i}/{len(_MUTATIONS)}] {name}: {status}")

    print(f"\n=== Results: {results['killed']} killed, {results['survived']} survived, "
          f"{results['skipped']} skipped ===\n")
    return results


if __name__ == "__main__":
    results = run()
    sys.exit(0 if results["survived"] == 0 else 1)
