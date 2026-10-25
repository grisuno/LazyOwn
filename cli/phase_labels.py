"""Canonical human-readable labels for kill-chain command phases.

Single source of truth for the phase display names used by the CLI hint
system. The keys mirror the ``phase_to_commands`` buckets of
``cli/command_index.json`` (produced by ``scripts/build_command_index.py``)
so every consumer renders the same label for the same phase key.
"""

from __future__ import annotations

PHASE_LABELS: dict[str, str] = {
    "recon": "Reconnaissance",
    "enum": "Enumeration",
    "exploit": "Exploitation",
    "postexp": "Post-Exploitation",
    "persist": "Persistence",
    "privesc": "Privilege Escalation",
    "cred": "Credential Access",
    "lateral": "Lateral Movement",
    "exfil": "Exfiltration",
    "c2": "Command & Control",
    "report": "Reporting",
    "misc": "Miscellaneous",
    "diagnostics": "Diagnostics",
    "uncategorized": "Uncategorized",
}


def phase_label(phase: str) -> str:
    """Return the human label for a phase, falling back to title case.

    Args:
        phase: Canonical phase key (e.g. ``recon``).

    Returns:
        The display label, or the title-cased key when unknown.
    """
    key = (phase or "").strip().lower()
    return PHASE_LABELS.get(key) or (key.title() if key else "Unknown")
