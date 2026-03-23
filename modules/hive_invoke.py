#!/usr/bin/env python3
"""
modules/hive_invoke.py
=======================
Invokes Claude Code CLI with the LazyOwn MCP server and forwards an operator
prompt for autonomous or hive-mind execution.

Claude Code will have access to the lazyown MCP server (configured in
~/.claude.json) and will use its tools to fulfil the request.

Usage (via hive addon)
----------------------
  hive enumerate all SMB shares on 10.10.11.78
  hive spawn 3 drones to perform AD enumeration
  hive start autonomous mode targeting 10.10.11.78
  hive what hosts and credentials have been captured so far
  hive -i enumerate Active Directory on 10.10.11.78  (interactive mode)

Usage (direct)
--------------
  python3 modules/hive_invoke.py [OPTIONS] <prompt words ...>

Options
-------
  -i, --interactive     Open Claude Code in interactive REPL mode so the
                        operator can follow up after the initial response.
                        Default: non-interactive print mode (-p).
  -e, --effort LEVEL    Effort level passed to Claude: low | medium | high | max
                        Default: high.
  -h, --help            Show this help message and exit.

Exit codes
----------
  0   Claude executed successfully.
  1   Missing prompt or claude binary not found.
  2   Claude returned a non-zero exit code.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_LAZYOWN_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# System context appended to every request
# ---------------------------------------------------------------------------

_SYSTEM_CONTEXT = """\
You are operating within the LazyOwn Red Team Framework via the hive command.
The LazyOwn MCP server (mcp__lazyown__*) is available with the following tools:

Hive Mind — multi-agent parallel execution:
  lazyown_hive_spawn     spawn parallel drones (roles: recon/exploit/analyze/cred/lateral/architect)
  lazyown_hive_plan      decompose a goal into drone tasks without spawning
  lazyown_hive_status    status of active drones and hive memory stats
  lazyown_hive_recall    semantic search over past drone results and sessions
  lazyown_hive_collect   wait for drones and produce a synthesized summary
  lazyown_hive_result    retrieve one specific drone result

Autonomous Daemon — fully self-driving execution loop:
  lazyown_autonomous_start   start the autonomous daemon with an initial objective
  lazyown_autonomous_status  check daemon health and current objective
  lazyown_autonomous_stop    stop the daemon
  lazyown_autonomous_inject  inject a new mid-run objective

Direct Command Execution:
  lazyown_run_command    execute any LazyOwn shell command (nmap, enum, exploit, etc.)
  lazyown_run_api        call the LazyOwn REST API

Intelligence and Context:
  lazyown_rag_query      semantic search over past session data
  lazyown_facts_show     structured facts (services, creds, paths) for a target
  lazyown_threat_model   MITRE ATT&CK threat model for the current session
  lazyown_recommend_next next recommended action category for a target
  lazyown_hive_plan      task decomposition planner

Decision guidance:
- For investigations that can run in parallel, always prefer lazyown_hive_spawn.
- For sustained, goal-driven autonomous operation, use lazyown_autonomous_start.
- For one-shot intelligence queries, use lazyown_rag_query or lazyown_facts_show.
- Always read lazyown_hive_status before spawning to avoid duplicate drones.\
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _find_claude() -> str | None:
    """Return the absolute path to the claude binary, or None if not found."""
    return shutil.which("claude")


def _parse_argv(argv: list[str]) -> tuple[bool, str, list[str]]:
    """
    Parse argv into (interactive, effort, prompt_words).

    Returns
    -------
    interactive : bool   — True when -i/--interactive is present
    effort      : str    — effort level string (default "high")
    prompt_words: list   — remaining words that form the prompt
    """
    interactive   = False
    effort        = "high"
    prompt_words: list[str] = []
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in ("-i", "--interactive"):
            interactive = True
        elif token in ("-e", "--effort") and i + 1 < len(argv):
            effort = argv[i + 1]
            i += 1
        elif token in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            prompt_words.append(token)
        i += 1
    return interactive, effort, prompt_words


def _run_print_mode(prompt: str, effort: str, claude_bin: str) -> int:
    """
    Run Claude Code in non-interactive print mode (-p).
    Output streams directly to the terminal.
    Permissions are skipped so tool calls execute without prompts.
    """
    proc = subprocess.run(
        [
            claude_bin,
            "--print",
            "--dangerously-skip-permissions",
            "--effort", effort,
            "--append-system-prompt", _SYSTEM_CONTEXT,
            prompt,
        ],
        cwd=str(_LAZYOWN_DIR),
    )
    return proc.returncode


def _run_interactive_mode(prompt: str, effort: str, claude_bin: str) -> int:
    """
    Start Claude Code in interactive REPL mode with the prompt pre-loaded as
    the first message.  The operator can follow up with additional questions.
    """
    proc = subprocess.run(
        [
            claude_bin,
            "--dangerously-skip-permissions",
            "--effort", effort,
            "--append-system-prompt", _SYSTEM_CONTEXT,
            prompt,
        ],
        cwd=str(_LAZYOWN_DIR),
    )
    return proc.returncode


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if not args or args == ["-h"] or args == ["--help"]:
        print(__doc__)
        return 0

    interactive, effort, prompt_words = _parse_argv(args)

    if not prompt_words:
        print("[hive] Error: no prompt provided.", file=sys.stderr)
        print("Usage: hive [--interactive] <prompt>", file=sys.stderr)
        return 1

    prompt = " ".join(prompt_words)

    claude_bin = _find_claude()
    if claude_bin is None:
        print(
            "[hive] Error: 'claude' binary not found in PATH.\n"
            "Install Claude Code with: npm install -g @anthropic-ai/claude-code",
            file=sys.stderr,
        )
        return 1

    mode_label = "interactive REPL" if interactive else "print (non-interactive)"
    print(f"[hive] Claude Code  mode={mode_label}  effort={effort}")
    print(f"[hive] Prompt       {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print("-" * 72)

    if interactive:
        rc = _run_interactive_mode(prompt, effort, claude_bin)
    else:
        rc = _run_print_mode(prompt, effort, claude_bin)

    if rc != 0:
        print(f"\n[hive] Claude exited with code {rc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
