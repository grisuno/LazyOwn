"""Mutation runner for the lazyaddon update contract.

Each mutant removes one safety guarantee: the opt-in flag, the path
confinement, the repository-root guard or the dirty-tree check.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "update_flag_ignored": {
        "file": "modules/addon_updater.py",
        "description": "Update addons even when update is false",
        "old": '    if not entry["update"]:',
        "new": "    if False:",
        "expected": "test_update_disabled_is_skipped must fail",
    },
    "traversal_allowed": {
        "file": "modules/addon_updater.py",
        "description": "Accept install paths containing ..",
        "old": '    if ".." in candidate.parts:\n        return None, "install_path traversal"',
        "new": '    if False:\n        return None, "install_path traversal"',
        "expected": "test_path_traversal_is_rejected must fail",
    },
    "repo_root_allowed": {
        "file": "modules/addon_updater.py",
        "description": "Allow pulling the LazyOwn repository itself",
        "old": '    if resolved == root.resolve():\n        return None, "install_path is the LazyOwn repository"',
        "new": '    if False:\n        return None, "install_path is the LazyOwn repository"',
        "expected": "test_repository_root_is_rejected must fail",
    },
    "dirty_tree_ignored": {
        "file": "modules/addon_updater.py",
        "description": "Pull over local operator edits",
        "old": "    if status_result.stdout.strip():",
        "new": "    if False:",
        "expected": "test_dirty_worktree_is_skipped must fail",
    },
}

TEST_TARGETS = ["tests/test_addon_updater.py"]


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


def run_tests() -> bool:
    """Run the scoped suite and return True on success."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_TARGETS, "-x", "-q", "-p", "no:cacheprovider"],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        timeout=600,
    )
    return result.returncode == 0


def main() -> int:
    """Execute baseline, every mutant and restore the source."""
    base_dir = Path(__file__).resolve().parent.parent
    print("=" * 62)
    print("Mutation Testing - Lazyaddon Update Contract")
    print("=" * 62)
    backups = backup_files(MUTATIONS, base_dir)
    try:
        print("\n[1] Baseline (no mutation)...")
        if not run_tests():
            print("  FAIL: Baseline tests do not pass.")
            return 1
        print("  PASS: Baseline green.")
        killed = survived = errors = 0
        for name, info in MUTATIONS.items():
            print(f"\n[2] Mutation: {name}")
            print(f"    {info['description']}")
            path = base_dir / info["file"]
            content = path.read_text(encoding="utf-8")
            if info["old"] not in content:
                print("    SKIP: target text not found")
                errors += 1
                continue
            path.write_text(content.replace(info["old"], info["new"], 1), encoding="utf-8")
            tests_pass = run_tests()
            path.write_text(content, encoding="utf-8")
            if not tests_pass:
                print("    KILLED: mutant detected by the tests.")
                killed += 1
            else:
                print("    SURVIVED: mutant NOT detected.")
                print(f"    Expected: {info['expected']}")
                survived += 1
        print("\n" + "=" * 62)
        print(f"Results: {killed} killed, {survived} survived, {errors} skipped")
        print("ALL MUTANTS KILLED." if survived == 0 else f"WARNING: {survived} survived.")
        print("=" * 62)
        return 0 if survived == 0 else 1
    finally:
        print("\n[3] Restoring originals...")
        restore_files(backups, base_dir, MUTATIONS)


if __name__ == "__main__":
    sys.exit(main())
