# Lazyaddon Update Specification

I define the opt-in git update contract for lazyaddons.

## Schema

Every `lazyaddons/*.yaml` carries a root `update: true|false` flag. The
shipped catalogue sets `true`. `tool.repo_url` and `tool.install_path`
name the repository and the worktree.

## Contract

`modules/addon_updater.py`:

- `load_addons()` parses YAML with `yaml.safe_load` and reports `update`,
  `repo_url`, `install_path` and `enabled`.
- `update_addon(name, dry_run=False)`:

1. refuses `update: false`;
2. refuses disabled addons and missing `repo_url`;
3. resolves `install_path` inside the repository, rejecting absolute
   paths, `..`, empty paths and the repository root;
4. requires an existing git worktree that is not the LazyOwn tree;
5. refuses a dirty worktree and detached HEAD;
6. runs `git pull --ff-only` without a shell or interactive prompts;
7. records the before/after commit.

- `update_all(names=None, dry_run=False)` deduplicates shared install
  paths, summarizes counts and appends one row to
  `sessions/addon_updates.jsonl`.

CLI: `lazy_addon update [name|--all] [--dry-run]` and
`marketplace update-addons`.

## Acceptance

- All shipped addons declare `update: true`.
- Path traversal and the LazyOwn root are rejected.
- Dirty worktrees are never modified.
- A fast-forward advances the worktree.
- Tests: `tests/test_addon_updater.py`.
- Mutation: `tests/run_mutation_addon_updater.py`.
