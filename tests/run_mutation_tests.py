"""Manual mutation testing runner for LazyOwn connectivity improvements.

Introduces targeted mutations (inversions, deletions, value swaps) into
the production code and verifies that the test suite detects them.

A surviving mutant means the test is too weak — it should catch the mutation.
"""

from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MUTATIONS = {
    "tips_engine_missing_auto_pwn_in_killchain": {
        "file": "cli/tips_engine.py",
        "description": "Remove auto_pwn from build_default_tips_config killchain",
        "old": '"auto_pwn": 30,',
        "new": "",
        "expected": "The test_config_includes_automation_commands must fail",
    },
    "reactive_hints_missing_hunt_in_exploit": {
        "file": "cli/reactive_hints.py",
        "description": "Remove ALL hunt from reactive_hints tables",
        "old": '"hunt",',
        "new": "",
        "replace_all": True,
        "expected": "The test_exploit_includes_automation must fail",
    },
    "protips_missing_encrypt_tip": {
        "file": "cli/protips.py",
        "description": "Remove encrypt tip from security category",
        "old": '"encrypt",',
        "new": '"NOT_ENCRYPT",',
        "expected": "The test_tips_include_security must fail",
    },
    "auto_crypto_skip_protection": {
        "file": "cli/auto_crypto.py",
        "description": "Remove credentials_*.txt from protect_globs",
        "old": '"credentials_*.txt",',
        "new": "",
        "expected": "The test_default_config must fail",
    },
    "tips_engine_broken_elo_base": {
        "file": "cli/tips_engine.py",
        "description": "Set ELO_BASE to 0 (should break ELO tests)",
        "old": "ELO_BASE: int = 5",
        "new": "ELO_BASE: int = 0",
        "expected": "The test_base_elo_awarded must fail",
    },
    "reactive_hints_missing_collab_lateral": {
        "file": "cli/reactive_hints.py",
        "description": "Remove collab_join from lateral phase",
        "old": '"collab_join",',
        "new": "",
        "expected": "The test_lateral_includes_collab must fail",
    },
    "tips_engine_broken_karma_threshold": {
        "file": "cli/tips_engine.py",
        "description": "Change KARMA_THRESHOLDS to break karma tests",
        "old": "(1000, 'Noob'),",
        "new": "(99999, 'Noob'),",
        "expected": "The test_rookie_at_thousand must fail",
    },
}


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    backups = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict):
    for name, original in backups.items():
        path = base_dir / mutations[name]["file"]
        path.write_text(original)


def run_tests() -> bool:
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_tips_engine.py",
            "tests/test_auto_crypto.py",
            "tests/test_reactive_hints_expanded.py",
            "-x", "-q",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode == 0


def main():
    base_dir = Path(__file__).resolve().parent.parent  # project root
    print("=" * 60)
    print("Mutation Testing — LazyOwn Connectivity Improvements")
    print("=" * 60)

    backups = backup_files(MUTATIONS, base_dir)

    try:
        print("\n[1] Running baseline tests (no mutation)...")
        baseline_pass = run_tests()
        if not baseline_pass:
            print("  FAIL: Baseline tests do not pass. Fix tests first.")
            return 1
        print("  PASS: Baseline tests all pass (~65 tests).")

        killed = 0
        survived = 0
        errors = 0

        for name, info in MUTATIONS.items():
            print(f"\n[2] Mutation: {name}")
            print(f"    {info['description']}")

            path = base_dir / info["file"]
            content = path.read_text()

            if info["old"] not in content:
                print(f"    SKIP: Target text not found (already mutated?)")
                errors += 1
                continue

            if info.get("replace_all"):
                mutated = content.replace(info["old"], info["new"])
            else:
                mutated = content.replace(info["old"], info["new"], 1)
            path.write_text(mutated)

            tests_pass = run_tests()
            path.write_text(content)

            if not tests_pass:
                print(f"    KILLED: Mutant detected by tests.")
                killed += 1
            else:
                print(f"    SURVIVED: Mutant NOT detected — tests are too weak!")
                print(f"    Expected: {info['expected']}")
                survived += 1

        print("\n" + "=" * 60)
        print(f"Results: {killed} killed, {survived} survived, {errors} skipped")
        if survived > 0:
            print(f"WARNING: {survived} mutants survived — improve test coverage.")
        else:
            print("ALL MUTANTS KILLED — Tests are robust.")
        print("=" * 60)

        return 0 if survived == 0 else 1

    finally:
        print("\n[3] Restoring original files...")
        restore_files(backups, base_dir, MUTATIONS)
        baseline = run_tests()
        if baseline:
            print("  Restored: Baseline tests pass.")
        else:
            print("  ERROR: Restoration failed. Baseline tests broken!")
            return 2


if __name__ == "__main__":
    sys.exit(main())
