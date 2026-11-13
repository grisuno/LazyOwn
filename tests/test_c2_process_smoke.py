"""Real-process smoke test: spawn lazyc2.py and drive it over HTTP.

Unlike the CSRF E2E suite (production primitives on a minimal Flask app),
this boots the actual monolith in a subprocess with an isolated working
directory and exercises the operator journey end to end:

    health probe -> login (form) -> session GET primes CSRF cookies ->
    tokenless POST rejected 403 -> echoed-token POST accepted.

Marked ``smoke`` so the default CI selection can opt in explicitly; it
needs the full runtime deps (same install as the test job) and ~10-20 s.
Run locally with:  pytest -m smoke tests/test_c2_process_smoke.py -v
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parent.parent
PORT_READY_TIMEOUT = 60.0
USER = "smokeop"
PASSWORD = "smoke-pass-12345"


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_port(port: int, proc: subprocess.Popen, timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"lazyc2.py exited early rc={proc.returncode}")
        with socket.socket() as sock:
            sock.settimeout(0.5)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.5)
    raise TimeoutError(f"C2 port {port} not ready in {timeout}s")


@pytest.fixture()
def c2_server(tmp_path):
    """Boot the real lazyc2.py against an isolated checkout copy."""
    workdir = tmp_path / "c2"
    workdir.mkdir()
    # The monolith resolves templates/static/modules relative to cwd and
    # its own file location; run the real file from the real checkout but
    # keep mutable state (sessions/, payload) inside tmp via env + copy.
    for name in ("templates", "static"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, workdir / name, dirs_exist_ok=True)
    payload = {}
    payload_src = ROOT / "payload.json"
    if payload_src.is_file():
        try:
            payload = json.loads(payload_src.read_text(encoding="utf-8"))
        except ValueError:
            payload = {}
    payload.update(
        {
            "api_key": payload.get("api_key") or "smoke-dummy-key",
            "lhost": "127.0.0.1",
            "c2_bind_address": "127.0.0.1",
            "c2_https_redirect": False,
            "c2_csrf_enabled": True,
            "rotate_keys_on_boot": False,
            "enable_c2_debug": False,
        }
    )
    (workdir / "payload.json").write_text(json.dumps(payload), encoding="utf-8")
    (workdir / "sessions").mkdir(exist_ok=True)

    port = _free_port()
    env = dict(os.environ)
    env.update(
        {
            "LAZYOWN_SESSIONS_DIR": str(workdir / "sessions"),
            "LAZYOWN_PAYLOAD_PATH": str(workdir / "payload.json"),
            "PYTHONUNBUFFERED": "1",
            "NOBANNER": "1",
        }
    )
    log = open(workdir / "server.log", "w+", encoding="utf-8")
    proc = subprocess.Popen(
        [sys.executable, "-W", "ignore", str(ROOT / "lazyc2.py"), str(port), USER, PASSWORD],
        cwd=str(workdir),
        env=env,
        stdout=log,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        _wait_port(port, proc, PORT_READY_TIMEOUT)
        yield base, workdir
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
        log.flush()
        log.seek(0)
        tail = log.read()[-4000:]
        log.close()
        if proc.returncode not in (0, -15, None):
            # Surface the server tail in the pytest report on failure.
            print(f"[c2 server log tail]\n{tail}")


@pytest.mark.smoke
class TestRealC2Process:
    def test_health_remote_shape(self, c2_server) -> None:
        base, _ = c2_server
        resp = requests.get(f"{base}/health", timeout=10)
        assert resp.status_code in (200, 503)
        body = resp.json()
        assert body["status"] in ("healthy", "unhealthy")
        # Loopback caller: detailed view must include checks, never a 500.
        assert "checks" in body

    def test_login_then_csrf_command_flow(self, c2_server) -> None:
        base, _ = c2_server
        sess = requests.Session()

        login = sess.post(
            f"{base}/login",
            data={"username": USER, "password": PASSWORD},
            timeout=15,
            allow_redirects=True,
        )
        assert login.status_code == 200, "login flow did not complete"

        # First authenticated page primes the CSRF cookies.
        page = sess.get(f"{base}/", timeout=15)
        assert page.status_code == 200
        token = sess.cookies.get("LAZY_CSRF_TOKEN")
        assert token, "authenticated GET did not deliver LAZY_CSRF_TOKEN"

        rejected = sess.post(
            f"{base}/issue_command",
            data={"client_id": "smoke", "command": "help"},
            timeout=15,
        )
        assert rejected.status_code == 403, "tokenless POST must be rejected"

        accepted = sess.post(
            f"{base}/issue_command",
            data={"client_id": "smoke", "command": "help"},
            headers={"X-XSRF-TOKEN": token},
            timeout=15,
            allow_redirects=False,
        )
        assert accepted.status_code in (200, 302), (
            f"echoed-token POST failed: {accepted.status_code} {accepted.text[:200]}"
        )

    def test_cli_basic_channel_without_token(self, c2_server) -> None:
        base, _ = c2_server
        resp = requests.post(
            f"{base}/issue_command",
            data={"client_id": "smoke", "command": "help"},
            auth=(USER, PASSWORD),
            timeout=15,
            allow_redirects=False,
        )
        assert resp.status_code in (200, 302), "valid Basic channel must bypass CSRF"
