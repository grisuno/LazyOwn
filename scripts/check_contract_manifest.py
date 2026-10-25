#!/usr/bin/env python3
"""Verify that documented contracts still exist on disk.

The repository publishes contract tables and public import examples in its
markdown. Markdown drifts silently when a module is renamed or a test file
is deleted. This script reads the contract tables and the public import
examples and fails when a documented module, test, or public symbol is
missing.

The check is intentionally conservative. It ignores globs, brace
expansions, placeholders, URLs, and session artefacts, because those are
patterns rather than concrete paths.

Usage:
    python3 scripts/check_contract_manifest.py
    python3 scripts/check_contract_manifest.py --verbose
"""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

BACKTICK_RE = re.compile(r"`([^`]+)`")
IMPORT_RE = re.compile(r"^\s*from\s+([A-Za-z_][\w.]*)\s+import\s+(.+)$")
DOTNAME_RE = re.compile(r"^[A-Za-z_][\w]*(\.[A-Za-z_][\w]*)+$")
IMPORT_NAME_RE = re.compile(r"[A-Za-z_][\w]*")


@dataclass
class ManifestConfig:
    """Configuration for the contract manifest check.

    Attributes:
        repo_root: Root of the checkout.
        docs_with_tables: Markdown files whose tables cite modules and tests.
        core_md: Consumer document whose import examples are the public API.
        path_extensions: File suffixes treated as concrete path references.
        skip_substrings: Fragments that mark a token as a pattern, not a path.
        skip_prefixes: Repo-relative prefixes that are runtime state.
    """

    repo_root: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    docs_with_tables: tuple[Path, ...] = ()
    core_md: Path = Path("CORE.md")
    path_extensions: tuple[str, ...] = (".py", ".yaml", ".yml", ".json", ".html", ".md", ".sh", ".lua", ".tool", ".ls")
    skip_substrings: tuple[str, ...] = ("*", "?", "{", "}", "<", ">", "[", "]", " ", "://")
    skip_prefixes: tuple[str, ...] = ("sessions/", "external/", "mutants/")

    def __post_init__(self) -> None:
        """Resolve relative paths against the repository root."""
        self.core_md = self._resolve(self.core_md)
        self.docs_with_tables = tuple(self._resolve(path) for path in self.docs_with_tables)

    def _resolve(self, path: Path) -> Path:
        """Return ``path`` anchored at the repository root when relative."""
        return path if path.is_absolute() else self.repo_root / path


DEFAULT_CONFIG = ManifestConfig(
    docs_with_tables=(
        Path("docs/SECURITY_CONTRACTS.md"),
        Path("docs/killchain_contracts.md"),
        Path("docs/refactor_contracts.md"),
    )
)


def _top_level_names(path: Path) -> set[str]:
    """Return the top-level names defined or imported by a Python file.

    Args:
        path: Path of the Python file to parse.
    Returns:
        The set of class, function, assignment, and import names declared at
        module level. An unparseable file yields an empty set.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(target.id for target in node.targets if isinstance(target, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.Import):
            names.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.update(alias.asname or alias.name for alias in node.names)
    return names


def _module_path(module: str, config: ManifestConfig) -> Path | None:
    """Map a dotted module name to an existing file, if one exists."""
    parts = module.split(".")
    candidate = config.repo_root.joinpath(*parts).with_suffix(".py")
    if candidate.is_file():
        return candidate
    package = config.repo_root.joinpath(*parts) / "__init__.py"
    if package.is_file():
        return package
    return None


def _dotted_symbol_exists(token: str, config: ManifestConfig) -> bool:
    """Return True when the dotted token resolves to a module or member."""
    parts = token.split(".")
    for split in range(len(parts), 0, -1):
        path = _module_path(".".join(parts[:split]), config)
        if path is None:
            continue
        remaining = parts[split:]
        if not remaining:
            return True
        names = _top_level_names(path)
        return all(member in names for member in remaining)
    return False


def _iter_table_cells(text: str) -> list[str]:
    """Return every cell of every markdown table row in ``text``."""
    cells: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells.extend(part.strip() for part in stripped.strip("|").split("|"))
    return cells


def _extract_path_tokens(text: str, config: ManifestConfig) -> set[str]:
    """Return concrete repo-relative path tokens cited by markdown tables."""
    tokens: set[str] = set()
    for cell in _iter_table_cells(text):
        for token in BACKTICK_RE.findall(cell):
            token = token.strip()
            if not token or any(fragment in token for fragment in config.skip_substrings):
                continue
            if token.startswith(config.skip_prefixes):
                continue
            if not token.endswith(config.path_extensions):
                continue
            tokens.add(token)
    return tokens


def _resolve_reference(token: str, config: ManifestConfig) -> Path | None:
    """Resolve a cited path or test name to a file, if it exists."""
    if "/" not in token and (token.startswith("test_") or token.startswith("run_mutation_")):
        candidate = config.repo_root / "tests" / token
    else:
        candidate = config.repo_root / token
    return candidate if candidate.is_file() else None


def _collect_doc_imports(text: str) -> list[tuple[str, str]]:
    """Return ``(module, name)`` pairs from every import example in a doc."""
    pairs: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = IMPORT_RE.match(line)
        if not match:
            continue
        module = match.group(1)
        for name in IMPORT_NAME_RE.findall(match.group(2)):
            pairs.append((module, name))
    return pairs


def check_manifest(config: ManifestConfig = DEFAULT_CONFIG) -> list[str]:
    """Return the list of documented contracts that are missing on disk.

    Args:
        config: Active check configuration.
    Returns:
        Human readable drift messages. An empty list means the manifest is
        consistent with the source.
    """
    drift: list[str] = []
    for doc in config.docs_with_tables:
        if not doc.is_file():
            drift.append(f"{doc.relative_to(config.repo_root)}: documented contract file is missing")
            continue
        text = doc.read_text(encoding="utf-8")
        for token in sorted(_extract_path_tokens(text, config)):
            if _resolve_reference(token, config) is None:
                drift.append(f"{doc.relative_to(config.repo_root)}: reference not found: {token}")

    if not config.core_md.is_file():
        drift.append(f"{config.core_md.relative_to(config.repo_root)}: public surface document is missing")
        return drift

    core_text = config.core_md.read_text(encoding="utf-8")
    for module, name in _collect_doc_imports(core_text):
        if not _dotted_symbol_exists(f"{module}.{name}", config):
            drift.append(f"{config.core_md.name}: public import not found: {module}.{name}")
    for table_token in sorted(_extract_dotted_tokens(core_text, config)):
        if not _dotted_symbol_exists(table_token, config):
            drift.append(f"{config.core_md.name}: public surface not found: {table_token}")
    return drift


def _extract_dotted_tokens(text: str, config: ManifestConfig) -> set[str]:
    """Return dotted identifier tokens from the public surface table.

    File-like tokens such as ``payload.json`` are skipped because they cite
    an artefact, not an importable module.
    """
    tokens: set[str] = set()
    for cell in _iter_table_cells(text):
        for token in BACKTICK_RE.findall(cell):
            token = token.strip()
            if not DOTNAME_RE.match(token):
                continue
            if token.endswith(config.path_extensions):
                continue
            if any(part.isdigit() for part in token.split(".")):
                continue
            tokens.add(token)
    return tokens


def main(argv: list[str] | None = None) -> int:
    """Run the manifest check and return the process exit code.

    Args:
        argv: Optional argument vector. Defaults to ``sys.argv``.
    Returns:
        0 when the manifest is consistent, 1 when drift is detected.
    """
    parser = argparse.ArgumentParser(prog="check_contract_manifest")
    parser.add_argument("--verbose", action="store_true", help="print the checked paths")
    args = parser.parse_args(argv)

    drift = check_manifest()
    if drift:
        for message in drift:
            print(f"[drift] {message}")
        print(f"contract manifest check failed with {len(drift)} finding(s)")
        return 1
    if args.verbose:
        print("checked contract tables in:")
        for doc in DEFAULT_CONFIG.docs_with_tables:
            print(f"  {doc.relative_to(DEFAULT_CONFIG.repo_root)}")
        print(f"  {DEFAULT_CONFIG.core_md.name}")
    print("contract manifest check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
