"""Safe CRUD for the YAML playbooks under ``playbooks/``.

Two playbook shapes coexist on disk:

- APT playbooks (``apt_*.yaml``) declare ``apt_name``, ``platforms`` and a
  ``phases`` list consumed by :mod:`modules.apt_playbooks`;
- generated plans (``attack_plan*.yaml``) declare ``apt_name`` plus a
  ``steps`` list consumed by :mod:`modules.playbook_engine`.

This module is the single writer for both. Every mutation is validated,
confined to the playbooks directory and written atomically so the TUI can
administrate files without ever leaving a half-written YAML behind.

The TUI (``lazy_orchestrator``) imports only this module for playbook
CRUD; readers keep loading YAML themselves.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is a hard dependency
    yaml = None  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent
PLAYBOOKS_DIR = BASE_DIR / "playbooks"
MAX_PLAYBOOK_BYTES = 500_000
_PREVIEW_LINES = 60
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_SUFFIXES = (".yaml", ".yml")


@dataclass(frozen=True)
class PlaybookEntry:
    """One playbook file rendered for the admin table."""

    file: str
    path: str
    name: str
    kind: str
    steps: int
    phases: int
    platforms: tuple[str, ...]
    description: str
    valid: bool
    error: str


def _yaml_module():
    """Return PyYAML or raise a clear runtime error."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for playbook administration")
    return yaml


def slugify(value: str) -> str:
    """Return a safe playbook filename stem.

    Args:
        value: Operator-supplied name.

    Returns:
        Lowercase ``[a-z0-9_-]`` slug with a 64-character cap.
    """
    text = re.sub(r"[^a-z0-9_-]+", "_", str(value or "").strip().lower()).strip("_-")
    return text[:64]


def playbook_path(filename: str, directory: Path | str | None = None) -> Path:
    """Resolve one playbook file inside the playbooks root.

    Args:
        filename: File name, with or without the ``.yaml`` suffix.
        directory: Override for tests; defaults to :data:`PLAYBOOKS_DIR`.

    Returns:
        The confined path.

    Raises:
        ValueError: Empty name, path traversal or unsupported suffix.
    """
    root = Path(directory or PLAYBOOKS_DIR).resolve()
    candidate = str(filename or "").strip()
    if not candidate:
        raise ValueError("playbook filename is required")
    if not candidate.endswith(_SUFFIXES):
        candidate = f"{candidate}.yaml"
    target = (root / candidate).resolve()
    if target.parent != root:
        raise ValueError(f"playbook path escapes {root}: {candidate!r}")
    if target.suffix.lower() not in _SUFFIXES:
        raise ValueError(f"unsupported playbook suffix: {target.suffix!r}")
    return target


def load_playbook(path: Path | str) -> dict[str, Any]:
    """Read one playbook YAML mapping.

    Args:
        path: File to read.

    Returns:
        The parsed mapping; empty when the file is not a mapping.

    Raises:
        OSError: File unreadable.
        RuntimeError: PyYAML unavailable.
    """
    target = Path(path)
    if target.stat().st_size > MAX_PLAYBOOK_BYTES:
        return {}
    module = _yaml_module()
    data = module.safe_load(target.read_text(encoding="utf-8", errors="replace"))
    return dict(data) if isinstance(data, dict) else {}


def playbook_kind(data: dict[str, Any]) -> str:
    """Return ``apt``, ``plan``, ``mixed`` or ``unknown`` for one mapping."""
    has_phases = isinstance(data.get("phases"), list)
    has_steps = isinstance(data.get("steps"), list)
    if has_phases and has_steps:
        return "mixed"
    if has_phases:
        return "apt"
    if has_steps:
        return "plan"
    return "unknown"


def validate_playbook(data: Any) -> list[str]:
    """Validate the minimal shape shared by both playbook formats.

    Args:
        data: Parsed YAML document.

    Returns:
        Human-readable errors; empty means valid.
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["playbook must be a mapping"]
    name = str(data.get("apt_name") or data.get("name") or "").strip()
    if not name:
        errors.append("apt_name is required")
    description = data.get("description")
    if description is not None and not isinstance(description, str):
        errors.append("description must be a string")
    platforms = data.get("platforms")
    if platforms is not None and not isinstance(platforms, list):
        errors.append("platforms must be a list")
    phases = data.get("phases")
    if phases is not None and not isinstance(phases, list):
        errors.append("phases must be a list")
    for index, phase in enumerate(phases or [], 1):
        if not isinstance(phase, dict):
            errors.append(f"phase #{index} must be a mapping")
            continue
        if not str(phase.get("name", "")).strip():
            errors.append(f"phase #{index} name is required")
        technique = phase.get("technique_id")
        if technique is not None and not isinstance(technique, str):
            errors.append(f"phase #{index} technique_id must be a string")
        atomic_tests = phase.get("atomic_tests")
        if atomic_tests is not None and not isinstance(atomic_tests, list):
            errors.append(f"phase #{index} atomic_tests must be a list")
    steps = data.get("steps")
    if steps is not None and not isinstance(steps, list):
        errors.append("steps must be a list")
    for index, step in enumerate(steps or [], 1):
        if not isinstance(step, dict):
            errors.append(f"step #{index} must be a mapping")
    if isinstance(phases, list) and isinstance(steps, list):
        errors.append("playbook cannot declare both phases and steps")
    return errors


def _count_steps(data: dict[str, Any]) -> int:
    """Count atomic tests for APT books and steps for generated plans."""
    steps = data.get("steps")
    if isinstance(steps, list):
        return len(steps)
    total = 0
    for phase in data.get("phases") or []:
        if not isinstance(phase, dict):
            continue
        atomic_tests = phase.get("atomic_tests")
        total += len(atomic_tests) if isinstance(atomic_tests, list) else 1
    return total


def summarize(path: Path | str) -> PlaybookEntry:
    """Build the admin-table row for one file without raising."""
    target = Path(path)
    try:
        data = load_playbook(target)
    except Exception as exc:
        return PlaybookEntry(
            file=target.name,
            path=str(target),
            name=target.stem,
            kind="unknown",
            steps=0,
            phases=0,
            platforms=(),
            description="",
            valid=False,
            error=str(exc)[:120],
        )
    errors = validate_playbook(data)
    phases = data.get("phases") if isinstance(data.get("phases"), list) else []
    return PlaybookEntry(
        file=target.name,
        path=str(target),
        name=str(data.get("apt_name") or data.get("name") or target.stem),
        kind=playbook_kind(data),
        steps=_count_steps(data),
        phases=len(phases),
        platforms=tuple(str(item) for item in (data.get("platforms") or [])),
        description=" ".join(str(data.get("description") or "").split())[:160],
        valid=not errors,
        error="; ".join(errors)[:120],
    )


def scan_playbooks(directory: Path | str | None = None) -> list[PlaybookEntry]:
    """Return every ``*.yaml``/``*.yml`` playbook, sorted by file name.

    Args:
        directory: Override for tests; defaults to :data:`PLAYBOOKS_DIR`.

    Returns:
        One entry per parseable or failing file; never raises.
    """
    root = Path(directory or PLAYBOOKS_DIR)
    if not root.is_dir():
        return []
    rows: list[PlaybookEntry] = []
    for suffix in _SUFFIXES:
        for fpath in sorted(root.glob(f"*{suffix}")):
            rows.append(summarize(fpath))
    rows.sort(key=lambda row: row.file.lower())
    return rows


def preview_playbook(path: Path | str, limit: int = _PREVIEW_LINES) -> str:
    """Return a bounded, sanitized text preview for the detail pane."""
    target = Path(path)
    try:
        text = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"unreadable: {exc}"
    lines = text.splitlines()
    shown = lines[: max(0, limit)]
    if len(lines) > len(shown):
        shown.append(f"... +{len(lines) - len(shown)} more line(s)")
    return "\n".join(shown)


def playbook_template(
    name: str,
    description: str = "",
    platforms: tuple[str, ...] | list[str] = ("linux",),
) -> dict[str, Any]:
    """Return a minimal APT playbook mapping ready for ``yaml.safe_dump``."""
    clean = str(name or "").strip() or "New Playbook"
    return {
        "apt_name": clean,
        "aliases": [],
        "source_urls": [],
        "description": str(description or "").strip(),
        "platforms": [str(item) for item in platforms if str(item).strip()] or ["linux"],
        "phases": [],
    }


def _write_atomic(target: Path, data: dict[str, Any]) -> None:
    """Validate and atomically replace one playbook file."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for playbook administration")
    text = yaml.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f".{target.name}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def create_playbook(
    filename: str,
    *,
    name: str = "",
    description: str = "",
    platforms: tuple[str, ...] | list[str] = ("linux",),
    directory: Path | str | None = None,
    overwrite: bool = False,
) -> Path:
    """Create one APT playbook file.

    Args:
        filename: Desired file name (slug); ``.yaml`` is appended when absent.
        name: ``apt_name`` value; defaults to the slug.
        description: Free-form description.
        platforms: Platform list.
        directory: Override for tests.
        overwrite: Replace an existing file instead of failing.

    Returns:
        The created path.

    Raises:
        FileExistsError: The file exists and ``overwrite`` is False.
        ValueError: Invalid slug, path or document.
    """
    stem = slugify(filename)
    if not stem or not _SLUG_RE.match(stem):
        raise ValueError(f"invalid playbook filename: {filename!r}")
    target = playbook_path(stem, directory)
    if target.exists() and not overwrite:
        raise FileExistsError(f"playbook already exists: {target.name}")
    data = playbook_template(name or stem, description, platforms)
    errors = validate_playbook(data)
    if errors:
        raise ValueError("; ".join(errors))
    _write_atomic(target, data)
    return target


def _target_for_write(path: Path | str, directory: Path | str | None) -> Path:
    """Resolve one existing playbook for a mutation without escaping its root."""
    if directory is not None:
        target = playbook_path(Path(path).name, directory)
    else:
        target = Path(path).resolve()
        if target.suffix.lower() not in _SUFFIXES:
            raise ValueError(f"unsupported playbook suffix: {target.suffix!r}")
    if not target.is_file():
        raise FileNotFoundError(f"playbook not found: {target.name}")
    return target


def update_playbook(
    path: Path | str,
    data: dict[str, Any],
    directory: Path | str | None = None,
) -> Path:
    """Validate and atomically rewrite one playbook.

    Args:
        path: Existing file path or file name inside ``directory``.
        data: New mapping.
        directory: Override for tests.

    Returns:
        The written path.

    Raises:
        ValueError: Invalid document or unsupported suffix.
        FileNotFoundError: The target does not exist.
    """
    target = _target_for_write(path, directory)
    errors = validate_playbook(data)
    if errors:
        raise ValueError("; ".join(errors))
    _write_atomic(target, data)
    return target


def save_playbook_yaml(
    path: Path | str,
    text: str,
    directory: Path | str | None = None,
) -> Path:
    """Parse, validate and write a raw YAML document.

    Args:
        path: Existing file path or file name.
        text: Raw YAML edited by the operator.
        directory: Override for tests.

    Returns:
        The written path.

    Raises:
        ValueError: Unparseable YAML or invalid playbook shape.
        FileNotFoundError: The target does not exist.
    """
    module = _yaml_module()
    try:
        data = module.safe_load(text)
    except module.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("playbook must be a YAML mapping")
    return update_playbook(path, dict(data), directory)


def delete_playbook(path: Path | str, directory: Path | str | None = None) -> bool:
    """Delete one playbook confined to the playbooks root.

    Args:
        path: File path or file name.
        directory: Override for tests.

    Returns:
        True when the file was removed.
    """
    try:
        target = _target_for_write(path, directory)
    except (ValueError, FileNotFoundError):
        return False
    try:
        target.unlink()
    except OSError:
        return False
    return True


__all__ = [
    "MAX_PLAYBOOK_BYTES",
    "PLAYBOOKS_DIR",
    "PlaybookEntry",
    "create_playbook",
    "delete_playbook",
    "load_playbook",
    "playbook_kind",
    "playbook_path",
    "playbook_template",
    "preview_playbook",
    "save_playbook_yaml",
    "scan_playbooks",
    "slugify",
    "summarize",
    "update_playbook",
    "validate_playbook",
]
