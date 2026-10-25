#!/usr/bin/env python3
"""Audit every registered shell command for dispatch and parser errors.

The audit boots the cmd2 shell once, runs ``help`` for every registered
command, and probes every ``@with_argparser`` command with an invalid flag so
cmd2 exercises the parser without running the command body. It reports any
command whose parser or dispatch raises. It is read-only: the probe flag is
rejected before the command body executes.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class AuditConfig:
    """Configuration for the command audit.

    Attributes:
        commands_dir: Directory that holds the cmd2 CommandSet modules.
        probe_flag: Invalid flag the parser must reject without running the body.
        safe_argv: Argument vector installed before importing the shell so the
            framework does not parse the audit's own arguments.
    """

    commands_dir: Path = field(default_factory=lambda: REPO_ROOT / "cli" / "commands")
    probe_flag: str = "--__audit_invalid__"
    safe_argv: tuple[str, ...] = ("lazyown", "-c", "exit")


def argparser_commands(config: AuditConfig) -> list[str]:
    """Return the command names decorated with ``@with_argparser``.

    Args:
        config: Active audit configuration.
    Returns:
        Sorted command names without the ``do_`` prefix.
    """
    names: list[str] = []
    for path in sorted(config.commands_dir.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.name.startswith("do_"):
                continue
            for decorator in node.decorator_list:
                target = decorator.func if isinstance(decorator, ast.Call) else decorator
                name = target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
                if name == "with_argparser":
                    names.append(node.name[3:])
    return sorted(set(names))


def audit(config: AuditConfig | None = None) -> list[str]:
    """Run the dispatch and parser audit.

    Args:
        config: Optional audit configuration.
    Returns:
        A list of ``command: error`` strings. Empty means every command passed.
    """
    active = config or AuditConfig()
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    sys.argv = list(active.safe_argv)
    from cmd2 import Cmd2ArgparseError

    import lazyown

    shell = lazyown.LazyOwnShell()
    errors: list[str] = []
    for name in sorted(shell.get_all_commands()):
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                shell.onecmd(f"help {name}")
        except SystemExit:
            pass
        except BaseException as exc:
            errors.append(f"help {name}: {type(exc).__name__}: {exc}")
    for name in argparser_commands(active):
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                shell.onecmd(f"{name} {active.probe_flag}")
        except (SystemExit, Cmd2ArgparseError):
            pass
        except BaseException as exc:
            errors.append(f"probe {name}: {type(exc).__name__}: {exc}")
    print(f"audited {len(shell.get_all_commands())} commands, {len(errors)} error(s)")
    return errors


def main(argv: list[str] | None = None) -> int:
    """Run the audit and return the process exit code."""
    parser = argparse.ArgumentParser(prog="command_audit")
    parser.add_argument("--probe-flag", default=AuditConfig.probe_flag, help="invalid flag for parser probes")
    args = parser.parse_args(argv)
    errors = audit(AuditConfig(probe_flag=args.probe_flag))
    for error in errors:
        print(f"[audit] {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
