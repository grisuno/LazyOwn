"""Tests for the network-bounded bootstrap and the bounded feed fetcher."""

from __future__ import annotations

import sys
import time
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules import (  # noqa: E402
    lazy_cve_feed,
    lazy_exposure,
)


class TestBoundedFetch:
    def test_value_returned_within_deadline(self):
        assert lazy_cve_feed._bounded(lambda: 42, 2.0) == 42

    def test_caller_freed_on_hang(self):
        started = time.monotonic()

        def _hang() -> str:
            time.sleep(3.0)
            return "late"

        result = lazy_cve_feed._bounded(_hang, 0.2)
        elapsed = time.monotonic() - started
        assert result is None
        assert elapsed < 1.5, "the caller must be freed at the deadline, not after the hang"

    def test_error_maps_to_none(self):
        def _boom() -> str:
            raise RuntimeError("x")

        assert lazy_cve_feed._bounded(_boom, 1.0) is None

    def test_osv_query_goes_through_bounded_path(self):
        source = Path(lazy_cve_feed.__file__).read_text(encoding="utf-8")
        assert "_bounded(_query_osv" in source
        assert source.count("urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC)") == 2
        assert "DNS_GRACE_SEC" in source


class TestBootstrapCacheOnly:
    def test_generate_report_forwards_allow_network(self):
        sighting = {
            "ip": "10.0.0.9",
            "state": "scanned",
            "services": {"22": {"port": 22, "name": "openssh", "version": "9.9", "protocol": "tcp"}},
        }
        with mock.patch.object(lazy_exposure.lazy_feedmatch, "live_bindings", return_value=[]) as spy:
            lazy_exposure.generate_report("10.0.0.9", [], sightings=[sighting], allow_network=False)
            assert spy.call_args.kwargs.get("allow_network") is False

    def test_ensure_report_forwards_allow_network(self):
        with mock.patch.object(lazy_exposure, "generate_report") as spy:
            spy.return_value = {"matches": [], "version_unknown": []}
            lazy_exposure.ensure_report("10.0.0.99", refresh=True, allow_network=False)
            assert spy.call_args.kwargs.get("allow_network") is False

    def test_bootstrap_uses_cache_only_report(self):
        from modules import lazy_runner

        source = Path(lazy_runner.__file__).read_text(encoding="utf-8")
        assert "ensure_report(scan_target, allow_network=False)" in source
