"""Agent flavour selection and agent-staging regression tests.

Covers the two fixes that keep stale staging from corrupting agents:

- :func:`cli.commands.command_and_control_migrated.select_agent_flavour`
  picks ``.ps1`` vs ``.sh`` from the plan platform or the scripts of the
  CURRENT run, never from the historical contents of
  ``sessions/temp_uploads/``.
- ``do_attack_plan`` derives the agent script list from files written
  during this run (mtime-gated) and ``do_atomic_agent`` picks its
  extension from the most recent script instead of glob order.

The shell-side checks are static (regex over the source) so the tests do
not have to boot ``LazyOwnShell`` or the Atomic resolver.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "cli" / "commands" / "command_and_control_migrated.py"


@pytest.fixture(scope="module", autouse=True)
def _add_repo_root_to_syspath() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


class TestSelectAgentFlavour:
    @pytest.fixture
    def select(self):
        from cli.commands.command_and_control_migrated import select_agent_flavour

        return select_agent_flavour

    def test_windows_platform_forces_powershell(self, select):
        assert select(["atomic_test_a.sh"], "windows") == ".ps1"

    def test_non_windows_platform_forces_shell(self, select):
        assert select(["atomic_test_a.ps1"], "linux") == ".sh"
        assert select(["atomic_test_a.ps1"], "macos") == ".sh"

    def test_unplatformed_runs_follow_generated_tests_only(self, select):
        assert select(["atomic_test_a.sh", "atomic_test_old.sh"], "") == ".sh"
        assert select(["atomic_test_a.ps1", "atomic_test_old.ps1"], "") == ".ps1"

    def test_mixed_run_prefers_majority(self, select):
        assert (
            select(["atomic_test_a.sh", "atomic_test_b.ps1", "atomic_test_c.ps1"], "")
            == ".ps1"
        )

    def test_mixed_tie_falls_back_to_shell(self, select):
        assert select(["atomic_test_a.sh", "atomic_test_b.ps1"], "") == ".sh"


class TestAttackPlanSources:
    def test_agent_scripts_derived_from_current_run(self):
        src = MODULE_PATH.read_text(encoding="utf-8")
        assert "select_agent_flavour(run_tests, platform)" in src
        assert ">= run_started" in src
        assert "run_started = time.time()" in src

    def test_stale_glob_counting_removed(self):
        src = MODULE_PATH.read_text(encoding="utf-8")
        assert 'glob(os.path.join(uploads, "atomic_test_*.sh"))' not in src
        assert "sh_count" not in src
        assert "ps_count" not in src

    def test_atomic_agent_extension_from_latest_script(self):
        src = MODULE_PATH.read_text(encoding="utf-8")
        assert "test_scripts[0].endswith" not in src
        assert re.search(r"max\(test_scripts, key=os\.path\.getmtime\)", src) is not None
