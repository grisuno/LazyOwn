# sdk/ — LazyOwn programmatic SDK

The single, stable, standalone facade over the framework. One lazymode
script imports `Lazy` and does in one call what used to take many
separate MCP tool round-trips. The facade composes the lower layers
(`core` config and process primitives, `modules` parsers) behind a small
typed surface and never imports the CLI shell or the Flask C2, so it
boots in a fresh subprocess without the cmd2/Flask startup cost.

This directory is the home of the "evolve to an SDK" effort: the MCP tool
layer and, over time, the CLI are migrated to consume `Lazy` so the same
operation is implemented once here instead of duplicated per surface.

## Files

| File | Role |
|------|------|
| `__init__.py` | Public exports: `Lazy` and the SDK error types. |
| `facade.py` | `Lazy` facade and its namespaces (`config`, `sessions`, `recon`, `sh`, `search_exploits`). |
| `errors.py` | Typed errors: `SdkError`, `ScopeBlocked`, `ConfigValidationError`, `SessionPathError`. |
| `lazymode/` | The lazymode code runners (Python subprocess + Lua in-process) and the API index for tool search. |

## How it works

`Lazy` exposes namespaces:

- `lazy.config` — read and write `payload.json`, writes coerced and
  validated against the payload schema before persisting.
- `lazy.sessions` — list and read campaign artefacts. Every name goes
  through a whitelist filter plus an `os.path.realpath` prefix check, so
  a name cannot escape the sessions directory.
- `lazy.recon` — run and parse nmap against a scope-checked target.
- `lazy.sh(command)` — escape hatch for a single shell command.
- `lazy.search_exploits(query)` — searchsploit lookup.

Two dependencies are injected so the surface is testable and safe:

- `command_runner` — returns combined captured output. Defaults to
  `core.process.run_command`; tests pass a fake so no process runs.
- `scope_check(command, target)` — raises `ScopeBlocked` for an
  out-of-scope target. The facade is fail-open: when no check is injected
  the scope guard is dormant. The lazymode runner builds the real check
  from the operator's `scope` / `scope_enforcement` payload posture.

## Adding a namespace

Add a small API class in `facade.py` (constructor takes only the
dependencies it needs: the sessions directory, the injected runner, the
scope check), wire it as an attribute in `Lazy.__init__`, and reuse an
existing `core` or `modules` primitive rather than reimplementing one.
Offensive helpers must call `scope_check` before executing. Add a
behaviour test per method to `tests/test_sdk_facade.py`.
