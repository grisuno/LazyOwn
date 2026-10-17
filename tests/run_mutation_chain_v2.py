"""Mutation runner for the chain v2 contract.

Each mutant removes one execution guarantee: conditions, capture,
retries, error policy or abort behaviour. The scoped suite must fail.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "when_always_true": {
        "file": "modules/chain_registry.py",
        "description": "Ignore the when condition so skipped steps execute",
        "old": '    text = str(expression or "").strip()\n    if not text:\n        return True',
        "new": '    text = str(expression or "").strip()\n    return True\n    if not text:\n        return True',
        "expected": "test_when_evaluator_is_safe_and_expressive must fail",
    },
    "apt_chain_output_hidden": {
        "file": "cli/commands/command_and_control_migrated.py",
        "description": "Hide raw command output from the operator",
        "old": "                if outcome.output:",
        "new": "                if False:",
        "expected": "test_apt_chain_prints_raw_output_and_opens_shell_on_main_thread must fail",
    },
    "verb_offloaded": {
        "file": "modules/chain_runner.py",
        "description": "Send cmd2 verbs through subprocess instead of the live shell",
        "old": "        if self._is_verb(command):",
        "new": "        if False:",
        "expected": "test_runner_routes_known_verb_through_shell must fail",
    },
    "onecmd_bool_printed": {
        "file": "modules/chain_runner.py",
        "description": "Print the boolean onecmd result instead of ignoring it",
        "old": "        if result is None or isinstance(result, bool):\n            return \"\"",
        "new": "        if result is None:\n            return \"\"",
        "expected": "test_runner_keeps_verbs_on_calling_thread must fail",
    },
    "nonzero_exit_ignored": {
        "file": "modules/chain_runner.py",
        "description": "Treat a non-zero subprocess exit as success",
        "old": "        if completed.returncode != 0:",
        "new": "        if False:",
        "expected": "test_runner_fails_on_nonzero_exit must fail",
    },
    "capture_not_stored": {
        "file": "modules/chain_runner.py",
        "description": "Do not persist captured output for later steps",
        "old": '                variables[step.capture] = outcome.captured',
        "new": "                pass",
        "expected": "test_runner_captures_output_for_later_steps must fail",
    },
    "retries_ignored": {
        "file": "modules/chain_runner.py",
        "description": "Execute only one attempt regardless of retries",
        "old": "        attempts_allowed = max(0, min(_MAX_RETRIES, int(step.retries or 0))) + 1",
        "new": "        attempts_allowed = 1",
        "expected": "test_runner_retries_then_succeeds must fail",
    },
    "continue_policy_ignored": {
        "file": "modules/chain_runner.py",
        "description": "Abort on every failure even when continue_on_error is true",
        "old": "            if not outcome.ok and not step.continue_on_error:",
        "new": "            if not outcome.ok:",
        "expected": "test_runner_continues_when_policy_allows must fail",
    },
    "abort_ignored": {
        "file": "modules/chain_runner.py",
        "description": "Keep running after a hard failure",
        "old": "                result.aborted = True",
        "new": "                result.aborted = False",
        "expected": "test_runner_aborts_unless_continue_on_error must fail",
    },
}

TEST_TARGETS = ["tests/test_chain_runner.py", "tests/test_chain_registry.py", "tests/test_apt_chain_integration.py"]


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
    print("Mutation Testing - Chain v2 Contract")
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
