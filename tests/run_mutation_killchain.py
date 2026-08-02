"""Manual mutation testing runner for the unified kill-chain contract.

Introduces targeted mutations (value swaps, logic inversions, security
hardening removals) into the production kill-chain, beacon-history and
auto-refresh code and verifies the test suite detects each one.

A surviving mutant means the tests are too weak to notice the behaviour
change, which violates the kill-chain Definition of Done.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "killchain_snapshot_frozen_current_phase": {
        "file": "modules/killchain.py",
        "description": "Freeze snapshot current_phase to recon so it can never reflect reality",
        "old": '"current_phase": current,',
        "new": '"current_phase": "recon",',
        "expected": "test_snapshot_reflects_explicit_phase_and_completed must fail",
    },
    "beacon_history_traversal_reintroduced": {
        "file": "modules/beacon_history.py",
        "description": "Remove client-id sanitisation so traversal is possible again",
        "old": 'safe_id = "".join(c for c in str(client_id) if c.isalnum() or c in "-_")',
        "new": "safe_id = str(client_id)",
        "expected": "test_records_path_is_bounded_inside_sessions must fail",
    },
    "beacon_history_append_rejected": {
        "file": "modules/beacon_history.py",
        "description": "Make append_record always report failure",
        "old": "        return True\n    except Exception as exc:",
        "new": "        return False\n    except Exception as exc:",
        "expected": "test_append_then_read_round_trips must fail",
    },
    "auto_refresh_periodic_cadence_broken": {
        "file": "cli/tips_engine.py",
        "description": "Disable the periodic cadence branch of the auto-refresh logic",
        "old": "(every > 0 and self._killchain_counter % every == 0) or (",
        "new": "(False and self._killchain_counter % every == 0) or (",
        "expected": "The periodic cadence tests must fail",
    },
}


TEST_TARGETS = [
    "tests/test_killchain_snapshot.py",
    "tests/test_beacon_history.py",
    "tests/test_killchain_auto_refresh.py",
]


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    backups: dict[str, str] = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    for name, original in backups.items():
        path = base_dir / mutations[name]["file"]
        path.write_text(original)


def run_tests() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_TARGETS, "-x", "-q"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.returncode == 0


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    print("=" * 62)
    print("Mutation Testing — Unified Kill-Chain / Beacon History Contract")
    print("=" * 62)

    backups = backup_files(MUTATIONS, base_dir)

    try:
        print("\n[1] Baseline (no mutation)...")
        if not run_tests():
            print("  FAIL: Baseline tests do not pass. Fix tests first.")
            return 1
        print("  PASS: Baseline green.")

        killed = survived = errors = 0
        for name, info in MUTATIONS.items():
            print(f"\n[2] Mutation: {name}")
            print(f"    {info['description']}")
            path = base_dir / info["file"]
            content = path.read_text()
            if info["old"] not in content:
                print("    SKIP: target text not found")
                errors += 1
                continue
            mutant = info["new"] if isinstance(info["new"], str) else info["new"]
            path.write_text(content.replace(info["old"], mutant, 1))
            tests_pass = run_tests()
            path.write_text(content)
            if not tests_pass:
                print("    KILLED: mutant detected by the tests.")
                killed += 1
            else:
                print("    SURVIVED: mutant NOT detected — tests too weak!")
                print(f"    Expected: {info['expected']}")
                survived += 1

        print("\n" + "=" * 62)
        print(f"Results: {killed} killed, {survived} survived, {errors} skipped")
        print("ALL MUTANTS KILLED — tests are robust." if survived == 0
              else f"WARNING: {survived} mutants survived.")
        print("=" * 62)
        return 0 if survived == 0 else 1

    finally:
        print("\n[3] Restoring originals...")
        restore_files(backups, base_dir, MUTATIONS)
        if run_tests():
            print("  Restored: baseline green.")
        else:
            print("  ERROR: restoration failed.")
            return 2


if __name__ == "__main__":
    sys.exit(main())