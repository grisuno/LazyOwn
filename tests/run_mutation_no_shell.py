"""Mutation gate for the no-shell execution contract.

The scanner in ``tests/test_no_shell_execution.py`` must fail when a real
``os.system`` call or a manual ``sys.stdout`` assignment reappears. Each
mutation injects one of those into a production file and asserts the scanner
kills the mutant.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET = BASE_DIR / "pwntomate.py"
TEST_FILE = "tests/test_no_shell_execution.py"

MUTATIONS = {
    "os_system_reintroduced": '\nimport os\n\nos.system("true")\n',
    "stdout_reassigned": "\nimport sys\n\nsys.stdout = None\n",
}


def _run_tests() -> bool:
    """Return True when the no-shell contract tests pass."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider"],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=str(BASE_DIR),
    )
    return result.returncode == 0


def main() -> int:
    """Run every mutant and return the process exit code."""
    original = TARGET.read_text(encoding="utf-8")
    try:
        if not _run_tests():
            print("FAIL: baseline tests do not pass.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        for name, snippet in MUTATIONS.items():
            TARGET.write_text(original + snippet, encoding="utf-8")
            mutant_pass = _run_tests()
            TARGET.write_text(original, encoding="utf-8")
            if mutant_pass:
                survived += 1
                print(f"SURVIVED {name}")
            else:
                killed += 1
                print(f"KILLED   {name}")

        print(f"Results: {killed} killed, {survived} survived")
        return 0 if survived == 0 else 1
    finally:
        TARGET.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
