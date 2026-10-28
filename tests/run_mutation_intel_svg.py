"""Mutation runner for the intel relations-svg contract.

Each mutant breaks one guarantee of ``modules/intel_fusion.relations_svg``:
the size cap, XML escaping or output determinism. The scoped suite must
fail for every mutant; a survivor means the svg tests are too weak.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "cap_ignored": {
        "file": "modules/intel_fusion.py",
        "description": "Selection ignores the node cap and returns everything",
        "old": '    ranked = sorted(nodes, key=_svg_rank)\n    return [str(n["id"]) for n in ranked[:cap]]',
        "new": '    ranked = sorted(nodes, key=_svg_rank)\n    return [str(n["id"]) for n in ranked]',
        "expected": "test_svg_selection_bounded_and_deterministic must fail",
    },
    "escape_skipped": {
        "file": "modules/intel_fusion.py",
        "description": "Untrusted labels render raw into the svg markup",
        "old": '    return escape(str(value or ""), {"\'": "&apos;", \'"\': "&quot;"})',
        "new": '    return str(value or "")',
        "expected": "test_relations_svg_escapes_untrusted_text must fail",
    },
    "determinism_broken": {
        "file": "modules/intel_fusion.py",
        "description": "Selection order follows a scrambled key so output wavers",
        "old": '    return (\n        0 if kind == "c2" else 1,\n        -int(node.get("heat_rank", 0) or 0),\n        -float(node.get("degree", 0) or 0),\n        str(node.get("id", "")),\n    )',
        "new": '    return (\n        0 if kind == "c2" else 1,\n        -int(node.get("heat_rank", 0) or 0),\n        -float(node.get("degree", 0) or 0),\n        \n    )',
        "expected": "test_svg_selection_bounded_and_deterministic must fail",
    },
    "hub_not_pinned": {
        "file": "modules/intel_fusion.py",
        "description": "The c2 hub no longer sits at the canvas centre",
        "old": '    if "c2" in ids:\n        positions["c2"] = (cx, cy)',
        "new": "    if False:\n        positions[\"c2\"] = (cx, cy)",
        "expected": "test_relations_svg_renders_nodes_edges_and_manifest must fail",
    },
}

TEST_TARGETS = ["tests/test_intel_fusion.py"]


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
    print("Mutation Testing - Intel Relations SVG Contract")
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
