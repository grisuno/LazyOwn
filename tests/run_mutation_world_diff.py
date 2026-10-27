"""Mutation runner for the lazy world-diff contract.

Each mutant removes one surface guarantee: change-kind detection, change
log dedupe/bounding, ghost lifecycle or the stats cooldown. The scoped
suite must fail.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "enrichment_flagged_as_change": {
        "file": "modules/lazy_world_diff.py",
        "description": "Flag first observation of a product as a change",
        "old": "            if not (was.get(\"product\") or was.get(\"version\")):",
        "new": "            if False:",
        "expected": "test_diff_service_change_requires_prior_identity must fail",
    },
    "dedupe_disabled": {
        "file": "modules/lazy_world_diff.py",
        "description": "Log repeat observations of the same change",
        "old": "        if same or per_host_count.get(ip, 0) + len(fresh) >= HOST_CHANGES_PER_HOST:",
        "new": "        if False:",
        "expected": "test_record_changes_dedupes_repeat must fail",
    },
    "ghost_clear_disabled": {
        "file": "modules/lazy_world_diff.py",
        "description": "Never clear a ghost state",
        "old": "        if record.get(\"state\") == _GHOST:",
        "new": "        if False:",
        "expected": "test_ghost_state_apply_roundtrip must fail",
    },
    "stats_cooldown_disabled": {
        "file": "modules/lazy_world_diff.py",
        "description": "Write a stats snapshot on every call",
        "old": "    if rows and stamp - float(rows[-1].get(\"ts\", 0) or 0) < SNAPSHOT_MIN_INTERVAL:",
        "new": "    if False:",
        "expected": "test_snapshot_engagement_cooldown must fail",
    },
}

TEST_TARGETS = ["tests/test_lazy_world_diff.py"]


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
    print("Mutation Testing - Lazy World Diff Contract")
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
