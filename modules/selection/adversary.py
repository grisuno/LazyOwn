"""Adversary selector: run a custom adversary emulation named by the objective.

Single contract: when the task goal names a custom adversary profile from
``lazyadversaries/*.yaml`` (by file slug, entry name or goal words), resolve
it to the concrete emulation id the ``adversary_yaml`` verb expects and
propose executing it locally: ``adversary_yaml <id> l``. Conservative:
abstains unless the goal names a known profile, so it never emulates an
adversary the operator did not ask for.
"""

from __future__ import annotations

import re
from pathlib import Path

from modules.selection.base import ActionDecision, SelectionContext

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_ADVERSARIES_DIR = BASE_DIR / "lazyadversaries"

_WORD_RE = re.compile(r"[a-z0-9_]+")
_MIN_TOKEN = 4


def load_profiles(adversaries_dir: str | Path | None = None) -> list[dict]:
    """Load every adversary profile dictionary shipped in the repo.

    Reads each ``lazyadversaries/*.yaml`` the same way the legacy shell
    loader does (lists extend, dicts stand alone) and projects every
    usable row onto ``{"id", "file", "slug", "name"}``.

    Args:
        adversaries_dir: Optional directory override; the repo default
            is anchored to the project root so the loader works from any
            working directory.

    Returns:
        A list of profile dicts; never raises.
    """
    import yaml

    directory = Path(adversaries_dir) if adversaries_dir else DEFAULT_ADVERSARIES_DIR
    try:
        files = sorted(directory.glob("*.yaml"))
    except OSError:
        return []
    profiles: list[dict] = []
    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
        slug = path.stem.strip().lower()
        for row in rows:
            if not isinstance(row, dict):
                continue
            try:
                profile_id = int(row.get("id"))
            except (TypeError, ValueError):
                continue
            name = str(row.get("name") or "").strip()
            if not name:
                continue
            profiles.append({
                "id": profile_id,
                "file": path.name,
                "slug": slug,
                "name": re.sub(r"\.\w+$", "", name).strip().lower(),
            })
    return profiles


def _goal_tokens(goal: str) -> set[str]:
    """Split the goal into comparable whole words (underscores kept)."""
    return {token for token in _WORD_RE.findall(str(goal or "").lower()) if token}


def resolve_profile(goal: str, adversaries_dir: str | Path | None = None) -> dict | None:
    """Resolve the adversary profile the goal names, if any.

    A profile matches when a goal token equals or prefixes its slug,
    its artifacts name or its file slug (so ``malleable beacon`` and
    ``malleable_beacon`` both resolve; whole-word prefix keeps ``amsi``
    and short real names reachable without matching random stop-words).
    When several profiles match, the one with the most matched words
    wins, so ``malleable beacon implant`` picks ``malleable_beacon``
    over any profile that merely shares the word ``implant``.

    Args:
        goal: Task goal text.
        adversaries_dir: Optional directory override.

    Returns:
        The matched profile dict from :func:`load_profiles`, or None.
    """
    tokens = _goal_tokens(goal)
    if not tokens:
        return None
    best: dict | None = None
    best_score: tuple[int, int] = (0, 0)
    for profile in load_profiles(adversaries_dir):
        words = set(_WORD_RE.findall(profile["slug"])) | set(_WORD_RE.findall(profile["name"]))
        matched = [
            token
            for token in sorted(tokens)
            if len(token) >= _MIN_TOKEN and any(word == token or word.startswith(token) for word in words)
        ]
        if not matched:
            continue
        score = (len(matched), max(len(token) for token in matched))
        if score > best_score:
            best, best_score = profile, score
    return best


class AdversarySelector:
    """Propose ``adversary_yaml <id> l`` when the goal names a profile."""

    name = "adversary"

    def __init__(self, adversaries_dir: str | Path | None = None, confirm: str = "l") -> None:
        """Bind the profile directory and the execution confirmation word.

        Args:
            adversaries_dir: Optional directory override; repo root is
                the default anchor.
            confirm: Verb execution confirmation (``l`` local, ``r``
                remote C2, ``n`` none). The loop proposes ``l`` by
                default because the goal explicitly named the profile.
        """
        self._dir = adversaries_dir
        self._confirm = confirm

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return the emulation action when the goal names a profile."""
        goal = str(ctx.extra.get("goal", "") or "")
        if not goal:
            return None
        profile = resolve_profile(goal, self._dir)
        if profile is None:
            return None
        command = f"adversary_yaml {profile['id']} {self._confirm}"
        if command in ctx.exclude:
            return None
        return ActionDecision(
            command=command,
            source=self.name,
            reason=(
                f"goal names adversary profile {profile['slug']} "
                f"(id={profile['id']}, artifact {profile['name']})"
            ),
            priority=4,
            mitre="",
        )


__all__ = ["DEFAULT_ADVERSARIES_DIR", "AdversarySelector", "load_profiles", "resolve_profile"]
