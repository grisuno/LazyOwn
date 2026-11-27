"""Mutation gate for the hardening-round fixes.

The tests in ``tests/test_hardening_round.py`` must fail when the fixes
regress: each mutation reintroduces one fixed defect and asserts the
suite kills the mutant. Mutations run against a throwaway copy of the
Python sources under a temp directory — the working tree is never
modified. A missing mutation anchor is a hard failure: a drifted anchor
would silently turn the gate off.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET = Path("modules/loop/command_sanitize.py")
PATHS_TARGET = Path("core/paths.py")
SECRETS_TARGET = Path("core/secrets.py")
TEST_FILE = "tests/test_hardening_round.py"

_SANDBOX_COPY_DIRS = ("modules", "core", "lazyc2", "cli", "tests", "config")
_SANDBOX_COPY_FILES = ("pyproject.toml", "setup.cfg", "pytest.ini")

MUTATIONS = {
    "quoting_destroyed_again": (
        TARGET,
        ("    return shlex.join(kept), reason", '    return " ".join(kept), reason'),
    ),
    "rw_downgraded_to_write_only": (
        PATHS_TARGET,
        ("            flags = os.O_RDWR", "            flags = os.O_WRONLY"),
    ),
    "sealing_fail_open_again": (
        SECRETS_TARGET,
        (
            '        raise SecurityViolation(f"secret sealing unavailable: {type(exc).__name__}") from exc',
            '        log.warning("secret sealing failed: %s", type(exc).__name__)\n        return text',
        ),
    ),
}


def _make_sandbox() -> Path:
    """Copy the Python sources the hardening tests need into a temp dir.

    Returns:
        Path of the sandbox root (caller removes it).
    """
    sandbox = Path(tempfile.mkdtemp(prefix="lazyown-mutation-"))
    for name in _SANDBOX_COPY_DIRS:
        shutil.copytree(
            BASE_DIR / name,
            sandbox / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
    for name in _SANDBOX_COPY_FILES:
        source = BASE_DIR / name
        if source.exists():
            shutil.copy2(source, sandbox / name)
    return sandbox


def _run_tests(root: Path) -> bool:
    """Return True when the hardening-round tests pass inside ``root``.

    Args:
        root: Sandbox directory used as the pytest working directory.

    Returns:
        True when the suite is green.

    Raises:
        subprocess.TimeoutExpired: If the suite exceeds its budget.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider"],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=str(root),
    )
    return result.returncode == 0


def main() -> int:
    """Run every mutant against the sandbox and return the exit code.

    Returns:
        0 when every mutant is killed, 1 otherwise (including when an
        anchor drifted and the mutation could not be applied).
    """
    sandbox = _make_sandbox()
    try:
        if not _run_tests(sandbox):
            print("FAIL: baseline tests do not pass in the sandbox.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        drifted = 0
        for name, (relative, (old, new)) in MUTATIONS.items():
            path = sandbox / relative
            original = path.read_text(encoding="utf-8")
            mutated = original.replace(old, new, 1)
            if mutated == original:
                print(f"FAIL: {name} — mutation anchor not found in {relative}; fix the anchor.")
                drifted += 1
                continue
            path.write_text(mutated, encoding="utf-8")
            try:
                if _run_tests(sandbox):
                    print(f"SURVIVED: {name}")
                    survived += 1
                else:
                    print(f"KILLED: {name}")
                    killed += 1
            finally:
                path.write_text(original, encoding="utf-8")

        print(f"\n{killed} killed, {survived} survived, {drifted} drifted")
        return 0 if (survived == 0 and drifted == 0) else 1
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
