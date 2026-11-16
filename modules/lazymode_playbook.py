"""Run and list lazymode-powered exploit playbooks.

A lazymode playbook is an ordinary LazyOwn playbook (validated and managed
by :mod:`modules.playbook_admin`, surfaced in the orchestrator Playbooks
tab) whose steps declare ``kind: lazymode``. Each such step carries a
lazymode script in its ``run`` field that drives the framework through the
``lazy`` SDK facade and returns a compact structured result, so one
playbook captures a whole exploitation path (recon-informed trigger,
session, proof) as a single administrable asset.

This module is the focused executor: it loads a playbook through the
shared admin layer, validates it, and runs each lazymode step via
:func:`sdk.lazymode.run`. The SDK import is deferred so importing this
module never forms a cycle with the SDK (which composes ``modules``
parsers lazily).
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from modules.playbook_admin import PLAYBOOKS_DIR, load_playbook, validate_playbook

_VECTOR_KIND = "lazymode"
_DEFAULT_STEP_TIMEOUT = 120.0
_TARGET_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-_:]{0,254}$")


def _iter_steps(data: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Yield every step mapping from a playbook's top-level or phase steps.

    Args:
        data: Parsed playbook mapping.

    Yields:
        Each step mapping, from top-level ``steps`` then each phase's
        ``steps``.
    """
    steps = data.get("steps")
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, dict):
                yield step
    for phase in data.get("phases") or []:
        if isinstance(phase, dict):
            for step in phase.get("steps") or []:
                if isinstance(step, dict):
                    yield step


def is_vector_playbook(data: dict[str, Any]) -> bool:
    """Return whether *data* declares at least one lazymode step.

    Args:
        data: Parsed playbook mapping.

    Returns:
        True when any step's kind is ``lazymode``.
    """
    return any(str(step.get("kind", "")).strip().lower() == _VECTOR_KIND for step in _iter_steps(data))


def list_vector_playbooks(directory: str | os.PathLike[str] | None = None) -> list[dict[str, Any]]:
    """Return a summary of every lazymode playbook in *directory*.

    Args:
        directory: Playbook directory; defaults to the shared
            ``playbooks/`` root.

    Returns:
        One summary mapping per lazymode playbook (file, name, vector,
        trigger, scenario, description), sorted by file name.
    """
    root = Path(directory or PLAYBOOKS_DIR)
    summaries: list[dict[str, Any]] = []
    if not root.is_dir():
        return summaries
    for path in sorted(root.glob("*.yaml")):
        try:
            data = load_playbook(path)
        except Exception:
            continue
        if not isinstance(data, dict) or not is_vector_playbook(data):
            continue
        summaries.append(
            {
                "file": path.name,
                "name": str(data.get("name") or data.get("apt_name") or path.stem),
                "vector": str(data.get("vector", "")),
                "trigger": data.get("trigger") or [],
                "scenario": str(data.get("scenario", "")),
                "description": str(data.get("description", "")),
            }
        )
    return summaries


def _resolve(name: str, root: Path) -> Path:
    """Resolve *name* to a playbook file inside *root*.

    Args:
        name: A file name (with or without ``.yaml``) or a playbook name.
        root: The playbook directory.

    Returns:
        The resolved playbook path.

    Raises:
        ValueError: When the name contains a path separator or traversal.
        FileNotFoundError: When no playbook matches.
    """
    if os.sep in name or (os.altsep and os.altsep in name) or ".." in name:
        raise ValueError(f"invalid playbook name: {name!r}")
    for candidate in (root / name, root / f"{name}.yaml"):
        if candidate.is_file():
            return candidate
    for path in sorted(root.glob("*.yaml")):
        try:
            data = load_playbook(path)
        except Exception:
            continue
        if str(data.get("name", "")).strip().lower() == name.strip().lower():
            return path
    raise FileNotFoundError(f"playbook not found: {name}")


def _prepare_script(source: str, target: str | None) -> str:
    """Prepend a validated ``target`` binding to a step script.

    Args:
        source: The step's lazymode script.
        target: The target to bind, or None to leave the script unchanged.

    Returns:
        The script with a leading ``target = ...`` line when a target is
        supplied.

    Raises:
        ValueError: When *target* is not a valid host token.
    """
    if not target:
        return source
    if not _TARGET_PATTERN.match(target):
        raise ValueError(f"invalid target: {target!r}")
    return f"target = {target!r}\n{source}"


def run_playbook(
    name: str,
    target: str | None = None,
    directory: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    """Run every lazymode step of a playbook and return the outcome.

    Args:
        name: Playbook file name or declared name.
        target: Host bound as the ``target`` variable in each step script;
            validated before injection.
        directory: Playbook directory; defaults to ``playbooks/``.
        timeout: Per-step wall-clock override in seconds.

    Returns:
        A result mapping with the playbook name, the target, an overall
        ``ok`` flag and one entry per executed step (its lazymode result).
    """
    root = Path(directory or PLAYBOOKS_DIR)
    path = _resolve(name, root)
    data = load_playbook(path)
    errors = validate_playbook(data)
    if errors:
        return {"playbook": path.name, "ok": False, "error": "; ".join(errors), "steps": []}

    from sdk.lazymode import run as lazymode_run

    results: list[dict[str, Any]] = []
    overall = True
    for index, step in enumerate(_iter_steps(data), 1):
        if str(step.get("kind", "")).strip().lower() != _VECTOR_KIND:
            continue
        lang = str(step.get("lang", "python")).strip().lower()
        script = _prepare_script(str(step.get("run", "")), target)
        step_timeout = float(step.get("timeout") or timeout or _DEFAULT_STEP_TIMEOUT)
        kwargs: dict[str, Any] = {}
        if lang == "python":
            kwargs["timeout"] = step_timeout
        outcome = lazymode_run(script, lang=lang, **kwargs)
        results.append({"step": index, "lang": lang, **outcome.to_dict()})
        if not outcome.ok:
            overall = False
            if not bool(step.get("continue_on_error", False)):
                break
    return {
        "playbook": path.name,
        "name": str(data.get("name") or data.get("apt_name") or path.stem),
        "target": target,
        "ok": overall,
        "steps": results,
    }
