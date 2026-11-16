# lazymode: code mode for LazyOwn

lazymode is programmatic tool calling for LazyOwn (the pattern Cloudflare
calls "code mode"). Instead of the model making many separate MCP tool
calls, it writes one script that drives the framework through a single SDK
facade and returns only what matters. The raw intermediate output (nmap
dumps, searchsploit listings, exploit transcripts) stays inside the script
and never enters the model context.

Two gains:

- Context. The 150+ MCP tool schemas no longer have to sit in context; two
  tools (search and exec) do. Intermediate output is bounded and does not
  round-trip through the context.
- Reliability. A loop of conditional tool calls becomes ordinary control
  flow the model writes in one pass.

## Surfaces

| Component | Path | Role |
|-----------|------|------|
| SDK facade | `sdk/facade.py` (`Lazy`) | Single programmatic surface: `config`, `sessions`, `recon`, `sh`, `search_exploits`. Standalone (no cmd2, no Flask). |
| Runners | `sdk/lazymode/runner.py` | Hybrid: `run_python` (bounded subprocess) and `run_lua` (in-process lupa). Shared `LazymodeResult`. |
| Surface index | `sdk/lazymode/index.py` | Live introspection of the facade for search. |
| MCP search tool | `skills/mcp_tools/lazymode_search.py` | `lazyown_lazymode_search`: discover the callable surface. |
| MCP exec tool | `skills/mcp_tools/lazymode_exec.py` | `lazyown_lazymode_exec`: run one script, return `{backend, ok, result, stdout, error, duration_s}`. |

The two tools live in the one-file-per-tool registry, so they add no
weight to the MCP server module. Full SDK contract: `sdk/README.md` and
`sdk/lazymode/README.md`.

## Workflow

1. `lazyown_lazymode_search("<keywords>")` to find the methods.
2. Write one script against the injected `lazy` object.
3. `lazyown_lazymode_exec(script, lang="python" | "lua")`.
4. Read the returned `result`; on `ok=false`, read `error` and fix.

Python sets a `result` variable; `print` is captured into `stdout`. Lua
uses a top-level `return` and may call `log(message)`; a method returning
a Python list or dict hands Lua a Python object, not a native table, so
for collection work prefer the Python backend.

## Hybrid runners

| Backend | Where | Isolation | State |
|---------|-------|-----------|-------|
| `python` (default) | separate process, CPU + memory + wall-clock bounded | strong (process boundary) | fresh `payload.json` and `sessions/` |
| `lua` | in-process lupa runtime | reuses the native plugin substrate | same facade, live process |

Both build the scope check from the operator payload via
`cli.scope_guard.ScopeGuard`, so a script cannot drive an offensive
operation against an out-of-scope target when the posture is `enforce`
(a denied target is refused in any posture). Session reads are confined
to `sessions/`. Captured stdout is bounded so a chatty command cannot
flood the context.

## Playbooks

A lazymode playbook captures a whole exploitation path (recon-informed
trigger, session, proof) as one administrable asset. `lazymode` is a
playbook action kind (`modules/playbook_admin.PLAYBOOK_ACTION_KINDS`), so
these playbooks are validated and managed by the existing orchestrator
Playbooks tab (`cli/lazy_orchestrator.py`, via `scan_playbooks`). The
focused runner is `modules/lazymode_playbook.py`:

- `list_vector_playbooks()` returns every lazymode playbook.
- `run_playbook(name, target)` runs each `kind: lazymode` step through
  `sdk.lazymode.run`, injecting a validated `target` variable.

Each step's `ok` means the step ran without a Python error; exploit
success is in `result.session_opened`.

Driven from either surface:

- MCP: `lazyown_lazymode_playbook` (action `list` or `run`).
- CLI: `lazymode_pb list | run <name> [target]`.

### Metasploitable 2 vectors

The shipped playbooks live in `playbooks/ms2_*.yaml`. `ms2_vsftpd` is
self-contained (a raw socket trigger of the vsftpd 2.3.4 backdoor,
returning a root shell on 6200). The rest delegate to the framework's
verified exploit specs (`exploits/<id>.yaml`) through
`modules.atomic_exploit_bridge.run_spec`, which drives the persistent
target session, rather than reimplementing the exploit.

| Playbook | Vector spec | Notes |
|----------|-------------|-------|
| `ms2_vsftpd.yaml` | `vsftpd_backdoor` | self-contained socket trigger, root on 6200 |
| `ms2_smb.yaml` | `samba_usermap` | CVE-2007-2447, usermap_script |
| `ms2_distcc.yaml` | `ms2_distcc_exec` | CVE-2004-2687 |
| `ms2_unrealircd.yaml` | `ms2_unrealircd_backdoor` | CVE-2010-2075 |
| `ms2_ingreslock.yaml` | `ms2_ingreslock` | ingreslock backdoor shell |
| `ms2_java_rmi.yaml` | `ms2_java_rmi` | CVE-2011-3556 |
| `ms2_tomcat.yaml` | `ms2_tomcat_manager` | default manager deploy |
| `ms2_postgres.yaml` | `ms2_postgres_default` | default credentials |
| `ms2_mysql.yaml` | `ms2_mysql_root` | passwordless root |

Adding a vector is a new `playbooks/ms2_*.yaml` whose lazymode step loads
and runs the matching verified spec; no new runner or tool code is needed.

## Adding capability

Add methods to the SDK facade (`sdk/facade.py`), not to the runners or the
tools. The search index introspects the facade live, so a new method is
searchable immediately and callable from a script at once.

## Tests

`tests/test_sdk_facade.py`, `tests/test_lazymode_runner.py`,
`tests/test_lazymode_playbook.py`.
