#!/usr/bin/env python3
"""
Tests for lazyown_facts.py — parsers and FactStore.

All file I/O uses tmp_path (pytest) or tempfile.TemporaryDirectory.
No writes to the real sessions/ directory.
"""

from __future__ import annotations

import json
import sys
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

# Make skills/ importable
_SKILLS_DIR = Path(__file__).parent.parent
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))

from lazyown_facts import (
    Config,
    CredentialFact,
    DiscoveredPath,
    FactStore,
    GobusterFfufParser,
    INmapXmlParser,
    KerbruteParser,
    NiktoParser,
    NucleiParser,
    RpcclientParser,
    SecretsdumpParser,
    ServiceFact,
    SslscanParser,
    CrackMapExecParser,
    Enum4linuxParser,
    VulnerabilityFact,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _make_config(tmp_path: Path) -> Config:
    """Return a Config pointing entirely at tmp_path."""
    sessions = tmp_path / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    return Config(
        base_dir=tmp_path,
        sessions_dir=sessions,
        facts_file=sessions / "policy_facts.json",
        xml_glob="scan_*.nmap.xml",
        txt_glob="*.txt",
        log_level="WARNING",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Individual parser unit tests
# ─────────────────────────────────────────────────────────────────────────────


class TestCrackMapExecParser:
    def test_crackmapexec_parser(self):
        """CME output with [+] credential line → extracts CredentialFact."""
        parser = CrackMapExecParser()
        sample = (
            "SMB  10.10.11.78  445  DC01  [+] DOMAIN\\Administrator:Password123\n"
        )
        creds, shares, access = parser.parse("10.10.11.78", sample, "cme.txt")
        assert len(creds) >= 1
        found = next((c for c in creds if c.username == "Administrator"), None)
        assert found is not None, f"Administrator not in {[c.username for c in creds]}"
        assert found.password == "Password123"
        assert found.host == "10.10.11.78"

    def test_crackmapexec_pwned(self):
        """Pwn3d! in CME output → AccessFact with level=admin."""
        parser = CrackMapExecParser()
        sample = (
            "SMB  10.10.11.78  445  DC01  [+] DOMAIN\\admin:Pass123 (Pwn3d!)\n"
        )
        creds, shares, access = parser.parse("10.10.11.78", sample, "cme.txt")
        assert any(a.level == "admin" for a in access)


class TestEnum4linuxParser:
    def test_enum4linux_parser(self):
        """enum4linux user + share line → extracts CredentialFact and ShareFact."""
        parser = Enum4linuxParser()
        sample = textwrap.dedent("""\
            user:[Administrator] rid:[0x1f4]
            user:[Guest] rid:[0x1f5]
            | SYSVOL | Disk | Logon server share |
        """)
        creds, shares, access = parser.parse("10.10.11.78", sample, "enum4linux_10.10.11.78.txt")
        usernames = [c.username for c in creds]
        assert "Administrator" in usernames
        assert "Guest" in usernames
        share_names = [s.share_name for s in shares]
        assert "SYSVOL" in share_names

    def test_enum4linux_access_when_results(self):
        """enum4linux that finds data → AccessFact with level=read."""
        parser = Enum4linuxParser()
        sample = "user:[jsmith] rid:[0x456]\n"
        creds, shares, access = parser.parse("10.10.11.78", sample, "enum4linux.txt")
        assert any(a.level == "read" for a in access)


class TestSecretsdumpParser:
    def test_secretsdump_parser(self):
        """NTLM hash line → CredentialFact with hash_type=NTLM."""
        parser = SecretsdumpParser()
        sample = (
            "DOMAIN\\Administrator:500:"
            "aad3b435b51404eeaad3b435b51404ee:"
            "31d6cfe0d16ae931b73c59d7e0c089c0:::\n"
        )
        creds, shares, access = parser.parse("10.10.11.78", sample, "secretsdump.txt")
        assert len(creds) >= 1
        cred = creds[0]
        assert cred.username == "Administrator"
        assert cred.hash_type == "NTLM"
        assert len(cred.hash_value) == 32
        assert cred.host == "10.10.11.78"


class TestKerbruteParser:
    def test_kerbrute_parser(self):
        """VALID USERNAME line → CredentialFact."""
        parser = KerbruteParser()
        sample = "2024/01/01 00:00:00 >  [+] VALID USERNAME: jsmith@domain.local\n"
        creds, shares, access = parser.parse("10.10.11.78", sample, "kerbrute.txt")
        assert len(creds) >= 1
        assert creds[0].username == "jsmith"
        assert creds[0].host == "10.10.11.78"

    def test_kerbrute_multiple_users(self):
        parser = KerbruteParser()
        sample = (
            "[+] VALID USERNAME: alice@corp.local\n"
            "[+] VALID USERNAME: bob@corp.local\n"
        )
        creds, _, _ = parser.parse("10.10.11.5", sample, "kerbrute.txt")
        usernames = [c.username for c in creds]
        assert "alice" in usernames
        assert "bob" in usernames


class TestRpcclientParser:
    def test_rpcclient_parser(self):
        """user:[Administrator] rid:[0x1f4] → CredentialFact."""
        parser = RpcclientParser()
        sample = "user:[Administrator] rid:[0x1f4]\nuser:[Guest] rid:[0x1f5]\n"
        creds, shares, access = parser.parse("10.10.11.78", sample, "rpcclient.txt")
        usernames = [c.username for c in creds]
        assert "Administrator" in usernames
        assert any(a.level == "read" for a in access)


class TestGobusterParser:
    def test_gobuster_parser_parse_extended(self):
        """/admin (Status: 200) [Size: 1234] → DiscoveredPath."""
        parser = GobusterFfufParser()
        sample = "/admin                (Status: 200) [Size: 1234]\n"
        creds, shares, access, vulns, paths = parser.parse_extended(
            "10.10.11.78", sample, "gobuster.txt", port=80
        )
        assert len(paths) >= 1
        path = paths[0]
        assert path.path == "/admin"
        assert path.status_code == 200
        assert path.size == 1234
        assert path.host == "10.10.11.78"

    def test_gobuster_multiple_paths(self):
        parser = GobusterFfufParser()
        sample = (
            "/admin                (Status: 200) [Size: 1234]\n"
            "/login                (Status: 301) [Size: 0]\n"
            "/api                  (Status: 403) [Size: 99]\n"
        )
        _, _, _, _, paths = parser.parse_extended("10.10.11.5", sample, "gobuster.txt", port=8080)
        path_strs = [p.path for p in paths]
        assert "/admin" in path_strs
        assert "/login" in path_strs
        assert "/api" in path_strs


class TestNiktoParser:
    def test_nikto_parser_parse_extended(self):
        """OSVDB nikto line → VulnerabilityFact with severity=medium."""
        parser = NiktoParser()
        sample = "+ OSVDB-3092: /admin/: This might be interesting...\n"
        creds, shares, access, vulns, paths = parser.parse_extended(
            "10.10.11.78", sample, "nikto.txt", port=80
        )
        assert len(vulns) >= 1
        vuln = vulns[0]
        assert vuln.vuln_id == "OSVDB-3092"
        assert vuln.severity == "medium"
        assert vuln.host == "10.10.11.78"
        assert vuln.source_tool == "nikto"

    def test_nikto_cve_line(self):
        parser = NiktoParser()
        sample = "+ CVE-2021-41773: /cgi-bin/: Possible CVE\n"
        _, _, _, vulns, _ = parser.parse_extended("192.168.1.1", sample, "nikto.txt")
        assert any(v.vuln_id == "CVE-2021-41773" for v in vulns)


class TestNucleiParser:
    def test_nuclei_parser_parse_extended(self):
        """[critical] [CVE-2021-41773] [http] http://host/ → VulnerabilityFact."""
        parser = NucleiParser()
        sample = "[critical] [CVE-2021-41773] [http] http://10.10.11.78/\n"
        creds, shares, access, vulns, paths = parser.parse_extended(
            "10.10.11.78", sample, "nuclei.txt", port=80
        )
        assert len(vulns) >= 1
        vuln = vulns[0]
        assert vuln.vuln_id == "CVE-2021-41773"
        assert vuln.severity == "critical"
        assert vuln.host == "10.10.11.78"
        assert vuln.source_tool == "nuclei"

    def test_nuclei_multiple_severities(self):
        parser = NucleiParser()
        sample = (
            "[high] [rce-template] [http] http://target/rce\n"
            "[info] [tech-detect] [http] http://target/\n"
        )
        _, _, _, vulns, _ = parser.parse_extended("target", sample, "nuclei.txt")
        severities = {v.severity for v in vulns}
        assert "high" in severities
        assert "info" in severities


class TestSslscanParser:
    def test_sslscan_parser_parse_extended(self):
        """TLSv1.0 enabled → VulnerabilityFact with severity=medium."""
        parser = SslscanParser()
        sample = "TLSv1.0 enabled\n"
        creds, shares, access, vulns, paths = parser.parse_extended(
            "10.10.11.78", sample, "sslscan.txt", port=443
        )
        assert len(vulns) >= 1
        vuln = vulns[0]
        assert vuln.severity == "medium"
        assert vuln.vuln_id == "WEAK-TLS"
        assert vuln.host == "10.10.11.78"
        assert vuln.source_tool == "sslscan"

    def test_sslscan_dedup(self):
        """Same protocol appearing twice in output → only one VulnerabilityFact."""
        parser = SslscanParser()
        sample = "TLSv1.0 enabled\nTLSv1.0 enabled\n"
        _, _, _, vulns, _ = parser.parse_extended("10.10.11.78", sample, "sslscan.txt")
        # Dedup happens inside parse_extended via 'seen' set
        weak_tls = [v for v in vulns if v.vuln_id == "WEAK-TLS" and "TLSv1.0" in v.title]
        assert len(weak_tls) == 1


# ─────────────────────────────────────────────────────────────────────────────
# INmapXmlParser
# ─────────────────────────────────────────────────────────────────────────────


class TestNmapXmlParser:
    MINIMAL_NMAP_XML = textwrap.dedent("""\
        <?xml version="1.0"?>
        <nmaprun>
          <host>
            <address addr="10.10.11.78" addrtype="ipv4"/>
            <ports>
              <port protocol="tcp" portid="445">
                <state state="open"/>
                <service name="microsoft-ds" product="Windows Server 2019" version=""/>
              </port>
              <port protocol="tcp" portid="80">
                <state state="open"/>
                <service name="http" product="Apache httpd" version="2.4.41"/>
              </port>
              <port protocol="tcp" portid="23">
                <state state="closed"/>
                <service name="telnet"/>
              </port>
            </ports>
          </host>
        </nmaprun>
    """)

    def test_nmap_xml_parse(self, tmp_path):
        """Minimal nmap XML string → ServiceFact objects (only open ports)."""
        xml_file = tmp_path / "scan_test.nmap.xml"
        xml_file.write_text(self.MINIMAL_NMAP_XML)
        parser = INmapXmlParser()
        facts = parser.parse(xml_file)
        assert len(facts) == 2, f"Expected 2 open ports, got {len(facts)}: {facts}"
        ports = {f.port for f in facts}
        assert 445 in ports
        assert 80 in ports
        assert 23 not in ports
        svc_445 = next(f for f in facts if f.port == 445)
        assert svc_445.host == "10.10.11.78"
        assert svc_445.service == "microsoft-ds"
        assert svc_445.state == "open"

    def test_nmap_xml_parse_invalid(self, tmp_path):
        """Malformed XML → empty list (no crash)."""
        xml_file = tmp_path / "scan_bad.nmap.xml"
        xml_file.write_text("<broken xml>")
        parser = INmapXmlParser()
        facts = parser.parse(xml_file)
        assert facts == []


# ─────────────────────────────────────────────────────────────────────────────
# FactStore integration tests
# ─────────────────────────────────────────────────────────────────────────────


class TestFactStore:
    def test_factstore_dedup(self, tmp_path):
        """Injecting the same ServiceFact twice → only one entry stored."""
        cfg = _make_config(tmp_path)
        store = FactStore(cfg)

        sf = ServiceFact(
            host="10.10.11.78",
            port=445,
            protocol="tcp",
            service="microsoft-ds",
            product="",
            version="",
            state="open",
        )
        # Inject manually twice
        hf = store._host("10.10.11.78")
        hf.services.append(sf)
        hf.services.append(sf)
        store._dedup_services(hf)
        assert len(hf.services) == 1

    def test_context_for_command(self, tmp_path):
        """Add service + cred facts, context_for_command('enum') returns port and username."""
        cfg = _make_config(tmp_path)
        store = FactStore(cfg)
        ip = "10.10.11.78"
        hf = store._host(ip)
        # Add SMB service
        hf.services.append(
            ServiceFact(
                host=ip,
                port=445,
                protocol="tcp",
                service="microsoft-ds",
                product="",
                version="",
                state="open",
            )
        )
        # Add credential
        hf.credentials.append(
            CredentialFact(
                host=ip,
                username="Administrator",
                password="",
                source_file="rpcclient.txt",
            )
        )

        ctx = store.context_for_command(ip, "enum")

        assert ctx.get("port") == 445
        assert ctx.get("username") == "Administrator"
        assert ctx.get("host") == ip

    def test_context_for_unknown_host(self, tmp_path):
        """context_for_command on unknown host → empty dict."""
        cfg = _make_config(tmp_path)
        store = FactStore(cfg)
        ctx = store.context_for_command("1.2.3.4", "enum")
        assert ctx == {}

    def test_factstore_save_and_reload(self, tmp_path):
        """Save facts to JSON then reload them correctly."""
        cfg = _make_config(tmp_path)
        store = FactStore(cfg)
        ip = "10.10.11.10"
        hf = store._host(ip)
        hf.services.append(
            ServiceFact(
                host=ip,
                port=22,
                protocol="tcp",
                service="ssh",
                product="OpenSSH",
                version="8.2",
                state="open",
            )
        )
        store.save()

        # Reload into a new store
        store2 = FactStore(cfg)
        hf2 = store2.get_host(ip)
        assert hf2 is not None
        assert len(hf2.services) == 1
        assert hf2.services[0].port == 22
        assert hf2.services[0].service == "ssh"

    def test_ingest_xml(self, tmp_path):
        """ingest_xml with valid file → service facts stored per-host."""
        xml_content = textwrap.dedent("""\
            <?xml version="1.0"?>
            <nmaprun>
              <host>
                <address addr="10.0.0.1" addrtype="ipv4"/>
                <ports>
                  <port protocol="tcp" portid="22">
                    <state state="open"/>
                    <service name="ssh"/>
                  </port>
                </ports>
              </host>
            </nmaprun>
        """)
        cfg = _make_config(tmp_path)
        xml_file = cfg.sessions_dir / "scan_test.nmap.xml"
        xml_file.write_text(xml_content)
        store = FactStore(cfg)
        count = store.ingest_xml(xml_file)
        assert count == 1
        hf = store.get_host("10.0.0.1")
        assert hf is not None
        assert hf.services[0].port == 22

    def test_ingest_text_crackmapexec(self, tmp_path):
        """ingest_text with CME output → credential stored for guessed host IP."""
        cfg = _make_config(tmp_path)
        txt = cfg.sessions_dir / "10.10.11.78_crackmapexec.txt"
        txt.write_text(
            "SMB  10.10.11.78  445  DC01  [+] DOMAIN\\testuser:secret123\n"
        )
        store = FactStore(cfg)
        count = store.ingest_text(txt, host_hint="10.10.11.78")
        assert count >= 1
        hf = store.get_host("10.10.11.78")
        assert hf is not None
        usernames = [c.username for c in hf.credentials]
        assert "testuser" in usernames

    def test_dedup_creds(self, tmp_path):
        """Injecting same CredentialFact twice → only one stored after dedup."""
        cfg = _make_config(tmp_path)
        store = FactStore(cfg)
        ip = "10.10.11.78"
        hf = store._host(ip)
        cf = CredentialFact(
            host=ip, username="admin", password="pass", source_file="x.txt"
        )
        hf.credentials.append(cf)
        hf.credentials.append(cf)
        store._dedup_creds(hf)
        assert len(hf.credentials) == 1
