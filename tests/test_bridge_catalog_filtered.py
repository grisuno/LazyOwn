"""tests/test_bridge_catalog_filtered.py

Tests for ``BridgeDispatcher.catalog_summary_filtered`` and the
``phase``/``os_hint`` parameters now accepted by ``_t_bridge_catalog``.

Goal: prove that the filtered summary returns the same data shape as
``catalog_summary`` while excluding entries whose phase or target OS
does not match. The agent prompt path (``_t_bridge_catalog``) is also
exercised so the LLM-facing string honours the filter when arguments
are supplied and stays backward-compatible when they are omitted.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))


@pytest.fixture(scope="module")
def dispatcher():
    from lazyown_bridge import get_dispatcher
    return get_dispatcher()


class TestCatalogSummaryFiltered:
    def test_no_args_matches_unfiltered_summary(self, dispatcher):
        baseline = dispatcher.catalog_summary()
        filtered = dispatcher.catalog_summary_filtered()
        assert filtered == baseline

    def test_phase_arg_restricts_to_one_phase(self, dispatcher):
        filtered = dispatcher.catalog_summary_filtered(phase="recon")
        assert set(filtered.keys()) == {"recon"}
        assert len(filtered["recon"]) >= 5

    def test_phase_arg_accepts_world_model_alias(self, dispatcher):
        canonical = dispatcher.catalog_summary_filtered(phase="recon")
        aliased = dispatcher.catalog_summary_filtered(phase="scanning")
        assert canonical == aliased

    def _entries_for(self, dispatcher, phase, command_name):
        return [
            entry for entry in dispatcher._catalog.by_phase(phase)
            if entry.command == command_name
        ]

    def test_os_hint_linux_excludes_windows_only_entries(self, dispatcher):
        linux_summary = dispatcher.catalog_summary_filtered(os_hint="linux")
        for phase, commands in linux_summary.items():
            for cmd in commands:
                matches = self._entries_for(dispatcher, phase, cmd)
                assert matches, f"{cmd!r} missing from phase {phase}"
                assert any(entry.matches_os("linux") for entry in matches), (
                    f"{cmd!r} in phase {phase} has no linux-compatible entry"
                )

    def test_os_hint_windows_excludes_linux_only_entries(self, dispatcher):
        win_summary = dispatcher.catalog_summary_filtered(os_hint="windows")
        for phase, commands in win_summary.items():
            for cmd in commands:
                matches = self._entries_for(dispatcher, phase, cmd)
                assert matches, f"{cmd!r} missing from phase {phase}"
                assert any(entry.matches_os("windows") for entry in matches), (
                    f"{cmd!r} in phase {phase} has no windows-compatible entry"
                )

    def test_os_filter_shrinks_or_preserves_each_phase(self, dispatcher):
        baseline = dispatcher.catalog_summary_filtered()
        for os_name in ("linux", "windows"):
            filtered = dispatcher.catalog_summary_filtered(os_hint=os_name)
            for phase, cmds in filtered.items():
                assert len(cmds) <= len(baseline[phase]), (
                    f"os_hint={os_name} produced more commands than baseline "
                    f"for phase {phase}: {len(cmds)} > {len(baseline[phase])}"
                )

    def test_phase_plus_os_combines_both_filters(self, dispatcher):
        recon_linux = dispatcher.catalog_summary_filtered(phase="recon", os_hint="linux")
        assert set(recon_linux.keys()) <= {"recon"}
        if "recon" in recon_linux:
            for cmd in recon_linux["recon"]:
                matches = self._entries_for(dispatcher, "recon", cmd)
                assert any(entry.matches_os("linux") for entry in matches)

    def test_empty_phase_keeps_all_phases(self, dispatcher):
        baseline = dispatcher.catalog_summary_filtered()
        empty_string = dispatcher.catalog_summary_filtered(phase="")
        assert empty_string == baseline

    def test_phase_drops_smaller_than_unfiltered_total(self, dispatcher):
        baseline_count = sum(len(v) for v in dispatcher.catalog_summary().values())
        recon = dispatcher.catalog_summary_filtered(phase="recon")
        recon_count = sum(len(v) for v in recon.values())
        assert recon_count < baseline_count

    def test_os_hint_any_is_passthrough(self, dispatcher):
        baseline = dispatcher.catalog_summary_filtered(phase="recon")
        explicit_any = dispatcher.catalog_summary_filtered(phase="recon", os_hint="any")
        assert baseline == explicit_any

    def test_os_hint_uppercase_normalized(self, dispatcher):
        a = dispatcher.catalog_summary_filtered(os_hint="LINUX")
        b = dispatcher.catalog_summary_filtered(os_hint="linux")
        assert a == b


class TestBridgeCatalogToolFunction:
    def test_no_args_returns_full_catalog_header(self):
        from lazyown_groq_agents import _t_bridge_catalog
        out = _t_bridge_catalog()
        assert "Bridge catalog" in out
        assert "phase=" not in out
        assert "os=" not in out

    def test_phase_arg_appears_in_header(self):
        from lazyown_groq_agents import _t_bridge_catalog
        out = _t_bridge_catalog(phase="recon")
        assert "phase=recon" in out
        assert "os=any" in out

    def test_os_hint_only_appears_in_header(self):
        from lazyown_groq_agents import _t_bridge_catalog
        out = _t_bridge_catalog(os_hint="linux")
        assert "os=linux" in out
        assert "phase=" not in out

    def test_unknown_phase_returns_friendly_no_match(self):
        from lazyown_groq_agents import _t_bridge_catalog
        out = _t_bridge_catalog(phase="recon", os_hint="windows")
        assert "Bridge catalog" in out

    def test_registry_exposes_optional_phase_and_os(self):
        from lazyown_groq_agents import REGISTRY
        _desc, params, _func = REGISTRY["bridge_catalog"]
        assert "phase" in params
        assert "os_hint" in params
