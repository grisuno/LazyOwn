"""Mutation runner for the consolidated OPSEC scorer contract.

Applies targeted mutations to ``modules/opsec_scorer.py`` and verifies that
``tests/test_opsec_scorer_consolidated.py`` detects each one.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "high_threshold_lowered": {
        "file": "modules/opsec_scorer.py",
        "description": "Lower the high-risk ceiling from 7 to 6",
        "old": "RISK_THRESHOLD_HIGH = 7",
        "new": "RISK_THRESHOLD_HIGH = 6",
        "expected": "test_risk_buckets_respect_thresholds must fail",
    },
    "medium_threshold_lowered": {
        "file": "modules/opsec_scorer.py",
        "description": "Lower the medium-risk ceiling from 4 to 3",
        "old": "RISK_THRESHOLD_MEDIUM = 4",
        "new": "RISK_THRESHOLD_MEDIUM = 3",
        "expected": "test_risk_buckets_respect_thresholds must fail",
    },
    "critical_enum_collapsed": {
        "file": "modules/opsec_scorer.py",
        "description": "Collapse CRITICAL enum value into HIGH",
        "old": "    CRITICAL = 4",
        "new": "    CRITICAL = 3",
        "expected": "test_enum_values must fail",
    },
    "warn_gate_relaxed": {
        "file": "modules/opsec_scorer.py",
        "description": "Downgrade HIGH gate from WARN to ALLOW",
        "old": "            return GateAction.WARN",
        "new": "            return GateAction.ALLOW",
        "expected": "test_gate_mapping must fail",
    },
    "mimikatz_profile_neutered": {
        "file": "modules/opsec_scorer.py",
        "description": "Neuter mimikatz base_noise in the gating profile",
        "old": '"mimikatz": {"base_noise": 10,',
        "new": '"mimikatz": {"base_noise": 1,',
        "expected": "test_risk_profiles_shared_table_intact must fail",
    },
    "risk_level_bucket_off_by_one": {
        "file": "modules/opsec_scorer.py",
        "description": "Drop the +1 so low noise maps to NONE",
        "old": "_risk_bucket(noise) + 1)",
        "new": "_risk_bucket(noise))",
        "expected": "test_risk_level_matches_bucket must fail",
    },
}


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    backups = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    for name, original in backups.items():
        (base_dir / mutations[name]["file"]).write_text(original)


def run_tests() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_opsec_scorer_consolidated.py", "-q"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode == 0


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    backups = backup_files(MUTATIONS, base_dir)

    print("Mutation Testing — consolidated OPSEC scorer contract")
    print("=" * 60)

    if not run_tests():
        print("FAIL: Baseline tests do not pass. Fix tests first.")
        return 1
    print("PASS: Baseline tests all pass.")

    killed = 0
    survived = 0
    skipped = 0

    try:
        for name, info in MUTATIONS.items():
            print(f"\nMutation: {name}")
            print(f"    {info['description']}")
            path = base_dir / info["file"]
            content = path.read_text()

            if info["old"] not in content:
                print("    SKIP: target text not found.")
                skipped += 1
                continue

            path.write_text(content.replace(info["old"], info["new"], 1))

            if run_tests():
                print("    SURVIVED: mutant NOT detected — tests are too weak.")
                print(f"    Expected: {info['expected']}")
                survived += 1
            else:
                print("    KILLED: mutant detected by tests.")
                killed += 1

            path.write_text(content)

        print("\n" + "=" * 60)
        print(f"Results: {killed} killed, {survived} survived, {skipped} skipped")
        print("ALL MUTANTS KILLED — tests are robust." if survived == 0 else
              "WARNING: mutants survived — improve test coverage.")
        print("=" * 60)
        return 0 if survived == 0 else 1
    finally:
        restore_files(backups, base_dir, MUTATIONS)
        if run_tests():
            print("Restored: baseline tests pass.")
        else:
            print("ERROR: restoration failed.")
            return 2


if __name__ == "__main__":
    sys.exit(main())
