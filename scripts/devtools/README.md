# scripts/devtools

Reusable development tools that only an agent or a maintainer needs. They are
not part of the operator surface and they are not imported by the framework at
runtime.

| File | Role |
|------|------|
| `core_smoke.py` | Import and call the public surfaces documented in `CORE.md`. Fails on the first missing name. |
| `command_audit.py` | Boot the shell once and audit every registered command: `help` dispatch for all, invalid-flag parser probes for the `@with_argparser` commands. |

## How it works

`core_smoke.py` reads its expected surface list from `SmokeConfig`, imports
each module, and asserts that every public attribute exists. It then calls a
safe subset: payload generation, value coercion, network validation, a path
join, the kill-chain snapshot, and a SQLite round trip inside a temporary
directory. It never writes to `sessions/`.

Run it from the repository root:

```bash
python3 scripts/devtools/core_smoke.py
python3 scripts/devtools/command_audit.py
```

## Adding a tool

Add one self-contained Python file with a module docstring, a config dataclass,
and a `main` function that returns an exit code. Keep it free of hardcoded
paths and campaign state. Add one row to the table above.
