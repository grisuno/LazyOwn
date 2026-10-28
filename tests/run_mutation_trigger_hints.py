"""Mutation runner for the cve_hot hint fingerprint contract.

Each mutant breaks one guarantee of ``modules/loop_triggers`` hint
fingerprinting: the same-evidence dedup, the version sensitivity of the
signature or the prune of expired signatures. The scoped suite must
fail for every mutant; a survivor means the trigger-hint tests are too
weak.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "dedup_skipped": {
        "file": "modules/loop_triggers.py",
        "description": "Every round queues the same verification hint again",
        "old": "                            if fingerprint in fingerprints:\n                                continue",
        "new": "                            if False:\n                                continue",
        "expected": "test_cve_hot_hint_proposed_once_per_signature must fail",
    },
    "version_ignored": {
        "file": "modules/loop_triggers.py",
        "description": "Stale banners keep deduping after the version bumps",
        "old": '            str(row.get("version", "") or ""),',
        "new": '            "",',
        "expected": "test_changed_banner_refires_the_hint must fail",
    },
    "prune_disabled": {
        "file": "modules/loop_triggers.py",
        "description": "Expired signatures never leave the fingerprint store",
        "old": "    fresh: dict[str, float] = {}\n    for key, seen in (store or {}).items():\n        try:\n            if now - float(seen) < float(ttl):\n                fresh[str(key)] = float(seen)",
        "new": "    fresh: dict[str, float] = {}\n    for key, seen in (store or {}).items():\n        try:\n            fresh[str(key)] = float(seen)",
        "expected": "test_hint_ttl_expires_and_refires and test_prune_drops_expired_fingerprints must fail",
    },
    "store_persist_skipped": {
        "file": "modules/loop_triggers.py",
        "description": "Fingerprints never reach disk so dedup dies with the round",
        "old": "                    if store_changed:\n                        try:",
        "new": "                    if False:\n                        try:",
        "expected": "test_hint_store_written_under_loop_stores must fail",
    },
}

TEST_TARGETS = ["tests/test_loop_trigger_hints.py"]


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
        timeout=900,
    )
    return result.returncode == 0


def main() -> int:
    """Execute baseline, every mutant and restore the source."""
    base_dir = Path(__file__).resolve().parent.parent
    print("=" * 62)
    print("Mutation Testing - CVE Hint Fingerprint Contract")
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
