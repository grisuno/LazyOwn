#!/usr/bin/env python3
"""Update APT playbooks with real Atomic Red Team test IDs.

Scans the Atomic Red Team repository (already cloned by the user) and maps
MITRE technique IDs to actual ``auto_generated_guid`` values, then patches
``playbooks/apt_*.yaml`` in place.

Usage::

    python3 scripts/update_apt_atomic_ids.py [path/to/atomic-red-team/atomics]

If no path is given it defaults to ``external/.exploit/atomic-red-team/atomics``.
"""

import glob
import os
import sys

import yaml


def build_technique_index(atomics_path: str) -> dict[str, list[dict]]:
    """Map technique_id -> list of {atomic_id, name, description}."""
    index: dict[str, list[dict]] = {}
    pattern = os.path.join(atomics_path, "**", "*.yaml")
    for file in glob.glob(pattern, recursive=True):
        try:
            with open(file, "r") as f:
                data = yaml.safe_load(f)
            if not data or "atomic_tests" not in data:
                continue
            technique_id = data.get("attack_technique", "")
            if not technique_id:
                continue
            for test in data["atomic_tests"]:
                entry = {
                    "atomic_id": test.get("auto_generated_guid", ""),
                    "name": test.get("name", ""),
                }
                index.setdefault(technique_id, []).append(entry)
        except Exception:
            continue
    return index


def update_playbooks(index: dict[str, list[dict]], playbook_dir: str = "playbooks") -> None:
    pattern = os.path.join(playbook_dir, "apt_*.yaml")
    updated = 0
    for path in glob.glob(pattern):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        changed = False
        for phase in data.get("phases", []):
            technique_id = phase.get("technique_id", "")
            candidates = index.get(technique_id, [])
            existing_ids = {t["atomic_id"] for t in phase.get("atomic_tests", [])}
            for cand in candidates:
                if cand["atomic_id"] and cand["atomic_id"] not in existing_ids:
                    phase.setdefault("atomic_tests", []).append({
                        "atomic_id": cand["atomic_id"],
                        "name": cand["name"],
                        "manual": True,
                    })
                    changed = True
        if changed:
            with open(path, "w") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            print(f"[+] Updated {path}")
            updated += 1
        else:
            print(f"[ ] No new mappings for {path}")
    print(f"\nDone. {updated} playbook(s) enriched.")


if __name__ == "__main__":
    atomics_path = sys.argv[1] if len(sys.argv) > 1 else "external/.exploit/atomic-red-team/atomics"
    if not os.path.exists(atomics_path):
        print(f"Error: Atomic Red Team path not found: {atomics_path}")
        print("Clone it first: git clone https://github.com/redcanaryco/atomic-red-team.git")
        sys.exit(1)
    print(f"[*] Scanning ART in {atomics_path}...")
    index = build_technique_index(atomics_path)
    print(f"[*] Indexed {len(index)} technique(s)")
    update_playbooks(index)
