# scripts

*Community 18 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `scripts` with dominant language py (cohesion 1.00). Central symbols: `_category_from_decorator`, `_indent_level`, `_module_all`, `build_migrated_module`, `extract_method`, `main`, `rewrite_globals`, `test_all_is_static_and_matches_class_name`. Core file: `scripts/migrate_lazyown.py` (6 symbols). Documented purpose: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.  Usage: python3 scripts/migrate_lazyown.py  What it does: 1. Parses lazyown.py.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/migrate_lazyown.py` | py | utility | 6 | yes |
| `tests/test_migrate_lazyown_generator.py` | py | testing | 6 | yes |

## Key Symbols

- `_category_from_decorator` (function, `scripts/migrate_lazyown.py:70`) `def _category_from_decorator(decorator)` - Return the category name from a ``with_category(...)`` decorator.
- `_indent_level` (function, `scripts/migrate_lazyown.py:84`) `def _indent_level(line)`
- `extract_method` (function, `scripts/migrate_lazyown.py:88`) `def extract_method(source, node)` - Return the raw source text of a function definition.
- `rewrite_globals` (function, `scripts/migrate_lazyown.py:96`) `def rewrite_globals(method_source)` - Replace bare module-global names with ``self.params[...]``.
- `build_migrated_module` (function, `scripts/migrate_lazyown.py:124`) `def build_migrated_module(phase, category, methods)` - Return the source text of a migrated ``CommandSet`` module.
- `main` (function, `scripts/migrate_lazyown.py:173`) `def main()`
- `_module_all` (function, `tests/test_migrate_lazyown_generator.py:27`) `def _module_all(source)` - Extract the ``__all__`` literal from ``source`` via AST.
- `test_generated_module_parses` (function, `tests/test_migrate_lazyown_generator.py:57`) `def test_generated_module_parses()`
- `test_all_is_static_and_matches_class_name` (function, `tests/test_migrate_lazyown_generator.py:62`) `def test_all_is_static_and_matches_class_name()`
- `test_compound_phase_title_casing` (function, `tests/test_migrate_lazyown_generator.py:68`) `def test_compound_phase_title_casing()`
- `test_no_unevaluated_fstring_all_literal` (function, `tests/test_migrate_lazyown_generator.py:74`) `def test_no_unevaluated_fstring_all_literal()`
- `test_method_bodies_are_embedded_in_order` (function, `tests/test_migrate_lazyown_generator.py:81`) `def test_method_bodies_are_embedded_in_order()`

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

- `scripts/migrate_lazyown.py`
- `tests/test_migrate_lazyown_generator.py`
