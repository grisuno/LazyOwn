"""Mirror LazyOwn skills for Hermes discovery.

Hermes loads skills from ``~/.hermes/skills/<group>/<name>/SKILL.md``
while opencode reads ``skills/<name>/SKILL.md`` in this repo, so the
two runtimes never share one directory. This module derives thin
Hermes-compatible mirrors under ``skills/<name>/hermes/SKILL.md`` from
the repo frontmatter (name, description, version, author, license) and
registers the parent ``skills/`` tree in the operator's
``~/.hermes/config.yaml`` ``skills.external_dirs`` — the same pattern
opencode uses with its ``skills.paths`` list.

Mirrors only re-target the frontmatter; the body stays byte-identical
so both agents read the same procedure. Never touches the operator's
config without an explicit call; every write backs the file up first.
"""

from __future__ import annotations

import re
import shutil
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Split SKILL.md into frontmatter dict and body."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw = match.group(1)
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith(" ") or line.startswith("\t"):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields, text[match.end() :]


def _hermes_frontmatter(name: str, fields: dict) -> str:
    """Build a Hermes-compatible frontmatter block for one skill."""
    description = fields.get("description", f"LazyOwn skill: {name}")
    version = fields.get("version", "1.0.0")
    author = fields.get("author", "LazyOwn RedTeam")
    license_name = fields.get("license", "MIT")
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"version: {version}\n"
        f"author: {author}\n"
        f"license: {license_name}\n"
        "platforms: [linux]\n"
        "metadata:\n"
        "  hermes:\n"
        f"    tags: [lazyown, {name}]\n"
        "    homepage: https://github.com/grisuno/LazyOwn\n"
        "---\n"
    )


def available_skills() -> list[str]:
    """Return repo skill names that ship a SKILL.md."""
    out = []
    if not SKILLS_DIR.is_dir():
        return out
    for child in sorted(SKILLS_DIR.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file() and child.name != "__pycache__":
            out.append(child.name)
    return out


def mirror_skill(name: str) -> dict:
    """Write the Hermes mirror of one skill.

    Args:
        name: Repo skill directory name.

    Returns:
        Summary with path and changed flag; never raises.
    """
    summary: dict = {"skill": name, "path": "", "changed": False}
    try:
        source = SKILLS_DIR / name / "SKILL.md"
        if not source.is_file():
            return {**summary, "error": f"skill not found: {name}"}
        text = source.read_text(encoding="utf-8")
        fields, body = _split_frontmatter(text)
        dest = SKILLS_DIR / name / "hermes" / "SKILL.md"
        rendered = _hermes_frontmatter(name, fields) + "\n" + body.lstrip("\n")
        if dest.is_file() and dest.read_text(encoding="utf-8") == rendered:
            return {**summary, "path": str(dest)}
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered, encoding="utf-8")
        summary.update({"path": str(dest), "changed": True})
    except Exception as exc:
        summary["error"] = str(exc)[:200]
    return summary


def mirror_all() -> dict:
    """Mirror every repo skill; return per-skill summaries."""
    results = [mirror_skill(name) for name in available_skills()]
    return {"mirrored": len([r for r in results if not r.get("error")]), "results": results}


def _hermes_config_path() -> Path:
    """Return the operator hermes config path."""
    return Path.home() / ".hermes" / "config.yaml"


def register_external_dirs() -> dict:
    """Register the repo skills tree in the hermes config.

    Appends the ``skills/<name>/hermes`` parents to
    ``skills.external_dirs`` (deduplicated) with a timestamped backup.
    Idempotent: a registered tree reports unchanged without writing.

    Returns:
        Summary with changed flag and backup path; never raises.
    """
    summary: dict = {"changed": False, "backup": "", "path": str(_hermes_config_path())}
    try:
        import yaml
    except ImportError:
        return {**summary, "error": "pyyaml not installed"}
    try:
        path = _hermes_config_path()
        if not path.is_file():
            return {**summary, "error": "hermes config not found"}
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        section = data.setdefault("skills", {})
        dirs = list(section.get("external_dirs") or [])
        wanted = [str(SKILLS_DIR / name / "hermes") for name in available_skills()]
        missing = [entry for entry in wanted if entry not in dirs]
        if not missing:
            return summary
        summary["backup"] = str(path.with_suffix(path.suffix + f".bak-{int(time.time())}"))
        shutil.copy2(path, summary["backup"])
        section["external_dirs"] = dirs + missing
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        summary["changed"] = True
    except Exception as exc:
        summary["error"] = str(exc)[:200]
    return summary


__all__ = ["available_skills", "mirror_all", "mirror_skill", "register_external_dirs"]
