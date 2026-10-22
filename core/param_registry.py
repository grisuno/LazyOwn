"""Operator-managed parameter registry.

One place to declare a parameter that every LazyOwn surface can use:
lazyaddons (``{param}`` substitution), aliases, pipelines and the shell
``assign`` command.

Why this exists
---------------
Every addon that needed its own knob used to brand a payload key
(``php2shell_url``, ``foo_target``, ``bar_profile``). The repository ended
up with thousands of single-consumer keys, each of them registered by hand
in four places: ``params/extended.yaml``, ``core/payload_schema.py``,
``lazyc2/addon_creator.py`` and the lazyaddon-creator skill. The registry
replaces that ritual with a data file.

Storage
-------
``params/operator.yaml`` holds the operator-created parameters::

    c2_profile:
      kind: string
      default: default
      description: "C2 profile name"
      category: general

Every ``params/*.yaml`` file is read by the shell at startup and merged
into ``self.params``. A mapping entry contributes its ``default`` value; a
flat entry contributes its value as-is (legacy behaviour).

Because the declaration is data, the payload schema and the addon-creator
validator pick the new keys up automatically: no source edit, no
addon-branded key, one declaration reused by every addon.

Design rules:

- The registry owns the file format, the CRUD and the projection of the
  entries into the payload schema. It never touches the shell directly:
  callers pass the shell in when they want the live params refreshed.
- Names are generic on purpose. A key that only makes sense for one addon
  is a design smell; use an existing generic key or add one here.
- Writes are atomic (temp file plus rename) so an interrupted edit never
  leaves a truncated YAML behind.

Usage:
    from core.param_registry import create_param, list_params, sync_shell_params

    create_param("c2_profile", kind="string", default="default", description="C2 profile")
    sync_shell_params(shell)
"""

from __future__ import annotations

import logging
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from core.payload_schema import SCHEMA, FieldKind, FieldSpec, _spec

log = logging.getLogger("param_registry")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY_PATH = REPO_ROOT / "params" / "operator.yaml"

PARAM_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,47}$")
PARAM_DESCRIPTION_MAX = 200
PARAM_NAME_MAX = 48

KIND_ALIASES: dict[str, FieldKind] = {
    "string": FieldKind.STRING,
    "str": FieldKind.STRING,
    "text": FieldKind.STRING,
    "int": FieldKind.INT,
    "integer": FieldKind.INT,
    "port": FieldKind.PORT,
    "bool": FieldKind.BOOL,
    "boolean": FieldKind.BOOL,
    "url": FieldKind.URL,
    "path": FieldKind.PATH,
    "ip": FieldKind.IP,
    "hostname": FieldKind.HOSTNAME,
    "hex": FieldKind.HEX,
    "json": FieldKind.JSON_BLOB,
    "opaque": FieldKind.OPAQUE,
}

_WRITE_LOCK = threading.RLock()


REGISTRY_HEADER = """# Operator-declared parameters.
#
# One place to declare a parameter that every surface can use: lazyaddons
# ({param} substitution), aliases, pipelines and the shell `assign` command.
# Manage it from the lazy_orchestrator TUI (Params tab) or with
# `param create <name> --kind string --default "" --desc "..."`.
#
# Format per entry:
#   name:
#     kind: string          # string|integer|boolean|url|path|ip|port|...
#     default: value
#     description: "help text"
#     category: general
#
# Use generic names: a key only one addon understands belongs in that
# addon, not in the shared catalog.
"""


@dataclass(frozen=True)
class OperatorParam:
    """One operator-declared parameter.

    Attributes:
        name: Placeholder token used in addon templates.
        kind: Payload field kind (``string``, ``integer``, ``url``, ...).
        default: Value the shell uses when the parameter is not set.
        description: Short help text shown to the operator.
        category: Payload schema category used by the wizard and reports.
        source: ``operator`` for registry entries, ``builtin`` for schema keys.
    """

    name: str
    kind: str = "string"
    default: Any = ""
    description: str = ""
    category: str = "general"
    source: str = "operator"

    def as_entry(self) -> dict[str, Any]:
        """Return the YAML mapping stored in ``params/operator.yaml``."""
        entry: dict[str, Any] = {"kind": self.kind, "default": self.default}
        if self.description:
            entry["description"] = self.description
        if self.category:
            entry["category"] = self.category
        return entry

    def to_spec(self) -> FieldSpec:
        """Return the payload schema spec for this parameter."""
        return _spec(
            self.name,
            KIND_ALIASES.get(self.kind, FieldKind.STRING),
            self.default,
            self.description or f"Operator-declared parameter {self.name}.",
            long_help=(
                "Declared in params/operator.yaml and reusable by every addon, "
                "alias and pipeline. Set it with 'assign {name} <value>'."
            ).format(name=self.name),
            example=str(self.default) if self.default != "" else self.name,
            category=self.category or "general",
        )


def registry_path(root: str | Path | None = None) -> Path:
    """Return the operator registry file path.

    Args:
        root: Optional repository root override (used by tests).

    Returns:
        Path of the ``params/operator.yaml`` file.
    """
    if root is None:
        return DEFAULT_REGISTRY_PATH
    return Path(root) / "params" / "operator.yaml"


def normalise_kind(kind: str) -> str:
    """Return the canonical kind name for a user-supplied kind.

    Args:
        kind: Raw kind name typed by the operator.

    Returns:
        The canonical kind, defaulting to ``string`` for unknown values.
    """
    clean = str(kind or "").strip().lower()
    if clean in KIND_ALIASES:
        return {FieldKind.INT: "integer", FieldKind.BOOL: "boolean"}.get(KIND_ALIASES[clean], clean)
    return "string"


def effective_value(entry: Any) -> Any:
    """Return the value a parameter contributes to the shell params.

    A mapping entry contributes its ``default``; a flat entry contributes
    its value as-is (legacy ``params/*.yaml`` behaviour).

    Args:
        entry: Raw YAML value of one parameter.

    Returns:
        The value the shell must receive.
    """
    if isinstance(entry, dict) and "default" in entry:
        return entry["default"]
    return entry


def _entry_to_param(name: str, entry: Any) -> OperatorParam:
    """Build an :class:`OperatorParam` from one raw YAML entry."""
    if isinstance(entry, dict):
        kind = normalise_kind(str(entry.get("kind") or "string"))
        default = effective_value(entry)
        description = str(entry.get("description") or "")
        category = str(entry.get("category") or "general")
    else:
        kind = "string"
        default = entry
        description = ""
        category = "general"
    return OperatorParam(
        name=name,
        kind=kind,
        default=default,
        description=description,
        category=category,
        source="operator",
    )


def load_entries(root: str | Path | None = None) -> dict[str, OperatorParam]:
    """Return every operator-declared parameter.

    Args:
        root: Optional repository root override (used by tests).

    Returns:
        Mapping of parameter name to its declaration. A missing or broken
        file yields an empty mapping instead of raising.
    """
    path = registry_path(root)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        return {}
    except (OSError, yaml.YAMLError) as exc:
        log.warning("param registry read failed at %s: %s", path, exc)
        return {}
    if not isinstance(raw, dict):
        return {}
    entries: dict[str, OperatorParam] = {}
    for name, entry in raw.items():
        key = str(name).strip()
        if not key or not PARAM_NAME_PATTERN.match(key):
            log.warning("param registry skipped illegal key: %r", name)
            continue
        entries[key] = _entry_to_param(key, entry)
    return entries


def list_params(
    root: str | Path | None = None,
    include_builtin: bool = True,
    keyword: str = "",
) -> list[OperatorParam]:
    """Return the parameters visible to the operator.

    Args:
        root: Optional repository root override (used by tests).
        include_builtin: Include the schema-backed builtin parameters.
        keyword: Case-insensitive filter over name and description.

    Returns:
        Parameters sorted by name.
    """
    merged: dict[str, OperatorParam] = {}
    if include_builtin:
        for name, spec in SCHEMA.items():
            merged[name] = OperatorParam(
                name=name,
                kind=spec.kind.value,
                default=spec.default,
                description=spec.description,
                category=spec.category,
                source="builtin",
            )
    for name, param in load_entries(root).items():
        merged[name] = param
    params = list(merged.values())
    needle = str(keyword or "").strip().lower()
    if needle:
        params = [p for p in params if needle in p.name.lower() or needle in p.description.lower()]
    return sorted(params, key=lambda item: (item.source != "operator", item.name))


def create_param(
    name: str,
    kind: str = "string",
    default: Any = "",
    description: str = "",
    category: str = "general",
    root: str | Path | None = None,
) -> OperatorParam:
    """Create an operator parameter and persist it in the registry.

    Args:
        name: Parameter name; must match ``^[a-z][a-z0-9_]{0,47}$``.
        kind: Payload field kind (``string``, ``integer``, ``url``, ...).
        default: Default value of the parameter.
        description: Short help text shown to the operator.
        category: Payload schema category.
        root: Optional repository root override (used by tests).

    Returns:
        The created parameter.

    Raises:
        ValueError: The name is illegal, the name is taken by another
            registry entry, or the description is too long.
    """
    key = str(name or "").strip()
    if not PARAM_NAME_PATTERN.match(key):
        raise ValueError(
            "parameter name must be lowercase, start with a letter and use only "
            "letters, digits and underscores (max 48 characters)"
        )
    if len(description) > PARAM_DESCRIPTION_MAX:
        raise ValueError(f"description exceeds {PARAM_DESCRIPTION_MAX} characters")
    with _WRITE_LOCK:
        entries = load_entries(root)
        if key in entries:
            raise ValueError(f"parameter already exists: {key}")
        param = OperatorParam(
            name=key,
            kind=normalise_kind(kind),
            default=default,
            description=str(description or ""),
            category=str(category or "general"),
        )
        entries[key] = param
        _write(entries, root)
    apply_to_schema(root)
    return param


def update_param(
    name: str,
    default: Any = None,
    description: str | None = None,
    kind: str | None = None,
    category: str | None = None,
    root: str | Path | None = None,
) -> OperatorParam:
    """Update an operator parameter in place.

    Args:
        name: Existing parameter name.
        default: New default value; ``None`` keeps the current one.
        description: New description; ``None`` keeps the current one.
        kind: New kind; ``None`` keeps the current one.
        category: New category; ``None`` keeps the current one.
        root: Optional repository root override (used by tests).

    Returns:
        The updated parameter.

    Raises:
        KeyError: The parameter does not exist in the registry.
        ValueError: The description is too long.
    """
    key = str(name or "").strip()
    with _WRITE_LOCK:
        entries = load_entries(root)
        current = entries.get(key)
        if current is None:
            raise KeyError(f"unknown operator parameter: {key}")
        if description is not None and len(description) > PARAM_DESCRIPTION_MAX:
            raise ValueError(f"description exceeds {PARAM_DESCRIPTION_MAX} characters")
        updated = OperatorParam(
            name=key,
            kind=normalise_kind(kind) if kind else current.kind,
            default=current.default if default is None else default,
            description=current.description if description is None else str(description),
            category=current.category if category is None else str(category),
        )
        entries[key] = updated
        _write(entries, root)
    apply_to_schema(root)
    return updated


def delete_param(name: str, root: str | Path | None = None) -> bool:
    """Delete an operator parameter from the registry.

    Args:
        name: Parameter name.
        root: Optional repository root override (used by tests).

    Returns:
        ``True`` when the parameter existed and was removed.

    Raises:
        KeyError: The parameter does not exist in the registry.
    """
    key = str(name or "").strip()
    with _WRITE_LOCK:
        entries = load_entries(root)
        if key not in entries:
            raise KeyError(f"unknown operator parameter: {key}")
        entries.pop(key)
        _write(entries, root)
    apply_to_schema(root)
    return True


def param_value(name: str, root: str | Path | None = None) -> Any:
    """Return the effective value of an operator parameter.

    Args:
        name: Parameter name.
        root: Optional repository root override (used by tests).

    Returns:
        The declared default, or ``None`` when the parameter is unknown.
    """
    entry = load_entries(root).get(str(name or "").strip())
    return None if entry is None else entry.default


def operator_specs(root: str | Path | None = None) -> dict[str, FieldSpec]:
    """Return the payload schema specs of the operator parameters.

    Args:
        root: Optional repository root override (used by tests).

    Returns:
        Mapping of parameter name to its schema spec.
    """
    return {name: param.to_spec() for name, param in load_entries(root).items()}


def apply_to_schema(root: str | Path | None = None) -> int:
    """Register the operator parameters in the payload schema.

    A sandboxed ``root`` (tests) never touches the process-wide schema:
    the caller owns that schema in that case.

    Args:
        root: Optional repository root override (used by tests).

    Returns:
        Number of parameters declared in the registry.
    """
    from core.payload_schema import register_specs, unregister_specs

    entries = load_entries(root)
    if root is not None:
        return len(entries)
    unregister_specs([name for name in SCHEMA if name not in entries])
    register_specs(operator_specs(root))
    return len(entries)


def sync_shell_params(shell: Any, root: str | Path | None = None) -> int:
    """Push the operator parameters into a live shell parameter dict.

    The shell substitutes addon placeholders from ``shell.params`` only, so
    a parameter created at runtime must land there to be usable in the same
    session.

    Args:
        shell: Object exposing a mutable ``params`` mapping.
        root: Optional repository root override (used by tests).

    Returns:
        Number of parameters pushed into the shell.
    """
    params = getattr(shell, "params", None)
    if not isinstance(params, dict):
        return 0
    entries = load_entries(root)
    for name, param in entries.items():
        params.setdefault(name, param.default)
    return len(entries)


def _write(entries: dict[str, OperatorParam], root: str | Path | None = None) -> bool:
    """Persist the parameter mapping atomically (tmp + rename).

    Args:
        entries: Full parameter mapping to store.
        root: Optional repository root override (used by tests).

    Returns:
        ``True`` on success, ``False`` when the filesystem refuses the write.
    """
    path = registry_path(root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        payload = {name: param.as_entry() for name, param in sorted(entries.items())}
        body = yaml.safe_dump(payload, sort_keys=True, allow_unicode=False)
        tmp.write_text(REGISTRY_HEADER + body, encoding="utf-8")
        tmp.replace(path)
        return True
    except OSError as exc:
        log.warning("param registry write failed at %s: %s", path, exc)
        return False


__all__ = [
    "KIND_ALIASES",
    "OperatorParam",
    "PARAM_NAME_PATTERN",
    "REGISTRY_HEADER",
    "apply_to_schema",
    "create_param",
    "delete_param",
    "effective_value",
    "list_params",
    "load_entries",
    "normalise_kind",
    "operator_specs",
    "param_value",
    "registry_path",
    "sync_shell_params",
    "update_param",
]


# The payload schema is the first consumer of the registry and it imports
# this module, so the projection is applied here too: whichever module is
# imported first, the schema ends up knowing every declared parameter.
apply_to_schema()
