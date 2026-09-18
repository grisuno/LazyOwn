# scripts

*Community 16 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `scripts` with dominant language py (cohesion 1.00). Central symbols: `ManifestConfig`, `__post_init__`, `_collect_doc_imports`, `_dotted_symbol_exists`, `_extract_dotted_tokens`, `_extract_path_tokens`, `_iter_table_cells`, `_module_path`. Core file: `scripts/check_contract_manifest.py` (13 symbols). Documented purpose: Verify that documented contracts still exist on disk.  The repository publishes contract tables and public import examples in its markdown. Markdown drifts sile.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/check_contract_manifest.py` | py | utility | 13 | yes |
| `tests/test_contract_manifest.py` | py | testing | 4 | yes |

## Key Symbols

- `ManifestConfig` (class, `scripts/check_contract_manifest.py:34`) `class ManifestConfig` - Configuration for the contract manifest check.
- `__post_init__` (method, `scripts/check_contract_manifest.py:53`) `def __post_init__(self)` - Resolve relative paths against the repository root.
- `_resolve` (method, `scripts/check_contract_manifest.py:58`) `def _resolve(self, path)` - Return ``path`` anchored at the repository root when relative.
- `_top_level_names` (method, `scripts/check_contract_manifest.py:72`) `def _top_level_names(path)` - Return the top-level names defined or imported by a Python file.
- `_module_path` (method, `scripts/check_contract_manifest.py:100`) `def _module_path(module, config)` - Map a dotted module name to an existing file, if one exists.
- `_dotted_symbol_exists` (method, `scripts/check_contract_manifest.py:112`) `def _dotted_symbol_exists(token, config)` - Return True when the dotted token resolves to a module or member.
- `_iter_table_cells` (method, `scripts/check_contract_manifest.py:127`) `def _iter_table_cells(text)` - Return every cell of every markdown table row in ``text``.
- `_extract_path_tokens` (method, `scripts/check_contract_manifest.py:138`) `def _extract_path_tokens(text, config)` - Return concrete repo-relative path tokens cited by markdown tables.
- `_resolve_reference` (method, `scripts/check_contract_manifest.py:154`) `def _resolve_reference(token, config)` - Resolve a cited path or test name to a file, if it exists.
- `_collect_doc_imports` (method, `scripts/check_contract_manifest.py:163`) `def _collect_doc_imports(text)` - Return ``(module, name)`` pairs from every import example in a doc.
- `check_manifest` (method, `scripts/check_contract_manifest.py:176`) `def check_manifest(config)` - Return the list of documented contracts that are missing on disk.
- `_extract_dotted_tokens` (method, `scripts/check_contract_manifest.py:209`) `def _extract_dotted_tokens(text, config)` - Return dotted identifier tokens from the public surface table.
- `main` (method, `scripts/check_contract_manifest.py:229`) `def main(argv)` - Run the manifest check and return the process exit code.
- `test_default_manifest_is_consistent` (function, `tests/test_contract_manifest.py:19`) `def test_default_manifest_is_consistent()` - The real repository must not report contract drift.
- `test_missing_module_reference_is_reported` (function, `tests/test_contract_manifest.py:24`) `def test_missing_module_reference_is_reported(tmp_path)` - A contract table that cites a missing module is drift.
- `test_missing_public_import_is_reported` (function, `tests/test_contract_manifest.py:38`) `def test_missing_public_import_is_reported(tmp_path)` - A public import example that names a missing symbol is drift.
- `test_dotted_symbol_exists_uses_ast_not_import` (function, `tests/test_contract_manifest.py:47`) `def test_dotted_symbol_exists_uses_ast_not_import(tmp_path)` - Symbol resolution parses the file and never executes it.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in scripts changed?
- Should scripts be split, given cohesion 1.00?

## Sources

- `scripts/check_contract_manifest.py`
- `tests/test_contract_manifest.py`
