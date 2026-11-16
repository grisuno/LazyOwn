"""MCP tool ``lazyown_lazymode_exec``: run one lazymode script.

The core of code mode for LazyOwn. The model writes a script that drives
the framework through the ``lazy`` SDK facade and returns only what
matters, so a task that used to take many tool round-trips becomes one
call and the intermediate output never enters the model context. Python
runs in a bounded subprocess; Lua runs in-process via lupa. The operator
scope posture is enforced inside the runner.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazymode_exec",
    description=(
        "Execute one lazymode script against the LazyOwn SDK facade (the "
        "'lazy' object). Use lazyown_lazymode_search first to discover the "
        "surface. Replaces many tool calls with one script; returns "
        "{backend, ok, result, stdout, error, duration_s}. Python runs in a "
        "bounded subprocess; Lua runs in-process."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "script": {
                "type": "string",
                "description": "Source code. Python sets a 'result' variable; "
                "Lua uses a top-level return and may call log(message).",
            },
            "lang": {
                "type": "string",
                "enum": ["python", "lua"],
                "description": "Runner backend; defaults to python.",
            },
            "timeout": {
                "type": "number",
                "description": "Wall-clock timeout in seconds (python backend).",
            },
        },
        "required": ["script"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Run the script with the selected backend and return its result.

    Args:
        arguments: Tool arguments; ``script``, optional ``lang`` and
            ``timeout``.
        tool_name: The dispatched tool name for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A one-element ``TextContent`` list with the execution result JSON.
    """
    if str(ctx.lazyown_dir) not in sys.path:
        sys.path.insert(0, str(ctx.lazyown_dir))
    from sdk.lazymode import run

    script = str(arguments.get("script", ""))
    lang = str(arguments.get("lang", "python"))
    kwargs: dict[str, Any] = {
        "payload_path": str(ctx.lazyown_dir / "payload.json"),
        "sessions_dir": str(ctx.sessions_dir),
    }
    if lang.strip().lower() == "python" and "timeout" in arguments:
        kwargs["timeout"] = float(arguments["timeout"])
    result = run(script, lang=lang, **kwargs)
    return ctx.text(tool_name, json.dumps(result.to_dict(), indent=2))
