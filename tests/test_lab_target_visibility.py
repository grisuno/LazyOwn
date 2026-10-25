"""Lab target visibility: start/status always show the container IP.

BDD scenarios. Given a running lab, When the operator starts or inspects
it, Then the container IP and the assign command are visible.
"""

from __future__ import annotations

from types import SimpleNamespace

from cli.commands.lab import LabCommandSet


def test_start_on_running_lab_reports_ip(capsys, monkeypatch):
    """Given a running Metasploitable lab, When started again, Then its IP is printed."""
    command = LabCommandSet()
    monkeypatch.setattr(command, "_docker_available", lambda: True)
    monkeypatch.setattr(command, "_running_containers", lambda: ["lazyown-lab-metasploitable"])
    monkeypatch.setattr(command, "_container_ip", lambda name: "172.17.0.2")
    monkeypatch.setattr(command, "_lab_ensure_web", lambda scenario, name: None)
    command._lab_start("metasploitable")
    output = capsys.readouterr().out
    assert "172.17.0.2" in output
    assert "assign rhost 172.17.0.2" in output


def test_status_reports_ip(capsys, monkeypatch):
    """Given a running lab, When status runs, Then the IP and assign line are visible."""
    command = LabCommandSet()
    monkeypatch.setattr(command, "_docker_available", lambda: True)
    monkeypatch.setattr(command, "_running_containers", lambda: ["lazyown-lab-metasploitable"])
    monkeypatch.setattr(command, "_container_ip", lambda name: "172.17.0.2")
    monkeypatch.setattr(
        "cli.commands.lab.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="running\n", stderr=""),
    )
    command._lab_status()
    output = capsys.readouterr().out
    assert "ip: 172.17.0.2" in output
    assert "assign rhost 172.17.0.2" in output
