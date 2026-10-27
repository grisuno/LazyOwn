"""Mutation runner for the beacon dispatch sink contract.

Each mutant removes one surface guarantee: the foothold gate, the C2
target gate or the clipboard opt-in. The scoped suite must fail.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "shell_gate_disabled": {
        "file": "modules/sinks/beacon_dispatch.py",
        "description": "Stage dispatch files for every event",
        "old": "    if not event.shell:",
        "new": "    if False:",
        "expected": "test_beacon_dispatch_sink_ignores_non_foothold must fail",
    },
    "lhost_gate_disabled": {
        "file": "modules/sinks/beacon_dispatch.py",
        "description": "Dispatch beacons with no configured C2 target",
        "old": "    if not lhost:",
        "new": "    if False:",
        "expected": "test_beacon_dispatch_sink_requires_c2_target must fail",
    },
    "clipboard_gate_disabled": {
        "file": "modules/sinks/beacon_dispatch.py",
        "description": "Copy the catch-back command without operator opt-in",
        "old": '    if payload.get("loop_auto_beacon"):',
        "new": "    if True:",
        "expected": "test_beacon_dispatch_sink_stages_foothold_command must fail",
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
        (base_dir / mutations[name]["file"]).write_text(original, encoding="utf-8")


def run_scoped_tests(base_dir: Path) -> tuple[bool, str]:
    """Run the scoped suite for the mutated file.

    Args:
        base_dir: Repository root.

    Returns:
        Tuple of (passed, combined output).
    """
    cmd = [sys.executable, "-m", "pytest", *TEST_TARGETS, "-q", "--no-header", "-p", "no:cacheprovider"]
    proc = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True, timeout=600, check=False)
    return proc.returncode == 0, (proc.stdout + proc.stderr)


def apply_mutation(info: dict, base_dir: Path) -> bool:
    """Apply one exact-string mutation.

    Args:
        info: Mutation entry with file/old/new.
        base_dir: Repository root.

    Returns:
        True when the old string was found and replaced.
    """
    path = base_dir / info["file"]
    source = path.read_text(encoding="utf-8")
    if info["old"] not in source:
        return False
    path.write_text(source.replace(info["old"], info["new"], 1), encoding="utf-8")
    return True


def main() -> int:
    """Run every mutant and report survivors.

    Returns:
        Process exit code; 1 when a mutant survives.
    """
    base_dir = Path(__file__).resolve().parent.parent
    backups = backup_files(MUTATIONS, base_dir)
    survivors: list[str] = []
    try:
        for name, info in MUTATIONS.items():
            if not apply_mutation(info, base_dir):
                print(f"MUTATION ANCHOR MISSING: {name}")
                survivors.append(name)
                continue
            passed, output = run_scoped_tests(base_dir)
            status = "KILLED" if not passed else "SURVIVED"
            print(f"{status}: {name} ({info['description']})")
            if passed:
                survivors.append(name)
            else:
                tail = output.strip().splitlines()[-1] if output.strip() else ""
                print(f"  evidence: {tail}")
    finally:
        restore_files(backups, base_dir, MUTATIONS)
    if survivors:
        print(f"SURVIVORS: {survivors}")
        return 1
    print("ALL MUTANTS KILLED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
