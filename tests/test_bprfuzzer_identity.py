"""Contract tests: browser identity inheritance in the lazy burp fuzzer."""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from modules import browser_sync
from modules import lazyown_bprfuzzer as bprfuzzer

SAMPLE_PROFILE = {
    "user_agent": "Mozilla/5.0 FuzzerAgent",
    "languages": ["en-US"],
    "client_hints": {},
    "cookies": [
        {"domain": "127.0.0.1", "name": "session", "value": "fuzz-cookie-1", "path": "/", "hostOnly": True}
    ],
}


class EchoHandler(BaseHTTPRequestHandler):
    """Capture the headers the fuzzer actually sends upstream."""

    captured: dict[str, str] = {}

    def do_GET(self):
        type(self).captured = {
            "cookie": self.headers.get("Cookie", ""),
            "ua": self.headers.get("User-Agent", ""),
        }
        self._reply()

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(length) if length else None
        type(self).captured = {
            "cookie": self.headers.get("Cookie", ""),
            "ua": self.headers.get("User-Agent", ""),
        }
        self._reply()

    def _reply(self):
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        return None


class BprfuzzerIdentitySpec(unittest.TestCase):
    """send_request and the internal proxy handler inherit the synced identity."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name) / "sessions"
        self.addCleanup(self._tmp.cleanup)
        for item in (
            patch.object(browser_sync, "_SESSIONS_DIR", base),
            patch.object(browser_sync, "_PAYLOAD_PATH", Path(self._tmp.name) / "payload.json"),
        ):
            item.start()
            self.addCleanup(item.stop)
        self.addCleanup(browser_sync.clear_profile)
        path = browser_sync._profile_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(SAMPLE_PROFILE))
        browser_sync._PROFILE_CACHE.update({"mtime_ns": 0, "profile": {}})
        self._echo = ThreadingHTTPServer(("127.0.0.1", 0), EchoHandler)
        threading.Thread(target=self._echo.serve_forever, daemon=True).start()
        self.addCleanup(self._echo.shutdown)
        self.echo_url = f"http://127.0.0.1:{self._echo.server_address[1]}/x"

    def test_send_request_inherits_identity(self):
        response = bprfuzzer.send_request(self.echo_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EchoHandler.captured["cookie"], "session=fuzz-cookie-1")
        self.assertEqual(EchoHandler.captured["ua"], "Mozilla/5.0 FuzzerAgent")

    def test_send_request_merge_preserves_operator_headers(self):
        response = bprfuzzer.send_request(
            self.echo_url, headers={"X-Custom": "1", "Cookie": "operator=keepme"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("operator=keepme", EchoHandler.captured["cookie"])
        self.assertIn("session=fuzz-cookie-1", EchoHandler.captured["cookie"])
        self.assertEqual(EchoHandler.captured["ua"], "Mozilla/5.0 FuzzerAgent")

    def test_send_request_body_rules_apply(self):
        rules_path = browser_sync._rules_path()
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text(json.dumps([{"type": "body_replace", "match": "pass=[^&]*", "replace": "pass=x"}]))
        browser_sync._RULES_CACHE.clear()
        response = bprfuzzer.send_request(
            self.echo_url, method="POST", headers={"X-Custom": "1"}, data="user=a&pass=secret"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("pass=x", response.request.body.decode())
        browser_sync._RULES_CACHE.clear()


if __name__ == "__main__":
    unittest.main()
