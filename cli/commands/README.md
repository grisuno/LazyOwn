# cli/commands

cmd2 `CommandSet` subpackage. Each file here defines a `CommandSet` class
that is auto-discovered by `cli/registry.py` and wired into `LazyOwnShell`
at startup. The package hosts both the active diagnostic / audit helpers
and the phase-scoped migration targets that gradually replace the legacy
`do_*` methods still living in `lazyown.py`.

## Files

| File | CommandSet | Status | Commands provided |
|------|-----------|--------|-------------------|
| `_base.py` | `LazyOwnCommandSet` | scaffolding | Shared base. Forwards unknown attribute reads to the bound shell (`self._cmd`) so migrated methods reference `self.params`, `self.scripts`, `self.run_script`, ... verbatim. |
| `_dormancy.py` | `PendingCommandSet` | scaffolding | Marker base class. Subclasses are discovered but skipped by `register_command_sets`, so the migrated modules coexist with the legacy `do_*` methods on `LazyOwnShell`. |
| `audit.py` | `AuditCommandSet` | active | `fz`, `form`, `status_tail`, `grep_log`, `reload_addons`, `audit_complete_keys`. |
| `diagnostics.py` | `DiagnosticsCommandSet` | active | Framework health checks, version info. |
| `ai.py` | `AiCommandSet` | pending | `do_ask`, `do_groq`, `do_ai_playbook`, `do_ai_toggle`. |
| `privilege_escalation.py` | `PrivilegeEscalationCommandSet` | pending | `do_sudo`, `do_smbserver`, `do_responder`, `do_linpeas`, `do_winpeas`, `do_les`, `do_suid_check`, `do_pspy`, `do_gtfo`. |
| `exfiltration.py` | `ExfiltrationCommandSet` | pending | `do_encrypt`, `do_decrypt`, `do_evilwinrm`, `do_secretsdump`, `do_getuserspns`, `do_gitdumper`, `do_evidence`, `do_getadusers`, `do_adgetpass`, `do_samdump2`, `do_reg_py`, `do_unzip`, `do_getnthash_py`, `do_upload_gofile`, `do_rsync`, `do_gmsadumper`, `do_dploot`, `download_file_from_c2` (helper), `do_download_c2`. |
| `__init__.py` | — | scaffolding | Package marker. |

## How it works

`cli/registry.py` walks the package with `pkgutil.iter_modules`,
imports each non-underscore submodule, and yields every concrete
`CommandSet` subclass declared inside (`iter_command_sets`).

`register_command_sets(shell)` instantiates each discovered class and
calls `shell.register_command_set(instance)`, but it skips classes
flagged via `cli.commands._dormancy.is_pending(...)`. The two
mechanisms together produce a single contract:

* Tests can inspect every set, including pending ones, by iterating
  `iter_command_sets()`.
* The live shell only registers the active sets, so the legacy `do_*`
  methods in `lazyown.py` remain authoritative until the migration
  prompt that deletes them.

## Migration roadmap

The legacy `LazyOwnShell` class still hosts hundreds of `do_*` methods
distributed across the cmd2 category strings declared in
`utils.py` (canonical) and `modules/categories.py`. The full plan
mirrors the `SHORT_TO_CATEGORY` mapping:

| Phase | Status | Target module | Original count |
|-------|--------|---------------|----------------|
| `ai` | done (pending) | `ai.py` | 4 |
| `privesc` | done (pending) | `privilege_escalation.py` | 9 |
| `exfil` | done (pending) | `exfiltration.py` | 20 (1 duplicate consolidated) |
| `reporting` | planned | `reporting.py` | 24 |
| `c2` | planned | `command_and_control.py` | 25 |
| `lateral` | planned | `lateral_movement.py` | 28 |
| `persistence` | planned | `persistence.py` | 30 |
| `credential` | planned | `credential_access.py` | 31 |
| `recon` | planned | `recon.py` | 37 |
| `post` | planned | `post_exploitation.py` | 45 |
| `exploit` | planned | `exploitation.py` | 60 |
| `scanning` | planned | `scanning.py` | 82 |
| `misc` | planned | `miscellaneous.py` | 87 |

Each pending module:

* Inherits from `PendingCommandSet` while the original methods remain
  in `lazyown.py`.
* Owns its category constants imported from `utils.py` (the canonical
  source).
* Declares module-level constants for paths, default values and other
  literals previously inlined inside the methods, so the migrated
  code carries no magic numbers and centralises configurable defaults
  for the future `payload.json` lookups.
* Re-uses the shared validators (`check_rhost`, `check_lhost`, ...)
  and printers (`print_msg`, `print_warn`, `print_error`) from
  `utils.py` so the runtime behaviour stays identical when the
  legacy copies are eventually deleted.

## Activating a pending set

1. Delete the equivalent `do_*` methods from `lazyown.py`. Keep the
   bridge catalog / phase guides in sync.
2. Edit the pending module: change the base class from
   `PendingCommandSet` to `LazyOwnCommandSet`.
3. Restart the shell (`./run`) or the MCP server
   (`bash skills/mcp_restart.sh`). The active set joins the cmd2
   namespace automatically.

`tests/test_command_set_migration.py` enforces the invariants during
the migration window: pending sets must mirror every legacy method
they replace, the legacy methods must still exist in `lazyown.py`, and
the migrated module bodies must not contain emoji or `TODO`/`FIXME`
markers.

## Adding a brand-new command set (active, non-migration)

1. Create `cli/commands/<name>.py`.
2. Subclass `cli.commands._base.LazyOwnCommandSet`.
3. Declare `phase` and `category`, then add `do_*` methods.
4. `cli/registry.py` picks it up on the next shell start. No registration
   bookkeeping is needed.

Do not place new commands here when they need to write back to
`payload.json` outside `do_assign` / `do_set`. Those mutations belong on
`LazyOwnShell` because the CommandSet base intentionally only forwards
attribute reads.
