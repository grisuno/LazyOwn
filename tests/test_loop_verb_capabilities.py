"""Verb capability metadata downgrades privileged verbs unattended (bug 2.5).

lazynmap needs root and a tty; the unattended loop has neither, so it degraded
and the planner kept re-proposing it (lazynmap -> block -> suggest -> lazynmap).
The loop now recognises the capability requirement and substitutes an
unprivileged scan (nmap -sT) at one execution chokepoint.
"""

from __future__ import annotations

import inspect

import modules.lazy_loop as loop
import modules.verb_capabilities as caps
import utils


def test_requires_privilege_flags_only_privileged_verbs():
    """Only verbs that need root or a tty are flagged."""
    assert caps.requires_privilege("lazynmap 172.17.0.2") is True
    assert caps.requires_privilege("/usr/local/bin/lazynmap 10.0.0.5") is True
    assert caps.requires_privilege("nmap -sT 172.17.0.2") is False
    assert caps.requires_privilege("curl -sS http://x") is False
    assert caps.requires_privilege("") is False


def test_capability_of_returns_record_or_empty():
    """Known verbs expose their requirements; unknown verbs return empty."""
    record = caps.capability_of("lazynmap 172.17.0.2")
    assert record["requires_root"] is True
    assert record["requires_tty"] is True
    assert record["fallback"].startswith("nmap -sT")
    assert caps.capability_of("nmap 1.2.3.4") == {}


def test_downgrade_rewrites_lazynmap_to_unprivileged_scan():
    """A lazynmap command becomes an unprivileged nmap connect scan."""
    rewritten, note = caps.downgrade_for_unattended("lazynmap 172.17.0.2", "172.17.0.2")
    assert rewritten == "nmap -sT -sV --top-ports 100 172.17.0.2"
    assert "downgrade" in note

    from_args, _ = caps.downgrade_for_unattended("lazynmap 10.9.9.9")
    assert from_args.endswith("10.9.9.9")


def test_downgrade_leaves_non_privileged_commands_untouched():
    """A command with no capability record is returned unchanged."""
    assert caps.downgrade_for_unattended("nmap -sT 172.17.0.2") == ("nmap -sT 172.17.0.2", "")


def test_worker_downgrade_depends_on_sudo_availability(monkeypatch):
    """The worker downgrades only when passwordless sudo is unavailable."""
    worker = loop.Worker.__new__(loop.Worker)

    monkeypatch.setattr(utils, "sudo_available", lambda: False)
    command, note = worker._downgrade_privileged("lazynmap 172.17.0.2", "172.17.0.2")
    assert command == "nmap -sT -sV --top-ports 100 172.17.0.2"
    assert note

    monkeypatch.setattr(utils, "sudo_available", lambda: True)
    command, note = worker._downgrade_privileged("lazynmap 172.17.0.2", "172.17.0.2")
    assert command == "lazynmap 172.17.0.2"
    assert note == ""


def test_guard_step_wires_the_capability_downgrade():
    """The shared execution path invokes the capability downgrade."""
    src = inspect.getsource(loop.Worker._guard_step)
    assert "_downgrade_privileged" in src


def test_prompts_no_longer_hard_prefer_lazynmap():
    """The agentic prompts stop telling the model to prefer lazynmap."""
    import modules.loop.worker_agentic as agentic

    text = inspect.getsource(agentic)
    assert "Prefer lazynmap" not in text
    assert "nmap -sT" in text
