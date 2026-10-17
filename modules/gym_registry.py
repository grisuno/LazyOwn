"""Gym definitions and persistent run state.

Gym challenges are YAML files under ``gyms/``. Runtime runs are stored in
the world model under the allowlisted ``gyms`` section, so ``gym status``,
``gym stop`` and the orchestrator Gyms tab all read the same state across
sessions.

State contract::

    {
      "version": 1,
      "next_id": 4,
      "active": {
        "gym0001": {
          "run_id": "gym0001",
          "challenge_id": "first_blood_web",
          "name": "First Blood - Web",
          "operator": "grisun0",
          "started_at": 1710000000.0,
          "target": "172.17.0.2",
          "status": "active"
        }
      },
      "legacy_imported": ["active_grisun0.json"]
    }

The module never accepts paths from operators: definitions are addressed
by slug and confined to :data:`GYMS_DIR`. Writes are atomic and YAML is
validated before it reaches disk.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import secrets
import threading
import time
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is a hard dependency
    yaml = None  # type: ignore

log = logging.getLogger("gym_registry")

_STATE_LOCK = threading.RLock()

BASE_DIR = Path(__file__).resolve().parent.parent
GYMS_DIR = BASE_DIR / "gyms"
GYM_DIR = BASE_DIR / "sessions" / "gym"
STATE_KEY = "gyms"
STATE_VERSION = 1
MAX_YAML_BYTES = 200_000
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_RUN_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_DIFFICULTIES = frozenset({"easy", "medium", "hard"})
_PHASES = (
    "recon",
    "scan",
    "enum",
    "exploit",
    "cred",
    "postexp",
    "privesc",
    "lateral",
    "exfil",
    "c2",
)
_PHASE_SET = frozenset(_PHASES)
_DEFAULT_NUMBERS = {
    "max_points": 1000,
    "speed_bonus_max": 300,
    "stealth_bonus_max": 200,
    "technique_diversity_bonus": 200,
    "elo_bonus": 100,
}


def _yaml_module():
    """Return PyYAML or raise a clear runtime error."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for gym administration")
    return yaml


def slugify(value: str) -> str:
    """Return a safe gym identifier.

    Args:
        value: Operator-supplied identifier.

    Returns:
        Lowercase ``[a-z0-9_-]`` slug capped at 64 characters.
    """
    text = re.sub(r"[^a-z0-9_-]+", "_", str(value or "").strip().lower()).strip("_-")
    return text[:64]


# ---------------------------------------------------------------------------
# Definition validation and loading
# ---------------------------------------------------------------------------


def validate_definition(data: Any, filename: str = "") -> list[str]:
    """Validate one gym definition mapping.

    Args:
        data: Parsed YAML document.
        filename: File stem; when present it must equal the definition id.

    Returns:
        Human-readable errors; an empty list means valid.
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["gym definition must be a mapping"]
    gym_id = str(data.get("id", "") or "").strip()
    if not gym_id or not _ID_RE.match(gym_id):
        errors.append(f"invalid id: {gym_id!r}")
    elif filename and gym_id != filename:
        errors.append(f"id {gym_id!r} does not match filename {filename!r}")
    for key in ("name", "scenario", "objective", "description", "success_check", "chain"):
        value = data.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(f"{key} must be a string")
    difficulty = str(data.get("difficulty", "") or "").strip().lower()
    if difficulty not in _DIFFICULTIES:
        errors.append(f"difficulty must be one of {sorted(_DIFFICULTIES)}")
    phases = data.get("phases")
    if not isinstance(phases, list) or not phases:
        errors.append("phases must be a non-empty list")
    else:
        for phase in phases:
            if str(phase) not in _PHASE_SET:
                errors.append(f"unknown phase: {phase!r}")
    for key in ("required_techniques", "bonus_techniques", "hints"):
        value = data.get(key, [])
        if value is not None and not isinstance(value, list):
            errors.append(f"{key} must be a list")
        elif isinstance(value, list) and any(not isinstance(item, str) for item in value):
            errors.append(f"{key} entries must be strings")
    for key, default in _DEFAULT_NUMBERS.items():
        value = data.get(key, default)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"{key} must be a non-negative integer")
    return errors


def definition_path(gym_id: str, directory: Path | str | None = None) -> Path:
    """Resolve one gym YAML file inside the gyms directory.

    Args:
        gym_id: Gym identifier or file name.
        directory: Override for tests; defaults to :data:`GYMS_DIR`.

    Returns:
        The confined path.

    Raises:
        ValueError: Invalid or escaping identifier.
    """
    root = Path(directory or GYMS_DIR).resolve()
    clean = slugify(Path(str(gym_id or "").strip()).stem)
    if not clean or not _ID_RE.match(clean):
        raise ValueError(f"invalid gym id: {gym_id!r}")
    target = (root / f"{clean}.yaml").resolve()
    if target.parent != root:
        raise ValueError(f"gym path escapes {root}: {gym_id!r}")
    return target


def _read_yaml(path: Path) -> dict[str, Any]:
    """Read one YAML mapping with a size cap."""
    target = Path(path)
    if not target.is_file() or target.stat().st_size > MAX_YAML_BYTES:
        return {}
    module = _yaml_module()
    data = module.safe_load(target.read_text(encoding="utf-8", errors="replace"))
    return dict(data) if isinstance(data, dict) else {}


def _normalize_definition(data: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic definition with every documented field."""
    definition = dict(data)
    definition["id"] = str(data.get("id", "") or "").strip()
    definition["name"] = str(data.get("name", "") or definition["id"])
    definition["description"] = str(data.get("description", "") or "")
    definition["scenario"] = str(data.get("scenario", "") or "")
    definition["objective"] = str(data.get("objective", "") or "")
    definition["difficulty"] = str(data.get("difficulty", "") or "easy").lower()
    definition["chain"] = str(data.get("chain", "") or "")
    definition["phases"] = [str(item) for item in (data.get("phases") or [])]
    for key in ("required_techniques", "bonus_techniques", "hints"):
        definition[key] = [str(item) for item in (data.get(key) or [])]
    for key, default in _DEFAULT_NUMBERS.items():
        definition[key] = int(data.get(key, default) or 0)
    definition["success_check"] = str(data.get("success_check", "") or "")
    return definition


def load_definitions(directory: Path | str | None = None) -> dict[str, dict[str, Any]]:
    """Load every valid gym definition.

    Args:
        directory: Override for tests; defaults to :data:`GYMS_DIR`.

    Returns:
        Mapping of gym id to normalized definition. Invalid files are
        logged and skipped, never raised.
    """
    root = Path(directory or GYMS_DIR)
    definitions: dict[str, dict[str, Any]] = {}
    if not root.is_dir():
        return definitions
    for path in sorted(root.glob("*.yaml")):
        if path.is_symlink():
            log.warning("skipping gym definition symlink: %s", path)
            continue
        try:
            data = _read_yaml(path)
        except Exception as exc:
            log.warning("gym definition unreadable at %s: %s", path, exc)
            continue
        errors = validate_definition(data, filename=path.stem)
        if errors:
            log.warning("gym definition invalid at %s: %s", path, "; ".join(errors))
            continue
        normalized = _normalize_definition(data)
        definitions[normalized["id"]] = normalized
    return definitions


def scan_definitions(directory: Path | str | None = None) -> list[dict[str, Any]]:
    """Return one row per YAML file, including invalid files.

    Args:
        directory: Override for tests; defaults to :data:`GYMS_DIR`.

    Returns:
        Rows with ``file``, ``path``, ``id``, ``name`` and ``error``.
    """
    root = Path(directory or GYMS_DIR)
    rows: list[dict[str, Any]] = []
    if not root.is_dir():
        return rows
    for path in sorted(root.glob("*.yaml")):
        if path.is_symlink():
            log.warning("skipping gym definition symlink: %s", path)
            continue
        try:
            data = _read_yaml(path)
            errors = validate_definition(data, filename=path.stem)
        except Exception as exc:
            data, errors = {}, [str(exc)]
        normalized = _normalize_definition(data) if not errors else {}
        rows.append(
            {
                "file": path.name,
                "path": str(path),
                "id": normalized.get("id", path.stem),
                "name": normalized.get("name", path.stem),
                "scenario": normalized.get("scenario", ""),
                "difficulty": normalized.get("difficulty", ""),
                "chain": normalized.get("chain", ""),
                "max_points": normalized.get("max_points", 0),
                "phases": normalized.get("phases", []),
                "objective": normalized.get("objective", ""),
                "description": normalized.get("description", ""),
                "valid": not errors,
                "error": "; ".join(errors)[:200],
            }
        )
    return rows


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    """Validate and atomically write one definition file."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for gym administration")
    errors = validate_definition(data, filename=path.stem)
    if errors:
        raise ValueError("; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    tmp = path.with_name(f".{path.name}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def create_definition(
    gym_id: str,
    *,
    name: str = "",
    scenario: str = "metasploitable",
    objective: str = "",
    description: str = "",
    difficulty: str = "easy",
    chain: str = "",
    phases: list[str] | None = None,
    hints: list[str] | None = None,
    max_points: int = 1000,
    elo_bonus: int = 100,
    directory: Path | str | None = None,
    overwrite: bool = False,
) -> Path:
    """Create one gym definition YAML.

    Args:
        gym_id: Identifier and file stem.
        name: Display name.
        scenario: Lab scenario or range.
        objective: Operator-facing goal.
        description: Long description.
        difficulty: ``easy``, ``medium`` or ``hard``.
        chain: Optional APT chain run by the gym.
        phases: Kill-chain phases covered.
        hints: Progressive hints.
        max_points: Score ceiling.
        elo_bonus: ELO awarded on success.
        directory: Override for tests.
        overwrite: Replace an existing definition.

    Returns:
        The created path.

    Raises:
        FileExistsError: The definition exists and ``overwrite`` is False.
        ValueError: Invalid identifier or document.
    """
    clean = slugify(gym_id)
    if not clean or not _ID_RE.match(clean):
        raise ValueError(f"invalid gym id: {gym_id!r}")
    path = definition_path(clean, directory)
    if path.exists() and not overwrite:
        raise FileExistsError(f"gym definition already exists: {path.name}")
    data = {
        "id": clean,
        "name": str(name or clean),
        "description": str(description or ""),
        "scenario": str(scenario or ""),
        "chain": str(chain or ""),
        "objective": str(objective or ""),
        "difficulty": str(difficulty or "easy").lower(),
        "phases": [str(item) for item in (phases or ["recon", "enum", "exploit"])],
        "required_techniques": [],
        "bonus_techniques": [],
        "max_points": int(max_points),
        "speed_bonus_max": _DEFAULT_NUMBERS["speed_bonus_max"],
        "stealth_bonus_max": _DEFAULT_NUMBERS["stealth_bonus_max"],
        "technique_diversity_bonus": _DEFAULT_NUMBERS["technique_diversity_bonus"],
        "hints": [str(item) for item in (hints or [])],
        "success_check": "",
        "elo_bonus": int(elo_bonus),
    }
    _write_yaml(path, data)
    return path


def update_definition_yaml(
    gym_id: str,
    text: str,
    directory: Path | str | None = None,
) -> Path:
    """Parse, validate and atomically rewrite one definition.

    Args:
        gym_id: Existing definition id or file stem.
        text: Raw YAML.
        directory: Override for tests.

    Returns:
        The written path.

    Raises:
        FileNotFoundError: The definition does not exist.
        ValueError: Invalid YAML or invalid definition.
    """
    path = definition_path(gym_id, directory)
    if not path.is_file():
        raise FileNotFoundError(f"gym definition not found: {path.name}")
    module = _yaml_module()
    try:
        data = module.safe_load(text)
    except module.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("gym definition must be a YAML mapping")
    _write_yaml(path, dict(data))
    return path


def delete_definition(
    gym_id: str,
    directory: Path | str | None = None,
    *,
    allow_active: bool = False,
) -> dict[str, Any]:
    """Delete one definition unless it has active runs.

    Args:
        gym_id: Definition id.
        directory: Override for tests.
        allow_active: Stop runs before deleting when True.

    Returns:
        Dict with ``success`` and either ``deleted`` or ``error``.
    """
    try:
        path = definition_path(gym_id, directory)
    except ValueError as exc:
        return {"success": False, "error": str(exc)}
    if not path.is_file():
        return {"success": False, "error": f"gym definition not found: {path.name}"}
    active = [run for run in get_active_runs() if run.get("challenge_id") == path.stem]
    if active and not allow_active:
        ids = ", ".join(run.get("run_id", "") for run in active)
        return {"success": False, "error": f"gym has active runs: {ids}"}
    if active:
        stop_runs(path.stem)
    try:
        path.unlink()
    except OSError as exc:
        return {"success": False, "error": str(exc)}
    return {"success": True, "deleted": path.name}


# ---------------------------------------------------------------------------
# Persistent run state
# ---------------------------------------------------------------------------


def _empty_state() -> dict[str, Any]:
    """Return a fresh state document."""
    return {"version": STATE_VERSION, "next_id": 1, "active": {}, "legacy_imported": []}


def _world_model():
    """Return the shared world model lazily."""
    from modules.world_model import get_world_model

    return get_world_model()


def _sanitize_state(raw: Any) -> dict[str, Any]:
    """Validate and normalize one persisted state document."""
    state = _empty_state()
    if not isinstance(raw, dict):
        return state
    try:
        state["next_id"] = max(1, int(raw.get("next_id", 1) or 1))
    except (TypeError, ValueError):
        state["next_id"] = 1
    imported = raw.get("legacy_imported")
    if isinstance(imported, list):
        state["legacy_imported"] = [str(item)[:128] for item in imported if isinstance(item, str)]
    active = raw.get("active")
    if not isinstance(active, dict):
        return state
    for run_id, run in active.items():
        if not isinstance(run_id, str) or not _RUN_ID_RE.match(run_id):
            continue
        if not isinstance(run, dict):
            continue
        challenge_id = str(run.get("challenge_id", "") or "").strip()
        if not challenge_id:
            continue
        try:
            started_at = float(run.get("started_at", 0) or 0)
        except (TypeError, ValueError):
            continue
        if started_at <= 0:
            continue
        state["active"][run_id] = {
            "run_id": run_id,
            "challenge_id": challenge_id,
            "name": str(run.get("name", "") or challenge_id),
            "operator": normalize_operator(run.get("operator", "")),
            "started_at": started_at,
            "target": str(run.get("target", "") or "")[:255],
            "status": "active",
        }
    return state


def normalize_operator(value: Any) -> str:
    """Return a bounded operator label."""
    text = " ".join(str(value or "").split())
    return text[:64] or "anonymous"


def read_state() -> dict[str, Any]:
    """Read the persistent gym state from the world model.

    Legacy ``sessions/gym/active_<operator>.json`` files are imported in
    memory until the next write marks them as migrated.

    Returns:
        Sanitized state document.
    """
    try:
        raw = _world_model().read_section(STATE_KEY)
    except Exception as exc:
        log.debug("gym state unavailable: %s", exc)
        raw = None
    state = _sanitize_state(raw)
    _merge_legacy(state)
    return state


def write_state(state: dict[str, Any]) -> bool:
    """Persist one state document to the world model."""
    clean = _sanitize_state(state)
    clean["version"] = STATE_VERSION
    clean["updated_at"] = time.time()
    try:
        return bool(_world_model().write_section(STATE_KEY, clean))
    except Exception as exc:
        log.warning("gym state write failed: %s", exc)
        return False


def _merge_legacy(state: dict[str, Any]) -> None:
    """Import legacy per-operator active files once per write."""
    imported = set(state.get("legacy_imported", []))
    if not GYM_DIR.is_dir():
        return
    for path in sorted(GYM_DIR.glob("active_*.json")):
        if path.name in imported or path.is_symlink():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        challenge_id = str(data.get("challenge_id", "") or "").strip()
        try:
            started_at = float(data.get("started_at", 0) or 0)
        except (TypeError, ValueError):
            continue
        if not challenge_id or started_at <= 0:
            continue
        run_id = f"legacy-{hashlib.sha1(path.name.encode()).hexdigest()[:8]}"
        state["active"].setdefault(
            run_id,
            {
                "run_id": run_id,
                "challenge_id": challenge_id,
                "name": challenge_id,
                "operator": normalize_operator(data.get("username", "")),
                "started_at": started_at,
                "target": str(data.get("target", "") or "")[:255],
                "status": "active",
            },
        )
        state["legacy_imported"].append(path.name)


def _next_run_id(state: dict[str, Any]) -> str:
    """Allocate a stable human-readable run id."""
    number = max(1, int(state.get("next_id", 1) or 1))
    active = state.setdefault("active", {})
    while f"gym{number:04d}" in active:
        number += 1
    state["next_id"] = number + 1
    return f"gym{number:04d}"


def start_run(
    challenge_id: str,
    definitions: dict[str, dict[str, Any]],
    *,
    target: str = "",
    operator: str = "",
) -> dict[str, Any]:
    """Start one run and persist it.

    Args:
        challenge_id: Definition id.
        definitions: Loaded definitions.
        target: Optional engagement target.
        operator: Operator label.

    Returns:
        Dict with ``success``, ``run`` and ``definition``; an existing
        active run for the same operator/challenge is returned instead of
        creating a duplicate.
    """
    clean = str(challenge_id or "").strip()
    definition = definitions.get(clean)
    if definition is None:
        return {"success": False, "error": f"unknown gym: {clean}"}
    operator_name = normalize_operator(operator)
    with _STATE_LOCK:
        state = read_state()
        for run in state["active"].values():
            if run.get("challenge_id") == clean and run.get("operator") == operator_name:
                return {"success": True, "already_active": True, "run": dict(run), "definition": definition}
        run_id = _next_run_id(state)
        run = {
            "run_id": run_id,
            "challenge_id": clean,
            "name": definition.get("name", clean),
            "operator": operator_name,
            "started_at": time.time(),
            "target": str(target or "")[:255],
            "status": "active",
        }
        state["active"][run_id] = run
        if not write_state(state):
            return {"success": False, "error": "could not persist gym state"}
        return {"success": True, "run": dict(run), "definition": definition}


def _matches(run: dict[str, Any], selector: str) -> bool:
    """Return True when a selector matches a run id, challenge id or name."""
    needle = str(selector or "").strip().lower()
    if not needle:
        return False
    return needle in {
        str(run.get("run_id", "")).lower(),
        str(run.get("challenge_id", "")).lower(),
        str(run.get("name", "")).lower(),
    }


def get_active_runs(selector: str = "", operator: str = "") -> list[dict[str, Any]]:
    """Return active runs, enriched with elapsed time.

    Args:
        selector: Optional run id, challenge id or gym name.
        operator: Optional operator filter.

    Returns:
        Active run rows sorted by start time.
    """
    state = read_state()
    operator_name = normalize_operator(operator) if operator else ""
    now = time.time()
    rows: list[dict[str, Any]] = []
    for run in state["active"].values():
        if operator_name and run.get("operator") != operator_name:
            continue
        if selector and not _matches(run, selector):
            continue
        row = dict(run)
        row["elapsed_seconds"] = max(0, int(now - float(run.get("started_at", now))))
        rows.append(row)
    rows.sort(key=lambda item: float(item.get("started_at", 0)))
    return rows


def select_run(
    selector: str = "",
    *,
    operator: str = "",
    definitions: dict[str, dict[str, Any]] | None = None,
) -> tuple[dict[str, Any] | None, str]:
    """Resolve one active run.

    Args:
        selector: Optional run id, challenge id or gym name.
        operator: Optional operator filter.
        definitions: Loaded definitions used to fill missing names.

    Returns:
        Tuple of the run and an error string. When no selector is given
        and more than one run is active for the operator, the caller must
        disambiguate with a run id.
    """
    runs = get_active_runs(selector=selector, operator=operator)
    if not runs:
        return None, "no active gym matches"
    if len(runs) > 1:
        ids = ", ".join(str(run.get("run_id", "")) for run in runs)
        return None, f"multiple active gyms ({ids}); pass a run id"
    run = runs[0]
    if definitions:
        definition = definitions.get(str(run.get("challenge_id", "")))
        if definition:
            run["definition"] = definition
    return run, ""


def stop_runs(selector: str = "", *, operator: str = "") -> dict[str, Any]:
    """Stop one or every active run.

    Args:
        selector: Optional run id, challenge id or gym name. Empty stops
            every active run.
        operator: Optional operator filter.

    Returns:
        Dict with ``success``, ``count`` and the ``stopped`` rows.
    """
    with _STATE_LOCK:
        state = read_state()
        operator_name = normalize_operator(operator) if operator else ""
        stopped: list[dict[str, Any]] = []
        for run_id, run in list(state["active"].items()):
            if operator_name and run.get("operator") != operator_name:
                continue
            if selector and not _matches(run, selector):
                continue
            stopped.append(dict(run))
            state["active"].pop(run_id, None)
        if not stopped:
            return {"success": False, "count": 0, "stopped": [], "error": "no active gym matches"}
        if not write_state(state):
            return {"success": False, "count": 0, "stopped": [], "error": "could not persist gym state"}
        return {"success": True, "count": len(stopped), "stopped": stopped}


def pop_run(
    selector: str = "",
    *,
    operator: str = "",
    definitions: dict[str, dict[str, Any]] | None = None,
) -> tuple[dict[str, Any] | None, str]:
    """Resolve and remove one run, returning its final state.

    Args:
        selector: Optional run id, challenge id or gym name.
        operator: Optional operator filter.
        definitions: Loaded definitions.

    Returns:
        Tuple of the removed run and an error string.
    """
    with _STATE_LOCK:
        run, error = select_run(selector, operator=operator, definitions=definitions)
        if run is None:
            return None, error
        state = read_state()
        state["active"].pop(str(run.get("run_id", "")), None)
        if not write_state(state):
            return None, "could not persist gym state"
        return run, ""


def state_summary() -> dict[str, Any]:
    """Return counters used by status output and the TUI."""
    state = read_state()
    return {
        "active": len(state.get("active", {})),
        "next_id": state.get("next_id", 1),
        "runs": get_active_runs(),
    }


def new_run_token() -> str:
    """Return an unguessable token for external integrations."""
    return secrets.token_hex(8)


__all__ = [
    "GYMS_DIR",
    "GYM_DIR",
    "STATE_KEY",
    "create_definition",
    "definition_path",
    "delete_definition",
    "get_active_runs",
    "load_definitions",
    "new_run_token",
    "normalize_operator",
    "pop_run",
    "read_state",
    "scan_definitions",
    "select_run",
    "slugify",
    "start_run",
    "state_summary",
    "stop_runs",
    "update_definition_yaml",
    "validate_definition",
    "write_state",
]
