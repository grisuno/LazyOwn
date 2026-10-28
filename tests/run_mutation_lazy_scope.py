"""Mutation runner for the lab-only default scope contract.

Each mutant breaks one guarantee of ``modules/lazy_scope``: the lab
classification of private space, the deny of public literals, the
all-answers-must-be-lab rule for resolved hostnames or the operator
allowlist escape hatch. The scoped suite must fail for every mutant; a
survivor means the scope tests are too weak.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "private_is_lab_disabled": {
        "file": "modules/lazy_scope.py",
        "description": "RFC1918 space no longer classifies as lab",
        "old": "    return (\n        parsed.is_loopback\n        or parsed.is_private\n        or parsed.is_link_local\n    )",
        "new": "    return (\n        parsed.is_loopback\n        or parsed.is_link_local\n    )",
        "expected": "test_loopback_and_rfc1918_are_lab must fail",
    },
    "public_literal_allowed": {
        "file": "modules/lazy_scope.py",
        "description": "Public IP literals slip through the literal branch",
        "old": '        return ScopeVerdict(False, "public-ip", f"{text} is not a lab address")',
        "new": '        return ScopeVerdict(True, "", f"{text} is not a lab address")',
        "expected": "test_public_ip_literal_denied and test_one_public_host_blocks_command must fail",
    },
    "mixed_answers_allowed": {
        "file": "modules/lazy_scope.py",
        "description": "One lab answer is enough even when others are public",
        "old": "    public = [addr for addr in addresses if not is_lab_address(addr)]\n    if public:",
        "new": "    public = []\n    if False:",
        "expected": "test_mixed_answers_denied must fail",
    },
    "unresolved_allowed": {
        "file": "modules/lazy_scope.py",
        "description": "Unresolvable hostnames are waved through",
        "old": '        return ScopeVerdict(False, "unresolved", f"{text} does not resolve")',
        "new": '        return ScopeVerdict(True, "", f"{text} does not resolve")',
        "expected": "test_unresolved_denied and test_allowlist_entry_allowed must fail",
    },
}

TEST_TARGETS = ["tests/test_lazy_scope.py"]


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
    print("Mutation Testing - Lab-Only Default Scope Contract")
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
