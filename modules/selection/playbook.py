"""Playbook selector: run an APT actor emulation named by the objective.

Single contract: when the task goal names a known APT actor (from the
``playbooks/`` library, by actor name, alias or chain slug) and a matching
``apt_<slug>`` chain exists, propose running it end to end via
``apt_chain``. The mapping source of truth is the chain side: every
generated ``apt_<slug>`` chain pins ``defaults.playbook`` to the exact
playbook key, so the selector enumerates chains once and links them to
the playbook summaries through that key. Conservative: abstains unless
the goal clearly names an actor, so it never emulates an actor the
operator did not ask for.
"""

from __future__ import annotations

import re
from pathlib import Path

from modules.selection.base import ActionDecision, SelectionContext

BASE_DIR = Path(__file__).resolve().parent.parent.parent
_WORD_RE = re.compile(r"[a-z0-9]+")
_MIN_TOKEN = 4


def _goal_tokens(goal: str) -> set[str]:
    """Whole words of the goal, long enough to mean an actor.

    Args:
        goal: Task goal text.

    Returns:
        Set of lowercase tokens with at least 4 characters.
    """
    return {token for token in _WORD_RE.findall(str(goal or "").lower()) if len(token) >= _MIN_TOKEN}


def _summary_words(summary: dict) -> set[str]:
    """Whole words of the actor's name and published aliases.

    Args:
        summary: ``AptPlaybook.to_summary()`` dict.

    Returns:
        Lowercase word set without fragments.
    """
    words = set(_WORD_RE.findall(str(summary.get("apt_name") or "").lower()))
    for alias in summary.get("aliases") or []:
        words |= set(_WORD_RE.findall(str(alias).lower()))
    return {word for word in words if word}


def _matches(tokens: set[str], words: set[str]) -> str | None:
    """Whole-word or >=4-char prefix match of goal tokens onto actor words.

    Args:
        tokens: Goal tokens (already length-filtered).
        words: Playbook alias words.

    Returns:
        The matched goal token, or None. ``lazarus`` matches
        ``lazarusgroup`` and ``zinc`` matches its alias; short
        stop-words never match.
    """
    for token in sorted(tokens):
        for word in words:
            if word == token:
                return token
            if len(token) >= _MIN_TOKEN and word.startswith(token):
                return token
    return None


class PlaybookSelector:
    """Propose ``apt_chain apt_<slug> <target>`` when the goal names an actor."""

    name = "playbook"

    def __init__(self, playbook_dir: str = "playbooks") -> None:
        """Bind the playbook directory for summary loading.

        Args:
            playbook_dir: Playbook directory; relative names anchor to
                the repo root when the working directory lacks one.
        """
        self._dir = playbook_dir

    def _summaries_with_binding(self) -> list[tuple[dict, str]]:
        """Return ``(summary, chain_name)`` pairs joined via defaults.playbook.

        Enumerates the playbook summaries once; the chain registry owns
        the mapping because every generated ``apt_<slug>`` chain pins
        ``defaults.playbook`` to the exact playbook key the engine uses.

        Returns:
            Joined pairs; empty when either library is unavailable.
        """
        try:
            from modules.apt_playbooks import AptPlaybookEngine
            from modules.chain_registry import load_all

            directory = self._dir
            if not Path(directory).exists():
                candidate = BASE_DIR / directory
                if candidate.exists():
                    directory = str(candidate)
            summaries = AptPlaybookEngine(playbook_dir=directory).list_playbooks()
        except Exception:
            return []
        binding: dict[str, str] = {}
        try:
            for chain_name, chain in load_all().items():
                if chain_name == "apt_chain":
                    continue
                playbook_key = str((chain.defaults or {}).get("playbook") or "").strip()
                if playbook_key and chain_name.startswith("apt_") and not binding.get(playbook_key):
                    binding[playbook_key] = chain_name
        except Exception:
            return []
        bound: list[tuple[dict, str]] = []
        for summary in summaries:
            key = str(summary.get("apt_name") or "").lower().replace(" ", "_")
            chain_name = binding.get(key)
            if chain_name:
                bound.append((summary, chain_name))
        return bound

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return an actor-emulation action when the goal names one, else None.

        Args:
            ctx: Live engagement snapshot from the runtime.

        Returns:
            A ``apt_chain <chain> <target>`` decision when the goal names
            an actor with a live chain, else None.
        """
        goal = str(ctx.extra.get("goal", "") or "").lower()
        if not ctx.target or not goal:
            return None
        tokens = _goal_tokens(goal)
        if not tokens:
            return None
        for summary, chain_name in self._summaries_with_binding():
            token = _matches(tokens, _summary_words(summary))
            if not token:
                continue
            command = f"apt_chain {chain_name} {ctx.target}"
            if command in ctx.exclude:
                continue
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"goal names APT actor {str(summary.get('apt_name'))} via '{token}'",
                priority=4,
            )
        return None


__all__ = ["PlaybookSelector"]
