"""Regression guard for the ``cli/commands`` migration generator.

``scripts/migrate_lazyown.py`` emits phase-scoped ``*CommandSet`` modules. A
prior version wrote the literal ``__all__ = [f"{phase.title()}CommandSet"]``
into every generated module -- an f-string that landed verbatim in the output
where ``phase`` is undefined at module scope. Each generated module therefore
raised ``NameError`` on import, which aborted
:func:`cli.registry.iter_command_sets` and silently dropped every command set
discovered after the offender.

These tests pin the generator contract so that regression cannot return: the
emitted ``__all__`` must be a static list naming exactly the generated class,
and the whole module must parse and expose that class name.
"""

from __future__ import annotations

import ast

from scripts.migrate_lazyown import build_migrated_module

SAMPLE_METHODS: list[tuple[str, str]] = [
    ("do_probe", "    def do_probe(self, line):\n        print_msg('probe')\n"),
]


def _module_all(source: str) -> list[str]:
    """Extract the ``__all__`` literal from ``source`` via AST.

    Args:
        source: Generated module source text.

    Returns:
        The list of string names assigned to ``__all__``.

    Raises:
        AssertionError: When ``__all__`` is missing or is not a list of string
            constants (for example an f-string that would fail at import time).
    """
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            continue
        assert isinstance(node.value, ast.List), "__all__ must be a static list literal"
        names: list[str] = []
        for element in node.value.elts:
            assert isinstance(element, ast.Constant) and isinstance(element.value, str), (
                "__all__ entries must be plain string constants, not f-strings or calls"
            )
            names.append(element.value)
        return names
    raise AssertionError("__all__ not found in generated module")


def test_generated_module_parses() -> None:
    source = build_migrated_module("recon", "recon_category", SAMPLE_METHODS)
    ast.parse(source)


def test_all_is_static_and_matches_class_name() -> None:
    source = build_migrated_module("recon", "recon_category", SAMPLE_METHODS)
    assert _module_all(source) == ["ReconCommandSet"]
    assert "class ReconCommandSet(LazyOwnCommandSet):" in source


def test_compound_phase_title_casing() -> None:
    source = build_migrated_module("command_and_control", "command_and_control_category", [])
    assert _module_all(source) == ["Command_And_ControlCommandSet"]
    assert "class Command_And_ControlCommandSet(LazyOwnCommandSet):" in source


def test_no_unevaluated_fstring_all_literal() -> None:
    source = build_migrated_module("scan", "scanning_category", [])
    assert 'f"{phase.title()}CommandSet"' not in source
    assert 'phase = "scan"' in source
    assert 'category = "scanning_category"' in source


def test_method_bodies_are_embedded_in_order() -> None:
    methods = [
        ("do_alpha", "    def do_alpha(self, line):\n        return None\n"),
        ("do_beta", "    def do_beta(self, line):\n        return None\n"),
    ]
    source = build_migrated_module("misc", "miscellaneous_category", methods)
    assert source.index("def do_alpha") < source.index("def do_beta")
