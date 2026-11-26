"""Contract tests for the C2 session-token gate (estorides parity)."""

from __future__ import annotations

import os
import tempfile
import time
import unittest
from unittest import mock

from flask import Flask, jsonify

from lazyc2.security.token_gate import (
    AUTH_ALT_HEADER,
    AUTH_COOKIE,
    TOKEN_TTL_SECONDS,
    SessionTokenGate,
    extract_token,
    install_token_gate,
)


class GateLifecycle(unittest.TestCase):
    """SessionTokenGate issue, check and expiry contract."""

    def test_rotate_mints_hex_token(self):
        gate = SessionTokenGate()
        first = gate.rotate()
        second = gate.rotate()
        self.assertEqual(len(first), 64)
        self.assertEqual(len(second), 64)
        self.assertNotEqual(first, second)
        self.assertTrue(gate.enabled)

    def test_check_constant_time_accepts_only_active(self):
        gate = SessionTokenGate()
        token = gate.rotate()
        self.assertTrue(gate.check(token))
        self.assertFalse(gate.check(token.upper()))
        self.assertFalse(gate.check("a" * 64))
        self.assertFalse(gate.check(None))
        self.assertFalse(gate.check(""))

    def test_expiry_after_ttl(self):
        gate = SessionTokenGate(ttl_seconds=1)
        token = gate.rotate()
        self.assertTrue(gate.check(token))
        with mock.patch("lazyc2.security.token_gate.time.monotonic", return_value=time.monotonic() + 2):
            self.assertTrue(gate.expired)
            self.assertFalse(gate.check(token))

    def test_expires_at_epoch_positive_window(self):
        gate = SessionTokenGate()
        gate.rotate()
        self.assertGreater(gate.expires_at_epoch(), time.time() + 60)

    def test_disabled_gate_never_authenticates(self):
        gate = SessionTokenGate()
        self.assertFalse(gate.enabled)
        self.assertFalse(gate.check("anything"))

    def test_cookie_kwargs_secure_and_ttl(self):
        gate = SessionTokenGate()
        kwargs = gate.issue_session_cookie_kwargs(secure=True)
        self.assertEqual(kwargs["max_age"], TOKEN_TTL_SECONDS)
        self.assertTrue(kwargs["httponly"])
        self.assertEqual(kwargs["samesite"], "Lax")
        self.assertTrue(kwargs["secure"])


class Extraction(unittest.TestCase):
    """Token extraction order over the Flask request context."""

    def setUp(self):
        self.app = Flask(__name__)

    def _extract(self, path="/probe"):
        with self.app.test_request_context(path):
            return extract_token()

    def test_bearer_header_wins(self):
        self.app.test_client()
        with self.app.test_request_context(
            "/probe", headers={"Authorization": "Bearer abc123", AUTH_ALT_HEADER: "alt999"}
        ):
            self.assertEqual(extract_token(), "abc123")

    def test_alt_header(self):
        with self.app.test_request_context("/probe", headers={AUTH_ALT_HEADER: "alt999"}):
            self.assertEqual(extract_token(), "alt999")

    def test_cookie(self):
        with self.app.test_request_context("/probe", headers={"Cookie": f"{AUTH_COOKIE}=ck1"}):
            self.assertEqual(extract_token(), "ck1")

    def test_query_param_get_only(self):
        self.assertEqual(self._extract("/probe?token=q1"), "q1")

    def test_query_param_rejected_on_post(self):
        self.assertEqual(self._extract("/probe?token=q1"), "q1")

    def test_missing_token_is_none(self):
        self.assertIsNone(self._extract("/probe"))


class InstalledGate(unittest.TestCase):
    """install_token_gate enforcement over a minimal Flask app."""

    def setUp(self):
        self.gate = SessionTokenGate()
        self.token = self.gate.rotate()
        self.app = Flask(__name__)
        self.app.config["TESTING"] = False

        @self.app.route("/api/data")
        def api_data():
            return jsonify({"ok": True})

        @self.app.route("/login")
        def login():
            return jsonify({"ok": "login"})

        install_token_gate(self.app, self.gate, lambda: request_path_exempt(self.app))

        def request_path_exempt(_app):
            from flask import request

            return request.path.startswith("/login")

    def _client(self):
        return self.app.test_client()

    def test_blocked_without_token(self):
        response = self._client().get("/api/data")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers.get("WWW-Authenticate"), 'Bearer realm="lazyown-c2"')

    def test_allowed_with_bearer(self):
        response = self._client().get("/api/data", headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)

    def test_allowed_with_alt_header(self):
        response = self._client().get("/api/data", headers={AUTH_ALT_HEADER: self.token})
        self.assertEqual(response.status_code, 200)

    def test_allowed_with_cookie(self):
        client = self._client()
        client.set_cookie(AUTH_COOKIE, self.token)
        response = client.get("/api/data")
        self.assertEqual(response.status_code, 200)

    def test_wrong_token_blocked(self):
        response = self._client().get("/api/data", headers={"Authorization": "Bearer wrong"})
        self.assertEqual(response.status_code, 401)

    def test_exempt_endpoint_open(self):
        response = self._client().get("/login")
        self.assertEqual(response.status_code, 200)

    def test_install_requires_enabled_gate(self):
        with self.assertRaises(ValueError):
            install_token_gate(Flask(__name__), SessionTokenGate(), lambda: False)


class McpTokenCache(unittest.TestCase):
    """MCP token cache file lifecycle."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._cwd = os.getcwd()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self._cwd)

    def test_store_and_load_roundtrip(self):
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills"))
        import lazyown_mcp

        lazyown_mcp._store_c2_token("tok123", time.time() + 600)
        self.assertEqual(lazyown_mcp._load_c2_token(), "tok123")
        path = lazyown_mcp._c2_token_path()
        self.assertEqual((os.stat(path).st_mode & 0o777), 0o600)

    def test_expired_token_ignored(self):
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills"))
        import lazyown_mcp

        lazyown_mcp._store_c2_token("old", time.time() - 10)
        self.assertEqual(lazyown_mcp._load_c2_token(), "")

    def test_env_token_wins(self):
        import sys

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills"))
        import lazyown_mcp

        lazyown_mcp._store_c2_token("cached", time.time() + 600)
        with mock.patch.dict(os.environ, {"LAZYOWN_C2_TOKEN": "from-env"}):
            self.assertEqual(lazyown_mcp._load_c2_token(), "from-env")


if __name__ == "__main__":
    unittest.main()
