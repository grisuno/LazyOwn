"""Parsing, printing and replanning support for the ``apt_chain`` CLI.

Keeps ``cli.commands.command_and_control_migrated`` thin: argument
parsing, step selection, checkpoint/resume wiring, result rendering and
the reactive replanner live here. Options are parsed manually so any
unknown flag fails loudly instead of being silently swallowed.
"""

from __future__ import annotations

import os
import re
import shlex
from dataclasses import dataclass, field
from typing import Any

from modules.chain_registry import Chain, ChainStep
from modules.chain_runner import ChainRunResult, ReplanContext
from modules.chain_state import list_checkpoints

_TOKEN_NAME_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
_VAR_PREFIXES = ("--var",)
_FLAGS_NO_VALUE = frozenset({"--dry-run", "--json", "--continue", "--replan", "--no-checkpoint"})
_FLAGS_WITH_VALUE = frozenset(
    {
        "--target",
        "--timeout",
        "--step",
        "--from-step",
        "--to-step",
        "--resume",
        "--playbook",
        "--chain",
        "--var",
        "--limit",
    }
)
_ADMIN_ACTIONS = frozenset({"list", "show", "validate", "enable", "disable", "checkpoints", "resume", "synth"})
_MAX_JSON_VALUES = 64


def _token_name_ok(name: str) -> bool:
    """True when a name matches the chain token grammar."""
    return bool(name) and (name[0].isalpha() or name[0] == "_") and set(name) <= _TOKEN_NAME_CHARS


@dataclass
class ChainArgs:
    """Parsed ``apt_chain`` invocation."""

    admin_action: str = ""
    admin_args: list[str] = field(default_factory=list)
    positional: list[str] = field(default_factory=list)
    dry_run: bool = False
    json_out: bool = False
    continue_all: bool = False
    replan: bool = False
    no_checkpoint: bool = False
    target: str = ""
    timeout: float = 0.0
    limit: int = 0
    vars: dict[str, str] = field(default_factory=dict)
    step_ids: list[str] = field(default_factory=list)
    from_step: str = ""
    to_step: str = ""
    resume_run_id: str = ""
    playbook: str = ""
    chain_override: str = ""
    errors: list[str] = field(default_factory=list)


def parse_chain_args(line: str) -> ChainArgs:
    """Parse one ``apt_chain`` command line into structured args.

    Unknown dash-flags become errors: the old silent-swallow behavior
    hid operator intent and is gone.
    """
    args = ChainArgs()
    try:
        parts = shlex.split(line or "")
    except ValueError as exc:
        args.errors.append(f"unbalanced quotes: {exc}")
        return args
    if not parts:
        return args
    if parts[0].lower() in _ADMIN_ACTIONS:
        args.admin_action = parts[0].lower()
        args.admin_args = [part for part in parts[1:] if not part.startswith("-")]
        for token in parts[1:]:
            if token.startswith("-") and token not in _FLAGS_NO_VALUE:
                args.errors.append(f"unknown option for {args.admin_action}: {token}")
        if args.admin_action == "list" and "--json" in [part.lower() for part in parts[1:]]:
            args.json_out = True
        if args.admin_action == "synth" and "--json" in [part.lower() for part in parts[1:]]:
            args.json_out = True
        return args
    index = 0
    while index < len(parts):
        token = parts[index]
        if token == "--var":
            value = parts[index + 1] if index + 1 < len(parts) else ""
            index += 2
            name, _, raw = value.partition("=")
            if not value or not _token_name_ok(name.strip()) or raw == "":
                args.errors.append(f"--var needs key=value (got {value!r})")
            else:
                args.vars[name.strip()] = raw
            continue
        if token in _FLAGS_NO_VALUE:
            if token == "--dry-run":
                args.dry_run = True
            elif token == "--json":
                args.json_out = True
            elif token == "--continue":
                args.continue_all = True
            elif token == "--replan":
                args.replan = True
            elif token == "--no-checkpoint":
                args.no_checkpoint = True
            index += 1
            continue
        if token in _FLAGS_WITH_VALUE or (token.startswith("-") and token != "-"):
            value = parts[index + 1] if index + 1 < len(parts) else ""
            index += 2
            if token in ("--json",):
                args.json_out = True
                continue
            if token.startswith("-") and token not in _FLAGS_WITH_VALUE:
                args.errors.append(f"unknown option: {token}")
                continue
            if not value or value.startswith("-"):
                args.errors.append(f"missing value for {token}")
                continue
            _set_value(args, token, value)
            continue
        args.positional.append(token)
        index += 1
    return args


def _set_value(args: ChainArgs, flag: str, value: str) -> None:
    """Assign one valued option onto the args struct."""
    if flag == "--target":
        args.target = value
    elif flag == "--chain":
        args.chain_override = value.lower()
    elif flag == "--resume":
        args.resume_run_id = value
    elif flag == "--from-step":
        args.from_step = value
    elif flag == "--to-step":
        args.to_step = value
    elif flag == "--playbook":
        args.playbook = value
    elif flag == "--step":
        args.step_ids = [part.strip() for part in value.split(",") if part.strip()]
    elif flag == "--limit":
        try:
            args.limit = max(1, int(value))
        except ValueError:
            args.errors.append(f"--limit needs an integer (got {value!r})")
    elif flag == "--timeout":
        try:
            args.timeout = float(value)
        except ValueError:
            args.errors.append(f"--timeout needs seconds (got {value!r})")


def resolve_admin(args: ChainArgs) -> dict[str, Any]:
    """Execute an admin action against the registry and checkpoint store."""
    from modules.chain_registry import CHAINS_DIR, scan_all, set_enabled, validate_chain
    from modules.chain_registry import get as get_chain

    if args.admin_action == "list":
        rows = scan_all(chains_dir=CHAINS_DIR)
        view = rows if len(rows) <= _MAX_JSON_VALUES else rows[:_MAX_JSON_VALUES]
        return {"ok": True, "action": "list", "rows": view}
    if args.admin_action == "checkpoints":
        return {"ok": True, "action": "checkpoints", "rows": list_checkpoints(limit=args.limit or 10)}
    if args.admin_action == "synth":
        playbook = args.admin_args[0].strip() if args.admin_args else ""
        target = ""
        if len(args.admin_args) > 1:
            target = args.admin_args[1].strip()
        elif args.target.strip():
            target = args.target.strip()
        if not target:
            return {"ok": False, "error": "synth needs a target (positional, --target or rhost)"}
        try:
            from modules.chain_synth import facts_for_target, synth_chain_data, write_generated_chain
        except Exception as exc:
            return {"ok": False, "error": f"chain synth unavailable: {exc}"}
        facts = facts_for_target(target)
        data, notes = synth_chain_data(
            playbook,
            target,
            facts.get("services", []),
            has_creds=bool(facts.get("has_creds")),
            os_hint=str(facts.get("os_hint", "")),
        )
        file_path, errors = write_generated_chain(data, CHAINS_DIR)
        return {
            "ok": file_path is not None,
            "action": "synth",
            "name": str(data.get("name", "")),
            "path": str(file_path) if file_path else "",
            "steps": len(data.get("steps", [])),
            "errors": errors,
            "notes": notes[:24],
        }
    name = (args.admin_args[0] if args.admin_args else "").strip().lower()
    if not name:
        return {"ok": False, "error": f"usage: apt_chain {args.admin_action} <chain>"}
    path = CHAINS_DIR / f"{name}.yaml"
    if not path.is_file():
        return {"ok": False, "error": f"chain file not found: {name}"}
    try:
        import yaml

        with path.open("r", encoding="utf-8", errors="replace") as handle:
            data = yaml.safe_load(handle)
    except Exception as exc:
        return {"ok": False, "error": f"unreadable: {exc}"}
    errors = (
        validate_chain(data, filename=path.stem, chains_dir=CHAINS_DIR) if isinstance(data, dict) else ["not a mapping"]
    )
    if args.admin_action == "validate":
        chain = get_chain(name, chains_dir=CHAINS_DIR)
        steps = [entry.get("run", "") for entry in (data.get("steps") or []) if isinstance(entry, dict)]
        return {
            "ok": not errors,
            "action": "validate",
            "name": name,
            "errors": errors,
            "steps": steps[:32],
            "enabled": bool(chain is not None),
        }
    if args.admin_action == "show":
        return {
            "ok": True,
            "action": "show",
            "name": name,
            "steps": [entry for entry in (data.get("steps") or []) if isinstance(entry, dict)][:32],
            "defaults": data.get("defaults", {}) if isinstance(data, dict) else {},
            "extends": data.get("extends", "") if isinstance(data, dict) else "",
            "description": data.get("description", "") if isinstance(data, dict) else "",
            "errors": errors,
        }
    if args.admin_action in ("enable", "disable"):
        if errors and args.admin_action == "enable":
            return {"ok": False, "error": f"chain invalid: {'; '.join(errors)}"}
        flipped = set_enabled(name, args.admin_action == "enable", chains_dir=CHAINS_DIR)
        return {"ok": flipped, "action": args.admin_action, "name": name, "error": "" if flipped else "flip failed"}
    return {"ok": False, "error": f"unsupported admin action: {args.admin_action}"}


def select_step_ids(chain: Chain, args: ChainArgs) -> tuple[set[str] | None, list[str]]:
    """Resolve --step/--from-step/--to-step into one id set."""
    errors: list[str] = []
    wanted: set[str] | None = None
    known_ids = [step.identifier for step in chain.steps]
    if args.step_ids:
        wanted = set()
        for token in args.step_ids:
            if token in known_ids:
                wanted.add(token)
            else:
                errors.append(f"--step id not found: {token}")
    if args.from_step or args.to_step:
        start = 0
        end = len(chain.steps)
        if args.from_step:
            if args.from_step in known_ids:
                start = known_ids.index(args.from_step)
                wanted = set()
            else:
                errors.append(f"--from-step id not found: {args.from_step}")
        if args.to_step:
            if args.to_step in known_ids:
                end = known_ids.index(args.to_step) + 1
                wanted = set()
            else:
                errors.append(f"--to-step id not found: {args.to_step}")
        if wanted is not None:
            wanted |= {step.identifier for step in chain.steps[start:end]}
    return (wanted if wanted is not None else None), errors


def adversarial_continue(chain: Chain) -> Chain:
    """Return a copy of the chain where every step continues on error."""
    import dataclasses

    steps = [dataclasses.replace(step, continue_on_error=True) for step in chain.steps]
    return dataclasses.replace(chain, steps=steps)


def render_result(result: ChainRunResult) -> list[str]:
    """Render one chain result as operator lines (JSON mode prints dict)."""
    lines = [f"[apt_chain] chain={result.name} target={result.target} run_id={result.run_id or '-'}"]
    for outcome in result.steps:
        if outcome.status in ("skipped", "dry-run"):
            lines.append(f"[apt_chain] {outcome.status}: {outcome.run} ({outcome.reason})")
        elif outcome.ok:
            verdict = f" [{outcome.verdict}]" if outcome.verdict else ""
            lines.append(f"[apt_chain] ok{verdict}: {outcome.run}")
            if outcome.missing_fields:
                lines.append(f"    missing fields: {', '.join(outcome.missing_fields)}")
            if outcome.output:
                lines.extend(f"    {part[:220]}" for part in outcome.output.splitlines()[:24])
        else:
            lines.append(f"[apt_chain] {outcome.status}: {outcome.run} ({outcome.reason})")
    for branch in result.branches:
        lines.append(f"[apt_chain] branch: {branch}")
    if result.aborted:
        lines.append(f"[apt_chain] aborted: {result.reason}")
    done = sum(1 for outcome in result.steps if outcome.ok)
    lines.append(
        f"[apt_chain] chain finished: {done}/{len(result.steps)} step(s) ok"
        " - a green run line means the step was issued, not that the target fell."
    )
    if result.verdicts:
        lines.append(
            "[apt_chain] chain "
            + ("evidence proven" if result.chain_proven else "evidence unproven")
            + f": {', '.join(f'{key}={value}' for key, value in result.verdicts.items())}"
        )
    return lines


def build_cli_approver(printer, input_fn=None):
    """Return an approver baked for interactive operators.

    Autonomous mode (``LAZYOWN_AUTONOMOUS=1``) auto-approves and logs
    the decision; interactive mode asks the operator failure-closed.
    """
    autonomous = os.environ.get("LAZYOWN_AUTONOMOUS", "") == "1"

    def approve(step_id: str, command: str) -> bool:
        if autonomous:
            printer(f"[apt_chain] auto-approved confirm step {step_id} (autonomous mode)")
            return True
        ask = input_fn or input
        try:
            answer = ask(f"[apt_chain] confirm step {step_id}?\n  {command}\n  approve [y/N] ")
        except (EOFError, KeyboardInterrupt):
            return False
        return str(answer).strip().lower() in ("y", "yes")

    return approve


def build_reactive_replanner():
    """Return a replanner driven by ``modules.reactive_engine``."""

    def replan(context: ReplanContext) -> None:
        from modules.reactive_engine import get_engine

        engine = get_engine()
        outcome = context.outcome
        if outcome is None or not outcome.output:
            return
        try:
            decisions = engine.analyse(outcome.output, command=outcome.run, platform=_platform())
        except Exception:
            return
        for decision in decisions:
            command = (_decision_command(decision) or "").strip()
            if not command or command.lower().startswith("apt_chain"):
                continue
            step = _step_from_decision(command, outcome, len(context.executed_ids))
            if step is not None:
                context.insert_step(step)

    return replan


def _decision_command(decision: Any) -> str:
    """Extract one actionable command from a reactive decision."""
    for attribute in ("command", "suggestion", "fix", "cmd"):
        value = getattr(decision, attribute, "")
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _step_from_decision(command: str, outcome: Any, executed_count: int):
    """Build one safe replan step from a suggested command."""
    from modules.chain_registry import ChainStep

    head = (command.split() or ["replan"])[0].lower()
    slug = "".join(char if char.isalnum() else "_" for char in head).strip("_")[:20] or "replan"
    if not _token_name_ok(slug) or slug.isdigit():
        slug = "replan"
    after = getattr(outcome, "id", "") if hasattr(outcome, "id") else str(executed_count)
    after_slug = "".join(char if char.islower() or char.isdigit() else "_" for char in str(after)) or "step"
    clean_id = re.sub(r"_+", "_", f"replan_{after_slug}_{slug}")[:64].rstrip("_")
    if not _token_name_ok(clean_id):
        clean_id = "replan_step"
    return ChainStep(
        run=command[:300],
        id=clean_id,
        phase="replan",
        description=f"reactive replan after {after or 'step'}",
        timeout=300,
    )


def build_llm_recovery_chain(result: ChainRunResult, target: str = "", task_id: str = "") -> Chain | None:
    """Ask the LLM pool for a temporary recovery chain after a failed run.

    The prompt carries the original objective shape (chain name and
    target), the steps that already succeeded and the failed steps with
    their last errors. The model proposes up to three alternative shell
    commands; each becomes a ``continue_on_error`` step so one bad
    suggestion cannot abort the whole recovery. Returns None when the
    pool is unavailable or replies nothing usable.
    """
    failed = [outcome for outcome in result.steps if not outcome.ok]
    if not failed:
        return None
    from modules.mediation import MediationDomains, resolve

    pool = resolve(MediationDomains.CHAIN).llm()
    if not pool.has_members():
        return None
    ok_ids = [outcome.id for outcome in result.steps if outcome.ok][:8]
    failed_lines = "\n".join(
        f"- {outcome.id}: {outcome.run[:160]} ({outcome.status}: {outcome.reason[:120]})" for outcome in failed[:5]
    )
    prompt = (
        f"The APT chain '{result.name}' against {target or result.target} failed.\n"
        f"Steps already ok: {', '.join(ok_ids) or 'none'}.\n"
        f"Failed steps:\n{failed_lines}\n"
        "Propose up to 3 alternative shell commands that recover the objective, "
        "one per line, no numbering, no explanations. Use only tools installed "
        "on this host. Never leave the authorized target. Never use sudo."
    )
    try:
        from modules.guardrails import TaskClass, global_harness

        reply = (
            global_harness().run_guarded(TaskClass.MISSION, pool.complete, prompt, max_tokens=300, task_id=task_id)
            or ""
        )
    except Exception:
        return None
    commands: list[str] = []
    for raw in reply.splitlines():
        command = raw.strip().strip("`").strip()
        head = command.split(maxsplit=1)[0].lower() if command else ""
        if len(command) < 4 or len(command) > 300 or command.startswith("#"):
            continue
        if head in ("sudo", "apt_chain"):
            continue
        if command not in commands:
            commands.append(command)
        if len(commands) >= 3:
            break
    if not commands:
        return None
    steps = [
        ChainStep(
            run=command,
            id=f"recovery_{index + 1}",
            phase="replan",
            description=f"LLM recovery step {index + 1}",
            timeout=300,
            continue_on_error=True,
        )
        for index, command in enumerate(commands)
    ]
    return Chain(
        name=f"{result.name}_recovery",
        description=f"LLM-generated recovery for {result.name}",
        defaults={"target": target or result.target},
        steps=steps,
    )


def _platform() -> str:
    """Guess the loop platform from the payload configuration."""
    import json

    config_path = os.path.join(os.getcwd(), "payload.json")
    try:
        with open(config_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return "windows" if str(payload.get("os", "") or "").lower().startswith("windows") else "linux"
    except Exception:
        return "linux"


__all__ = [
    "ChainArgs",
    "build_cli_approver",
    "build_llm_recovery_chain",
    "build_reactive_replanner",
    "parse_chain_args",
    "render_result",
    "resolve_admin",
    "select_step_ids",
]
