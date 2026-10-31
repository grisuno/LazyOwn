"""Reusable PoC verbs: standalone exploit scripts as loop-routable actions.

The ``modules`` directory ships standalone proof-of-concept scripts
(``49803.py``, ``CVE-2023-28432.py``, ``CVE-2018-15133.php``, ...). Until
now each was a one-shot file an operator had to remember and invoke by
hand: the autonomous loop, the apt_chain pipeline and the lazy
orchestrator could not reach a single one. This module turns every
catalogued PoC into a first-class verb:

- ``config/poc_verbs.yaml`` declares the script, interpreter, phase,
  risk, trigger keywords and argument templates;
- argument templates reference ``payload.json`` placeholders
  (``{rhost}``, ``{rport}``, ``{lhost}``, ``{lport}``, ``{user}``,
  ``{password}``, ``{domain}``, ``{url}``) so one declaration serves any
  target the operator assigns;
- :func:`render_argv` expands the templates into an ``argv`` list
  (never a shell string) plus the list of placeholders that stayed
  unresolved;
- :func:`propose_intents` maps discovered service tokens to
  ``lazy_poc run <name> <target>`` lines the planner and the daemon can
  queue, mirroring the lazyaddon trigger flow;
- the shell verb ``lazy_poc`` executes the rendered ``argv`` with the
  shared safe-subprocess primitive, so the PoCs ride the same Guard,
  scope and audit path as every other loop verb.

Parsing is fail-safe like the verb catalog: an unreadable or oversized
YAML degrades to an empty registry instead of breaking the loop.
"""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG_PATH = REPO_ROOT / "config" / "poc_verbs.yaml"

PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

MAX_CATALOG_BYTES = 200_000
CACHE_TTL_SEC = 2.0

PLACEHOLDER_ALIASES: dict[str, tuple[str, ...]] = {
    "rhost": ("rhost", "target"),
    "rport": ("rport",),
    "lhost": ("lhost",),
    "lport": ("lport",),
    "user": ("user", "username"),
    "password": ("password", "pass"),
    "domain": ("domain",),
    "url": ("url",),
}

INTERPRETERS: dict[str, tuple[str, ...]] = {
    "python3": ("python3",),
    "php": ("php",),
    "mitmdump": ("mitmdump",),
}

_VALID_PHASES = frozenset(
    {"recon", "enum", "exploit", "privesc", "lateral", "postexp", "exfil", "c2", "misc"}
)
_VALID_RISKS = frozenset({"safe", "exploit", "dangerous"})

_LOCK = threading.Lock()
_CACHE: dict[str, object] = {"at": 0.0, "path": None, "verbs": None}


@dataclass(frozen=True)
class PocArg:
    """One rendered argument of a PoC verb.

    Attributes:
        flag: Option flag prepended to the value (``-u``); may be empty
            for positional arguments.
        value: Template or literal; ``{placeholder}`` tokens expand from
            the operator payload.
        default: Literal used when every placeholder inside ``value``
            stays unresolved.
    """

    flag: str = ""
    value: str = ""
    default: str = ""


@dataclass(frozen=True)
class PocVerb:
    """One catalogued proof-of-concept verb.

    Attributes:
        name: Verb name used in ``lazy_poc run <name>``.
        title: Human title.
        description: One-line description.
        script: Script path relative to ``modules/``.
        interpreter: Runner key (``python3``/``php``/``mitmdump``).
        phase: Kill-chain phase.
        risk: Risk class routed by the Guard.
        os: Target platform (``any``/``linux``/``windows``).
        enabled: Whether the loop may propose and run it.
        triggers: Service/keyword tokens that make the selector fire.
        requires: Binaries that must exist before execution.
        args: Ordered argument templates.
        timeout_sec: Per-run wall-clock cap.
    """

    name: str
    title: str = ""
    description: str = ""
    script: str = ""
    interpreter: str = "python3"
    phase: str = "exploit"
    risk: str = "exploit"
    os: str = "any"
    enabled: bool = True
    triggers: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    args: tuple[PocArg, ...] = ()
    proposal_overrides: tuple[tuple[str, str], ...] = ()
    timeout_sec: float = 120.0

    def to_dict(self) -> dict:
        """Return a JSON-serialisable summary for the orchestrator surfaces."""
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "script": self.script,
            "interpreter": self.interpreter,
            "phase": self.phase,
            "risk": self.risk,
            "os": self.os,
            "enabled": self.enabled,
            "triggers": list(self.triggers),
            "requires": list(self.requires),
            "args": [
                {"flag": arg.flag, "value": arg.value, "default": arg.default} for arg in self.args
            ],
            "proposal_overrides": dict(self.proposal_overrides),
            "timeout_sec": self.timeout_sec,
        }


@dataclass(frozen=True)
class RenderedPoc:
    """The expansion result of one PoC verb against operator input.

    Attributes:
        verb: Source :class:`PocVerb`.
        argv: Full ``argv`` list ready for ``subprocess`` (``shell=False``).
        missing: Placeholders that stayed unresolved (run is refused).
        resolved: Placeholder values actually used, masked secrets aside.
    """

    verb: PocVerb
    argv: tuple[str, ...]
    missing: tuple[str, ...]
    resolved: dict[str, str] = field(default_factory=dict)


def _placeholder_names(template: str) -> list[str]:
    """Return every ``{placeholder}`` name a template references."""
    return PLACEHOLDER_RE.findall(template or "")


def _resolve_placeholder(name: str, overrides: dict[str, str], params: dict) -> str:
    """Resolve one placeholder from overrides then the operator payload.

    Args:
        name: Placeholder name without braces.
        overrides: Explicit ``key=value`` runtime overrides.
        params: ``payload.json`` mapping.

    Returns:
        The resolved value, or an empty string when unknown.
    """
    for key in PLACEHOLDER_ALIASES.get(name, (name,)):
        if key in overrides and str(overrides[key]).strip():
            return str(overrides[key])
    for key in PLACEHOLDER_ALIASES.get(name, (name,)):
        value = params.get(key)
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _parse_args(raw: object) -> tuple[PocArg, ...]:
    """Normalise the YAML ``args`` list into typed specs."""
    if not isinstance(raw, list):
        return ()
    out: list[PocArg] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        flag = str(item.get("flag", "") or "").strip()
        value = str(item.get("value", "") or "").strip()
        default = str(item.get("default", "") or "").strip()
        if not flag and not value:
            continue
        out.append(PocArg(flag=flag, value=value, default=default))
    return tuple(out[:16])


def _parse_verb(name: str, raw: dict) -> PocVerb | None:
    """Build one :class:`PocVerb` from a YAML mapping, or None when invalid."""
    script = str(raw.get("script", "") or "").strip()
    if not script:
        return None
    interpreter = str(raw.get("interpreter", "python3") or "python3").strip().lower()
    if interpreter not in INTERPRETERS:
        return None
    phase = str(raw.get("phase", "exploit") or "exploit").strip().lower()
    risk = str(raw.get("risk", "exploit") or "exploit").strip().lower()
    try:
        timeout = float(raw.get("timeout_sec", 120) or 120)
    except (TypeError, ValueError):
        timeout = 120.0
    return PocVerb(
        name=name,
        title=str(raw.get("title", "") or name)[:120],
        description=str(raw.get("description", "") or "")[:400],
        script=script,
        interpreter=interpreter,
        phase=phase if phase in _VALID_PHASES else "exploit",
        risk=risk if risk in _VALID_RISKS else "exploit",
        os=str(raw.get("os", "any") or "any").strip().lower(),
        enabled=bool(raw.get("enabled", True)),
        triggers=tuple(
            str(token).strip().lower()
            for token in (raw.get("triggers") or [])
            if str(token).strip()
        )[:12],
        requires=tuple(
            str(binary).strip()
            for binary in (raw.get("requires") or [])
            if str(binary).strip()
        )[:8],
        args=_parse_args(raw.get("args")),
        proposal_overrides=tuple(
            (str(key).strip().lower(), str(value).strip())
            for key, value in (raw.get("proposal_overrides") or {}).items()
            if str(key).strip()
        )[:8],
        timeout_sec=max(10.0, min(timeout, 1800.0)),
    )


def _load_catalog(path: Path) -> dict[str, PocVerb]:
    """Read and parse the PoC catalog YAML into typed verbs."""
    if yaml is None:
        return {}
    try:
        if path.stat().st_size > MAX_CATALOG_BYTES:
            return {}
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    raw_verbs = data.get("pocs") if isinstance(data.get("pocs"), dict) else data.get("verbs")
    if not isinstance(raw_verbs, dict):
        return {}
    out: dict[str, PocVerb] = {}
    for name, raw in raw_verbs.items():
        key = str(name or "").strip().lower().replace(" ", "_")
        if not key or not isinstance(raw, dict):
            continue
        verb = _parse_verb(key, raw)
        if verb is not None:
            out[key] = verb
    return out


def poc_verbs(catalog_path: str | Path | None = None) -> dict[str, PocVerb]:
    """Return the catalogued PoC verbs (cached, fail-safe).

    Args:
        catalog_path: Optional override path (tests and sandboxes).

    Returns:
        Mapping of verb name to :class:`PocVerb`; empty when no catalog
        is readable.
    """
    path = Path(catalog_path) if catalog_path is not None else DEFAULT_CATALOG_PATH
    if path.name == DEFAULT_CATALOG_PATH.name and path.parent == DEFAULT_CATALOG_PATH.parent:
        path = DEFAULT_CATALOG_PATH
    key = str(path)
    import time

    with _LOCK:
        cached = _CACHE["verbs"]
        fresh = cached is not None and _CACHE["path"] == key and (time.monotonic() - float(_CACHE["at"])) < CACHE_TTL_SEC
        if fresh:
            return dict(cached)
    verbs = _load_catalog(path)
    with _LOCK:
        _CACHE["verbs"] = dict(verbs)
        _CACHE["path"] = key
        _CACHE["at"] = time.monotonic()
    return verbs


def get_poc(name: str, catalog_path: str | Path | None = None) -> PocVerb | None:
    """Return one PoC verb by name, or None when unknown/disabled-less.

    Args:
        name: Verb name as used in ``lazy_poc run <name>``.
        catalog_path: Optional catalog override.

    Returns:
        The :class:`PocVerb`, or None when absent.
    """
    return poc_verbs(catalog_path).get(str(name or "").strip().lower())


def interpreter_argv(verb: PocVerb) -> tuple[str, ...]:
    """Return the ``argv`` prefix that launches the PoC script.

    ``mitmdump`` addons run as ``mitmdump -s <script>``; every other
    interpreter runs the script directly.
    """
    script = str(REPO_ROOT / "modules" / verb.script)
    if verb.interpreter == "mitmdump":
        return ("mitmdump", "-s", script)
    return (verb.interpreter, script)


def render_argv(
    verb: PocVerb,
    params: dict,
    target: str = "",
    overrides: dict[str, str] | None = None,
) -> RenderedPoc:
    """Expand one PoC verb into a safe ``argv`` list.

    Resolution order per placeholder: runtime overrides, the positional
    target (binds ``{rhost}``), then ``payload.json`` values through the
    alias table. When every placeholder in a template resolves empty the
    literal ``default`` applies; an argument that still resolves empty
    is dropped so half-configured PoCs never run with stale flags.

    Args:
        verb: The catalogued PoC.
        params: Operator payload mapping (``payload.json``).
        target: Target host that overrides ``{rhost}``.
        overrides: Explicit runtime ``key=value`` overrides.

    Returns:
        A :class:`RenderedPoc`; ``missing`` lists unresolved placeholder
        names that carry no default, which the caller treats as refuse.
    """
    merged_overrides = {str(k).lower(): str(v) for k, v in (overrides or {}).items()}
    if target:
        merged_overrides.setdefault("rhost", str(target))
    resolved: dict[str, str] = {}
    missing: list[str] = []
    for name in sorted({n for arg in verb.args for n in _placeholder_names(arg.value)}):
        value = _resolve_placeholder(name, merged_overrides, params or {})
        if value:
            resolved[name] = value
    argv: list[str] = list(interpreter_argv(verb))
    for arg in verb.args:
        rendered = PLACEHOLDER_RE.sub(
            lambda match: resolved.get(match.group(1), match.group(0)), arg.value
        )
        still_unresolved = _placeholder_names(rendered)
        if still_unresolved:
            if arg.default:
                rendered = arg.default
            else:
                for name in still_unresolved:
                    if name not in missing:
                        missing.append(name)
                continue
        if arg.flag:
            argv.extend((arg.flag, rendered))
        elif rendered:
            argv.append(rendered)
    masked = {key: (value if key not in ("password", "pass") else "***") for key, value in resolved.items()}
    return RenderedPoc(verb=verb, argv=tuple(argv), missing=tuple(missing), resolved=masked)


def missing_requirements(verb: PocVerb) -> list[str]:
    """Return the PoC's required binaries that are absent on this host."""
    import shutil

    out: list[str] = []
    for binary in verb.requires:
        if shutil.which(binary) is None:
            out.append(binary)
    interpreter_binary = INTERPRETERS.get(verb.interpreter, (verb.interpreter,))[0]
    if shutil.which(interpreter_binary) is None:
        out.append(interpreter_binary)
    script_path = REPO_ROOT / "modules" / verb.script
    if not script_path.is_file():
        out.append(f"script:{verb.script}")
    return out


def propose_intents(
    service_texts: list[str] | tuple[str, ...],
    target: str = "",
    limit: int = 4,
    catalog_path: str | Path | None = None,
) -> list[str]:
    """Propose ``lazy_poc run`` intent lines for matching service tokens.

    Mirrors the lazyaddon trigger flow: every enabled PoC whose trigger
    token appears in the discovered service text becomes a
    ``lazy_poc run <name> <target>`` line the planner can queue. Known
    lines are never duplicated, and the cap keeps one service burst from
    flooding the round.

    Args:
        service_texts: Discovered service strings for the target.
        target: Host under test appended to the intent line.
        limit: Maximum intents returned.

    Returns:
        Intent summary lines, most specific trigger first.
    """
    text = " ".join(str(item or "") for item in service_texts).lower()
    tokens = set(re.findall(r"[a-z0-9]+", text))
    out: list[str] = []
    for verb in poc_verbs(catalog_path).values():
        if not verb.enabled or not verb.triggers:
            continue
        if not any(trigger in tokens for trigger in verb.triggers):
            continue
        line = f"lazy_poc run {verb.name} {target}".strip()
        for key, value in verb.proposal_overrides:
            line = f"{line} {key}={value}"
        if line not in out:
            out.append(line)
        if len(out) >= max(1, int(limit)):
            break
    return out


def verbs_summary(catalog_path: str | Path | None = None) -> list[dict]:
    """Return every PoC verb as a dict for TUI and MCP surfaces."""
    return [verb.to_dict() for verb in poc_verbs(catalog_path).values()]


__all__ = [
    "PocArg",
    "PocVerb",
    "RenderedPoc",
    "get_poc",
    "interpreter_argv",
    "missing_requirements",
    "poc_verbs",
    "propose_intents",
    "render_argv",
    "verbs_summary",
]
