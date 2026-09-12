"""Mutation gate for the contract manifest drift checker.

Each mutation weakens one resolution rule in
``scripts/check_contract_manifest.py``. ``tests/test_contract_manifest.py``
must kill every mutant. Survival means a documented contract could drift
without CI noticing.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE = BASE_DIR / "scripts" / "check_contract_manifest.py"
TEST_FILE = "tests/test_contract_manifest.py"

MUTATIONS = {
    "missing_path_never_reported": {
        "old": "return candidate if candidate.is_file() else None",
        "new": "return candidate",
    },
    "dotted_symbol_always_resolves": {
        "old": "return all(member in names for member in remaining)",
        "new": "return True",
    },
    "doc_imports_never_collected": {
        "old": "    pairs: list[tuple[str, str]] = []\n    for line in text.splitlines():",
        "new": "    return []\n    pairs: list[tuple[str, str]] = []\n    for line in text.splitlines():",
    },
}


def _run_tests() -> bool:
    """Return True when the manifest test module passes."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(BASE_DIR),
    )
    return result.returncode == 0


def main() -> int:
    """Run every mutant and return the process exit code."""
    original = SOURCE.read_text(encoding="utf-8")

    try:
        if not _run_tests():
            print("FAIL: baseline tests do not pass.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        for name, mutation in MUTATIONS.items():
            if mutation["old"] not in original:
                print(f"BROKEN {name}: target expression not found.")
                survived += 1
                continue
            SOURCE.write_text(original.replace(mutation["old"], mutation["new"], 1), encoding="utf-8")
            mutant_pass = _run_tests()
            SOURCE.write_text(original, encoding="utf-8")
            if mutant_pass:
                survived += 1
                print(f"SURVIVED {name}")
            else:
                killed += 1
                print(f"KILLED   {name}")

        print(f"Results: {killed} killed, {survived} survived")
        return 0 if survived == 0 else 1
    finally:
        SOURCE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
