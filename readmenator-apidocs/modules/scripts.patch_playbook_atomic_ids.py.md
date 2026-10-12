# `scripts.patch_playbook_atomic_ids`

> Source: [scripts/patch_playbook_atomic_ids.py:1](../../scripts/patch_playbook_atomic_ids.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Patch APT playbooks: replace placeholder atomic_ids with real technique_ids.

This ensures do_atomic_gen can find real Atomic Red Team tests via the
MITRE technique ID fallback.
