# mcp_tools

One file per MCP tool. Each module here is a single tool contract: its
JSON schema and its handler, discovered declaratively by the registry and
wired into `skills/lazyown_mcp.py` at import time. This replaces the former
monolith where every schema lived in one multi-thousand-line `list_tools`
literal and every handler in a giant `call_tool` if/elif chain.

## Files

| File | Role |
|------|------|
| `__init__.py` | Discovery + registration: `iter_tool_modules`, `iter_schemas`, `register_handlers`. |
| `_context.py` | `MCPContext`, the dependency-injection bundle handed to every handler. |
| `get_config.py` | Reference tool (`lazyown_get_config`): the template to copy. |

Underscore-prefixed modules (`_context`) are scaffolding and are skipped by
discovery.

## How it works

`skills/lazyown_mcp.py` builds one `MCPContext` from its runtime helpers
(`text`, `load_payload`) and calls `register_handlers(_TOOL_HANDLERS, ctx)`
at import, so discovered tools join the same O(1) dispatch table as the
legacy `@register_handler` tools. `list_tools()` appends `_registry_schemas()`
to its legacy literal, so a new tool file appears in the catalogue with no
edit to the god-file. Discovery failures degrade to an empty list; they
never break tool listing or dispatch.

A tool module imports nothing from `lazyown_mcp`; it takes every dependency
from the injected `ctx`. This keeps the tool files import-pure and makes a
circular import impossible.

## Adding (or migrating) a tool

1. Create `mcp_tools/<verb>_<noun>.py`.
2. Declare the schema:

   ```python
   from mcp import types
   from mcp_tools._context import MCPContext

   TOOL = types.Tool(name="lazyown_<verb>_<noun>", description="...", inputSchema={...})

   def handle(arguments: dict, tool_name: str, ctx: MCPContext) -> list:
       """One-line summary."""
       return ctx.text(tool_name, "...")
   ```

3. If the handler needs a runtime helper not on `MCPContext`, add it as a
   typed field in `_context.py` and pass it from `lazyown_mcp.py` where the
   context is built. Do not import the runtime into the tool file.
4. When migrating an existing tool, delete its legacy `@register_handler`
   function and its `types.Tool(...)` block from `lazyown_mcp.py` in the same
   change. `tests/test_mcp_tools_registry.py` fails if a name is served by
   both paths at once.
5. Run `bash skills/mcp_restart.sh` after editing MCP code.

Async handlers are supported: declare `async def handle(...)` and the
registry wraps it so the dispatch `await`s it.
