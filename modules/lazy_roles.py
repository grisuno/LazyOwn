"""Lazy specialist roles for the autonomous loop.

Ports the useful half of the multi-agent pattern (dedicated planning,
execution, memory, review and repair perspectives) with Lazy branding and
Lazy execution semantics: roles are prompt perspectives over the existing
``LlmPool``, not separate services. Workers keep executing real Lazy shell
commands through the Guard; a role only shapes what the model proposes.

Stdlib only.
"""

from __future__ import annotations

LAZY_ROLES: dict[str, dict] = {
    "scout": {
        "lane": "search",
        "phases": ("recon", "enum"),
        "prompt": (
            "You are the Lazy scout. Research the target surface and return "
            "concrete next probes. Lazy commands are high-level abstractions: "
            "payload auto-injects rhost and wordlists. Reply with ONLY one "
            "Lazy command name plus its target."
        ),
    },
    "pwner": {
        "lane": "environment",
        "phases": ("exploit", "lateral"),
        "prompt": (
            "You are the Lazy pwner. Turn confirmed services into access. "
            "Prefer the smallest reliable Lazy exploit primitive for the "
            "phase. Reply with ONLY one Lazy command name plus its target."
        ),
    },
    "coder": {
        "lane": "environment",
        "phases": ("exploit", "persist", "c2"),
        "prompt": (
            "You are the Lazy coder. Write or adapt the smallest script that "
            "unblocks the intent. Keep it portable, non-interactive and "
            "staged under sessions/ with a stable filename."
        ),
    },
    "keeper": {
        "lane": "memory",
        "phases": ("recon", "enum", "exploit", "report"),
        "prompt": (
            "You are the Lazy keeper. Recall what this campaign already "
            "proved: prior facts, findings and tool outcomes for this "
            "target. Cite intent ids and digests, never invent results."
        ),
    },
    "sage": {
        "lane": "review",
        "phases": ("recon", "enum", "exploit", "privesc", "lateral", "report"),
        "prompt": (
            "You are the Lazy sage, senior reviewer. Assess progress, name "
            "the single biggest blocker, propose one alternative approach, "
            "and state the next step. Be terse and evidence-bound."
        ),
    },
    "wright": {
        "lane": "environment",
        "phases": ("recon", "exploit"),
        "prompt": (
            "You are the Lazy wright. Prepare the environment: missing "
            "binaries, wordlists, listeners and payload staging. Every "
            "setup step must be non-interactive and idempotent."
        ),
    },
    "mirror": {
        "lane": "review",
        "phases": ("exploit", "privesc", "report"),
        "prompt": (
            "You are the Lazy mirror. Re-examine the last intent outcome "
            "against the original goal. Decide reproduced, fixed or "
            "inconclusive, and say what single replay would settle it."
        ),
    },
    "scribe": {
        "lane": "report",
        "phases": ("report",),
        "prompt": (
            "You are the Lazy scribe. Compress transcripts into a dense "
            "finding: affected asset, evidence lines, impact and replay. "
            "Keep hosts, ports, credentials and versions; drop repetition."
        ),
    },
    "mender": {
        "lane": "repair",
        "phases": ("recon", "enum", "exploit", "privesc", "lateral", "report"),
        "prompt": (
            "You are the Lazy mender. Repair the failed tool call with the "
            "minimal change that satisfies its schema: keep the original "
            "intent, fix only the broken argument, return single-line JSON."
        ),
    },
}


def list_roles() -> list[dict]:
    """Return every Lazy role descriptor.

    Returns:
        List of dicts with name, lane, phases and prompt.
    """
    return [{"name": name, **spec} for name, spec in LAZY_ROLES.items()]


def role_prompt(role: str, goal: str = "", context: str = "") -> str:
    """Build the system prompt for one role.

    Args:
        role: Role name from :data:`LAZY_ROLES`.
        goal: Current task goal prepended as objective.
        context: Optional bounded context appended after the role brief.

    Returns:
        Full prompt text.

    Raises:
        KeyError: Unknown role.
    """
    clean = (role or "").strip().lower()
    if clean not in LAZY_ROLES:
        raise KeyError(f"unknown lazy role: {role!r}")
    parts = [LAZY_ROLES[clean]["prompt"]]
    if (goal or "").strip():
        parts.append(f"Objective: {goal.strip()[:500]}")
    if (context or "").strip():
        parts.append(f"Context: {context.strip()[:2000]}")
    return "\n".join(parts)


def roles_for_phase(phase: str) -> list[str]:
    """Return role names serving one kill-chain phase.

    Args:
        phase: Kill-chain phase.

    Returns:
        Role names in definition order.
    """
    wanted = (phase or "").strip().lower()
    return [name for name, spec in LAZY_ROLES.items() if wanted in spec["phases"]]


CONFORMANCE_PROBE = (
    "Task: name the single best Lazy shell command for a TCP port scan of 10.0.0.5. "
    "Reply with ONLY the command line."
)
CONFORMANCE_FILE = "llm_conformance.json"


def conformance(role: str = "") -> dict:
    """Probe every pool member with role prompts, like provider conformance.

    Each member answers the same fixed probe under each role perspective.
    Results persist to ``sessions/lazy/llm_conformance.json`` with a
    fastest-healthy affinity map (role -> member) the planner can prefer.

    Args:
        role: Single role to probe, or all roles when empty.

    Returns:
        Summary with per-member results and affinity. Never raises.
    """
    import json
    import time
    from pathlib import Path as _Path

    summary: dict = {"members": 0, "roles": [], "affinity": {}}
    try:
        from modules.lazy_engine import LlmPool
        from modules.lazy_loop import _llm_error_reply

        pool = LlmPool()
        members = pool.members()
        summary["members"] = len(members)
        if not members:
            return summary
        wanted = [str(role or "").strip().lower()] if (role or "").strip() else list(LAZY_ROLES)
        wanted = [r for r in wanted if r in LAZY_ROLES]
        summary["roles"] = wanted
        results: dict[str, dict[str, dict]] = {}
        for member in members:
            name = str(member.get("name", ""))
            lane: dict[str, dict] = {}
            for role_name in wanted:
                prompt = role_prompt(role_name, "conformance probe") + "\n" + CONFORMANCE_PROBE
                start = time.monotonic()
                try:
                    reply = pool.complete(
                        prompt,
                        max_tokens=60,
                        members=[{"name": name, "model": member.get("model", name), "priority": 0}],
                    ) or ""
                except Exception:
                    reply = ""
                ms = int((time.monotonic() - start) * 1000)
                lane[role_name] = {
                    "ok": bool(reply.strip()) and not _llm_error_reply(reply),
                    "ms": ms,
                    "chars": len(reply.strip()),
                    "reply": reply.strip()[:120],
                }
            results[name] = lane
        affinity = {}
        for role_name in wanted:
            healthy = [(m, r[role_name]["ms"]) for m, r in results.items() if r[role_name]["ok"]]
            affinity[role_name] = min(healthy, key=lambda kv: kv[1])[0] if healthy else ""
        summary["affinity"] = affinity
        try:
            store = _Path(__file__).resolve().parent.parent / "sessions" / "lazy"
            store.mkdir(parents=True, exist_ok=True)
            (store / CONFORMANCE_FILE).write_text(
                json.dumps({"at": time.time(), "results": results, "affinity": affinity}, indent=2), encoding="utf-8"
            )
        except OSError:
            pass
        summary["results"] = results
    except Exception:
        pass
    return summary


__all__ = ["CONFORMANCE_FILE", "CONFORMANCE_PROBE", "LAZY_ROLES", "conformance", "list_roles", "role_prompt", "roles_for_phase"]
