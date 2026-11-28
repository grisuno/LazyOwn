"""Characterization tests for the wired orphan features.

Pins the behavior of the commands that reach previously-unreachable
modules: ``reflective_dll`` (PE analysis), ``adcs_request`` (ESC1/ESC8
certificate abuse), the ``kerberos_ticket sapphire`` S4U2self forging
branch and ``kerberos_build`` (raw protocol message construction).
"""

from __future__ import annotations

import cmd2
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _bound(command_set_cls, params: dict | None = None):
    """Return (command_set, shell_mock) with the set registered on a cmd2 shell."""
    shell = cmd2.Cmd(allow_cli_args=False)
    shell.params = params or {"rhost": "10.10.10.1", "domain": "corp.local"}
    shell.perror = MagicMock()
    shell.poutput = MagicMock()
    cmdset = command_set_cls()
    shell.register_command_set(cmdset)
    return cmdset, shell


def test_reflective_dll_writes_stubs(tmp_path, monkeypatch):
    import modules.reflective_dll as reflective_mod
    from cli.commands.payload_arsenal import PayloadArsenalCommandSet

    cmdset, shell = _bound(PayloadArsenalCommandSet)
    monkeypatch.chdir(tmp_path)
    pe = tmp_path / "implant.dll"
    pe.write_bytes(b"MZ" + b"\x00" * 64)

    fake_plan = {
        "technique": "createremotethread",
        "target_pid": 0,
        "entry_rva": 0x1000,
        "image_base": 0x400000,
        "required_imports": ["kernel32.dll"],
        "steps": ["OpenProcess"],
    }
    fake_loader = MagicMock()
    fake_loader.sha256 = "cafe" * 16
    fake_loader.architecture = "x64"
    fake_loader.required_imports = ["kernel32.dll"]
    fake_loader.plan_injection.return_value = fake_plan
    fake_loader.generate_c_stub.return_value = "// stub"
    fake_loader.generate_powershell_stub.return_value = "# stub"

    with patch.object(reflective_mod, "ReflectiveLoader", MagicMock(return_value=fake_loader)):
        cmdset.do_reflective_dll(str(pe))

    assert (tmp_path / "sessions" / "reflective_implant_loader.c").read_text() == "// stub"
    assert (tmp_path / "sessions" / "reflective_implant_loader.ps1").read_text() == "# stub"
    shell.perror.assert_not_called()


def test_reflective_dll_missing_file_errors():
    from cli.commands.payload_arsenal import PayloadArsenalCommandSet

    cmdset, shell = _bound(PayloadArsenalCommandSet)
    cmdset.do_reflective_dll("/nonexistent/implant.dll")
    shell.perror.assert_called_once()


def test_adcs_request_esc1_builds_kwargs(tmp_path, monkeypatch):
    import modules.adcs_attacks as adcs_mod
    from cli.commands.active_directory import ActiveDirectoryCommandSet

    cmdset, shell = _bound(ActiveDirectoryCommandSet)
    monkeypatch.chdir(tmp_path)

    captured = {}

    def fake_esc1(self, **kwargs):
        captured.update(kwargs)
        return True

    with patch.object(adcs_mod.ADCSCertipyWrapper, "request_certificate_esc1", fake_esc1):
        cmdset.do_adcs_request(
            "esc1 --user svc_sql --pass 'P@ss' --domain corp.local --dc 10.10.10.10 "
            "--ca CORP-CA --template VulnTemplate --target-user Administrator"
        )

    assert captured["username"] == "svc_sql"
    assert captured["domain"] == "corp.local"
    assert captured["dc_ip"] == "10.10.10.10"
    assert captured["ca_name"] == "CORP-CA"
    assert captured["template_name"] == "VulnTemplate"
    assert captured["target_user"] == "Administrator"
    assert captured["output_file"] == "sessions/Administrator_esc1.pfx"
    shell.poutput.assert_called()


def test_adcs_request_rejects_missing_ca():
    from cli.commands.active_directory import ActiveDirectoryCommandSet

    cmdset, shell = _bound(ActiveDirectoryCommandSet)
    cmdset.do_adcs_request("esc1 --user svc_sql --pass x --domain corp.local --dc 10.10.10.10")
    shell.perror.assert_called_once()


def test_adcs_request_rejects_bad_dc():
    from cli.commands.active_directory import ActiveDirectoryCommandSet

    cmdset, shell = _bound(ActiveDirectoryCommandSet)
    cmdset.do_adcs_request("esc8 --user u --pass p --domain d --dc 'bad;host'")
    shell.perror.assert_called_once()


def test_kerberos_ticket_sapphire_forges_and_saves(tmp_path, monkeypatch):
    import modules.kerberos_tickets as kt_mod
    from cli.commands.active_directory import ActiveDirectoryCommandSet

    cmdset, shell = _bound(ActiveDirectoryCommandSet)
    monkeypatch.chdir(tmp_path)
    tgt_file = tmp_path / "tgt.kirbi"
    tgt_file.write_bytes(b"TGTDATA")

    def fake_forge(self, **kwargs):
        assert kwargs["tgt"] == b"TGTDATA"
        assert kwargs["session_key"] == b"\xaa\xbb"
        assert kwargs["target_service"] == "cifs/DC01.corp.local"
        return {
            "ticket_type": "sapphire_s4u2self",
            "domain": "CORP.LOCAL",
            "target_user": "Administrator",
            "target_service": "cifs/DC01.corp.local",
            "request": MagicMock(),
            "padata": [{"padata_type": 129, "padata_value": b"x"}],
            "req_body": {"realm": "CORP.LOCAL"},
        }

    with patch.object(kt_mod.SapphireTicketForger, "forge_s4u2self", fake_forge):
        cmdset.do_kerberos_ticket(
            f"sapphire --tgt {tgt_file} --key aabb --spn cifs/DC01.corp.local --domain corp.local"
        )

    artifact = tmp_path / "sessions" / "sapphire_s4u2self_CORP.LOCAL.json"
    data = json.loads(artifact.read_text())
    assert data["ticket_type"] == "sapphire_s4u2self"
    assert data["target_service"] == "cifs/DC01.corp.local"


def test_kerberos_build_asreq_derives_key(tmp_path, monkeypatch):
    from cli.commands.active_directory import ActiveDirectoryCommandSet

    cmdset, shell = _bound(ActiveDirectoryCommandSet)
    monkeypatch.chdir(tmp_path)

    cmdset.do_kerberos_build("asreq --user svc_sql --domain corp.local --pass 'P@ss'")

    artifact = tmp_path / "sessions" / "as_req_svc_sql.json"
    data = json.loads(artifact.read_text())
    assert data["pvno"] == 5
    assert data["msg_type"] == 10
    assert data["req_body"]["cname"] == "svc_sql"
    assert data["req_body"]["realm"] == "CORP.LOCAL"
    assert len(data["key"]) > 0
