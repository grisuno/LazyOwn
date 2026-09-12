"""Tests for the contract manifest drift checker.

The checker is the CI gate that keeps the documented contract tables and the
public import examples honest. These tests pin the positive case on the real
repository and the negative cases on a synthetic tree.
"""

from __future__ import annotations

from pathlib import Path

from scripts.check_contract_manifest import (
    ManifestConfig,
    _dotted_symbol_exists,
    check_manifest,
)


def test_default_manifest_is_consistent() -> None:
    """The real repository must not report contract drift."""
    assert check_manifest() == []


def test_missing_module_reference_is_reported(tmp_path: Path) -> None:
    """A contract table that cites a missing module is drift."""
    doc = tmp_path / "docs" / "contracts.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        "| Contract | Module | Test |\n|---|---|---|\n| ghost | `modules/ghost.py` | `test_ghost.py` |\n",
        encoding="utf-8",
    )
    (tmp_path / "CORE.md").write_text("# CORE\n", encoding="utf-8")
    config = ManifestConfig(repo_root=tmp_path, docs_with_tables=(Path("docs/contracts.md"),))
    drift = check_manifest(config)
    assert any("modules/ghost.py" in message for message in drift)


def test_missing_public_import_is_reported(tmp_path: Path) -> None:
    """A public import example that names a missing symbol is drift."""
    (tmp_path / "utils.py").write_text("class Config:\n    pass\n", encoding="utf-8")
    (tmp_path / "CORE.md").write_text("```python\nfrom utils import Config, Missing\n```\n", encoding="utf-8")
    config = ManifestConfig(repo_root=tmp_path, docs_with_tables=())
    drift = check_manifest(config)
    assert any("utils.Missing" in message for message in drift)


def test_dotted_symbol_exists_uses_ast_not_import(tmp_path: Path) -> None:
    """Symbol resolution parses the file and never executes it."""
    marker = tmp_path / "side_effect.txt"
    module = tmp_path / "danger.py"
    module.write_text(
        "from pathlib import Path\nPath('side_effect.txt').write_text('ran')\nclass Present:\n    pass\n",
        encoding="utf-8",
    )
    config = ManifestConfig(repo_root=tmp_path, docs_with_tables=())
    assert _dotted_symbol_exists("danger.Present", config) is True
    assert _dotted_symbol_exists("danger.Absent", config) is False
    assert not marker.exists()
