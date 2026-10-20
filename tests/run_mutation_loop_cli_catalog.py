"""Mutation runner for the planner catalog visibility contract.

Each mutant attacks one guarantee: fail-closed absence, the kill-chain
phase filter, the enabled-only filter and the prompt wiring.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tests.mutation_common import run_all  # noqa: E402

MUTATIONS = {
    "phase_filter_off": {
        "file": "modules/lazy_cli_bridge.py",
        "description": "Ignore the kill-chain phase when building the verbs line",
        "old": '            if bool(row.get("enabled")) and str(row.get("phase") or "") == phase',
        "new": '            if bool(row.get("enabled"))',
        "expected": "test_catalog_cli_for_phase_lists_enabled_only must fail",
    },
    "enabled_filter_off": {
        "file": "modules/lazy_cli_bridge.py",
        "description": "Advertise disabled commands to the planner",
        "old": '            if bool(row.get("enabled")) and str(row.get("phase") or "") == phase',
        "new": '_ = row\n            if str(row.get("phase") or "") == phase',
        "expected": "test_catalog_cli_for_phase_lists_enabled_only must fail",
    },
    "fail_closed_lost": {
        "file": "modules/lazy_cli_bridge.py",
        "description": "Return a generic list when the catalog view fails",
        "old": "    except Exception:\n        return \"\"",
        "new": "    except Exception:\n        return \"lazynmap\"",
        "expected": "test_missing_catalog_view_adds_nothing must fail",
    },
    "prompt_wiring_off": {
        "file": "modules/lazy_loop.py",
        "description": "Stop carrying allowed commands in the prompt context",
        "old": '            parts.append(f"Allowed commands: {allowed}")',
        "new": "            _ = allowed",
        "expected": "test_prompt_context_carries_allowed_commands must fail",
    },
}

TEST_TARGETS = ["tests/test_loop_cli_catalog.py"]


def main() -> int:
    """Execute baseline, every mutant and restore the source."""
    return run_all(MUTATIONS, TEST_TARGETS)


if __name__ == "__main__":
    sys.exit(main())
