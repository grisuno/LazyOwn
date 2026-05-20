"""Command palette test suite.

Single, self-contained test surface for the operator command palette
feature spanning three layers:

- The static AST generator in ``scripts/build_command_index.py`` and the
  on-disk artefact ``cli/command_index.json``.
- The read-only loader API in ``cli/palette.py``.
- The pure parser, query, renderer and completer in ``cli/palette_command.py``
  and the thin glue wired into ``lazyown.py``.

Architecture follows the same SOLID partitioning as the production code:

- :class:`PaletteSuiteConfig` is the only place where paths, expected
  invariants, schema fields, AST conventions and known legacy duplicates
  live. Every test class consumes the config rather than redeclaring
  literals.
- One test class per responsibility so a failure points at one specific
  contract — index invariants, legacy duplicates, generator determinism,
  generator helpers, loader API, argument parser, index query, renderer,
  completer, top-level dispatcher, ``lazyown.py`` wiring.
- Behavioural tests for the parser, query, renderer and completer run
  against a synthetic in-memory index produced by
  :func:`_build_synthetic_index`, so they remain decoupled from the size
  and contents of the live ``cli/command_index.json``.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import pytest


@dataclass(frozen=True)
class PaletteSuiteConfig:
    """Centralised constants for the entire palette suite.

    Every literal the suite depends on lives here so adding a new probe
    or moving the index file means editing one location.
    """

    do_command_prefix: str = "do_"
    expected_schema_version: int = 1
    summary_max_chars: int = 160
    summary_truncation_marker: str = "…"
    sample_index_phases: tuple[str, ...] = ("recon", "exploit", "misc")
    synthetic_recon_unique_count: int = 2
    synthetic_exploit_unique_count: int = 1
    synthetic_misc_unique_count: int = 1
    synthetic_search_alpha_min_hits: int = 2
    synthetic_method_definitions: int = 5
    synthetic_unique_commands: int = 4
    synthetic_duplicates: int = 1
    synthetic_categories: int = 3
    required_top_level_keys: frozenset[str] = frozenset(
        {
            "schema_version",
            "sources",
            "source_sha256",
            "totals",
            "phase_to_commands",
            "category_to_commands",
            "duplicates",
            "commands",
        }
    )
    required_command_fields: frozenset[str] = frozenset(
        {
            "name",
            "line",
            "summary",
            "category",
            "phase",
            "source_file",
            "class_name",
            "duplicate_of",
        }
    )
    required_lazyown_imports: tuple[str, ...] = (
        "from cli.palette import CommandIndexError as _CommandIndexError",
        "from cli.palette import load_index as _load_command_index",
        "from cli.palette_command import PaletteCompleter as _PaletteCompleter",
        "from cli.palette_command import PaletteRenderConfig as _PaletteRenderConfig",
        "from cli.palette_command import render as _render_palette",
    )
    expected_lazyown_methods: frozenset[str] = frozenset({"do_palette", "complete_palette"})
    lazyown_shell_class_name: str = "LazyOwnShell"
    known_duplicate_lines: dict[str, frozenset[int]] = field(
        default_factory=lambda: {
            "do_shellshock": frozenset({12297, 15775}),
            "do_download_c2": frozenset({26386, 27853}),
        }
    )
    invalid_index_payload: str = "{not json"
    case_sensitive_invariant_phase_index: int = 0
    mcp_tool_name: str = "lazyown_palette"
    mcp_input_property: str = "line"
    mcp_required_imports: tuple[str, ...] = (
        "from cli.palette import CommandIndexError as _PaletteIndexError",
        "from cli.palette import load_index as _palette_load_index",
        "from cli.palette_command import render_json as _palette_render_json",
    )
    c2_required_imports: tuple[str, ...] = (
        "from cli.palette import CommandIndexError as _PaletteIndexError",
        "from cli.palette import load_index as _palette_load_index",
        "from cli.palette_command import build_palette_view as _palette_build_view",
    )
    c2_route_decorator: str = "@app.route('/palette', methods=['GET'])"
    c2_route_function: str = "palette_view"
    c2_template_filename: str = "palette.html"
    c2_template_required_markers: tuple[str, ...] = (
        "{% extends 'base.html' %}",
        "{% block content %}",
        'id="palette-search"',
        'id="palette-phase-filter"',
        'id="palette-data"',
        "{{ context_json | safe }}",
    )
    base_template_required_markers: tuple[str, ...] = (
        'id="lazyown-cmdk-overlay"',
        'id="lazyown-cmdk-input"',
        'id="lazyown-cmdk-list"',
        "fetch('/api/palette'",
        "event.key === 'k' || event.key === 'K'",
    )
    base_template_telemetry_markers: tuple[str, ...] = (
        "function scoreCommand(",
        "payload.recents",
        "cmd-runs",
        "cmdk-section",
    )
    api_palette_route_decorator: str = "@app.route('/api/palette', methods=['GET'])"
    api_palette_route_function: str = "palette_api"
    api_palette_rate_limit_marker: str = "@limiter.limit(_PALETTE_API_RATE_LIMIT)"
    api_palette_rate_limit_constant: str = "_PALETTE_API_RATE_LIMIT"
    json_required_keys: frozenset[str] = frozenset({"mode", "phase", "query", "target", "results", "phase_counts"})
    view_required_keys: frozenset[str] = frozenset(
        {
            "page_title",
            "page_subtitle",
            "search_placeholder",
            "phase_filter_all_label",
            "empty_results_message",
            "search_flag",
            "info_flag",
            "phases",
            "commands",
            "totals",
        }
    )
    view_phase_required_keys: frozenset[str] = frozenset({"id", "label", "count"})
    view_totals_required_keys: frozenset[str] = frozenset({"commands", "phases"})

    @property
    def repo_root(self) -> Path:
        """Absolute path to the repository root."""
        return Path(__file__).resolve().parent.parent

    @property
    def index_path(self) -> Path:
        """Absolute path to the on-disk command index JSON."""
        return self.repo_root / "cli" / "command_index.json"

    @property
    def lazyown_path(self) -> Path:
        """Absolute path to the legacy ``lazyown.py`` entry point."""
        return self.repo_root / "lazyown.py"

    @property
    def cli_commands_dir(self) -> Path:
        """Directory holding the modular phase ``CommandSet`` files."""
        return self.repo_root / "cli" / "commands"

    @property
    def mcp_path(self) -> Path:
        """Absolute path to the MCP server entry point."""
        return self.repo_root / "skills" / "lazyown_mcp.py"

    @property
    def lazyc2_path(self) -> Path:
        """Absolute path to the C2 web server entry point."""
        return self.repo_root / "lazyc2.py"

    @property
    def palette_template_path(self) -> Path:
        """Absolute path to the C2 palette Jinja2 template."""
        return self.repo_root / "templates" / self.c2_template_filename

    @property
    def base_template_path(self) -> Path:
        """Absolute path to the shared C2 base layout template."""
        return self.repo_root / "templates" / "base.html"

    @property
    def graphify_path(self) -> Path:
        """Absolute path to the graphify export consumed by neighbour lookups."""
        return self.repo_root / "graphify-out" / "graph_lazyown.json"


@pytest.fixture(scope="session")
def suite_config() -> PaletteSuiteConfig:
    """Single, immutable configuration shared by every test class."""
    return PaletteSuiteConfig()


@pytest.fixture(scope="session", autouse=True)
def _ensure_repo_on_path(suite_config: PaletteSuiteConfig) -> None:
    """Make repository top-level packages importable for the suite."""
    if str(suite_config.repo_root) not in sys.path:
        sys.path.insert(0, str(suite_config.repo_root))


@pytest.fixture(scope="session")
def index_document(suite_config: PaletteSuiteConfig) -> dict[str, Any]:
    """The on-disk command-index document, loaded once per session."""
    if not suite_config.index_path.exists():
        pytest.fail(
            f"{suite_config.index_path.relative_to(suite_config.repo_root)} is missing. "
            "Run 'python3 scripts/build_command_index.py' first."
        )
    return json.loads(suite_config.index_path.read_text(encoding="utf-8"))


def _iter_command_modules(config: PaletteSuiteConfig) -> Iterable[Path]:
    """Yield every public ``cli/commands/*.py`` module path."""
    if not config.cli_commands_dir.is_dir():
        return ()
    return tuple(
        p for p in sorted(config.cli_commands_dir.iterdir()) if p.suffix == ".py" and not p.name.startswith("_")
    )


def _collect_do_method_names(path: Path, prefix: str) -> set[str]:
    """Return every direct ``do_*`` method name in any class in ``path``."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    out: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name.startswith(prefix):
                out.add(child.name)
    return out


@pytest.fixture(scope="session")
def ast_command_names(suite_config: PaletteSuiteConfig) -> frozenset[str]:
    """Static AST sweep of every operator-visible ``do_*`` name."""
    names: set[str] = set()
    names.update(_collect_do_method_names(suite_config.lazyown_path, suite_config.do_command_prefix))
    for path in _iter_command_modules(suite_config):
        names.update(_collect_do_method_names(path, suite_config.do_command_prefix))
    return frozenset(names)


def _build_synthetic_index(config: PaletteSuiteConfig) -> dict[str, Any]:
    """Construct a small, deterministic in-memory index for behaviour tests.

    Shape mirrors the schema of the on-disk artefact so every consumer of
    the production index can be exercised without loading the full
    catalogue.
    """
    prefix = config.do_command_prefix
    phase_recon, phase_exploit, phase_misc = config.sample_index_phases
    commands: list[dict[str, Any]] = [
        {
            "name": f"{prefix}rec_alpha",
            "line": 100,
            "summary": "Recon alpha helper.",
            "category": "01. Reconnaissance",
            "phase": phase_recon,
            "source_file": "lazyown.py",
            "class_name": config.lazyown_shell_class_name,
            "community": None,
            "duplicate_of": None,
        },
        {
            "name": f"{prefix}rec_beta",
            "line": 200,
            "summary": "Recon beta helper.",
            "category": "01. Reconnaissance",
            "phase": phase_recon,
            "source_file": "lazyown.py",
            "class_name": config.lazyown_shell_class_name,
            "community": None,
            "duplicate_of": None,
        },
        {
            "name": f"{prefix}exp_alpha",
            "line": 300,
            "summary": "Exploit alpha helper.",
            "category": "03. Exploitation",
            "phase": phase_exploit,
            "source_file": "lazyown.py",
            "class_name": config.lazyown_shell_class_name,
            "community": None,
            "duplicate_of": None,
        },
        {
            "name": f"{prefix}misc_alpha",
            "line": 400,
            "summary": "Miscellaneous helper.",
            "category": "12. Miscellaneous",
            "phase": phase_misc,
            "source_file": "lazyown.py",
            "class_name": config.lazyown_shell_class_name,
            "community": None,
            "duplicate_of": None,
        },
        {
            "name": f"{prefix}rec_alpha",
            "line": 999,
            "summary": "Recon alpha duplicate.",
            "category": "01. Reconnaissance",
            "phase": phase_recon,
            "source_file": "lazyown.py",
            "class_name": config.lazyown_shell_class_name,
            "community": None,
            "duplicate_of": f"{prefix}rec_alpha",
        },
    ]
    phase_to_commands: dict[str, list[str]] = {}
    for command in commands:
        phase_to_commands.setdefault(command["phase"], []).append(command["name"])
    for phase, names in phase_to_commands.items():
        phase_to_commands[phase] = sorted(set(names))
    return {
        "schema_version": config.expected_schema_version,
        "sources": ["lazyown.py"],
        "source_sha256": {"lazyown.py": "deadbeef"},
        "totals": {
            "method_definitions": config.synthetic_method_definitions,
            "unique_commands": config.synthetic_unique_commands,
            "duplicates": config.synthetic_duplicates,
            "phases": len(config.sample_index_phases),
            "categories": config.synthetic_categories,
        },
        "phase_to_commands": phase_to_commands,
        "category_to_commands": {},
        "duplicates": [
            {
                "name": f"{prefix}rec_alpha",
                "occurrences": [
                    {
                        "line": 100,
                        "source_file": "lazyown.py",
                        "class_name": config.lazyown_shell_class_name,
                    },
                    {
                        "line": 999,
                        "source_file": "lazyown.py",
                        "class_name": config.lazyown_shell_class_name,
                    },
                ],
            }
        ],
        "commands": commands,
    }


@pytest.fixture
def synthetic_index(suite_config: PaletteSuiteConfig) -> dict[str, Any]:
    """In-memory index used by parser/query/renderer/completer tests."""
    return _build_synthetic_index(suite_config)


def _extract_method_body(src: str, name: str) -> str:
    """Return the textual body of a method defined in ``src``.

    Args:
        src: Full source text of a Python module.
        name: Method name to locate.

    Returns:
        The slice between the ``def <name>(...)`` line and the next sibling
        ``def`` / decorator at the same indentation, or the empty string
        when the method is missing.
    """
    pattern = re.compile(
        rf"^(\s*)def {re.escape(name)}\(.*?\):\n(.*?)(?=^\1(?:def |@cmd2|@with_)|^class )",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(src)
    return match.group(2) if match else ""


class TestCommandIndexInvariants:
    """Hard guarantees about the on-disk command-index document."""

    def test_schema_version_matches_config(
        self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """Schema version is pinned and must match the configured expectation."""
        assert index_document["schema_version"] == suite_config.expected_schema_version

    def test_top_level_keys_present(self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig) -> None:
        """Every required top-level key is present in the document."""
        missing = suite_config.required_top_level_keys - set(index_document)
        assert missing == set(), f"missing top-level keys: {sorted(missing)}"

    def test_totals_match_command_list(self, index_document: dict[str, Any]) -> None:
        """``totals`` is consistent with the underlying command list."""
        commands = index_document["commands"]
        totals = index_document["totals"]
        unique_names = {command["name"] for command in commands}
        assert totals["method_definitions"] == len(commands)
        assert totals["unique_commands"] == len(unique_names)
        assert totals["duplicates"] == len(index_document["duplicates"])

    def test_required_command_fields(self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig) -> None:
        """Each command entry exposes the full required field set."""
        for command in index_document["commands"]:
            missing = suite_config.required_command_fields - set(command)
            assert missing == set(), f"{command.get('name')} missing {sorted(missing)}"
            assert command["name"].startswith(suite_config.do_command_prefix)
            assert isinstance(command["line"], int) and command["line"] > 0
            assert isinstance(command["phase"], str) and command["phase"]

    def test_phase_buckets_match_commands(self, index_document: dict[str, Any]) -> None:
        """``phase_to_commands`` is exactly derivable from ``commands``."""
        derived: dict[str, set[str]] = {}
        for command in index_document["commands"]:
            derived.setdefault(command["phase"], set()).add(command["name"])
        for phase, names in index_document["phase_to_commands"].items():
            assert set(names) == derived[phase], f"phase {phase} bucket drift"

    def test_no_command_lost_vs_ast(
        self,
        index_document: dict[str, Any],
        ast_command_names: frozenset[str],
    ) -> None:
        """The index must hold every command an AST sweep can discover."""
        index_names = {command["name"] for command in index_document["commands"]}
        missing = ast_command_names - index_names
        extra = index_names - ast_command_names
        assert missing == set(), f"index lost commands: {sorted(missing)}"
        assert extra == set(), f"index has commands absent from source: {sorted(extra)}"

    def test_unique_count_matches_ast(
        self,
        index_document: dict[str, Any],
        ast_command_names: frozenset[str],
    ) -> None:
        """The unique-command total agrees with the AST sweep."""
        assert index_document["totals"]["unique_commands"] == len(ast_command_names)


class TestKnownLegacyDuplicates:
    """The two pre-existing legacy duplicates must remain visible."""

    def test_duplicate_names_listed(self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig) -> None:
        """Each known legacy duplicate is reported in ``duplicates``."""
        names = {entry["name"] for entry in index_document["duplicates"]}
        assert suite_config.known_duplicate_lines.keys() <= names

    def test_duplicate_lines_match(self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig) -> None:
        """Duplicate locations must match the recorded line numbers."""
        by_name = {entry["name"]: entry for entry in index_document["duplicates"]}
        for name, expected_lines in suite_config.known_duplicate_lines.items():
            actual = frozenset(occ["line"] for occ in by_name[name]["occurrences"])
            assert actual == expected_lines, f"{name} drift: actual={sorted(actual)} expected={sorted(expected_lines)}"

    def test_duplicate_marked_in_command_list(
        self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """Each duplicate name appears with ``duplicate_of`` set."""
        flagged = {command["name"] for command in index_document["commands"] if command.get("duplicate_of")}
        assert set(suite_config.known_duplicate_lines) <= flagged

    def test_one_canonical_per_duplicate(
        self, index_document: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """Exactly one canonical (non-shadowed) entry survives per name."""
        for name in suite_config.known_duplicate_lines:
            rows = [c for c in index_document["commands"] if c["name"] == name]
            canonical = [r for r in rows if r["duplicate_of"] is None]
            assert len(canonical) == 1, f"{name}: expected one canonical entry, got {len(canonical)}"


class TestGeneratorDeterminism:
    """A second build must produce a byte-identical document."""

    def test_render_document_is_idempotent(self) -> None:
        """Two consecutive builds produce equal documents."""
        from scripts.build_command_index import build_index, render_document

        first = render_document(build_index())
        second = render_document(build_index())
        assert first == second

    def test_check_mode_passes_on_committed_index(self, index_document: dict[str, Any]) -> None:
        """A fresh build must equal the committed JSON byte-for-byte."""
        from scripts.build_command_index import build_index, render_document

        fresh = render_document(build_index())
        assert fresh == index_document, "cli/command_index.json is stale. Re-run scripts/build_command_index.py."


class TestGeneratorHelpers:
    """Pure-function unit tests for the small helpers in the generator."""

    def test_summary_truncates_to_max_chars(self, suite_config: PaletteSuiteConfig) -> None:
        """Long docstrings are truncated to the configured maximum."""
        from scripts.build_command_index import _summary_from_docstring

        long_text = "x " * (suite_config.summary_max_chars * 2)
        node = ast.parse(f'def f():\n    """{long_text}"""\n').body[0]
        summary = _summary_from_docstring(node)
        assert len(summary) <= suite_config.summary_max_chars
        assert summary.endswith(suite_config.summary_truncation_marker)

    def test_summary_first_line_only(self) -> None:
        """Only the first non-empty docstring line is captured."""
        from scripts.build_command_index import _summary_from_docstring

        node = ast.parse('def f():\n    """First.\n\n    Second."""\n').body[0]
        assert _summary_from_docstring(node) == "First."

    def test_resolve_category_constant_name(self) -> None:
        """A category constant resolves through the lookup table."""
        from scripts.build_command_index import _resolve_category

        node = ast.parse("@cmd2.with_category(recon_category)\ndef f(): pass\n").body[0]
        assert _resolve_category(node.decorator_list) == "01. Reconnaissance"

    def test_resolve_category_string_literal(self) -> None:
        """A literal-string category is returned verbatim."""
        from scripts.build_command_index import _resolve_category

        node = ast.parse('@cmd2.with_category("13. Lua Plugin")\ndef f(): pass\n').body[0]
        assert _resolve_category(node.decorator_list) == "13. Lua Plugin"

    def test_resolve_category_missing(self) -> None:
        """A method with no category decorator yields ``None``."""
        from scripts.build_command_index import _resolve_category

        node = ast.parse("def f(): pass\n").body[0]
        assert _resolve_category(node.decorator_list) is None


class TestPaletteLoader:
    """Behaviour of :mod:`cli.palette` against the live index."""

    def setup_method(self) -> None:
        """Reset the LRU cache so each test sees a fresh load."""
        from cli.palette import load_index

        load_index.cache_clear()

    def test_load_index_returns_document(self, suite_config: PaletteSuiteConfig) -> None:
        """The loader returns a document with the pinned schema version."""
        from cli import palette

        document = palette.load_index()
        assert document["schema_version"] == suite_config.expected_schema_version

    def test_all_commands_excludes_duplicates_by_default(self) -> None:
        """Default listing omits shadowed duplicate entries."""
        from cli import palette

        rows = palette.all_commands()
        assert all(row["duplicate_of"] is None for row in rows)

    def test_all_commands_with_duplicates_includes_them(self) -> None:
        """Explicit opt-in returns the raw method-level list."""
        from cli import palette

        with_duplicates = palette.all_commands(include_duplicates=True)
        canonical = palette.all_commands()
        assert len(with_duplicates) - len(canonical) == len(palette.duplicates())

    def test_filter_by_phase_returns_only_matching_phase(self, suite_config: PaletteSuiteConfig) -> None:
        """Filter result rows all carry the requested phase."""
        from cli import palette

        target_phase = suite_config.sample_index_phases[suite_config.case_sensitive_invariant_phase_index]
        rows = palette.filter_by_phase(target_phase)
        assert all(row["phase"] == target_phase for row in rows)

    def test_filter_by_phase_unknown_returns_empty(self) -> None:
        """Unknown phases yield an empty list, not an exception."""
        from cli import palette

        assert palette.filter_by_phase("zzz_unknown_phase_xyz") == []

    def test_get_resolves_with_or_without_prefix(self, suite_config: PaletteSuiteConfig) -> None:
        """The ``get`` helper accepts both ``do_x`` and ``x`` forms."""
        from cli import palette

        prefix = suite_config.do_command_prefix
        with_prefix = palette.get(f"{prefix}assign")
        without_prefix = palette.get("assign")
        assert with_prefix is not None
        assert with_prefix == without_prefix

    def test_missing_index_raises_command_index_error(self, tmp_path: Path) -> None:
        """A missing index path raises :class:`CommandIndexError`."""
        from cli.palette import CommandIndexError, load_index

        load_index.cache_clear()
        with pytest.raises(CommandIndexError):
            load_index(str(tmp_path / "missing.json"))

    def test_malformed_json_raises_command_index_error(self, tmp_path: Path, suite_config: PaletteSuiteConfig) -> None:
        """Invalid JSON content raises :class:`CommandIndexError`."""
        from cli.palette import CommandIndexError, load_index

        bad = tmp_path / "bad.json"
        bad.write_text(suite_config.invalid_index_payload, encoding="utf-8")
        load_index.cache_clear()
        with pytest.raises(CommandIndexError):
            load_index(str(bad))


class TestPaletteArgumentParser:
    """Routing rules for raw command lines."""

    @pytest.fixture
    def parser(self):
        """A parser bound to the default render config."""
        from cli.palette_command import PaletteArgumentParser, PaletteRenderConfig

        return PaletteArgumentParser(PaletteRenderConfig())

    def test_empty_line_routes_to_overview(self, parser, suite_config: PaletteSuiteConfig) -> None:
        """Empty input always produces the overview."""
        from cli.palette_command import PaletteMode

        result = parser.parse("", known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.OVERVIEW

    def test_known_phase_token_routes_to_phase(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """A single token that matches a phase routes to phase mode."""
        from cli.palette_command import PaletteMode

        target = suite_config.sample_index_phases[0]
        result = parser.parse(target, known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.PHASE
        assert result.phase == target

    def test_unknown_token_routes_to_search(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """A non-phase token routes to fuzzy search."""
        from cli.palette_command import PaletteMode

        result = parser.parse("zzzz_xyz", known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.SEARCH
        assert result.query == "zzzz_xyz"

    def test_phase_with_query_token(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """A phase plus a second token narrows the listing."""
        from cli.palette_command import PaletteMode

        phase = suite_config.sample_index_phases[0]
        result = parser.parse(f"{phase} alpha", known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.PHASE
        assert result.phase == phase
        assert result.query == "alpha"

    def test_search_flag_routes_to_search(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """The ``--search`` flag forces search mode."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig

        flag = PaletteRenderConfig().search_flag
        result = parser.parse(f"{flag} nmap", known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.SEARCH
        assert result.query == "nmap"

    def test_info_flag_routes_to_detail(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """The ``--info`` flag forces detail mode."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig

        flag = PaletteRenderConfig().info_flag
        result = parser.parse(
            f"{flag} {suite_config.do_command_prefix}assign",
            known_phases=suite_config.sample_index_phases,
        )
        assert result.mode is PaletteMode.DETAIL
        assert result.target_name == f"{suite_config.do_command_prefix}assign"

    def test_phase_match_is_case_insensitive(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """Phase matching does not depend on letter case."""
        from cli.palette_command import PaletteMode

        target = suite_config.sample_index_phases[0]
        result = parser.parse(target.upper(), known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.PHASE
        assert result.phase == target

    def test_malformed_quote_does_not_raise(self, suite_config: PaletteSuiteConfig, parser) -> None:
        """Unterminated quotes degrade gracefully to whitespace split."""
        from cli.palette_command import PaletteMode

        result = parser.parse('"unterminated', known_phases=suite_config.sample_index_phases)
        assert result.mode in {PaletteMode.SEARCH, PaletteMode.OVERVIEW}


class TestPaletteIndexQuery:
    """Behaviour of :class:`PaletteIndexQuery` over a synthetic index."""

    @pytest.fixture
    def query(self, synthetic_index: dict[str, Any]):
        """A fresh query bound to the synthetic index."""
        from cli.palette_command import PaletteIndexQuery

        return PaletteIndexQuery(synthetic_index)

    def test_commands_excludes_duplicates(self, query) -> None:
        """The canonical command list contains no shadowed duplicates."""
        for row in query.commands:
            assert row["duplicate_of"] is None

    def test_phases_returns_sorted(self, query, suite_config: PaletteSuiteConfig) -> None:
        """Phases are returned in deterministic alphabetical order."""
        assert query.phases == sorted(suite_config.sample_index_phases)

    def test_phase_counts_match_phase_buckets(self, query, synthetic_index: dict[str, Any]) -> None:
        """Reported counts equal the unique names per phase bucket."""
        for phase, names in synthetic_index["phase_to_commands"].items():
            assert query.phase_counts[phase] == len(set(names))

    def test_in_phase_filters_to_target(self, query, suite_config: PaletteSuiteConfig) -> None:
        """``in_phase`` returns only commands carrying the target phase."""
        target = suite_config.sample_index_phases[0]
        assert query.in_phase(target)
        assert all(row["phase"] == target for row in query.in_phase(target))

    def test_search_substring_match(self, query, suite_config: PaletteSuiteConfig) -> None:
        """Substring search hits both names and summaries."""
        rows = query.search("alpha", limit=suite_config.synthetic_method_definitions)
        assert len(rows) >= suite_config.synthetic_search_alpha_min_hits

    def test_search_zero_limit_returns_empty(self, query) -> None:
        """Zero limit short-circuits to empty results."""
        assert query.search("alpha", limit=0) == []

    def test_search_negative_limit_returns_empty(self, query) -> None:
        """Negative limit short-circuits to empty results."""
        assert query.search("alpha", limit=-1) == []

    def test_detail_with_prefix(self, query, suite_config: PaletteSuiteConfig) -> None:
        """Detail lookup with the explicit ``do_`` prefix succeeds."""
        prefix = suite_config.do_command_prefix
        entry = query.detail(f"{prefix}rec_alpha")
        assert entry is not None
        assert entry["name"] == f"{prefix}rec_alpha"

    def test_detail_without_prefix(self, query, suite_config: PaletteSuiteConfig) -> None:
        """Detail lookup auto-prefixes when ``do_`` is absent."""
        prefix = suite_config.do_command_prefix
        entry = query.detail("rec_alpha")
        assert entry is not None
        assert entry["name"] == f"{prefix}rec_alpha"

    def test_detail_unknown_returns_none(self, query) -> None:
        """Unknown lookup targets yield ``None`` instead of raising."""
        assert query.detail("zzzzz_xyz") is None

    def test_detail_empty_returns_none(self, query) -> None:
        """Empty lookup target yields ``None``."""
        assert query.detail("") is None


class TestPaletteRenderer:
    """Plain-text formatting of query results."""

    @pytest.fixture
    def renderer(self):
        """A renderer bound to the default config."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        return PaletteRenderer(PaletteRenderConfig())

    def test_overview_lists_every_phase(self, renderer, suite_config: PaletteSuiteConfig) -> None:
        """Overview output mentions every phase passed in."""
        counts = {phase: 1 for phase in suite_config.sample_index_phases}
        out = renderer.render_overview(counts)
        for phase in suite_config.sample_index_phases:
            assert phase in out

    def test_overview_empty_returns_only_header(self, renderer) -> None:
        """Empty input collapses to the configured header line."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        assert renderer.render_overview({}) == cfg.overview_header

    def test_phase_listing_includes_header(self, renderer, suite_config: PaletteSuiteConfig) -> None:
        """Phase listing starts with the configured prefix and target."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        target = suite_config.sample_index_phases[0]
        rows = [{"name": f"{suite_config.do_command_prefix}x", "summary": "X helper."}]
        out = renderer.render_phase(target, rows)
        assert out.startswith(f"{cfg.phase_header_prefix}{target}")
        assert f"{suite_config.do_command_prefix}x" in out

    def test_phase_listing_empty_uses_empty_message(self, renderer, suite_config: PaletteSuiteConfig) -> None:
        """Empty phase listing surfaces the dedicated empty marker."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        out = renderer.render_phase(suite_config.sample_index_phases[0], [])
        assert cfg.phase_empty_message in out

    def test_search_includes_query_in_header(self, renderer) -> None:
        """Search output reflects the query string in the header."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        out = renderer.render_search("nmap", [{"name": "do_nmap", "summary": "nmap helper"}])
        assert "nmap" in out
        assert cfg.search_header_prefix.strip() in out

    def test_search_empty_uses_empty_message(self, renderer) -> None:
        """Empty search surfaces the dedicated empty marker."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        out = renderer.render_search("nmap", [])
        assert cfg.search_empty_message in out

    def test_detail_renders_every_label(self, renderer, suite_config: PaletteSuiteConfig) -> None:
        """Detail view mentions every recorded label of the entry."""
        prefix = suite_config.do_command_prefix
        entry = {
            "name": f"{prefix}x",
            "phase": suite_config.sample_index_phases[0],
            "category": "01. Reconnaissance",
            "source_file": "lazyown.py",
            "line": 100,
            "summary": "X helper.",
        }
        out = renderer.render_detail(entry)
        assert f"{prefix}x" in out
        assert suite_config.sample_index_phases[0] in out
        assert "lazyown.py" in out

    def test_detail_missing_returns_configured_message(self, renderer) -> None:
        """``None`` entry surfaces the configured detail-missing message."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        assert renderer.render_detail(None) == cfg.detail_missing_message


class TestPaletteCompleter:
    """Tab-completion candidate selection."""

    @pytest.fixture
    def completer(self):
        """A completer bound to the default config."""
        from cli.palette_command import PaletteCompleter, PaletteRenderConfig

        return PaletteCompleter(PaletteRenderConfig())

    def test_first_position_offers_phases_and_flags(
        self, completer, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """First-positional completion lists every phase plus flags."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        line = "palette "
        candidates = completer.complete("", line, len(line), synthetic_index)
        for phase in suite_config.sample_index_phases:
            assert phase in candidates
        assert cfg.search_flag in candidates
        assert cfg.info_flag in candidates

    def test_first_position_prefix_filtering(
        self, completer, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """A non-empty prefix narrows the first-positional candidates."""
        target = suite_config.sample_index_phases[0]
        head = target[: max(1, len(target) // 2)]
        line = f"palette {head}"
        candidates = completer.complete(head, line, len(line), synthetic_index)
        assert all(c.startswith(head) for c in candidates)

    def test_second_position_after_phase_lists_phase_commands(
        self, completer, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """After a phase token, position 2 yields phase-scoped names."""
        target = suite_config.sample_index_phases[0]
        line = f"palette {target} "
        candidates = completer.complete("", line, len(line), synthetic_index)
        assert candidates
        for name in candidates:
            assert name.startswith(suite_config.do_command_prefix)

    def test_second_position_after_info_lists_all_commands(self, completer, synthetic_index: dict[str, Any]) -> None:
        """After ``--info``, position 2 lists every canonical command."""
        from cli.palette_command import PaletteRenderConfig

        cfg = PaletteRenderConfig()
        line = f"palette {cfg.info_flag} "
        candidates = completer.complete("", line, len(line), synthetic_index)
        unique_names = {command["name"] for command in synthetic_index["commands"] if command["duplicate_of"] is None}
        assert set(candidates) == unique_names

    def test_third_position_returns_empty(
        self, completer, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """Completion past the phase + query tokens yields nothing."""
        target = suite_config.sample_index_phases[0]
        line = f"palette {target} alpha "
        candidates = completer.complete("", line, len(line), synthetic_index)
        assert candidates == []

    def test_completer_is_data_driven(self, completer) -> None:
        """The completer reflects only the supplied index."""
        custom_index = {
            "commands": [
                {
                    "name": "do_xyz",
                    "phase": "recon",
                    "duplicate_of": None,
                    "summary": "",
                    "category": None,
                    "line": 1,
                    "source_file": "lazyown.py",
                    "class_name": "LazyOwnShell",
                }
            ],
            "phase_to_commands": {"recon": ["do_xyz"]},
        }
        line = "palette recon "
        candidates = completer.complete("", line, len(line), custom_index)
        assert candidates == ["do_xyz"]


class TestPaletteEntryPoint:
    """The top-level :func:`render` dispatcher."""

    def test_overview_when_line_is_empty(self, synthetic_index: dict[str, Any]) -> None:
        """Empty input dispatches to the overview renderer."""
        from cli.palette_command import PaletteRenderConfig, render

        cfg = PaletteRenderConfig()
        assert cfg.overview_header in render(synthetic_index, "")

    def test_phase_when_token_is_known_phase(
        self, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """A single known phase token dispatches to the phase listing."""
        from cli.palette_command import render

        target = suite_config.sample_index_phases[0]
        out = render(synthetic_index, target)
        assert target in out
        assert f"{suite_config.do_command_prefix}rec_alpha" in out

    def test_search_when_token_is_unknown(
        self, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """An unknown token dispatches to fuzzy search."""
        from cli.palette_command import render

        out = render(synthetic_index, "alpha")
        prefix = suite_config.do_command_prefix
        assert f"{prefix}rec_alpha" in out or f"{prefix}exp_alpha" in out

    def test_detail_when_info_flag(self, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig) -> None:
        """The ``--info`` flag dispatches to the detail renderer."""
        from cli.palette_command import PaletteRenderConfig, render

        cfg = PaletteRenderConfig()
        prefix = suite_config.do_command_prefix
        out = render(synthetic_index, f"{cfg.info_flag} {prefix}rec_alpha")
        assert f"{prefix}rec_alpha" in out

    def test_custom_config_overrides_defaults(self, synthetic_index: dict[str, Any]) -> None:
        """Caller-supplied config replaces every default surface string."""
        from cli.palette_command import PaletteRenderConfig, render

        custom = PaletteRenderConfig(overview_header="ALT-HEADER")
        out = render(synthetic_index, "", config=custom)
        assert "ALT-HEADER" in out


class TestLazyOwnWiring:
    """Static verification that ``lazyown.py`` exposes the palette glue."""

    @pytest.fixture(scope="class")
    def src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``lazyown.py``."""
        return suite_config.lazyown_path.read_text(encoding="utf-8")

    def test_required_imports_present(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """Every import that the wiring depends on appears in the file."""
        for line in suite_config.required_lazyown_imports:
            assert line in src, f"missing import: {line}"

    def test_methods_defined_on_lazyown_shell(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """``do_palette`` and ``complete_palette`` belong to ``LazyOwnShell``."""
        tree = ast.parse(src)
        defined: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == suite_config.lazyown_shell_class_name:
                defined.update(
                    child.name for child in node.body if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
        for name in suite_config.expected_lazyown_methods:
            assert name in defined, f"{name} not defined on {suite_config.lazyown_shell_class_name}"

    def test_do_palette_loads_index_and_renders(self, src: str) -> None:
        """``do_palette`` body delegates to the loader and the renderer."""
        body = _extract_method_body(src, "do_palette")
        assert "_load_command_index(" in body
        assert "_render_palette(" in body

    def test_do_palette_handles_index_error(self, src: str) -> None:
        """``do_palette`` body recovers gracefully from a missing index."""
        body = _extract_method_body(src, "do_palette")
        assert "_CommandIndexError" in body

    def test_complete_palette_uses_completer(self, src: str) -> None:
        """``complete_palette`` body delegates to the shared completer instance."""
        body = _extract_method_body(src, "complete_palette")
        assert "_PALETTE_COMPLETER.complete(" in body

    def test_complete_palette_handles_index_error(self, src: str) -> None:
        """``complete_palette`` body returns silently on a missing index."""
        body = _extract_method_body(src, "complete_palette")
        assert "_CommandIndexError" in body


class TestPaletteJsonRenderer:
    """Behaviour of :func:`render_json` and :class:`PaletteJsonRenderer`."""

    def test_overview_when_line_is_empty(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Empty input produces overview mode with phase counts."""
        from cli.palette_command import PaletteMode, render_json

        result = render_json(synthetic_index, "")
        assert suite_config.json_required_keys <= set(result)
        assert result["mode"] == PaletteMode.OVERVIEW.value
        assert result["results"] == []
        assert result["phase_counts"]
        for phase, names in synthetic_index["phase_to_commands"].items():
            assert result["phase_counts"][phase] == len(set(names))

    def test_phase_mode_returns_filtered_rows(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """A known phase token routes to phase mode with the right rows."""
        from cli.palette_command import PaletteMode, render_json

        target_phase = suite_config.sample_index_phases[0]
        result = render_json(synthetic_index, target_phase)
        assert result["mode"] == PaletteMode.PHASE.value
        assert result["phase"] == target_phase
        assert all(row["phase"] == target_phase for row in result["results"])

    def test_phase_mode_with_query_narrows_rows(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Adding a token after the phase filters by name or summary."""
        from cli.palette_command import PaletteMode, render_json

        target_phase = suite_config.sample_index_phases[0]
        result = render_json(synthetic_index, f"{target_phase} alpha")
        assert result["mode"] == PaletteMode.PHASE.value
        assert result["query"] == "alpha"
        assert result["results"]
        assert all("alpha" in row["name"].lower() for row in result["results"])

    def test_search_mode_returns_query_and_hits(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """The ``--search`` flag forces search mode and surfaces hits."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig, render_json

        flag = PaletteRenderConfig().search_flag
        result = render_json(synthetic_index, f"{flag} alpha")
        assert result["mode"] == PaletteMode.SEARCH.value
        assert result["query"] == "alpha"
        assert all(
            "alpha" in row["name"].lower() or "alpha" in (row.get("summary") or "").lower() for row in result["results"]
        )

    def test_detail_mode_returns_single_entry(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """The ``--info`` flag returns a one-element ``results`` list."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig, render_json

        flag = PaletteRenderConfig().info_flag
        target = f"{suite_config.do_command_prefix}rec_alpha"
        result = render_json(synthetic_index, f"{flag} {target}")
        assert result["mode"] == PaletteMode.DETAIL.value
        assert result["target"] == target
        assert len(result["results"]) == 1
        assert result["results"][0]["name"] == target

    def test_detail_mode_unknown_returns_empty_results(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """Unknown detail target yields empty results, not an exception."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig, render_json

        flag = PaletteRenderConfig().info_flag
        result = render_json(synthetic_index, f"{flag} do_definitely_unknown")
        assert result["mode"] == PaletteMode.DETAIL.value
        assert result["results"] == []

    def test_render_json_output_is_serialisable(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """Every documented mode round-trips through ``json.dumps``."""
        from cli.palette_command import PaletteRenderConfig, render_json

        cfg = PaletteRenderConfig()
        for line in ("", "recon", "alpha", f"{cfg.search_flag} alpha", f"{cfg.info_flag} do_rec_alpha"):
            payload = render_json(synthetic_index, line)
            json.dumps(payload)

    def test_palette_json_result_to_dict_matches_schema(
        self,
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Direct construction of :class:`PaletteJsonResult` exposes the schema."""
        from cli.palette_command import PaletteJsonResult, PaletteMode

        result = PaletteJsonResult(mode=PaletteMode.OVERVIEW.value)
        document = result.to_dict()
        assert suite_config.json_required_keys <= set(document)
        assert document["results"] == []
        assert document["phase_counts"] == {}


class TestPaletteViewBuilder:
    """Behaviour of :func:`build_palette_view`."""

    def test_returns_required_top_level_keys(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Every documented context key is present in the result."""
        from cli.palette_command import build_palette_view

        view = build_palette_view(synthetic_index)
        missing = suite_config.view_required_keys - set(view)
        assert missing == set(), f"missing context keys: {sorted(missing)}"

    def test_phase_entries_carry_required_fields(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Each phase descriptor exposes ``id``, ``label`` and ``count``."""
        from cli.palette_command import build_palette_view

        view = build_palette_view(synthetic_index)
        for entry in view["phases"]:
            missing = suite_config.view_phase_required_keys - set(entry)
            assert missing == set(), f"phase {entry} missing {sorted(missing)}"
            assert isinstance(entry["count"], int) and entry["count"] >= 0

    def test_totals_match_canonical_command_count(
        self,
        synthetic_index: dict[str, Any],
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Totals reflect the canonical (deduplicated) command list."""
        from cli.palette_command import build_palette_view

        view = build_palette_view(synthetic_index)
        canonical = [c for c in synthetic_index["commands"] if c["duplicate_of"] is None]
        assert view["totals"]["commands"] == len(canonical)
        assert view["totals"]["phases"] == len(view["phases"])
        assert suite_config.view_totals_required_keys <= set(view["totals"])

    def test_commands_sorted_by_name(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """Command rows are sorted alphabetically for deterministic UI."""
        from cli.palette_command import build_palette_view

        view = build_palette_view(synthetic_index)
        names = [row["name"] for row in view["commands"]]
        assert names == sorted(names)

    def test_phases_ordered_by_kill_chain(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """Known phases appear in the configured kill-chain order."""
        from cli.palette_command import PaletteRenderConfig, build_palette_view

        cfg = PaletteRenderConfig()
        view = build_palette_view(synthetic_index)
        ordered = [p["id"] for p in view["phases"]]
        rank = {phase: idx for idx, phase in enumerate(cfg.overview_phase_order)}
        ranked = [rank[p] for p in ordered if p in rank]
        assert ranked == sorted(ranked)

    def test_unknown_phases_appear_after_known_ones(
        self,
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """Phases not in the kill-chain order land at the bottom alphabetically."""
        from cli.palette_command import PaletteRenderConfig, build_palette_view

        cfg = PaletteRenderConfig()
        index = {
            "commands": [
                {
                    "name": f"{suite_config.do_command_prefix}known",
                    "phase": "recon",
                    "duplicate_of": None,
                    "summary": "",
                    "category": None,
                    "line": 1,
                    "source_file": "lazyown.py",
                    "class_name": suite_config.lazyown_shell_class_name,
                },
                {
                    "name": f"{suite_config.do_command_prefix}custom",
                    "phase": "zzcustom",
                    "duplicate_of": None,
                    "summary": "",
                    "category": None,
                    "line": 2,
                    "source_file": "lazyown.py",
                    "class_name": suite_config.lazyown_shell_class_name,
                },
            ],
            "phase_to_commands": {
                "recon": [f"{suite_config.do_command_prefix}known"],
                "zzcustom": [f"{suite_config.do_command_prefix}custom"],
            },
        }
        view = build_palette_view(index)
        ordered_ids = [p["id"] for p in view["phases"]]
        assert ordered_ids.index("recon") < ordered_ids.index("zzcustom")
        assert "zzcustom" not in cfg.overview_phase_order

    def test_flags_exposed_for_ui_chips(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """Search and info flags are exposed verbatim to the template."""
        from cli.palette_command import PaletteRenderConfig, build_palette_view

        cfg = PaletteRenderConfig()
        view = build_palette_view(synthetic_index)
        assert view["search_flag"] == cfg.search_flag
        assert view["info_flag"] == cfg.info_flag

    def test_custom_view_config_overrides_labels(
        self,
        synthetic_index: dict[str, Any],
    ) -> None:
        """Caller-supplied :class:`PaletteViewConfig` overrides default labels."""
        from cli.palette_command import PaletteViewConfig, build_palette_view

        custom = PaletteViewConfig(page_title="ALT TITLE", page_subtitle="ALT SUBTITLE")
        view = build_palette_view(synthetic_index, view_config=custom)
        assert view["page_title"] == "ALT TITLE"
        assert view["page_subtitle"] == "ALT SUBTITLE"

    def test_empty_index_yields_zero_totals(
        self,
        suite_config: PaletteSuiteConfig,
    ) -> None:
        """An empty index does not raise and reports zero totals."""
        from cli.palette_command import build_palette_view

        view = build_palette_view({"commands": [], "phase_to_commands": {}})
        assert view["totals"]["commands"] == 0
        assert view["totals"]["phases"] == 0
        assert view["commands"] == []


class TestMcpPaletteWiring:
    """Static verification of the MCP ``lazyown_palette`` tool wiring."""

    @pytest.fixture(scope="class")
    def src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of the MCP server module."""
        return suite_config.mcp_path.read_text(encoding="utf-8")

    def test_tool_declared_in_list_tools(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The tool name appears in the declared ``list_tools`` block."""
        assert f'name="{suite_config.mcp_tool_name}"' in src

    def test_input_schema_documents_line_property(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The input schema exposes a ``line`` string property."""
        tool_block = self._tool_declaration_block(src, suite_config.mcp_tool_name)
        assert tool_block, f"tool declaration for {suite_config.mcp_tool_name} not found"
        assert f'"{suite_config.mcp_input_property}"' in tool_block

    def test_dispatcher_branch_present(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """``call_tool`` includes a branch for the palette tool."""
        assert f'name == "{suite_config.mcp_tool_name}"' in src

    def test_dispatcher_branch_imports_render_json(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The dispatcher imports the structured renderer entry point."""
        branch = self._dispatcher_branch(src, suite_config.mcp_tool_name)
        assert branch
        for required in suite_config.mcp_required_imports:
            assert required in branch, f"missing import in dispatcher: {required}"

    def test_dispatcher_branch_handles_missing_index(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The dispatcher returns a structured error when the index is missing."""
        branch = self._dispatcher_branch(src, suite_config.mcp_tool_name)
        assert branch
        assert "_PaletteIndexError" in branch
        assert '"error"' in branch

    def test_dispatcher_branch_calls_render_json(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The dispatcher invokes :func:`render_json` to produce the payload."""
        branch = self._dispatcher_branch(src, suite_config.mcp_tool_name)
        assert branch
        assert "_palette_render_json(" in branch

    @staticmethod
    def _tool_declaration_block(src: str, tool_name: str) -> str:
        """Slice the ``types.Tool`` declaration up to the next sibling tool.

        The MCP tool list is a flat list of ``types.Tool(...)`` calls; we
        scan from the marker to the next top-level ``types.Tool(`` opening
        instead of trying to balance parens inside nested input schemas.
        """
        pattern = re.compile(
            rf'types\.Tool\(\s*name="{re.escape(tool_name)}".*?(?=\n        types\.Tool\(|\n    \])',
            re.DOTALL,
        )
        match = pattern.search(src)
        return match.group(0) if match else ""

    @staticmethod
    def _dispatcher_branch(src: str, tool_name: str) -> str:
        pattern = re.compile(
            rf'name == "{re.escape(tool_name)}":(?P<body>.*?)(?=\n    elif name == "lazyown_|\n    # ──)',
            re.DOTALL,
        )
        match = pattern.search(src)
        return match.group("body") if match else ""


class TestC2PaletteRoute:
    """Static verification of the C2 ``/palette`` route + template."""

    @pytest.fixture(scope="class")
    def src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``lazyc2.py``."""
        return suite_config.lazyc2_path.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def template_src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``templates/palette.html``."""
        if not suite_config.palette_template_path.exists():
            pytest.fail(f"{suite_config.palette_template_path.relative_to(suite_config.repo_root)} is missing.")
        return suite_config.palette_template_path.read_text(encoding="utf-8")

    def test_required_imports_present(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The C2 module imports every helper the route depends on."""
        for required in suite_config.c2_required_imports:
            assert required in src, f"missing import: {required}"

    def test_route_decorator_present(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The route decorator is registered on the Flask app."""
        assert suite_config.c2_route_decorator in src

    def test_route_function_defined(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The route handler function is defined."""
        tree = ast.parse(src)
        function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        assert suite_config.c2_route_function in function_names

    def test_route_uses_requires_auth(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler is gated by ``@requires_auth``."""
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == suite_config.c2_route_function:
                names = []
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        names.append(decorator.id)
                    elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                        names.append(decorator.func.attr)
                assert "requires_auth" in names, f"{node.name} missing @requires_auth"
                return
        pytest.fail(f"{suite_config.c2_route_function} not found in lazyc2.py")

    def test_route_loads_index_and_builds_view(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler delegates to the loader and the view builder."""
        body = _extract_method_body(src, suite_config.c2_route_function)
        assert "_palette_load_index(" in body
        assert "_palette_build_view(" in body

    def test_route_renders_palette_template(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler renders the dedicated palette template."""
        body = _extract_method_body(src, suite_config.c2_route_function)
        assert f"render_template('{suite_config.c2_template_filename}'" in body

    def test_route_handles_missing_index(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler returns a non-200 status when the index is missing."""
        body = _extract_method_body(src, suite_config.c2_route_function)
        assert "_PaletteIndexError" in body
        assert "503" in body

    def test_template_extends_base_layout(self, template_src: str, suite_config: PaletteSuiteConfig) -> None:
        """The palette template extends the shared layout and defines the markers."""
        for marker in suite_config.c2_template_required_markers:
            assert marker in template_src, f"template missing marker: {marker}"

    def test_template_escapes_user_facing_strings(self, template_src: str) -> None:
        """The template renders raw command data through an escape helper.

        The embedded JSON is delivered with ``| safe`` (it is operator-trusted
        data baked at render time) but every per-command field that lands in
        the DOM goes through the JS ``escape`` helper to avoid XSS via
        docstring contents.
        """
        assert "function escape(" in template_src
        assert "innerHTML = rows.join" in template_src


def _build_synthetic_graph() -> dict[str, Any]:
    """Construct a tiny in-memory graphify document for neighbour tests.

    Two ``do_*`` commands share two helpers and one diverges; the file label
    and a noisy ``.cmd()`` callee verify the renderer's exclusion logic.
    """
    return {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"id": "lazyown_do_alpha", "label": "do_alpha()"},
            {"id": "lazyown_do_beta", "label": "do_beta()"},
            {"id": "lazyown_do_gamma", "label": "do_gamma()"},
            {"id": "helper_a", "label": "helper_a()"},
            {"id": "helper_b", "label": "helper_b()"},
            {"id": "helper_c", "label": "helper_c()"},
            {"id": "noise_cmd", "label": ".cmd()"},
            {"id": "lazyown_py", "label": "lazyown.py"},
        ],
        "links": [
            {"source": "lazyown_do_alpha", "target": "helper_a", "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_alpha", "target": "helper_b", "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_alpha", "target": "noise_cmd", "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_alpha", "target": "lazyown_py", "relation": "contains", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_beta", "target": "helper_a", "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_beta", "target": "helper_b", "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_beta", "target": "helper_c", "relation": "uses", "confidence": "EXTRACTED"},
            {"source": "lazyown_do_gamma", "target": "helper_c", "relation": "calls", "confidence": "EXTRACTED"},
        ],
    }


@pytest.fixture
def synthetic_graph() -> dict[str, Any]:
    """In-memory graph used by :class:`TestPaletteGraph`."""
    return _build_synthetic_graph()


class TestPaletteGraphLoader:
    """Behaviour of :mod:`cli.palette_graph`."""

    def setup_method(self) -> None:
        """Reset the LRU cache so each test sees a fresh load."""
        from cli.palette_graph import load_graph

        load_graph.cache_clear()

    def test_load_graph_against_repo_artefact(self, suite_config: PaletteSuiteConfig) -> None:
        """The committed graphify export resolves into a populated index."""
        from cli.palette_graph import load_graph

        if not suite_config.graphify_path.exists():
            pytest.skip(f"{suite_config.graphify_path} not present in this checkout")
        graph = load_graph(str(suite_config.graphify_path))
        assert graph.adjacency
        assert graph.command_to_node
        assert any(name.startswith(suite_config.do_command_prefix) for name in graph.command_to_node)

    def test_missing_graph_raises_graph_index_error(self, tmp_path: Path) -> None:
        """A missing path raises :class:`GraphIndexError`."""
        from cli.palette_graph import GraphIndexError, load_graph

        load_graph.cache_clear()
        with pytest.raises(GraphIndexError):
            load_graph(str(tmp_path / "missing.json"))

    def test_malformed_graph_raises_graph_index_error(self, tmp_path: Path) -> None:
        """Invalid JSON raises :class:`GraphIndexError`."""
        from cli.palette_graph import GraphIndexError, load_graph

        bad = tmp_path / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        load_graph.cache_clear()
        with pytest.raises(GraphIndexError):
            load_graph(str(bad))

    def test_safe_load_graph_returns_none_when_missing(self, tmp_path: Path) -> None:
        """:func:`safe_load_graph` swallows the error and returns ``None``."""
        from cli.palette_graph import load_graph, safe_load_graph

        load_graph.cache_clear()
        assert safe_load_graph(str(tmp_path / "missing.json")) is None

    def test_callees_returns_helpers_only(self, synthetic_graph: dict[str, Any], tmp_path: Path) -> None:
        """``callees`` skips file-typed nodes and excluded noise labels."""
        from cli.palette_graph import callees, load_graph

        path = tmp_path / "g.json"
        path.write_text(json.dumps(synthetic_graph), encoding="utf-8")
        load_graph.cache_clear()
        graph = load_graph(str(path))
        out = callees(graph, "do_alpha")
        assert "helper_a()" in out
        assert "helper_b()" in out
        assert ".cmd()" not in out
        assert "lazyown.py" not in out

    def test_callees_handles_unknown_command(self, synthetic_graph: dict[str, Any], tmp_path: Path) -> None:
        """Unknown command names yield an empty list, not an exception."""
        from cli.palette_graph import callees, load_graph

        path = tmp_path / "g.json"
        path.write_text(json.dumps(synthetic_graph), encoding="utf-8")
        load_graph.cache_clear()
        graph = load_graph(str(path))
        assert callees(graph, "do_no_such_thing") == []

    def test_callees_with_none_graph_is_empty(self) -> None:
        """``callees`` accepts ``None`` (post-graceful-degradation) gracefully."""
        from cli.palette_graph import callees

        assert callees(None, "do_alpha") == []

    def test_related_commands_uses_shared_helpers(self, synthetic_graph: dict[str, Any], tmp_path: Path) -> None:
        """Two commands sharing helpers appear as related; the third does not."""
        from cli.palette_graph import load_graph, related_commands

        path = tmp_path / "g.json"
        path.write_text(json.dumps(synthetic_graph), encoding="utf-8")
        load_graph.cache_clear()
        graph = load_graph(str(path))
        related = related_commands(graph, "do_alpha")
        assert "do_beta" in related
        assert "do_gamma" not in related

    def test_related_commands_with_none_graph_is_empty(self) -> None:
        """``related_commands`` returns an empty list when no graph is loaded."""
        from cli.palette_graph import related_commands

        assert related_commands(None, "do_alpha") == []

    def test_enrich_detail_attaches_calls_and_related(
        self, synthetic_graph: dict[str, Any], tmp_path: Path, suite_config: PaletteSuiteConfig
    ) -> None:
        """:func:`enrich_detail` adds ``calls`` and ``related`` to the entry."""
        from cli.palette_graph import enrich_detail, load_graph

        path = tmp_path / "g.json"
        path.write_text(json.dumps(synthetic_graph), encoding="utf-8")
        load_graph.cache_clear()
        graph = load_graph(str(path))
        entry = {
            "name": f"{suite_config.do_command_prefix}alpha",
            "phase": "recon",
            "summary": "alpha summary",
        }
        enriched = enrich_detail(graph, entry)
        assert enriched is not None
        assert "calls" in enriched and isinstance(enriched["calls"], list)
        assert "related" in enriched and isinstance(enriched["related"], list)

    def test_enrich_detail_passes_through_none(self) -> None:
        """``None`` inputs short-circuit to ``None`` so the renderer can format the missing case."""
        from cli.palette_graph import enrich_detail

        assert enrich_detail(None, None) is None


class TestPaletteDetailEnrichment:
    """Renderers must surface graph-derived ``calls`` and ``related`` lists."""

    def _entry(self, suite_config: PaletteSuiteConfig) -> dict[str, Any]:
        prefix = suite_config.do_command_prefix
        return {
            "name": f"{prefix}alpha",
            "phase": suite_config.sample_index_phases[0],
            "category": "01. Reconnaissance",
            "source_file": "lazyown.py",
            "line": 100,
            "summary": "alpha summary",
            "calls": ["helper_a()", "helper_b()"],
            "related": [f"{prefix}beta", f"{prefix}gamma"],
        }

    def test_text_detail_includes_calls(self, suite_config: PaletteSuiteConfig) -> None:
        """The text detail view embeds the configured ``calls`` row."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        cfg = PaletteRenderConfig()
        out = PaletteRenderer(cfg).render_detail(self._entry(suite_config))
        assert cfg.detail_label_calls in out
        assert "helper_a()" in out

    def test_text_detail_includes_related(self, suite_config: PaletteSuiteConfig) -> None:
        """The text detail view embeds the configured ``related`` row."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        cfg = PaletteRenderConfig()
        prefix = suite_config.do_command_prefix
        out = PaletteRenderer(cfg).render_detail(self._entry(suite_config))
        assert cfg.detail_label_related in out
        assert f"{prefix}beta" in out

    def test_text_detail_truncates_neighbour_list(self, suite_config: PaletteSuiteConfig) -> None:
        """Neighbour lists longer than the configured cap are trimmed."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        cfg = PaletteRenderConfig()
        entry = self._entry(suite_config)
        entry["calls"] = [f"h{i}()" for i in range(cfg.detail_neighbour_max + 5)]
        out = PaletteRenderer(cfg).render_detail(entry)
        assert "h0()" in out
        assert f"h{cfg.detail_neighbour_max + 4}()" not in out

    def test_text_detail_omits_calls_when_empty(self, suite_config: PaletteSuiteConfig) -> None:
        """Absent / empty neighbour lists do not produce label rows."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        cfg = PaletteRenderConfig()
        entry = self._entry(suite_config)
        entry["calls"] = []
        entry["related"] = []
        out = PaletteRenderer(cfg).render_detail(entry)
        assert cfg.detail_label_calls not in out
        assert cfg.detail_label_related not in out

    def test_render_top_level_attaches_neighbour_lists(
        self, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """When graph data is absent the dispatcher still degrades gracefully."""
        from cli.palette_command import PaletteRenderConfig, render

        cfg = PaletteRenderConfig()
        prefix = suite_config.do_command_prefix
        out = render(synthetic_index, f"{cfg.info_flag} {prefix}rec_alpha")
        assert f"{prefix}rec_alpha" in out

    def test_render_json_detail_contains_neighbour_keys(
        self, synthetic_index: dict[str, Any], suite_config: PaletteSuiteConfig
    ) -> None:
        """``render_json`` detail-mode entries always carry the new keys.

        The synthetic index has no matching graph node, so the keys may be
        empty lists; what matters is that the schema is consistent so MCP
        agents can rely on ``calls`` / ``related`` always being present.
        """
        from cli.palette_command import PaletteMode, PaletteRenderConfig, render_json

        cfg = PaletteRenderConfig()
        prefix = suite_config.do_command_prefix
        result = render_json(synthetic_index, f"{cfg.info_flag} {prefix}rec_alpha")
        assert result["mode"] == PaletteMode.DETAIL.value
        assert result["results"]
        entry = result["results"][0]
        assert "calls" in entry
        assert "related" in entry

    def test_build_palette_view_attaches_neighbour_keys(self, synthetic_index: dict[str, Any]) -> None:
        """The web-view payload exposes ``calls``/``related`` for client-side rendering."""
        from cli.palette_command import build_palette_view

        view = build_palette_view(synthetic_index)
        assert view["commands"]
        for entry in view["commands"]:
            assert "calls" in entry
            assert "related" in entry

    def test_build_palette_view_exposes_next_flag(self, synthetic_index: dict[str, Any]) -> None:
        """The view payload exposes the ``--next`` verb for the UI chips."""
        from cli.palette_command import PaletteRenderConfig, build_palette_view

        cfg = PaletteRenderConfig()
        view = build_palette_view(synthetic_index)
        assert view["next_flag"] == cfg.next_flag


class TestPaletteNextMode:
    """``--next`` recommends the phase that follows in the kill-chain order."""

    @pytest.fixture
    def parser(self):
        """A parser bound to the default render config."""
        from cli.palette_command import PaletteArgumentParser, PaletteRenderConfig

        return PaletteArgumentParser(PaletteRenderConfig())

    def test_next_flag_routes_to_next_mode(self, parser, suite_config: PaletteSuiteConfig) -> None:
        """The ``--next`` flag forces next mode."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig

        flag = PaletteRenderConfig().next_flag
        result = parser.parse(f"{flag} recon", known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.NEXT
        assert result.phase == "recon"

    def test_next_flag_without_phase(self, parser, suite_config: PaletteSuiteConfig) -> None:
        """``--next`` without an argument carries a ``None`` phase."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig

        flag = PaletteRenderConfig().next_flag
        result = parser.parse(flag, known_phases=suite_config.sample_index_phases)
        assert result.mode is PaletteMode.NEXT
        assert result.phase is None

    def test_query_next_phase_returns_following_phase(self, synthetic_index: dict[str, Any]) -> None:
        """``next_phase`` resolves the phase after the supplied reference."""
        from cli.palette_command import PaletteIndexQuery, PaletteRenderConfig

        cfg = PaletteRenderConfig()
        query = PaletteIndexQuery(synthetic_index)
        assert query.next_phase("recon", ordering=cfg.overview_phase_order) == "exploit"

    def test_query_next_phase_unknown_returns_none(self, synthetic_index: dict[str, Any]) -> None:
        """An unknown reference phase yields ``None``."""
        from cli.palette_command import PaletteIndexQuery, PaletteRenderConfig

        cfg = PaletteRenderConfig()
        query = PaletteIndexQuery(synthetic_index)
        assert query.next_phase("zzz_unknown", ordering=cfg.overview_phase_order) is None

    def test_query_next_phase_at_end_returns_none(self) -> None:
        """The last configured phase has no successor."""
        from cli.palette_command import PaletteIndexQuery, PaletteRenderConfig

        cfg = PaletteRenderConfig()
        last_phase = cfg.overview_phase_order[-1]
        idx = {
            "commands": [],
            "phase_to_commands": {last_phase: []},
        }
        query = PaletteIndexQuery(idx)
        assert query.next_phase(last_phase, ordering=cfg.overview_phase_order) is None

    def test_render_next_returns_phase_listing(self, synthetic_index: dict[str, Any]) -> None:
        """The text dispatcher prints the next phase header and entries."""
        from cli.palette_command import PaletteRenderConfig, render

        cfg = PaletteRenderConfig()
        out = render(synthetic_index, f"{cfg.next_flag} recon")
        assert cfg.next_header_prefix in out
        assert "exploit" in out

    def test_render_next_empty_returns_message(self) -> None:
        """When no successor exists the renderer surfaces the empty marker."""
        from cli.palette_command import PaletteRenderConfig, render

        cfg = PaletteRenderConfig()
        last_phase = cfg.overview_phase_order[-1]
        idx = {
            "commands": [
                {
                    "name": "do_x",
                    "phase": last_phase,
                    "duplicate_of": None,
                    "summary": "",
                    "category": None,
                    "line": 1,
                    "source_file": "lazyown.py",
                    "class_name": "LazyOwnShell",
                }
            ],
            "phase_to_commands": {last_phase: ["do_x"]},
        }
        out = render(idx, f"{cfg.next_flag} {last_phase}")
        assert cfg.next_empty_message in out

    def test_render_json_next_mode(self, synthetic_index: dict[str, Any]) -> None:
        """``render_json`` returns next mode with the resolved phase."""
        from cli.palette_command import PaletteMode, PaletteRenderConfig, render_json

        cfg = PaletteRenderConfig()
        result = render_json(synthetic_index, f"{cfg.next_flag} recon")
        assert result["mode"] == PaletteMode.NEXT.value
        assert result["phase"] == "exploit"
        assert all(row["phase"] == "exploit" for row in result["results"])

    def test_completer_offers_next_flag_at_first_position(
        self, synthetic_index: dict[str, Any]
    ) -> None:
        """The first-position completion list includes ``--next``."""
        from cli.palette_command import PaletteCompleter, PaletteRenderConfig

        cfg = PaletteRenderConfig()
        completer = PaletteCompleter(cfg)
        line = "palette "
        candidates = completer.complete("", line, len(line), synthetic_index)
        assert cfg.next_flag in candidates

    def test_completer_after_next_offers_phases(self, synthetic_index: dict[str, Any]) -> None:
        """After ``--next`` the completer offers phase identifiers."""
        from cli.palette_command import PaletteCompleter, PaletteRenderConfig

        cfg = PaletteRenderConfig()
        completer = PaletteCompleter(cfg)
        line = f"palette {cfg.next_flag} "
        candidates = completer.complete("", line, len(line), synthetic_index)
        for phase in synthetic_index["phase_to_commands"]:
            assert phase in candidates


class TestC2PaletteApiRoute:
    """Static verification of the JSON ``/api/palette`` endpoint."""

    @pytest.fixture(scope="class")
    def src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``lazyc2.py``."""
        return suite_config.lazyc2_path.read_text(encoding="utf-8")

    def test_route_decorator_present(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The API route decorator is registered on the Flask app."""
        assert suite_config.api_palette_route_decorator in src

    def test_route_function_defined(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler function is defined."""
        tree = ast.parse(src)
        function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        assert suite_config.api_palette_route_function in function_names

    def test_route_uses_requires_auth(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler is gated by ``@requires_auth``."""
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == suite_config.api_palette_route_function:
                names = []
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        names.append(decorator.id)
                    elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                        names.append(decorator.func.attr)
                assert "requires_auth" in names, f"{node.name} missing @requires_auth"
                return
        pytest.fail(f"{suite_config.api_palette_route_function} not found in lazyc2.py")

    def test_route_returns_jsonified_view(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler delegates to the same view builder as the HTML route."""
        body = _extract_method_body(src, suite_config.api_palette_route_function)
        assert "_palette_load_index(" in body
        assert "_palette_build_view(" in body
        assert "jsonify" in body

    def test_route_handles_missing_index(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """A missing index resolves to a JSON 503 instead of an HTML page."""
        body = _extract_method_body(src, suite_config.api_palette_route_function)
        assert "_PaletteIndexError" in body
        assert "503" in body


class TestBaseTemplateOverlay:
    """Static verification of the global Cmd+K / Ctrl+K overlay markup."""

    @pytest.fixture(scope="class")
    def base_src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``templates/base.html``."""
        if not suite_config.base_template_path.exists():
            pytest.fail(f"{suite_config.base_template_path.relative_to(suite_config.repo_root)} is missing.")
        return suite_config.base_template_path.read_text(encoding="utf-8")

    def test_overlay_markup_present(self, base_src: str, suite_config: PaletteSuiteConfig) -> None:
        """Every required overlay element marker is in the template."""
        for marker in suite_config.base_template_required_markers:
            assert marker in base_src, f"missing overlay marker: {marker}"

    def test_overlay_is_authenticated_only(self, base_src: str) -> None:
        """The overlay only renders for logged-in operators."""
        idx = base_src.find('id="lazyown-cmdk-overlay"')
        assert idx >= 0
        prelude = base_src[:idx]
        assert "current_user.is_authenticated" in prelude

    def test_overlay_escapes_command_strings(self, base_src: str) -> None:
        """The client-side renderer routes user-visible fields through an escape helper."""
        assert "function escapeHtml(" in base_src
        assert "list.innerHTML = html" in base_src

    def test_overlay_links_to_full_palette(self, base_src: str) -> None:
        """The overlay footer links back to the full palette view."""
        assert "url_for('palette_view')" in base_src


class TestMcpPaletteDescription:
    """The MCP description must advertise the new modes."""

    @pytest.fixture(scope="class")
    def src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of the MCP server module."""
        return suite_config.mcp_path.read_text(encoding="utf-8")

    def test_description_mentions_next_mode(self, src: str) -> None:
        """The tool description advertises ``--next``."""
        assert "--next" in src

    def test_description_mentions_calls_and_related(self, src: str) -> None:
        """The tool description advertises the new neighbour fields."""
        assert "calls" in src
        assert "related" in src


def _write_synthetic_csv(target: Path) -> None:
    """Materialise a deterministic session-report CSV used by telemetry tests.

    The shape mirrors the real artefact written by
    :meth:`LazyOwnShell.log_command_to_csv` — a single header row followed by
    a chronological sequence of invocations. The fixture covers:

    - repeated invocations (``do_lazynmap`` × 3) for run-count assertions,
    - co-occurrence within the default window (``do_lazynmap`` → ``do_smbclient``),
    - mixed prefixed/non-prefixed forms in the ``command`` column,
    - excluded sentinel verbs (``exit``, blank rows) that must be ignored.
    """
    lines = [
        "start,end,source_ip,source_port,destination_ip,destination_port,domain,subdomain,url,pivot_port,command,args",
        "2026-05-09 09:00:00,2026-05-09 09:00:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,lazynmap,",
        "2026-05-09 09:01:00,2026-05-09 09:01:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,smbclient,",
        "2026-05-09 09:02:00,2026-05-09 09:02:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,lazynmap,",
        "2026-05-09 09:03:00,2026-05-09 09:03:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,smbclient,",
        "2026-05-09 09:04:00,2026-05-09 09:04:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,enum4linux,",
        "2026-05-09 09:05:00,2026-05-09 09:05:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,do_lazynmap,",
        "2026-05-09 09:06:00,2026-05-09 09:06:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,exit,",
        "2026-05-09 09:07:00,2026-05-09 09:07:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,,",
        "2026-05-09 09:08:00,2026-05-09 09:08:01,127.0.0.1,1,1.1.1.1,80,t.htb,d,http://t,1:80,assign,rhost=1.2.3.4",
    ]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture
def synthetic_telemetry_path(tmp_path: Path) -> Path:
    """Yield a path to a freshly-written synthetic telemetry CSV."""
    target = tmp_path / "session.csv"
    _write_synthetic_csv(target)
    return target


@pytest.fixture(autouse=True)
def _reset_telemetry_cache() -> None:
    """Reset the lru_cache so every telemetry test sees its own CSV."""
    try:
        from cli.palette_telemetry import load_telemetry
    except Exception:
        return
    load_telemetry.cache_clear()


class TestPaletteTelemetryLoader:
    """Behavioural CSV parser, recents and co-occurrence."""

    def test_safe_load_returns_empty_index_when_csv_missing(self, tmp_path: Path) -> None:
        """A non-existent CSV degrades to an empty index, never raises."""
        from cli.palette_telemetry import safe_load_telemetry

        result = safe_load_telemetry(str(tmp_path / "nope.csv"))
        assert result is not None
        assert dict(result.stats_by_command) == {}
        assert result.recent_order == ()
        assert dict(result.cooccurrence) == {}

    def test_load_telemetry_counts_invocations(self, synthetic_telemetry_path: Path) -> None:
        """The loader aggregates per-command run counts from the CSV."""
        from cli.palette_telemetry import load_telemetry

        index = load_telemetry(str(synthetic_telemetry_path))
        assert "do_lazynmap" in index.stats_by_command
        assert index.stats_by_command["do_lazynmap"].runs == 3
        assert index.stats_by_command["do_smbclient"].runs == 2

    def test_load_telemetry_normalises_prefix(self, synthetic_telemetry_path: Path) -> None:
        """Both prefixed and non-prefixed CSV entries collapse onto ``do_<verb>``."""
        from cli.palette_telemetry import load_telemetry

        index = load_telemetry(str(synthetic_telemetry_path))
        assert "lazynmap" not in index.stats_by_command
        assert "do_lazynmap" in index.stats_by_command

    def test_load_telemetry_skips_excluded_commands(self, synthetic_telemetry_path: Path) -> None:
        """Sentinel rows (``exit``, blanks) never make it into the index."""
        from cli.palette_telemetry import load_telemetry

        index = load_telemetry(str(synthetic_telemetry_path))
        assert "do_exit" not in index.stats_by_command
        assert "do_" not in index.stats_by_command

    def test_load_telemetry_records_last_seen(self, synthetic_telemetry_path: Path) -> None:
        """``last_seen`` is the most recent timestamp seen for that command."""
        from cli.palette_telemetry import load_telemetry

        index = load_telemetry(str(synthetic_telemetry_path))
        assert index.stats_by_command["do_lazynmap"].last_seen == "2026-05-09 09:05:00"

    def test_recent_order_is_most_recent_first_and_unique(self, synthetic_telemetry_path: Path) -> None:
        """Recents are deduplicated and ordered most-recent-first."""
        from cli.palette_telemetry import load_telemetry, recents

        index = load_telemetry(str(synthetic_telemetry_path))
        names = recents(index)
        assert names[0] == "do_assign"
        assert len(names) == len(set(names))
        assert "do_lazynmap" in names

    def test_cooccurrence_emits_top_followers(self, synthetic_telemetry_path: Path) -> None:
        """Commands following ``do_lazynmap`` within the window are ranked."""
        from cli.palette_telemetry import load_telemetry, runs_after

        index = load_telemetry(str(synthetic_telemetry_path))
        followers = runs_after(index, "do_lazynmap")
        assert "do_smbclient" in followers
        assert followers.index("do_smbclient") <= 1

    def test_cooccurrence_respects_min_count(self, tmp_path: Path) -> None:
        """A pair seen only once never makes it into the result."""
        from cli.palette_telemetry import load_telemetry, runs_after

        target = tmp_path / "session.csv"
        target.write_text(
            "start,command,args\n"
            "2026-05-09 09:00:00,lazynmap,\n"
            "2026-05-09 09:01:00,smbclient,\n",
            encoding="utf-8",
        )
        load_telemetry.cache_clear()
        index = load_telemetry(str(target))
        assert runs_after(index, "do_lazynmap") == []

    def test_command_stats_normalises_lookup_prefix(self, synthetic_telemetry_path: Path) -> None:
        """``command_stats`` accepts both ``do_x`` and ``x`` forms."""
        from cli.palette_telemetry import command_stats, load_telemetry

        index = load_telemetry(str(synthetic_telemetry_path))
        with_prefix = command_stats(index, "do_lazynmap")
        without_prefix = command_stats(index, "lazynmap")
        assert with_prefix is not None
        assert with_prefix == without_prefix

    def test_runs_after_handles_none_telemetry(self) -> None:
        """A ``None`` telemetry index degrades to empty results."""
        from cli.palette_telemetry import command_stats, recents, runs_after

        assert runs_after(None, "do_x") == []
        assert command_stats(None, "do_x") is None
        assert recents(None) == []

    def test_enrich_detail_attaches_runs_and_runs_after(self, synthetic_telemetry_path: Path) -> None:
        """The enrichment helper carries telemetry into a detail entry."""
        from cli.palette_telemetry import enrich_detail, load_telemetry

        index = load_telemetry(str(synthetic_telemetry_path))
        entry = {"name": "do_lazynmap", "phase": "recon", "summary": ""}
        enriched = enrich_detail(index, entry)
        assert enriched is not None
        assert enriched["runs"] == 3
        assert enriched["last_seen"] == "2026-05-09 09:05:00"
        assert "do_smbclient" in enriched["runs_after"]
        assert entry == {"name": "do_lazynmap", "phase": "recon", "summary": ""}

    def test_enrich_detail_passes_through_none(self) -> None:
        """``None`` input remains ``None`` so the renderer can show its message."""
        from cli.palette_telemetry import enrich_detail

        assert enrich_detail(None, None) is None

    def test_load_telemetry_raises_on_unreadable_path(self, tmp_path: Path) -> None:
        """A directory in the CSV slot raises a typed error."""
        from cli.palette_telemetry import TelemetryIndexError, load_telemetry

        target = tmp_path / "session.csv"
        target.mkdir()
        load_telemetry.cache_clear()
        with pytest.raises(TelemetryIndexError):
            load_telemetry(str(target))


class TestPaletteDetailTelemetryRendering:
    """The detail renderer surfaces telemetry rows when available."""

    def test_render_detail_shows_runs_and_runs_after(self) -> None:
        """Run count, last seen and runs-after rows render when populated."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        cfg = PaletteRenderConfig()
        renderer = PaletteRenderer(cfg)
        entry = {
            "name": "do_lazynmap",
            "phase": "recon",
            "category": "01. Reconnaissance",
            "source_file": "lazyown.py",
            "line": 42,
            "summary": "Run nmap.",
            "runs": 7,
            "last_seen": "2026-05-09 09:05:00",
            "runs_after": ["do_smbclient", "do_enum4linux"],
        }
        out = renderer.render_detail(entry)
        assert cfg.detail_label_runs in out
        assert "7" in out
        assert cfg.detail_label_last_seen in out
        assert "2026-05-09 09:05:00" in out
        assert cfg.detail_label_runs_after in out
        assert "do_smbclient" in out

    def test_render_detail_skips_telemetry_rows_when_zero(self) -> None:
        """A command with zero runs hides the telemetry rows entirely."""
        from cli.palette_command import PaletteRenderConfig, PaletteRenderer

        cfg = PaletteRenderConfig()
        renderer = PaletteRenderer(cfg)
        entry = {
            "name": "do_x",
            "phase": "recon",
            "category": "01. Reconnaissance",
            "source_file": "lazyown.py",
            "line": 1,
            "summary": "",
            "runs": 0,
            "last_seen": "",
            "runs_after": [],
        }
        out = renderer.render_detail(entry)
        assert cfg.detail_label_runs not in out.split(cfg.line_separator)
        assert cfg.detail_label_runs_after not in out

    def test_build_palette_view_includes_recents_key(self, synthetic_index: dict[str, Any]) -> None:
        """The view payload exposes a ``recents`` field for the overlay."""
        from cli.palette_command import build_palette_view

        view = build_palette_view(synthetic_index)
        assert "recents" in view
        assert isinstance(view["recents"], list)


class TestC2PaletteApiRateLimit:
    """The JSON catalogue endpoint must be rate-limited."""

    @pytest.fixture(scope="class")
    def src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``lazyc2.py``."""
        return suite_config.lazyc2_path.read_text(encoding="utf-8")

    def test_rate_limit_decorator_present(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The handler is decorated with ``@limiter.limit(...)``."""
        assert suite_config.api_palette_rate_limit_marker in src

    def test_rate_limit_constant_defined(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The rate-limit value is defined as a module-level constant."""
        constant = suite_config.api_palette_rate_limit_constant
        pattern = rf"{re.escape(constant)}\s*="
        assert re.search(pattern, src) is not None, f"missing constant: {constant}"

    def test_rate_limit_falls_back_to_default(self, src: str, suite_config: PaletteSuiteConfig) -> None:
        """The fallback default (``60 per minute``) is wired into the constant."""
        constant = suite_config.api_palette_rate_limit_constant
        idx = src.find(constant)
        assert idx >= 0
        line_end = src.find("\n", idx)
        assert "60 per minute" in src[idx:line_end]


class TestBaseTemplateOverlayTelemetry:
    """The Cmd+K overlay surfaces telemetry without breaking existing markers."""

    @pytest.fixture(scope="class")
    def base_src(self, suite_config: PaletteSuiteConfig) -> str:
        """The full text of ``templates/base.html``."""
        return suite_config.base_template_path.read_text(encoding="utf-8")

    def test_telemetry_markers_present(self, base_src: str, suite_config: PaletteSuiteConfig) -> None:
        """Every required telemetry marker is in the overlay markup."""
        for marker in suite_config.base_template_telemetry_markers:
            assert marker in base_src, f"missing telemetry marker: {marker}"

    def test_score_function_uses_runs_signal(self, base_src: str) -> None:
        """The fuzzy ranker incorporates run counts as a tiebreaker."""
        assert "c.runs" in base_src
        assert "Math.min" in base_src

    def test_recents_section_renders_when_input_empty(self, base_src: str) -> None:
        """The renderer emits a ``recent`` section when no query is typed."""
        assert "recents.length" in base_src
        assert "recent" in base_src.lower()


class TestPaletteEnrichmentBlend:
    """``_enrich_detail_entry`` blends graph and telemetry data."""

    def test_enrichment_returns_entry_when_both_modules_missing(self, monkeypatch) -> None:
        """A double-import failure still returns the original entry untouched."""
        import builtins

        from cli import palette_command

        original_import = builtins.__import__

        def blocking_import(name, *args, **kwargs):
            if name in {"cli.palette_graph", "cli.palette_telemetry"}:
                raise ImportError(f"blocked: {name}")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", blocking_import)
        entry = {"name": "do_x", "phase": "recon", "summary": ""}
        result = palette_command._enrich_detail_entry(entry)
        assert result == entry

    def test_enrichment_passes_through_none(self) -> None:
        """``None`` continues to mean "command not found" downstream."""
        from cli import palette_command

        assert palette_command._enrich_detail_entry(None) is None
