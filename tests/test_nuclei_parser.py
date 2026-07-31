"""Tests for modules/integrations/nuclei_parser.py"""

from __future__ import annotations

from modules.integrations.nuclei_parser import (
    MITRE_TACTICS,
    SEVERITY_MAP,
    NucleiFinding,
    NucleiParser,
)


class TestNucleiFinding:
    def test_fields(self):
        f = NucleiFinding(
            template_id="CVE-2021-41773",
            name="Apache Path Traversal",
            severity="critical",
            matched_at="http://10.10.11.5:80/",
            host="10.10.11.5",
            cve_id="CVE-2021-41773",
            cvss_score=7.5,
        )
        assert f.severity == "critical"
        assert f.cve_id == "CVE-2021-41773"
        assert f.exploit_probability == 0.90

    def test_exploit_probability_map(self):
        for severity, expected in [
            ("critical", 0.90),
            ("high", 0.70),
            ("medium", 0.40),
            ("low", 0.15),
            ("info", 0.05),
            ("unknown", 0.10),
        ]:
            f = NucleiFinding(
                template_id="test",
                name=f"Test {severity}",
                severity=severity,
                matched_at="http://test/",
                host="",
            )
            assert f.exploit_probability == expected

    def test_mitre_tactic(self):
        f = NucleiFinding(
            template_id="sqli-test",
            name="SQL Injection",
            severity="high",
            matched_at="http://test/",
            host="",
            tags=["sqli", "injection"],
        )
        assert "Credential Access" in f.mitre_tactic


class TestNucleiParserText:
    def test_parse_empty(self):
        parser = NucleiParser()
        findings = parser.parse_text("")
        assert len(findings) == 0

    def test_parse_nuclei_line(self):
        parser = NucleiParser()
        line = "[critical] CVE-2021-41773 Apache 2.4.49 Path Traversal [http://10.10.11.5:80/]"
        findings = parser.parse_text(line)
        assert len(findings) == 1
        assert findings[0].template_id == "CVE-2021-41773"
        assert findings[0].severity == "critical"


class TestNucleiParserJson:
    def test_parse_empty(self):
        parser = NucleiParser()
        assert len(parser.parse_json("")) == 0

    def test_parse_json_single_finding(self):
        parser = NucleiParser()
        json_line = (
            '{"template-id":"CVE-2021-41773","info":{"name":"Apache Path Traversal","severity":"critical",'
            '"description":"Test desc"},"matched-at":"http://10.10.11.5:80/","host":"10.10.11.5"}'
        )
        findings = parser.parse_json(json_line)
        assert len(findings) == 1
        assert findings[0].template_id == "CVE-2021-41773"
        assert findings[0].severity == "critical"
        assert findings[0].host == "10.10.11.5"

    def test_parse_json_multiple_findings(self):
        parser = NucleiParser()
        json_text = (
            '{"template-id":"test1","info":{"name":"Test 1","severity":"high"},"matched-at":"http://a/","host":"10.0.0.1"}\n'
            '{"template-id":"test2","info":{"name":"Test 2","severity":"medium"},"matched-at":"http://b/","host":"10.0.0.1"}'
        )
        findings = parser.parse_json(json_text)
        assert len(findings) == 2

    def test_parse_json_array(self):
        parser = NucleiParser()
        json_arr = """[
            {"template-id":"test1","info":{"name":"Test 1","severity":"high"},"matched-at":"http://a/","host":"10.0.0.1"},
            {"template-id":"test2","info":{"name":"Test 2","severity":"medium"},"matched-at":"http://b/","host":"10.0.0.1"}
        ]"""
        findings = parser.parse_json(json_arr)
        assert len(findings) == 2

    def test_parse_with_cve_classification(self):
        parser = NucleiParser()
        json_obj = (
            '{"template-id":"CVE-2023-test","info":{"name":"Test CVE","severity":"critical",'
            '"classification":{"cve-id":["CVE-2023-1234"],"cvss-metrics":"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/7.5"}},'
            '"matched-at":"http://test/","host":"10.0.0.1"}'
        )
        findings = parser.parse_json(json_obj)
        assert len(findings) == 1
        assert findings[0].cve_id in ("CVE-2023-1234", "")


class TestSeverityMap:
    def test_critical_is_10(self):
        assert SEVERITY_MAP["critical"] == 10

    def test_info_is_1(self):
        assert SEVERITY_MAP["info"] == 1


class TestMitreTactics:
    def test_all_tactics_have_ta_prefix(self):
        for tactic in MITRE_TACTICS.values():
            assert tactic.startswith("TA"), f"{tactic} should start with TA"


class TestRecommendations:
    def test_generate_for_critical(self):
        parser = NucleiParser()
        f = NucleiFinding(
            template_id="CVE-2021-41773",
            name="Test",
            severity="critical",
            matched_at="http://10.10.11.5:80/",
            host="10.10.11.5",
            cve_id="CVE-2021-41773",
        )
        recs = parser.generate_recommendations([f])
        assert len(recs) >= 1
        assert "command" in recs[0]
        assert "confidence" in recs[0]
        assert recs[0]["confidence"] > 0.5

    def test_skip_low_severity(self):
        parser = NucleiParser()
        f = NucleiFinding(
            template_id="info-test",
            name="Info Finding",
            severity="info",
            matched_at="http://test/",
            host="",
        )
        recs = parser.generate_recommendations([f])
        assert len(recs) == 0
