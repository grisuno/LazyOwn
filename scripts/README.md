# scripts

Build, maintenance, and quality-gate scripts. These run outside the framework,
from the shell, from CI, or from the DEPLOY pipeline, never from within the
LazyOwn CLI.

## Files

| File | Purpose |
|------|---------|
| `build_command_index.py` | Rebuilds `cli/command_index.json` from the `do_*` methods, aliases, addons, and plugins. Run after adding a command, alias, addon, or plugin. |
| `check_contract_manifest.py` | Fails when a contract table or a `CORE.md` public import cites a missing module, test, or symbol. |
| `sync_doc_stats.py` | Rewrites the live counts (commands, MCP tools, addons, plugins, tools) into the docs. `--check` fails CI on drift. |
| `top_tier_check.py` | Hygiene audit: counts, version sync, tracked secrets, release inputs. |
| `generate_sbom.py` | Emits a CycloneDX SBOM from the dependency set without network access. |
| `journal.py` | Appends one entry per unit of work to a GitHub Discussion category. |
| `read_journal.py` | Prints the recent journal entries before a change is written. |
| `mutate.sh` | Runs the curated mutation runners, scoped to the changed files by default, and fails on a survivor. |
| `test_bdd.sh` | Runs the behavior-driven pytest modules, scoped to the changed files by default. |
| `patch_playbook_atomic_ids.py` | Resolves Atomic Red Team IDs in `playbooks/` and `lazyadversaries/` against the local corpus. |
| `update_apt_atomic_ids.py` | Variant of the above focused on APT adversary profiles. |
| `backfill_addon_os_trigger.py` | Backfills the `os` and `trigger` fields on lazyaddons. |
| `activate_migrations.py` | Enables the migrated CommandSet modules. |
| `migrate_commandsets.py`, `migrate_lazyown.py`, `fix_migrated_classes.py` | One-off migration tooling for the command split. |
| `setup_hermes_mcp.sh` | Registers the MCP server with Hermes, resolving the repo path at runtime. |
| `validate_agent_contract.sh` | Checks the agent contract file. |
| `devtools/` | Reusable development tools. See `devtools/README.md`. |
| `__init__.py` | Makes the directory importable as a package. |

## Running the scripts

```bash
python3 scripts/build_command_index.py          # after a new command or addon
python3 scripts/sync_doc_stats.py               # refresh live counts in the docs
python3 scripts/check_contract_manifest.py      # gate: docs vs source
scripts/mutate.sh                               # gate: mutation, scoped
scripts/test_bdd.sh                             # gate: BDD, scoped
python3 -m scripts.read_journal                 # read the journal before writing
bash scripts/setup_hermes_mcp.sh                # register the MCP server
```

The contract, mutation, BDD, and journal gates are documented in
`docs/quality_gates.md`.

## DEPLOY pipeline

`DEPLOY.sh` calls the build and documentation scripts as part of the release
process. Run them manually only when you need to verify output without
creating a release commit.

## Adding a script

Add one self-contained file with a module docstring, a config dataclass for
its constants, and a `main` function that returns an exit code. Keep it free of
hardcoded paths and of campaign state. Add one row to the table above. Every
new directory carries its own `README.md`.
