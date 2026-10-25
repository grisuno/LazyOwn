#!/usr/bin/env python3
"""Call one LazyOwn MCP tool over stdio and print its text content.

Reusable hermes-style client used by operators, agents and tests:

    python3 scripts/mcp_call.py lazyown_campaign_sitrep '{"format":"json"}'
    python3 scripts/mcp_call.py lazyown_run_command \
        '{"command":"list","timeout":60}' --timeout 120

The MCP server is spawned from the repository that ships this script. The
interpreter is resolved portably: the first project virtualenv found
(``env``, ``venv``, ``.venv``) wins, otherwise the running interpreter is
reused. No user-specific absolute paths are ever written here. Parent
environment variables (``AUTO_USE_LLM``, ``AUTO_USE_SWAN``, credentials)
flow to the server subprocess unchanged, so the caller controls engine
toggles from the outside.

Exit codes: 0 tool answer printed, 1 tool answered with isError, 2 usage
error, 3 the ``mcp`` package is missing, 4 timeout or transport failure,
5 server-side exception relayed.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SERVER_RELATIVE_PATH = Path("skills") / "lazyown_mcp.py"
_VENV_CANDIDATES = ("env", "venv", ".venv")
_EXIT_OK = 0
_EXIT_TOOL_ERROR = 1
_EXIT_USAGE = 2
_EXIT_NO_MCP = 3
_EXIT_TRANSPORT = 4
_EXIT_NO_CONTENT = 5


class _ToolAnswer:
    """Normalized MCP tool answer."""

    def __init__(self, text: str, is_error: bool) -> None:
        self.text = text.strip()
        self.is_error = is_error


@dataclass(frozen=True)
class _LoopSettings:
    """Invocation container shared by the executor."""

    name: str
    arguments: dict
    timeout_sec: float
    stderr_file: Path | None


def _server_command() -> list[str]:
    """Resolve the interpreter and server path for the stdio subprocess.

    Returns:
        argv list shaped ``[interpreter, server_script]``.

    Raises:
        RuntimeError: If the server script is missing from the repo copy.
    """
    server_path = REPO_ROOT / SERVER_RELATIVE_PATH
    if not server_path.is_file():
        raise RuntimeError(f"missing MCP server script: {server_path}")
    for candidate in _VENV_CANDIDATES:
        interpreter = REPO_ROOT / candidate / "bin" / "python"
        if interpreter.is_file():
            return [str(interpreter), str(server_path)]
    return [sys.executable, str(server_path)]


def _parse_arguments(raw: str) -> dict:
    """Parse the JSON tool arguments payload.

    Args:
        raw: Literal JSON object string (empty string parses as empty dict).

    Returns:
        Parsed mapping handed to the MCP tool.

    Raises:
        ValueError: If the payload is not a JSON object.
    """
    if not raw.strip():
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("tool arguments must be a JSON object")
    return parsed


def _extract_answer(result) -> _ToolAnswer:
    """Collate MCP tool result content into one answer object.

    Args:
        result: ``CallToolResult`` returned by the client session.

    Returns:
        Normalized answer with concatenated text and the error flag.
    """
    parts: list[str] = []
    for item in result.content:
        text = getattr(item, "text", None)
        parts.append(text if text is not None else repr(item))
    return _ToolAnswer("\n".join(parts), bool(result.isError))


async def _call_once(settings: _LoopSettings, command: list[str]) -> _ToolAnswer:
    """Spawn the server, initialize the session and run one tool call.

    Args:
        settings: Parsed invocation settings.
        command: Resolved server argv.

    Returns:
        Normalized tool answer.

    Raises:
        TimeoutError: When the call exceeds the configured budget.
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    errlog = None
    if settings.stderr_file is not None:
        settings.stderr_file.parent.mkdir(parents=True, exist_ok=True)
        errlog = settings.stderr_file.open("w", encoding="utf-8", errors="replace")
    params = StdioServerParameters(command=command[0], args=command[1:], cwd=str(REPO_ROOT))
    try:
        async with stdio_client(params, errlog=errlog if errlog is not None else sys.stderr) as streams:
            read_stream, write_stream = streams
            async with ClientSession(read_stream, write_stream) as session:
                await asyncio.wait_for(session.initialize(), timeout=settings.timeout_sec)
                result = await asyncio.wait_for(
                    session.call_tool(settings.name, settings.arguments),
                    timeout=settings.timeout_sec,
                )
                return _extract_answer(result)
    finally:
        if errlog is not None:
            errlog.close()


def _build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser.

    Returns:
        Configured parser with tool, arguments, timeout and stderr options.
    """
    parser = argparse.ArgumentParser(
        prog="mcp_call",
        description="Call one LazyOwn MCP tool and print its answer.",
    )
    parser.add_argument("tool", help="Registered MCP tool name (see skills/lazyown.md)")
    parser.add_argument("arguments", nargs="?", default="{}", help="JSON object with tool arguments")
    parser.add_argument("--timeout", type=float, default=120.0, help="Seconds per call (default 120)")
    parser.add_argument(
        "--server-stderr",
        metavar="PATH",
        help="Capture server stderr to PATH for debugging crashes",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse the CLI, execute one MCP tool and print its answer.

    Args:
        argv: Optional argv override for embedding callers.

    Returns:
        Process exit code using the documented exit-code contract.

    Raises:
        SystemExit: Only via the caller wiring; this function returns codes.
    """
    try:
        import mcp  # noqa: F401
    except ImportError:
        print("mcp package missing: install requirements-light.txt or 'pip install mcp'", file=sys.stderr)
        return _EXIT_NO_MCP
    parser = _build_parser()
    parsed = parser.parse_args(argv)
    try:
        arguments = _parse_arguments(parsed.arguments)
    except ValueError as exc:
        print(f"arguments: {exc}", file=sys.stderr)
        return _EXIT_USAGE
    try:
        command = _server_command()
    except RuntimeError as exc:
        print(f"repository layout: {exc}", file=sys.stderr)
        return _EXIT_USAGE
    settings = _LoopSettings(
        name=parsed.tool,
        arguments=arguments,
        timeout_sec=max(1.0, float(parsed.timeout)),
        stderr_file=Path(parsed.server_stderr) if parsed.server_stderr else None,
    )
    try:
        answer = asyncio.run(_call_once(settings, command))
    except TimeoutError:
        print(f"tool '{settings.name}' timed out after {settings.timeout_sec}s", file=sys.stderr)
        return _EXIT_TRANSPORT
    except (BrokenPipeError, ConnectionError, RuntimeError, OSError) as exc:
        print(f"transport failure: {exc}", file=sys.stderr)
        return _EXIT_TRANSPORT
    if answer.text:
        print(answer.text)
    if answer.is_error:
        return _EXIT_TOOL_ERROR
    return _EXIT_OK if answer.text else _EXIT_NO_CONTENT


if __name__ == "__main__":
    raise SystemExit(main())
