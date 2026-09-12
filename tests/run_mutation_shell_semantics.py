"""Mutation gate for shell semantics and colored output.

Each mutation removes one rule from the shell-semantics contract and asserts
the matching test fails. Survival means the regression guard is not wired.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAFE_EXEC = BASE_DIR / "core" / "safe_exec.py"
HARDENING = BASE_DIR / "core" / "hardening.py"
SAFE_SUBPROCESS = BASE_DIR / "core" / "safe_subprocess.py"
TEST_FILE = "tests/test_shell_semantics.py"

MUTATIONS = (
    (
        "needs_shell_always_false",
        SAFE_EXEC,
        "    if \"&&\" in command:\n        return True\n    return bool(_SHELL_SYNTAX_PATTERN.search(command))",
        "    return False",
    ),
    (
        "terminal_env_never_forces",
        HARDENING,
        '        env.setdefault("CLICOLOR_FORCE", "1")\n        env.setdefault("FORCE_COLOR", "1")',
        "        pass",
    ),
    (
        "safe_runner_ignores_shell_syntax",
        SAFE_SUBPROCESS,
        '        argv = ["bash", "-c", command] if needs_shell(command) else (shlex.split(command) if command else [])',
        "        argv = shlex.split(command) if command else []",
    ),
)


def _run_tests() -> bool:
    """Return True when the shell-semantics tests pass."""
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
    originals = {path: path.read_text(encoding="utf-8") for _, path, _, _ in MUTATIONS}
    try:
        if not _run_tests():
            print("FAIL: baseline tests do not pass.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        for name, path, old, new in MUTATIONS:
            original = originals[path]
            if old not in original:
                print(f"BROKEN {name}: target not found")
                survived += 1
                continue
            path.write_text(original.replace(old, new, 1), encoding="utf-8")
            mutant_pass = _run_tests()
            path.write_text(original, encoding="utf-8")
            if mutant_pass:
                survived += 1
                print(f"SURVIVED {name}")
            else:
                killed += 1
                print(f"KILLED   {name}")

        print(f"Results: {killed} killed, {survived} survived")
        return 0 if survived == 0 else 1
    finally:
        for path, original in originals.items():
            path.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
