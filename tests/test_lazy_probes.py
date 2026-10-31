"""BDD tests for the read-only validation command registry."""

from __future__ import annotations

from modules.lazy_probes import (
    CHECK_HTTP_PROBE,
    CHECK_NSE_SCRIPT,
    CHECK_NUCLEI_TEMPLATE,
    CHECK_PACKAGE_VERSION,
    CHECK_SERVICE_STATE,
    CHECK_VERSION_BANNER,
    TARGET_PORT,
    check_errors,
    range_text,
    render_check,
    render_checks,
)


class TestAllowlist:
    def test_unknown_kind_rejected(self):
        story = "an unknown kind fails loudly with the reason"
        result = check_errors("frobnicate", {})
        assert result and "unknown check kind" in result[0], story

    def test_version_banner_needs_port(self):
        story = "the banner check needs a port and a product"
        result = check_errors(CHECK_VERSION_BANNER, {"port": 8080})
        assert any("product" in item for item in result), story

    def test_http_probe_restricts_methods(self):
        story = "the probe method allowlist is enforced"
        result = check_errors(CHECK_HTTP_PROBE, {"method": "DELETE"})
        assert result, story

    def test_http_probe_path_charset(self):
        story = "spaces and control characters never reach the command line"
        result = check_errors(CHECK_HTTP_PROBE, {"path": "/x y"})
        assert result, story

    def test_nuclei_id_grammar(self):
        story = "template ids must match the nuclei id grammar"
        assert not check_errors(CHECK_NUCLEI_TEMPLATE, {"template_id": "CVE-2024-21762"}), story
        assert check_errors(CHECK_NUCLEI_TEMPLATE, {"template_id": "a; rm -rf /"}), story

    def test_package_ecosystem_allowlist(self):
        story = "package ecosystems are allowlisted"
        result = check_errors(CHECK_PACKAGE_VERSION, {"ecosystem": "slapd", "package": "openssh"})
        assert result, story


class TestRender:
    def test_version_banner_renders(self):
        story = "the banner check renders an nmap invocation with the structured expect"
        check = render_check(CHECK_VERSION_BANNER, {
            "port": 8080, "product": "tomcat", "ranges": [{"fixed": "10.0.20"}]
        })
        assert check.errors == [], story
        assert check.read_only is not False, story
        assert f"-p 8080 {TARGET_PORT}" in check.command, story
        assert check.expect["kind"] == "version_in_range", story
        assert "every version before 10.0.20" in check.explain, story

    def test_http_probe_quotes_url(self):
        story = "the probe url is shell-quoted and the expect carries codes"
        check = render_check(CHECK_HTTP_PROBE, {"method": "HEAD", "path": "/foo bar" })
        assert check.errors, story
        check = render_check(CHECK_HTTP_PROBE, {"method": "HEAD", "path": "/admin", "codes": [200, 301]})
        assert check.command.startswith("curl -sS -i -m1 -I"), story
        assert check.expect["codes"] == [200, 301], story

    def test_nuclei_quoting(self):
        story = "the template id rides inside the nuclei invocation shell-safe"
        check = render_check(CHECK_NUCLEI_TEMPLATE, {"template_id": "CVE-2024-21762"})
        assert "nuclei -duc -id CVE-2024-21762 -u <TARGET>" in check.command, story
        evil = render_check(CHECK_NUCLEI_TEMPLATE, {"template_id": "x'; touch /tmp/pwn"})
        assert evil.errors or "'" not in evil.command, story

    def test_nse_script_quoting(self):
        story = "nse scripts are quoted and carry a contains verdict"
        check = render_check(CHECK_NSE_SCRIPT, {"script": "ssl-heartbleed", "port": 443, "contains": "HEARTBEAT"})
        assert "--script ssl-heartbleed" in check.command, story
        assert check.expect["contains"] == "HEARTBEAT", story

    def test_package_version_dpkg(self):
        story = "dpkg renders dpkg-query with a version_lt expect"
        check = render_check(CHECK_PACKAGE_VERSION, {"ecosystem": "dpkg", "package": "openssh-server", "fixed_version": "9.6p1"})
        assert check.command.startswith("dpkg-query -W -f='"), story
        assert check.expect["bound"] == "9.6p1", story

    def test_service_state(self):
        story = "service state renders systemctl with an output_equals verdict"
        check = render_check(CHECK_SERVICE_STATE, {"service": "sshd", "state": "running"})
        assert check.command == "systemctl is-active sshd", story
        assert check.expect == {"kind": "output_equals", "value": "active"}, story

    def test_batch_order_kept(self):
        story = "a batch renders in order with per-item errors"
        rendered = render_checks([
            {"kind": CHECK_SERVICE_STATE, "params": {"service": "sshd", "state": "running"}},
            {"kind": "nope", "params": {}},
        ])
        assert rendered[0].errors == [], story
        assert rendered[1].errors, story

    def test_range_text_phrases(self):
        story = "range bounds read as a human phrase"
        text = range_text([{"introduced": "10.0.0", "fixed": "10.0.20"}, {"last_affected": "9.9.1"}])
        assert "up to but not including 10.0.20" in text, story
        assert "through 9.9.1" in text, story
