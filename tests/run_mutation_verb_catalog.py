"""Mutation runner for the verb catalog contract.

Each mutant disables one catalog guarantee: builtin seeding, operator
state preservation, index-driven discovery or fail-closed gating. The
scoped suite must fail for every mutant; a survivor means the contract
is weak.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tests.mutation_common import run_all  # noqa: E402

MUTATIONS = {
    "builtins_seed_disabled": {
        "file": "modules/verb_catalog.py",
        "description": "Seed builtin verbs off so auto verbs turn off",
        "old": '"enabled": name in builtins,',
        "new": '"enabled": False,',
        "expected": "test_sync_seeds_all_index_commands must fail",
    },
    "sync_resets_operator_state": {
        "file": "modules/verb_catalog.py",
        "description": "Ignore stored operator choices during sync",
        "old": "            else:\n                entry = dict(stored)",
        "new": "            else:\n                entry = {}",
        "expected": "test_sync_preserves_operator_choices must fail",
    },
    "index_discovery_off": {
        "file": "modules/verb_catalog.py",
        "description": "Skip the command index so discovery falls back",
        "old": "        if cfg.index_path.is_file():",
        "new": "        if False:",
        "expected": "test_index_commands_reads_command_index_json must fail",
    },
    "gate_force_allow": {
        "file": "modules/auto_registry.py",
        "description": "Allow catalog commands even when disabled",
        "old": '    return bool(entry and entry.get("source") == "catalog" and entry.get("enabled"))',
        "new": "    return True",
        "expected": "test_disabled_command_is_not_routable must fail",
    },
}

TEST_TARGETS = ["tests/test_verb_catalog.py"]


def main() -> int:
    """Execute baseline, every mutant and restore the source."""
    return run_all(MUTATIONS, TEST_TARGETS)


if __name__ == "__main__":
    sys.exit(main())
