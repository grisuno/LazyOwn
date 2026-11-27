"""Layer-architecture gate: cli -> modules -> core, never upward.

The framework's import direction is a strict layer stack: ``core`` is
the bottom (imports nothing above it), ``modules`` may import ``core``
but not the CLI/C2 surfaces, and ``cli``/entry points may import
everything. Upward imports are the cycles readmenator keeps flagging;
this AST gate fails the build when one appears (including deferred
imports inside functions — they execute at runtime and are still
coupling — and package-relative imports such as ``from ..cli import x``).
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_CORE = "core"
_MODULES = "modules"
_CLI_LAYERS = ("cli", "lazyown", "lazyc2", "utils")

_FORBIDDEN_UPWARD: dict[str, tuple[str, ...]] = {
    _CORE: (_MODULES, *_CLI_LAYERS),
    _MODULES: _CLI_LAYERS,
}

_SKIP_FILES = frozenset(
    {
        # build copies and third-party stubs
        "build",
        "modules_ext",
        "external",
        "graphify-out",
        "mutants",
        ".venv",
    }
)

_SIBLING_PACKAGES = frozenset(
    {
        "lazyownbt",
        "lazyown_mcp_helpers",
        "lazyown_llm",
        "lazyown_parquet_db",
        "lazyown_sdk",
        "ai_model",
    }
)

# Known upward imports pending inversion (fail-soft optional UI
# integrations or documented delegation contracts). The ratchet fails
# on any NEW upward import; entries shrink as each one inverts.
_BASELINE_UPWARD = frozenset(
    {
        # shell-coupled helpers (needs_sudo/sudo_available/resolve_alias/
        # lazyown_set_config/get_credentials/is_exist) still living in the
        # ``utils`` barrel; each entry disappears when the helper moves to
        # its canonical core/modules home.
        "modules/atomic_cli.py",
        "modules/c2_builder.py",
        "modules/chain_runner.py",
        "modules/lazy_runner.py",
        "modules/loop/worker_execution.py",
        "modules/loop/worker_gating.py",
        "modules/purple_sync.py",
        "modules/winbox_gym.py",
        # fail-soft optional UI integrations pending inversion.
        "modules/attack_surface3d.py",
        "modules/chain_loop.py",
        "modules/engage_summary.py",
        "modules/tools/monitor_smoke.py",
        "modules/unified_dashboard.py",
    }
)


def _package_of(relative: Path) -> str:
    """Dotted package path of a repo-relative ``*.py`` file.

    Args:
        relative: Path relative to the repo root (``modules/loop/x.py``).

    Returns:
        The dotted package (``modules.loop``); empty for top-level files.
    """
    parts = relative.parts[:-1]
    return ".".join(parts)


def _imports_of(tree: ast.AST, package: str) -> list[str]:
    """Collect every module name referenced by import statements.

    Absolute imports keep their dotted name; relative imports
    (``from ..cli import x``) resolve against the file's own package so
    upward couplings cannot hide behind a leading dot.

    Args:
        tree: Parsed module AST.
        package: Dotted package of the file being inspected.

    Returns:
        Fully qualified module names referenced by the tree.
    """
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                if node.module:
                    found.append(node.module)
                continue
            base = package.split(".") if package else []
            for _ in range(node.level - 1):
                base.pop() if base else None
            target = ".".join(base + ([node.module] if node.module else []))
            if target:
                found.append(target)
            if node.module is None:
                found.extend(f"{target}.{alias.name}" if target else alias.name for alias in node.names)
    return found


def _python_files(root: Path) -> list[Path]:
    """Yield gate-relevant ``*.py`` files below ``root``.

    Args:
        root: Directory to walk.

    Returns:
        Python files whose path avoids every ``_SKIP_FILES`` segment.
    """
    return [path for path in root.rglob("*.py") if not (_SKIP_FILES & set(path.relative_to(REPO_ROOT).parts))]


def _violations_for(path: Path, layer: str) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        return []
    rel = str(path.relative_to(REPO_ROOT))
    if rel in _BASELINE_UPWARD:
        return []
    hits = []
    package = _package_of(path.relative_to(REPO_ROOT))
    for module_name in _imports_of(tree, package):
        top = module_name.split(".", 1)[0]
        if top in _SIBLING_PACKAGES:
            continue
        if top in _FORBIDDEN_UPWARD[layer]:
            hits.append(f"{rel}: {layer} -> {module_name}")
    return hits


def test_core_never_imports_modules_or_cli() -> None:
    """The bottom layer imports nothing above it."""
    violations: list[str] = []
    for path in _python_files(REPO_ROOT / _CORE):
        violations.extend(_violations_for(path, _CORE))
    assert not violations, "core upward imports:\n" + "\n".join(sorted(violations))


def test_modules_never_import_cli_or_entry_points() -> None:
    """The middle layer never reaches the CLI or the entry-point modules."""
    violations: list[str] = []
    for path in _python_files(REPO_ROOT / _MODULES):
        violations.extend(_violations_for(path, _MODULES))
    assert not violations, "modules upward imports:\n" + "\n".join(sorted(violations))
