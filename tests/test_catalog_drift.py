"""Catalog drift gate: bridge suggestions must point at real commands.

``modules/lazyown_bridge.CommandCatalog`` feeds phase suggestions that are
executed verbatim through the shell. A catalog entry whose command no
longer exists is a ghost: the suggestion renders, the execution fails.
The generated ``cli/command_index.json`` (from ``scripts/build_command_index.py``)
is the authority for what the shell can run.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "cli" / "command_index.json"
BRIDGE_PATH = REPO_ROOT / "modules" / "lazyown_bridge.py"

_CATALOG_ENTRY_RE = re.compile(r'CatalogEntry\(\s*"([^"]+)"\s*,\s*\n?\s*"([^"]+)"', re.S)


def _indexed_commands() -> set[str]:
    document = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {entry["name"].removeprefix("do_") for entry in document["commands"]}


def test_bridge_catalog_has_no_ghost_commands() -> None:
    """Every catalog command must be a registered shell command."""
    source = BRIDGE_PATH.read_text(encoding="utf-8")
    catalog_commands = {command for command, _phase in _CATALOG_ENTRY_RE.findall(source)}
    indexed = _indexed_commands()
    ghosts = sorted(catalog_commands - indexed)
    assert not ghosts, f"ghost catalog commands (not in cli/command_index.json): {ghosts}"


def test_bridge_catalog_has_no_same_phase_duplicates() -> None:
    """A (command, phase) pair may appear at most once in the catalog."""
    source = BRIDGE_PATH.read_text(encoding="utf-8")
    pairs = _CATALOG_ENTRY_RE.findall(source)
    duplicates = sorted({pair for pair in pairs if pairs.count(pair) > 1})
    assert not duplicates, f"duplicated (command, phase) catalog entries: {duplicates}"


def test_command_index_is_fresh() -> None:
    """The committed index must match a fresh rebuild (no drift)."""
    import subprocess
    import sys

    fresh = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build_command_index.py"), "--stdout"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert fresh.returncode == 0, fresh.stderr
    committed = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    rebuilt = json.loads(fresh.stdout)
    assert committed["totals"] == rebuilt["totals"], (
        f"index totals drift: committed {committed['totals']} vs rebuilt {rebuilt['totals']} "
        "(run 'python3 scripts/build_command_index.py')"
    )
