"""Mutation gate for the hardening-round fixes.

The tests in ``tests/test_hardening_round.py`` must fail when the fixes
regress: each mutation reintroduces one fixed defect and asserts the
suite kills the mutant.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET = BASE_DIR / "modules" / "loop" / "command_sanitize.py"
PATHS_TARGET = BASE_DIR / "core" / "paths.py"
SECRETS_TARGET = BASE_DIR / "core" / "secrets.py"
TEST_FILE = "tests/test_hardening_round.py"

MUTATIONS = {
    "quoting_destroyed_again": (
        TARGET,
        ("    return shlex.join(kept), reason", '    return " ".join(kept), reason'),
    ),
    "rw_downgraded_to_write_only": (
        PATHS_TARGET,
        (
            "        flags |= os.O_RDWR | os.O_CREAT",
            "        flags |= os.O_WRONLY | os.O_CREAT",
        ),
    ),
    "sealing_fail_open_again": (
        SECRETS_TARGET,
        (
            '        raise SecurityViolation(f"secret sealing failed: {type(exc).__name__}") from exc',
            '        log.warning("secret sealing failed: %s", type(exc).__name__)\n        return text',
        ),
    ),
}


def _run_tests() -> bool:
    """Return True when the hardening-round tests pass."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider"],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=str(BASE_DIR),
    )
    return result.returncode == 0


def main() -> int:
    """Run every mutant and return the process exit code."""
    originals = {path: path.read_text(encoding="utf-8") for path, _ in MUTATIONS.values()}
    try:
        if not _run_tests():
            print("FAIL: baseline tests do not pass.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        for name, (path, (old, new)) in MUTATIONS.items():
            mutated = originals[path].replace(old, new, 1)
            if mutated == originals[path]:
                print(f"SKIP: {name} — mutation anchor not found in {path.name}")
                continue
            path.write_text(mutated, encoding="utf-8")
            try:
                if _run_tests():
                    print(f"SURVIVED: {name}")
                    survived += 1
                else:
                    print(f"KILLED: {name}")
                    killed += 1
            finally:
                path.write_text(originals[path], encoding="utf-8")

        print(f"\n{killed} killed, {survived} survived")
        return 0 if survived == 0 else 1
    finally:
        for path, original in originals.items():
            path.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
