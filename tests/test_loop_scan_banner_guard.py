"""The scanner-banner guard: a scan that echoes a backdoor's shell prompt in
its fingerprint must never be mistaken for a live foothold.

Metasploitable's ingreslock backdoor (port 1524) answers nmap's service probe
with a live ``root@host:/#`` prompt, which nmap embeds verbatim in its report.
The shell detector therefore sees shell evidence inside pure recon output and
the loop would announce ``interactive shell obtained via nmap`` and advance the
kill chain on a phantom foothold. A scanner can never own a session, so the
loop ignores the banner; a genuine ``nc`` to the same backdoor still proves the
shell.

Every scenario states Given, When, Then.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

NMAP_INGRESLOCK_OUTPUT = """PORT     STATE SERVICE     VERSION
1524/tcp open  ingreslock?
1 service unrecognized despite returning data.
SF-Port1524-TCP:V=7.991%I=7%D=11/19%r(NULL,15,"root@5ad8907eff5d:/#\\x20")
"""

NC_SHELL_OUTPUT = "root@5ad8907eff5d:/# id\nuid=0(root) gid=0(root) groups=0(root)\n"


def _intent(node_id: int = 3):
    """ExploreLike node stub carrying only the fields the helper reads."""
    return SimpleNamespace(node_id=node_id)


def _worker(task_id: str = "t-scan-guard"):
    """Minimal worker with only the fields ``_publish_shell_proof`` touches."""
    from modules.lazy_loop import Worker

    return Worker("worker-scan", task_id, None, None, None, None, None, None, shell=None)


@pytest.fixture()
def sink_log():
    """Reset the process-wide bus and capture published events."""
    from modules import outcome_bus

    outcome_bus.reset_bus()
    published: list = []

    def fake_record(**kwargs):
        from modules.outcome_bus import OutcomeEvent

        published.append(OutcomeEvent(**kwargs))
        return {"event_bus": True}

    original = outcome_bus.record_event
    outcome_bus.record_event = fake_record
    try:
        yield published
    finally:
        outcome_bus.record_event = original
        outcome_bus.reset_bus()


class TestScanOnlyVerb:
    def test_scanners_are_scan_only(self):
        """Given scanner verbs, When classified, Then each is scan-only."""
        from modules.atomic_exploit_bridge import is_scan_only_verb

        for command in (
            "nmap -sT -sV 172.17.0.2",
            "lazynmap 172.17.0.2",
            "masscan -p1-65535 10.0.0.0/8",
            "/usr/bin/rustscan -a 172.17.0.2",
            "naabu -host 172.17.0.2",
            "sudo nmap -sS 172.17.0.2",
            "sudo -n masscan -p80 10.0.0.0/8",
        ):
            assert is_scan_only_verb(command), command

    def test_interactive_shell_verbs_are_not_scan_only(self):
        """Given verbs that legitimately open a shell, When classified,
        Then none is scan-only, so a real foothold is never suppressed."""
        from modules.atomic_exploit_bridge import is_scan_only_verb

        for command in (
            "nc 172.17.0.2 1524",
            "ncat 172.17.0.2 1524",
            "telnet 172.17.0.2 23",
            "socat - TCP:172.17.0.2:1524",
            "auto_pwn 172.17.0.2",
            "atomic_shell --interactive",
            "",
        ):
            assert not is_scan_only_verb(command), command


class TestScanBannerGuard:
    def test_detector_fires_on_the_nmap_banner(self):
        """Given nmap output that embeds the ingreslock prompt, When the shell
        detector runs, Then it fires: the guard, not a weak detector, is what
        prevents the false positive."""
        from modules.atomic_exploit_bridge import shell_output_evidence

        assert shell_output_evidence(NMAP_INGRESLOCK_OUTPUT) is True

    def test_scan_banner_never_publishes_a_shell(self, sink_log):
        """Given an nmap step whose fingerprint echoes a root prompt, When
        shell-proof publication runs, Then no exploit event is published."""
        worker = _worker("t-scan-suppress")
        result = worker._publish_shell_proof(
            _intent(), "172.17.0.2", "nmap -sT -sV 172.17.0.2", NMAP_INGRESLOCK_OUTPUT
        )
        assert result is False, "a scanner banner must not fabricate a foothold"
        assert sink_log == [], "no exploit event may reach the bus from a scan banner"

    def test_real_nc_shell_still_publishes(self, sink_log):
        """Given a genuine nc session to the same backdoor, When shell-proof
        publication runs, Then one exploit outcome with the shell flag lands:
        the guard suppresses only scanners, never real footholds."""
        worker = _worker("t-nc-shell")
        result = worker._publish_shell_proof(
            _intent(), "172.17.0.2", "nc 172.17.0.2 1524", NC_SHELL_OUTPUT
        )
        assert result is True, "a real nc foothold must still publish"
        event = sink_log[-1]
        assert event.kind == "exploit" and event.shell and event.success
        assert event.target == "172.17.0.2" and event.task_id == "t-nc-shell"
