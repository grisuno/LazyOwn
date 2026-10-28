"""Behavioural tests for the lab-only default scope guard.

Given an autonomous loop round with no explicit task scope, when the loop
resolves a target for a step, then public addresses and hostnames that
resolve outside the lab are denied while loopback, RFC1918 space and
operator-approved allowlist entries pass.
"""

from __future__ import annotations

from pathlib import Path

from modules import lazy_loop as lazy_loop_module
from modules import lazy_scope


class TestAddressClassification:
    """Given IP literals, classification follows lab-only rules."""

    def test_loopback_and_rfc1918_are_lab(self):
        for address in ["127.0.0.1", "10.0.0.5", "192.168.122.95", "172.16.0.9", "172.31.255.1"]:
            assert lazy_scope.is_lab_address(address), address

    def test_public_addresses_are_not_lab(self):
        for address in ["8.8.8.8", "1.1.1.1", "93.184.216.34"]:
            assert not lazy_scope.is_lab_address(address), address

    def test_ipv6_loopback_and_unique_local_are_lab(self):
        for address in ["::1", "fe80::1", "fd00::5"]:
            assert lazy_scope.is_lab_address(address), address

    def test_ipv4_mapped_public_is_not_lab(self):
        assert not lazy_scope.is_lab_address("::ffff:8.8.8.8")

    def test_ipv4_mapped_private_is_lab(self):
        assert lazy_scope.is_lab_address("::ffff:192.168.1.10")

    def test_garbage_is_not_lab(self):
        assert not lazy_scope.is_lab_address("not-an-ip")
        assert not lazy_scope.is_lab_address("")


class TestHostExtraction:
    """Given free text, candidate hosts are pulled out in order."""

    def test_ips_and_domains_extracted(self):
        hosts = lazy_scope.extract_hosts("nmap -sV 10.0.0.5 corp.example.com 192.168.1.1")
        assert hosts == ["10.0.0.5", "corp.example.com", "192.168.1.1"]

    def test_file_suffixes_are_not_hosts(self):
        hosts = lazy_scope.extract_hosts("cat payload.json report.md")
        assert "payload.json" not in hosts
        assert "report.md" not in hosts

    def test_duplicates_collapse(self):
        hosts = lazy_scope.extract_hosts("ping 10.0.0.5 && ping 10.0.0.5")
        assert hosts == ["10.0.0.5"]

    def test_empty_text_yields_nothing(self):
        assert lazy_scope.extract_hosts("") == []


class TestScopeVerdict:
    """Given a target, the verdict allows only lab-local answers."""

    def test_lab_ip_literal_allowed(self):
        verdict = lazy_scope.scope_verdict("192.168.122.95")
        assert verdict.allowed

    def test_public_ip_literal_denied(self):
        verdict = lazy_scope.scope_verdict("8.8.8.8")
        assert not verdict.allowed
        assert verdict.reason == "public-ip"

    def test_hostname_resolving_private_allowed(self):
        verdict = lazy_scope.scope_verdict("winbox.lab", resolver=lambda name: ("10.1.1.9",))
        assert verdict.allowed

    def test_hostname_resolving_public_denied(self):
        verdict = lazy_scope.scope_verdict("evil.com", resolver=lambda name: ("8.8.8.8",))
        assert not verdict.allowed
        assert verdict.reason == "public-resolve"

    def test_mixed_answers_denied(self):
        verdict = lazy_scope.scope_verdict(
            "split.brain", resolver=lambda name: ("10.0.0.1", "8.8.4.4")
        )
        assert not verdict.allowed

    def test_unresolved_denied(self):
        verdict = lazy_scope.scope_verdict("ghost.lab", resolver=lambda name: ())
        assert not verdict.allowed
        assert verdict.reason == "unresolved"

    def test_allowlist_entry_allowed(self):
        verdict = lazy_scope.scope_verdict(
            "partner.example.com",
            resolver=lambda name: (),
            allowlist=frozenset({"partner.example.com"}),
        )
        assert verdict.allowed

    def test_empty_target_denied(self):
        verdict = lazy_scope.scope_verdict("")
        assert not verdict.allowed


class TestCommandScope:
    """Given a whole command line, every host inside must pass."""

    def test_all_lab_command_allowed(self):
        verdict = lazy_scope.command_scope_verdict("nmap -sV 10.0.0.5 192.168.1.1")
        assert verdict.allowed

    def test_one_public_host_blocks_command(self):
        verdict = lazy_scope.command_scope_verdict("curl http://8.8.8.8/payload")
        assert not verdict.allowed
        assert verdict.reason == "public-ip"

    def test_hostname_public_blocks_command(self):
        verdict = lazy_scope.command_scope_verdict(
            "curl http://telemetry.example.com/x",
            resolver=lambda name: ("8.8.8.8",),
        )
        assert not verdict.allowed


class TestAllowlist:
    """Given the operator allowlist file, entries load clean."""

    def test_missing_file_is_empty(self, tmp_path: Path):
        assert lazy_scope.read_allowlist(tmp_path) == frozenset()

    def test_comments_and_blanks_skipped(self, tmp_path: Path):
        (tmp_path / lazy_scope.ALLOWLIST_FILENAME).write_text(
            "# approved\n\npartner.example.com\n10.9.9.9\n",
            encoding="utf-8",
        )
        allowed = lazy_scope.read_allowlist(tmp_path)
        assert allowed == frozenset({"partner.example.com", "10.9.9.9"})


class TestLoopWiring:
    """Given the autonomous loop, the lab default guards unscooped targets."""

    def test_scope_default_method_wired(self):
        source = Path(lazy_loop_module.__file__).read_text(encoding="utf-8")
        assert "_lab_scope_default" in source
        assert "scope-lab-default" in source
