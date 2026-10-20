"""Mutation runner for the trigger policy contract.

Each mutant breaks one declarative guarantee: the shipped YAML is the
seed source, coercion keeps operator intent (enabled=False), unknown
seeds cannot enter the store, and reading validates the document.

"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tests.mutation_common import run_all  # noqa: E402

MUTATIONS = {
    "yaml_policy_ignored": {
        "file": "modules/trigger_policy.py",
        "description": "Drop the triggers section so no seed ever loads",
        "old": '    raw = document.get("triggers") if isinstance(document, dict) else None',
        "new": '    raw = []',
        "expected": "test_orchestrator_yaml_declares_trigger_seeds must fail",
    },
    "seed_enabled_flag_forced": {
        "file": "modules/trigger_policy.py",
        "description": "Force seeds enabled so disabled YAML rows cannot stay off",
        "old": '                "enabled": bool(flag) if isinstance(flag, bool) else True,',
        "new": '                "enabled": True,',
        "expected": "test_seeds_coerce_and_skip_unknown_kinds must fail",
    },
    "store_accepts_unknown_kinds": {
        "file": "modules/loop_triggers.py",
        "description": "Skip kind validation so garbage seeds enter the store",
        "old": "            if kind not in core.TRIGGER_KINDS:\n                continue",
        "new": "            if False:\n                continue",
        "expected": "test_seed_store_is_idempotent must fail",
    },
    "validation_never_reports": {
        "file": "modules/trigger_policy.py",
        "description": "Make validation accept unknown kinds silently",
        "old": "        if not isinstance(kind, str) or kind not in TRIGGER_KINDS:",
        "new": "        if False:",
        "expected": "test_validate_policy_rejects_bad_documents must fail",
    },
}

TEST_TARGETS = ["tests/test_trigger_policy.py"]


def main() -> int:
    """Execute baseline, every mutant and restore the source."""
    return run_all(MUTATIONS, TEST_TARGETS)


if __name__ == "__main__":
    sys.exit(main())
