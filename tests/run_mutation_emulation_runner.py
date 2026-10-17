"""Mutation runner for the emulation-runner contract.

Each mutant removes one guarantee: manual gating, dry-run safety, error
normalization or the YAML-first command source.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "manual_gate_disabled": {
        "file": "modules/emulation_runner.py",
        "description": "Execute manual Atomic tests without operator opt-in",
        "old": "        if manual and not include_manual:",
        "new": "        if False and manual and not include_manual:",
        "expected": "test_runner_skips_manual_tests_by_default must fail",
    },
    "dry_run_executes": {
        "file": "modules/emulation_runner.py",
        "description": "Execute commands even when dry_run is set",
        "old": "        if dry_run:\n            result.status = \"dry-run\"\n            return result",
        "new": "        if False:\n            result.status = \"dry-run\"\n            return result",
        "expected": "test_runner_dry_run_never_calls_executor must fail",
    },
    "step_error_not_normalized": {
        "file": "modules/emulation_runner.py",
        "description": "Let executor exceptions escape run_steps",
        "old": "                except Exception as exc:\n                    result = EmulationResult(",
        "new": "                except ZeroDivisionError as exc:\n                    result = EmulationResult(",
        "expected": "test_run_steps_handles_dry_run_and_failures must fail",
    },
    "yaml_first_disabled": {
        "file": "modules/autonomous_exploit_engine.py",
        "description": "Skip the YAML command source and use the hardcoded map",
        "old": "            if spec is not None:\n                return [\n                    run\n                    for run, _timeout in _build_commands(",
        "new": "            if False and spec is not None:\n                return [\n                    run\n                    for run, _timeout in _build_commands(",
        "expected": "test_engine_prefers_yaml_command_chain must fail",
    },
    "bridge_drops_manual_flag": {
        "file": "modules/atomic_exploit_bridge.py",
        "description": "Drop include_manual when delegating to the runner",
        "old": "        include_manual=include_manual,",
        "new": "        include_manual=False,",
        "expected": "test_bridge_emulate_delegates_to_runner must fail",
    },
}

TEST_TARGETS = ["tests/test_emulation_runner.py"]


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
    print("Mutation Testing - Emulation Runner Contract")
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
