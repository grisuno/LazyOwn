"""Layer-architecture gate: cli -> modules -> core, never upward.

The framework's import direction is a strict layer stack: ``core`` is
the bottom (imports nothing above it), ``modules`` may import ``core``
but not the CLI/C2 surfaces, and ``cli``/entry points may import
everything. Upward imports are the cycles readmenator keeps flagging;
this AST gate fails the build when one appears (including deferred
imports inside functions — they execute at runtime and are still
coupling).
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_CORE = "core"
_MODULES = "modules"
_CLI_LAYERS = ("cli", "lazyown", "lazyc2")

_FORBIDDEN_UPWARD: dict[str, tuple[str, ...]] = {
    _CORE: (_MODULES, *_CLI_LAYERS),
    _MODULES: _CLI_LAYERS,
}

_SKIP_FILES = {
    # build copies and third-party stubs
    "build",
    "modules_ext",
    "external",
    "graphify-out",
    "mutants",
    ".venv",
}

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
        "modules/attack_surface3d.py",
        "modules/chain_loop.py",
        "modules/engage_summary.py",
        "modules/lazy_runner.py",
        "modules/tools/monitor_smoke.py",
        "modules/unified_dashboard.py",
    }
)


def _top_level(name: str) -> str:
    return name.split(".", 1)[0]


def _imports_of(tree: ast.AST) -> list[str]:
    """Collect every module name referenced by import statements."""
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.append(node.module)
    return found


def _violations_for(path: Path, layer: str) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        return []
    rel = str(path.relative_to(REPO_ROOT))
    if rel in _BASELINE_UPWARD:
        return []
    hits = []
    for module_name in _imports_of(tree):
        top = _top_level(module_name)
        if top in _SIBLING_PACKAGES:
            continue
        if top in _FORBIDDEN_UPWARD[layer]:
            hits.append(f"{rel}: {layer} -> {module_name}")
    return hits


def test_core_never_imports_modules_or_cli() -> None:
    """The bottom layer imports nothing above it."""
    violations: list[str] = []
    for path in (REPO_ROOT / _CORE).rglob("*.py"):
        violations.extend(_violations_for(path, _CORE))
    assert not violations, "core upward imports:\n" + "\n".join(sorted(violations))


def test_modules_never_import_cli_or_entry_points() -> None:
    """The middle layer never reaches the CLI or the entry-point modules."""
    violations: list[str] = []
    for path in (REPO_ROOT / _MODULES).rglob("*.py"):
        violations.extend(_violations_for(path, _MODULES))
    assert not violations, "modules upward imports:\n" + "\n".join(sorted(violations))
