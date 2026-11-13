"""auto_pwn success contract: precise evidence, never recon noise."""

from __future__ import annotations

import pytest

RECON_OUTPUT = (
    "HTTP/1.1 200 OK\n"
    "Server: Apache/2.2.8 (Ubuntu) DAV/2\n"
    "X-Powered-By: PHP/5.2.4-2ubuntu5.10\n"
    "Content-Type: text/html\n\n"
    + "<html><body><h1>Welcome</h1><p>" + "x" * 500 + "</p></body></html>"
)


@pytest.fixture()
def engine():
    from modules.autonomous_exploit_engine import AutonomousExploitEngine

    return object.__new__(AutonomousExploitEngine)


def test_evaluate_exploit_output_root_shell():
    from modules.ctf_capture import evaluate_exploit_output

    outcome = evaluate_exploit_output("uid=0(root) gid=0(root) groups=0(root)")
    assert outcome["shell_objective"] is True
    assert "root_shell" in outcome["matched"]


def test_evaluate_exploit_output_credentials_header_not_cred():
    from modules.ctf_capture import evaluate_exploit_output

    assert evaluate_exploit_output("[*] msfadmin:msfadmin")["shell_objective"] is False


def test_evaluate_exploit_output_shadow_dump():
    from modules.ctf_capture import evaluate_exploit_output

    outcome = evaluate_exploit_output("root:$1$abcdef$0123456789:17401:0:99999:7:::")
    assert outcome["shell_objective"] is True
    assert "shadow_dump" in outcome["matched"]


def test_evaluate_exploit_output_recon_is_not_success():
    from modules.ctf_capture import evaluate_exploit_output

    outcome = evaluate_exploit_output(RECON_OUTPUT)
    assert outcome["shell_objective"] is False
    assert outcome["matched"] == {}


def test_check_success_recon_banner_is_failure(engine):
    assert engine._check_success(RECON_OUTPUT, None) is False


def test_check_success_long_recon_is_failure(engine):
    long_recon = "Starting Nmap 7.99\n" + ("port 80 open service http\n" * 40)
    assert len(long_recon) > 200
    assert engine._check_success(long_recon, None) is False


def test_check_success_shell_evidence(engine):
    assert engine._check_success("uid=0(root) gid=0(root) groups=0(root)", None) is True
    assert engine._check_success("www-data@metasploitable:/var/www$ ", None) is True


def test_check_success_meterpreter_banner(engine):
    assert engine._check_success("Meterpreter session 1 opened (10.0.0.1:4444)", None) is True


def test_check_success_shadow_dump(engine):
    assert engine._check_success("root:$1$abcdef$0123456789:17401:0:99999:7:::", None) is True


def test_check_success_empty_output(engine):
    assert engine._check_success("", None) is False


def test_steps_for_initial_access_resolves_auto_pwn():
    from modules.auto_registry import steps_for

    steps = steps_for("gain initial access on 172.17.0.2", "172.17.0.2")
    assert steps == ["auto_pwn 172.17.0.2"]
