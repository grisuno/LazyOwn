"""Cross-CommandSet command-name uniqueness contract.

cmd2 refuses to register a second ``do_<name>`` once a command exists
(and aborts the whole CommandSet mid-registration), which happened live
with ``do_lazy_evidence`` defined by both ``lazyops`` and ``lazyloop``.
This test parses ``cli/commands/*.py`` and fails on any ``do_*`` name
defined by more than one class.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

COMMANDS_DIR = Path(__file__).resolve().parent.parent / "cli" / "commands"


def _is_command_set(node: ast.ClassDef) -> bool:
    """Whether the class extends a ``*CommandSet`` base (cmd2 scope)."""
    for base in node.bases:
        target = base.attr if isinstance(base, ast.Attribute) else getattr(base, "id", "")
        if target.endswith("CommandSet"):
            return True
    return False


def _command_definitions() -> dict[str, list[str]]:
    """Map every CommandSet ``do_*`` name to its ``file:class`` owners."""
    owners: dict[str, list[str]] = defaultdict(list)
    for path in sorted(COMMANDS_DIR.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef) or not _is_command_set(node):
                continue
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith("do_"):
                    owners[item.name].append(f"{path.name}:{node.name}")
    return owners


def test_no_command_defined_by_two_command_sets() -> None:
    """A ``do_*`` name must have exactly one owning CommandSet class."""
    collisions = {name: owners for name, owners in _command_definitions().items() if len(set(owners)) > 1}
    assert not collisions, f"do_* defined by multiple CommandSets: {collisions}"
