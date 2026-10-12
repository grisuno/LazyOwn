"""Skill context injection for planner/worker prompts.

Scans the repository ``skills/`` tree for SKILL.md documents (and loose
markdown guides), matches them against the task goal with keyword
scoring and feeds bounded excerpts into :func:`build_prompt_context`,
so the autonomous LLM agents inherit operator playbooks without a
separate tool call.

Selection contract:
    ``lazy_skill inject <name> --task T`` pins a skill in the task
    record; auto-matching stays on unless ``lazy_skill auto off``.
"""

from __future__ import annotations

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = BASE_DIR / "skills"
MAX_SKILLS = 3
EXCERPT_CHARS = 600
MIN_KEYWORD_LEN = 3

_CACHE: dict[str, tuple[float, dict]] = {}


def _frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from the body, tolerating its absence."""
    meta: dict = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                key, _, value = line.partition(":")
                if value.strip():
                    meta[key.strip().lower()] = value.strip().strip("\"'")
            text = text[end + 4:]
    return meta, text


def _skill_files() -> list[Path]:
    """Return skill documents: ``*/SKILL.md`` plus loose ``*.md`` guides."""
    files: list[Path] = []
    try:
        files.extend(sorted(SKILLS_DIR.glob("*/SKILL.md")))
        files.extend(sorted(path for path in SKILLS_DIR.glob("*.md") if path.is_file()))
    except OSError:
        return []
    return files


def _load(path: Path) -> dict:
    """Parse one skill document with an mtime cache."""
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return {}
    cached = _CACHE.get(str(path))
    if cached and cached[0] == mtime:
        return cached[1]
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    meta, body = _frontmatter(raw)
    default_name = path.parent.name if path.name == "SKILL.md" else path.stem
    name = str(meta.get("name") or default_name)
    description = str(meta.get("description") or "").strip()
    if not description:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                description = stripped
                break
    collapsed = re.sub(r"\s+", " ", re.sub(r"^#.*$", "", body, flags=re.MULTILINE)).strip()
    keywords = {token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]+", f"{name} {description}")
                if len(token) >= MIN_KEYWORD_LEN}
    entry = {"name": name, "path": str(path), "description": description[:300],
             "excerpt": collapsed[:EXCERPT_CHARS], "keywords": sorted(keywords)}
    _CACHE[str(path)] = (mtime, entry)
    return entry


def list_skills() -> list[dict]:
    """Return every parsed skill sorted by name."""
    entries = [_load(path) for path in _skill_files()]
    return sorted((entry for entry in entries if entry), key=lambda item: item["name"])


def get_skill(name: str) -> dict | None:
    """Find one skill by exact or case-insensitive name."""
    wanted = (name or "").strip().lower()
    if not wanted:
        return None
    for entry in list_skills():
        if entry["name"].lower() == wanted:
            return entry
    return None


def match_skills(text: str, limit: int = MAX_SKILLS) -> list[dict]:
    """Rank skills whose keywords appear in the text, best first."""
    lowered = (text or "").lower()
    if not lowered.strip():
        return []
    scored: list[tuple[int, dict]] = []
    for entry in list_skills():
        score = sum(1 for keyword in entry["keywords"] if keyword in lowered)
        if entry["name"].lower() in lowered:
            score += 2
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["name"]))
    return [entry for _score, entry in scored[: max(1, int(limit))]]


def skills_context(text: str = "", explicit: list[str] | None = None,
                   auto: bool = True, budget: int = 800) -> str:
    """Render pinned plus auto-matched skills as one prompt section.

    Args:
        text: Goal/intent text used for auto matching.
        explicit: Skill names pinned on the task record.
        auto: Whether keyword auto-matching runs.
        budget: Max characters of the rendered section.

    Returns:
        ``Skills: name :: excerpt | ...`` or an empty string.
    """
    chosen: list[dict] = []
    seen: set[str] = set()
    for name in explicit or []:
        entry = get_skill(str(name))
        if entry and entry["name"] not in seen:
            chosen.append(entry)
            seen.add(entry["name"])
    if auto:
        for entry in match_skills(text, limit=MAX_SKILLS):
            if entry["name"] not in seen:
                chosen.append(entry)
                seen.add(entry["name"])
    if not chosen:
        return ""
    chunks = [f"{entry['name']}: {entry['excerpt'][:300]}" for entry in chosen[:MAX_SKILLS]]
    return ("Skills: " + " | ".join(chunks))[: max(200, int(budget))]


__all__ = ["EXCERPT_CHARS", "MAX_SKILLS", "SKILLS_DIR",
           "get_skill", "list_skills", "match_skills", "skills_context"]
