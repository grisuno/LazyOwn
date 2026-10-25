"""Typed verb manifests - semantics for routable shell verbs.

Every routable shell command is a verb. Today the registry knows only
names, phases and keyword strings (``config/verbs.yaml``, the built-in
``AUTO_VERBS`` and the command index). This module stores the missing
signature: what a verb requires from the world model before it can run,
what facts it produces, what it costs and how loud it is.

Manifest document (``config/verb_manifests.yaml``)::

    manifests:
      lazynmap:
        version: 1
        title: Nmap service scan
        phase: recon
        description: Discover open ports and service versions.
        mitre: [T1046]
        keywords: [scan, ports, services]
        needs_target: true
        cost: {tokens: 200, seconds: 300, toolcalls: 1}
        noise: {weight: 0.7, why: "full connect scan rings network sensors.",
                sigma: [LAZ-010]}
        preconditions:
          - {fact: host_known, host: "{target}"}
        effects:
          - {fact: services_discovered, host: "{target}"}
          - {fact: scan_completed, host: "{target}"}
        idempotent: true

Facts form a closed vocabulary consumed by three surfaces:

- ``plan_check``: semantic chain dry-runs (``apt_chain --dry-run`` stops
  being pure token resolution and reports proven-unmet preconditions).
- the detection oracle: ``noise.weight`` is the operator prior that
  profiles combine with the oracle probability.
- the planner: ``cost`` and ``keywords`` rank proposals beyond text match.

Parsing is fail-safe: an invalid manifest logs and disappears instead of
breaking the loop, mirroring :mod:`modules.verb_catalog` behaviour.
"""

from __future__ import annotations

import logging
import re
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from modules.chain_registry import ChainStep

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

log = logging.getLogger("verb_manifest")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST_PATH = REPO_ROOT / "config" / "verb_manifests.yaml"

_MAX_MANIFEST_BYTES = 200_000
_CACHE_TTL_SEC = 2.0
_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, object] = {"at": 0.0, "path": None, "manifests": None}

_TOKEN_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

_FACT_FIELDS = ("host", "port", "service", "os", "scope", "level", "kind", "path", "name", "state")
_FACT_IDS = frozenset(
    {
        "host_known",
        "service_open",
        "os",
        "credentials",
        "access",
        "session",
        "artifact",
        "scan_completed",
        "services_discovered",
        "min_version_collected",
        "c2",
        "fact",
    }
)
_MAX_FACTS_PER_VERB = 16
_MAX_KEYWORDS_PER_VERB = 32
_COST_RANGES = ((0, 2_000_000, "tokens"), (0, 86_400, "seconds"), (0, 10_000, "toolcalls"))


@dataclass(frozen=True)
class ManifestCost:
    """Operator-declared resource cost of one verb invocation.

    Args:
        tokens: Model tokens the verb output typically consumes.
        seconds: Typical wall clock in seconds.
        toolcalls: Number of tool executions carried out.
    """

    tokens: int = 0
    seconds: float = 0.0
    toolcalls: int = 1


@dataclass(frozen=True)
class ManifestNoise:
    """Operator prior of how loud the verb is, before the oracle speaks.

    Args:
        weight: Detection prior in [0.0, 1.0] (0 silent, 1 trivially seen).
        why: One-line reason the operator assigned this weight.
        sigma: Sigma rule ids the verb typically trips.
    """

    weight: float = 0.0
    why: str = ""
    sigma: tuple[str, ...] = ()


@dataclass(frozen=True)
class FactPredicate:
    """One fact the world model may hold, with optional corner arguments.

    Args:
        fact: Closed-vocabulary fact id (see ``_FACT_IDS``).
        host: Host the fact binds to, ``"{target}"`` tolerated as wildcard.
        port: Optional port string.
        service: Optional service name.
        os: Optional OS family (linux, windows, macos, unix).
        scope: Optional credential scope (any, domain, host).
        level: Optional access level (none, user, shell, root).
        kind: Optional session kind (web, shell, c2, db).
        path: Optional artifact path.
        name: Optional free-form fact name (for ``fact`` ids).
        state: Optional state string (e.g. c2 running).
    """

    fact: str
    host: str = ""
    port: str = ""
    service: str = ""
    os: str = ""
    scope: str = ""
    level: str = ""
    kind: str = ""
    path: str = ""
    name: str = ""
    state: str = ""

    def args(self) -> dict[str, str]:
        """Return the set corner arguments."""
        return {key: str(getattr(self, key)) for key in _FACT_FIELDS if getattr(self, key)}

    def is_wild(self, key: str) -> bool:
        """Return True when that argument is a ``{token}`` wildcard."""
        value = str(getattr(self, key))
        return _TOKEN_RE.fullmatch(value) is not None

    def matches(self, other: FactPredicate) -> bool:
        """Return True when this fact instance satisfies the other.

        Args:
            other: Requirement predicate; a missing or wildcard argument
                matches anything, a literal must agree exactly (hosts are
                compared case-insensitively).

        Returns:
            True when every shared field is compatible.
        """
        if other.fact != self.fact:
            return False
        for key in _FACT_FIELDS:
            wanted = str(getattr(other, key))
            have = str(getattr(self, key))
            if not wanted or other.is_wild(key):
                continue
            if key == "host":
                if have.lower() != wanted.lower():
                    return False
            elif have != wanted:
                return False
        return True


@dataclass(frozen=True)
class VerbManifest:
    """Typed signature of one shell verb.

    Args:
        verb: Shell command name (``do_<verb>`` or binary this wraps).
        version: Manifest schema version (currently 1).
        title: Short human title.
        phase: Canonical kill-chain phase.
        description: One-line description.
        mitre: MITRE ATT&CK technique ids.
        keywords: Planner keyword signals.
        needs_target: Whether the verb binds a loop target.
        cost: Declared resource cost.
        noise: Declared detection-noise prior.
        preconditions: Facts required before a call is meaningful.
        effects: Facts a successful call produces.
        idempotent: Re-runs are safe (skip/steal-facts decisions).
    """

    verb: str
    version: int = 1
    title: str = ""
    phase: str = ""
    description: str = ""
    mitre: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    needs_target: bool = True
    cost: ManifestCost = ManifestCost()
    noise: ManifestNoise = ManifestNoise()
    preconditions: tuple[FactPredicate, ...] = ()
    effects: tuple[FactPredicate, ...] = ()
    idempotent: bool = False


def parse_predicate(data: object) -> FactPredicate:
    """Parse one predicate mapping into a FactPredicate.

    Args:
        data: YAML/JSON mapping with ``fact`` plus optional corner fields.

    Returns:
        The parsed predicate.

    Raises:
        ValueError: When the entry is not a mapping, ``fact`` is missing
            or the fact id is outside the closed vocabulary.
    """
    if not isinstance(data, dict):
        raise ValueError("predicate must be a mapping")
    fact = str(data.get("fact", "") or "").strip()
    if fact not in _FACT_IDS:
        raise ValueError(f"unknown fact id: {fact!r}")
    fields: dict[str, str] = {}
    for key in _FACT_FIELDS:
        value = data.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        if len(text) > 200:
            raise ValueError(f"predicate field {key!r} too long")
        fields[key] = text
    return FactPredicate(fact=fact, **fields)


def _parse_cost(data: object) -> ManifestCost:
    """Return declared cost, tolerating missing or malformed entries.

    Args:
        data: Cost mapping from the YAML document.

    Returns:
        A filtered ManifestCost.
    """
    if not isinstance(data, dict):
        return ManifestCost()
    raw = {key: data.get(key) for key in ("tokens", "seconds", "toolcalls")}
    try:
        return ManifestCost(
            tokens=int(raw["tokens"] or 0),
            seconds=float(raw["seconds"] or 0.0),
            toolcalls=int(raw["toolcalls"] or 1),
        )
    except (TypeError, ValueError):
        return ManifestCost()


def _parse_noise(data: object) -> ManifestNoise:
    """Return declared noise prior, dropping malformed weight values.

    Args:
        data: Noise mapping from the YAML document.

    Returns:
        A filtered ManifestNoise.
    """
    if not isinstance(data, dict):
        return ManifestNoise()
    try:
        weight = min(1.0, max(0.0, float(data.get("weight") or 0.0)))
    except (TypeError, ValueError):
        weight = 0.0
    why = str(data.get("why", "") or "")[:300]
    sigma = tuple(str(item)[:40] for item in (data.get("sigma") or []) if str(item)[:40])
    return ManifestNoise(weight=weight, why=why, sigma=sigma)


def parse_manifest(verb: str, data: object) -> VerbManifest:
    """Validate and parse one manifest document entry.

    Args:
        verb: Shell verb the entry describes.
        data: Raw YAML mapping from the manifest file.

    Returns:
        The parsed manifest.

    Raises:
        ValueError: When the entry violates the schema.
    """
    verb = str(verb or "").strip().lower()
    if not re.match(r"^[a-z][a-z0-9_]{0,63}$", verb):
        raise ValueError(f"invalid verb name: {verb!r}")
    if not isinstance(data, dict):
        raise ValueError("manifest must be a mapping")
    version = data.get("version", 1)
    if isinstance(version, bool) or int(version) != 1:
        raise ValueError(f"unsupported manifest version: {version!r}")
    pre = tuple(parse_predicate(item) for item in (data.get("preconditions") or [])[:_MAX_FACTS_PER_VERB])
    eff = tuple(parse_predicate(item) for item in (data.get("effects") or [])[:_MAX_FACTS_PER_VERB])
    keywords = tuple(str(item)[:40] for item in (data.get("keywords") or [])[:_MAX_KEYWORDS_PER_VERB])
    mitre = tuple(str(item)[:20] for item in (data.get("mitre") or [])[:16])
    return VerbManifest(
        verb=verb,
        version=1,
        title=str(data.get("title", "") or "")[:120],
        phase=str(data.get("phase", "") or "")[:24],
        description=str(data.get("description", "") or "")[:300],
        mitre=mitre,
        keywords=keywords,
        needs_target=bool(data.get("needs_target", True)),
        cost=_parse_cost(data.get("cost")),
        noise=_parse_noise(data.get("noise")),
        preconditions=pre,
        effects=eff,
        idempotent=bool(data.get("idempotent", False)),
    )


def _load_document(path: Path) -> dict[str, VerbManifest]:
    """Read and parse the manifest file; any problem yields an empty view.

    Args:
        path: YAML manifest path.

    Returns:
        Mapping of verb to parsed manifest (empty when absent or invalid).
    """
    if yaml is None or not path.is_file():
        return {}
    if path.stat().st_size > _MAX_MANIFEST_BYTES:
        log.warning("verb manifest file too large: %s", path)
        return {}
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - yaml may raise many things
        log.warning("unreadable verb manifest %s: %s", path, exc)
        return {}
    manifests: dict[str, VerbManifest] = {}
    entries = raw.get("manifests") if isinstance(raw, dict) else None
    if entries is None:
        entries = raw if isinstance(raw, dict) else {}
    for name, data in entries.items():
        try:
            manifest = parse_manifest(str(name), data)
        except (ValueError, TypeError) as exc:
            log.warning("skipping verb manifest %r: %s", name, exc)
            continue
        manifests[manifest.verb] = manifest
    return manifests


def manifests(path: Path | str | None = None) -> dict[str, VerbManifest]:
    """Return parsed manifests with a small TTL cache.

    Args:
        path: Override the default manifest file (tests, alt configs).

    Returns:
        Mapping verb -> VerbManifest; empty on any failure.
    """
    chosen = Path(path or DEFAULT_MANIFEST_PATH)
    with _CACHE_LOCK:
        hit = (
            _CACHE["path"] == chosen
            and isinstance(_CACHE["manifests"], dict)
            and (time.time() - float(_CACHE["at"])) < _CACHE_TTL_SEC
        )
        if hit:
            return _CACHE["manifests"]  # type: ignore[return-value]
        loaded = _load_document(chosen)
        _CACHE["path"] = chosen
        _CACHE["manifests"] = loaded
        _CACHE["at"] = time.time()
        return dict(loaded)


def manifest_for(verb: str, path: Path | str | None = None) -> VerbManifest | None:
    """Return the manifest of one verb, or None when untyped.

    Args:
        verb: Shell command name.
        path: Override the default manifest file.

    Returns:
        Parsed VerbManifest when declared, else None.
    """
    if not verb:
        return None
    return manifests(path).get(str(verb).strip().lower())


def facts_for_target(host: str) -> list[FactPredicate]:
    """Project the world model facts of one host into predicates.

    Args:
        host: Target host string.

    Returns:
        Read-only fact list; empty when the world model knows nothing.

    Raises:
        OSError: Never, failures degrade to an empty list.
    """
    facts: list[FactPredicate] = [FactPredicate(fact="host_known", host=host or "{target}")]
    try:
        from modules.world_model import get_world_model

        wm = get_world_model()
        entry = wm.get_host(host or "")
        credentials = list(wm.snapshot().get("credentials") or [])
    except Exception:  # noqa: BLE001 - the world model must never block planning
        return facts
    if entry is None:
        return facts
    for service in (entry.services or {}).values():
        facts.append(
            FactPredicate(
                fact="service_open",
                host=host,
                port=str(getattr(service, "port", "") or ""),
                service=str(getattr(service, "name", "") or "").lower(),
            )
        )
    os_hint = str(getattr(entry, "os_hint", "") or "").lower()
    for family in ("linux", "windows", "macos", "unix"):
        if family in os_hint:
            facts.append(FactPredicate(fact="os", host=host, os=family))
            break
    state = str(getattr(entry.state, "value", entry.state) or "").lower()
    if state in ("unscanned", "scanned", "enumerated"):
        facts.append(FactPredicate(fact="scan_completed", host=host))
        if state == "enumerated":
            facts.append(FactPredicate(fact="services_discovered", host=host))
    if state in ("exploited", "owned"):
        facts.append(FactPredicate(fact="access", host=host, level="shell"))
    if state == "owned":
        facts.append(FactPredicate(fact="access", host=host, level="root"))
    for credential in credentials:
        if not credential.get("confirmed", False):
            continue
        credential_host = str(credential.get("host", "") or "").lower()
        if not credential_host or credential_host in (str(host).lower(), "{target}") or host in credential_host:
            facts.append(FactPredicate(fact="credentials", host=host, scope="any"))
            break
    return facts


def plan_check(
    steps: list[ChainStep],
    tokens: dict[str, str],
    path: Path | str | None = None,
    facts: list[FactPredicate] | None = None,
) -> list[str]:
    """Check a chain semantically: every typed precondition must be supplied.

    Args:
        steps: The chain steps in execution order.
        tokens: Resolved variables (the chain target lives here).
        path: Optional manifest file override.
        facts: Known facts injection (tests, alternative fact sources);
            defaults to the world model projection of the target.

    Returns:
        Warning strings for provably unmet preconditions. Untyped verbs
        are summarised, never individually nags, since the store is
        sparse by design.
    """
    store = manifests(path)
    if not store:
        return []
    target = str(tokens.get("target", "") or "")
    known: list[FactPredicate] = []
    if facts is None and target:
        known.extend(facts_for_target(target))
    known.extend(facts or [])
    problems: list[str] = []
    untyped = 0
    for step in steps:
        fields = str(step.run).strip().split()
        if not fields:
            untyped += 1
            continue
        if fields[0].lower() == "sudo" and len(fields) > 1:
            fields = fields[1:]
        verb = fields[0].lower()
        manifest = store.get(verb)
        if manifest is None:
            untyped += 1
            continue
        for required in manifest.preconditions:
            met = any(candidate.matches(required) for candidate in known)
            if not met:
                args = " ".join(f"{key}={value}" for key, value in required.args().items())
                text = args or f"target={target or '?'}"
                problems.append(f"{step.identifier} ({verb}) needs {required.fact} {text}".strip())
        for produced in manifest.effects:
            known.append(produced)
    if untyped:
        problems.append(f"{untyped} untyped verb(s) not checked")
    return problems


def coverage(total_verbs: int, path: Path | str | None = None) -> dict[str, object]:
    """Summarise manifest coverage for registry reporting.

    Args:
        total_verbs: Size of the current shell command registry.
        path: Optional manifest file override.

    Returns:
        Mapping with typed count, untyped remainder and per-verb rows.
    """
    store = manifests(path)
    rows = [
        {
            "verb": manifest.verb,
            "phase": manifest.phase,
            "preconditions": len(manifest.preconditions),
            "effects": len(manifest.effects),
            "noise": manifest.noise.weight,
            "cost_tokens": manifest.cost.tokens,
            "idempotent": manifest.idempotent,
        }
        for manifest in sorted(store.values(), key=lambda item: item.verb)
    ]
    return {
        "total_verbs": int(total_verbs),
        "typed": len(store),
        "untyped": max(0, total_verbs - len(store)),
        "rows": rows,
    }
