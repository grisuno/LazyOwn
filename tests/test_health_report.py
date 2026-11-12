"""Tests for the health report assembly of the LazyOwn C2.

Covers both the remote (aggregated-only) and local/operator (detailed)
responses, including the regression where a remote caller received a 500
instead of a valid aggregated status.
"""

from __future__ import annotations

import pytest
from flask import Flask, jsonify, request

from lazyc2.security.health import build_health_report, gather_health


def _on_error_silent(name: str, exc: BaseException) -> None:
    return None


class TestGatherHealth:
    def test_probe_failure_is_reported_not_raised(self) -> None:
        def _boom() -> str:
            raise RuntimeError("sessions dir gone")

        seen = []
        checks = gather_health(
            (("sessions_dir", _boom), ("database", lambda: "ok")),
            on_error=lambda name, exc: seen.append((name, exc)),
        )
        assert checks == {"sessions_dir": "error", "database": "ok"}
        assert seen and seen[0][0] == "sessions_dir"

    def test_empty_probe_result_defaults_to_ok(self) -> None:
        checks = gather_health((("sessions_dir", lambda: None),))
        assert checks == {"sessions_dir": "ok"}


class TestBuildHealthReport:
    def test_remote_caller_gets_aggregated_status_without_checks(self) -> None:
        report, code = build_health_report({"database": "ok"}, detailed=False)
        assert code == 200
        assert report == {"status": "healthy"}
        assert "checks" not in report
        assert "daemon" not in report

    def test_remote_unhealthy_keeps_503_and_hides_checks(self) -> None:
        report, code = build_health_report({"database": "error"}, detailed=False)
        assert code == 503
        assert report == {"status": "unhealthy"}
        assert "checks" not in report

    def test_detailed_caller_gets_checks_and_daemon(self) -> None:
        report, code = build_health_report(
            {"database": "ok", "autonomous_daemon": "stopped"},
            detailed=True,
            daemon_status={"pid": 4242},
        )
        assert code == 503
        assert report["status"] == "unhealthy"
        assert report["checks"] == {"database": "ok", "autonomous_daemon": "stopped"}
        assert report["daemon"] == {"pid": 4242}

    def test_detailed_unhealthy_includes_checks_with_503(self) -> None:
        report, code = build_health_report({"sessions_dir": "error"}, detailed=True)
        assert code == 503
        assert report["status"] == "unhealthy"
        assert report["checks"] == {"sessions_dir": "error"}


class TestRouteLevelRemoteBehavior:
    def _app(self):
        app = Flask(__name__)

        @app.route("/health")
        def health():
            detailed = request.remote_addr in {"127.0.0.1", "::1", "localhost"}
            checks = gather_health(
                (("database", lambda: "ok"), ("sessions_dir", lambda: "ok")),
                on_error=_on_error_silent,
            )
            report, code = build_health_report(checks, detailed=detailed)
            return jsonify(report), code

        return app

    def test_remote_addr_returns_200_aggregated(self) -> None:
        client = self._app().test_client()
        response = client.get("/health", environ_base={"REMOTE_ADDR": "203.0.113.9"})
        assert response.status_code == 200
        assert response.get_json() == {"status": "healthy"}

    def test_loopback_addr_gets_detail(self) -> None:
        client = self._app().test_client()
        response = client.get("/health", environ_base={"REMOTE_ADDR": "127.0.0.1"})
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["checks"] == {"database": "ok", "sessions_dir": "ok"}


class TestLazyC2Wiring:
    def test_health_route_uses_report_builder_not_pop(self) -> None:
        src = open("lazyc2.py", encoding="utf-8").read()
        health = src.split("def health_check():", 1)[1].split("\ndef ", 1)[0]
        assert "_build_health_report" in health
        assert "_gather_health" in health
        assert ".pop(" not in health
        assert '_is_local_request' in health


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
