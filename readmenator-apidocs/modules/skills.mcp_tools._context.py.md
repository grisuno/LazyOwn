# `skills.mcp_tools._context`

> Source: [skills/mcp_tools/_context.py:1](../../skills/mcp_tools/_context.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Dependency-injection context handed to every `[`mcp_tools`](skills.lazyown_automapper.py.md#automapper-mcp_tools)` handler.

Each tool module under [`mcp_tools`](skills.lazyown_automapper.py.md#automapper-mcp_tools) is import-pure: it declares a
``TOOL`` schema and a ``handle(arguments, tool_name, ctx)`` function and
imports nothing from the multi-thousand-line ``lazyown_mcp`` runtime. The
runtime builds one [`MCPContext`](#mcpcontext) bundling the shared helpers and
passes it in, so a tool file never imports the runtime and no circular
import can form. New shared helpers are added here as a field when a
migrated tool first needs them, keeping the contract explicit and typed.

## Contents

- **Classes:** [`MCPContext`](#mcpcontext)

## Classes

<a id="mcpcontext"></a>

### `MCPContext`

`class` `dataclass` | [skills/mcp_tools/_context.py:21](../../skills/mcp_tools/_context.py#L21)

Decorators: `@dataclass(frozen=True)`

```python
class MCPContext
```

Shared runtime helpers injected into each tool handler.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`text`](#mcpcontext-text) | `Callable[[str, str], list]` |  | Render `[`content`](skills.lazyown_context.py.md#compactionresult-content)` into the MCP ``TextContent`` envelope for ``tool_name`` (compaction and transcript recording included). |
| [`load_payload`](#mcpcontext-load_payload) | `Callable[[], dict[str, Any]]` |  | Return the current ``payload.json`` as a dict, read fresh so operator edits made via the CLI are always observed. |
| [`save_payload`](#mcpcontext-save_payload) | `Callable[[dict[str, Any]], str]` |  | Persist a payload dict back to ``payload.json`` and return the written path, used by config-mutating tools. |
| [`lazyown_dir`](#mcpcontext-lazyown_dir) | `Path` |  | Absolute path to the LazyOwn repository root, for tools that resolve modules or other repo-relative resources. |
| [`sessions_dir`](#mcpcontext-sessions_dir) | `Path` |  | Absolute path to the ``sessions/`` campaign-state directory, for tools that read or write artefacts there. |
| [`modules_dir`](#mcpcontext-modules_dir) | `Path` |  | Absolute path to the ``modules/`` package directory. |
| [`skills_dir`](#mcpcontext-skills_dir) | `Path` |  | Absolute path to the ``skills/`` directory. |
| [`run_command`](#mcpcontext-run_command) | `Callable[[str, int], str]` |  | Execute one LazyOwn shell command line with a timeout and return its captured output, for tools that drive the CLI. |
| [`c2_request`](#mcpcontext-c2_request) | `Callable[..., dict[str, Any]]` |  | Make an authenticated request to the C2 server (``path``, ``method``, optional ``body``) and return the parsed JSON response, for tools that read beacon or dashboard state. |
| [`get_policy`](#mcpcontext-get_policy) | `Callable[[], Any \| None]` |  | Return the shared policy-integration singleton when the optional policy engine is available, else None, for tools that report command outcomes to the policy layer. |
| [`get_transcript`](#mcpcontext-get_transcript) | `Callable[[], Any \| None]` |  | Return the active transcript recorder or None, for tools that audit spawns or report harness state. |
| [`get_perm_system`](#mcpcontext-get_perm_system) | `Callable[[], Any \| None]` |  | Return the permission system or None. |
| [`get_hooks`](#mcpcontext-get_hooks) | `Callable[[], Any \| None]` |  | Return the hooks runner or None. |
| [`get_claudemd`](#mcpcontext-get_claudemd) | `Callable[[], Any \| None]` |  | Return the loaded CLAUDE.md hierarchy or None. |
| [`job_store`](#mcpcontext-job_store) | `Any` |  | The shared background-job store singleton, so async-run and job-status tools observe the same jobs. |
| [`list_tools`](#mcpcontext-list_tools) | `Callable[[], Any]` |  | The server's async ``list_tools`` coroutine, for tools that search or enumerate the whole catalogue. |
| [`sitrep_recommendations`](#mcpcontext-sitrep_recommendations) | `Callable[..., list]` |  | Return the top campaign recommendations, for session-brief tools. |

---
