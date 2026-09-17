# Subsystem: scripts

## scripts/__init__.py
- Layer: utility
- Doc: Repository-side maintenance scripts.  Modules in this package are entry points for the developer workflow (index generat
- Language: py

## scripts/activate_migrations.py
- Layer: data_access
- Doc: Activate dormant CommandSet migrations.  Usage: python3 scripts/activate_migrations.py [--dry-run] [--phase <name>]  Sca
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
- Doc: One-shot backfill: add ``os`` and ``trigger`` keys to every lazyaddon.  This script is idempotent. It scans ``lazyaddons
- Language: py
- Symbols:
  - `classify_os` (function, line 104) `def classify_os(filename)`
  - `known_trigger` (function, line 121) `def known_trigger(name)`
  - `render_trigger` (function, line 127) `def render_trigger(trigger)`
  - `patch` (function, line 141) `def patch(path)`
  - `main` (function, line 175) `def main()`

## scripts/check_contract_manifest.py
- Layer: utility
- Doc: Verify that documented contracts still exist on disk.  The repository publishes contract tables and public import exampl
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
- Layer: utility
- Doc: Generate a minimal CycloneDX SBOM from the pinned requirements files.  Stdlib only, no network: parses ``requirements.tx
- Language: py
- Symbols:
  - `parse_requirement` (function, line 25) `def parse_requirement(line)`
  - `collect_components` (function, line 37) `def collect_components(with_ml)`
  - `project_version` (function, line 68) `def project_version()`
  - `build_sbom` (function, line 74) `def build_sbom(with_ml)`
  - `main` (function, line 92) `def main()`

## scripts/journal.py
- Layer: utility
- Doc: Read-before-you-write journal over GitHub Discussions.  I keep a durable engineering journal in a GitHub Discussion cate
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
- Layer: utility
- Doc: Merge _migrated.py CommandSet methods into clean phase modules.  Reads each ``*_migrated.py`` file under ``cli/commands/
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
- Doc: Staged migration script: extract do_* methods from lazyown.py into cli/commands/.  Usage: python3 scripts/migrate_lazyow
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
- Layer: utility
- Doc: Mutation gate for LazyOwn.  The gate runs the curated mutation runners under tests/. Each runner mutates one production 
- Language: sh
- Symbols:
  - `runners` (function, line 29)
  - `changed_sources` (function, line 33)
  - `usage` (function, line 40)

## scripts/patch_playbook_atomic_ids.py
- Layer: utility
- Doc: Patch APT playbooks: replace placeholder atomic_ids with real technique_ids.  This ensures do_atomic_gen can find real A
- Language: py

## scripts/read_journal.py
- Layer: utility
- Doc: Print the recent engineering journal before a change is written.  This is the read half of the read-before-you-write loo
- Language: py
- Symbols:
  - `_build_parser` (function, line 19) `def _build_parser()`
  - `main` (function, line 29) `def main(argv)`
- Depends on: `scripts/journal.py`

## scripts/setup_hermes_mcp.sh
- Layer: infrastructure
- Doc: setup_hermes_mcp.sh — register LazyOwn MCP server in Hermes Agent config Usage: bash scripts/setup_hermes_mcp.sh [--chec
- Language: sh

## scripts/sync_doc_stats.py
- Layer: utility
- Doc: Sync documentation numbers with the live codebase — single source of truth.  Counts are measured from the code itself an
- Language: py
- Symbols:
  - `canonical_command_count` (function, line 82) `def canonical_command_count(root)`
  - `project_version` (function, line 95) `def project_version(root)`
  - `measure_stats` (function, line 104) `def measure_stats(root)`
  - `render` (function, line 131) `def render(template, stats)`
  - `sync` (function, line 136) `def sync(check, stats, root)`
  - `main` (function, line 160) `def main()`

## scripts/test_bdd.sh
- Layer: testing
- Doc: Behavior-driven (BDD) suite gate for LazyOwn.  Every BDD scenario lives in a pytest module whose tests state the Given, 
- Language: sh
- Symbols:
  - `bdd_modules` (function, line 33)
  - `changed_tests` (function, line 37)

## scripts/top_tier_check.py
- Layer: utility
- Doc: Top-tier hygiene audit for LazyOwn.  Fails (exit 1) on any credibility blocker: - version drift between README / pyproje
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
- Layer: utility
- Doc: Update APT playbooks with real Atomic Red Team test IDs.  Scans the Atomic Red Team repository (already cloned by the us
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
