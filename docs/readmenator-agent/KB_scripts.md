# Subsystem: scripts

## scripts/__init__.py
- Layer: utility
- Language: py

## scripts/activate_migrations.py
- Layer: data_access
- Language: py
- Symbols:
  - `MigrationError` (class, line 28) `class MigrationError(Exception)`
  - `find_migrated_sets` (method, line 32) `def find_migrated_sets()`
  - `extract_command_names` (method, line 42) `def extract_command_names(migrated_path)`
  - `find_in_lazyown` (method, line 52) `def find_in_lazyown(command_names)`
  - `remove_from_lazyown` (method, line 62) `def remove_from_lazyown(locations, dry_run)`
  - `activate_migrated_file` (method, line 75) `def activate_migrated_file(migrated_path, dry_run)`
  - `main` (method, line 88) `def main()`

## scripts/backfill_addon_os_trigger.py
- Layer: utility
- Language: py
- Symbols:
  - `classify_os` (function, line 104) `def classify_os(filename)`
  - `known_trigger` (function, line 121) `def known_trigger(name)`
  - `render_trigger` (function, line 127) `def render_trigger(trigger)`
  - `patch` (function, line 141) `def patch(path)`
  - `main` (function, line 175) `def main()`

## scripts/fix_migrated_classes.py
- Layer: utility
- Language: py

## scripts/migrate_commandsets.py
- Layer: utility
- Language: py
- Symbols:
  - `_extract_method_source` (function, line 38) `def _extract_method_source(source, method_name)`
  - `_method_names_from_file` (function, line 52) `def _method_names_from_file(filepath)`
  - `_find_class_end` (function, line 69) `def _find_class_end(source_lines)`
  - `_append_methods` (function, line 83) `def _append_methods(clean_path, methods)`
  - `merge_phase` (function, line 117) `def merge_phase(phase, dry_run)`
  - `main` (function, line 158) `def main()`

## scripts/migrate_lazyown.py
- Layer: utility
- Language: py
- Symbols:
  - `_category_from_decorator` (function, line 70) `def _category_from_decorator(decorator)`
  - `_indent_level` (function, line 84) `def _indent_level(line)`
  - `extract_method` (function, line 88) `def extract_method(source, node)`
  - `rewrite_globals` (function, line 96) `def rewrite_globals(method_source)`
  - `build_migrated_module` (function, line 124) `def build_migrated_module(phase, category, methods)`
  - `main` (function, line 173) `def main()`
- Imported by: `mutants/tests/test_migrate_lazyown_generator.py`, `tests/test_migrate_lazyown_generator.py`

## scripts/patch_playbook_atomic_ids.py
- Layer: utility
- Language: py

## scripts/setup_hermes_mcp.sh
- Layer: infrastructure
- Doc: setup_hermes_mcp.sh — register LazyOwn MCP server in Hermes Agent config Usage: bash scripts/setup_hermes_mcp.sh [--chec
- Language: sh

## scripts/sync_doc_stats.py
- Layer: utility
- Language: py
- Symbols:
  - `canonical_command_count` (function, line 69) `def canonical_command_count(root)`
  - `measure_stats` (function, line 82) `def measure_stats(root)`
  - `render` (function, line 104) `def render(template, stats)`
  - `sync` (function, line 109) `def sync(check, stats, root)`
  - `main` (function, line 133) `def main()`

## scripts/update_apt_atomic_ids.py
- Layer: utility
- Language: py
- Symbols:
  - `build_technique_index` (function, line 22) `def build_technique_index(atomics_path)`
  - `update_playbooks` (function, line 46) `def update_playbooks(index, playbook_dir)`

## scripts/validate_agent_contract.sh
- Layer: utility
- Doc: validate_agent_contract.sh  CI validation of the AGENTS.md branching model and coding standards. Called by .github/workf
- Language: sh
- Symbols:
  - `check` (function, line 23)
