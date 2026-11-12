"""Contract tests for the browser identity sync module."""

from __future__ import annotations

import json
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from modules import browser_sync


def _post(url: str, payload: dict, token_header: str = ""):
    body = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    if token_header:
        request.add_header(browser_sync.TOKEN_HEADER, token_header)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


SAMPLE_PROFILE = {
    "user_agent": "Mozilla/5.0 TestAgent",
    "languages": ["en-US", "es"],
    "client_hints": {"Sec-CH-UA-Platform": '"Linux"', "X-Evil": "1"},
    "cookies": [
        {"domain": ".example.com", "name": "session", "value": "abcdef", "path": "/", "secure": True},
        {"domain": "api.example.com", "name": "api_token", "value": "zzz", "hostOnly": True},
        {"domain": ".other.net", "name": "track", "value": "no"},
    ],
}


class BrowserSyncSpec(unittest.TestCase):
    """Receiver lifecycle, sync contract and injection contract."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name) / "sessions"
        self.addCleanup(self._tmp.cleanup)
        self._patches = [
            patch.object(browser_sync, "_SESSIONS_DIR", base),
            patch.object(browser_sync, "_PAYLOAD_PATH", Path(self._tmp.name) / "payload.json"),
        ]
        for item in self._patches:
            item.start()
            self.addCleanup(item.stop)
        self.addCleanup(browser_sync.clear_profile)
        self.addCleanup(browser_sync.get_receiver().stop)
        browser_sync._PAYLOAD_CACHE.clear()
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        browser_sync._RULES_CACHE.clear()

    def _payload(self, inject: bool = True) -> None:
        (Path(self._tmp.name) / "payload.json").write_text(json.dumps({"browser_sync_inject": inject}))

    def _write_profile(self, data: dict) -> None:
        path = browser_sync._profile_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))

    def test_token_stable_until_reset(self):
        first = browser_sync.token()
        self.assertEqual(first, browser_sync.token())
        self.assertNotEqual(first, browser_sync.reset_token())

    def test_receiver_start_ephemeral_and_status(self):
        status = browser_sync.start_receiver(port=0)
        self.assertTrue(status["running"])
        self.assertGreater(status["port"], 0)
        self.assertIn(browser_sync.ENDPOINT_PATH, status["endpoint"])
        self.assertEqual(status["endpoint"], browser_sync.start_receiver(port=0)["endpoint"])

    def test_receiver_stop(self):
        browser_sync.start_receiver(port=0)
        stopped = browser_sync.stop_receiver()
        self.assertFalse(stopped["running"])
        self.assertFalse(browser_sync.stop_receiver()["running"])

    def test_health_endpoint(self):
        status = browser_sync.start_receiver(port=0)
        with urllib.request.urlopen(status["endpoint"].replace(browser_sync.ENDPOINT_PATH, browser_sync.HEALTH_PATH), timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertTrue(json.loads(response.read())["ok"])

    def test_sync_roundtrip_writes_profile_and_jar(self):
        status = browser_sync.start_receiver(port=0)
        code, body = _post(status["endpoint"], SAMPLE_PROFILE, status["token"])
        self.assertEqual(code, 200)
        self.assertEqual(body["cookies"], 3)
        profile = json.loads(browser_sync._profile_path().read_text())
        self.assertEqual(len(profile["cookies"]), 3)
        self.assertEqual(profile["user_agent"], "Mozilla/5.0 TestAgent")
        self.assertNotIn("X-Evil", profile["client_hints"])
        jar = browser_sync._jar_path().read_text()
        self.assertIn("\tTRUE\t/\tTRUE\t0\tsession\tabcdef", jar)
        self.assertIn("other.net\tTRUE\t/\tFALSE\t0\ttrack\tno", jar)
        self.assertNotIn("other.net", jar.splitlines()[2])
        host_only_line = [line for line in jar.splitlines() if "api_token" in line]
        self.assertEqual(len(host_only_line), 1)
        self.assertIn("FALSE", host_only_line[0].split("\t")[1])

    def test_sync_requires_token(self):
        status = browser_sync.start_receiver(port=0)
        code, _ = _post(status["endpoint"], SAMPLE_PROFILE, "wrong-token")
        self.assertEqual(code, 401)
        code, _ = _post(status["endpoint"], SAMPLE_PROFILE, "")
        self.assertEqual(code, 401)
        self.assertFalse(browser_sync._profile_path().exists())

    def test_sync_rejects_bad_shapes(self):
        status = browser_sync.start_receiver(port=0)
        request = urllib.request.Request(status["endpoint"], data=b"not json", method="POST")
        request.add_header(browser_sync.TOKEN_HEADER, status["token"])
        try:
            urllib.request.urlopen(request, timeout=5)
            self.fail("expected 400")
        except urllib.error.HTTPError as exc:
            self.assertEqual(exc.code, 400)
        code, _ = _post(status["endpoint"], {"nope": 1}, status["token"])
        self.assertEqual(code, 400)

    def test_sync_rejects_oversized_body(self):
        status = browser_sync.start_receiver(port=0)
        payload = {"cookies": [{"domain": ".a.com", "name": "x", "value": "y" * browser_sync.MAX_SYNC_BODY}]}
        code, _ = _post(status["endpoint"], payload, status["token"])
        self.assertEqual(code, 413)

    def test_cookie_host_matching(self):
        cookies = SAMPLE_PROFILE["cookies"]
        self.assertTrue(browser_sync.cookie_matches_host(cookies[0], "example.com"))
        self.assertTrue(browser_sync.cookie_matches_host(cookies[0], "sub.example.com"))
        self.assertFalse(browser_sync.cookie_matches_host(cookies[1], "example.com"))
        self.assertTrue(browser_sync.cookie_matches_host(cookies[1], "api.example.com"))

    def test_cookie_path_matching(self):
        cookie = {"domain": ".example.com", "name": "admin", "path": "/admin"}
        self.assertTrue(browser_sync.cookie_matches_path(cookie, "/admin/x"))
        self.assertTrue(browser_sync.cookie_matches_path(cookie, "/admin"))
        self.assertFalse(browser_sync.cookie_matches_path(cookie, "/administration"))
        self.assertFalse(browser_sync.cookie_matches_path(cookie, "/public"))
        self.assertTrue(browser_sync.cookie_matches_path({"domain": ".x", "path": "/"}, "/anything"))

    def test_cookie_expiry_filtering(self):
        past = {"domain": ".example.com", "name": "dead", "expirationDate": time.time() - 60}
        future = {"domain": ".example.com", "name": "live", "expirationDate": time.time() + 3600}
        self.assertTrue(browser_sync.cookie_expired(past))
        self.assertFalse(browser_sync.cookie_expired(future))
        self.assertFalse(browser_sync.cookie_expired({"domain": ".example.com", "name": "session"}))
        self.assertFalse(browser_sync.cookie_expired({"domain": ".x", "expirationDate": "garbage"}))

    def test_secure_cookie_scheme_filtering(self):
        self._payload(inject=True)
        profile = dict(SAMPLE_PROFILE)
        profile["cookies"] = [
            {"domain": ".example.com", "name": "sec", "value": "v1", "secure": True},
            {"domain": ".example.com", "name": "plain", "value": "v2", "secure": False},
        ]
        self._write_profile(profile)
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        out_http, _ = browser_sync.apply_identity_headers(
            "example.com", {"Host": "example.com"}, b"", path="/", scheme="http"
        )
        self.assertNotIn("sec", out_http.get("Cookie", ""))
        self.assertIn("plain=v2", out_http["Cookie"])
        out_https, _ = browser_sync.apply_identity_headers(
            "example.com", {"Host": "example.com"}, b"", path="/", scheme="https"
        )
        self.assertIn("sec=v1", out_https["Cookie"])
        self.assertIn("plain=v2", out_https["Cookie"])

    def test_path_scoped_cookie_not_leaked(self):
        self._payload(inject=True)
        profile = dict(SAMPLE_PROFILE)
        profile["cookies"] = [
            {"domain": ".example.com", "name": "admin", "value": "secret", "path": "/admin"},
        ]
        self._write_profile(profile)
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        out_public, _ = browser_sync.apply_identity_headers(
            "example.com", {"Host": "example.com"}, b"", path="/public", scheme="https"
        )
        self.assertNotIn("Cookie", out_public)
        out_admin, _ = browser_sync.apply_identity_headers(
            "example.com", {"Host": "example.com"}, b"", path="/admin/users", scheme="https"
        )
        self.assertIn("admin=secret", out_admin["Cookie"])

    def test_rfc6265_cookie_ordering(self):
        cookies = [
            {"domain": ".example.com", "name": "root", "value": "r", "path": "/"},
            {"domain": ".example.com", "name": "deep", "value": "d", "path": "/admin/tools"},
            {"domain": "api.example.com", "name": "host", "value": "h", "path": "/admin/tools"},
        ]
        profile = dict(SAMPLE_PROFILE)
        profile["cookies"] = cookies
        self.assertEqual(
            [c["name"] for c in browser_sync.cookies_for_host(profile, "api.example.com", "/admin/tools/x")],
            ["host", "deep", "root"],
        )

    def test_expired_cookie_not_injected(self):
        self._payload(inject=True)
        profile = dict(SAMPLE_PROFILE)
        profile["cookies"] = [
            {"domain": ".example.com", "name": "dead", "value": "v", "expirationDate": time.time() - 1},
            {"domain": ".example.com", "name": "live", "value": "v", "expirationDate": time.time() + 60},
        ]
        self._write_profile(profile)
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        out, _ = browser_sync.apply_identity_headers("example.com", {"Host": "example.com"}, b"")
        self.assertEqual(out["Cookie"], "live=v")

    def test_empty_value_cookie_skipped_in_merge(self):
        cookies = [{"domain": ".example.com", "name": "empty", "value": ""}, SAMPLE_PROFILE["cookies"][0]]
        merged = browser_sync.build_cookie_header("existing=1", cookies)
        self.assertNotIn("empty", merged)
        self.assertIn("session=abcdef", merged)

    def test_cookie_header_merge(self):
        existing = "api_token=old; analytics=1"
        merged = browser_sync.build_cookie_header(existing, SAMPLE_PROFILE["cookies"])
        self.assertIn("api_token=zzz", merged)
        self.assertIn("analytics=1", merged)
        self.assertIn("session=abcdef", merged)

    def test_rules_applied(self):
        rules = [
            {"type": "header_replace", "match": "curl", "replace": "Firefox"},
            {"type": "header_add", "match": "Referer", "replace": "https://example.com/"},
            {"type": "header_set", "match": "X-A", "replace": "b"},
            {"type": "header_remove", "match": "X-Drop"},
            {"type": "body_replace", "match": "password=[^&]*", "replace": "password=x"},
            {"type": "header_replace", "match": "Host", "replace": "evil"},
            {"enabled": False, "type": "header_add", "match": "X-Off", "replace": "1"},
        ]
        browser_sync._rules_path().parent.mkdir(parents=True, exist_ok=True) or browser_sync._rules_path().write_text(json.dumps(rules))
        browser_sync._RULES_CACHE.clear()
        headers = {"User-Agent": "curl/8.0", "Host": "example.com", "X-Drop": "1"}
        body = b"user=me&password=hunter2"
        out_headers, out_body, applied = browser_sync.apply_rules(headers, body)
        self.assertEqual(out_headers["User-Agent"], "Firefox/8.0")
        self.assertEqual(out_headers["Referer"], "https://example.com/")
        self.assertEqual(out_headers["X-A"], "b")
        self.assertNotIn("X-Drop", out_headers)
        self.assertNotIn("X-Off", out_headers)
        self.assertEqual(out_headers["Host"], "example.com")
        self.assertEqual(out_body, b"user=me&password=x")
        self.assertGreater(applied, 0)

    def test_identity_injection_end_to_end(self):
        self._payload(inject=True)
        self._write_profile(SAMPLE_PROFILE)
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        headers = {"User-Agent": "curl/8.0", "Host": "example.com", "Accept-Encoding": "gzip"}
        out, body = browser_sync.apply_identity_headers("example.com", headers, b"")
        self.assertEqual(out["Cookie"], "session=abcdef")
        self.assertEqual(out["User-Agent"], "Mozilla/5.0 TestAgent")
        self.assertEqual(out["Accept-Language"], "en-US,es")
        self.assertEqual(out["Sec-CH-UA-Platform"], '"Linux"')
        self.assertNotIn("X-Evil", out)
        api_out, _ = browser_sync.apply_identity_headers("api.example.com", {"Host": "api.example.com"}, b"")
        self.assertIn("api_token=zzz", api_out["Cookie"])
        self.assertIn("session=abcdef", api_out["Cookie"])

    def test_identity_injection_disabled(self):
        self._payload(inject=False)
        self._write_profile(SAMPLE_PROFILE)
        browser_sync._PAYLOAD_CACHE.clear()
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        headers = {"User-Agent": "curl/8.0", "Cookie": "existing=1"}
        out, _ = browser_sync.apply_identity_headers("example.com", headers, b"")
        self.assertEqual(out["Cookie"], "existing=1")
        self.assertEqual(out["User-Agent"], "curl/8.0")

    def test_clear_profile(self):
        self._write_profile({})
        browser_sync._jar_path().write_text("")
        result = browser_sync.clear_profile()
        self.assertIn("profile.json", result["removed"])
        self.assertFalse(browser_sync._profile_path().exists())

    def test_receiver_status_reports_profile(self):
        self._write_profile(SAMPLE_PROFILE)
        status = browser_sync.start_receiver(port=0)
        self.assertEqual(status["cookies"], 3)
        self.assertIn("example.com", status["domains"])

    def test_apply_identity_to_url(self):
        self._payload(inject=True)
        self._write_profile(SAMPLE_PROFILE)
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        headers, _ = browser_sync.apply_identity_to_url(
            "https://api.example.com/v1/x?q=1", {"User-Agent": "curl/8.0"}, None
        )
        self.assertIn("api_token=zzz", headers["Cookie"])
        self.assertIn("session=abcdef", headers["Cookie"])
        self.assertEqual(headers["User-Agent"], "Mozilla/5.0 TestAgent")

    def test_apply_identity_to_url_no_profile(self):
        headers, body = browser_sync.apply_identity_to_url("http://example.com/", {"User-Agent": "curl/8.0"}, b"ab")
        self.assertEqual(headers, {"User-Agent": "curl/8.0"})
        self.assertEqual(body, b"ab")

    def test_ensure_wiring_starts_receiver_and_proxy_env(self):
        import types

        calls = {}

        class _StubProxy:
            def start(self, port=0, upstream=""):
                calls["start"] = (port, upstream)
                return {"running": True, "host": "127.0.0.1", "port": 12345, "ca_path": "/tmp/ca.pem"}

        stub = types.ModuleType("modules.lazy_proxy")
        stub.get_proxy = lambda: _StubProxy()
        stub.apply_env = lambda ca, host, port: calls.setdefault("env", (ca, host, port))
        (Path(self._tmp.name) / "payload.json").write_text(
            json.dumps({"proxy_autostart": True, "proxy_port": 0, "browser_sync_port": 0})
        )
        browser_sync._PAYLOAD_CACHE.clear()
        import modules

        with patch.dict("sys.modules", {"modules.lazy_proxy": stub}):
            with patch.object(modules, "lazy_proxy", stub, create=True):
                with patch.object(browser_sync, "WIRING_ENABLED", True):
                    result = browser_sync.ensure_wiring()
        self.assertTrue(result["receiver"]["running"])
        self.assertTrue(result["proxy"]["running"])
        self.assertEqual(calls["start"][1], "")
        self.assertEqual(calls["env"], ("/tmp/ca.pem", "127.0.0.1", 12345))

    def test_ensure_wiring_disabled_flag(self):
        with patch.object(browser_sync, "WIRING_ENABLED", False):
            result = browser_sync.ensure_wiring()
        self.assertTrue(result.get("disabled"))
        self.assertFalse(result["receiver"])

    def test_ensure_wiring_payload_ports(self):
        (Path(self._tmp.name) / "payload.json").write_text(
            json.dumps({"browser_sync_enabled": True, "browser_sync_port": 0, "proxy_autostart": False})
        )
        browser_sync._PAYLOAD_CACHE.clear()
        with patch.object(browser_sync, "WIRING_ENABLED", True):
            result = browser_sync.ensure_wiring()
        self.assertTrue(result["receiver"]["running"])
        self.assertFalse(result["proxy"].get("running", False))

    def test_ensure_wiring_default_port_matches_documented_default(self):
        (Path(self._tmp.name) / "payload.json").write_text(json.dumps({"proxy_autostart": False}))
        browser_sync._PAYLOAD_CACHE.clear()
        with patch.object(browser_sync, "WIRING_ENABLED", True):
            result = browser_sync.ensure_wiring()
        self.assertEqual(result["receiver"]["port"], browser_sync.DEFAULT_SYNC_PORT)

    def test_artifacts_mode_0600(self):
        status = browser_sync.start_receiver(port=0)
        code, _ = _post(status["endpoint"], SAMPLE_PROFILE, status["token"])
        self.assertEqual(code, 200)
        self.assertEqual(browser_sync._profile_path().stat().st_mode & 0o777, 0o600)
        self.assertEqual(browser_sync._jar_path().stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
