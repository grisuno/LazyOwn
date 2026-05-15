# scripts

Build and maintenance scripts. These run outside the framework — from the
shell, from CI, or from the DEPLOY pipeline — not from within the LazyOwn
CLI.

## Files

| File | Purpose |
|------|---------|
| `build_command_index.py` | Rebuilds `cli/command_index.json` by scanning all `do_*` methods in `lazyown.py`, aliases in `cli/aliases.yaml`, addons in `lazyaddons/*.yaml`, and plugins in `plugins/`. Run after adding any new command or addon. |
| `patch_playbook_atomic_ids.py` | Resolves Atomic Red Team test IDs in `playbooks/*.yaml` and `lazyadversaries/*.yaml` against the local `external/atomic-red-team/` corpus. Fixes missing or outdated `atomic_id` fields. |
| `update_apt_atomic_ids.py` | Variant of the above focused on APT adversary profiles in `lazyadversaries/`. Adds new Atomic test mappings when the upstream corpus is updated. |
| `__init__.py` | Makes the directory importable as a package so scripts can use relative imports. |

## Running the scripts

```bash
# Rebuild the command index after adding a command, addon, or plugin
python scripts/build_command_index.py

# Fix Atomic Red Team test IDs in playbooks
python scripts/patch_playbook_atomic_ids.py

# Update APT profiles with new Atomic mappings
python scripts/update_apt_atomic_ids.py
```

## DEPLOY pipeline

`DEPLOY.sh` calls these scripts automatically as part of the release process.
Run them manually only when you need to verify output without creating a
release commit.
