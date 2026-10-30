"""Chain registry - ordered orchestration chains from ``chains/*.yaml``.

One file per chain, same philosophy as ``lazyaddons/`` and ``exploits/``.
The ``apt_chain`` shell command interprets these files instead of
hardcoding its steps, so operators extend the orchestration by editing
YAML. Every step must be a routable shell command; resolution (tokens,
conditions, skip rules, newest-file globs) happens here, execution stays
in :mod:`modules.chain_runner` where timeouts and outcomes belong.

Schema version 2 adds ``when`` conditions, per-step timeouts, retries,
error policy, output capture, artefacts and sink tags. Version 1 files
remain valid with the same defaults.
"""

from __future__ import annotations

import ast
import glob
import hashlib
import logging
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

log = logging.getLogger("chain_registry")

_BASE_DIR = Path(__file__).resolve().parent.parent
CHAINS_DIR = _BASE_DIR / "chains"

_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_CAPTURE_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_TOKEN_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_MAX_YAML_BYTES = 100_000
_MAX_WHEN_CHARS = 500
_MAX_STEP_TIMEOUT = 3600
_MAX_RETRIES = 5
_MAX_TOTAL_TIMEOUT = 86_400
_MAX_VERIFY_CHARS = 500
_MAX_CAPTURE_REGEX_CHARS = 256
_MAX_JSON_KEYS = 8
_MAX_EXPECT_EXITS = 8
_EXPECT_EXIT_MAX = 255
_EXPECT_EXIT_RE = re.compile(r"^(0|[1-9][0-9]{0,2})$")
_JUMP_RE = _NAME_RE
_MAX_STEP_LIST_ITEMS = 16
_MAX_LIST_ITEM_CHARS = 128
_BUDGET_KEYS = frozenset({"attempts", "seconds"})
_MAX_BUDGET_ATTEMPTS = _MAX_RETRIES + 1
_MAX_BUDGET_SECONDS = _MAX_STEP_TIMEOUT
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MAX_EVIDENCE_PATH_CHARS = 512
_SHELL_METACHARS = re.compile(r"[;&|<>()`$\\]")
_SHELL_METACHARS_REASON = (
    "declare variable in raw_vars to interpolate it verbatim, or shell-quote the value in YAML"
)
_MAX_SKIP_MAX_AGE = 365 * 86400


def skip_pending(path: str, max_age: int, now: float | None = None) -> str | None:
    """Return the skip reason when an artefact is present and fresh.

    The freshness window makes recurring chains re-run stale work
    instead of skipping forever: an artefact older than ``skip_max_age``
    seconds stops being a skip guard and its step executes again.

    Args:
        path: Rendered artefact path.
        max_age: Maximum accepted age in seconds; 0 keeps the artefact
            valid forever.
        now: Reference epoch; defaults to current time.

    Returns:
        Skip reason text, or None when the step must run.
    """
    if not path or not os.path.exists(path):
        return None
    if not max_age:
        return f"exists: {path}"
    try:
        stamp = os.stat(path).st_mtime
    except OSError:
        return f"exists: {path}"
    reference = now if now is not None else time.time()
    if reference - stamp <= max_age:
        return f"exists: {path}"
    return None
_YAML_REQUIRED = (
    "PyYAML is required for chain YAML: pip install pyyaml, or run 'doctor --fix' "
    "to install missing packages"
)


@dataclass
class ChainStep:
    """One ordered step: shell line plus optional guards and outcome policy.

    Hunting fields (v3) turn a step into a chain-of-evidence node:
    ``depends_on`` gates execution on predecessor evidence verdicts,
    ``required_fields`` verifies field presence in captured evidence,
    ``benign_alternatives`` annotates benign explanations, ``budget``
    caps attempts and wall time, and ``evidence_sha256`` pins artefact
    integrity across re-runs.
    """

    run: str = ""
    id: str = ""
    phase: str = ""
    description: str = ""
    when: str = ""
    skip_if_exists: str = ""
    skip_max_age: int = 0
    resolve_newest_glob: str = ""
    resolve_newest_as: str = ""
    timeout: int = 0
    retries: int = 0
    continue_on_error: bool = False
    capture: str = ""
    capture_regex: str = ""
    capture_json: str = ""
    expect: str = ""
    expect_exit: list[int] = field(default_factory=list)
    verify: str = ""
    pre_check: str = ""
    parallel: bool = False
    on_fail: str = ""
    on_success: str = ""
    confirm: bool = False
    artifacts: list[str] = field(default_factory=list)
    sinks: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    required_fields: list[str] = field(default_factory=list)
    benign_alternatives: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    evidence_sha256: dict[str, str] = field(default_factory=dict)
    budget: dict[str, int] = field(default_factory=dict)

    @property
    def identifier(self) -> str:
        """Return the declared id or a stable generated one."""
        return self.id or f"step_{hashlib.sha1(self.run.encode('utf-8')).hexdigest()[:8]}"


@dataclass
class Chain:
    """A validated chain with defaults, variables and ordered steps."""

    name: str = ""
    description: str = ""
    version: int = 1
    tags: list[str] = field(default_factory=list)
    platforms: list[str] = field(default_factory=list)
    defaults: dict[str, str] = field(default_factory=dict)
    vars: dict[str, str] = field(default_factory=dict)
    steps: list[ChainStep] = field(default_factory=list)
    source: str = ""
    enabled: bool = True
    extends: str = ""
    fallback: str = ""
    total_timeout: int = 0
    raw_vars: tuple[str, ...] = ()

    def resolve(self, tokens: dict[str, str]) -> list[dict[str, Any]]:
        """Substitute tokens, evaluate conditions and guards.

        Returns one mapping per step with ``run``, ``skipped`` and
        ``reason`` plus the v2 policy fields. The runner repeats this
        resolution after every capture so later steps see earlier output.
        """
        merged = {str(k): str(v) for k, v in {**self.defaults, **self.vars, **tokens}.items()}
        resolved: list[dict[str, Any]] = []
        for step in self.steps:
            rendered = _render(step.run, merged)
            base = {
                "id": step.identifier,
                "phase": step.phase,
                "description": step.description,
                "timeout": step.timeout,
                "retries": step.retries,
                "continue_on_error": step.continue_on_error,
                "capture": step.capture,
                "capture_regex": step.capture_regex,
                "capture_json": step.capture_json,
                "expect": step.expect,
                "expect_exit": list(step.expect_exit),
                "verify": step.verify,
                "pre_check": step.pre_check,
                "parallel": step.parallel,
                "on_fail": step.on_fail,
                "on_success": step.on_success,
                "confirm": step.confirm,
                "artifacts": list(step.artifacts),
                "sinks": list(step.sinks),
                "depends_on": list(step.depends_on),
                "required_fields": list(step.required_fields),
                "benign_alternatives": list(step.benign_alternatives),
                "evidence": list(step.evidence),
                "evidence_sha256": dict(step.evidence_sha256),
                "budget": dict(step.budget),
                "step": step,
            }
            if step.when and not evaluate_when(step.when, merged):
                resolved.append({**base, "run": rendered, "skipped": True, "reason": "when false"})
                continue
            skip_path = _render(step.skip_if_exists, merged) if step.skip_if_exists else ""
            if skip_path:
                skip_reason = skip_pending(skip_path, step.skip_max_age)
                if skip_reason:
                    resolved.append({**base, "run": rendered, "skipped": True, "reason": skip_reason})
                    continue
            if step.resolve_newest_glob and step.resolve_newest_as:
                matches = sorted(glob.glob(_render(step.resolve_newest_glob, merged)), key=os.path.getmtime)
                if not matches:
                    resolved.append({**base, "run": rendered, "skipped": True, "reason": "no newest match"})
                    continue
                merged[step.resolve_newest_as] = os.path.abspath(matches[-1])
                rendered = _render(step.run, merged)
            unresolved = _TOKEN_RE.search(rendered)
            if unresolved:
                resolved.append(
                    {**base, "run": rendered, "skipped": True, "reason": f"unresolved token: {unresolved.group(0)}"}
                )
                continue
            resolved.append({**base, "run": rendered, "skipped": False, "reason": ""})
        return resolved


def _render(template: str, variables: dict[str, str]) -> str:
    """Substitute single-brace tokens in one pass."""
    text = str(template or "")
    for key, value in variables.items():
        text = text.replace("{" + key + "}", str(value))
    return text


_ALLOWED_WHEN = (
    ast.Expression,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.UnaryOp,
    ast.Not,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.In,
    ast.NotIn,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.List,
    ast.Tuple,
    ast.Set,
)


def _when_tree(expression: str) -> tuple[ast.Expression | None, str]:
    """Parse and sandbox one ``when`` expression.

    Args:
        expression: Condition text.

    Returns:
        Tuple of parsed tree (or None) and an error string. Empty input
        returns ``(None, "")`` and means true.
    """
    text = str(expression or "").strip()
    if not text:
        return None, ""
    if len(text) > _MAX_WHEN_CHARS:
        return None, f"when exceeds {_MAX_WHEN_CHARS} chars"
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        return None, f"invalid when expression: {exc.msg}"
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_WHEN):
            return None, f"unsupported when element: {type(node).__name__}"
        if isinstance(node, ast.Name) and node.id in ("__import__", "eval", "exec", "open"):
            return None, f"forbidden name in when: {node.id}"
    return tree, ""


def evaluate_when(expression: str, variables: dict[str, str] | None = None) -> bool:
    """Evaluate a safe ``when`` expression against string variables.

    The grammar accepts names, string/boolean constants, ``and``, ``or``,
    ``not``, ``==``, ``!=``, ``in`` and ``not in``. Calls, attributes and
    arithmetic are rejected. Undefined names resolve to an empty string.

    Args:
        expression: Condition text; empty means true.
        variables: Name-to-string mapping.

    Returns:
        Boolean result; malformed expressions evaluate to False.
    """
    text = str(expression or "").strip()
    if not text:
        return True
    tree, _error = _when_tree(text)
    if tree is None:
        return False
    values = {str(key): str(value) for key, value in (variables or {}).items()}

    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            lowered = node.id.lower()
            if lowered in ("true", "false", "none"):
                return {"true": True, "false": False, "none": None}[lowered]
            return values.get(node.id, "")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not bool(_eval(node.operand))
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return [_eval(element) for element in node.elts]
        if isinstance(node, ast.BoolOp):
            results = [_eval(value) for value in node.values]
            return all(results) if isinstance(node.op, ast.And) else any(results)
        if isinstance(node, ast.Compare):
            left = _eval(node.left)
            for operator, comparator in zip(node.ops, node.comparators, strict=False):
                right = _eval(comparator)
                if isinstance(operator, ast.Eq):
                    ok = left == right
                elif isinstance(operator, ast.NotEq):
                    ok = left != right
                elif isinstance(operator, ast.In):
                    ok = left in right
                elif isinstance(operator, ast.NotIn):
                    ok = left not in right
                else:
                    return False
                if not ok:
                    return False
                left = right
            return True
        return False

    try:
        return bool(_eval(tree))
    except Exception:
        return False


def validate_chain(data: Any, filename: str = "", chains_dir: Path | str | None = None) -> list[str]:
    """Validate raw YAML data against the chain schema."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["document must be a mapping"]
    name = str(data.get("name", ""))
    if not _NAME_RE.match(name):
        errors.append(f"invalid name: {name!r}")
    if filename and name != filename:
        errors.append(f"name {name!r} does not match filename {filename!r}")
    version = data.get("version", 1)
    if isinstance(version, bool) or version not in (1, 2):
        errors.append(f"unsupported version: {version!r}")
    for key in ("defaults", "vars"):
        value = data.get(key, {})
        if value is not None and not isinstance(value, dict):
            errors.append(f"{key} must be a mapping")
    raw_vars = data.get("raw_vars", [])
    if not isinstance(raw_vars, list) or any(not isinstance(item, str) or not item.strip() for item in raw_vars):
        errors.append("raw_vars must be a list of variable names")
    else:
        raw_names = {str(item).strip() for item in raw_vars}
        for key in ("defaults", "vars"):
            values = data.get(key, {})
            if not isinstance(values, dict):
                continue
            for var, value in values.items():
                text = str(value or "")
                if str(var) in raw_names:
                    continue
                if _SHELL_METACHARS.search(text):
                    errors.append(
                        f"{key}.{var} contains shell metacharacters; {_SHELL_METACHARS_REASON}"
                    )
    for key in ("tags", "platforms"):
        value = data.get(key, [])
        if value is not None and not isinstance(value, list):
            errors.append(f"{key} must be a list")
    extends = str(data.get("extends", "") or "")
    if extends and not _NAME_RE.match(extends):
        errors.append(f"invalid extends: {extends!r}")
    if extends and extends == str(data.get("name", "")):
        errors.append("a chain cannot extend itself")
    if extends and extends != str(data.get("name", "")) and chains_dir is not None:
        parent_file = Path(chains_dir) / f"{extends}.yaml"
        if not parent_file.is_file():
            errors.append(f"unknown parent chain file: {parent_file.name}")
    fallback = str(data.get("fallback", "") or "")
    if fallback:
        if not _NAME_RE.match(fallback):
            errors.append(f"invalid fallback: {fallback!r}")
        elif fallback == str(data.get("name", "")):
            errors.append("a chain cannot be its own fallback")
        elif chains_dir is not None:
            fallback_file = Path(chains_dir) / f"{fallback}.yaml"
            if not fallback_file.is_file():
                errors.append(f"unknown fallback chain file: {fallback_file.name}")
    total_timeout = data.get("total_timeout", 0)
    if isinstance(total_timeout, bool) or not isinstance(total_timeout, int) or not 0 <= total_timeout <= _MAX_TOTAL_TIMEOUT:
        errors.append(f"total_timeout must be 0-{_MAX_TOTAL_TIMEOUT} seconds")
    if "enabled" in data and not isinstance(data["enabled"], bool):
        errors.append("enabled must be true or false")
    steps = data.get("steps")
    if extends and steps is not None and not isinstance(steps, list):
        errors.append("steps must be a list when present")
    elif not extends and (not isinstance(steps, list) or not steps):
        errors.append("steps must be a non-empty list")
    if isinstance(steps, list):
        seen_ids: set[str] = set()
        jumps: list[tuple[str, str]] = []
        for step in steps:
            if not isinstance(step, dict) or not str(step.get("run", "")).strip():
                errors.append("every step needs a non-empty run string")
                continue
            step_id = str(step.get("id", "") or "")
            step_label = step_id or str(step.get("run"))[:60]
            if step_id:
                if not _NAME_RE.match(step_id):
                    errors.append(f"invalid step id: {step_id!r}")
                elif step_id in seen_ids:
                    errors.append(f"duplicate step id: {step_id!r}")
                seen_ids.add(step_id)
            when = str(step.get("when", "") or "")
            if when:
                _tree, when_error = _when_tree(when)
                if when_error:
                    errors.append(f"step {step_id or step.get('run')!r}: {when_error}")
            timeout = step.get("timeout", 0)
            if isinstance(timeout, bool) or not isinstance(timeout, int) or not 0 <= timeout <= _MAX_STEP_TIMEOUT:
                errors.append(f"step {step_id or step.get('run')!r}: timeout must be 0-{_MAX_STEP_TIMEOUT}")
            skip_max_age = step.get("skip_max_age", 0)
            if isinstance(skip_max_age, bool) or not isinstance(skip_max_age, int) or not 0 <= skip_max_age <= _MAX_SKIP_MAX_AGE:
                errors.append(
                    f"step {step_id or step.get('run')!r}: skip_max_age must be 0-{_MAX_SKIP_MAX_AGE} seconds"
                )
            retries = step.get("retries", 0)
            if isinstance(retries, bool) or not isinstance(retries, int) or not 0 <= retries <= _MAX_RETRIES:
                errors.append(f"step {step_id or step.get('run')!r}: retries must be 0-{_MAX_RETRIES}")
            if "continue_on_error" in step and not isinstance(step["continue_on_error"], bool):
                errors.append(f"step {step_id or step.get('run')!r}: continue_on_error must be boolean")
            capture = str(step.get("capture", "") or "")
            if capture and not _CAPTURE_RE.match(capture):
                errors.append(f"step {step_id or step.get('run')!r}: invalid capture name {capture!r}")
            capture_regex = str(step.get("capture_regex", "") or "")
            if capture_regex:
                if len(capture_regex) > _MAX_CAPTURE_REGEX_CHARS:
                    errors.append(f"step {step_label}: capture_regex exceeds {_MAX_CAPTURE_REGEX_CHARS} chars")
                else:
                    try:
                        re.compile(capture_regex)
                    except re.error as exc:
                        errors.append(f"step {step_label}: invalid capture_regex: {exc}")
            capture_json = str(step.get("capture_json", "") or "")
            if capture_json:
                keys = [key.strip() for key in capture_json.split(",") if key.strip()]
                if not keys or len(keys) > _MAX_JSON_KEYS:
                    errors.append(f"step {step_label}: capture_json accepts 1-{_MAX_JSON_KEYS} keys")
                else:
                    for key in keys:
                        if not _CAPTURE_RE.match(key):
                            errors.append(f"step {step_label}: invalid capture_json key {key!r}")
            verify = str(step.get("verify", "") or "")
            if verify and len(verify) > _MAX_VERIFY_CHARS:
                errors.append(f"step {step_label}: verify exceeds {_MAX_VERIFY_CHARS} chars")
            pre_check = str(step.get("pre_check", "") or "")
            if pre_check and len(pre_check) > _MAX_VERIFY_CHARS:
                errors.append(f"step {step_label}: pre_check exceeds {_MAX_VERIFY_CHARS} chars")
            if "parallel" in step and not isinstance(step["parallel"], bool):
                errors.append(f"step {step_label}: parallel must be true or false")
            elif step.get("parallel") is True:
                for forbidden in ("capture", "capture_regex", "capture_json", "resolve_newest", "on_fail", "on_success"):
                    if step.get(forbidden):
                        errors.append(
                            f"step {step_label}: parallel steps cannot declare {forbidden} "
                            "(parallel outcomes merge after the group, in declaration order)"
                        )
            expect_exit = step.get("expect_exit", [])
            if expect_exit and not isinstance(expect_exit, (int, list)):
                errors.append(f"step {step_label}: expect_exit must be an int or a list of ints")
            codes = [expect_exit] if isinstance(expect_exit, int) else (expect_exit or [])
            if isinstance(expect_exit, (int, list)):
                if len(codes) > _MAX_EXPECT_EXITS:
                    errors.append(f"step {step_label}: expect_exit accepts up to {_MAX_EXPECT_EXITS} codes")
                else:
                    for code in codes:
                        if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code <= _EXPECT_EXIT_MAX:
                            errors.append(f"step {step_label}: expect_exit codes must be 0-{_EXPECT_EXIT_MAX}")
            if "confirm" in step and not isinstance(step["confirm"], bool):
                errors.append(f"step {step_label}: confirm must be true or false")
            for jump_key in ("on_fail", "on_success"):
                jump = str(step.get(jump_key, "") or "")
                if jump and not _JUMP_RE.match(jump):
                    errors.append(f"step {step_label}: invalid {jump_key} target {jump!r}")
                elif jump and step_id and jump == step_id:
                    errors.append(f"step {step_label}: {jump_key} cannot target itself")
                elif jump:
                    jumps.append((step_label, jump, jump_key))
            resolver = step.get("resolve_newest")
            if resolver is not None:
                if not isinstance(resolver, dict) or not resolver.get("glob") or not resolver.get("as"):
                    errors.append("resolve_newest needs glob and as keys")
            depends_on = step.get("depends_on", [])
            if not isinstance(depends_on, list) or len(depends_on) > _MAX_STEP_LIST_ITEMS:
                errors.append(f"step {step_label}: depends_on must be a list of at most {_MAX_STEP_LIST_ITEMS} ids")
            else:
                for dependency in depends_on:
                    if not isinstance(dependency, str) or not dependency.strip():
                        errors.append(f"step {step_label}: depends_on entries must be non-empty strings")
                    elif dependency == step_id:
                        errors.append(f"step {step_label}: depends_on cannot target itself")
                    else:
                        jumps.append((step_label, dependency, "depends_on"))
            for list_key in ("required_fields", "benign_alternatives", "evidence"):
                values = step.get(list_key, [])
                if not isinstance(values, list) or len(values) > _MAX_STEP_LIST_ITEMS:
                    errors.append(f"step {step_label}: {list_key} must be a list of at most {_MAX_STEP_LIST_ITEMS} items")
                    continue
                for item in values:
                    if not isinstance(item, str) or not item.strip() or len(item) > _MAX_LIST_ITEM_CHARS:
                        errors.append(f"step {step_label}: {list_key} entries must be strings up to {_MAX_LIST_ITEM_CHARS} chars")
                        break
            evidence_sha = step.get("evidence_sha256", {})
            if not isinstance(evidence_sha, dict) or len(evidence_sha) > _MAX_STEP_LIST_ITEMS:
                errors.append(f"step {step_label}: evidence_sha256 must be a mapping of path to sha256")
            else:
                for path, digest in evidence_sha.items():
                    if not isinstance(path, str) or not path.strip() or len(path) > _MAX_EVIDENCE_PATH_CHARS:
                        errors.append(f"step {step_label}: evidence_sha256 keys must be non-empty paths")
                        break
                    if not isinstance(digest, str) or not _SHA256_RE.match(digest):
                        errors.append(f"step {step_label}: evidence_sha256[{path!r}] must be a 64-char lowercase hex digest")
                        break
            budget = step.get("budget", {})
            if not isinstance(budget, dict) or len(budget) > len(_BUDGET_KEYS):
                errors.append(f"step {step_label}: budget must be a mapping with keys {sorted(_BUDGET_KEYS)}")
            else:
                for key, value in budget.items():
                    if key not in _BUDGET_KEYS:
                        errors.append(f"step {step_label}: unknown budget key {key!r}")
                        break
                    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                        errors.append(f"step {step_label}: budget {key} must be a non-negative integer")
                        break
                    if key == "attempts" and value > _MAX_BUDGET_ATTEMPTS:
                        errors.append(f"step {step_label}: budget attempts must be 0-{_MAX_BUDGET_ATTEMPTS}")
                        break
                    if key == "seconds" and value > _MAX_BUDGET_SECONDS:
                        errors.append(f"step {step_label}: budget seconds must be 0-{_MAX_BUDGET_SECONDS}")
                        break
        for step_label, jump, jump_key in jumps:
            if jump not in seen_ids:
                errors.append(f"step {step_label}: {jump_key} target {jump!r} is not a known step id")
    return errors


def render_text_token_braces(text: str) -> str:
    """Return text with every ``{name}`` token replaced by a placeholder."""
    return _TOKEN_RE.sub("{_}", str(text or ""))


def load_all(chains_dir: Path | str = CHAINS_DIR) -> dict[str, Chain]:
    """Load every valid, enabled chain file (skips the rest loudly)."""
    if yaml is None:
        raise RuntimeError(_YAML_REQUIRED)
    directory = Path(chains_dir)
    raw: dict[str, dict[str, Any]] = {}
    if directory.exists():
        for path in sorted(directory.glob("*.yaml")):
            try:
                if path.stat().st_size > _MAX_YAML_BYTES:
                    log.warning("Skipping oversized chain file: %s", path)
                    continue
                with path.open("r", encoding="utf-8", errors="replace") as fh:
                    data = yaml.safe_load(fh)
            except Exception as exc:
                log.warning("Skipping unreadable chain file %s: %s", path, exc)
                continue
            errors = validate_chain(data, filename=path.stem, chains_dir=directory)
            if errors:
                log.warning("Skipping invalid chain %s: %s", path, "; ".join(errors))
                continue
            if data.get("enabled", True) is False:
                log.info("Chain disabled, skipping: %s", path)
                continue
            raw[str(data["name"])] = {"data": data, "source": str(path)}
    chains: dict[str, Chain] = {}
    for name in raw:
        try:
            chains[name] = _materialize(name, raw, stack=())
        except ValueError as exc:
            log.warning("Skipping chain %s: %s", name, exc)
    return chains


def _materialize(name: str, raw: dict[str, dict[str, Any]], stack: tuple[str, ...]) -> Chain:
    """Resolve one chain, flattening an ``extends`` hop (cycle-safe)."""
    if name in stack:
        raise ValueError(f"extends cycle: {' -> '.join((*stack, name))}")
    entry = raw[name]
    data = entry["data"]
    parent_name = str(data.get("extends", "") or "")
    parent_steps: list[ChainStep] = []
    parent_defaults: dict[str, str] = {}
    parent_vars: dict[str, str] = {}
    parent_tags: list[str] = []
    parent_platforms: list[str] = []
    if parent_name:
        if parent_name not in raw:
            raise ValueError(f"unknown parent chain: {parent_name!r}")
        parent = _materialize(parent_name, raw, (*stack, name))
        parent_steps = list(parent.steps)
        parent_defaults = dict(parent.defaults)
        parent_vars = dict(parent.vars)
        parent_tags = list(parent.tags)
        parent_platforms = list(parent.platforms)
    steps = parent_steps
    own_raw = data.get("steps") or []
    if own_raw:
        steps = [_step_from_raw(item) for item in own_raw]
    if not steps:
        raise ValueError("chain has no steps after inheritance")
    tags = list(dict.fromkeys(parent_tags + [str(tag) for tag in (data.get("tags") or [])]))
    platforms = list(dict.fromkeys(parent_platforms + [str(item) for item in (data.get("platforms") or [])]))
    return Chain(
        name=str(data["name"]),
        description=str(data.get("description", "") or ""),
        version=int(data.get("version", 1) or 1),
        tags=tags,
        platforms=platforms,
        defaults={**parent_defaults, **{str(k): str(v) for k, v in (data.get("defaults") or {}).items()}},
        vars={**parent_vars, **{str(k): str(v) for k, v in (data.get("vars") or {}).items()}},
        steps=steps,
        source=entry["source"],
        enabled=True,
        extends=parent_name,
        fallback=str(data.get("fallback", "") or ""),
        total_timeout=int(data.get("total_timeout", 0) or 0),
        raw_vars=tuple(str(item).strip() for item in (data.get("raw_vars") or []) if str(item).strip()),
    )


def _nonneg_int(raw: Any) -> int:
    """Return a clamped non-negative integer, or 0 on any malformed input."""
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return 0
    return max(0, value)


def _step_from_raw(item: dict[str, Any]) -> ChainStep:
    """Build one validated step from YAML data."""
    resolver = item.get("resolve_newest") or {}
    raw_exits = item.get("expect_exit", []) or []
    codes = [int(raw_exits)] if isinstance(raw_exits, int) and not isinstance(raw_exits, bool) else [
        int(code) for code in raw_exits if str(code).strip().isdigit()
    ]
    raw_budget = item.get("budget") or {}
    budget = {}
    if isinstance(raw_budget, dict):
        for key in ("attempts", "seconds"):
            value = raw_budget.get(key)
            if isinstance(value, int) and not isinstance(value, bool) and value > 0:
                budget[key] = value
    return ChainStep(
        run=str(item["run"]),
        id=str(item.get("id", "") or ""),
        phase=str(item.get("phase", "") or ""),
        description=str(item.get("description", "") or ""),
        when=str(item.get("when", "") or ""),
        skip_if_exists=str(item.get("skip_if_exists", "") or ""),
        skip_max_age=_nonneg_int(item.get("skip_max_age", 0)),
        resolve_newest_glob=str(resolver.get("glob", "") or ""),
        resolve_newest_as=str(resolver.get("as", "") or ""),
        timeout=int(item.get("timeout", 0) or 0),
        retries=int(item.get("retries", 0) or 0),
        continue_on_error=bool(item.get("continue_on_error", False)),
        capture=str(item.get("capture", "") or ""),
        capture_regex=str(item.get("capture_regex", "") or ""),
        capture_json=str(item.get("capture_json", "") or ""),
        expect=str(item.get("expect", "") or ""),
        expect_exit=codes,
        verify=str(item.get("verify", "") or ""),
        pre_check=str(item.get("pre_check", "") or ""),
        parallel=bool(item.get("parallel", False)),
        on_fail=str(item.get("on_fail", "") or ""),
        on_success=str(item.get("on_success", "") or ""),
        confirm=bool(item.get("confirm", False)),
        artifacts=[str(value) for value in (item.get("artifacts") or []) if str(value).strip()],
        sinks=[str(value) for value in (item.get("sinks") or []) if str(value).strip()],
        depends_on=[str(value).strip() for value in (item.get("depends_on") or []) if str(value).strip()],
        required_fields=[str(value).strip() for value in (item.get("required_fields") or []) if str(value).strip()],
        benign_alternatives=[
            str(value).strip() for value in (item.get("benign_alternatives") or []) if str(value).strip()
        ],
        evidence=[str(value).strip() for value in (item.get("evidence") or []) if str(value).strip()],
        evidence_sha256={
            str(path).strip(): str(digest).strip()
            for path, digest in (item.get("evidence_sha256") or {}).items()
            if str(path).strip() and str(digest).strip()
        },
        budget=budget,
    )


def get(name: str, chains_dir: Path | str = CHAINS_DIR) -> Chain | None:
    """Return one chain by name, or None."""
    return load_all(chains_dir).get((name or "").strip().lower())


def scan_all(chains_dir: Path | str = CHAINS_DIR) -> list[dict[str, Any]]:
    """List every chain file including disabled ones (for administration)."""
    if yaml is None:
        raise RuntimeError(_YAML_REQUIRED)
    directory = Path(chains_dir)
    rows: list[dict[str, Any]] = []
    if not directory.exists():
        return rows
    for path in sorted(directory.glob("*.yaml")):
        try:
            if path.stat().st_size > _MAX_YAML_BYTES:
                rows.append(
                    {
                        "name": path.stem,
                        "enabled": False,
                        "valid": False,
                        "error": "oversized file",
                        "source": str(path),
                    }
                )
                continue
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                data = yaml.safe_load(fh)
        except Exception as exc:
            rows.append(
                {
                    "name": path.stem,
                    "enabled": False,
                    "valid": False,
                    "error": f"unreadable: {exc}",
                    "source": str(path),
                }
            )
            continue
        errors = (
            validate_chain(data, filename=path.stem, chains_dir=directory)
            if isinstance(data, dict)
            else ["not a mapping"]
        )
        steps = data.get("steps") or [] if isinstance(data, dict) else []
        rows.append(
            {
                "name": str(data.get("name", path.stem)) if isinstance(data, dict) else path.stem,
                "enabled": bool(data.get("enabled", True)) if isinstance(data, dict) else False,
                "version": int(data.get("version", 1) or 1) if isinstance(data, dict) else 1,
                "extends": str(data.get("extends", "") or "") if isinstance(data, dict) else "",
                "fallback": str(data.get("fallback", "") or "") if isinstance(data, dict) else "",
                "steps": len(steps) if isinstance(steps, list) else 0,
                "playbook": str((data.get("defaults", {}) or {}).get("playbook", "")) if isinstance(data, dict) else "",
                "tags": list(data.get("tags") or []) if isinstance(data, dict) else [],
                "platforms": list(data.get("platforms") or []) if isinstance(data, dict) else [],
                "description": str(data.get("description", "") or "") if isinstance(data, dict) else "",
                "valid": not errors,
                "error": "; ".join(errors),
                "source": str(path),
            }
        )
    return rows


def set_enabled(name: str, enabled: bool, chains_dir: Path | str = CHAINS_DIR) -> bool:
    """Flip a chain's ``enabled`` flag in its YAML file (round-trip)."""
    if yaml is None:
        raise RuntimeError(_YAML_REQUIRED)
    wanted = (name or "").strip().lower()
    directory = Path(chains_dir)
    for path in sorted(directory.glob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        if str(data.get("name", "")).strip().lower() != wanted:
            continue
        data["enabled"] = bool(enabled)
        with path.open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    return False


def generate_for_playbook(
    engine_key: str,
    apt_display: str = "",
    description: str = "",
    chains_dir: Path | str = CHAINS_DIR,
    overwrite: bool = False,
) -> Path:
    """Write a per-APT chain file inheriting the base APT chain."""
    if yaml is None:
        raise RuntimeError(_YAML_REQUIRED)
    key = (engine_key or "").strip()
    if not key:
        raise ValueError("engine_key must not be empty")
    slug = re.sub(r"[^a-z0-9_]+", "_", key.lower()).strip("_")
    if not _NAME_RE.match(f"apt_{slug}"):
        raise ValueError(f"Cannot derive a chain name from playbook key: {engine_key!r}")
    directory = Path(chains_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"apt_{slug}.yaml"
    if path.exists() and not overwrite:
        raise FileExistsError(f"Chain file already exists: {path}")
    doc = {
        "name": f"apt_{slug}",
        "version": 2,
        "description": description or f"Full APT chain for {apt_display or key} (extends apt_chain).",
        "enabled": True,
        "extends": "apt_chain",
        "defaults": {"playbook": key},
    }
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(doc, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return path


__all__ = [
    "CHAINS_DIR",
    "Chain",
    "ChainStep",
    "evaluate_when",
    "generate_for_playbook",
    "get",
    "load_all",
    "scan_all",
    "set_enabled",
    "validate_chain",
]
