"""Target preflight for loops and auto_pwn: lab state and TCP reachability."""

from __future__ import annotations

import socket


def test_lab_state_maps_running_and_stopped():
    from modules import loop_preflight

    state = loop_preflight.lab_state_for(
        "172.17.0.9",
        scenarios=("metasploitable",),
        running=["lazyown-lab-metasploitable"],
        existing=["lazyown-lab-metasploitable"],
        ip_lookup=lambda name: "172.17.0.9",
    )
    assert state["scenario"] == "metasploitable"
    assert state["running"] is True

    state = loop_preflight.lab_state_for(
        "172.17.0.9",
        scenarios=("metasploitable",),
        running=[],
        existing=["lazyown-lab-metasploitable"],
        ip_lookup=lambda name: "172.17.0.9",
    )
    assert state["running"] is False

    assert loop_preflight.lab_state_for(
        "172.17.0.99",
        scenarios=("metasploitable",),
        running=[],
        existing=["lazyown-lab-metasploitable"],
        ip_lookup=lambda name: "172.17.0.9",
    ) == {}


def test_check_target_fails_fast_on_stopped_lab():
    from modules import loop_preflight

    outcome = loop_preflight.check_target(
        "172.17.0.9",
        lab={"scenario": "metasploitable", "container": "lazyown-lab-metasploitable", "ip": "172.17.0.9", "running": False},
    )
    assert outcome["ok"] is False
    assert "metasploitable" in outcome["reason"]
    assert outcome["hint"] == "lab start metasploitable"
    assert loop_preflight.recovery_hint(outcome) == "recover with: lab start metasploitable"


def test_check_target_passes_on_running_lab():
    from modules import loop_preflight

    outcome = loop_preflight.check_target(
        "172.17.0.9",
        lab={"scenario": "metasploitable", "container": "lazyown-lab-metasploitable", "ip": "172.17.0.9", "running": True},
    )
    assert outcome["ok"] is True
    assert "running" in outcome["reason"]


def test_check_target_probes_tcp(monkeypatch):
    from modules import loop_preflight

    monkeypatch.setattr(loop_preflight, "lab_state_for", lambda *a, **k: {})
    monkeypatch.setattr(
        loop_preflight, "probe_tcp_detailed", lambda target, ports=None, timeout=None: ([22, 80], 0)
    )
    outcome = loop_preflight.check_target("10.0.0.5")
    assert outcome["ok"] is True
    assert outcome["open_ports"] == [22, 80]

    monkeypatch.setattr(
        loop_preflight, "probe_tcp_detailed", lambda target, ports=None, timeout=None: ([], 0)
    )
    outcome = loop_preflight.check_target("10.0.0.5")
    assert outcome["ok"] is False
    assert "no TCP service" in outcome["reason"]


def test_check_target_refused_means_alive(monkeypatch):
    from modules import loop_preflight

    monkeypatch.setattr(loop_preflight, "lab_state_for", lambda *a, **k: {})
    monkeypatch.setattr(
        loop_preflight, "probe_tcp_detailed", lambda target, ports=None, timeout=None: ([], 17)
    )
    outcome = loop_preflight.check_target("10.0.0.5")
    assert outcome["ok"] is True
    assert "host alive" in outcome["reason"]


def test_check_target_without_target():
    from modules import loop_preflight

    outcome = loop_preflight.check_target("")
    assert outcome["ok"] is False
    assert "no target" in outcome["reason"]


def test_probe_tcp_real_socket():
    from modules import loop_preflight

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]

    def _accept():
        try:
            server.accept()
        except OSError:
            pass

    import threading as _threading

    worker = _threading.Thread(target=_accept, daemon=True)
    worker.start()
    try:
        open_ports = loop_preflight.probe_tcp("127.0.0.1", ports=[port], timeout=2.0)
        assert open_ports == [port]
    finally:
        server.close()
        worker.join(timeout=2)


def test_no_preflight_hint_override():
    from modules import loop_preflight

    outcome = loop_preflight.check_target("10.255.255.1", ports=[], connect_timeout=0.1)
    assert outcome["ok"] is False
    assert loop_preflight.recovery_hint(outcome).startswith("override with")


def test_preflight_flag_parses():
    from modules.lazy_runner import parse_loop_line

    config = parse_loop_line("--target 10.0.0.5 --no-preflight gain access")
    assert config.no_preflight is True
    assert parse_loop_line("--target 10.0.0.5 gain access").no_preflight is False
