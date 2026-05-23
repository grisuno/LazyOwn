#!/usr/bin/env python3
"""Patch APT playbooks: replace placeholder atomic_ids with real technique_ids.

This ensures do_atomic_gen can find real Atomic Red Team tests via the
MITRE technique ID fallback.
"""

import glob

import yaml

for path in sorted(glob.glob("playbooks/apt_*.yaml")):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    changed = False
    for phase in data.get("phases", []):
        technique_id = phase.get("technique_id", "")
        for test in phase.get("atomic_tests", []):
            old = test.get("atomic_id", "")
            # If it doesn't look like a real MITRE ID (Txxxx) and it's a placeholder UUID,
            # replace it with the technique_id so do_atomic_gen can fallback
            if old and not old.upper().startswith("T"):
                test["atomic_id"] = technique_id
                changed = True

    if changed:
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print(f"[+] Patched {path}")
    else:
        print(f"[ ] {path} already clean")
