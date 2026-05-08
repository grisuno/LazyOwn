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
            "do_shellshock": frozenset({10649, 14427}),
            "do_download_c2": frozenset({24386, 25853}),
        }
    )
    invalid_index_payload: str = "{not json"
    case_sensitive_invariant_phase_index: int = 0

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
