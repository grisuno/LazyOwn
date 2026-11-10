"""Safe CRUD for the BOF YAML configurations under ``bofs/``.

Every BOF is one YAML file declaring its capability and the lazyaddon
beacon client that delivers it (``beacon`` for Windows COFF BOFs,
``blacksandbeacon`` for Linux ELF BOFs). This module is the single
writer for BOF configuration files: every mutation is validated,
confined to the BOF directory and written atomically.

The TUI (``cli.lazy_orchestrator``) BOFs tab and the catalog loaders
(:mod:`modules.bof_registry`) import only this module for file access;
delivery logic lives separately in :mod:`modules.bof_delivery`.
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
BOFS_DIR = BASE_DIR / "bofs"
MAX_BOF_BYTES = 50_000
_PREVIEW_LINES = 60
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_SUFFIXES = (".yaml", ".yml")

BOF_CLIENTS: tuple[str, ...] = ("beacon", "blacksandbeacon")
BOF_PLATFORMS: tuple[str, ...] = ("windows", "linux")
BOF_CATEGORIES: tuple[str, ...] = (
    "reconnaissance",
    "enumeration",
    "credential_access",
    "persistence",
    "execution",
    "collection",
    "privilege_escalation",
)
BOF_REQUIRED_FIELDS: tuple[str, ...] = ("name", "description", "author", "url", "source_file", "client", "platform")
_MITRE_RE = re.compile(r"^T\d{4}(?:\.\d{3})?$")


@dataclass(frozen=True)
class BofEntryRow:
    """One BOF YAML file rendered for the admin table."""

    file: str
    path: str
    name: str
    client: str
    platform: str
    category: str
    artifact: str
    staged: bool
    valid: bool
    error: str


def _yaml_module():
    """Return PyYAML or raise a clear runtime error."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for BOF administration")
    return yaml


def slugify(value: str) -> str:
    """Return a safe BOF filename stem.

    Args:
        value: Operator-supplied name.

    Returns:
        Lowercase ``[a-z0-9_-]`` slug with a 64-character cap.
    """
    text = re.sub(r"[^a-z0-9_-]+", "_", str(value or "").strip().lower()).strip("_-")
    return text[:64]


def bof_path(filename: str, directory: Path | str | None = None) -> Path:
    """Resolve one BOF file inside the bofs root.

    Args:
        filename: File name, with or without the ``.yaml`` suffix.
        directory: Override for tests; defaults to :data:`BOFS_DIR`.

    Returns:
        The confined path.

    Raises:
        ValueError: Empty name, path traversal or unsupported suffix.
    """
    root = Path(directory or BOFS_DIR).resolve()
    candidate = str(filename or "").strip()
    if not candidate:
        raise ValueError("bof filename is required")
    if not candidate.endswith(_SUFFIXES):
        candidate = f"{candidate}.yaml"
    target = (root / candidate).resolve()
    if target.parent != root:
        raise ValueError(f"bof path escapes {root}: {candidate!r}")
    return target


def load_bof(path: Path | str) -> dict[str, Any]:
    """Read one BOF YAML mapping.

    Args:
        path: File to read.

    Returns:
        The parsed mapping; empty when unreadable, oversized or not a
        mapping.

    Raises:
        OSError: File unreadable past the safety checks.
        RuntimeError: PyYAML unavailable.
    """
    target = Path(path)
    if target.stat().st_size > MAX_BOF_BYTES:
        return {}
    module = _yaml_module()
    data = module.safe_load(target.read_text(encoding="utf-8", errors="replace"))
    return dict(data) if isinstance(data, dict) else {}


def validate_bof(data: Any) -> list[str]:
    """Validate one BOF mapping against the delivery contract.

    Args:
        data: Parsed YAML document.

    Returns:
        A list of human-readable errors (empty when valid).
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["document must be a mapping"]
    name = str(data.get("name", "")).strip()
    if not _SLUG_RE.match(name):
        errors.append(f"invalid name: {name!r} (expected [a-z0-9_] slug)")
    client = str(data.get("client", "")).strip().lower()
    if client not in BOF_CLIENTS:
        errors.append(f"unknown client: {client!r} (expected: {', '.join(BOF_CLIENTS)})")
    platform = str(data.get("platform", "")).strip().lower()
    if platform not in BOF_PLATFORMS:
        errors.append(f"unknown platform: {platform!r} (expected: {', '.join(BOF_PLATFORMS)})")
    category = str(data.get("category", "")).strip().lower()
    if category and category not in BOF_CATEGORIES:
        errors.append(f"unknown category: {category!r}")
    mitre = str(data.get("mitre_technique", "") or "").strip()
    if mitre and not _MITRE_RE.match(mitre):
        errors.append(f"invalid mitre_technique: {mitre!r}")
    artifact = str(data.get("client_artifact", "") or "").strip()
    if artifact:
        if artifact.startswith(("/", "..")) or ".." in artifact.split("/") or "\\" in artifact:
            errors.append(f"client_artifact must be a repository-relative path: {artifact!r}")
        elif "\\" in artifact:
            errors.append(f"client_artifact must use forward slashes: {artifact!r}")
    for key in BOF_REQUIRED_FIELDS:
        if not str(data.get(key, "") or "").strip():
            errors.append(f"missing required field: {key}")
    for key in ("required_args", "optional_args"):
        value = data.get(key)
        if value is not None and (not isinstance(value, list) or any(not isinstance(item, str) for item in value)):
            errors.append(f"{key} must be a list of strings")
    if client and platform:
        expected = "windows" if client == "beacon" else "linux"
        if platform != expected:
            errors.append(f"client {client!r} delivers {expected} BOFs, platform says {platform!r}")
    return errors


def scan_bofs(directory: Path | str | None = None, sessions_dir: str = "sessions") -> list[BofEntryRow]:
    """Scan the bofs directory, returning admin rows for every file.

    Args:
        directory: Override for tests; defaults to :data:`BOFS_DIR`.
        sessions_dir: Staging root used to report the staged flag.

    Returns:
        One :class:`BofEntryRow` per ``.yaml`` file, invalid ones included.
    """
    root = Path(directory or BOFS_DIR)
    staging = Path(sessions_dir) / "temp_uploads" / "bofs"
    rows: list[BofEntryRow] = []
    for path in sorted(root.glob("*.yaml")):
        valid = True
        error = ""
        data: dict[str, Any] = {}
        try:
            data = load_bof(path)
            errors = validate_bof(data)
            if errors:
                valid = False
                error = "; ".join(errors)[:120]
        except Exception as exc:
            valid = False
            error = f"unreadable: {exc}"[:120]
        artifact = str(data.get("client_artifact", "") or "")
        staged = (staging / str(path.stem)).is_file()
        rows.append(
            BofEntryRow(
                file=path.name,
                path=str(path),
                name=str(data.get("name", "") or path.stem),
                client=str(data.get("client", "") or ""),
                platform=str(data.get("platform", "") or ""),
                category=str(data.get("category", "") or ""),
                artifact=artifact,
                staged=staged,
                valid=valid,
                error=error,
            )
        )
    return rows


def bof_template(name: str = "", description: str = "", client: str = "blacksandbeacon") -> dict[str, Any]:
    """Return a minimal BOF mapping ready for ``yaml.safe_dump``."""
    return {
        "name": str(name or "").strip() or "new_bof",
        "description": str(description or "").strip() or "BOF capability description",
        "author": "LazyOwn",
        "url": "https://github.com/grisuno/blacksandbeacon",
        "source_file": "bof/new_bof/bof.c",
        "client": client,
        "platform": "linux" if client == "blacksandbeacon" else "windows",
        "category": "reconnaissance",
        "client_artifact": f"build/bof/{name}.x64.o" if name else "",
        "required_args": [],
        "optional_args": [],
        "mitre_technique": "",
        "enabled": True,
    }


def _write_atomic(target: Path, data: dict[str, Any]) -> None:
    """Validate and atomically replace one BOF file."""
    module = _yaml_module()
    text = module.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f".{target.name}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def create_bof(
    filename: str,
    *,
    name: str = "",
    description: str = "",
    client: str = "blacksandbeacon",
    directory: Path | str | None = None,
    overwrite: bool = False,
) -> Path:
    """Create one BOF configuration file.

    Args:
        filename: Desired file name (slug); ``.yaml`` is appended when absent.
        name: ``name`` value; defaults to the slug.
        description: Free-form capability description.
        client: Delivering lazyaddon client.
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
        raise ValueError(f"invalid bof filename: {filename!r}")
    target = bof_path(stem, directory)
    if target.exists() and not overwrite:
        raise FileExistsError(f"bof already exists: {target.name}")
    data = bof_template(name or stem, description, client)
    errors = validate_bof(data)
    if errors:
        raise ValueError("; ".join(errors))
    artifact = str(data.get("client_artifact", "") or "").strip()
    if artifact:
        data["client_artifact"] = artifact.format(name=stem) if "{name}" in artifact else artifact
    _write_atomic(target, data)
    return target


def update_bof(
    path: Path | str,
    data: dict[str, Any],
    directory: Path | str | None = None,
) -> Path:
    """Validate and atomically rewrite one BOF configuration.

    Args:
        path: Existing file path or file name inside ``directory``.
        data: New mapping.
        directory: Override for tests.

    Returns:
        The written path.

    Raises:
        ValueError: Invalid document.
        FileNotFoundError: The target does not exist.
    """
    if directory is not None:
        target = bof_path(Path(path).name, directory)
    else:
        target = bof_path(str(path))
    if not target.is_file():
        raise FileNotFoundError(f"bof not found: {target.name}")
    errors = validate_bof(data)
    if errors:
        raise ValueError("; ".join(errors))
    _write_atomic(target, data)
    return target


def save_bof_yaml(
    path: Path | str,
    text: str,
    directory: Path | str | None = None,
) -> Path:
    """Validate raw YAML text and atomically write it to the bofs root.

    Args:
        path: File name (slug accepted) inside ``directory``, or absolute
            path inside it.
        text: Raw YAML text.
        directory: Override for tests; defaults to :data:`BOFS_DIR`.

    Returns:
        The written path.

    Raises:
        ValueError: Invalid YAML text or invalid document.
    """
    module = _yaml_module()
    try:
        data = module.safe_load(text)
    except Exception as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("BOF YAML must be a mapping")
    target = bof_path(str(path), directory)
    if not target.is_file():
        raise FileNotFoundError(f"bof not found: {target.name}")
    data.pop("name", None)
    data["name"] = target.stem
    errors = validate_bof(data)
    if errors:
        raise ValueError("; ".join(errors))
    _write_atomic(target, data)
    return target


def preview_bof(path: Path | str, limit: int = _PREVIEW_LINES) -> str:
    """Return a bounded YAML preview for one BOF file.

    Args:
        path: File path.
        limit: Maximum lines to render.

    Returns:
        A preview string prefixed with the first description lines.
    """
    target = Path(path)
    try:
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return f"unreadable: {exc}"
    shown = lines[: max(1, limit)]
    if len(lines) > len(shown):
        shown.append(f"... +{len(lines) - len(shown)} more line(s)")
    return "\n".join(shown)


def delete_bof(path: Path | str, directory: Path | str | None = None) -> bool:
    """Delete one BOF configuration file after validation.

    Args:
        path: Existing file name or path inside ``directory``.
        directory: Override for tests; defaults to :data:`BOFS_DIR`.

    Returns:
        True when the file was removed.

    Raises:
        ValueError: When the resolved path escapes the bofs root.
    """
    target = bof_path(Path(path).name, directory)
    if not target.is_file():
        return False
    target.unlink()
    return True


__all__ = [
    "BOFS_DIR",
    "BOF_CATEGORIES",
    "BOF_CLIENTS",
    "BOF_PLATFORMS",
    "BofEntryRow",
    "bof_path",
    "bof_template",
    "create_bof",
    "delete_bof",
    "load_bof",
    "preview_bof",
    "save_bof_yaml",
    "scan_bofs",
    "slugify",
    "update_bof",
    "validate_bof",
]
