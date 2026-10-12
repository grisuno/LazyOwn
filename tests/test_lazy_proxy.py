"""Recorder proxy: CA, HTTP/HTTPS capture, engine ingestion, auto-binding."""

from __future__ import annotations

import http.client
import socket
import ssl
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from modules.lazy_proxy import ProxyController, env_for_ca


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


class _EchoHandler(BaseHTTPRequestHandler):
    """Minimal upstream returning a JSON body."""

    def do_GET(self):  # noqa: N802 - stdlib naming
        body = b'{"ok": true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # noqa: ANN002, ANN003
        return None


def _start_upstream(tls_context: ssl.SSLContext | None = None) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _EchoHandler)
    if tls_context is not None:
        server.socket = tls_context.wrap_socket(server.socket, server_side=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _read_until(sock: socket.socket, marker: bytes, limit: int = 65536) -> bytes:
    data = b""
    while marker not in data and len(data) < limit:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def test_ca_and_leaf_verify(tmp_path):
    """BDD: generated leaves chain to the CA and cover the host name."""
    from cryptography import x509

    from modules.lazy_proxy import CertificateAuthority

    authority = CertificateAuthority(tmp_path / "pki")
    context = authority.context_for("example.test")
    assert context is not None
    assert authority.context_for("example.test") is context
    leaf = x509.load_pem_x509_certificate(
        (authority.leaf_dir / "example.test.pem").read_bytes())
    assert leaf.issuer == authority._ca_cert.subject
    san = leaf.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
    assert "example.test" in san.get_values_for_type(x509.DNSName)
    assert authority.cert_path.exists()


def test_http_capture_records_exchange(tmp_path):
    """BDD: a proxied HTTP GET lands in the recorder with bodies."""
    upstream = _start_upstream()
    up_port = upstream.server_address[1]
    controller = ProxyController()
    status = controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        conn = http.client.HTTPConnection("127.0.0.1", status["port"], timeout=5)
        conn.request("GET", f"http://127.0.0.1:{up_port}/spec")
        response = conn.getresponse()
        body = response.read()
        conn.close()
        assert response.status == 200
        assert b'"ok": true' in body
        rows = controller.recorder().query(host="127.0.0.1")
        match = [row for row in rows if row["url"].endswith("/spec")]
        assert match
        stored = controller.recorder().get_body(match[0]["id"])
        assert "ok" in stored["resp_body"]
        assert stored["req_headers"]["Host"].startswith("127.0.0.1")
    finally:
        controller.stop()
        upstream.shutdown()


def test_https_mitm_capture(tmp_path):
    """BDD: CONNECT tunnels are terminated and recorded end to end."""
    from modules.lazy_proxy import CertificateAuthority

    upstream_authority = CertificateAuthority(tmp_path / "upstream_pki")
    upstream_ctx = upstream_authority.context_for("localhost")
    upstream = _start_upstream(upstream_ctx)
    up_port = upstream.server_address[1]
    controller = ProxyController()
    status = controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        client_ctx = ssl.create_default_context(cafile=controller.ca_path())
        raw = socket.create_connection(("127.0.0.1", status["port"]), timeout=5)
        raw.sendall(
            f"CONNECT localhost:{up_port} HTTP/1.1\r\n"
            f"Host: localhost:{up_port}\r\n\r\n".encode())
        assert b"200" in _read_until(raw, b"\r\n\r\n")
        tls = client_ctx.wrap_socket(raw, server_hostname="localhost")
        tls.sendall(b"GET /secure HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
        response = _read_until(tls, b'"ok": true')
        tls.close()
        assert b"200" in response.split(b"\r\n", 1)[0]
        rows = controller.recorder().query(host="localhost")
        assert rows
        stored = controller.recorder().get_body(rows[0]["id"])
        assert stored["scheme"] == "https"
        assert "ok" in stored["resp_body"]
    finally:
        controller.stop()
        upstream.shutdown()


def test_env_for_ca_exports_trust(tmp_path):
    """BDD: the trust environment covers curl, requests and node."""
    env = env_for_ca(str(tmp_path / "ca.pem"), "127.0.0.1", 8899)
    assert env["HTTP_PROXY"] == "http://127.0.0.1:8899"
    assert env["HTTPS_PROXY"] == env["HTTP_PROXY"]
    assert env["REQUESTS_CA_BUNDLE"].endswith("ca.pem")
    assert env["SSL_CERT_FILE"] == env["REQUESTS_CA_BUNDLE"]
    assert env["NODE_EXTRA_CA_CERTS"] == env["REQUESTS_CA_BUNDLE"]


def test_engine_ingests_recorder_rows(tmp_path, monkeypatch):
    """BDD: round ingestion mirrors recorder rows into the task log."""
    import modules.lazy_loop as loop
    import modules.lazy_proxy as proxy_module

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    controller = ProxyController()
    monkeypatch.setattr(proxy_module, "_CONTROLLER", controller)
    controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        controller.recorder().record("GET", "http://10.0.0.9/admin", 200,
                                     b"", b"panel", "text/html",
                                     {"Host": "10.0.0.9"}, {"Content-Type": "text/html"},
                                     host="10.0.0.9", port=80, scheme="http",
                                     task=task_id)
        assert engine.ingest_proxy_traffic(task_id) == 1
        assert engine.ingest_proxy_traffic(task_id) == 0
        traffic = loop.TrafficLog(task_id)
        rows = traffic.search("10.0.0.9")
        assert rows
        assert rows[0]["meta"]["exchange_id"]
        body = traffic.recorder_body(rows[0]["digest"])
        assert body["resp_body"] == "panel"
    finally:
        controller.stop()


def test_writeback_auto_binds_recent_traffic(tmp_path, monkeypatch):
    """BDD: a fresh finding carries the latest exchanges as evidence."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    traffic = loop.TrafficLog(task_id)
    traffic.record("http", "GET http://127.0.0.1/admin", "HTTP 200")
    intent = graph.add_node("intent", "probe admin panel")
    worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                         loop.ActivityLog(task_id), traffic,
                         loop.Guard(task_id), engine.store)
    wrote = worker._writeback(intent, [("curl http://127.0.0.1/admin",
                                        "vulnerable cve-2021-1234 panel")])
    assert wrote["findings"] == 1
    finding = graph.list("finding")[-1]
    refs = traffic.evidence(finding.node_id, graph)
    assert refs
    assert refs[0]["note"] == "auto-bound"


def test_proxy_status_and_stop(tmp_path):
    """BDD: status reports the CA and exchanges; stop is idempotent."""
    controller = ProxyController()
    assert controller.status()["running"] is False
    status = controller.start(port=0, traffic_dir=tmp_path / "traffic")
    assert status["running"] is True
    assert status["port"] > 0
    assert status["ca_path"].endswith("ca.pem")
    stopped = controller.stop()
    assert stopped["running"] is False
    assert controller.stop()["running"] is False


def test_status_declares_https_mitm(tmp_path):
    """BDD: status states HTTP and HTTPS capture via MITM."""
    controller = ProxyController()
    status = controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        assert status["mitm"] is True
        assert "http" in status["captures"]
        assert "https" in status["captures"]
    finally:
        controller.stop()


def test_install_ca_trust_prompts_only_when_needed(tmp_path, monkeypatch):
    """BDD: the anchor is written once; later starts skip sudo entirely."""
    import types

    import modules.lazy_proxy as proxy_module

    anchors = tmp_path / "anchors"
    anchors.mkdir()
    monkeypatch.setattr(proxy_module, "TRUST_TARGETS", ((str(anchors), ()),))
    ca_path = tmp_path / "ca.pem"
    ca_path.write_bytes(b"-----BEGIN CERTIFICATE-----\nfake\n-----END CERTIFICATE-----\n")
    calls: list[list[str]] = []

    def runner(argv):
        calls.append(list(argv))
        Path(argv[-1]).write_bytes(Path(argv[-2]).read_bytes())
        return types.SimpleNamespace(returncode=0)

    first = proxy_module.install_ca_trust(ca_path, runner=runner)
    assert first["installed"] is True, first
    assert first["reason"] == "installed"
    assert len(calls) == 1
    assert proxy_module.ca_trusted(ca_path) is True
    second = proxy_module.install_ca_trust(ca_path, runner=runner)
    assert second["installed"] is True
    assert second["reason"] == "already trusted"
    assert len(calls) == 1
    missing = proxy_module.install_ca_trust(tmp_path / "nope.pem", runner=runner)
    assert missing["installed"] is False


def test_recorder_body_search_and_archive_roundtrip(tmp_path):
    """BDD: FTS body search and archive export/import preserve traffic."""
    from modules.traffic_recorder import TrafficRecorder

    recorder = TrafficRecorder(tmp_path / "traffic")
    recorder.record("GET", "http://t.example/admin", 200,
                    b"", b"welcome to the admin panel", "text/html")
    recorder.record("POST", "http://t.example/login", 302,
                    b"user=admin&pass=hunter2", b"redirect")
    hits = recorder.search_body("hunter2")
    assert len(hits) == 1
    assert hits[0]["url"] == "http://t.example/login"
    assert recorder.search_body("no-such-marker") == []
    archive_path = tmp_path / "export.zip"
    exported = recorder.export_archive(archive_path)
    assert exported["exported"] == 2
    assert exported["bodies"] == 2
    restored = TrafficRecorder(tmp_path / "restored")
    imported = restored.import_archive(archive_path)
    assert imported["imported"] == 2
    assert restored.count() == 2
    assert restored.search_body("admin panel")
    row = restored.query(host="t.example")[0]
    body = restored.get_body(row["id"])
    assert body["resp_headers"] == {}
    assert "admin" in (body["req_body"] + body["resp_body"])


def test_recorder_gc_removes_old_exchanges(tmp_path, monkeypatch):
    """BDD: gc removes exchanges older than the cut-off and keeps fresh ones."""
    import modules.traffic_recorder as recorder_module
    from modules.traffic_recorder import TrafficRecorder

    clock = {"now": 1_000_000.0}
    monkeypatch.setattr(recorder_module.time, "time", lambda: clock["now"])
    recorder = TrafficRecorder(tmp_path / "traffic")
    recorder.record("GET", "http://old.example/a", 200, b"", b"old")
    clock["now"] = 1_000_000.0 + 86400 * 40
    recorder.record("GET", "http://new.example/b", 200, b"", b"new")
    result = recorder.gc(older_than_sec=86400 * 30)
    assert result["removed"] == 1
    assert recorder.count() == 1
    assert recorder.query(host="new.example")
    assert recorder.gc(older_than_sec=0)["removed"] == 0


def test_task_scoped_query_and_export(tmp_path):
    """BDD: per-task archives only carry that task's exchanges."""
    from modules.traffic_recorder import TrafficRecorder

    recorder = TrafficRecorder(tmp_path / "traffic")
    recorder.record("GET", "http://a.example/1", 200, task="t1")
    recorder.record("GET", "http://b.example/2", 200, task="t2")
    assert len(recorder.query(task="t1")) == 1
    archive = tmp_path / "t1.zip"
    result = recorder.export_archive(archive, task="t1")
    assert result["exported"] == 1
    restored = TrafficRecorder(tmp_path / "restored")
    restored.import_archive(archive)
    assert len(restored.query(task="t1")) == 1
    assert restored.query(task="t2") == []


def test_engine_exports_task_traffic_and_gc_runs_once(tmp_path, monkeypatch):
    """BDD: terminal task export plus interval-gated retention sweep."""
    import modules.lazy_proxy as proxy_module

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    controller = ProxyController()
    monkeypatch.setattr(proxy_module, "_CONTROLLER", controller)
    controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        recorder = controller.recorder()
        recorder.record("GET", "http://t.example/x", 200, b"", b"body", task=task_id)
        recorder.record("GET", "http://old.example/y", 200, b"", b"old", task="t9998")
        with recorder._connect() as conn:
            conn.execute("UPDATE exchanges SET ts = ts - 86400 * 40 WHERE task = 't9998'")
        exported = engine.export_task_traffic(task_id)
        assert exported["exported"] == 1
        assert Path(exported["path"]).exists()
        assert engine.export_task_traffic("t9999")["exported"] == 0
        engine.proxy_gc_days = 30
        engine.proxy_gc_interval_sec = 10 ** 9
        assert engine._maybe_proxy_gc() == 1
        assert engine._maybe_proxy_gc() == 0
    finally:
        controller.stop()


def test_recorder_inbox_auto_import(tmp_path, monkeypatch):
    """BDD: run_round imports inbox archives once and moves them aside."""
    import modules.lazy_proxy as proxy_module
    from modules.traffic_recorder import TrafficRecorder

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    controller = ProxyController()
    monkeypatch.setattr(proxy_module, "_CONTROLLER", controller)
    controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        source = TrafficRecorder(tmp_path / "source")
        source.record("GET", "http://inbox.example/a", 200, b"", b"inbox body",
                      task="t9990")
        archive = tmp_path / "export.zip"
        source.export_archive(archive)
        inbox = tmp_path / "traffic" / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        archive.replace(inbox / "export.zip")
        engine.run_round(task_id, workers=1, executor=lambda command: "ok\n")
        assert controller.recorder().query(host="inbox.example")
        assert (inbox / "imported" / "export.zip").exists()
        assert engine._maybe_import_inbox() == 0
    finally:
        controller.stop()


def test_install_ca_nss_with_fake_profiles(tmp_path, monkeypatch):
    """BDD: NSS install runs certutil per profile and skips trusted ones."""
    import types

    import modules.lazy_proxy as proxy_module

    ca_path = tmp_path / "ca.pem"
    ca_path.write_bytes(b"-----BEGIN CERTIFICATE-----\nNSS\n-----END CERTIFICATE-----\n")
    monkeypatch.setattr(
        proxy_module.shutil, "which",
        lambda name: "/usr/bin/certutil" if name == "certutil" else None)
    profiles = [str(tmp_path / "p1"), str(tmp_path / "p2")]
    for profile in profiles:
        Path(profile).mkdir()
    commands: list[list[str]] = []

    def runner(argv):
        commands.append(list(argv))
        joined = " ".join(argv)
        if "-L" in argv:
            return types.SimpleNamespace(returncode=0 if profiles[0] in joined else 1)
        return types.SimpleNamespace(returncode=0)

    result = proxy_module.install_ca_nss(ca_path, runner=runner, profiles=profiles)
    assert result["profiles"] == 2
    assert result["installed"] == 2
    add_calls = [call for call in commands if "-A" in call]
    assert len(add_calls) == 1
    assert f"sql:{profiles[1]}" in " ".join(add_calls[0])
    assert proxy_module.NSS_NICKNAME in add_calls[0]
    missing = proxy_module.install_ca_nss(tmp_path / "nope.pem", runner=runner)
    assert missing["installed"] == 0
    empty = proxy_module.install_ca_nss(ca_path, runner=runner, profiles=[])
    assert empty["reason"] == "no NSS profiles"
    monkeypatch.setattr(proxy_module.shutil, "which", lambda name: None)
    no_certutil = proxy_module.install_ca_nss(ca_path, runner=runner,
                                              profiles=profiles)
    assert no_certutil["reason"] == "certutil not installed"


def test_body_ranged_reads(tmp_path):
    """BDD: blob-style ranged reads page through stored bodies."""
    from modules.traffic_recorder import TrafficRecorder

    recorder = TrafficRecorder(tmp_path / "traffic")
    recorder.record("GET", "http://t.example/big", 200,
                    b"", b"0123456789abcdef", "text/plain")
    row = recorder.query(host="t.example")[0]
    first = recorder.read_body(row["id"], part="resp", offset=0, length=6)
    assert first["data"] == "012345"
    assert first["total"] == 16
    assert first["eof"] is False
    tail = recorder.read_body(row["id"], part="resp", offset=6, length=100)
    assert tail["data"] == "6789abcdef"
    assert tail["eof"] is True
    try:
        recorder.read_body(row["id"], part="nope")
    except ValueError:
        pass
    else:
        raise AssertionError("bad part must raise")


def test_upstream_chaining_captures_in_both(tmp_path):
    """BDD: a chained proxy forwards through the upstream and both record."""
    upstream = _start_upstream()
    up_port = upstream.server_address[1]
    chained_upstream = ProxyController()
    upstream_status = chained_upstream.start(port=0, traffic_dir=tmp_path / "a")
    front = ProxyController()
    front_status = front.start(port=0, traffic_dir=tmp_path / "b",
                               upstream=f"127.0.0.1:{upstream_status['port']}")
    try:
        conn = http.client.HTTPConnection("127.0.0.1", front_status["port"], timeout=5)
        conn.request("GET", f"http://127.0.0.1:{up_port}/chained")
        response = conn.getresponse()
        assert response.status == 200
        assert b'"ok": true' in response.read()
        conn.close()
        assert front.recorder().query(host="127.0.0.1")
        assert chained_upstream.recorder().query(host="127.0.0.1")
        assert front_status["upstream"].endswith(str(upstream_status["port"]))
    finally:
        front.stop()
        chained_upstream.stop()
        upstream.shutdown()


def test_websocket_passthrough_recorded(tmp_path):
    """BDD: a WebSocket upgrade tunnels raw bytes and records the handshake."""
    import socket as socket_module

    listener = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
    listener.setsockopt(socket_module.SOL_SOCKET, socket_module.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    ws_port = listener.getsockname()[1]

    def _serve():
        conn, _ = listener.accept()
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(4096)
            if not chunk:
                return
            data += chunk
        conn.sendall(b"HTTP/1.1 101 Switching Protocols\r\n"
                     b"Upgrade: websocket\r\nConnection: Upgrade\r\n\r\n")
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            conn.sendall(chunk)
        conn.close()

    threading.Thread(target=_serve, daemon=True).start()
    controller = ProxyController()
    status = controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        raw = socket.create_connection(("127.0.0.1", status["port"]), timeout=5)
        raw.sendall(
            f"GET http://127.0.0.1:{ws_port}/ws HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{ws_port}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n\r\n".encode())
        assert b"101" in _read_until(raw, b"\r\n\r\n")
        raw.sendall(b"ping-echo")
        assert b"ping-echo" in _read_until(raw, b"ping-echo")
        raw.close()
        rows = controller.recorder().query(host="127.0.0.1")
        ws_rows = [row for row in rows if row["status"] == 101]
        assert ws_rows
        stored = controller.recorder().get_body(ws_rows[0]["id"])
        assert stored["note"] == "websocket tunnel"
    finally:
        controller.stop()
        listener.close()


def test_writeback_auto_binds_body_hits(tmp_path, monkeypatch):
    """BDD: finding evidence auto-binds proxy exchanges matching its text."""
    import modules.lazy_loop as loop
    import modules.lazy_proxy as proxy_module

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    controller = ProxyController()
    monkeypatch.setattr(proxy_module, "_CONTROLLER", controller)
    controller.start(port=0, traffic_dir=tmp_path / "traffic")
    try:
        controller.recorder().record("GET", "http://127.0.0.1/login", 200,
                                     b"", b"JWT token=swordfish-42", task=task_id)
        assert engine.ingest_proxy_traffic(task_id) == 1
        graph = loop.ExplorationGraph(task_id)
        traffic = loop.TrafficLog(task_id)
        intent = graph.add_node("intent", "probe admin panel")
        worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                             loop.ActivityLog(task_id), traffic,
                             loop.Guard(task_id), engine.store)
        wrote = worker._writeback(intent, [("probe panel",
                                            "vulnerable swordfish-42 exposed")])
        assert wrote["findings"] == 1
        finding = graph.list("finding")[-1]
        refs = traffic.evidence(finding.node_id, graph)
        assert any(str(ref.get("note", "")).startswith("body:") for ref in refs)
    finally:
        controller.stop()
