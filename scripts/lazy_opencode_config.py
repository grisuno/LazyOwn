"""Patch operator agent configs to use the Lazy llama.cpp server.

Shared by ``scripts/lazy_llamacpp_setup.sh`` and the
``lazyown_opencode_config`` MCP tool so interactive and agentic flows
apply byte-identical merges. Every write backs the file up first and
never touches an existing setup without an explicit call.

Targets:
- ``opencode``: ``~/.config/opencode/opencode.json`` gains the
  ``llamacpp`` provider plus the ``local-model`` entry.
- ``hermes``: ``~/.hermes/config.yaml`` gains the ``llamacpp``
  provider entry and points the default model at it.
"""

from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path

LLAMACPP_HOST = "http://localhost:8080/v1"
LLAMACPP_PROVIDER = "llamacpp"
LLAMACPP_MODEL = "local-model"
LLAMACPP_MODEL_NAME = "Qwen 27B Local"


def _backup(path: Path) -> str:
    """Copy path to a timestamped backup; return the backup path."""
    backup = path.with_suffix(path.suffix + f".bak-{int(time.time())}")
    shutil.copy2(path, backup)
    return str(backup)


def _opencode_path() -> Path:
    """Return the opencode config path."""
    return Path.home() / ".config" / "opencode" / "opencode.json"


def _hermes_path() -> Path:
    """Return the hermes config path."""
    return Path.home() / ".hermes" / "config.yaml"


def patch_opencode(set_default: bool = False, host: str = LLAMACPP_HOST) -> dict:
    """Merge the llamacpp provider into the opencode config.

    Args:
        set_default: Also set the top-level model to llamacpp/local-model.
        host: Server base URL (``.../v1``).

    Returns:
        Summary with changed flag, backup path and path. Never raises.
    """
    summary: dict = {"target": "opencode", "changed": False, "backup": "", "path": ""}
    try:
        path = _opencode_path()
        summary["path"] = str(path)
        if not path.is_file():
            return {**summary, "error": "opencode config not found"}
        data = json.loads(path.read_text(encoding="utf-8"))
        provider = data.setdefault("provider", {}).setdefault(LLAMACPP_PROVIDER, {})
        changed = False
        for key, value in (
            ("name", "llama.cpp"),
            ("npm", "@ai-sdk/openai-compatible"),
        ):
            if provider.get(key) != value:
                provider[key] = value
                changed = True
        options = provider.setdefault("options", {})
        if options.get("baseURL") != host:
            options["baseURL"] = host
            changed = True
        models = provider.setdefault("models", {})
        if models.get(LLAMACPP_MODEL) != {"name": LLAMACPP_MODEL_NAME}:
            models[LLAMACPP_MODEL] = {"name": LLAMACPP_MODEL_NAME}
            changed = True
        if set_default and data.get("model") != f"{LLAMACPP_PROVIDER}/{LLAMACPP_MODEL}":
            data["model"] = f"{LLAMACPP_PROVIDER}/{LLAMACPP_MODEL}"
            changed = True
        if not changed:
            return summary
        summary["backup"] = _backup(path)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        summary["changed"] = True
    except Exception as exc:
        summary["error"] = str(exc)[:200]
    return summary


def patch_hermes(host: str = LLAMACPP_HOST) -> dict:
    """Point the hermes config at the local llama.cpp server.

    Surgical merge: only the llamacpp provider entry and the default
    model pointer are ensured; every other key (and the operator's own
    provider fields like ``name``/``transport``) is preserved. The file
    is rewritten only when a required value actually differs.

    Args:
        host: Server base URL (``.../v1``).

    Returns:
        Summary with changed flag, backup path and path. Never raises.
    """
    summary: dict = {"target": "hermes", "changed": False, "backup": "", "path": ""}
    try:
        import yaml
    except ImportError:
        return {**summary, "error": "pyyaml not installed"}
    try:
        path = _hermes_path()
        summary["path"] = str(path)
        if not path.is_file():
            return {**summary, "error": "hermes config not found"}
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        providers = data.setdefault("providers", {})
        entry = providers.setdefault(LLAMACPP_PROVIDER, {})
        changed = False
        if entry.get("api") != host:
            entry["api"] = host
            changed = True
        if entry.get("default_model") != LLAMACPP_MODEL:
            entry["default_model"] = LLAMACPP_MODEL
            changed = True
        models = entry.get("models") or []
        if LLAMACPP_MODEL not in models:
            entry["models"] = [*models, LLAMACPP_MODEL]
            changed = True
        model = data.setdefault("model", {})
        for key, value in (
            ("base_url", host),
            ("default", LLAMACPP_MODEL),
            ("provider", f"custom:{LLAMACPP_PROVIDER}"),
        ):
            if model.get(key) != value:
                model[key] = value
                changed = True
        if not changed:
            return summary
        summary["backup"] = _backup(path)
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        summary["changed"] = True
    except Exception as exc:
        summary["error"] = str(exc)[:200]
    return summary


def main(argv: list[str] | None = None) -> int:
    """CLI entry: ``--target opencode|hermes|both [--set-default]``."""
    parser = argparse.ArgumentParser(description="Point agent configs at the Lazy llama.cpp server.")
    parser.add_argument("--target", default="both", choices=("opencode", "hermes", "both"))
    parser.add_argument("--add-llamacpp", action="store_true")
    parser.add_argument("--set-default", action="store_true")
    parser.add_argument("--host", default=LLAMACPP_HOST)
    args = parser.parse_args(argv)
    results = []
    if args.target in ("opencode", "both"):
        results.append(patch_opencode(set_default=args.set_default, host=args.host))
    if args.target in ("hermes", "both"):
        results.append(patch_hermes(host=args.host))
    print(json.dumps(results, indent=2))
    return 0 if all(r.get("changed") or not r.get("error") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["patch_hermes", "patch_opencode"]
