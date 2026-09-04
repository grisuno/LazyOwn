"""Tests for the documentation-stats single source of truth.

The module under test lives in ``scripts/``, which is not an importable
package, so it is surfaced by importing it via ``importlib.util`` from its
path. These tests lock the contract that documentation numbers are derived
from the committed command index and never drift independently.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def _load_module():
    spec = importlib.util.spec_from_file_location("sync_doc_stats", SCRIPTS_DIR / "sync_doc_stats.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def mod():
    return _load_module()


def test_canonical_command_count_reads_index(mod, tmp_path):
    cli_dir = tmp_path / "cli"
    cli_dir.mkdir()
    (cli_dir / "command_index.json").write_text(json.dumps({"totals": {"unique_commands": 729}}), encoding="utf-8")
    assert mod.canonical_command_count(tmp_path) == 729


def test_measure_stats_command_count_matches_index(mod, tmp_path):
    cli_dir = tmp_path / "cli"
    skills_dir = tmp_path / "skills"
    modules_dir = tmp_path / "modules"
    for directory in (
        cli_dir,
        skills_dir,
        modules_dir,
        tmp_path / "lazyaddons",
        tmp_path / "plugins",
        tmp_path / "playbooks",
    ):
        directory.mkdir(exist_ok=True)
    for directory in (tmp_path / "lazyaddons", tmp_path / "plugins", tmp_path / "playbooks"):
        directory.mkdir(exist_ok=True)
    (cli_dir / "command_index.json").write_text(json.dumps({"totals": {"unique_commands": 729}}), encoding="utf-8")
    (cli_dir / "aliases.yaml").write_text("lazynmap: ''\n", encoding="utf-8")
    (skills_dir / "lazyown_mcp.py").write_text('name="lazyown_a"', encoding="utf-8")
    (modules_dir / "lazyown_bridge.py").write_text("CatalogEntry(", encoding="utf-8")

    stats = mod.measure_stats(tmp_path)

    assert stats["cli_commands"] == 729
    assert stats["cli_hundreds"] == 700
    assert stats["mcp_tools"] == 1
    assert stats["aliases"] == 1


def test_sync_check_does_not_write(mod, tmp_path):
    (tmp_path / "ESSENTIALS.md").write_text("All 606 commands with descriptions", encoding="utf-8")
    stats = {
        "cli_commands": 729,
        "aliases": 126,
        "mcp_tools": 153,
        "bridge_catalog": 363,
    }
    stale = mod.sync(check=True, stats=stats, root=tmp_path)
    assert stale
    assert "All 606 commands with descriptions" in (tmp_path / "ESSENTIALS.md").read_text(encoding="utf-8")


def test_sync_apply_rewrites_when_stale(mod, tmp_path):
    (tmp_path / "ESSENTIALS.md").write_text("All 606 commands with descriptions", encoding="utf-8")
    stats = {
        "cli_commands": 729,
        "aliases": 126,
        "mcp_tools": 153,
        "bridge_catalog": 363,
    }
    mod.sync(check=False, stats=stats, root=tmp_path)
    assert "All 729 commands with descriptions" in (tmp_path / "ESSENTIALS.md").read_text(encoding="utf-8")


def test_render_formats_template(mod):
    assert mod.render("All {cli_commands} commands", {"cli_commands": 729}) == "All 729 commands"
