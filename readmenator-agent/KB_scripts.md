# Subsystem: scripts

## scripts/__init__.py
- Doc: Repository-side maintenance scripts.
- Layer: utility
- Language: py

## scripts/activate_migrations.py
- Doc: Activate dormant CommandSet migrations.
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
- Doc: One-shot backfill: add ``os`` and ``trigger`` keys to every lazyaddon.
- Layer: utility
- Language: py
- Symbols:
  - `classify_os` (function, line 104) `def classify_os(filename)`
  - `known_trigger` (function, line 121) `def known_trigger(name)`
  - `render_trigger` (function, line 127) `def render_trigger(trigger)`
  - `patch` (function, line 141) `def patch(path)`
  - `main` (function, line 175) `def main()`

## scripts/check_contract_manifest.py
- Doc: Verify that documented contracts still exist on disk.
- Layer: utility
- Language: py
- Symbols:
  - `ManifestConfig` (class, line 34) `class ManifestConfig`
  - `_top_level_names` (method, line 72) `def _top_level_names(path)`
  - `_module_path` (method, line 100) `def _module_path(module, config)`
  - `_dotted_symbol_exists` (method, line 112) `def _dotted_symbol_exists(token, config)`
  - `_iter_table_cells` (method, line 127) `def _iter_table_cells(text)`
  - `_extract_path_tokens` (method, line 138) `def _extract_path_tokens(text, config)`
  - `_resolve_reference` (method, line 154) `def _resolve_reference(token, config)`
  - `_collect_doc_imports` (method, line 163) `def _collect_doc_imports(text)`
  - `check_manifest` (method, line 176) `def check_manifest(config)`
  - `_extract_dotted_tokens` (method, line 209) `def _extract_dotted_tokens(text, config)`
  - `main` (method, line 229) `def main(argv)`
  - `__post_init__` (method, line 53) `def __post_init__(self)`
  - `_resolve` (method, line 58) `def _resolve(self, path)`
- Imported by: `tests/test_contract_manifest.py`

## scripts/fix_migrated_classes.py
- Layer: utility
- Language: py

## scripts/generate_sbom.py
- Doc: Generate a minimal CycloneDX SBOM from the pinned requirements files.
- Layer: utility
- Language: py
- Symbols:
  - `parse_requirement` (function, line 25) `def parse_requirement(line)`
  - `collect_components` (function, line 37) `def collect_components(with_ml)`
  - `project_version` (function, line 68) `def project_version()`
  - `build_sbom` (function, line 74) `def build_sbom(with_ml)`
  - `main` (function, line 92) `def main()`

## scripts/journal.py
- Doc: Read-before-you-write journal over GitHub Discussions.
- Layer: utility
- Language: py
- Symbols:
  - `JournalError` (class, line 48) `class JournalError(RuntimeError)`
  - `JournalConfig` (class, line 53) `class JournalConfig`
  - `_run_git` (method, line 90) `def _run_git(args)`
  - `_git_remote_slug` (method, line 114) `def _git_remote_slug()`
  - `_default_runner` (method, line 124) `def _default_runner(args)`
  - `Journal` (class, line 149) `class Journal`
  - `_build_parser` (method, line 245) `def _build_parser()`
  - `main` (method, line 264) `def main(argv)`
  - `from_git_remote` (method, line 71) `def from_git_remote(cls, remote, category)`
  - `_graphql` (method, line 163) `def _graphql(self, query, variables)`
  - `repo_id` (method, line 184) `def repo_id(self)`
  - `category_id` (method, line 192) `def category_id(self)`
  - `post` (method, line 206) `def post(self, title, body)`
  - `entries` (method, line 223) `def entries(self, limit)`
- Imported by: `scripts/read_journal.py`, `tests/test_journal.py`

## scripts/migrate_commandsets.py
- Doc: Merge _migrated.py CommandSet methods into clean phase modules.
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
- Doc: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.
- Layer: utility
- Language: py
- Symbols:
  - `_category_from_decorator` (function, line 70) `def _category_from_decorator(decorator)`
  - `_indent_level` (function, line 84) `def _indent_level(line)`
  - `extract_method` (function, line 88) `def extract_method(source, node)`
  - `rewrite_globals` (function, line 96) `def rewrite_globals(method_source)`
  - `build_migrated_module` (function, line 124) `def build_migrated_module(phase, category, methods)`
  - `main` (function, line 173) `def main()`
- Imported by: `tests/test_migrate_lazyown_generator.py`

## scripts/mutate.sh
- Doc: Mutation gate for LazyOwn.
- Layer: utility
- Language: sh
- Symbols:
  - `runners` (function, line 29)
  - `changed_sources` (function, line 33)
  - `usage` (function, line 40)

## scripts/patch_playbook_atomic_ids.py
- Doc: Patch APT playbooks: replace placeholder atomic_ids with real technique_ids.
- Layer: utility
- Language: py

## scripts/publish_wiki.sh
- Doc: Publish LazyOwn documentation to the GitHub wiki.
- Layer: utility
- Language: sh
- Symbols:
  - `log` (function, line 37)
  - `fail` (function, line 38)
  - `write_home` (function, line 58)
  - `write_installation` (function, line 92)
  - `write_c2_api` (function, line 150)
  - `write_plugins` (function, line 174)
  - `write_sidebar` (function, line 188)
  - `write_footer` (function, line 207)

## scripts/read_journal.py
- Doc: Print the recent engineering journal before a change is written.
- Layer: utility
- Language: py
- Symbols:
  - `_build_parser` (function, line 19) `def _build_parser()`
  - `main` (function, line 29) `def main(argv)`
- Depends on: `scripts/journal.py`

## scripts/setup_hermes_mcp.sh
- Doc: — register LazyOwn MCP server in Hermes Agent config Usage: bash scripts/setup_hermes_mcp.sh...
- Layer: infrastructure
- Language: sh

## scripts/smoke_onboarding.sh
- Doc: Smoke test for the 5-minute onboarding path.
- Layer: utility
- Language: sh
- Symbols:
  - `check` (function, line 8)

## scripts/sync_doc_stats.py
- Doc: Sync documentation numbers with the live codebase — single source of truth.
- Layer: utility
- Language: py
- Symbols:
  - `canonical_command_count` (function, line 87) `def canonical_command_count(root)`
  - `project_version` (function, line 100) `def project_version(root)`
  - `measure_stats` (function, line 109) `def measure_stats(root)`
  - `render` (function, line 136) `def render(template, stats)`
  - `sync` (function, line 141) `def sync(check, stats, root)`
  - `main` (function, line 165) `def main()`

## scripts/test_bdd.sh
- Doc: Behavior-driven (BDD) suite gate for LazyOwn.
- Layer: testing
- Language: sh
- Symbols:
  - `bdd_modules` (function, line 33)
  - `changed_tests` (function, line 37)

## scripts/top_tier_check.py
- Doc: Top-tier hygiene audit for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `fail` (function, line 23) `def fail(message)`
  - `ok` (function, line 28) `def ok(message)`
  - `count_cli_commands` (function, line 32) `def count_cli_commands()`
  - `count_mcp_tools` (function, line 43) `def count_mcp_tools()`
  - `count_addons` (function, line 48) `def count_addons()`
  - `check_versions` (function, line 52) `def check_versions()`
  - `check_doc_counts` (function, line 70) `def check_doc_counts(commands, mcp, addons)`
  - `check_tracked_secrets` (function, line 81) `def check_tracked_secrets()`
  - `check_release_inputs` (function, line 108) `def check_release_inputs()`
  - `main` (function, line 116) `def main()`

## scripts/update_apt_atomic_ids.py
- Doc: Update APT playbooks with real Atomic Red Team test IDs.
- Layer: utility
- Language: py
- Symbols:
  - `build_technique_index` (function, line 22) `def build_technique_index(atomics_path)`
  - `update_playbooks` (function, line 46) `def update_playbooks(index, playbook_dir)`

## scripts/validate_agent_contract.sh
- Doc: CI validation of the AGENTS.md branching model and coding standards.
- Layer: utility
- Language: sh
- Symbols:
  - `pass` (function, line 23)
  - `fail` (function, line 27)
  - `check` (function, line 32)
  - `check_no_hardcoded_passwords` (function, line 59)
  - `check_no_hardcoded_wordlists` (function, line 74)
