"""SSRF guard tests for the lazy burp fuzzer proxy."""

from __future__ import annotations

import http.client
import threading
import unittest
from http.server import HTTPServer

from modules import lazyown_bprfuzzer as bprfuzzer


class ProxyTargetValidationSpec(unittest.TestCase):
    def setUp(self):
        bprfuzzer._PROXY_ALLOWED_HOSTS.clear()
        self.addCleanup(bprfuzzer._PROXY_ALLOWED_HOSTS.clear)

    def test_denies_metadata_endpoint_even_when_listed(self):
        bprfuzzer.configure_proxy_allowlist(["169.254.169.254", "metadata.google.internal"])
        self.assertEqual(bprfuzzer._validated_proxy_target("http://169.254.169.254/latest/meta-data/"), "")
        self.assertEqual(bprfuzzer._validated_proxy_target("http://metadata.google.internal/computeMetadata/v1/"), "")

    def test_denies_hosts_outside_the_allowlist(self):
        bprfuzzer.configure_proxy_allowlist(["app.internal"])
        self.assertEqual(bprfuzzer._validated_proxy_target("http://evil.example/"), "")
        self.assertEqual(bprfuzzer._validated_proxy_target("file:///etc/passwd"), "")

    def test_rebuilds_url_from_the_allowlist_entry(self):
        bprfuzzer.configure_proxy_allowlist(["app.internal"])
        safe = bprfuzzer._validated_proxy_target("http://app.internal:8443/admin?x=1")
        self.assertEqual(safe, "http://app.internal:8443/admin?x=1")

    def test_loopback_requires_explicit_opt_in(self):
        bprfuzzer.configure_proxy_allowlist(["app.internal"])
        previous = bprfuzzer._PROXY_ALLOW_LOOPBACK
        bprfuzzer._PROXY_ALLOW_LOOPBACK = False
        try:
            self.assertEqual(bprfuzzer._validated_proxy_target("http://127.0.0.1:9000/"), "")
            bprfuzzer._PROXY_ALLOW_LOOPBACK = True
            self.assertEqual(bprfuzzer._validated_proxy_target("http://127.0.0.1:9000/"), "http://127.0.0.1:9000/")
        finally:
            bprfuzzer._PROXY_ALLOW_LOOPBACK = previous

    def test_proxy_answers_403_for_disallowed_target(self):
        bprfuzzer.configure_proxy_allowlist(["app.internal"])
        server = HTTPServer(("127.0.0.1", 0), bprfuzzer.ProxyHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        connection = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
        connection.request("GET", "http://169.254.169.254/latest/meta-data/")
        response = connection.getresponse()
        self.assertEqual(response.status, 403)
        connection.close()


if __name__ == "__main__":
    unittest.main()
