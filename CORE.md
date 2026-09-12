# CORE.md - LazyOwn for consumers

This file is for an agent or a program that uses LazyOwn as a dependency.
It is not for an agent that edits the repository. If you modify the source,
read `AGENTS.md` and `CLAUDE.md` instead. I keep the three files separate
because each answers a different question and mixing them wastes context.

I wrote this document from the source as it stands. Every name below exists
in the tree today. When the source and this file disagree, the source wins
and this file is a bug.

## What I consider public

The public surface is the set of names in this document. Everything else is
internal and can change without notice. The public names follow Semantic
Versioning in the sense that a breaking change to one of them requires a
major version bump in `pyproject.toml`.

| Surface | Import | Role |
|---------|--------|------|
| Configuration wrapper | `utils.Config`, `utils.load_payload` | Read and write `payload.json` |
| Configuration core | `core.config` | `load_payload`, `save_payload`, `Config`, `resolve_aes_key` |
| Structural protocols | `core.protocols` | `Selector`, `LLMBackend`, `MemoryStore`, `BridgeCatalog`, `OutcomeEvaluator` |
| LLM backends | `modules.llm_factory` | Provider selection, budget proxy, errors |
| SQLite layer | `modules.db` | Workspaces, hosts, services, vulns, creds, loot, notes, nmap import |
| Module catalog | `modules.module_registry` | Discover and search addons, plugins, modules, tools, playbooks |
| Payload factory | `modules.payload_factory` | Generate reverse shells, PowerShell, shellcode |
| Kill chain | `modules.killchain` | Phases, progress, atomic updates |
| World model | `modules.world_model` | Host state machine, credentials, vulnerabilities, context |
| Hardening primitives | `core.hardening` | Path, host, port, filename validation and safe process calls |
| Safe execution | `core.safe_exec` | Injection-resistant command, URL, and file helpers |

## Install

From a checkout:

```sh
python3 -m pip install -e .
```

From PyPI, when the release workflow has published the wheel:

```sh
python3 -m pip install lazyown
```

The console entry point is `lazyown = lazyown:main`. LazyOwn targets Python
3.10 and newer. The full dependency list is heavy because the framework
covers exploitation, C2, and reporting. Install `.[ml]`, `.[dev]`, or the
other extras only when you need them.

## Configuration

`payload.json` in the working directory is the single source of runtime
configuration. Every component reads it. The typed shape lives in
`core.payload_schema` as a `SCHEMA` mapping. I expose three functions there:
`validate_payload` for a whole-file report, `validate_value` for one field,
and `coerce_value` for a safe cast such as a string port to an integer.

Read configuration in process:

```python
from utils import Config, load_payload

params = load_payload()
cfg = Config(params)
print(cfg.rhost)
```

Outside the process, use the same import. Cross-process state travels through
`payload.json` and the `sessions/` directory, never through new ad hoc JSON
files.

## LLM backends

Never instantiate a concrete backend. The factory reads the provider, model,
host, and credentials from `payload.json` and returns the abstract backend,
wrapped by the daily-budget proxy.

```python
from modules.llm_factory import get_llm_backend, try_get_llm_backend

backend = get_llm_backend()
print(backend.complete("You are terse.", "List two open ports."))
```

`get_llm_backend` raises `LLMBackendUnavailableError` when the provider
cannot be built. `try_get_llm_backend` returns `None` instead. Register a new
provider in `modules.llm_factory.SUPPORTED_BACKENDS` after implementing the
`core.protocols.LLMBackend` signature.

## Database layer

`modules.db` gives a workspace-isolated SQLite store with an nmap XML
importer. The table names are fixed and validated against a frozenset, so
callers cannot inject an arbitrary table.

```python
from modules.db import get_db

db = get_db()
workspace_id = db.workspace_create("engagement-1")
host_id = db.host_add(workspace_id, "10.10.11.5", hostname="target")
db.service_add(host_id, port=22, name="ssh", version="OpenSSH 8.2")
print(db.status(workspace_id))
```

One `LazyOwnDB` instance is thread safe. Close it when you are done.

## Module registry

`modules.module_registry` indexes the five extension surfaces. The registry is
a process-wide singleton.

```python
from modules.module_registry import ModuleRegistry

registry = ModuleRegistry.get_instance()
matches = registry.search("smb")
for module in matches:
    print(module.name, module.module_type)
```

`format_module_table` and `format_module_detail` render the catalog for a
terminal.

## Payload factory

`modules.payload_factory` generates payloads without `msfvenom` for the
common combinations and formats them as text, Python, or shellcode.

```python
from modules.payload_factory import PayloadFactory

factory = PayloadFactory()
factory.generate("cmd/unix/reverse_shell", lhost="10.10.14.20", lport=4444)
```

`PayloadFactory.register` extends the catalog with a new `PayloadTemplate`.

## Security primitives

`core.hardening` and `core.safe_exec` are the functions I use before any
filesystem, process, or network boundary. Reuse them instead of writing your
own validation. `safe_path_join` combines a sanitized component with an
allowed directory and rejects a path that escapes it. `safe_run_argv` runs a
list without a shell. `validate_host`, `validate_network_cidr`, and
`validate_port_spec` reject malformed network input. `defused_xml_parse`
parses XML without external entity expansion.

## Kill chain and world model

`modules.killchain` owns the phase definitions and the only write path,
`KillChain.advance_phase`. `modules.world_model` owns the per-host state
machine and persists to `sessions/world_model.json` on every mutation. Read
the kill-chain snapshot instead of deriving phases yourself.

```python
from modules.killchain import KillChain
from modules.world_model import WorldModel, HostState

wm = WorldModel()
wm.add_host("10.10.11.5")
wm.advance_host("10.10.11.5", HostState.SCANNED)
print(KillChain.snapshot())
```

## Protocols for orchestration

If you build a selector, a memory store, or an outcome evaluator for the
autonomous layer, implement the matching `core.protocols` interface. The
orchestrator depends on the Protocol, not on your class, which keeps the
dependency direction correct.

## MCP integration

The Model Context Protocol server lives in `skills/lazyown_mcp.py`. It reuses
the CLI and the C2, so a tool always maps to an existing command or helper.
Start it with `python3 skills/lazyown_mcp.py`, or register it with your MCP
client through `.mcp.json`.

## Versioning and compatibility

`pyproject.toml` holds the version. `version.json` mirrors it for the release
workflow. I publish `dev`, `pp`, and `main` branches; releases are tagged on
`main`. I do not promise compatibility for internal modules. I do promise
that a breaking change to a name in the public table above is a major bump.

## What is internal

`lazyc2.py`, `lazyown.py`, the `cli/` command sets, the `skills/` agents, and
the web templates are entry points and orchestration, not a library. Import
them only if you intend to drive the whole framework. The `modules/legacy/`
package holds old single-purpose scripts that predate the current contracts;
do not depend on it.

## Getting help

Read `QUICKSTART.md` for operator onboarding, `docs/SECURITY_CONTRACTS.md`
for the security invariants, and `AGENTS.md` for the internals if you plan to
contribute. The source of truth is always the code.
