"""Dependency-injection context handed to every ``mcp_tools`` handler.

Each tool module under :mod:`mcp_tools` is import-pure: it declares a
``TOOL`` schema and a ``handle(arguments, tool_name, ctx)`` function and
imports nothing from the multi-thousand-line ``lazyown_mcp`` runtime. The
runtime builds one :class:`MCPContext` bundling the shared helpers and
passes it in, so a tool file never imports the runtime and no circular
import can form. New shared helpers are added here as a field when a
migrated tool first needs them, keeping the contract explicit and typed.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MCPContext:
    """Shared runtime helpers injected into each tool handler.

    Attributes:
        text: Render ``content`` into the MCP ``TextContent`` envelope for
            ``tool_name`` (compaction and transcript recording included).
        load_payload: Return the current ``payload.json`` as a dict, read
            fresh so operator edits made via the CLI are always observed.
        save_payload: Persist a payload dict back to ``payload.json`` and
            return the written path, used by config-mutating tools.
        lazyown_dir: Absolute path to the LazyOwn repository root, for tools
            that resolve modules or other repo-relative resources.
        sessions_dir: Absolute path to the ``sessions/`` campaign-state
            directory, for tools that read or write artefacts there.
        modules_dir: Absolute path to the ``modules/`` package directory.
        skills_dir: Absolute path to the ``skills/`` directory.
        run_command: Execute one LazyOwn shell command line with a timeout
            and return its captured output, for tools that drive the CLI.
        c2_request: Make an authenticated request to the C2 server
            (``path``, ``method``, optional ``body``) and return the parsed
            JSON response, for tools that read beacon or dashboard state.
        get_policy: Return the shared policy-integration singleton when the
            optional policy engine is available, else None, for tools that
            report command outcomes to the policy layer.
        get_transcript: Return the active transcript recorder or None, for
            tools that audit spawns or report harness state.
        get_perm_system: Return the permission system or None.
        get_hooks: Return the hooks runner or None.
        get_claudemd: Return the loaded CLAUDE.md hierarchy or None.
        job_store: The shared background-job store singleton, so async-run
            and job-status tools observe the same jobs.
        list_tools: The server's async ``list_tools`` coroutine, for tools
            that search or enumerate the whole catalogue.
        sitrep_recommendations: Return the top campaign recommendations, for
            session-brief tools.
    """

    text: Callable[[str, str], list]
    load_payload: Callable[[], dict[str, Any]]
    save_payload: Callable[[dict[str, Any]], str]
    lazyown_dir: Path
    sessions_dir: Path
    modules_dir: Path
    skills_dir: Path
    run_command: Callable[[str, int], str]
    c2_request: Callable[..., dict[str, Any]]
    get_policy: Callable[[], Any | None]
    get_transcript: Callable[[], Any | None]
    get_perm_system: Callable[[], Any | None]
    get_hooks: Callable[[], Any | None]
    get_claudemd: Callable[[], Any | None]
    job_store: Any
    list_tools: Callable[[], Any]
    sitrep_recommendations: Callable[..., list]
