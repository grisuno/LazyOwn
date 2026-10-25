"""Manual mutation testing runner for the LazyAddon creator contract.

Introduces targeted mutations (validation bypasses, security hardening
removals, renderer corruptions) into ``lazyc2/addon_creator.py`` and
``lazyc2/blueprints/addons.py`` and verifies the test suite detects each
one.

A surviving mutant means the tests are too weak to notice the behaviour
change, which violates the addon creator Definition of Done.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "name_whitelist_disabled": {
        "file": "lazyc2/addon_creator.py",
        "description": "Disable the name whitelist check so bad names validate",
        "old": "elif not self.config.name_pattern.fullmatch(name):",
        "new": "elif False:",
        "expected": "test_invalid_name_reports_issue must fail",
    },
    "store_containment_disabled": {
        "file": "lazyc2/addon_creator.py",
        "description": "Drop the realpath containment defence in depth",
        "old": "        if not target.is_relative_to(base):",
        "new": "        if False:",
        "expected": "test_traversal_name_rejected_on_save must fail",
    },
    "existing_path_pattern_disabled": {
        "file": "lazyc2/addon_creator.py",
        "description": "Existing-file lookups accept path separators and traversal",
        "old": "        if not pattern.fullmatch(name):",
        "new": "        if False:",
        "expected": "test_load_still_rejects_traversal_through_existing_path must fail",
    },
    "list_filenames_swapped_for_yaml_names": {
        "file": "lazyc2/addon_creator.py",
        "description": "List links point at the YAML name instead of the file stem",
        "old": '                    "filename": path.stem,',
        "new": '                    "filename": str(data.get("name") or path.stem),',
        "expected": "test_list_page_links_by_filename_for_legacy_names must fail",
    },
    "enabled_forced_false": {
        "file": "lazyc2/addon_creator.py",
        "description": "Renderer always emits enabled: false",
        "old": '"enabled": bool(draft.enabled),',
        "new": '"enabled": False,',
        "expected": "test_rendered_document_is_canonical must fail",
    },
    "placeholder_check_disabled": {
        "file": "lazyc2/addon_creator.py",
        "description": "Unknown command placeholders are silently accepted",
        "old": "            if token in param_names or token in self.config.payload_placeholders:",
        "new": "            if True:",
        "expected": "test_unknown_placeholder_reports_issue must fail",
    },
    "double_brace_check_disabled": {
        "file": "lazyc2/addon_creator.py",
        "description": "Double-brace placeholders are no longer flagged",
        "old": "        for double_match in self.config.double_brace_pattern.findall(text):",
        "new": "        for double_match in []:",
        "expected": "test_nested_brace_placeholder_reports_issue must fail",
    },
    "form_param_rows_truncated": {
        "file": "lazyc2/addon_creator.py",
        "description": "Only the first form param row is parsed",
        "old": '    while f"params-{index}-name" in form:',
        "new": "    while index < 1:",
        "expected": "test_parse_complete_form must fail",
    },
    "save_no_longer_atomic": {
        "file": "lazyc2/addon_creator.py",
        "description": "Write directly to the target, leaving temp files behind",
        "old": "            os.replace(temp_path, target)",
        "new": '            target.write_text(yaml_text, encoding="utf-8")',
        "expected": "test_save_is_atomic_and_leaves_no_temp_files must fail",
    },
    "csrf_gate_removed": {
        "file": "lazyc2/blueprints/addons.py",
        "description": "Mutating routes accept requests without a CSRF token",
        "old": "        if not policy.check_request(session_id, request):",
        "new": "        if False:",
        "expected": "test_post_without_csrf_is_rejected must fail",
    },
}

TEST_TARGETS = ["tests/test_addon_creator.py"]


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    """Store the original content of every mutated file.

    Args:
        mutations: The mutation catalogue.
        base_dir: The repository root.

    Returns:
        A mapping of mutation name to original file content.
    """
    backups: dict[str, str] = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text(encoding="utf-8")
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    """Restore every mutated file to its original content.

    Args:
        backups: Original contents keyed by mutation name.
        base_dir: The repository root.
        mutations: The mutation catalogue.
    """
    for name, original in backups.items():
        path = base_dir / mutations[name]["file"]
        path.write_text(original, encoding="utf-8")


def run_tests() -> bool:
    """Run the contract suite and report whether it passed.

    Returns:
        True when the suite is green.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_TARGETS, "-q"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.returncode == 0


def main() -> int:
    """Execute the mutation gate and restore the tree afterwards.

    Returns:
        0 when every mutant was killed, 1 when any survived.
    """
    base_dir = Path(__file__).resolve().parent.parent
    print("=" * 62)
    print("Mutation Testing - LazyAddon Creator Contract")
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
                print("    SURVIVED: mutant NOT detected - tests too weak!")
                print(f"    Expected: {info['expected']}")
                survived += 1

        print("\n" + "=" * 62)
        print(f"Results: {killed} killed, {survived} survived, {errors} skipped")
        print("ALL MUTANTS KILLED - tests are robust." if survived == 0 else f"WARNING: {survived} mutants survived.")
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
