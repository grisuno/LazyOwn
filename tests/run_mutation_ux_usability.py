"""Mutation testing runner for the UX usability contracts.

Introduces targeted mutations into the production code that revert the fixes
this work shipped. If a mutant survives, the test suite failed to detect the
regression — meaning the usability gap would silently reappear.

Mutations:
    1. off level no longer suppresses surfaces        — killed by test_tips_engine
    2. minimal level runs the full surface set        — killed by test_tips_engine
    3. contextual_help drops canonical phase labels   — killed by test_phase_labels
    4. canonical command count drifts by one          — killed by test_sync_doc_stats
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEST_FILES = (
    "tests/test_tips_engine.py",
    "tests/test_phase_labels.py",
    "tests/test_sync_doc_stats.py",
)

MUTATIONS = {
    "off_does_not_suppress": {
        "file": "cli/tips_engine.py",
        "description": "Disable the off-level early return (revert noise reduction).",
        "old": "if self.config.hints_level == HINTS_LEVEL_OFF:",
        "new": "if self.config.hints_level == \"__never__\":",
        "expected": "test_off_suppresses_all_surfaces MUST fail",
    },
    "minimal_runs_everything": {
        "file": "cli/tips_engine.py",
        "description": "Drop the minimal branch so minimal renders all surfaces.",
        "old": "if self.config.hints_level == HINTS_LEVEL_MINIMAL:",
        "new": "if self.config.hints_level == \"__never__\":",
        "expected": "test_minimal_runs_autosuggest_only MUST fail",
    },
    "contextual_help_local_phase_labels": {
        "file": "cli/contextual_help.py",
        "description": "Reintroduce a divergent local PHASE_LABELS mapping.",
        "old": "from cli.phase_labels import PHASE_LABELS",
        "new": "PHASE_LABELS: dict = {}",
        "expected": "test_contextual_help_reuses_canonical_labels MUST fail",
    },
    "canonical_command_count_off_by_one": {
        "file": "scripts/sync_doc_stats.py",
        "description": "Make the canonical command count drift by one.",
        "old": 'return int(document["totals"]["unique_commands"])',
        "new": 'return int(document["totals"]["unique_commands"]) + 1',
        "expected": "test_canonical_command_count_reads_index MUST fail",
    },
}


def _run_tests() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_FILES, "-x", "-q"],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=str(BASE_DIR),
    )
    return result.returncode == 0


def _backups(mutations: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for name, info in mutations.items():
        path = BASE_DIR / info["file"]
        result[name] = path.read_text(encoding="utf-8")
    return result


def _restore(backups: dict[str, str], mutations: dict) -> None:
    for name, original in backups.items():
        (BASE_DIR / mutations[name]["file"]).write_text(original, encoding="utf-8")


def main() -> int:
    backups = _backups(MUTATIONS)
    try:
        print("Mutation Testing — UX usability contracts")

        if not _run_tests():
            print("FAIL: baseline tests do not pass; fix tests first.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        for name, info in MUTATIONS.items():
            path = BASE_DIR / info["file"]
            content = path.read_text(encoding="utf-8")
            if info["old"] not in content:
                print(f"SKIP {name}: target text not found.")
                continue
            path.write_text(content.replace(info["old"], info["new"], 1), encoding="utf-8")
            mutant_pass = _run_tests()
            path.write_text(content, encoding="utf-8")
            if mutant_pass:
                survived += 1
                print(f"SURVIVED {name}: {info['expected']}")
            else:
                killed += 1
                print(f"KILLED   {name}")

        print(f"Results: {killed} killed, {survived} survived")
        if survived:
            print("WARNING: mutants survived - improve test coverage.")
        return 0 if survived == 0 else 1
    finally:
        _restore(backups, MUTATIONS)
        if _run_tests():
            print("Restored: baseline tests pass.")
        else:
            print("ERROR: restoration failed.")
            return 2


if __name__ == "__main__":
    sys.exit(main())
