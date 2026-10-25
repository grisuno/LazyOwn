"""Mutation runner for the orchestrator YAML contract.

Each mutant removes one YAML precedence or profile limit. The scoped
suite must fail for every mutant; a survivor means the contract is weak.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "active_profile_ignores_payload": {
        "file": "modules/orchestrator_config.py",
        "description": "Ignore the payload profile so the default always wins",
        "old": '    selected = str(_section().get("profile", "") or "")',
        "new": '    selected = ""',
        "expected": "test_payload_profile_overrides_yaml must fail",
    },
    "limits_ignore_profile": {
        "file": "modules/orchestrator_config.py",
        "description": "Return fallback limits instead of profile limits",
        "old": '    merged.update(profile_config().get("limits") or {})',
        "new": "    merged.update({})",
        "expected": "test_payload_profile_overrides_yaml must fail",
    },
    "stage_params_empty": {
        "file": "modules/orchestrator_config.py",
        "description": "Drop stage parameters so per-stage throttles vanish",
        "old": '    return dict((stages().get(str(name)) or {}).get("params") or {})',
        "new": "    return {}",
        "expected": "test_stage_params_resolve_and_payload_still_overrides must fail",
    },
    "engine_retest_ignores_profile": {
        "file": "modules/lazy_loop.py",
        "description": "Hardcode the retest limit so the engine ignores YAML",
        "old": '        self.retest_limit = max(0, int(resolved.get("retest_limit", 3) or 0))',
        "new": "        self.retest_limit = 3",
        "expected": "test_engine_uses_profile_limits must fail",
    },
    "runner_rounds_ignore_profile": {
        "file": "modules/lazy_runner.py",
        "description": "Skip profile rounds so unset flags keep the CLI default",
        "old": "    if not config.rounds_set:",
        "new": "    if False:",
        "expected": "test_runner_parses_profile_and_resolves_defaults must fail",
    },
}

TEST_TARGETS = ["tests/test_orchestrator_yaml.py"]


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
    print("Mutation Testing - Orchestrator YAML Contract")
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
