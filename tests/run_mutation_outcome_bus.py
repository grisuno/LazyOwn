"""Mutation runner for the outcome-bus contract.

Each mutant removes one fan-out guarantee: dedupe, payload toggles, C2
notes or the bridge result mapping. The scoped suite must fail.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "dedupe_disabled": {
        "file": "modules/outcome_bus.py",
        "description": "Process the same event twice",
        "old": "            if cached is not None:",
        "new": "            if False:",
        "expected": "test_bus_fans_out_dedupes_and_audits must fail",
    },
    "toggles_ignored": {
        "file": "modules/outcome_bus.py",
        "description": "Ignore payload sink toggles",
        "old": '        return [name for name in names if bool(toggles.get(name, True))]',
        "new": "        return names",
        "expected": "test_bus_respects_sink_toggles must fail",
    },
    "c2_note_disabled": {
        "file": "modules/sinks/c2_surfaces.py",
        "description": "Skip operator notes for shell outcomes",
        "old": "        changed = append_note(line, sessions_dir=sessions) or changed",
        "new": "        changed = changed",
        "expected": "test_c2_surface_sink_writes_banner_cve_and_note must fail",
    },
    "bridge_cve_mapping_lost": {
        "file": "modules/atomic_exploit_bridge.py",
        "description": "Drop the CVE surface status from the bridge result",
        "old": '        "cves": c2 and bool(spec.cve),',
        "new": '        "cves": False,',
        "expected": "test_record_outcome_builds_one_exploit_event must fail",
    },
}

TEST_TARGETS = ["tests/test_outcome_bus.py"]


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
    print("Mutation Testing - Outcome Bus Contract")
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
