"""Shared driver for curated mutation runners.

Provides backup/restore, the scoped pytest invocation and the standard
report so each runner file only declares its mutants, the scoped test
targets and nothing else.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    """Snapshot original file contents."""
    backups: dict[str, str] = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text(encoding="utf-8")
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    """Restore original file contents."""
    for name, original in backups.items():
        path = base_dir / mutations[name]["file"]
        path.write_text(original, encoding="utf-8")


def run_tests(test_targets: list[str]) -> bool:
    """Run the scoped suite and return True on success."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *test_targets, "-x", "-q", "-p", "no:cacheprovider"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    return result.returncode == 0


def title(name: str) -> None:
    """Print the runner banner."""
    print("=" * 62)
    print(name)
    print("=" * 62)


def run_all(mutations: dict, test_targets: list[str]) -> int:
    """Execute baseline, every mutant and restore the source."""
    backups = backup_files(mutations, REPO_ROOT)
    try:
        title("Mutation Testing")
        print("\n[1] Baseline (no mutation)...")
        if not run_tests(test_targets):
            print("  FAIL: Baseline tests do not pass.")
            return 1
        print("  PASS: Baseline green.")
        killed = survived = skipped = 0
        for name, info in mutations.items():
            print(f"\n[2] Mutation: {name}")
            print(f"    {info['description']}")
            path = REPO_ROOT / info["file"]
            content = path.read_text(encoding="utf-8")
            if info["old"] not in content:
                print("    SKIP: target text not found")
                skipped += 1
                continue
            path.write_text(content.replace(info["old"], info["new"], 1), encoding="utf-8")
            tests_pass = run_tests(test_targets)
            path.write_text(content, encoding="utf-8")
            if not tests_pass:
                print("    KILLED: mutant detected by the tests.")
                killed += 1
            else:
                print("    SURVIVED: mutant NOT detected.")
                print(f"    Expected: {info['expected']}")
                survived += 1
        print("\n" + "=" * 62)
        print(f"Results: {killed} killed, {survived} survived, {skipped} skipped")
        print("ALL MUTANTS KILLED." if survived == 0 else f"WARNING: {survived} survived.")
        print("=" * 62)
        if survived:
            print("\n[3] Restoring originals...")
            return 1
        return 0
    finally:
        print("\n[3] Restoring originals...")
        restore_files(backups, REPO_ROOT, mutations)
