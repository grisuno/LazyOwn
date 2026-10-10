"""Manual mutation runner for the LAZY port contracts.

Introduces targeted mutations into the integrated modules and
verifies the scoped BDD suite detects each one.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "intercept_allow_bypass": {
        "file": "modules/intercept.py",
        "description": "Force deny verdicts to allow so deny rules never fire",
        "old": "                    if rule.action == InterceptAction.DENY.value:\n                        return InterceptVerdict(\n                            action=\"deny\",",
        "new": "                    if rule.action == InterceptAction.DENY.value:\n                        return InterceptVerdict(\n                            action=\"allow\",",
        "expected": "test_c01_deny_rule_and_expiry must fail",
    },
    "evidence_hash_skip": {
        "file": "modules/evidence.py",
        "description": "Skip integrity verification on read",
        "old": "        if hash_bytes(data) != target.stem:",
        "new": "        if False and hash_bytes(data) != target.stem:",
        "expected": "evidence integrity tests must fail",
    },
    "finding_no_auto_fix": {
        "file": "modules/finding_lifecycle.py",
        "description": "Resolve fixed retests to ignored so status never flips",
        "old": "    if normalized == \"fixed\":\n        set_status(db, target_id, \"fixed\")",
        "new": "    if normalized == \"fixed\":\n        set_status(db, target_id, \"ignored\")",
        "expected": "test_c06_finding_lifecycle_on_campaign_db must fail",
    },
    "pool_no_failover": {
        "file": "modules/llm_pool.py",
        "description": "Break failover so the first failure raises immediately",
        "old": "                errors.append(f\"{member.name}: {exc}\")",
        "new": "                raise PoolExhausted(str(exc))",
        "expected": "test_c07_pool_failover_and_exhaustion must fail",
    },
    "engage_gate_deny_disabled": {
        "file": "skills/autonomous_daemon.py",
        "description": "Disable the engage safety gate so denied commands execute",
        "old": "                if _verdict is not None and _verdict.action == \"deny\":",
        "new": "                if _verdict is not None and _verdict.action == \"never\":",
        "expected": "test_denied_command_never_executes must fail",
    },
}

TEST_TARGETS = [
    "tests/test_safety_gates.py",
    "tests/test_autonomous_ops.py",
    "tests/test_engage_gates.py",
    "tests/test_daemon_loop.py",
]


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    """Snapshot original file contents."""
    backups: dict[str, str] = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    """Restore original file contents."""
    for name, original in backups.items():
        path = base_dir / mutations[name]["file"]
        path.write_text(original)


def run_tests() -> bool:
    """Run the scoped BDD targets and return True on success."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_TARGETS, "-x", "-q"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.returncode == 0


def main() -> int:
    """Execute baseline then each mutation and report kills."""
    base_dir = Path(__file__).resolve().parent.parent
    print("=" * 62)
    print("Mutation Testing - Autonomous Operations Contracts")
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
            content = path.read_text()
            if info["old"] not in content:
                print("    SKIP: target text not found")
                errors += 1
                continue
            path.write_text(content.replace(info["old"], info["new"], 1))
            tests_pass = run_tests()
            path.write_text(content)
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
