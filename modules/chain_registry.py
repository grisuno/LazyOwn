"""Chain registry — ordered orchestration chains from ``chains/*.yaml``.

One file per chain, same philosophy as ``lazyaddons/`` and ``exploits/``.
The ``apt_chain`` shell command interprets these files instead of
hardcoding its steps, so operators extend the orchestration by editing
YAML. Every step must be a routable shell command; resolution (tokens,
skip conditions, newest-file globs) happens here, execution stays in
the shell where output and timeouts belong.
"""

from __future__ import annotations

import glob
import logging
import os
import re
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
_MAX_YAML_BYTES = 100_000


@dataclass
class ChainStep:
    """One ordered step: shell line plus optional guards."""

    run: str = ""
    skip_if_exists: str = ""
    resolve_newest_glob: str = ""
    resolve_newest_as: str = ""


@dataclass
class Chain:
    """A validated chain with defaults and ordered steps."""

    name: str = ""
    description: str = ""
    defaults: dict[str, str] = field(default_factory=dict)
    steps: list[ChainStep] = field(default_factory=list)
    source: str = ""
    enabled: bool = True
    extends: str = ""

    def resolve(self, tokens: dict[str, str]) -> list[dict[str, Any]]:
        """Substitute tokens and evaluate guards.

        Returns [{run, skipped, reason}...] in order. ``resolve_newest``
        globs run at resolve time against the caller's cwd.
        """
        merged = {str(k): str(v) for k, v in {**self.defaults, **tokens}.items()}
        resolved: list[dict[str, Any]] = []
        for step in self.steps:
            rendered = step.run
            for key, value in merged.items():
                rendered = rendered.replace(f"{{{key}}}", value)
            skip_path = ""
            if step.skip_if_exists:
                skip_path = step.skip_if_exists
                for key, value in merged.items():
                    skip_path = skip_path.replace(f"{{{key}}}", value)
                if skip_path and os.path.exists(skip_path):
                    resolved.append({"run": rendered, "skipped": True, "reason": f"exists: {skip_path}"})
                    continue
            if step.resolve_newest_glob and step.resolve_newest_as:
                matches = sorted(glob.glob(step.resolve_newest_glob), key=os.path.getmtime)
                if not matches:
                    resolved.append({"run": rendered, "skipped": True, "reason": "no newest match"})
                    continue
                merged[step.resolve_newest_as] = matches[-1]
                rendered = step.run
                for key, value in merged.items():
                    rendered = rendered.replace(f"{{{key}}}", value)
            if re.search(r"\{[A-Za-z_]+\}", rendered):
                resolved.append({"run": rendered, "skipped": True, "reason": "unresolved token"})
                continue
            resolved.append({"run": rendered, "skipped": False, "reason": ""})
        return resolved


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
    defaults = data.get("defaults", {})
    if defaults is not None and not isinstance(defaults, dict):
        errors.append("defaults must be a mapping")
    extends = str(data.get("extends", "") or "")
    if extends and not _NAME_RE.match(extends):
        errors.append(f"invalid extends: {extends!r}")
    if extends and extends == str(data.get("name", "")):
        errors.append("a chain cannot extend itself")
    if extends and extends != str(data.get("name", "")) and chains_dir is not None:
        parent_file = Path(chains_dir) / f"{extends}.yaml"
        if not parent_file.is_file():
            errors.append(f"unknown parent chain file: {parent_file.name}")
    if "enabled" in data and not isinstance(data["enabled"], bool):
        errors.append("enabled must be true or false")
    steps = data.get("steps")
    if extends and steps is not None and not isinstance(steps, list):
        errors.append("steps must be a list when present")
    elif not extends and (not isinstance(steps, list) or not steps):
        errors.append("steps must be a non-empty list")
    elif isinstance(steps, list):
        for step in steps:
            if not isinstance(step, dict) or not str(step.get("run", "")).strip():
                errors.append("every step needs a non-empty run string")
                continue
            resolver = step.get("resolve_newest")
            if resolver is not None:
                if not isinstance(resolver, dict) or not resolver.get("glob") or not resolver.get("as"):
                    errors.append("resolve_newest needs glob and as keys")
    return errors


def load_all(chains_dir: Path | str = CHAINS_DIR) -> dict[str, Chain]:
    """Load every valid, enabled chain file (skips the rest loudly).

    Chains with ``extends: <parent>`` inherit the parent's steps (one
    level is flattened here; deeper nesting resolves recursively) and
    merge ``defaults`` over the parent's. Disabled chains never load.
    """
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install pyyaml")
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
    """Resolve one chain, flattening a single extends hop (cycle-safe)."""
    if name in stack:
        raise ValueError(f"extends cycle: {' -> '.join((*stack, name))}")
    entry = raw[name]
    data = entry["data"]
    parent_name = str(data.get("extends", "") or "")
    parent_steps: list[ChainStep] = []
    parent_defaults: dict[str, str] = {}
    if parent_name:
        if parent_name not in raw:
            raise ValueError(f"unknown parent chain: {parent_name!r}")
        parent = _materialize(parent_name, raw, (*stack, name))
        parent_steps = list(parent.steps)
        parent_defaults = dict(parent.defaults)
    steps = parent_steps
    own_raw = data.get("steps") or []
    if own_raw:
        steps = []
        for item in own_raw:
            resolver = item.get("resolve_newest") or {}
            steps.append(
                ChainStep(
                    run=str(item["run"]),
                    skip_if_exists=str(item.get("skip_if_exists", "") or ""),
                    resolve_newest_glob=str(resolver.get("glob", "") or ""),
                    resolve_newest_as=str(resolver.get("as", "") or ""),
                )
            )
    if not steps:
        raise ValueError("chain has no steps after inheritance")
    return Chain(
        name=str(data["name"]),
        description=str(data.get("description", "") or ""),
        defaults={**parent_defaults, **{str(k): str(v) for k, v in (data.get("defaults") or {}).items()}},
        steps=steps,
        source=entry["source"],
        enabled=True,
        extends=parent_name,
    )


def get(name: str, chains_dir: Path | str = CHAINS_DIR) -> Chain | None:
    """Return one chain by name, or None."""
    return load_all(chains_dir).get((name or "").strip().lower())


def scan_all(chains_dir: Path | str = CHAINS_DIR) -> list[dict[str, Any]]:
    """List every chain file including disabled ones (for administration).

    Returns [{name, enabled, extends, steps, playbook, description,
    source}...] sorted by name. Unreadable or invalid files appear with
    ``valid: False`` and an ``error`` note instead of being silently
    skipped — the admin surface must show what needs fixing.
    """
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install pyyaml")
    directory = Path(chains_dir)
    rows: list[dict[str, Any]] = []
    if not directory.exists():
        return rows
    for path in sorted(directory.glob("*.yaml")):
        try:
            if path.stat().st_size > _MAX_YAML_BYTES:
                rows.append({"name": path.stem, "enabled": False, "valid": False,
                             "error": "oversized file", "source": str(path)})
                continue
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                data = yaml.safe_load(fh)
        except Exception as exc:
            rows.append({"name": path.stem, "enabled": False, "valid": False,
                         "error": f"unreadable: {exc}", "source": str(path)})
            continue
        errors = validate_chain(data, filename=path.stem, chains_dir=directory) if isinstance(data, dict) else ["not a mapping"]
        steps = data.get("steps") or [] if isinstance(data, dict) else []
        rows.append(
            {
                "name": str(data.get("name", path.stem)) if isinstance(data, dict) else path.stem,
                "enabled": bool(data.get("enabled", True)) if isinstance(data, dict) else False,
                "extends": str(data.get("extends", "") or "") if isinstance(data, dict) else "",
                "steps": len(steps) if isinstance(steps, list) else 0,
                "playbook": str((data.get("defaults", {}) or {}).get("playbook", "")) if isinstance(data, dict) else "",
                "description": str(data.get("description", "") or "") if isinstance(data, dict) else "",
                "valid": not errors,
                "error": "; ".join(errors),
                "source": str(path),
            }
        )
    return rows


def set_enabled(name: str, enabled: bool, chains_dir: Path | str = CHAINS_DIR) -> bool:
    """Flip a chain's ``enabled`` flag in its YAML file (round-trip).

    Returns False when the file is missing or unreadable. Other keys
    keep their values; key order is preserved on write.
    """
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install pyyaml")
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
    """Write a per-APT chain file inheriting the base APT chain.

    ``engine_key`` is the exact ``AptPlaybookEngine`` lookup key
    (e.g. ``rocke``, ``apt29``) pinned as the playbook default; the
    chain file name is a sanitized ``apt_<slug>.yaml``. Steps live in
    the parent and stay in one place. Returns the written path.
    """
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install pyyaml")
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
        "description": description or f"Full APT chain for {apt_display or key} (extends apt_chain).",
        "enabled": True,
        "extends": "apt_chain",
        "defaults": {"playbook": key},
    }
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(doc, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return path
