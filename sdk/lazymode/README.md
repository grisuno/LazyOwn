# sdk/lazymode/ — code mode for LazyOwn

lazymode is programmatic tool calling for LazyOwn (Cloudflare calls the
pattern "code mode"). Instead of the model making ten separate MCP tool
round-trips, it writes one script that drives the framework through the
`lazy` SDK facade and returns only what matters. Two wins:

- Context: the 150+ MCP tool schemas no longer have to live in the model
  context; two tools (search + exec) do. Intermediate output (raw nmap,
  searchsploit dumps) stays inside the script and never re-enters context.
- Reliability: a loop of conditional tool calls becomes natural control
  flow the model writes in one pass.

## Files

| File | Role |
|------|------|
| `__init__.py` | Public exports: `run`, `run_python`, `run_lua`, `search`, `build_index`, `LazymodeResult`. |
| `runner.py` | The hybrid runners and the operator scope check built from the payload. |
| `_bootstrap.py` | Subprocess entry point for the Python backend; emits the result envelope after a sentinel. |
| `index.py` | Live introspection of the SDK surface for `lazymode_search`. |

## The two backends (hybrid)

| Backend | Where | Isolation | State it sees |
|---------|-------|-----------|---------------|
| `run_python` | separate process, CPU + memory + wall-clock bounded | strong (process boundary) | fresh `payload.json` + `sessions/` |
| `run_lua` | in-process lupa runtime | lupa (reuses the native plugin substrate) | same facade, live process |

Python is the default: a crash or runaway loop cannot affect the caller.
Lua reuses the Lua runtime LazyOwn already ships for its plugin system,
so it is pure reuse; it starts faster but is less isolated.

## Writing a script

Python (set a `result` variable; `print` is captured):

```python
target = lazy.config.get("rhost")
services = lazy.recon.nmap(target, flags="-sV -T4 -F")
top = [s for s in services if s.get("version")][:5]
result = {"count": len(services), "fingerprints": top}
```

Lua (top-level `return`; the Python methods are bound, so use dot syntax;
`log(message)` records progress). A method returning a Python list or dict
hands Lua a Python object, not a native table, so Lua's `#` and friends do
not apply; for collection work prefer the Python backend:

```lua
log("scanning")
local out = lazy.sh("whoami")
return out
```

## Safety

Both runners build the scope check from the operator payload via
`cli.scope_guard.ScopeGuard`, so a script cannot drive an offensive
operation against an out-of-scope target when the posture is `enforce`
(and a denied target is refused in any posture). Session reads are
confined to `sessions/` by the SDK. The runner boundary bounds CPU,
memory and wall-clock for the Python backend.

## MCP tools

`skills/mcp_tools/lazymode_search.py` (`lazyown_lazymode_search`) and
`skills/mcp_tools/lazymode_exec.py` (`lazyown_lazymode_exec`) are the two
tools that back this surface. They live in the one-file-per-tool registry,
so they add no weight to the MCP server module.

## Adding capability

Add methods to the SDK facade (`sdk/facade.py`), not here. The index
introspects the facade live, so a new method is searchable immediately and
usable from a script with no change to the runners or the tools.
