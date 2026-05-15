# cli/commands

cmd2 `CommandSet` subpackage. Each file here defines a `CommandSet` class
that is auto-discovered by `cli/registry.py` and wired into `LazyOwnShell`
at startup. This keeps the main `lazyown.py` free of audit-specific command
logic while still surfacing the commands in the same CLI namespace.

## Files

| File | CommandSet | Commands provided |
|------|-----------|-------------------|
| `audit.py` | `AuditCommandSet` | `fz`, `form`, `status_tail`, `grep_log`, `reload_addons`, `audit_complete_keys` |
| `diagnostics.py` | `DiagnosticsCommandSet` | Framework health checks, version info |
| `_base.py` | `BaseCommandSet` | Shared helpers inherited by all command sets |
| `__init__.py` | — | Package marker; exports the `CommandSet` classes for auto-discovery |

## Adding a command set

1. Create `cli/commands/<name>.py`.
2. Define a class that subclasses `cmd2.CommandSet`.
3. Add `do_*` methods following the same conventions as `lazyown.py` commands.
4. Import and register it in `cli/commands/__init__.py`.
5. `cli/registry.py` picks it up on the next shell start.

Do not place commands here that need `self.params` write-back — those belong
in `lazyown.py` because `CommandSet` instances do not own the params dict.
Read-only inspection and display commands are the right fit for this package.
